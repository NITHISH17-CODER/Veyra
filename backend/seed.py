"""
Convenient CLI runner for PathPilot AI master database seeder.

Usage:
    python seed.py
"""

from app.database.connection import SessionLocal
from app.database.seed import seed_database

if __name__ == "__main__":
    db = SessionLocal()
    try:
        stats = seed_database(db)
    finally:
        db.close()
