"""
Database connection — SQLAlchemy engine and session factory.

All credentials are loaded from the .env file via app.core.config.settings.
No passwords are ever hardcoded in source code.
"""

import os
import ssl

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# ── Engine ─────────────────────────────────────────────────────────────────────
engine_args = {
    "pool_pre_ping": True,
    "echo": settings.DEBUG,
}

if "sqlite" in settings.DATABASE_URL.lower():
    engine_args["connect_args"] = {"check_same_thread": False}
else:
    engine_args.update({
        "pool_size": 10,
        "max_overflow": 20,
        "pool_recycle": 1800,
    })

    # Cloud MySQL providers (Aiven, PlanetScale, Railway, AWS RDS, etc.) require SSL.
    # Enable SSL when DATABASE_SSL env var is set or when not connecting to localhost on MySQL.
    if "mysql" in settings.DATABASE_URL.lower() or "pymysql" in settings.DATABASE_URL.lower():
        database_ssl = os.getenv("DATABASE_SSL", "").lower()
        is_localhost = any(host in settings.DATABASE_URL for host in ["localhost", "127.0.0.1"])

        if database_ssl == "true" or (database_ssl != "false" and not is_localhost):
            ssl_ctx = ssl.create_default_context()
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE
            engine_args["connect_args"] = {"ssl": ssl_ctx}

engine = create_engine(
    settings.DATABASE_URL,
    **engine_args,
)



# ── Session factory ────────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    FastAPI dependency that provides a database session.

    Usage in a route:
        @router.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
