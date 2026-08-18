from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.database import get_db
from app.models import User, RefreshToken
from app.deps import get_current_user
from app.redis_client import redis_client
from app.security import decode_access_token

router = APIRouter(prefix="/auth", tags=["Session"])

class LogoutRequest(BaseModel):
    access_token: str
    refresh_token: str | None = None

@router.get("/sessions")
async def list_sessions(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.cache_service import cache_get, cache_set
    cache_key = f"cache:sessions:{user.id}"
    cached = await cache_get(cache_key)
    if cached:
        return {"success": True, "data": cached, "meta": {"cache": "hit"}}

    result = await db.execute(
        select(RefreshToken)
        .where(RefreshToken.user_id == user.id, RefreshToken.is_revoked == False)
        .order_by(RefreshToken.last_active_at.desc())
    )
    sessions = result.scalars().all()

    data = {
        "sessions": [
            {
                "id": str(s.id),
                "device_name": s.device_name,
                "device_type": s.device_type,
                "ip_address": s.ip_address,
                "location": s.location,
                "last_active_at": s.last_active_at.isoformat() if s.last_active_at else None,
                "created_at": s.created_at.isoformat(),
            }
            for s in sessions
        ]
    }
    await cache_set(cache_key, data, ttl_seconds=30)

    return {"success": True, "data": data, "meta": {"cache": "miss"}}

@router.delete("/sessions/{session_id}")
async def revoke_session(session_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RefreshToken).where(RefreshToken.id == session_id, RefreshToken.user_id == user.id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "message": "Sesi tidak ditemukan"})

    session.is_revoked = True
    await db.commit()
    
    from app.cache_service import cache_invalidate
    await cache_invalidate(f"cache:sessions:{user.id}")

    return {"success": True, "data": {"revoked": True}, "meta": None}

@router.post("/logout")
async def logout(payload: LogoutRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        decoded = decode_access_token(payload.access_token)
        jti = decoded.get("jti")
        exp = decoded.get("exp")
        if jti and exp:
            ttl = max(int(exp - datetime.now(timezone.utc).timestamp()), 1)
            await redis_client.setex(f"blacklist:{jti}", ttl, "1")
    except ValueError:
        pass

    if payload.refresh_token:
        from app.security import hash_token
        token_hash = hash_token(payload.refresh_token)
        result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash, RefreshToken.user_id == user.id))
        session = result.scalar_one_or_none()
        if session:
            session.is_revoked = True
            await db.commit()
            
    return {"success": True, "data": {"logged_out": True}, "meta": None}

@router.post("/logout-all")
async def logout_all(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(
        update(RefreshToken).where(RefreshToken.user_id == user.id, RefreshToken.is_revoked == False).values(is_revoked=True)
    )
    await db.commit()
    
    from app.cache_service import cache_invalidate
    await cache_invalidate(f"cache:sessions:{user.id}")

    return {"success": True, "data": {"logged_out_all": True}, "meta": None}