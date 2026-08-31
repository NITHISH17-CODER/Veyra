"""
Database Schema Migration Helper — Adds missing columns to MySQL tables.
"""

import sys
import os
from sqlalchemy import text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.database.connection import engine
from app.database.base import Base
import app.models

def sync_schema():
    with engine.connect() as conn:
        print("Checking & Syncing MySQL Projects table columns...")
        
        columns_to_add_projects = [
            ("level", "VARCHAR(50) DEFAULT 'BASIC'"),
            ("career_name", "VARCHAR(100) NULL"),
            ("prerequisites_json", "JSON NULL"),
            ("learning_outcomes", "JSON NULL"),
            ("milestones_json", "JSON NULL"),
            ("objectives_json", "JSON NULL"),
            ("technologies_json", "JSON NULL"),
            ("requirements_json", "JSON NULL"),
        ]

        for col_name, col_type in columns_to_add_projects:
            try:
                conn.execute(text(f"ALTER TABLE projects ADD COLUMN {col_name} {col_type};"))
                conn.commit()
                print(f" Added column 'projects.{col_name}'")
            except Exception as e:
                # Column probably exists
                pass

        columns_to_add_progress = [
            ("score", "FLOAT NULL"),
            ("strengths", "JSON NULL"),
            ("weaknesses", "JSON NULL"),
            ("missing_requirements", "JSON NULL"),
            ("technical_feedback", "TEXT NULL"),
            ("recommended_improvements", "JSON NULL"),
        ]

        for col_name, col_type in columns_to_add_progress:
            try:
                conn.execute(text(f"ALTER TABLE user_project_progress ADD COLUMN {col_name} {col_type};"))
                conn.commit()
                print(f" Added column 'user_project_progress.{col_name}'")
            except Exception as e:
                pass

        print("Schema sync complete.")

if __name__ == "__main__":
    sync_schema()
