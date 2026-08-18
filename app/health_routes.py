import time
from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine
from app.redis_client import redis_client

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health():
    return {"success": True, "data": {"status": "ok"}, "meta": None}

@router.get("/health/db")
async def health_db():
    start = time.perf_counter()
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        return {"success": True, "data": {"status": "ok", "response_time_ms": elapsed_ms}, "meta": None}
    except Exception as e:
        return {"success": False, "error": {"code": "DB_UNREACHABLE", "message": str(e)}}

@router.get("/health/redis")
async def health_redis():
    start = time.perf_counter()
    try:
        await redis_client.ping()
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        return {"success": True, "data": {"status": "ok", "response_time_ms": elapsed_ms}, "meta": None}
    except Exception as e:
        return {"success": False, "error": {"code": "REDIS_UNREACHABLE", "message": str(e)}}

@router.get("/health/schema")
async def health_schema():
    async with engine.connect() as conn:
        result = await conn.execute(text("""
            SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result.fetchall()]

        schema_info = {}
        for table in tables:
            cols_result = await conn.execute(text(f"""
                SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}'
            """))
            count_result = await conn.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
            schema_info[table] = {
                "columns": [{"name": c, "type": t} for c, t in cols_result.fetchall()],
                "row_count": count_result.scalar(),
            }

    return {"success": True, "data": {"tables": schema_info}, "meta": {"total_tables": len(tables)}}

@router.get("/health/db-stats")
async def health_db_stats():
    async with engine.connect() as conn:
        pool_status = engine.pool.status()
        version_result = await conn.execute(text("SHOW server_version"))
        version = version_result.scalar()
        size_result = await conn.execute(text("SELECT pg_database_size(current_database())"))
        size_bytes = size_result.scalar()

    return {
        "success": True,
        "data": {"pool_status": pool_status, "postgres_version": version, "database_size_bytes": size_bytes},
        "meta": None,
    }
