"""
Migration script v3 — Adds missing columns to assessment_questions and course_final_questions tables.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database.connection import engine
from sqlalchemy import text


def column_exists(conn, table, col):
    result = conn.execute(text(f"SHOW COLUMNS FROM `{table}` LIKE '{col}'"))
    return bool(result.fetchone())


assessment_questions_columns = [
    ("question_type", "VARCHAR(50) DEFAULT 'mcq'"),
    ("correct_indices", "JSON NULL"),
    ("starter_code", "TEXT NULL"),
    ("code_language", "VARCHAR(50) NULL"),
    ("test_cases_json", "JSON NULL"),
    ("related_lesson_id", "INT NULL"),
    ("related_skill_name", "VARCHAR(100) NULL"),
    ("difficulty", "VARCHAR(50) DEFAULT 'Intermediate'"),
]

course_final_questions_columns = [
    ("question_type", "VARCHAR(50) DEFAULT 'mcq'"),
    ("correct_indices", "JSON NULL"),
    ("starter_code", "TEXT NULL"),
    ("code_language", "VARCHAR(50) NULL"),
    ("test_cases_json", "JSON NULL"),
    ("related_skill_name", "VARCHAR(100) NULL"),
    ("difficulty", "VARCHAR(50) DEFAULT 'Intermediate'"),
]

def migrate_v3():
    with engine.begin() as conn:
        print("Syncing assessment_questions table schema...")
        for col_name, col_def in assessment_questions_columns:
            if not column_exists(conn, "assessment_questions", col_name):
                conn.execute(text(f"ALTER TABLE assessment_questions ADD COLUMN {col_name} {col_def}"))
                print(f"  + Added column assessment_questions.{col_name}")

        print("Syncing course_final_questions table schema...")
        for col_name, col_def in course_final_questions_columns:
            if not column_exists(conn, "course_final_questions", col_name):
                conn.execute(text(f"ALTER TABLE course_final_questions ADD COLUMN {col_name} {col_def}"))
                print(f"  + Added column course_final_questions.{col_name}")

    print("\n[OK] Database Schema Migration v3 Completed Successfully.")

if __name__ == "__main__":
    migrate_v3()
