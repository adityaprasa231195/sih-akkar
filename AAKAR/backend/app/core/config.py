import os
from typing import List

class Settings:
    PROJECT_NAME: str = "AAKAR"
    TAGLINE: str = "Mapping Every Corner of India"
    ORGANIZATION: str = "Ministry of Rural Development, Dept of Land Resources (DoLR), Government of India"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "aakar-super-secret-key-production-ready-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./aakar.db")
    
    # Redis & Celery
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # System benchmark settings
    MANUAL_BASELINE_HOURS_PER_HA: float = 48.0
    
    # ULPIN default location codes
    DEFAULT_STATE: str = "MH"
    DEFAULT_DISTRICT: str = "07"
    DEFAULT_TALUKA: str = "03"
    DEFAULT_VILLAGE: str = "0012"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

settings = Settings()
