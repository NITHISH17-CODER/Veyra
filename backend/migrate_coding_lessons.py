"""
Database schema update and sample coding lesson seed script.
"""

from sqlalchemy import text
from app.database.connection import engine
from app.database.session import SessionLocal
from app.database.base import Base
import app.models  # load all models

def migrate():
    print("Running database migrations for coding IDE integration...")
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        # Add new columns to course_lessons if not exist
        cols = [
            ("has_coding", "TINYINT(1) DEFAULT 0 NOT NULL"),
            ("starter_code", "TEXT NULL"),
            ("default_language", "VARCHAR(50) DEFAULT 'python' NULL"),
            ("default_version", "VARCHAR(50) NULL"),
            ("coding_instructions", "TEXT NULL"),
            ("stdin_example", "TEXT NULL"),
            ("expected_output", "TEXT NULL"),
        ]

        for col_name, col_type in cols:
            try:
                conn.execute(text(f"ALTER TABLE course_lessons ADD COLUMN {col_name} {col_type};"))
                conn.commit()
                print(f"Added column '{col_name}' to course_lessons table.")
            except Exception as e:
                print(f"Column '{col_name}' already exists or alter skipped: {e}")

    # Seed coding attributes into lessons
    db = SessionLocal()
    try:
        from app.models.course_learning import CourseLesson
        lessons = db.query(CourseLesson).all()
        print(f"Found {len(lessons)} total lessons. Updating coding practice attributes...")
        
        for idx, l in enumerate(lessons):
            # Check title or code snippet to configure coding lessons
            title_lower = (l.title or "").lower()
            desc_lower = (l.description or "").lower()
            snippet = l.code_snippet or ""

            # Default set coding flag for lessons with code snippets or coding terms
            if any(term in title_lower or term in desc_lower for term in ["python", "javascript", "js", "html", "css", "java", "c++", "cpp", "code", "syntax", "array", "function", "variable", "class", "react"]):
                l.has_coding = True
                
                if "html" in title_lower or "html" in desc_lower:
                    l.default_language = "html"
                    l.starter_code = snippet or "<h1>Welcome to PathPilot AI</h1>\n<p>Edit this HTML to see live preview!</p>\n<button onclick=\"alert('Hello PathPilot!')\">Click Me</button>"
                    l.coding_instructions = "Modify the HTML code to add a styled header and paragraph."
                elif "java" in title_lower or "java" in desc_lower:
                    l.default_language = "java"
                    l.starter_code = snippet or "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello from PathPilot Java Compiler!\");\n    }\n}"
                    l.coding_instructions = "Write a Java program to compute the factorial of a number."
                elif "c++" in title_lower or "cpp" in title_lower:
                    l.default_language = "cpp"
                    l.starter_code = snippet or "#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << \"PathPilot C++ Compiler Ready!\" << endl;\n    return 0;\n}"
                    l.coding_instructions = "Write a C++ program to process array elements."
                elif "javascript" in title_lower or "js" in title_lower or "react" in title_lower:
                    l.default_language = "javascript"
                    l.starter_code = snippet or "// PathPilot Interactive JavaScript IDE\nfunction calculatePath(skillScore) {\n  console.log('Analyzing skill score:', skillScore);\n  return skillScore >= 80 ? 'Mastery' : 'Keep Learning';\n}\n\nconsole.log(calculatePath(85));"
                    l.coding_instructions = "Implement the function logic and run your code to verify stdout output."
                else:
                    l.default_language = "python"
                    l.starter_code = snippet or "# PathPilot Interactive Python IDE\ndef analyze_skill_gap(current_skills, target_skills):\n    missing = set(target_skills) - set(current_skills)\n    print(f'Identified {len(missing)} skill gaps: {list(missing)}')\n    return missing\n\nanalyze_skill_gap(['Python', 'SQL'], ['Python', 'SQL', 'FastAPI', 'Docker'])\n"
                    l.coding_instructions = "Edit the Python script and press 'Run' to execute in isolated sandbox."

        db.commit()
        print("Coding attributes successfully seeded into database lessons!")
    except Exception as exc:
        print(f"Error seeding coding attributes: {exc}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
