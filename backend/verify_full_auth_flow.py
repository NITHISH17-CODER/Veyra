"""
Comprehensive Verification Script for PathPilot AI Authentication, Registration, MySQL Persistence, JWT Token, Onboarding & User Isolation.
"""

import sys
import os

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import SessionLocal
from app.models.user import User
from app.models.learner_profile import LearnerProfile

client = TestClient(app)

def run_all_tests():
    print("\n============================================================")
    print("STARTING FULL AUTHENTICATION & REGISTRATION END-TO-END VERIFICATION")
    print("============================================================\n")

    db = SessionLocal()

    test_email_a = "e2e_user_a@example.com"
    test_email_b = "e2e_user_b@example.com"

    # Cleanup any prior test run records
    for em in [test_email_a, test_email_b]:
        usr = db.query(User).filter(User.email == em).first()
        if usr:
            db.delete(usr)
    db.commit()
    db.close()

    # -------------------------------------------------------------------
    # TEST C: Weak password rejection & error message
    # -------------------------------------------------------------------
    print("[TEST C] Testing weak password rejection...")
    res_weak = client.post(
        "/api/auth/register",
        json={"name": "Weak User", "email": "weak@example.com", "password": "password123"}
    )
    assert res_weak.status_code == 422, f"Expected 422, got {res_weak.status_code}"
    err_detail = str(res_weak.json())
    assert "Password must contain at least 8 characters" in err_detail, f"Unexpected error msg: {err_detail}"
    print("  [PASS] Weak password correctly rejected with clear 422 error message.")

    # -------------------------------------------------------------------
    # TEST D: Password mismatch check (handled on frontend) & invalid email
    # -------------------------------------------------------------------
    print("[TEST D] Testing invalid email format...")
    res_invalid_email = client.post(
        "/api/auth/register",
        json={"name": "Invalid Email", "email": "invalid-email-format", "password": "PathPilot@123"}
    )
    assert res_invalid_email.status_code == 422, f"Expected 422, got {res_invalid_email.status_code}"
    print("  [PASS] Invalid email format correctly rejected with 422.")

    # -------------------------------------------------------------------
    # TEST A: New User Registration & MySQL Insertion
    # -------------------------------------------------------------------
    print("[TEST A] Testing successful registration for User A...")
    res_reg = client.post(
        "/api/auth/register",
        json={
            "name": "User Alpha",
            "email": "  E2E_User_A@Example.com  ",
            "password": "PathPilot@123"
        }
    )
    assert res_reg.status_code == 201, f"Expected 201, got {res_reg.status_code} - {res_reg.text}"
    reg_data = res_reg.json()
    assert "access_token" in reg_data
    token_a = reg_data["access_token"]
    assert reg_data["user"]["email"] == test_email_a
    assert reg_data["user"]["name"] == "User Alpha"
    assert reg_data["user"]["onboarding_completed"] == False
    print("  [PASS] Registration succeeded. Token issued. Onboarding completed status is False.")

    # Direct MySQL Verification
    db = SessionLocal()
    db_user_a = db.query(User).filter(User.email == test_email_a).first()
    assert db_user_a is not None, "User A record not found in MySQL!"
    assert db_user_a.name == "User Alpha"
    assert db_user_a.email == test_email_a
    assert db_user_a.password_hash != "PathPilot@123", "Plaintext password saved in DB!"
    assert db_user_a.password_hash.startswith("$2b$") or db_user_a.password_hash.startswith("$2a$"), "Password hash not bcrypt!"
    assert db_user_a.onboarding_completed == False
    user_a_id = db_user_a.id
    db.close()
    print(f"  [PASS] MySQL Direct Check Passed: User ID {user_a_id}, bcrypt hash verified, plain password omitted.")

    # -------------------------------------------------------------------
    # TEST B: Duplicate Email Prevention
    # -------------------------------------------------------------------
    print("[TEST B] Testing duplicate email registration...")
    res_dup = client.post(
        "/api/auth/register",
        json={
            "name": "User Alpha Clone",
            "email": "e2e_user_a@example.com",
            "password": "PathPilot@123"
        }
    )
    assert res_dup.status_code == 409, f"Expected 409 Conflict, got {res_dup.status_code}"
    dup_body = res_dup.json()
    assert dup_body["code"] == "EMAIL_ALREADY_EXISTS"
    assert "already exists" in dup_body["message"].lower()
    print("  [PASS] Duplicate email blocked with HTTP 409 Conflict and clear warning message.")

    # -------------------------------------------------------------------
    # TEST F & G: Login Error Cases (Wrong password & Non-existent email)
    # -------------------------------------------------------------------
    print("[TEST F] Testing wrong password login...")
    res_wrong_pw = client.post(
        "/api/auth/login",
        json={"email": test_email_a, "password": "WrongPassword@123"}
    )
    assert res_wrong_pw.status_code == 401, f"Expected 401, got {res_wrong_pw.status_code}"
    assert res_wrong_pw.json()["detail"] == "Invalid email or password."
    print("  [PASS] Wrong password login returned generic 401 Unauthorized.")

    print("[TEST G] Testing nonexistent email login...")
    res_no_email = client.post(
        "/api/auth/login",
        json={"email": "nonexistent_e2e_user@example.com", "password": "PathPilot@123"}
    )
    assert res_no_email.status_code == 401, f"Expected 401, got {res_no_email.status_code}"
    assert res_no_email.json()["detail"] == "Invalid email or password."
    print("  [PASS] Non-existent email login returned generic 401 Unauthorized.")

    # -------------------------------------------------------------------
    # TEST E: Successful Login
    # -------------------------------------------------------------------
    print("[TEST E] Testing successful login with normalized email...")
    res_login = client.post(
        "/api/auth/login",
        json={"email": "  E2E_USER_A@example.com ", "password": "PathPilot@123"}
    )
    assert res_login.status_code == 200, f"Expected 200, got {res_login.status_code}"
    login_data = res_login.json()
    assert "access_token" in login_data
    assert login_data["user"]["email"] == test_email_a
    assert login_data["user"]["onboarding_completed"] == False
    print("  [PASS] Login succeeded. Returned valid JWT token and user info.")

    # -------------------------------------------------------------------
    # TEST H: Authenticated GET /api/auth/me
    # -------------------------------------------------------------------
    print("[TEST H] Testing GET /api/auth/me session persistence...")
    res_me = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert res_me.status_code == 200, f"Expected 200, got {res_me.status_code}"
    me_data = res_me.json()
    assert me_data["id"] == user_a_id
    assert me_data["email"] == test_email_a
    print("  [PASS] Session restored via JWT token!")

    # -------------------------------------------------------------------
    # TEST K: Onboarding Submission & Status Update in MySQL
    # -------------------------------------------------------------------
    print("[TEST K] Testing onboarding submission and onboarding_completed flag...")
    onboarding_payload = {
        "education": "B.Tech Computer Science",
        "education_level": "Bachelor's Degree",
        "field_of_study": "Computer Science",
        "experience_level": "Intermediate",
        "career_goal": "Software Development Engineer (SDE)",
        "objective": "Build production SaaS applications",
        "interests": ["Web Development", "AI"],
        "skills": [{"name": "Python", "proficiency": 4}],
        "learning_hours_per_week": 15,
        "learning_style": "Project-based",
        "difficulty_preference": "Intermediate"
    }

    res_onboarding = client.post(
        "/api/onboarding",
        json=onboarding_payload,
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert res_onboarding.status_code in (200, 201), f"Expected 200/201, got {res_onboarding.status_code} - {res_onboarding.text}"
    print("  [PASS] Onboarding submitted successfully.")

    # Verify onboarding_completed is now True in DB and in auth endpoints
    db = SessionLocal()
    db_user_a_updated = db.query(User).filter(User.id == user_a_id).first()
    assert db_user_a_updated.onboarding_completed == True, "onboarding_completed is not True in MySQL!"
    db.close()

    res_me_after = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert res_me_after.json()["onboarding_completed"] == True
    print("  [PASS] MySQL and GET /api/auth/me confirm onboarding_completed is now True!")

    # Login again as existing onboarding-completed user
    res_login_after = client.post(
        "/api/auth/login",
        json={"email": test_email_a, "password": "PathPilot@123"}
    )
    assert res_login_after.json()["user"]["onboarding_completed"] == True
    print("  [PASS] Login as onboarding-complete user returns onboarding_completed=True for /dashboard redirect!")

    # -------------------------------------------------------------------
    # TEST O: User Data Isolation
    # -------------------------------------------------------------------
    print("[TEST O] Testing User Data Isolation between User A and User B...")
    res_reg_b = client.post(
        "/api/auth/register",
        json={
            "name": "User Beta",
            "email": test_email_b,
            "password": "PathPilot@456"
        }
    )
    assert res_reg_b.status_code == 201
    token_b = res_reg_b.json()["access_token"]

    # User B fetches profile -> receives 404 or User B's profile (not User A's profile)
    res_prof_b = client.get(
        "/api/profile",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert res_prof_b.status_code in (404, 200)
    if res_prof_b.status_code == 200:
        assert res_prof_b.json()["user_id"] != user_a_id, "User B accessed User A's profile data!"
    print("  [PASS] Strict User Data Isolation verified!")

    # -------------------------------------------------------------------
    # Clean up test accounts from MySQL
    # -------------------------------------------------------------------
    db = SessionLocal()
    for em in [test_email_a, test_email_b]:
        usr = db.query(User).filter(User.email == em).first()
        if usr:
            db.delete(usr)
    db.commit()
    db.close()

    print("\n============================================================")
    print("ALL AUTHENTICATION & REGISTRATION END-TO-END TESTS PASSED 100%!")
    print("============================================================\n")

if __name__ == "__main__":
    run_all_tests()
