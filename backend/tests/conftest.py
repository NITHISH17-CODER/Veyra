import pytest
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Use in-memory SQLite database for testing if MySQL is not available
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_pytest.db")
os.environ["DEBUG"] = "False"
os.environ["SECRET_KEY"] = "test-secret-key-for-pytest-execution"

from app.database.connection import engine, SessionLocal
from app.database.base import Base
import app.models
from app.database.seed import seed_database


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create all tables and seed required reference catalog before running tests."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        from app.models.skill import Skill
        if db.query(Skill).count() == 0:
            seed_database(db)
    finally:
        db.close()

    yield

    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test_pytest.db"):
        try:
            os.remove("test_pytest.db")
        except Exception:
            pass
