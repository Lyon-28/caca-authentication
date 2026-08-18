import secrets
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.device_service import parse_device, get_device_type
from app.location_service import get_location_from_ip
from app.email_service import send_email
from app.audit_service import detect_suspicious_login
from app.redis_client import redis_client
from app.cache_service import cache_get, cache_set, cache_invalidate, user_cache_key
from app.rate_limit import rate_limit_by_ip, rate_limit_by_key
from app.database import get_db
from app.models import Tenant, User, RefreshToken, IpRule
from app.schemas import UserRegister, UserLogin
from app.security import (
    hash_password, verify_password, create_access_token,
    create_refresh_token, hash_token, decode_access_token,
)
from app.deps import get_tenant_from_key, get_current_user, check_ip_blocked
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

async def issue_token_pair(db: AsyncSession, user: User, tenant_id, request: Request | None = None):
    refresh_token = create_refresh_token()
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)

    ip_address = None
    device_name = None
    location = None
    if request is not None:
        ip_address = request.client.host if request.client else None
        device_name = parse_device(request.headers.get("user-agent", ""))
        location = await get_location_from_ip(ip_address) if ip_address else None

    device_type = None
    if request is not None:
        device_type = get_device_type(request.headers.get("user-agent", ""))

    session = RefreshToken(
        user_id=user.id,
        tenant_id=tenant_id,
        token_hash=hash_token(refresh_token),
        expires_at=expires_at,
        ip_address=ip_address,
        device_name=device_name,
        device_type=device_type,
        location=location,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    access_token = create_access_token(user.id, tenant_id, session.id)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(
    payload: UserRegister,
    request: Request,
    tenant: Tenant = Depends(get_tenant_from_key),
    db: AsyncSession = Depends(get_db),
):
    await rate_limit_by_ip(request, "register", limit=10, window_seconds=300)

    result = await db.execute(select(User).where(User.email == payload.email, User.tenant_id == tenant.id))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail={"code": "EMAIL_TAKEN", "message": "Email sudah terdaftar"})

    user = User(
        tenant_id=tenant.id,
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_email_verified=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    tokens = await issue_token_pair(db, user, tenant.id, request)

    verify_token = secrets.token_urlsafe(32)
    await redis_client.setex(f"verify_email:{tenant.id}:{verify_token}", 86400, str(user.id))
    verify_link = f"{settings.frontend_url}/verify-email?token={verify_token}"
    delivery = await send_email(user.email, "verify_email", {"link": verify_link})

    return {
        "success": True,
        "data": {
            "user": {"id": str(user.id), "email": user.email, "is_email_verified": user.is_email_verified},
            "tokens": tokens,
        },
        "meta": {"verification_email": delivery},
    }

@router.post("/login")
async def login_user(
    payload: UserLogin,
    request: Request,
    tenant: Tenant = Depends(get_tenant_from_key),
    db: AsyncSession = Depends(get_db),
):
    await check_ip_blocked(request, db)
    await rate_limit_by_ip(request, "login", limit=15, window_seconds=300)
    await rate_limit_by_key("login_email", f"{tenant.id}:{payload.email}", limit=8, window_seconds=300)

    result = await db.execute(select(User).where(User.email == payload.email, User.tenant_id == tenant.id))
    user = result.scalar_one_or_none()

    if user and user.locked_until and user.locked_until > datetime.now(timezone.utc):
        raise HTTPException(status_code=403, detail={"code": "ACCOUNT_LOCKED", "message": "Akun terkunci sementara, verifikasi email atau hubungi admin"})

    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        if user:
            user.failed_login_attempts += 1
            if user.failed_login_attempts == 3:
                await send_email(user.email, "suspicious_activity", {"detail": "Terdeteksi 3x percobaan login gagal beruntun pada akun kamu."})
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=30)
                await send_email(user.email, "suspicious_activity", {"detail": "Akun dikunci karena 5x percobaan login gagal beruntun."})
            await db.commit()

            ip = request.client.host if request.client else "unknown"
            fail_key = f"failban:{ip}"
            fails = await redis_client.incr(fail_key)
            await redis_client.expire(fail_key, 600)
            if fails >= 20:
                db.add(IpRule(tenant_id=tenant.id, ip_address=ip, rule_type="blacklist", reason="Terlalu banyak login gagal"))
                await db.commit()

        raise HTTPException(status_code=401, detail={"code": "INVALID_CREDENTIALS", "message": "Email atau password salah"})

    if not user.is_active:
        raise HTTPException(status_code=403, detail={"code": "ACCOUNT_DISABLED", "message": "Akun dinonaktifkan"})

    is_new_device = user.failed_login_attempts > 0 or not await db.execute(
        select(RefreshToken).where(RefreshToken.user_id == user.id, RefreshToken.ip_address == (request.client.host if request.client else None))
    )
    user.failed_login_attempts = 0
    user.locked_until = None
    await db.commit()

    tokens = await issue_token_pair(db, user, tenant.id, request)

    current_location = await get_location_from_ip(request.client.host if request.client else "")
    current_device = parse_device(request.headers.get("user-agent", ""))
    current_hour = datetime.now(timezone.utc).hour

    await detect_suspicious_login(db, user, current_location, current_device, current_hour)

    return {
        "success": True,
        "data": {
            "user": {"id": str(user.id), "email": user.email, "is_email_verified": user.is_email_verified},
            "tokens": tokens,
        },
        "meta": None,
    }

