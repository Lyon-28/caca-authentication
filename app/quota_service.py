from datetime import datetime, timezone
from app.redis_client import redis_client

def current_year_month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")

def usage_key(tenant_id) -> str:
    return f"usage:{tenant_id}:{current_year_month()}"

async def increment_usage(tenant_id) -> int:
    key = usage_key(tenant_id)
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, 2764800)
    return count

async def get_usage(tenant_id) -> int:
    count = await redis_client.get(usage_key(tenant_id))
    return int(count) if count else 0

async def check_quota(tenant_id, quota_limit: int):
    from fastapi import HTTPException
    usage = await get_usage(tenant_id)
    if usage >= quota_limit:
        raise HTTPException(
            status_code=429,
            detail={"code": "QUOTA_EXCEEDED", "message": "Kuota bulanan tenant telah habis"},
        )