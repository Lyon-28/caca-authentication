import httpx
import time
import hashlib
import base64
import secrets
from jose import jwt as jose_jwt
from app.redis_client import redis_client
from app.config import settings

PROVIDERS = {
    "google": {
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "user_url": "https://www.googleapis.com/oauth2/v3/userinfo",
        "scope": "openid email profile",
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
    },
    "github": {
        "auth_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "user_url": "https://api.github.com/user",
        "scope": "read:user user:email",
        "client_id": settings.github_client_id,
        "client_secret": settings.github_client_secret,
    },
    "facebook": {
        "auth_url": "https://www.facebook.com/v19.0/dialog/oauth",
        "token_url": "https://graph.facebook.com/v19.0/oauth/access_token",
        "user_url": "https://graph.facebook.com/me?fields=id,name,email",
        "scope": "email public_profile",
        "client_id": settings.facebook_client_id,
        "client_secret": settings.facebook_client_secret,
    },
    "microsoft": {
        "auth_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "user_url": "https://graph.microsoft.com/oidc/userinfo",
        "scope": "openid email profile",
        "client_id": settings.microsoft_client_id,
        "client_secret": settings.microsoft_client_secret,
    },
    "discord": {
        "auth_url": "https://discord.com/api/oauth2/authorize",
        "token_url": "https://discord.com/api/oauth2/token",
        "user_url": "https://discord.com/api/users/@me",
        "scope": "identify email",
        "client_id": settings.discord_client_id,
        "client_secret": settings.discord_client_secret,
    },
    "linkedin": {
        "auth_url": "https://www.linkedin.com/oauth/v2/authorization",
        "token_url": "https://www.linkedin.com/oauth/v2/accessToken",
        "user_url": "https://api.linkedin.com/v2/userinfo",
        "scope": "openid email profile",
        "client_id": settings.linkedin_client_id,
        "client_secret": settings.linkedin_client_secret,
    },
    "apple": {
        "auth_url": "https://appleid.apple.com/auth/authorize",
        "token_url": "https://appleid.apple.com/auth/token",
        "user_url": None,
        "scope": "name email",
        "client_id": settings.apple_client_id,
        "client_secret": None,
    },
    "twitter": {
        "auth_url": "https://twitter.com/i/oauth2/authorize",
        "token_url": "https://api.twitter.com/2/oauth2/token",
        "user_url": "https://api.twitter.com/2/users/me",
        "scope": "users.read tweet.read offline.access",
        "client_id": settings.twitter_client_id,
        "client_secret": settings.twitter_client_secret,
    },
    "instagram": {
        "auth_url": "https://www.instagram.com/oauth/authorize",
        "token_url": "https://api.instagram.com/oauth/access_token",
        "user_url": "https://graph.instagram.com/me?fields=id,username",
        "scope": "instagram_business_basic",
        "client_id": settings.instagram_app_id,
        "client_secret": settings.instagram_app_secret,
    },
}

def generate_pkce_pair() -> tuple[str, str]:
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    return verifier, challenge
    
def get_authorize_url(provider: str, state: str, code_challenge: str | None = None) -> str:
    cfg = PROVIDERS[provider]
    redirect_uri = f"{settings.oauth_redirect_base}/auth/oauth/{provider}/callback"
    url = (
        f"{cfg['auth_url']}?client_id={cfg['client_id']}&redirect_uri={redirect_uri}"
        f"&scope={cfg['scope']}&response_type=code&state={state}"
    )
    if code_challenge:
        url += f"&code_challenge={code_challenge}&code_challenge_method=S256"
    return url

async def get_apple_client_secret() -> str:
    cached = await redis_client.get("apple_client_secret")
    if cached:
        return cached
    secret = generate_apple_client_secret()
    await redis_client.setex("apple_client_secret", 15000000, secret)
    return secret

async def exchange_code(provider: str, code: str, code_verifier: str | None = None) -> dict:
    cfg = PROVIDERS[provider]
    redirect_uri = f"{settings.oauth_redirect_base}/auth/oauth/{provider}/callback"
    client_secret = await get_apple_client_secret() if provider == "apple" else cfg["client_secret"]

    data = {
        "client_id": cfg["client_id"],
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    if code_verifier:
        data["code_verifier"] = code_verifier

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(cfg["token_url"], data=data, headers={"Accept": "application/json"})
        resp.raise_for_status()
        return resp.json()

async def fetch_user_info(provider: str, access_token: str) -> dict:
    cfg = PROVIDERS[provider]
    if not cfg["user_url"]:
        return {}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(cfg["user_url"], headers={"Authorization": f"Bearer {access_token}"})
        resp.raise_for_status()
        return resp.json()

def normalize_user_info(provider: str, raw: dict) -> dict:
    if provider == "google":
        return {"id": raw.get("sub"), "email": raw.get("email"), "name": raw.get("name")}
    if provider == "github":
        return {"id": str(raw.get("id")), "email": raw.get("email"), "name": raw.get("name") or raw.get("login")}
    if provider == "facebook":
        return {"id": raw.get("id"), "email": raw.get("email"), "name": raw.get("name")}
    if provider == "microsoft":
        return {"id": raw.get("sub"), "email": raw.get("email"), "name": raw.get("name")}
    if provider == "discord":
        return {"id": raw.get("id"), "email": raw.get("email"), "name": raw.get("username")}
    if provider == "linkedin":
        return {"id": raw.get("sub"), "email": raw.get("email"), "name": raw.get("name")}
    if provider == "twitter":
        data = raw.get("data", {})
        return {"id": data.get("id"), "email": None, "name": data.get("name")}
    if provider == "instagram":
        return {"id": raw.get("id"), "email": None, "name": raw.get("username")}
    return {"id": raw.get("id"), "email": raw.get("email"), "name": raw.get("name")}