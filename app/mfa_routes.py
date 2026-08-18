from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.database import get_db
from app.models import User
from app.deps import get_current_user
from app.totp_service import generate_totp_secret, get_provisioning_uri, generate_qr_base64, verify_totp_code

router = APIRouter(prefix="/mfa", tags=["MFA"])

class TotpVerifyRequest(BaseModel):
    code: str

@router.post("/totp/setup")
async def setup_totp(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    secret = generate_totp_secret()
    user.totp_secret = secret
    user.totp_enabled = False
    await db.commit()

    uri = get_provisioning_uri(secret, user.email)
    qr_base64 = generate_qr_base64(uri)

    return {"success": True, "data": {"secret": secret, "qr_code_base64": qr_base64, "otpauth_uri": uri}, "meta": None}

@router.post("/totp/enable")
async def enable_totp(payload: TotpVerifyRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user.totp_secret:
        raise HTTPException(status_code=400, detail={"code": "TOTP_NOT_SETUP", "message": "Jalankan setup TOTP terlebih dahulu"})

    if not verify_totp_code(user.totp_secret, payload.code):
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOTP", "message": "Kode TOTP salah"})

    user.totp_enabled = True
    await db.commit()

    return {"success": True, "data": {"totp_enabled": True}, "meta": None}

@router.post("/totp/verify")
async def verify_totp(payload: TotpVerifyRequest, user: User = Depends(get_current_user)):
    if not user.totp_enabled or not user.totp_secret:
        raise HTTPException(status_code=400, detail={"code": "TOTP_NOT_ENABLED", "message": "TOTP belum diaktifkan"})

    if not verify_totp_code(user.totp_secret, payload.code):
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOTP", "message": "Kode TOTP salah"})

    return {"success": True, "data": {"verified": True}, "meta": None}

@router.post("/totp/disable")
async def disable_totp(payload: TotpVerifyRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not verify_totp_code(user.totp_secret or "", payload.code):
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOTP", "message": "Kode TOTP salah"})

    user.totp_secret = None
    user.totp_enabled = False
    await db.commit()

    return {"success": True, "data": {"totp_enabled": False}, "meta": None}