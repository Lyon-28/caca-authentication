import secrets
import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes)

def verify_password(plain: str, hashed: str) -> bool:
    plain_bytes = plain.encode("utf-8")[:72]
    return pwd_context.verify(plain_bytes, hashed)

def generate_api_keys() -> tuple[str, str]:
    secret_key = f"caca-sk_{secrets.token_urlsafe(32)}"
    public_key = f"caca-pk_{secrets.token_urlsafe(32)}"
    return secret_key, public_key

def create_access_token(user_id: uuid.UUID, tenant_id: uuid.UUID, session_id: uuid.UUID | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id),
        "session_id": str(session_id) if session_id else None,
        "type": "access",
        "exp": expire,
        "jti": secrets.token_hex(16),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise ValueError("Token tidak valid atau kadaluarsa")
        
def create_admin_token() -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=8)
    payload = {
        "role": "admin",
        "type": "admin_access",
        "exp": expire,
        "jti": secrets.token_hex(16),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def decode_admin_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise ValueError("Token admin tidak valid atau kadaluarsa")
    if payload.get("type") != "admin_access" or payload.get("role") != "admin":
        raise ValueError("Token bukan admin token")
    return payload
    
def create_tenant_token(tenant_id: uuid.UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=8)
    payload = {
        "sub": str(tenant_id),
        "type": "tenant_access",
        "exp": expire,
        "jti": secrets.token_hex(16),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def decode_tenant_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise ValueError("Token tenant tidak valid atau kadaluarsa")
    if payload.get("type") != "tenant_access":
        raise ValueError("Token bukan tenant token")
    return payload