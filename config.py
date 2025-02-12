"""
Application configuration module.

This module defines settings for the application using pydantic Settings,
including database credentials, JWT configurations, and AWS S3 storage settings.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    PROJECT_NAME: str = "Clinikk TV Backend"
    VERSION: str = "1.0.0"

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Storage settings
    STORAGE_PROVIDER: str = "S3"
    STORAGE_BUCKET: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "ap-south-1"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    """
    Cached function to get application settings.

    Returns:
        Settings: An instance of the Settings class.
    """
    return Settings()


settings = get_settings()
