import asyncio
from datetime import datetime, timezone
from alembic.config import Config
from alembic import command
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.config import settings
from app.database import engine, Base
from app.logging_config import logger
from app.tenant_routes import router as tenant_router
from app.auth_routes import router as auth_router
from app.otp_routes import router as otp_router
from app.session_routes import router as session_router
from app.oauth_routes import router as oauth_router
from app.profile_routes import router as profile_router
from app.mfa_routes import router as mfa_router
from app.metrics_routes import router as metrics_router
from app.health_routes import router as health_router
from app.terms_routes import router as terms_router
from app.admin_routes import router as admin_router
from app.geocoding_routes import router as geocoding_router
from app.newsletter_routes import router as newsletter_router

app = FastAPI(
    title="Caca Auth",
    version="0.1.0",
    description="Production-ready Authentication & Authorization API",
    docs_url="/docs",
    redoc_url="/redoc"
)

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@app.on_event("startup")
async def startup():
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, run_migrations)
        logger.info("migrations_applied")
    except Exception as e:
        logger.error("migration_failed", extra={"extra_data": {"error": str(e)}})
        raise
    logger.info("app_starting", extra={"extra_data": {"env": settings.env}})
    
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail
    if isinstance(detail, dict):
        error = detail
    else:
        error = {"code": "ERROR", "message": str(detail)}
    return JSONResponse(status_code=exc.status_code, content={"success": False, "error": error})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for err in exc.errors():
        err = dict(err)
        if "ctx" in err and isinstance(err["ctx"], dict) and "error" in err["ctx"]:
            err["ctx"] = {**err["ctx"], "error": str(err["ctx"]["error"])}
        details.append(err)

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {"code": "VALIDATION_ERROR", "message": "Input tidak valid", "details": details},
        },
    )
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tenant_router)
app.include_router(auth_router)
app.include_router(otp_router)
app.include_router(session_router)
app.include_router(oauth_router)
app.include_router(profile_router)
app.include_router(mfa_router)
app.include_router(metrics_router)
app.include_router(health_router)
app.include_router(terms_router)
app.include_router(admin_router)
app.include_router(geocoding_router)
app.include_router(newsletter_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

"""
@app.get("/")
async def root():
    return FileResponse("static/index.html")
"""
@app.get("/")
async def root():
    return {
        "success": True,
        "data": {
            "name": "Caca Auth API",
            "version": "0.1.0",
            "status": "operational",
            "environment": settings.env,
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "health_check": "/health",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "meta": None,
    }

app.get("/health/detailed", response_model=schemas.HealthResponse)
async def health_check():
    uptime = time.time() - startup_time
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "uptime_seconds": round(uptime, 2)
        "success": True, 
        "data": {"status": "ok"}, "meta": None}
