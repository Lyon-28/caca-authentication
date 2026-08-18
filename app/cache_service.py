import json
from app.redis_client import redis_client

DEFAULT_TTL = 300

async def cache_get(key: str) -> dict | None:
    raw = await redis_client.get(key)
    if raw:
        return json.loads(raw)
    return None

async def cache_set(key: str, value: dict, ttl_seconds: int = DEFAULT_TTL):
    await redis_client.setex(key, ttl_seconds, json.dumps(value))

async def cache_invalidate(key: str):
    await redis_client.delete(key)

async def cache_invalidate_prefix(prefix: str):
    cursor = 0
    while True:
        cursor, keys = await redis_client.scan(cursor, match=f"{prefix}*", count=100)
        if keys:
            await redis_client.delete(*keys)
        if cursor == 0:
            break

def user_cache_key(user_id) -> str:
    return f"cache:user:{user_id}"

def session_cache_key(session_id) -> str:
    return f"cache:session:{session_id}"