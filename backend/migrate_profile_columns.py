"""
Database Migration Script — Add avatar_url and verification status columns.
"""

from sqlalchemy import text
from app.database.connection import engine

def migrate():
    print("Starting database migration for profile fields...")
    with engine.begin() as conn:
        # 1. Check avatar_url on users table
        res = conn.execute(text("""
            SELECT COUNT(*) FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' AND COLUMN_NAME = 'avatar_url';
        """)).scalar()
        if res == 0:
            print("Adding 'avatar_url' column to 'users' table...")
            conn.execute(text("ALTER TABLE users ADD COLUMN avatar_url VARCHAR(500) NULL;"))

        # 2. Check verification columns on learner_profiles table
        cols_to_add = [
            ("resume_status", "VARCHAR(50) DEFAULT 'not_uploaded'"),
            ("resume_error", "TEXT"),
            ("github_status", "VARCHAR(50) DEFAULT 'not_connected'"),
            ("github_error", "TEXT"),
            ("linkedin_status", "VARCHAR(50) DEFAULT 'not_connected'"),
            ("linkedin_error", "TEXT"),
        ]

        for col_name, col_def in cols_to_add:
            res = conn.execute(text(f"""
                SELECT COUNT(*) FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'learner_profiles' AND COLUMN_NAME = '{col_name}';
            """)).scalar()
            if res == 0:
                print(f"Adding '{col_name}' column to 'learner_profiles' table...")
                conn.execute(text(f"ALTER TABLE learner_profiles ADD COLUMN {col_name} {col_def};"))

    print("Profile fields migration completed successfully!")

if __name__ == "__main__":
    migrate()
