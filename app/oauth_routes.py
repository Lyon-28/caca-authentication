import secrets
from jose import jwt as jose_jwt
from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Tenant, User, OAuthAccount
from app.deps import get_tenant_from_key
from app.oauth_service import PROVIDERS, get_authorize_url, exchange_code, fetch_user_info, normalize_user_info
from app.redis_client import redis_client
from app.auth_routes import issue_token_pair
from app.config import settings

router = APIRouter(prefix="/auth/oauth", tags=["OAuth"])

@router.get("/{provider}/start")
async def oauth_start(provider: str, tenant: Tenant = Depends(get_tenant_from_key)):
    if provider not in PROVIDERS:
        raise HTTPException(status_code=400, detail={"code": "UNKNOWN_PROVIDER", "message": "Provider tidak didukung"})

    state = secrets.token_urlsafe(24)
    await redis_client.setex(f"oauth_state:{state}", 600, str(tenant.id))

    code_challenge = None
    if provider == "twitter":
        from app.oauth_service import generate_pkce_pair
        verifier, code_challenge = generate_pkce_pair()
        await redis_client.setex(f"oauth_pkce:{state}", 600, verifier)

    return {"success": True, "data": {"authorize_url": get_authorize_url(provider, state, code_challenge)}, "meta": None}

@router.get("/{provider}/callback")
async def oauth_callback(provider: str, code: str, state: str, db: AsyncSession = Depends(get_db)):
    if provider == "apple":
        raise HTTPException(status_code=400, detail={"code": "WRONG_METHOD", "message": "Apple callback menggunakan POST, bukan GET"})

    tenant_id = await redis_client.get(f"oauth_state:{state}")
    if not tenant_id:
        raise HTTPException(status_code=401, detail={"code": "INVALID_STATE", "message": "State tidak valid atau kadaluarsa"})
    await redis_client.delete(f"oauth_state:{state}")

    code_verifier = None
    if provider == "twitter":
        code_verifier = await redis_client.get(f"oauth_pkce:{state}")
        await redis_client.delete(f"oauth_pkce:{state}")

    token_data = await exchange_code(provider, code, code_verifier)
    
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail={"code": "OAUTH_FAILED", "message": "Gagal mendapatkan token dari provider"})

    raw_info = await fetch_user_info(provider, access_token)
    info = normalize_user_info(provider, raw_info)

    result = await db.execute(select(OAuthAccount).where(OAuthAccount.provider == provider, OAuthAccount.provider_user_id == str(info["id"])))
    oauth_account = result.scalar_one_or_none()

    if oauth_account:
        result = await db.execute(select(User).where(User.id == oauth_account.user_id))
        user = result.scalar_one_or_none()
    else:
        user = None
        if info.get("email"):
            result = await db.execute(select(User).where(User.email == info["email"], User.tenant_id == tenant_id))
            user = result.scalar_one_or_none()

        if not user:
            user = User(
                tenant_id=tenant_id,
                email=info.get("email") or f"{provider}-{info['id']}@no-email.local",
                name=info.get("name"),
                is_email_verified=bool(info.get("email")),
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        db.add(OAuthAccount(user_id=user.id, provider=provider, provider_user_id=str(info["id"]), email=info.get("email")))
        await db.commit()

    tokens = await issue_token_pair(db, user, tenant_id)
    redirect_url = f"{settings.frontend_url}/oauth-success?access_token={tokens['access_token']}&refresh_token={tokens['refresh_token']}"

    return RedirectResponse(redirect_url)
    
@router.post("/apple/callback")
async def apple_callback(code: str = Form(...), state: str = Form(...), user: str | None = Form(None), db: AsyncSession = Depends(get_db)):
    tenant_id = await redis_client.get(f"oauth_state:{state}")
    if not tenant_id:
        raise HTTPException(status_code=401, detail={"code": "INVALID_STATE", "message": "State tidak valid atau kadaluarsa"})
    await redis_client.delete(f"oauth_state:{state}")

    token_data = await exchange_code("apple", code)
    id_token = token_data.get("id_token")
    if not id_token:
        raise HTTPException(status_code=401, detail={"code": "OAUTH_FAILED", "message": "Gagal mendapatkan id_token dari Apple"})

    claims = jose_jwt.get_unverified_claims(id_token)
    apple_sub = claims.get("sub")
    email = claims.get("email")

    name = None
    if user:
        import json
        try:
            user_data = json.loads(user)
            name_data = user_data.get("name", {})
            name = f"{name_data.get('firstName', '')} {name_data.get('lastName', '')}".strip() or None
        except Exception:
            pass

    result = await db.execute(select(OAuthAccount).where(OAuthAccount.provider == "apple", OAuthAccount.provider_user_id == apple_sub))
    oauth_account = result.scalar_one_or_none()

    if oauth_account:
        result = await db.execute(select(User).where(User.id == oauth_account.user_id))
        db_user = result.scalar_one_or_none()
    else:
        db_user = None
        if email:
            result = await db.execute(select(User).where(User.email == email, User.tenant_id == tenant_id))
            db_user = result.scalar_one_or_none()

        if not db_user:
            db_user = User(tenant_id=tenant_id, email=email or f"apple-{apple_sub}@no-email.local", name=name, is_email_verified=bool(email))
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)

        db.add(OAuthAccount(user_id=db_user.id, provider="apple", provider_user_id=apple_sub, email=email))
        await db.commit()

    tokens = await issue_token_pair(db, db_user, tenant_id)
    redirect_url = f"{settings.frontend_url}/oauth-success?access_token={tokens['access_token']}&refresh_token={tokens['refresh_token']}"
    return RedirectResponse(redirect_url)