@router.post("/refresh")
async def refresh_token_endpoint(
    refresh_token: str,
    tenant: Tenant = Depends(get_tenant_from_key),
    db: AsyncSession = Depends(get_db),
):
    token_hash = hash_token(refresh_token)
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash, RefreshToken.tenant_id == tenant.id))
    stored = result.scalar_one_or_none()

    if not stored or stored.is_revoked or stored.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail={"code": "INVALID_REFRESH_TOKEN", "message": "Refresh token tidak valid atau kadaluarsa"})

    result = await db.execute(select(User).where(User.id == stored.user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail={"code": "USER_NOT_FOUND", "message": "User tidak ditemukan"})

    stored.is_revoked = True
    tokens = await issue_token_pair(db, user, tenant.id)

    return {"success": True, "data": {"tokens": tokens}, "meta": None}

@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    cache_key = user_cache_key(user.id)
    cached = await cache_get(cache_key)
    if cached:
        return {"success": True, "data": cached, "meta": {"cache": "hit"}}

    data = {
        "id": str(user.id),
        "email": user.email,
        "is_email_verified": user.is_email_verified,
        "is_active": user.is_active,
    }
    await cache_set(cache_key, data, ttl_seconds=120)

    return {"success": True, "data": data, "meta": {"cache": "miss"}}
    
class VerifyEmailRequest(BaseModel):
    token: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v):
        from app.schemas import validate_password_strength
        return validate_password_strength(v)

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v):
        from app.schemas import validate_password_strength
        return validate_password_strength(v)

@router.post("/verify-email")
async def verify_email(payload: VerifyEmailRequest, tenant: Tenant = Depends(get_tenant_from_key), db: AsyncSession = Depends(get_db)):
    key = f"verify_email:{tenant.id}:{payload.token}"
    user_id = await redis_client.get(key)
    if not user_id:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Token tidak valid atau kadaluarsa"})

    await redis_client.delete(key)
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail={"code": "USER_NOT_FOUND", "message": "User tidak ditemukan"})

    user.is_email_verified = True
    user.locked_until = None
    await db.commit()
    await cache_invalidate(user_cache_key(user.id))

    return {"success": True, "data": {"verified": True}, "meta": None}

@router.post("/resend-verification")
async def resend_verification(payload: ForgotPasswordRequest, tenant: Tenant = Depends(get_tenant_from_key), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email, User.tenant_id == tenant.id))
    user = result.scalar_one_or_none()
    if not user or user.is_email_verified:
        return {"success": True, "data": {"sent": True}, "meta": None}

    verify_token = secrets.token_urlsafe(32)
    await redis_client.setex(f"verify_email:{tenant.id}:{verify_token}", 86400, str(user.id))
    verify_link = f"{settings.frontend_url}/verify-email?token={verify_token}"
    delivery = await send_email(user.email, "verify_email", {"link": verify_link})

    return {"success": True, "data": {"delivery": delivery}, "meta": None}

@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordRequest, tenant: Tenant = Depends(get_tenant_from_key), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email, User.tenant_id == tenant.id))
    user = result.scalar_one_or_none()
    if not user:
        return {"success": True, "data": {"sent": True}, "meta": None}

    reset_token = secrets.token_urlsafe(32)
    await redis_client.setex(f"reset_pw:{tenant.id}:{reset_token}", 3600, str(user.id))
    reset_link = f"{settings.frontend_url}/reset-password?token={reset_token}"
    delivery = await send_email(user.email, "reset_password", {"link": reset_link})

    return {"success": True, "data": {"delivery": delivery}, "meta": None}

@router.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest, tenant: Tenant = Depends(get_tenant_from_key), db: AsyncSession = Depends(get_db)):
    key = f"reset_pw:{tenant.id}:{payload.token}"
    user_id = await redis_client.get(key)
    if not user_id:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Token tidak valid atau kadaluarsa"})

    await redis_client.delete(key)
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail={"code": "USER_NOT_FOUND", "message": "User tidak ditemukan"})
    
    user.password_hash = hash_password(payload.new_password)
    await db.commit()
    await cache_invalidate(user_cache_key(user.id))
    await send_email(user.email, "password_changed", {})

    return {"success": True, "data": {"reset": True}, "meta": None}

@router.post("/change-password")
async def change_password(payload: ChangePasswordRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user.is_email_verified:
        raise HTTPException(status_code=403, detail={"code": "EMAIL_NOT_VERIFIED", "message": "Verifikasi email diperlukan untuk mengubah password"})

    if not user.password_hash or not verify_password(payload.old_password, user.password_hash):
        raise HTTPException(status_code=401, detail={"code": "INVALID_PASSWORD", "message": "Password lama salah"})

    user.password_hash = hash_password(payload.new_password)
    await db.commit()
    await cache_invalidate(user_cache_key(user.id))
    await send_email(user.email, "password_changed", {})

    return {"success": True, "data": {"changed": True}, "meta": None}