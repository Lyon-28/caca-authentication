import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.database import get_db
from app.models import Tenant, User, UserPreference
from app.deps import get_tenant_from_token
from app.email_service import send_email
from app.audit_service import log_activity

router = APIRouter(prefix="/tenant/newsletter", tags=["Newsletter"])

class NewsletterSend(BaseModel):
    subject: str
    body: str
    only_verified: bool = True
    respect_preferences: bool = True

@router.post("/send")
async def send_newsletter(payload: NewsletterSend, tenant: Tenant = Depends(get_tenant_from_token), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.tenant_id == tenant.id, User.is_active == True)
    if payload.only_verified:
        query = query.where(User.is_email_verified == True)
    result = await db.execute(query)
    users = result.scalars().all()

    recipients = users
    if payload.respect_preferences:
        pref_result = await db.execute(select(UserPreference.user_id).where(UserPreference.notifications_enabled == False))
        opted_out = {row[0] for row in pref_result.all()}
        recipients = [u for u in users if u.id not in opted_out]

    sent_count = 0
    failed_count = 0

    async def send_one(user):
        nonlocal sent_count, failed_count
        result = await send_email(user.email, "newsletter", {"subject": payload.subject, "body": payload.body})
        if result["sent"]:
            sent_count += 1
        else:
            failed_count += 1

    batch_size = 20
    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i + batch_size]
        await asyncio.gather(*[send_one(u) for u in batch])

    await log_activity(db, "newsletter_sent", tenant_id=tenant.id, detail=f"subject={payload.subject}, sent={sent_count}, failed={failed_count}")

    return {
        "success": True,
        "data": {"total_recipients": len(recipients), "sent": sent_count, "failed": failed_count},
        "meta": None,
    }

@router.get("/preview-recipients")
async def preview_recipients(only_verified: bool = True, respect_preferences: bool = True, tenant: Tenant = Depends(get_tenant_from_token), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.tenant_id == tenant.id, User.is_active == True)
    if only_verified:
        query = query.where(User.is_email_verified == True)
    result = await db.execute(query)
    users = result.scalars().all()

    count = len(users)
    if respect_preferences:
        pref_result = await db.execute(select(UserPreference.user_id).where(UserPreference.notifications_enabled == False))
        opted_out = {row[0] for row in pref_result.all()}
        count = len([u for u in users if u.id not in opted_out])

    return {"success": True, "data": {"recipient_count": count}, "meta": None}