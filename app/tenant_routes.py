from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.deps import get_tenant_from_token
from app.quota_service import get_usage, current_year_month
from app.redis_client import redis_client
from app.database import get_db
from app.models import Tenant
from app.schemas import TenantRegister, TenantLogin
from app.security import hash_password, verify_password, generate_api_keys, create_tenant_token


router = APIRouter(prefix="/tenant", tags=["Tenant"])

@router.post("/register")
async def register_tenant(payload: TenantRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tenant).where(Tenant.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail={"code": "EMAIL_TAKEN", "message": "Email sudah terdaftar"})

    secret_key, public_key = generate_api_keys()
    tenant = Tenant(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        secret_key=secret_key,
        public_key=public_key,
    )
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)

    return {
        "success": True,
        "data": {
            "id": str(tenant.id),
            "name": tenant.name,
            "email": tenant.email,
            "secret_key": tenant.secret_key,
            "public_key": tenant.public_key,
        },
        "meta": {"note": "Simpan secret_key sekarang, tidak akan ditampilkan lagi secara penuh setelah ini"},
    }

@router.post("/login")
async def login_tenant(payload: TenantLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tenant).where(Tenant.email == payload.email))
    tenant = result.scalar_one_or_none()
    if not tenant or not verify_password(payload.password, tenant.password_hash):
        raise HTTPException(status_code=401, detail={"code": "INVALID_CREDENTIALS", "message": "Email atau password salah"})

    if not tenant.is_active:
        raise HTTPException(status_code=403, detail={"code": "TENANT_DISABLED", "message": "Akun tenant dinonaktifkan"})

    token = create_tenant_token(tenant.id)

    return {
        "success": True,
        "data": {
            "id": str(tenant.id),
            "name": tenant.name,
            "email": tenant.email,
            "token": token,
        },
        "meta": {"expires_in_hours": 8},
    }
    
@router.get("/dashboard")
async def tenant_dashboard(tenant: Tenant = Depends(get_tenant_from_token), db: AsyncSession = Depends(get_db)):
    from app.models import User
    from sqlalchemy import select, func

    total_users = await db.execute(select(func.count(User.id)).where(User.tenant_id == tenant.id))
    usage = await get_usage(tenant.id)

    return {
        "success": True,
        "data": {
            "tenant": {"id": str(tenant.id), "name": tenant.name, "email": tenant.email, "plan": tenant.plan},
            "api_keys": {
                "secret_key_preview": tenant.secret_key[:14] + "..." + tenant.secret_key[-4:],
                "public_key": tenant.public_key,
            },
            "usage": {
                "period": current_year_month(),
                "requests_used": usage,
                "requests_quota": tenant.monthly_quota,
                "percentage": round((usage / tenant.monthly_quota) * 100, 2) if tenant.monthly_quota else 0,
            },
            "total_users": total_users.scalar() or 0,
        },
        "meta": None,
    }

@router.post("/regenerate-keys")
async def regenerate_keys(tenant: Tenant = Depends(get_tenant_from_token), db: AsyncSession = Depends(get_db)):
    secret_key, public_key = generate_api_keys()
    tenant.secret_key = secret_key
    tenant.public_key = public_key
    await db.commit()

    return {
        "success": True,
        "data": {"secret_key": secret_key, "public_key": public_key},
        "meta": {"note": "Key lama langsung tidak berlaku. Simpan secret_key sekarang, tidak akan ditampilkan lagi secara penuh."},
    }

@router.post("/logout")
async def tenant_logout(authorization: str = Header(...)):
    from app.security import decode_tenant_token
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_tenant_token(token)
        jti = payload.get("jti")
        exp = payload.get("exp")
        if jti and exp:
            ttl = max(int(exp - datetime.now(timezone.utc).timestamp()), 1)
            await redis_client.setex(f"tenant_blacklist:{jti}", ttl, "1")
    except ValueError:
        pass
    return {"success": True, "data": {"logged_out": True}, "meta": None}