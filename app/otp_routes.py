import secrets
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Tenant, User
from app.deps import get_tenant_from_key, check_ip_blocked
from app.redis_client import redis_client
from app.email_service import send_email
from app.sms_service import send_sms
from app.rate_limit import rate_limit_by_key
from app.security import create_access_token
from app.config import settings
from app.auth_routes import issue_token_pair
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Passwordless"])

class MagicLinkRequest(BaseModel):
    email: EmailStr

class MagicLinkVerify(BaseModel):
    token: str

class OtpRequest(BaseModel):
    phone: str

class OtpVerify(BaseModel):
    phone: str
    code: str

async def get_or_create_user(db: AsyncSession, tenant_id, email: str | None = None, phone: str | None = None):
    query = select(User).where(User.tenant_id == tenant_id)
    query = query.where(User.email == email) if email else query.where(User.phone == phone)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        user = User(tenant_id=tenant_id, email=email or f"{uuid.uuid4()}@no-email.local", phone=phone, is_email_verified=bool(email))
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user

@router.post("/magic-link/request")
async def request_magic_link(payload: MagicLinkRequest, request: Request, tenant: Tenant = Depends(get_tenant_from_key)):
    await rate_limit_by_key("magic_link", f"{tenant.id}:{payload.email}", limit=3, window_seconds=300)

    token = secrets.token_urlsafe(32)
    await redis_client.setex(f"magiclink:{tenant.id}:{token}", 900, payload.email)

    link = f"{settings.frontend_url}/magic-login?token={token}"
    result = await send_email(payload.email, "magic_link", {"link": link})

    return {"success": True, "data": {"delivery": result}, "meta": None}

@router.post("/magic-link/verify")
async def verify_magic_link(payload: MagicLinkVerify, tenant: Tenant = Depends(get_tenant_from_key), db: AsyncSession = Depends(get_db)):
    key = f"magiclink:{tenant.id}:{payload.token}"
    email = await redis_client.get(key)
    if not email:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Link tidak valid atau kadaluarsa"})

    await redis_client.delete(key)
    user = await get_or_create_user(db, tenant.id, email=email)
    tokens = await issue_token_pair(db, user, tenant.id)

    return {"success": True, "data": {"user": {"id": str(user.id), "email": user.email}, "tokens": tokens}, "meta": None}

@router.post("/otp/request")
async def request_otp(payload: OtpRequest, tenant: Tenant = Depends(get_tenant_from_key)):
    await rate_limit_by_key("otp", f"{tenant.id}:{payload.phone}", limit=3, window_seconds=300)

    code = f"{secrets.randbelow(1000000):06d}"
    await redis_client.setex(f"otp:{tenant.id}:{payload.phone}", 300, code)

    result = await send_sms(payload.phone, f"Kode OTP kamu: {code}. Berlaku 5 menit.")

    return {"success": True, "data": {"delivery": result}, "meta": None}

@router.post("/otp/verify")
async def verify_otp(payload: OtpVerify, tenant: Tenant = Depends(get_tenant_from_key), db: AsyncSession = Depends(get_db)):
    key = f"otp:{tenant.id}:{payload.phone}"
    stored_code = await redis_client.get(key)
    if not stored_code or stored_code != payload.code:
        raise HTTPException(status_code=401, detail={"code": "INVALID_OTP", "message": "Kode OTP salah atau kadaluarsa"})

    await redis_client.delete(key)
    user = await get_or_create_user(db, tenant.id, phone=payload.phone)
    tokens = await issue_token_pair(db, user, tenant.id)

    return {"success": True, "data": {"user": {"id": str(user.id), "phone": user.phone}, "tokens": tokens}, "meta": None}

@router.post("/anonymous")
async def anonymous_login(tenant: Tenant = Depends(get_tenant_from_key), db: AsyncSession = Depends(get_db)):
    user = User(tenant_id=tenant.id, email=f"anon-{uuid.uuid4()}@anonymous.local", is_anonymous=True, is_email_verified=False)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    tokens = await issue_token_pair(db, user, tenant.id)

    return {"success": True, "data": {"user": {"id": str(user.id), "is_anonymous": True}, "tokens": tokens}, "meta": None}