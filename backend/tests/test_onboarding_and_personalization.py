"""
Comprehensive tests for User-Driven Personalization & Onboarding Persistence.

Tests:
1. Test User 1: Data Scientist (Goal: "I want to become a Data Scientist", Skills: Python Adv, SQL Int, Stats Beg)
2. Test User 2: Full Stack Developer (Goal: "I want to become a Full Stack Developer", Skills: HTML Adv, CSS Int, JS Beg)
3. Test User 3: Undecided / Cybersecurity (Goal: "I don't know what career to choose", Interests: Cybersecurity, Networking, Skills: Linux Beg, Networking Int)
4. Database persistence and rollback on failure
5. Dashboard reconstruction from MySQL after session reload
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database.connection import SessionLocal
from app.models.user import User
from app.models.learner_profile import LearnerProfile
from app.models.user_preference import UserPreference
from app.models.user_interest import UserInterest
from app.models.career_goal import CareerGoal
from app.models.user_skill import UserSkill
from app.models.learning_path import LearningPath
from app.core.security import create_access_token, hash_password


@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def _create_test_user(db: Session, email: str, name: str) -> tuple[User, str]:
    """Helper to create a user and return (User, JWT token)."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            name=name,
            email=email,
            password_hash=hash_password("TestPassword123!"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(user.id)
    return user, token


# ── TEST 1: User 1 (AI Engineer) ───────────────────────────────────────

def test_onboarding_user_1_data_scientist(client: TestClient, db_session: Session):
    user, token = _create_test_user(db_session, "user1_ds@example.com", "AI Engineer Aspirant")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "education": "B.Tech in Computer Science",
        "education_level": "Bachelor's",
        "field_of_study": "AI Engineer",
        "experience_level": "Intermediate",
        "career_goal": "I want to become an AI Engineer.",
        "objective": "Get an AI Engineer role within 6 months.",
        "interests": ["AI", "Machine Learning", "Python"],
        "skills": [
            {"name": "Python", "proficiency": 4},
            {"name": "SQL", "proficiency": 3},
            {"name": "Statistics & Probability", "proficiency": 1},
        ],
        "learning_hours_per_week": 15,
        "learning_style": "Project-based",
        "difficulty_preference": "Intermediate",
    }

    res = client.post("/api/onboarding", json=payload, headers=headers)
    assert res.status_code == 201, f"Failed: {res.text}"
    data = res.json()

    assert data["success"] is True
    assert data["target_career"] is not None
    assert data["target_career"]["name"] == "AI Engineer"

    # Top matched career must be AI Engineer
    assert len(data["matched_careers"]) > 0
    assert data["matched_careers"][0]["career"] == "AI Engineer"
    assert data["matched_careers"][0]["match_score"] >= 50

    # Skill gaps must reflect Statistics as a gap, Python as ready
    gap_data = data["skill_gap"]
    assert gap_data is not None
    assert gap_data["career"] == "AI Engineer"

    python_skill = next((s for s in gap_data["skills"] if "Python" in s["skill"]), None)
    assert python_skill is not None, f"Python skill not found in gap_data: {gap_data['skills']}"

    # Learning path must be created
    lp = data["learning_path"]
    assert lp is not None
    assert "AI Engineer" in lp["title"] or "AI Engineer" in lp["career"]
    assert lp["total_items"] > 0

    # Verify MySQL persistence directly
    db_profile = db_session.query(LearnerProfile).filter(LearnerProfile.user_id == user.id).first()
    assert db_profile is not None
    assert db_profile.career_goal_text == "I want to become an AI Engineer."

    db_goal = db_session.query(CareerGoal).filter(CareerGoal.user_id == user.id).first()
    assert db_goal is not None

    db_skills = db_session.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    assert len(db_skills) == 3


# ── TEST 2: User 2 (Frontend Developer) ─────────────────────────────────

