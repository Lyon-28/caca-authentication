import os

import asyncio
import time
from datetime import datetime, timezone

from alembic.config import Config
from alembic import command
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
# from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.code_samples import add_code_samples
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title="Caca Auth",
    version="0.1.0",
    description="Production-ready Authentication & Authorization API",
    docs_url="/docs",
    redoc_url=None,
)

startup_time = time.time()

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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema = add_code_samples(openapi_schema, base_url="https://caca-authentication.vercel.app")
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

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

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "..", "static")), name="static")

"""
@app.get("/")
async def root():
    return FileResponse("static/index.html")
"""

@app.get("/redoc", include_in_schema=False)
async def custom_redoc():
    return FileResponse(os.path.join(BASE_DIR, "..", "static", "redoc.html"))


@app.get("/")
async def root():
    return {
        "success": True,
        "data": {
            "name": app.title,
            "version": app.version,
            "status": "operational",
            "environment": settings.env,
            "docs_url": app.docs_url,
            "redoc_url": app.redoc_url,
            "health_check": "/health",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "meta": None,
    }


@app.get("/health/detailed")
async def health_detailed():
    uptime = time.time() - startup_time
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "version": app.version,
            "uptime_seconds": round(uptime, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "meta": None,
    }
