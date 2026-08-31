"""
Migration script for creating user_learning_activity, user_streaks, notifications, and certificates tables in MySQL.
"""

from app.database.connection import engine
from app.database.base import Base
import app.models  # load all models

def migrate():
    print("Creating enhancement tables in MySQL database if they do not exist...")
    Base.metadata.create_all(bind=engine)
    print("Enhancement schema migration complete!")

if __name__ == "__main__":
    migrate()
