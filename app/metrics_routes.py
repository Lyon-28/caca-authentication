from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct
from app.database import get_db
from app.models import User, RefreshToken, ActivityLog, Tenant
from app.deps import get_tenant_from_token

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/overview")
async def metrics_overview(tenant: Tenant = Depends(get_tenant_from_token), db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    day_ago = now - timedelta(days=1)
    month_ago = now - timedelta(days=30)

    dau_result = await db.execute(
        select(func.count(distinct(RefreshToken.user_id))).where(RefreshToken.tenant_id == tenant.id, RefreshToken.last_active_at >= day_ago)
    )
    mau_result = await db.execute(
        select(func.count(distinct(RefreshToken.user_id))).where(RefreshToken.tenant_id == tenant.id, RefreshToken.last_active_at >= month_ago)
    )

    total_users = await db.execute(select(func.count(User.id)).where(User.tenant_id == tenant.id))
    registrations_30d = await db.execute(
        select(func.count(User.id)).where(User.tenant_id == tenant.id, User.created_at >= month_ago)
    )

    login_success = await db.execute(
        select(func.count(ActivityLog.id)).where(ActivityLog.tenant_id == tenant.id, ActivityLog.action == "login_success", ActivityLog.created_at >= month_ago)
    )
    login_failed = await db.execute(
        select(func.count(ActivityLog.id)).where(ActivityLog.tenant_id == tenant.id, ActivityLog.action == "login_failed", ActivityLog.created_at >= month_ago)
    )

    success_count = login_success.scalar() or 0
    failed_count = login_failed.scalar() or 0
    total_attempts = success_count + failed_count

    return {
        "success": True,
        "data": {
            "dau": dau_result.scalar() or 0,
            "mau": mau_result.scalar() or 0,
            "total_users": total_users.scalar() or 0,
            "registrations_30d": registrations_30d.scalar() or 0,
            "login_success_rate": round(success_count / total_attempts, 4) if total_attempts else None,
            "login_failure_rate": round(failed_count / total_attempts, 4) if total_attempts else None,
        },
        "meta": {"period": "30d"},
    }

@router.get("/auth-methods")
async def metrics_auth_methods(tenant: Tenant = Depends(get_tenant_from_token), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ActivityLog.action, func.count(ActivityLog.id))
        .where(ActivityLog.tenant_id == tenant.id, ActivityLog.action.like("login_via_%"))
        .group_by(ActivityLog.action)
    )
    rows = result.all()
    return {"success": True, "data": {"breakdown": {action: count for action, count in rows}}, "meta": None}
