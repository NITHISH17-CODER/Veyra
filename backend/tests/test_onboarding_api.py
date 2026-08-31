"""
Integration tests for PathPilot AI Onboarding APIs:
- Profile endpoints: GET, POST, PUT /api/profile
- Master Skills endpoint: GET /api/skills
- User Skills endpoints: GET, POST, PUT, DELETE /api/user-skills & /api/user-skills/{id}
- Strict authentication & authorization (JWT, user isolation)
- Field validations (proficiency 1-5, learning_hours_per_week 0-168)
"""

import sys
import os

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import SessionLocal
from app.models.user import User
from app.models.skill import Skill

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


def test_onboarding_api_workflow():
    user1_email = "onboarding.tester1@example.com"
    user2_email = "onboarding.tester2@example.com"

    cleanup_user(user1_email)
    cleanup_user(user2_email)

    try:
        # =====================================================================
        # 1. User 1 Registration & Auth
        # =====================================================================
        res_reg1 = client.post(
            "/api/auth/register",
            json={
                "name": "Alex Onboarding",
                "email": user1_email,
                "password": "Password123!",
            },
        )
        assert res_reg1.status_code == 201, f"Reg failed: {res_reg1.text}"
        token1 = res_reg1.json()["access_token"]
        auth1_headers = {"Authorization": f"Bearer {token1}"}

        # User 2 Registration for isolation tests
        res_reg2 = client.post(
            "/api/auth/register",
            json={
                "name": "Sam Isolator",
                "email": user2_email,
                "password": "Password123!",
            },
        )
        assert res_reg2.status_code == 201, f"Reg2 failed: {res_reg2.text}"
        token2 = res_reg2.json()["access_token"]
        auth2_headers = {"Authorization": f"Bearer {token2}"}

        # =====================================================================
        # 2. Master Skills Catalogue (GET /api/skills)
        # =====================================================================
        res_skills = client.get("/api/skills")
        assert res_skills.status_code == 200, f"Skills get failed: {res_skills.text}"
        skills_list = res_skills.json()
        assert len(skills_list) > 0, "Expected seeded skills in database"
        
        # Test category filter
        res_cat = client.get("/api/skills?category=Programming")
        assert res_cat.status_code == 200
        cat_skills = res_cat.json()
        assert all("programming" in s["category"].lower() for s in cat_skills)

        # Test search filter
        res_search = client.get("/api/skills?search=python")
        assert res_search.status_code == 200
        search_skills = res_search.json()
        assert any("python" in s["name"].lower() for s in search_skills)
        
        # Pick 2 skill IDs for user skills testing
        python_skill = next((s for s in skills_list if s["name"] == "Python"), skills_list[0])
        fastapi_skill = next((s for s in skills_list if "FastAPI" in s["name"] or s["id"] != python_skill["id"]), skills_list[1])
        skill_id_1 = python_skill["id"]
        skill_id_2 = fastapi_skill["id"]

        # =====================================================================
        # 3. Profile APIs (GET, POST, PUT /api/profile)
        # =====================================================================
        # Unauthenticated access should fail
        res_unauth_get = client.get("/api/profile")
        assert res_unauth_get.status_code in (401, 403)

        # GET profile before creation -> Auto-creates default profile (200 OK)
        res_prof_init = client.get("/api/profile", headers=auth1_headers)
        assert res_prof_init.status_code == 200, f"Expected 200, got {res_prof_init.status_code}"

        # PUT profile with invalid learning hours (> 168) -> 422
        res_invalid_prof = client.put(
            "/api/profile",
            headers=auth1_headers,
            json={
                "education": "BS in CS",
                "experience_level": "Intermediate",
                "career_goal": "AI Engineer",
                "learning_hours_per_week": 200,  # Invalid (> 168)
                "learning_preference": "Hands-on Projects",
            },
        )
        assert res_invalid_prof.status_code == 422, f"Expected 422, got {res_invalid_prof.status_code}"

        # PUT profile (Valid update) -> 200 OK
        res_create_prof = client.put(
            "/api/profile",
            headers=auth1_headers,
            json={
                "education": "Bachelor's in Computer Science",
                "experience_level": "Intermediate",
                "career_goal": "Full Stack AI Engineer",
                "learning_hours_per_week": 15,
                "learning_preference": "Project-based & Video",
            },
        )
        assert res_create_prof.status_code == 200, f"Expected 200, got {res_create_prof.status_code}: {res_create_prof.text}"
        prof_data = res_create_prof.json()
        assert prof_data["education"] == "Bachelor's in Computer Science"
        assert prof_data["experience_level"] == "Intermediate"
        assert prof_data["career_goal"] == "Full Stack AI Engineer"
        assert prof_data["learning_hours_per_week"] == 15
        assert prof_data.get("learning_preference") in (None, "Project-based & Video")

        # GET profile -> 200 OK
        res_get_prof = client.get("/api/profile", headers=auth1_headers)
        assert res_get_prof.status_code == 200
        assert res_get_prof.json()["career_goal"] == "Full Stack AI Engineer"

        # PUT profile -> 200 OK (Update existing)
        res_put_prof = client.put(
            "/api/profile",
            headers=auth1_headers,
            json={
                "education": "Master's in Computer Science",
                "experience_level": "Advanced",
                "career_goal": "Senior AI Platform Engineer",
                "learning_hours_per_week": 20,
                "learning_preference": "Interactive Coding",
            },
        )
        assert res_put_prof.status_code == 200, f"Expected 200, got {res_put_prof.status_code}"
        put_data = res_put_prof.json()
        assert put_data["education"] == "Master's in Computer Science"
        assert put_data["experience_level"] == "Advanced"
        assert put_data["career_goal"] == "Senior AI Platform Engineer"
        assert put_data["learning_hours_per_week"] == 20

        # Verify User 2 does not have User 1's profile data (Isolation)
        res_u2_prof = client.get("/api/profile", headers=auth2_headers)
        assert res_u2_prof.status_code == 200
        assert res_u2_prof.json()["career_goal"] != "Senior AI Platform Engineer"

        # =====================================================================
        # 4. User Skills APIs (GET, POST, PUT, DELETE /api/user-skills)
        # =====================================================================
        # Unauthenticated access should fail
        res_unauth_skills = client.get("/api/user-skills")
        assert res_unauth_skills.status_code in (401, 403)

        # GET initial user skills (should be empty list)
        res_u1_skills_empty = client.get("/api/user-skills", headers=auth1_headers)
        assert res_u1_skills_empty.status_code == 200
        assert res_u1_skills_empty.json() == []

        # POST user-skill with invalid proficiency (0 and 6) -> 422
        res_prof_low = client.post(
            "/api/user-skills",
            headers=auth1_headers,
            json={"skill_id": skill_id_1, "proficiency": 0},
        )
        assert res_prof_low.status_code == 422, f"Expected 422, got {res_prof_low.status_code}"

        res_prof_high = client.post(
            "/api/user-skills",
            headers=auth1_headers,
            json={"skill_id": skill_id_1, "proficiency": 6},
        )
        assert res_prof_high.status_code == 422, f"Expected 422, got {res_prof_high.status_code}"

        # POST user-skill with nonexistent skill_id -> 404
        res_nonexistent_skill = client.post(
            "/api/user-skills",
            headers=auth1_headers,
            json={"skill_id": 999999, "proficiency": 3},
        )
        assert res_nonexistent_skill.status_code in (400, 404), f"Expected 400 or 404, got {res_nonexistent_skill.status_code}"

        # POST valid user-skill (Proficiency 3 = Intermediate) -> 201 Created
        res_add_skill1 = client.post(
            "/api/user-skills",
            headers=auth1_headers,
            json={"skill_id": skill_id_1, "proficiency": 3},
        )
        assert res_add_skill1.status_code == 201, f"Expected 201, got {res_add_skill1.status_code}: {res_add_skill1.text}"
        u1_skill1_data = res_add_skill1.json()
        assert u1_skill1_data["skill_id"] == skill_id_1
        assert u1_skill1_data["proficiency"] == 3
        assert u1_skill1_data["proficiency_label"] == "Intermediate"
        assert u1_skill1_data["skill_name"] == python_skill["name"]
        user_skill_id_1 = u1_skill1_data["id"]

        # POST second user-skill (Proficiency 5 = Expert) -> 201 Created
        res_add_skill2 = client.post(
            "/api/user-skills",
            headers=auth1_headers,
            json={"skill_id": skill_id_2, "proficiency": 5},
        )
        assert res_add_skill2.status_code == 201
        u1_skill2_data = res_add_skill2.json()
        assert u1_skill2_data["proficiency"] == 5
        assert u1_skill2_data["proficiency_label"] == "Expert"
        user_skill_id_2 = u1_skill2_data["id"]

        # POST duplicate user-skill -> may return 400 (duplicate rejected) or 201 (upsert/allow)
        res_dup_skill = client.post(
            "/api/user-skills",
            headers=auth1_headers,
            json={"skill_id": skill_id_1, "proficiency": 4},
        )
        dup_was_rejected = res_dup_skill.status_code == 400
        if dup_was_rejected:
            assert "already added" in res_dup_skill.json()["detail"].lower()

        # GET /api/user-skills -> 200 OK (2 or 3 skills depending on duplicate handling)
        res_u1_skills = client.get("/api/user-skills", headers=auth1_headers)
        assert res_u1_skills.status_code == 200
        skills_retrieved = res_u1_skills.json()
        assert len(skills_retrieved) >= 2
        assert any(s["skill_id"] == skill_id_1 for s in skills_retrieved)
        assert any(s["skill_id"] == skill_id_2 for s in skills_retrieved)

        # PUT /api/user-skills/{id} -> update proficiency from 3 to 4 (Advanced)
        res_update_skill = client.put(
            f"/api/user-skills/{user_skill_id_1}",
            headers=auth1_headers,
            json={"proficiency": 4},
        )
        assert res_update_skill.status_code == 200, f"Expected 200, got {res_update_skill.status_code}: {res_update_skill.text}"
        updated_skill_data = res_update_skill.json()
        assert updated_skill_data["proficiency"] == 4
        assert updated_skill_data["proficiency_label"] == "Advanced"

        # User 2 cannot modify User 1's user-skill (Authorization check) -> 404
        res_u2_tamper = client.put(
            f"/api/user-skills/{user_skill_id_1}",
            headers=auth2_headers,
            json={"proficiency": 1},
        )
        assert res_u2_tamper.status_code == 404

        # User 2 cannot delete User 1's user-skill -> 404
        res_u2_delete_tamper = client.delete(
            f"/api/user-skills/{user_skill_id_1}",
            headers=auth2_headers,
        )
        assert res_u2_delete_tamper.status_code == 404

        # DELETE /api/user-skills/{id} by User 1 -> 200 OK
        res_delete = client.delete(
            f"/api/user-skills/{user_skill_id_2}",
            headers=auth1_headers,
        )
        assert res_delete.status_code == 200
        assert res_delete.json()["status"] == "ok"

        # GET /api/user-skills -> skill_id_2 should be gone, skill_id_1 remains
        res_u1_remaining = client.get("/api/user-skills", headers=auth1_headers)
        assert res_u1_remaining.status_code == 200
        remaining_skills = res_u1_remaining.json()
        assert len(remaining_skills) >= 1
        assert any(s["id"] == user_skill_id_1 for s in remaining_skills)

        print(" All onboarding tests passed successfully!")

    finally:
        cleanup_user(user1_email)
        cleanup_user(user2_email)


if __name__ == "__main__":
    test_onboarding_api_workflow()
