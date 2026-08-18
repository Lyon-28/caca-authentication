import re
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Dict, Any

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    uptime_seconds: float
    
class Envelope(BaseModel):
    success: bool
    data: dict | None = None
    meta: dict | None = None

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict | None = None

class TenantRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return validate_password_strength(v)

class TenantLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return validate_password_strength(v)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

def validate_password_strength(v: str) -> str:
    if len(v) < 8:
        raise ValueError("Password minimal 8 karakter")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password harus mengandung huruf besar")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password harus mengandung huruf kecil")
    if not re.search(r"[0-9]", v):
        raise ValueError("Password harus mengandung angka")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", v):
        raise ValueError("Password harus mengandung simbol")
    return v