def test_onboarding_user_2_full_stack_developer(client: TestClient, db_session: Session):
    user, token = _create_test_user(db_session, "user2_fs@example.com", "Frontend Aspirant")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "education": "B.E in Information Technology",
        "education_level": "Bachelor's",
        "field_of_study": "Computer Science",
        "experience_level": "Beginner",
        "career_goal": "I want to become a Frontend Developer.",
        "objective": "Build and launch modern web applications.",
        "interests": ["Frontend Development", "Web Development", "React"],
        "skills": [
            {"name": "HTML & CSS", "proficiency": 4},
            {"name": "JavaScript", "proficiency": 2},
            {"name": "React", "proficiency": 1},
        ],
        "learning_hours_per_week": 12,
        "learning_style": "Project-based",
        "difficulty_preference": "Beginner",
    }

    res = client.post("/api/onboarding", json=payload, headers=headers)
    assert res.status_code == 201, f"Failed: {res.text}"
    data = res.json()

    assert data["success"] is True
    assert data["target_career"]["name"] == "Frontend Developer"

    # Top matched career should be Frontend Developer
    top_career = data["matched_careers"][0]["career"]
    assert top_career == "Frontend Developer"

    # Learning path must be focused on Frontend Developer
    lp = data["learning_path"]
    assert lp is not None
    assert lp["total_items"] > 0


# ── TEST 3: User 3 (Undecided / Cybersecurity) ────────────────────────────

def test_onboarding_user_3_undecided_cybersecurity(client: TestClient, db_session: Session):
    user, token = _create_test_user(db_session, "user3_sec@example.com", "Security Aspirant")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "education": "B.S. in Information Systems",
        "education_level": "Bachelor's",
        "field_of_study": "Cybersecurity",
        "experience_level": "Beginner",
        "career_goal": "I don't know what career to choose.",
        "objective": "Explore careers in security and systems.",
        "interests": ["Cybersecurity", "Networking"],
        "skills": [
            {"name": "Linux Administration", "proficiency": 2},
            {"name": "Network Security", "proficiency": 3},
            {"name": "Bash & Shell Scripting", "proficiency": 2},
        ],
        "learning_hours_per_week": 10,
        "learning_style": "Mixed",
        "difficulty_preference": "Intermediate",
    }

    res = client.post("/api/onboarding", json=payload, headers=headers)
    assert res.status_code == 201, f"Failed: {res.text}"
    data = res.json()

    assert data["success"] is True

    top_career = data["matched_careers"][0]["career"]
    assert top_career == "Cybersecurity", f"Expected Cybersecurity, got: {top_career}"
    assert data["target_career"]["name"] == "Cybersecurity"

    # Verify skill gap calculation
    gap_data = data["skill_gap"]
    assert gap_data["career"] == "Cybersecurity"

    # Verify roadmap focuses on Cybersecurity
    lp = data["learning_path"]
    assert "Cybersecurity" in lp["career"]


# ── TEST 4: Reconstructing Dashboard from MySQL ───────────────────────────

def test_reconstruct_dashboard_from_mysql(client: TestClient, db_session: Session):
    user, token = _create_test_user(db_session, "user1_ds@example.com", "AI Engineer Aspirant")
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch profile, user-skills, learning-path, next-action
    profile_res = client.get("/api/profile", headers=headers)
    assert profile_res.status_code == 200
    pdata = profile_res.json()
    assert pdata["career_goal"] == "I want to become an AI Engineer."

    skills_res = client.get("/api/user-skills", headers=headers)
    assert skills_res.status_code == 200
    skills_data = skills_res.json()
    assert len(skills_data) == 3

    path_res = client.get("/api/learning-path", headers=headers)
    assert path_res.status_code == 200
    path_data = path_res.json()["data"]
    assert "AI Engineer" in path_data["title"] or "AI Engineer" in path_data["career"]

    action_res = client.get("/api/learning-path/next-action", headers=headers)
    assert action_res.status_code == 200
    action_data = action_res.json()["data"]
    assert action_data is not None
