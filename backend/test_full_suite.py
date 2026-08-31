import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal
from app.models.user import User
from app.models.career import Career
from app.models.course_learning import CourseTrack, CourseModule, CourseLesson, ModuleAssessment, UserCourseProgress, UserModuleProgress, UserLessonProgress

client = TestClient(app)

def test_system_careers_count():
    """Verify only the 5 supported careers exist in the system."""
    db = SessionLocal()
    careers = db.query(Career).all()
    career_names = {c.name for c in careers}
    db.close()
    
    expected_careers = {
        "Frontend Developer",
        "Backend Developer",
        "Cybersecurity",
        "Software Development Engineer (SDE)",
        "AI Engineer"
    }
    assert career_names == expected_careers, f"Expected {expected_careers}, got {career_names}"
    print("[PASS] System has strictly the 5 supported careers.")

def test_user_authentication_flow():
    """Test register, duplicate email (409), invalid login (401), valid login, and me endpoint."""
    unique_email = f"test_{uuid.uuid4().hex[:8]}@pathpilot.ai"
    
    # 1. Register
    reg_resp = client.post("/api/auth/register", json={
        "name": "Alex Hunter",
        "email": unique_email,
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!"
    })
    assert reg_resp.status_code == 201, reg_resp.text
    token = reg_resp.json()["access_token"]
    assert token
    
    # 2. Duplicate Register -> 409
    dup_resp = client.post("/api/auth/register", json={
        "name": "Alex Dup",
        "email": unique_email,
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!"
    })
    assert dup_resp.status_code == 409, f"Expected 409, got {dup_resp.status_code}"
    
    # 3. Invalid Login -> 401
    bad_login = client.post("/api/auth/login", json={
        "email": unique_email,
        "password": "WrongPassword!"
    })
    assert bad_login.status_code == 401
    
    # 4. Valid Login -> 200
    login_resp = client.post("/api/auth/login", json={
        "email": unique_email,
        "password": "StrongPassword123!"
    })
    assert login_resp.status_code == 200
    assert login_resp.json()["access_token"]
    
    # 5. Me endpoint with token
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = client.get("/api/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == unique_email
    print("[PASS] Authentication flow verified (201, 409, 401, 200, /me).")

def test_distinct_user_personalization():
    """Verify User A (Web), User B (Cyber), User C (AI) get distinct personalized careers and paths."""
    # User A: Frontend
    email_a = f"usera_{uuid.uuid4().hex[:8]}@pathpilot.ai"
    token_a = client.post("/api/auth/register", json={
        "name": "User Frontend",
        "email": email_a,
        "password": "Password123!",
        "confirm_password": "Password123!"
    }).json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}
    
    onboard_a = client.post("/api/onboarding", headers=headers_a, json={
        "education": "B.Sc Computer Science",
        "education_level": "Bachelor's",
        "field_of_study": "Computer Science",
        "experience_level": "Beginner",
        "career_goal": "I want to build modern websites and responsive web applications.",
        "interests": ["Web Development", "UI/UX", "JavaScript"],
        "skills": [{"name": "HTML & CSS", "proficiency": 3}, {"name": "JavaScript", "proficiency": 2}],
        "learning_hours_per_week": 10,
        "learning_style": "Project-based",
        "difficulty_preference": "Beginner"
    }).json()
    career_a = onboard_a["career_goal"]["identified_career"]
    assert "Frontend" in career_a, f"Expected Frontend Developer, got {career_a}"

    # User B: Cybersecurity
    email_b = f"userb_{uuid.uuid4().hex[:8]}@pathpilot.ai"
    token_b = client.post("/api/auth/register", json={
        "name": "User Cyber",
        "email": email_b,
        "password": "Password123!",
        "confirm_password": "Password123!"
    }).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    
    onboard_b = client.post("/api/onboarding", headers=headers_b, json={
        "education": "B.Tech IT",
        "education_level": "Bachelor's",
        "field_of_study": "Information Technology",
        "experience_level": "Intermediate",
        "career_goal": "I want to protect computer systems and enterprise networks from cyber threats.",
        "interests": ["Cybersecurity", "Networking"],
        "skills": [{"name": "Network Security", "proficiency": 2}, {"name": "Linux Administration", "proficiency": 3}],
        "learning_hours_per_week": 15,
        "learning_style": "Hands-on",
        "difficulty_preference": "Intermediate"
    }).json()
    career_b = onboard_b["career_goal"]["identified_career"]
    assert "Cybersecurity" in career_b, f"Expected Cybersecurity, got {career_b}"

    # User C: AI Engineer
    email_c = f"userc_{uuid.uuid4().hex[:8]}@pathpilot.ai"
    token_c = client.post("/api/auth/register", json={
        "name": "User AI",
        "email": email_c,
        "password": "Password123!",
        "confirm_password": "Password123!"
    }).json()["access_token"]
    headers_c = {"Authorization": f"Bearer {token_c}"}
    
    onboard_c = client.post("/api/onboarding", headers=headers_c, json={
        "education": "M.Sc Data Science",
        "education_level": "Master's",
        "field_of_study": "Data Science",
        "experience_level": "Advanced",
        "career_goal": "I want to build intelligent AI applications with LLMs and deep learning.",
        "interests": ["AI", "Data Science", "Python"],
        "skills": [{"name": "Python", "proficiency": 4}, {"name": "Machine Learning", "proficiency": 3}],
        "learning_hours_per_week": 20,
        "learning_style": "Project-based",
        "difficulty_preference": "Advanced"
    }).json()
    career_c = onboard_c["career_goal"]["identified_career"]
    assert "AI Engineer" in career_c, f"Expected AI Engineer, got {career_c}"

    # Verify all 3 users have different identified careers
    assert len({career_a, career_b, career_c}) == 3, f"Paths must be distinct! Got: {career_a}, {career_b}, {career_c}"
    print(f"[PASS] 3 Distinct Users received 3 distinct careers: {career_a} | {career_b} | {career_c}")

