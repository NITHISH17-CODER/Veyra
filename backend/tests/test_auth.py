"""
Integration tests for Authentication endpoints (Register, Login, Me, Token security).
"""

import sys
import os

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import SessionLocal
from app.models.user import User

client = TestClient(app)


def test_authentication_workflow():
    db = SessionLocal()
    test_email = "alex.dev@example.com"

    # 1. Clean up user if already exists
    u = db.query(User).filter(User.email == test_email).first()
    if u:
        db.delete(u)
        db.commit()
    db.close()

    # 2. Test Password Validation Failures (Tests 3-6)
    # Less than 8 chars: "Nit@12"
    res_short = client.post(
        "/api/auth/register",
        json={"name": "Alex", "email": "short@example.com", "password": "Nit@12"},
    )
    assert res_short.status_code == 422, f"Expected 422, got {res_short.status_code}"

    # Missing uppercase & special char: "nithish123"
    res_no_upper = client.post(
        "/api/auth/register",
        json={"name": "Alex", "email": "noupper@example.com", "password": "nithish123"},
    )
    assert res_no_upper.status_code == 422, f"Expected 422, got {res_no_upper.status_code}"

    # Missing lowercase: "NITHISH@123"
    res_no_lower = client.post(
        "/api/auth/register",
        json={"name": "Alex", "email": "nolower@example.com", "password": "NITHISH@123"},
    )
    assert res_no_lower.status_code == 422, f"Expected 422, got {res_no_lower.status_code}"

    # Missing number: "Nithish@"
    res_no_num = client.post(
        "/api/auth/register",
        json={"name": "Alex", "email": "nonum@example.com", "password": "Nithish@"},
    )
    assert res_no_num.status_code == 422, f"Expected 422, got {res_no_num.status_code}"

    # 3. Test Successful Registration (Test 1)
    res_reg = client.post(
        "/api/auth/register",
        json={
            "name": "Alex Rivera",
            "email": "  Alex.Dev@Example.com  ",
            "password": "Nithish@123",
        },
    )
    assert res_reg.status_code == 201, f"Expected 201, got {res_reg.status_code}"
    data_reg = res_reg.json()
    assert "access_token" in data_reg
    assert data_reg["token_type"] == "bearer"
    assert data_reg["user"]["email"] == test_email
    assert data_reg["user"]["name"] == "Alex Rivera"

    # 4. Test Duplicate Email Prevention returns HTTP 409 Conflict (Test 2)
    res_dup = client.post(
        "/api/auth/register",
        json={
            "name": "Alex Clone",
            "email": "alex.dev@example.com",
            "password": "AnotherPassword#2026",
        },
    )
    assert res_dup.status_code == 409, f"Expected 409 Conflict, got {res_dup.status_code}"
    dup_body = res_dup.json()
    assert dup_body["code"] == "EMAIL_ALREADY_EXISTS"
    assert "already exists" in dup_body["message"].lower()

    # 5. Test Successful Login (Test 8)
    res_login = client.post(
        "/api/auth/login",
        json={
            "email": "ALEX.DEV@example.com",
            "password": "Nithish@123",
        },
    )
    assert res_login.status_code == 200, f"Expected 200, got {res_login.status_code}"
    data_login = res_login.json()
    assert "access_token" in data_login
    token = data_login["access_token"]

    # 6. Test Wrong Password Login returns generic 401 (Test 9)
    res_wrong_pw = client.post(
        "/api/auth/login",
        json={
            "email": test_email,
            "password": "WrongPassword123",
        },
    )
    assert res_wrong_pw.status_code == 401, f"Expected 401, got {res_wrong_pw.status_code}"
    assert res_wrong_pw.json()["detail"] == "Invalid email or password."

    # 7. Test Nonexistent Email Login returns generic 401 (Test 10)
    res_nonexistent = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent_user_9999@example.com",
            "password": "SomePassword@123",
        },
    )
    assert res_nonexistent.status_code == 401, f"Expected 401, got {res_nonexistent.status_code}"
    assert res_nonexistent.json()["detail"] == "Invalid email or password."

    # 8. Test Authenticated GET /api/auth/me (200 OK) (Test 11)
    res_me = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res_me.status_code == 200, f"Expected 200, got {res_me.status_code}"
    data_me = res_me.json()
    assert data_me["email"] == test_email
    assert data_me["name"] == "Alex Rivera"

    # 9. Test Unauthenticated GET /api/auth/me (401 / 403) (Test 12)
    res_unauth = client.get("/api/auth/me")
    assert res_unauth.status_code in (401, 403), f"Expected 401/403, got {res_unauth.status_code}"

    # 10. Clean up
    db = SessionLocal()
    u = db.query(User).filter(User.email == test_email).first()
    if u:
        db.delete(u)
        db.commit()
    db.close()


if __name__ == "__main__":
    test_authentication_workflow()
    print("All auth tests in tests/test_auth.py executed successfully!")

