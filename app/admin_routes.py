from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.database import get_db
from app.models import User, Tenant, IpRule, ActivityLog
from app.security import verify_password, create_admin_token, decode_admin_token
from app.redis_client import redis_client
from app.config import settings

router = APIRouter(prefix="/admin", tags=["Admin"])

class AdminLogin(BaseModel):
    email: str
    password: str

async def require_admin(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "Token admin tidak ditemukan"})
    token = authorization.split(" ", 1)[1]

    try:
        payload = decode_admin_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Token admin tidak valid atau kadaluarsa"})

    jti = payload.get("jti")
    if jti and await redis_client.get(f"admin_blacklist:{jti}"):
        raise HTTPException(status_code=401, detail={"code": "TOKEN_REVOKED", "message": "Token admin telah di-revoke"})

    return True

@router.post("/login")
async def admin_login(payload: AdminLogin):
    if payload.email != settings.admin_email or not verify_password(payload.password, settings.admin_password_hash):
        raise HTTPException(status_code=401, detail={"code": "INVALID_CREDENTIALS", "message": "Kredensial admin salah"})
    token = create_admin_token()
    return {"success": True, "data": {"token": token, "expires_in_hours": 8}, "meta": None}

@router.post("/logout")
async def admin_logout(authorization: str = Header(...)):
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_admin_token(token)
        jti = payload.get("jti")
        exp = payload.get("exp")
        if jti and exp:
            ttl = max(int(exp - datetime.now(timezone.utc).timestamp()), 1)
            await redis_client.setex(f"admin_blacklist:{jti}", ttl, "1")
    except ValueError:
        pass
    return {"success": True, "data": {"logged_out": True}, "meta": None}

@router.get("/users")
async def list_users(tenant_id: str | None = None, page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    query = select(User)
    if tenant_id:
        query = query.where(User.tenant_id == tenant_id)
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()

    return {
        "success": True,
        "data": {"users": [{"id": str(u.id), "email": u.email, "is_active": u.is_active, "is_email_verified": u.is_email_verified} for u in users]},
        "meta": {"page": page, "limit": limit},
    }

@router.post("/users/{user_id}/block")
async def block_user(user_id: str, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail={"code": "USER_NOT_FOUND", "message": "User tidak ditemukan"})
    user.is_active = False
    await db.commit()
    return {"success": True, "data": {"blocked": True}, "meta": None}

@router.post("/users/{user_id}/unblock")
async def unblock_user(user_id: str, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail={"code": "USER_NOT_FOUND", "message": "User tidak ditemukan"})
    user.is_active = True
    user.locked_until = None
    user.failed_login_attempts = 0
    await db.commit()
    return {"success": True, "data": {"unblocked": True}, "meta": None}

@router.post("/users/{user_id}/reset-mfa")
async def reset_mfa(user_id: str, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail={"code": "USER_NOT_FOUND", "message": "User tidak ditemukan"})
    user.totp_secret = None
    user.totp_enabled = False
    await db.commit()
    return {"success": True, "data": {"mfa_reset": True}, "meta": None}

@router.get("/tenants")
async def list_tenants(db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(Tenant))
    tenants = result.scalars().all()
    return {"success": True, "data": {"tenants": [{"id": str(t.id), "name": t.name, "email": t.email, "is_active": t.is_active} for t in tenants]}, "meta": None}

@router.get("/ip-rules")
async def list_ip_rules(db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(IpRule))
    rules = result.scalars().all()
    return {"success": True, "data": {"rules": [{"id": str(r.id), "ip_address": r.ip_address, "rule_type": r.rule_type, "reason": r.reason} for r in rules]}, "meta": None}

class IpRuleCreate(BaseModel):
    tenant_id: str
    ip_address: str
    rule_type: str
    reason: str | None = None

@router.post("/ip-rules")
async def create_ip_rule(payload: IpRuleCreate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    rule = IpRule(**payload.model_dump())
    db.add(rule)
    await db.commit()
    return {"success": True, "data": {"created": True}, "meta": None}

@router.delete("/ip-rules/{rule_id}")
async def delete_ip_rule(rule_id: str, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    result = await db.execute(select(IpRule).where(IpRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if rule:
        await db.delete(rule)
        await db.commit()
    return {"success": True, "data": {"deleted": True}, "meta": None}

@router.get("/logs")
async def list_logs(user_id: str | None = None, limit: int = 50, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    query = select(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(limit)
    if user_id:
        query = query.where(ActivityLog.user_id == user_id)
    result = await db.execute(query)
    logs = result.scalars().all()
    return {
        "success": True,
        "data": {"logs": [{"action": l.action, "user_id": str(l.user_id) if l.user_id else None, "ip_address": l.ip_address, "detail": l.detail, "created_at": l.created_at.isoformat()} for l in logs]},
        "meta": None,
    }