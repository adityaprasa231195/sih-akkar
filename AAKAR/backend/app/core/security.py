import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Any
from jose import jwt, JWTError
from app.core.config import settings

def get_password_hash(password: str) -> str:
    salt = "aakar_cadastral_salt"
    return f"sha256${hashlib.sha256((password + salt).encode('utf-8')).hexdigest()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if hashed_password.startswith("$plain$"):
        return plain_password == hashed_password.replace("$plain$", "")
    if hashed_password.startswith("sha256$"):
        return get_password_hash(plain_password) == hashed_password
    # Fallback direct comparison
    return plain_password == hashed_password

def create_access_token(subject: str | Any, role: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": str(subject),
        "role": role,
        "exp": expire
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
