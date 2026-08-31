"""
Centralised application settings loaded from environment variables / .env file.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application-wide configuration."""

    # ── General ────────────────────────────────────────────────────────────
    APP_NAME: str = "PathPilot AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # ── Database ───────────────────────────────────────────────────────────
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/pathpilot_ai"

    # ── CORS ───────────────────────────────────────────────────────────────
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",   # Vite dev-server
        "http://localhost:3000",
    ]

    # ── AI / LLM (placeholder) ────────────────────────────────────────────
    OPENAI_API_KEY: str = ""

    # ── JWT / Auth ─────────────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-to-a-long-random-string"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
