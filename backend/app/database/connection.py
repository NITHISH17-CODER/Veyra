"""
Database connection — SQLAlchemy engine and session factory.

All credentials are loaded from the .env file via app.core.config.settings.
No passwords are ever hardcoded in source code.
"""

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
        "pool_recycle": 3600,
    })

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
