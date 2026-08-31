"""
Integration tests for PathPilot AI Recommendation Engine.

Covers:
    - Skill Gap Engine (with various user skill levels)
    - Career Readiness Score calculation
    - Career Matching Engine
    - Course Recommendation Engine
    - Project Recommendation Engine
    - Learning Path Generation
    - Next Best Action
    - Edge cases (no skills, advanced user, etc.)
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import SessionLocal
from app.models.user import User
from app.models.user_skill import UserSkill
from app.models.learner_profile import LearnerProfile
from app.models.skill import Skill
from app.models.career import Career

client = TestClient(app)


def cleanup_user(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            db.delete(user)
            db.commit()
    finally:
        db.close()


def setup_test_user(email: str, name: str, skills: dict[str, int] | None = None, profile_data: dict | None = None):
    """
    Register user, optionally add skills and profile.
    skills: dict mapping skill name -> proficiency (1-5)
    Returns (token, user_id, headers).
    """
    res = client.post("/api/auth/register", json={
        "name": name,
        "email": email,
        "password": "TestPassword123!",
    })
    assert res.status_code == 201, f"Registration failed: {res.text}"
    token = res.json()["access_token"]
    user_id = res.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    if profile_data:
        res_prof = client.post("/api/profile", headers=headers, json=profile_data)
        assert res_prof.status_code == 201, f"Profile creation failed: {res_prof.text}"

    if skills:
        db = SessionLocal()
        try:
            for skill_name, proficiency in skills.items():
                skill = db.query(Skill).filter(Skill.name == skill_name).first()
                if skill:
                    us = UserSkill(
                        user_id=user_id,
                        skill_id=skill.id,
                        proficiency=proficiency,
                    )
                    db.add(us)
            db.commit()
        finally:
            db.close()

    return token, user_id, headers


def test_recommendation_engine():
    email_1 = "rec.test.ml@example.com"       # ML learner with gaps
    email_2 = "rec.test.noskills@example.com"  # User with no skills
    email_3 = "rec.test.advanced@example.com"  # Advanced user

    cleanup_user(email_1)
    cleanup_user(email_2)
    cleanup_user(email_3)

    try:
        # =====================================================================
        # Setup: User 1 — ML learner with some skills
        # Python=4(Advanced), SQL=3(Intermediate), Statistics=1(Beginner), ML=1(Beginner)
        # =====================================================================
        token1, uid1, h1 = setup_test_user(
            email_1, "ML Learner",
            skills={
                "Python": 4,
                "SQL": 3,
                "Statistics & Probability": 1,
                "Machine Learning": 1,
            },
            profile_data={
                "education": "Bachelor's in Computer Science",
                "experience_level": "Intermediate",
                "career_goal": "Machine Learning Engineer",
                "learning_hours_per_week": 15,
                "learning_preference": "Project-based",
            },
        )

        # =====================================================================
        # Setup: User 2 — No skills at all
        # =====================================================================
        token2, uid2, h2 = setup_test_user(
            email_2, "Fresh Learner",
            skills=None,
            profile_data={
                "education": "High School",
                "experience_level": "Beginner",
                "career_goal": "Data Analyst",
                "learning_hours_per_week": 10,
                "learning_preference": "Video",
            },
        )

        # =====================================================================
        # Setup: User 3 — Advanced user with many skills
        # =====================================================================
        token3, uid3, h3 = setup_test_user(
            email_3, "Expert Dev",
            skills={
                "Python": 5,
                "SQL": 4,
                "Statistics & Probability": 4,
                "Machine Learning": 4,
                "Deep Learning": 4,
                "PyTorch": 4,
                "Docker": 3,
                "MLOps": 3,
                "FastAPI": 4,
                "Git & GitHub Actions": 4,
            },
            profile_data={
                "education": "Master's in AI",
                "experience_level": "Advanced",
                "career_goal": "Machine Learning Engineer",
                "learning_hours_per_week": 20,
                "learning_preference": "Hands-on Projects",
            },
        )

        # Get AI Engineer career_id
        db = SessionLocal()
        ml_career = db.query(Career).filter(Career.name == "AI Engineer").first()
        assert ml_career is not None, "AI Engineer career must exist in seed data"
        ml_career_id = ml_career.id
        db.close()

        # =================================================================
        # TEST 1: Skill Gap — User 1 (AI Learner with gaps)
        # =================================================================
        print("\n=== TEST 1: Skill Gap (AI Learner) ===")
        res = client.get(f"/api/careers/{ml_career_id}/skill-gap", headers=h1)
        assert res.status_code == 200, f"Skill gap failed: {res.text}"
        gap = res.json()["data"]

        assert gap["career"] == "AI Engineer"
        assert 0 <= gap["readiness_score"] <= 100
        assert gap["total_skills"] > 0
        assert gap["gap_count"] > 0

        python_skill = next((s for s in gap["skills"] if s["skill"] == "Python"), None)
        assert python_skill is not None
        print(f"  Python: current={python_skill['current_level']}, "
              f"required={python_skill['required_level']}, gap={python_skill['gap']}, "
              f"status={python_skill['status']}")

        ml_skill = next(
            (s for s in gap["skills"] if s["skill"] == "Machine Learning"),
            None,
        )
        if ml_skill:
            assert ml_skill["gap"] > 0, "ML should have a gap (user=1, required=4)"
            assert ml_skill["status"] in ("medium_gap", "major_gap")
            print(f"  Machine Learning: current={ml_skill['current_level']}, "
                  f"required={ml_skill['required_level']}, gap={ml_skill['gap']}, "
                  f"status={ml_skill['status']}")

        print(f"  Readiness: {gap['readiness_score']}%, "
              f"Ready: {gap['ready_count']}, Gaps: {gap['gap_count']}")

        # =================================================================
        # TEST 2: Skill Gap — User 2 (No skills)
        # =================================================================
        print("\n=== TEST 2: Skill Gap (No Skills) ===")
        res2 = client.get(f"/api/careers/{ml_career_id}/skill-gap", headers=h2)
        assert res2.status_code == 200
        gap2 = res2.json()["data"]
        assert gap2["readiness_score"] == 0, "User with no skills should have 0 readiness"
        assert gap2["gap_count"] == gap2["total_skills"]
        print(f"  Readiness: {gap2['readiness_score']}% (expected 0)")

        # =================================================================
        # TEST 3: Skill Gap — User 3 (Advanced)
        # =================================================================
        print("\n=== TEST 3: Skill Gap (Advanced User) ===")
        res3 = client.get(f"/api/careers/{ml_career_id}/skill-gap", headers=h3)
        assert res3.status_code == 200
        gap3 = res3.json()["data"]
        assert gap3["readiness_score"] > 50, \
            f"Advanced user should have >50% readiness, got {gap3['readiness_score']}%"
        print(f"  Readiness: {gap3['readiness_score']}%, "
              f"Ready: {gap3['ready_count']}, Gaps: {gap3['gap_count']}")

        # =================================================================
        # TEST 4: Career Matching
        # =================================================================
        print("\n=== TEST 4: Career Matching ===")
        res_match = client.post("/api/careers/recommend", headers=h1, json={
            "goal": "I want to become an AI Engineer",
        })
        assert res_match.status_code == 200
        matches = res_match.json()["data"]
        assert len(matches) > 0, "Should have at least 1 career match"
        assert len(matches) <= 5, "Should return at most 5 matches"

        ml_match = next((m for m in matches if "AI" in m["career"]), None)
        assert ml_match is not None, "AI Engineer should appear in recommendations"
        assert ml_match["match_score"] > 0
        assert "matching_skills" in ml_match["reason_data"]
        assert "skill_gaps" in ml_match["reason_data"]

        for m in matches[:3]:
            print(f"  {m['career']}: score={m['match_score']}, "
                  f"skill_match={m['reason_data']['skill_match_pct']}%")

        # =================================================================
        # TEST 5: Career Matching — User 2 (no skills, goal: Software Engineer)
        # =================================================================
        print("\n=== TEST 5: Career Matching (No Skills) ===")
        res_match2 = client.post("/api/careers/recommend", headers=h2, json={
            "goal": "I want to become a Software Engineer",
        })
        assert res_match2.status_code == 200
        matches2 = res_match2.json()["data"]
        assert len(matches2) > 0
        print(f"  Top match: {matches2[0]['career']} (score={matches2[0]['match_score']})")

        # =================================================================
        # TEST 6: Course Recommendations
        # =================================================================
        print("\n=== TEST 6: Course Recommendations ===")
        res_courses = client.get(
            f"/api/courses/recommended?career_id={ml_career_id}",
            headers=h1,
        )
        assert res_courses.status_code == 200
        courses = res_courses.json()["data"]
        assert len(courses) > 0, "Should recommend at least 1 course"
        assert len(courses) <= 10

        for c in courses[:3]:
            assert "id" in c
            assert "title" in c
            assert "recommendation_score" in c
            assert "matched_skills" in c
            assert len(c["matched_skills"]) > 0
            print(f"  {c['title']}: score={c['recommendation_score']}, "
                  f"skills={c['matched_skills']}")

        beginner_python = [c for c in courses
                          if "python" in c["title"].lower()
                          and c.get("difficulty", "").lower() == "beginner"]
        if beginner_python:
            ml_courses = [c for c in courses if any(
                "ai" in s.lower() or "python" in s.lower() for s in c["matched_skills"]
            )]
            if ml_courses:
                assert beginner_python[0]["recommendation_score"] <= ml_courses[0]["recommendation_score"], \
                    "Beginner Python should NOT outrank ML courses for this user"

        # =================================================================
        # TEST 7: Course Recommendations — Advanced User
        # =================================================================
        print("\n=== TEST 7: Course Recommendations (Advanced) ===")
        res_courses3 = client.get(
            f"/api/courses/recommended?career_id={ml_career_id}",
            headers=h3,
        )
        assert res_courses3.status_code == 200
        courses3 = res_courses3.json()["data"]
        print(f"  Courses for advanced user: {len(courses3)}")

        # =================================================================
        # TEST 8: Project Recommendations
        # =================================================================
        print("\n=== TEST 8: Project Recommendations ===")
        res_projects = client.get(
            f"/api/projects/recommended?career_id={ml_career_id}",
            headers=h1,
        )
        assert res_projects.status_code == 200
        projects = res_projects.json()["data"]
        assert len(projects) > 0, "Should recommend at least 1 project"
        assert len(projects) <= 5

        for p in projects[:3]:
            assert "id" in p
            assert "title" in p
            assert "recommendation_score" in p
            assert "matched_skills" in p
            print(f"  {p['title']}: score={p['recommendation_score']}, "
                  f"skills={p['matched_skills']}")

        # =================================================================
        # TEST 9: Learning Path Generation
        # =================================================================
        print("\n=== TEST 9: Learning Path Generation ===")
        res_path = client.post("/api/learning-path/generate", headers=h1, json={
            "career_id": ml_career_id,
        })
        assert res_path.status_code == 201, f"Path gen failed: {res_path.text}"
        path_data = res_path.json()["data"]

        assert path_data["career"] == "AI Engineer"
        assert path_data["total_items"] > 0
        assert path_data["learning_path_id"] > 0
        assert "items" in path_data

        items = path_data["items"]
        assert items[0]["status"] == "current"
        if len(items) > 1:
            assert items[1]["status"] == "locked"

        print(f"  Path: {path_data['title']}")
        print(f"  Items: {path_data['total_items']}, "
              f"Estimated months: {path_data.get('estimated_months')}")
        print(f"  Ready skills: {path_data.get('ready_skills', [])}")
        for item in items[:5]:
            print(f"    #{item['sequence_number']} [{item['item_type']}] "
                  f"{item['title']} ({item['status']})")

        # =================================================================
        # TEST 10: Duplicate Path Prevention
        # =================================================================
        print("\n=== TEST 10: Duplicate Path Prevention ===")
        res_path2 = client.post("/api/learning-path/generate", headers=h1, json={
            "career_id": ml_career_id,
        })
        assert res_path2.status_code == 201
        path_data2 = res_path2.json()["data"]
        assert path_data2["learning_path_id"] != path_data["learning_path_id"], \
            "Should create a new path (old one archived)"
        db = SessionLocal()
        from app.models.learning_path import LearningPath
        old_path = db.query(LearningPath).filter(
            LearningPath.id == path_data["learning_path_id"]
        ).first()
        assert old_path.status == "archived", \
            f"Old path should be archived, got: {old_path.status}"
        db.close()
        print(f"  New path ID: {path_data2['learning_path_id']}, old archived [OK]")

        # =================================================================
        # TEST 11: Next Best Action
        # =================================================================
        print("\n=== TEST 11: Next Best Action ===")
        res_next = client.get("/api/learning-path/next-action", headers=h1)
        assert res_next.status_code == 200
        next_action = res_next.json()["data"]
        assert next_action is not None
        assert "title" in next_action
        assert "type" in next_action
        assert "priority" in next_action
        assert next_action["priority"] in ("high", "medium", "normal", "low")
        print(f"  Next: {next_action['title']} ({next_action['type']}) "
              f"priority={next_action['priority']}")

        # =================================================================
        # TEST 12: Next Action for user with no path
        # =================================================================
        print("\n=== TEST 12: Next Action (No Path) ===")
        res_next2 = client.get("/api/learning-path/next-action", headers=h2)
        assert res_next2.status_code == 200
        assert res_next2.json()["data"] is None
        print("  No path -> data=null [OK]")

        # =================================================================
        # TEST 13: Unauthorized access
        # =================================================================
        print("\n=== TEST 13: Unauthorized Access ===")
        res_unauth = client.get(f"/api/careers/{ml_career_id}/skill-gap")
        assert res_unauth.status_code in (401, 403)
        res_unauth2 = client.post("/api/careers/recommend", json={"goal": "test"})
        assert res_unauth2.status_code in (401, 403)
        res_unauth3 = client.get("/api/courses/recommended")
        assert res_unauth3.status_code in (401, 403)
        res_unauth4 = client.get("/api/projects/recommended")
        assert res_unauth4.status_code in (401, 403)
        res_unauth5 = client.post("/api/learning-path/generate", json={"career_id": 1})
        assert res_unauth5.status_code in (401, 403)
        print("  All endpoints reject unauthenticated requests [OK]")

        # =================================================================
        # TEST 14: Invalid career ID
        # =================================================================
        print("\n=== TEST 14: Invalid Career ID ===")
        res_bad = client.get("/api/careers/99999/skill-gap", headers=h1)
        assert res_bad.status_code == 404
        print("  Invalid career -> 404 [OK]")

        # =================================================================
        # TEST 15: Learning Sequence Logic Verification
        # =================================================================
        print("\n=== TEST 15: Learning Sequence Logic ===")
        items = path_data2["items"]
        item_titles_lower = [i["title"].lower() for i in items]

        beginner_py_items = [t for t in item_titles_lower
                           if "python" in t and "beginner" in t]
        assert len(beginner_py_items) == 0, \
            f"Should not recommend beginner Python (user=4): {beginner_py_items}"
        print("  No beginner Python in path [OK]")

        print("\n" + "=" * 60)
        print(" ALL RECOMMENDATION ENGINE TESTS PASSED! [OK]")
        print("=" * 60)

    finally:
        cleanup_user(email_1)
        cleanup_user(email_2)
        cleanup_user(email_3)


if __name__ == "__main__":
    test_recommendation_engine()
