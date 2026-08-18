import uuid
from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from sqlalchemy import select, update
from app.database import get_db
from app.models import Tenant, User, IpRule, RefreshToken
from app.security import decode_access_token
from app.redis_client import redis_client

async def get_tenant_from_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: AsyncSession = Depends(get_db),
) -> Tenant:
    result = await db.execute(select(Tenant).where(Tenant.secret_key == x_api_key, Tenant.is_active == True))
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=401, detail={"code": "INVALID_API_KEY", "message": "API key tidak valid"})

    from app.quota_service import increment_usage, check_quota
    await check_quota(tenant.id, tenant.monthly_quota)
    await increment_usage(tenant.id)

    return tenant

async def get_current_user(
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "Token tidak ditemukan"})
    token = authorization.split(" ", 1)[1]

    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Token tidak valid atau kadaluarsa"})

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Token bukan access token"})

    jti = payload.get("jti")
    if jti and await redis_client.get(f"blacklist:{jti}"):
        raise HTTPException(status_code=401, detail={"code": "TOKEN_REVOKED", "message": "Token telah di-revoke"})

    user_id = uuid.UUID(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id, User.is_active == True))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail={"code": "USER_NOT_FOUND", "message": "User tidak ditemukan"})

    await touch_last_active(db, user.id, payload.get("session_id"))
    return user
    
async def check_ip_blocked(request, db):
    ip = request.client.host if request.client else "unknown"
    result = await db.execute(select(IpRule).where(IpRule.ip_address == ip, IpRule.rule_type == "blacklist"))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail={"code": "IP_BLOCKED", "message": "IP kamu telah diblokir"})
    return ip
    
async def touch_last_active(db: AsyncSession, user_id, session_id: str | None):
    if not session_id:
        return
    throttle_key = f"active_throttle:{session_id}"
    if await redis_client.get(throttle_key):
        return
    await redis_client.setex(throttle_key, 60, "1")

    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.id == session_id, RefreshToken.is_revoked == False)
        .values(last_active_at=datetime.now(timezone.utc))
    )
    await db.commit()
    
async def get_tenant_from_token(
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db),
) -> Tenant:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "Token tidak ditemukan"})
    token = authorization.split(" ", 1)[1]

    from app.security import decode_tenant_token
    try:
        payload = decode_tenant_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Token tidak valid atau kadaluarsa"})

    jti = payload.get("jti")
    if jti and await redis_client.get(f"tenant_blacklist:{jti}"):
        raise HTTPException(status_code=401, detail={"code": "TOKEN_REVOKED", "message": "Token telah di-revoke"})

    tenant_id = uuid.UUID(payload["sub"])
    result = await db.execute(select(Tenant).where(Tenant.id == tenant_id, Tenant.is_active == True))
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=401, detail={"code": "TENANT_NOT_FOUND", "message": "Tenant tidak ditemukan"})
    return tenant
