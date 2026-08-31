"""
Database connection — SQLAlchemy engine and session factory.

All credentials are loaded from the .env file via app.core.config.settings.
No passwords are ever hardcoded in source code.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# ── Engine ─────────────────────────────────────────────────────────────────────
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # verify connections before handing them out
    pool_size=10,             # maintain up to 10 persistent connections
    max_overflow=20,          # allow up to 20 additional overflow connections
    pool_recycle=3600,        # recycle connections after 1 hour (MySQL wait_timeout)
    echo=settings.DEBUG,      # log SQL statements in debug mode
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