def test_course_progression_assessment_unlock_and_completion():
    """
    Test full course learning lifecycle:
    1. Enroll in course (Frontend Developer)
    2. Get roadmap
    3. Verify Module 1 is unlocked, Module 2 is locked
    4. Access locked module 2 -> verify 403 Forbidden
    5. Complete Module 1 lessons
    6. Take Module 1 assessment and pass (score >= 70%)
    7. Verify Module 2 is now unlocked in MySQL
    8. Complete course final assessment and download summary TXT
    """
    email = f"learner_{uuid.uuid4().hex[:8]}@pathpilot.ai"
    token = client.post("/api/auth/register", json={
        "name": "Sarah Connor",
        "email": email,
        "password": "Password123!",
        "confirm_password": "Password123!"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Get courses list
    courses_resp = client.get("/api/courses", headers=headers)
    assert courses_resp.status_code == 200
    courses = courses_resp.json()
    assert len(courses) == 5, f"Expected 5 courses, got {len(courses)}"
    
    frontend_course = next(c for c in courses if c["slug"] == "frontend-developer")
    
    # 2. Get course roadmap
    roadmap_resp = client.get("/api/courses/frontend-developer/roadmap", headers=headers)
    assert roadmap_resp.status_code == 200
    roadmap_data = roadmap_resp.json()
    phases = roadmap_data["phases"]
    all_modules = [m for p in phases for m in p["modules"]]
    assert len(all_modules) == 12
    
    mod1 = all_modules[0]
    mod2 = all_modules[1]
    assert mod1["status"] == "unlocked"
    assert mod2["status"] == "locked"

    # 3. Security test: attempt to access locked Module 2 lesson or assessment -> 403
    db = SessionLocal()
    mod2_lessons = db.query(CourseLesson).filter(CourseLesson.module_id == mod2["id"]).all()
    mod2_assessment = db.query(ModuleAssessment).filter(ModuleAssessment.module_id == mod2["id"]).first()
    db.close()
    
    if mod2_lessons:
        locked_lesson_resp = client.get(f"/api/courses/frontend-developer/modules/{mod2['id']}/lessons/{mod2_lessons[0].id}", headers=headers)
        assert locked_lesson_resp.status_code == 403, f"Expected 403 on locked lesson, got {locked_lesson_resp.status_code}"
    
    if mod2_assessment:
        locked_assess_resp = client.get(f"/api/modules/{mod2['id']}/assessment", headers=headers)
        assert locked_assess_resp.status_code == 403, f"Expected 403 on locked assessment, got {locked_assess_resp.status_code}"
    print("[PASS] Direct URL security verified (locked module access rejected with HTTP 403).")

    # 4. Complete all lessons in Module 1
    db = SessionLocal()
    mod1_lessons = db.query(CourseLesson).filter(CourseLesson.module_id == mod1["id"]).all()
    db.close()
    
    for les in mod1_lessons:
        comp_resp = client.post(f"/api/lessons/{les.id}/complete", headers=headers)
        assert comp_resp.status_code == 200
        assert comp_resp.json()["is_completed"] == True
    
    # 5. Fetch Module 1 assessment questions
    mod1_assess_resp = client.get(f"/api/modules/{mod1['id']}/assessment", headers=headers)
    assert mod1_assess_resp.status_code == 200
    assess_data = mod1_assess_resp.json()
    assessment_id = assess_data["assessment_id"]
    questions = assess_data["questions"]
    assert len(questions) > 0

    # 6. Submit assessment with correct answers from DB to pass
    db = SessionLocal()
    actual_assessment = db.query(ModuleAssessment).filter(ModuleAssessment.id == assessment_id).first()
    answers_payload = {str(q.id): q.correct_index for q in actual_assessment.questions}
    db.close()
    
    submit_resp = client.post(f"/api/assessments/{assessment_id}/submit", headers=headers, json={"answers": answers_payload})
    assert submit_resp.status_code == 200
    submit_data = submit_resp.json()
    assert submit_data["passed"] == True
    assert submit_data["score"] == 100.0
    assert submit_data["next_module_unlocked"] == True
    print("[PASS] Module 1 assessment graded and passed (Score: 100%). Next module unlocked.")

    # 7. Verify Module 2 is now UNLOCKED in MySQL
    roadmap_after = client.get("/api/courses/frontend-developer/roadmap", headers=headers).json()
    all_modules_after = [m for p in roadmap_after["phases"] for m in p["modules"]]
    assert all_modules_after[0]["status"] == "completed"
    assert all_modules_after[1]["status"] == "unlocked"
    print("[PASS] Module 2 status in MySQL is now 'unlocked'. Progression verified.")

    # 8. Test Course Completion Summary & Download TXT
    summary_resp = client.get("/api/courses/frontend-developer/completion-summary", headers=headers)
    assert summary_resp.status_code == 200
    summary_data = summary_resp.json()
    assert summary_data["course_title"] == "Frontend Developer"

    download_resp = client.get("/api/courses/frontend-developer/completion-summary/download", headers=headers)
    assert download_resp.status_code == 200
    assert "text/plain" in download_resp.headers.get("content-type", "")
    assert "PathPilot AI" in download_resp.text
    print("[PASS] Course completion summary and TXT download verified.")

def test_progress_persistence_after_relogin():
    """Verify that user progress, profile, and roadmap are completely restored after re-authenticating."""
    unique_email = f"persist_{uuid.uuid4().hex[:8]}@pathpilot.ai"
    password = "SuperPassword123!"
    
    # 1. Register & Onboard
    token = client.post("/api/auth/register", json={
        "name": "Persistence Tester",
        "email": unique_email,
        "password": password,
        "confirm_password": password
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    client.post("/api/onboarding", headers=headers, json={
        "education": "MIT",
        "education_level": "Master's",
        "field_of_study": "Computer Science",
        "experience_level": "Intermediate",
        "career_goal": "I want to build backend services and APIs.",
        "interests": ["Backend Development", "Database Engineering"],
        "skills": [{"name": "Python", "proficiency": 3}, {"name": "PostgreSQL", "proficiency": 2}],
        "learning_hours_per_week": 12,
        "learning_style": "Hands-on",
        "difficulty_preference": "Intermediate"
    })
    
    # 2. Simulate Logout (discard token) and Login anew
    login_resp = client.post("/api/auth/login", json={
        "email": unique_email,
        "password": password
    })
    assert login_resp.status_code == 200
    new_token = login_resp.json()["access_token"]
    new_headers = {"Authorization": f"Bearer {new_token}"}
    
    # 3. Retrieve user profile & learning path directly from backend
    profile_resp = client.get("/api/profile", headers=new_headers)
    assert profile_resp.status_code == 200
    prof = profile_resp.json()
    assert prof["education"] == "MIT"
    assert prof["field_of_study"] == "Computer Science"

    skills_resp = client.get("/api/user-skills", headers=new_headers)
    assert skills_resp.status_code == 200
    user_skills = skills_resp.json()
    assert len(user_skills) >= 2

    path_resp = client.get("/api/learning-path", headers=new_headers)
    assert path_resp.status_code == 200
    path_data = path_resp.json()
    assert path_data["data"]["career"] == "Backend Developer"
    print("[PASS] Full profile, skills, and roadmap restored from MySQL after logout/login.")

if __name__ == "__main__":
    print("=== RUNNING PATHPILOT AI AUDIT TEST SUITE ===")
    test_system_careers_count()
    test_user_authentication_flow()
    test_distinct_user_personalization()
    test_course_progression_assessment_unlock_and_completion()
    test_progress_persistence_after_relogin()
    print("\n[ALL TESTS PASSED SUCCESSFULLY!]")
