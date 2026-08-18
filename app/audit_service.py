import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.email_service import send_email
from app.models import ActivityLog, RefreshToken
from app.logging_config import logger
from app.config import settings

async def log_activity(db: AsyncSession, action: str, tenant_id=None, user_id=None, ip_address: str | None = None, detail: str | None = None):
    entry = ActivityLog(tenant_id=tenant_id, user_id=user_id, action=action, ip_address=ip_address, detail=detail)
    db.add(entry)
    await db.commit()

    logger.info(action, extra={"extra_data": {
        "tenant_id": str(tenant_id) if tenant_id else None,
        "user_id": str(user_id) if user_id else None,
        "ip_address": ip_address,
        "detail": detail,
    }})

    await export_to_siem(action, tenant_id, user_id, ip_address, detail)

async def export_to_siem(action, tenant_id, user_id, ip_address, detail):
    payload = {
        "action": action,
        "tenant_id": str(tenant_id) if tenant_id else None,
        "user_id": str(user_id) if user_id else None,
        "ip_address": ip_address,
        "detail": detail,
    }

    if settings.datadog_api_key:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                await client.post(
                    "https://http-intake.logs.datadoghq.com/api/v2/logs",
                    headers={"DD-API-KEY": settings.datadog_api_key, "Content-Type": "application/json"},
                    json=[{"message": action, "service": "caca-auth", **payload}],
                )
        except Exception:
            pass

    if settings.axiom_api_token:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                await client.post(
                    f"https://api.axiom.co/v1/datasets/{settings.axiom_dataset}/ingest",
                    headers={"Authorization": f"Bearer {settings.axiom_api_token}"},
                    json=[payload],
                )
        except Exception:
            pass

    if settings.betterstack_source_token:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                await client.post(
                    "https://in.logs.betterstack.com",
                    headers={"Authorization": f"Bearer {settings.betterstack_source_token}"},
                    json={"message": action, **payload},
                )
        except Exception:
            pass
        
async def detect_suspicious_login(db: AsyncSession, user, current_location: str, current_device: str, current_hour: int):
    reasons = []

    result = await db.execute(
        select(RefreshToken.location, RefreshToken.device_name)
        .where(RefreshToken.user_id == user.id, RefreshToken.is_revoked == False)
        .limit(10)
    )
    history = result.all()
    known_locations = {loc for loc, _ in history if loc}
    known_devices = {dev for _, dev in history if dev}

    if known_locations and current_location not in known_locations and current_location != "Unknown":
        reasons.append(f"Login dari lokasi baru: {current_location}")

    if known_devices and current_device not in known_devices:
        reasons.append(f"Login dari perangkat baru: {current_device}")

    if not (6 <= current_hour <= 23):
        reasons.append(f"Login pada waktu tidak biasa: jam {current_hour:02d}:00")

    if reasons:
        detail = " | ".join(reasons)
        await send_email(user.email, "suspicious_activity", {"detail": detail})
        logger.warning("suspicious_login_detected", extra={"extra_data": {"user_id": str(user.id), "reasons": reasons}})

    return reasons