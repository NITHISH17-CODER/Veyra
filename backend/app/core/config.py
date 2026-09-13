"""
Centralised application settings loaded from environment variables / .env file.
"""

import json
from typing import List, Union, Any
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application-wide configuration."""

    # ── General ────────────────────────────────────────────────────────────
    APP_NAME: str = "Veyra AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ── Database ───────────────────────────────────────────────────────────
    # In cloud/production, provide DATABASE_URL in Render environment variables (Cloud MySQL / PostgreSQL).
    # Default is self-contained SQLite database for seamless zero-config persistence.
    DATABASE_URL: str = "sqlite:///./veyra_production.db"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, v: Any) -> str:
        if isinstance(v, str):
            url = v.strip()
            if not url:
                return "sqlite:///./veyra_production.db"
            # Render PostgreSQL URLs start with postgres:// or postgresql://
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql://", 1)
            # Cloud MySQL URLs often start with mysql://
            elif url.startswith("mysql://") and not url.startswith("mysql+pymysql://"):
                url = url.replace("mysql://", "mysql+pymysql://", 1)
            return url
        return str(v)


    # ── CORS ───────────────────────────────────────────────────────────────
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://veyra3.netlify.app",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            v_trimmed = v.strip()
            if v_trimmed.startswith("[") and v_trimmed.endswith("]"):
                try:
                    return json.loads(v_trimmed)
                except Exception:
                    pass
            return [origin.strip() for origin in v_trimmed.split(",") if origin.strip()]
        return v

    # ── AI / LLM ──────────────────────────────────────────────────────────
    OPENAI_API_KEY: str = ""

    # ── JWT / Auth ─────────────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-to-a-long-random-string"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

