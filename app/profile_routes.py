import secrets
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models import User, UserPreference, EmailChangeRequest
from app.deps import get_current_user
from app.storage_service import upload_file, delete_file
from app.email_service import send_email
from app.cache_service import cache_invalidate, user_cache_key
from app.redis_client import redis_client
from app.config import settings

router = APIRouter(prefix="/profile", tags=["Profile"])

MIN_AVATAR_SIZE = 500 * 1024
MAX_AVATAR_SIZE = 5 * 1024 * 1024
MAX_DOC_SIZE = 10 * 1024 * 1024

class ProfileUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None
    birth_date: str | None = None

class PreferencesUpdate(BaseModel):
    language: str | None = None
    timezone: str | None = None
    notifications_enabled: bool | None = None
    privacy_profile_public: bool | None = None

class ChangeEmailRequest(BaseModel):
    new_email: EmailStr

class ChangeEmailConfirm(BaseModel):
    token: str

@router.patch("")
async def update_profile(payload: ProfileUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if payload.name is not None:
        user.name = payload.name
    if payload.bio is not None:
        user.bio = payload.bio
    if payload.birth_date is not None:
        user.birth_date = payload.birth_date
    await db.commit()
    await cache_invalidate(user_cache_key(user.id))

    return {"success": True, "data": {"id": str(user.id), "name": user.name, "bio": user.bio, "birth_date": user.birth_date}, "meta": None}

@router.post("/avatar")
async def upload_avatar(file: UploadFile = File(...), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    content = await file.read()
    size = len(content)

    if size < MIN_AVATAR_SIZE or size > MAX_AVATAR_SIZE:
        raise HTTPException(status_code=400, detail={"code": "INVALID_FILE_SIZE", "message": "Ukuran avatar harus antara 500KB - 5MB"})

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail={"code": "INVALID_FILE_TYPE", "message": "File harus berupa gambar"})

    from PIL import Image
    import io
    img = Image.open(io.BytesIO(content))
    img.thumbnail((512, 512))
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=85, optimize=True)
    optimized = buf.getvalue()

    old_avatar_url = user.avatar_url
    url = await upload_file(optimized, f"avatar-{user.id}.jpg", "image/jpeg")

    user.avatar_url = url
    await db.commit()
    await cache_invalidate(user_cache_key(user.id))

    if old_avatar_url:
        await delete_file(old_avatar_url)

    return {"success": True, "data": {"avatar_url": url}, "meta": None}

@router.delete("/avatar")
async def delete_avatar(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    old_url = user.avatar_url
    user.avatar_url = None
    await db.commit()
    await cache_invalidate(user_cache_key(user.id))

    if old_url:
        await delete_file(old_url)

    return {"success": True, "data": {"deleted": True}, "meta": None}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    content = await file.read()
    if len(content) > MAX_DOC_SIZE:
        raise HTTPException(status_code=400, detail={"code": "FILE_TOO_LARGE", "message": "Ukuran file maksimal 10MB"})

    url = await upload_file(content, file.filename, file.content_type or "application/octet-stream")
    return {"success": True, "data": {"url": url, "filename": file.filename, "size": len(content)}, "meta": None}

@router.get("/preferences")
async def get_preferences(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserPreference).where(UserPreference.user_id == user.id))
    pref = result.scalar_one_or_none()
    if not pref:
        pref = UserPreference(user_id=user.id)
        db.add(pref)
        await db.commit()
        await db.refresh(pref)

    return {
        "success": True,
        "data": {
            "language": pref.language,
            "timezone": pref.timezone,
            "notifications_enabled": pref.notifications_enabled,
            "privacy_profile_public": pref.privacy_profile_public,
        },
        "meta": None,
    }

@router.patch("/preferences")
async def update_preferences(payload: PreferencesUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserPreference).where(UserPreference.user_id == user.id))
    pref = result.scalar_one_or_none()
    if not pref:
        pref = UserPreference(user_id=user.id)
        db.add(pref)

    for field in ("language", "timezone", "notifications_enabled", "privacy_profile_public"):
        value = getattr(payload, field)
        if value is not None:
            setattr(pref, field, value)

    await db.commit()
    return {"success": True, "data": {"updated": True}, "meta": None}

