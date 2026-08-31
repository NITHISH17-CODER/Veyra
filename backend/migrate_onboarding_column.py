"""
Database Migration Script — Safe addition of onboarding_completed column to users table.
"""

from sqlalchemy import text
from app.database.connection import engine

def migrate():
    print("Starting database migration for onboarding_completed column...")
    with engine.begin() as conn:
        # Check if column already exists
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
              AND TABLE_NAME = 'users' 
              AND COLUMN_NAME = 'onboarding_completed';
        """))
        exists = result.scalar() > 0

        if not exists:
            print("Adding 'onboarding_completed' column to 'users' table...")
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN onboarding_completed TINYINT(1) NOT NULL DEFAULT 0;
            """))
            print("Column added successfully.")
        else:
            print("Column 'onboarding_completed' already exists.")

        # Update users who already have a learner_profile
        print("Migrating existing user onboarding status based on learner_profiles...")
        res = conn.execute(text("""
            UPDATE users 
            SET onboarding_completed = 1 
            WHERE id IN (SELECT DISTINCT user_id FROM learner_profiles);
        """))
        print(f"Updated {res.rowcount} users with completed onboarding.")

    print("Migration complete!")

if __name__ == "__main__":
    migrate()
