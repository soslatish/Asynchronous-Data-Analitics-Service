from pydantic_settings import BaseSettings
from typing import Optional
import os
from functools import lru_cache


class Settings(BaseSettings):

    PROJECT_NAME: str = "Device Monitoring System"
    API_V1_STR: str = "/api"
    DEBUG: bool = False

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./device_monitoring.db")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey123")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    #CORS 
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()