@router.post("/change-email/request")
async def request_change_email(payload: ChangeEmailRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user.is_email_verified:
        raise HTTPException(status_code=403, detail={"code": "EMAIL_NOT_VERIFIED", "message": "Verifikasi email saat ini diperlukan sebelum mengganti email"})

    existing = await db.execute(select(User).where(User.email == payload.new_email, User.tenant_id == user.tenant_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail={"code": "EMAIL_TAKEN", "message": "Email baru sudah dipakai akun lain"})

    old_token = secrets.token_urlsafe(32)
    new_token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    change_request = EmailChangeRequest(
        user_id=user.id,
        old_email=user.email,
        new_email=payload.new_email,
        old_email_token=old_token,
        new_email_token=new_token,
        expires_at=expires_at,
    )
    db.add(change_request)
    await db.commit()

    old_confirm_link = f"{settings.frontend_url}/confirm-email-change?token={old_token}"
    new_confirm_link = f"{settings.frontend_url}/confirm-email-change?token={new_token}"

    delivery_old = await send_email(
        user.email, "suspicious_activity",
        {"detail": f"Permintaan ganti email ke {payload.new_email}. Jika ini kamu, konfirmasi lewat: {old_confirm_link}. Kalau bukan kamu, abaikan email ini dan segera amankan akun."},
    )
    delivery_new = await send_email(payload.new_email, "verify_email", {"link": new_confirm_link})

    return {
        "success": True,
        "data": {"delivery_old_email": delivery_old, "delivery_new_email": delivery_new},
        "meta": {"note": "Email harus dikonfirmasi dari KEDUA alamat (lama dan baru) sebelum perubahan berlaku. Link berlaku 1 jam."},
    }

@router.post("/change-email/confirm")
async def confirm_change_email(payload: ChangeEmailConfirm, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EmailChangeRequest).where(
            (EmailChangeRequest.old_email_token == payload.token) | (EmailChangeRequest.new_email_token == payload.token)
        )
    )
    change_request = result.scalar_one_or_none()

    if not change_request:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Token tidak valid"})

    if change_request.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail={"code": "TOKEN_EXPIRED", "message": "Token sudah kadaluarsa, ulangi permintaan ganti email"})

    if change_request.old_email_confirmed and change_request.new_email_confirmed:
        raise HTTPException(status_code=400, detail={"code": "ALREADY_CONFIRMED", "message": "Permintaan ini sudah selesai dikonfirmasi"})

    is_old_token = payload.token == change_request.old_email_token
    if is_old_token:
        if change_request.old_email_confirmed:
            raise HTTPException(status_code=400, detail={"code": "ALREADY_CONFIRMED", "message": "Konfirmasi dari email lama sudah dilakukan"})
        change_request.old_email_confirmed = True
    else:
        if change_request.new_email_confirmed:
            raise HTTPException(status_code=400, detail={"code": "ALREADY_CONFIRMED", "message": "Konfirmasi dari email baru sudah dilakukan"})
        change_request.new_email_confirmed = True

    fully_confirmed = change_request.old_email_confirmed and change_request.new_email_confirmed

    if fully_confirmed:
        result = await db.execute(select(User).where(User.id == change_request.user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail={"code": "USER_NOT_FOUND", "message": "User tidak ditemukan"})

        user.email = change_request.new_email
        user.is_email_verified = True
        await db.commit()
        await cache_invalidate(user_cache_key(user.id))
        await log_activity(db, "email_changed", tenant_id=user.tenant_id, user_id=user.id, detail=f"old={change_request.old_email}, new={change_request.new_email}")

        return {
            "success": True,
            "data": {"email_changed": True, "new_email": user.email},
            "meta": {"note": "Kedua konfirmasi selesai, email berhasil diganti"},
        }

    await db.commit()
    waiting_side = "email lama" if is_old_token else "email baru"
    return {
        "success": True,
        "data": {"email_changed": False, "confirmed_side": "old_email" if is_old_token else "new_email"},
        "meta": {"note": f"Konfirmasi dari {'email baru' if is_old_token else 'email lama'} masih ditunggu sebelum email benar-benar berubah"},
    }

@router.post("/deactivate")
async def deactivate_account(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user.deactivated_at = datetime.now(timezone.utc)
    user.is_active = False
    await db.commit()
    await cache_invalidate(user_cache_key(user.id))
    return {"success": True, "data": {"deactivated": True}, "meta": None}

@router.post("/reactivate")
async def reactivate_account(user_id: str, tenant_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id, User.tenant_id == tenant_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail={"code": "USER_NOT_FOUND", "message": "User tidak ditemukan"})

    user.deactivated_at = None
    user.is_active = True
    await db.commit()
    return {"success": True, "data": {"reactivated": True}, "meta": None}

@router.delete("/delete")
async def delete_account(hard: bool = False, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if hard:
        await db.delete(user)
    else:
        user.deleted_at = datetime.now(timezone.utc)
        user.is_active = False
    await db.commit()
    return {"success": True, "data": {"deleted": True, "hard": hard}, "meta": None}