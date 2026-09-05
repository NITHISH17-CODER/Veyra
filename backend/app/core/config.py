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
    APP_NAME: str = "PathPilot AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # ── Database ───────────────────────────────────────────────────────────
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/pathpilot_ai"

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
