import uuid
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal
from app.models.user import User
from app.models.learner_profile import LearnerProfile
from app.models.user_preference import UserPreference
from app.models.user_skill import UserSkill

client = TestClient(app)

def test_complete_profile_workflow():
    """Verify complete PathPilot AI Profile editing, evidence verification, photo handling, and MySQL persistence."""
    unique_email = f"profile_test_{uuid.uuid4().hex[:8]}@pathpilot.ai"
    
    # 1. Register test user
    reg_resp = client.post("/api/auth/register", json={
        "name": "Jane Developer",
        "email": unique_email,
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    assert reg_resp.status_code == 201, reg_resp.text
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_id = reg_resp.json()["user"]["id"]
    print(f"\n[PASS] User registered with ID {user_id}")

    # 2. GET Profile
    get_res = client.get("/api/profile", headers=headers)
    assert get_res.status_code == 200, get_res.text
    prof_data = get_res.json()
    assert prof_data["full_name"] == "Jane Developer"
    print("[PASS] Initial GET /api/profile succeeded.")

    # 3. PUT Profile (Edit fields including Learning Hours = 12)
    update_res = client.put("/api/profile", headers=headers, json={
        "full_name": "Jane Doe SDE",
        "career_goal": "Full Stack AI Engineer",
        "education": "B.Tech",
        "field_of_study": "Computer Science and Engineering",
        "college": "SRM Institute of Science and Technology",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "passed_out_year": 2025,
        "learning_hours_per_week": 12
    })
    assert update_res.status_code == 200, update_res.text
    updated_data = update_res.json()
    assert updated_data["full_name"] == "Jane Doe SDE"
    assert updated_data["career_goal"] == "Full Stack AI Engineer"
    assert updated_data["education"] == "B.Tech"
    assert updated_data["learning_hours_per_week"] == 12
    print("[PASS] Profile update PUT /api/profile succeeded.")

    # Verify database persistence for learning_hours_per_week sync with UserPreference
    db = SessionLocal()
    pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    assert pref is not None
    assert pref.learning_hours_per_week == 12
    db.close()
    print("[PASS] Learning hours per week synced to UserPreference in MySQL.")

    # 4. Photo Upload
    test_img_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc\xf8\xff\xff?\x03\x00\x05\xfe\x02\xfe\xa79\xfd\xfd\x00\x00\x00\x00IEND\xaeB`\x82"
    photo_res = client.post("/api/profile/photo", headers=headers, files={
        "file": ("test_avatar.png", test_img_content, "image/png")
    })
    assert photo_res.status_code == 200, photo_res.text
    assert photo_res.json()["avatar_url"] is not None
    assert "/uploads/avatars/" in photo_res.json()["avatar_url"]
    print(f"[PASS] Photo uploaded: {photo_res.json()['avatar_url']}")

    # 5. GitHub Verification (Valid & Invalid)
    gh_valid = client.post("/api/profile/github", headers=headers, json={
        "github_url": "https://github.com/torvalds"
    })
    assert gh_valid.status_code == 200, gh_valid.text
    assert gh_valid.json()["github_status"] == "connected"
    print("[PASS] GitHub valid URL verified and connected.")

    gh_invalid = client.post("/api/profile/github", headers=headers, json={
        "github_url": "https://notgithub.com/invaliduser"
    })
    assert gh_invalid.status_code == 200, gh_invalid.text
    assert gh_invalid.json()["github_status"] == "failed"
    print("[PASS] GitHub invalid URL correctly marked as failed.")

    # 6. LinkedIn Verification (Valid & Invalid)
    li_valid = client.post("/api/profile/linkedin", headers=headers, json={
        "linkedin_url": "https://www.linkedin.com/in/janedoe"
    })
    assert li_valid.status_code == 200, li_valid.text
    assert li_valid.json()["linkedin_status"] == "connected"
    print("[PASS] LinkedIn valid URL verified and connected.")

    li_invalid = client.post("/api/profile/linkedin", headers=headers, json={
        "linkedin_url": "https://facebook.com/fake"
    })
    assert li_invalid.status_code == 200, li_invalid.text
    assert li_invalid.json()["linkedin_status"] == "failed"
    print("[PASS] LinkedIn invalid URL correctly marked as failed.")

    # 7. Resume Upload & Verification
    sample_resume = b"Jane Doe - Software Engineer. Experienced in Python, React, JavaScript, SQL, and FastApi. Graduated with B.Tech in Computer Science."
    res_upload = client.post("/api/profile/resume", headers=headers, files={
        "file": ("resume.txt", sample_resume, "text/plain")
    })
    assert res_upload.status_code == 200, res_upload.text
    res_json = res_upload.json()
    assert res_json["resume_status"] == "verified"
    assert res_json["resume_analysis_json"] is not None
    assert "skills" in res_json["resume_analysis_json"]
    print("[PASS] Resume uploaded, parsed, and verified by AI.")

    # 8. User Skills Management
    add_skill_res = client.post("/api/user-skills", headers=headers, json={
        "skill_name": "FastAPI",
        "proficiency": 4
    })
    assert add_skill_res.status_code == 201, add_skill_res.text
    user_skill_id = add_skill_res.json()["id"]
    print(f"[PASS] User skill 'FastAPI' added with ID {user_skill_id}.")

    # Delete User Skill
    del_skill_res = client.delete(f"/api/user-skills/{user_skill_id}", headers=headers)
    assert del_skill_res.status_code == 200, del_skill_res.text
    print("[PASS] User skill deleted successfully.")

    # Final DB Verification
    db = SessionLocal()
    final_user = db.query(User).filter(User.id == user_id).first()
    final_profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == user_id).first()
    
    assert final_user.name == "Jane Doe SDE"
    assert final_user.avatar_url is not None
    assert final_profile.career_goal_text == "Full Stack AI Engineer"
    assert final_profile.learning_hours_per_week == 12
    assert final_profile.github_status == "failed"  # Last attempted was invalid
    assert final_profile.linkedin_status == "failed"  # Last attempted was invalid
    assert final_profile.resume_status == "verified"
    db.close()
    
    print("\n[ALL TESTS PASSED] PathPilot AI Profile workflow & database persistence verified!")

if __name__ == "__main__":
    test_complete_profile_workflow()
