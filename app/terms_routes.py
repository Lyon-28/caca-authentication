from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.database import get_db
from app.models import TermsVersion, TermsAcceptance, User
from app.deps import get_current_user

router = APIRouter(prefix="/terms", tags=["Terms"])

class TermsCreate(BaseModel):
    version: str
    content: str

class TermsAccept(BaseModel):
    version: str

@router.post("/versions")
async def create_terms_version(payload: TermsCreate, db: AsyncSession = Depends(get_db)):
    term = TermsVersion(version=payload.version, content=payload.content)
    db.add(term)
    await db.commit()
    await db.refresh(term)
    return {"success": True, "data": {"id": str(term.id), "version": term.version}, "meta": None}

@router.get("/latest")
async def get_latest_terms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TermsVersion).order_by(TermsVersion.created_at.desc()).limit(1))
    term = result.scalar_one_or_none()
    if not term:
        raise HTTPException(status_code=404, detail={"code": "NO_TERMS", "message": "Belum ada versi terms"})
    return {"success": True, "data": {"version": term.version, "content": term.content}, "meta": None}

@router.post("/accept")
async def accept_terms(payload: TermsAccept, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TermsVersion).where(TermsVersion.version == payload.version))
    term = result.scalar_one_or_none()
    if not term:
        raise HTTPException(status_code=404, detail={"code": "TERMS_NOT_FOUND", "message": "Versi terms tidak ditemukan"})

    db.add(TermsAcceptance(user_id=user.id, terms_version_id=term.id))
    await db.commit()

    return {"success": True, "data": {"accepted": True, "version": term.version}, "meta": None}

@router.get("/status")
async def terms_status(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    latest_result = await db.execute(select(TermsVersion).order_by(TermsVersion.created_at.desc()).limit(1))
    latest = latest_result.scalar_one_or_none()
    if not latest:
        return {"success": True, "data": {"needs_acceptance": False}, "meta": None}

    accepted_result = await db.execute(
        select(TermsAcceptance).where(TermsAcceptance.user_id == user.id, TermsAcceptance.terms_version_id == latest.id)
    )
    accepted = accepted_result.scalar_one_or_none()

    return {"success": True, "data": {"needs_acceptance": accepted is None, "latest_version": latest.version}, "meta": None}