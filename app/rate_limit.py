from fastapi import HTTPException, Request
from app.redis_client import redis_client

async def check_rate_limit(key: str, limit: int, window_seconds: int):
    current = await redis_client.incr(key)
    if current == 1:
        await redis_client.expire(key, window_seconds)
    if current > limit:
        raise HTTPException(
            status_code=429,
            detail={"code": "RATE_LIMITED", "message": "Terlalu banyak percobaan, coba lagi nanti"},
        )

async def rate_limit_by_ip(request: Request, scope: str, limit: int = 20, window_seconds: int = 60):
    ip = request.client.host if request.client else "unknown"
    await check_rate_limit(f"ratelimit:{scope}:ip:{ip}", limit, window_seconds)

async def rate_limit_by_key(scope: str, key: str, limit: int, window_seconds: int):
    await check_rate_limit(f"ratelimit:{scope}:{key}", limit, window_seconds)