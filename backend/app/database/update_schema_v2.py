"""
Migration script v2 — Adds background, graduation, resume, GitHub, LinkedIn, and skill evidence columns to MySQL tables.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database.connection import engine
from sqlalchemy import text


def column_exists(conn, table, col):
    result = conn.execute(text(f"SHOW COLUMNS FROM `{table}` LIKE '{col}'"))
    return result.rowcount > 0 or bool(result.fetchone())


learner_profile_columns = [
    ("current_level", "VARCHAR(50) NULL"),
    ("college", "VARCHAR(255) NULL"),
    ("state", "VARCHAR(100) NULL"),
    ("district", "VARCHAR(100) NULL"),
    ("passed_out_year", "INT NULL"),
    ("target_role", "VARCHAR(255) NULL"),
    ("resume_url", "VARCHAR(500) NULL"),
    ("resume_text", "LONGTEXT NULL"),
    ("resume_analysis_json", "JSON NULL"),
    ("github_url", "VARCHAR(500) NULL"),
    ("github_repos_json", "JSON NULL"),
    ("linkedin_url", "VARCHAR(500) NULL"),
    ("linkedin_text", "TEXT NULL"),
]

user_skill_columns = [
    ("source", "VARCHAR(50) NULL DEFAULT 'manual'"),
    ("evidence_text", "TEXT NULL"),
    ("confidence_score", "FLOAT NULL DEFAULT 1.0"),
]

with engine.connect() as conn:
    print("Syncing learner_profiles table schema...")
    for col_name, col_def in learner_profile_columns:
        if not column_exists(conn, "learner_profiles", col_name):
            conn.execute(text(f"ALTER TABLE learner_profiles ADD COLUMN {col_name} {col_def}"))
            conn.commit()
            print(f"  + Added column learner_profiles.{col_name}")
        else:
            print(f"  = Exists learner_profiles.{col_name}")

    print("Syncing user_skills table schema...")
    for col_name, col_def in user_skill_columns:
        if not column_exists(conn, "user_skills", col_name):
            conn.execute(text(f"ALTER TABLE user_skills ADD COLUMN {col_name} {col_def}"))
            conn.commit()
            print(f"  + Added column user_skills.{col_name}")
        else:
            print(f"  = Exists user_skills.{col_name}")

print("\n[OK] Database Schema Migration v2 Completed Successfully.")
