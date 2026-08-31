"""
Backward-compatible re-exports.

Prefer importing from ``app.database`` directly:

    from app.database import engine, SessionLocal, Base, get_db
"""

from app.database.connection import engine, SessionLocal, get_db  # noqa: F401
from app.database.base import Base  # noqa: F401
