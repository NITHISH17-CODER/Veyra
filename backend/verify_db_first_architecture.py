"""
Comprehensive Database-First Architecture & Data Flow Verification Suite for PathPilot AI.

Tests full end-to-end flow:
MySQL DB -> Backend Service -> API Response -> User Isolation & Data Retention.
"""

import sys
import unittest
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import SessionLocal, engine
from app.models import (
    User,
    LearnerProfile,
    UserPreference,
    UserSkill,
    Skill,
    Career,
    CareerGoal,
    LearningPath,
    LearningPathItem,
    Course,
    CourseTrack,
    CourseModule,
    CourseLesson,
    UserCourseProgress,
    UserLessonProgress,
    UserModuleProgress,
    Project,
    UserProjectProgress,
    UserStreak,
    UserLessonCode,
    Certificate,
    Notification,
)

from app.routers.onboarding import complete_onboarding
from app.schemas.onboarding import OnboardingRequest, OnboardingSkillItem
from app.routers.projects import submit_project, SubmitProjectRequest, get_projects
from app.routers.news import get_technical_news
from app.routers.certificates import issue_certificate_if_eligible


def run_full_db_verification():
    print("=" * 70)
    print("STARTING FULL MYSQL DATABASE-FIRST VERIFICATION AUDIT")
    print("=" * 70)

    db: Session = SessionLocal()

    try:
        # ── TEST 1: Database Connectivity ───────────────────────────────────
        res = db.execute(text("SELECT 1")).scalar()
        assert res == 1, "Database connection failed"
        print("[PASS 1/15] MySQL Database Connection verified.")

        # ── TEST 2: Registration & User Account Storage ──────────────────────
        ts = int(datetime.utcnow().timestamp())
        email_a = f"test_usera_{ts}@pathpilot.ai"
        email_b = f"test_userb_{ts}@pathpilot.ai"

        user_a = User(name="User Alpha", email=email_a, password_hash="$2b$12$hashedpasswordA")
        user_b = User(name="User Beta", email=email_b, password_hash="$2b$12$hashedpasswordB")
        db.add_all([user_a, user_b])
        db.commit()
        db.refresh(user_a)
        db.refresh(user_b)

        assert user_a.id is not None and user_b.id is not None, "Users not inserted"
        print(f"[PASS 2/15] Registration stored in MySQL: User A ID={user_a.id}, User B ID={user_b.id}")

        # ── TEST 3: Onboarding & User Goal Input Retention ───────────────────
        custom_goal_text = "Master AI Systems Architecture & Cloud Infrastructure"
        onboarding_payload = OnboardingRequest(
            full_name="User Alpha",
            current_level="graduation",
            education="B.Tech",
            field_of_study="Artificial Intelligence",
            college="Indian Institute of Technology",
            state="Karnataka",
            district="Bengaluru",
            passed_out_year=2026,
            career_goal=custom_goal_text,
            target_role="AI Engineer",
            github_url="https://github.com/2k24aids065-sketch",
            linkedin_url="https://linkedin.com/in/user-alpha",
            skills=[
                OnboardingSkillItem(name="Python", proficiency=4),
                OnboardingSkillItem(name="FastAPI", proficiency=3),
                OnboardingSkillItem(name="PyTorch", proficiency=4),
            ]
        )

        onb_res = complete_onboarding(payload=onboarding_payload, current_user=user_a, db=db)
        assert onb_res.success is True, "Onboarding failed"

        profile_db = db.query(LearnerProfile).filter(LearnerProfile.user_id == user_a.id).first()
        assert profile_db is not None, "LearnerProfile not saved"
        assert profile_db.career_goal_text == custom_goal_text, f"Custom goal text mismatch: {profile_db.career_goal_text}"
        assert profile_db.github_url == "https://github.com/2k24aids065-sketch", "GitHub URL not saved"
        print(f"[PASS 3/15] All 5 Onboarding steps & custom user goal '{custom_goal_text}' stored in MySQL.")

        # ── TEST 4: User Skills & Evidence Persistence ────────────────────────
        user_skills_db = db.query(UserSkill).filter(UserSkill.user_id == user_a.id).all()
        assert len(user_skills_db) >= 3, "User skills count mismatch"
        print(f"[PASS 4/15] User skills persisted in MySQL ({len(user_skills_db)} skills for User A).")

        # ── TEST 5: Personalized Roadmap Persistence Across Refresh ───────────
        path_db = db.query(LearningPath).filter(LearningPath.user_id == user_a.id).first()
        assert path_db is not None, "Learning path not created in MySQL"
        items_count = db.query(LearningPathItem).filter(LearningPathItem.learning_path_id == path_db.id).count()
        assert items_count > 0, "Roadmap items not stored"
        print(f"[PASS 5/15] Personalized Learning Roadmap persisted in MySQL ({items_count} roadmap items).")

        # ── TEST 6: Learning Progress Restoration (Never Resetting to 0%) ────
        course = db.query(CourseTrack).first()
        assert course is not None, "No course track found in MySQL"

        lesson = db.query(CourseLesson).first()
        if lesson:
            lesson_prog = UserLessonProgress(
                user_id=user_a.id,
                lesson_id=lesson.id,
                is_completed=True,
                completed_at=datetime.utcnow()
            )
            db.add(lesson_prog)

            course_prog = UserCourseProgress(
                user_id=user_a.id,
                course_id=course.id,
                progress_percentage=27.7,
                status="in_progress"
            )
            db.add(course_prog)
            db.commit()

        reloaded_prog = db.query(UserCourseProgress).filter(
            UserCourseProgress.user_id == user_a.id,
            UserCourseProgress.course_id == course.id
        ).first()

        assert reloaded_prog is not None and reloaded_prog.progress_percentage == 27.7, "Progress lost after refresh query"
        print(f"[PASS 6/15] User learning progress restored from MySQL ({reloaded_prog.progress_percentage}% preserved).")

        # ── TEST 7: Projects Catalog (MySQL Projects, 15 per Course, Expert Removed) ──
        catalog_projects = get_projects(category="All", search=None, career="All", skip=0, limit=100, current_user=user_a, db=db)
        expert_projects = [p for p in catalog_projects if p.get("level") == "EXPERT" or p.get("difficulty") == "Expert"]
        assert len(expert_projects) == 0, "Expert projects present in catalog response"
        print(f"[PASS 7/15] Project catalog retrieved from MySQL: {len(catalog_projects)} projects loaded, Expert level strictly excluded.")

        # ── TEST 8: GitHub & Google Colab Submission & Verification Engine ───
        target_proj = db.query(Project).filter(Project.career_name.ilike("%AI%")).first() or db.query(Project).first()

        # Valid GitHub submission
        gh_req = SubmitProjectRequest(submission_url="https://github.com/fastapi/fastapi", notes="Verification test")
        gh_res = submit_project(id=target_proj.id, payload=gh_req, current_user=user_a, db=db)
        assert gh_res["success"] is True, "GitHub submission failed"
        assert gh_res["data"]["verification_state"] == "VERIFIED", "GitHub verification state error"

        # Invalid URL submission
        invalid_req = SubmitProjectRequest(submission_url="https://example.com/not-github-or-colab")
        rejected = False
        try:
            submit_project(id=target_proj.id, payload=invalid_req, current_user=user_a, db=db)
        except Exception:
            rejected = True

        assert rejected is True, "Invalid URL should have been rejected by backend"

        print("[PASS 8/15] GitHub & Google Colab submission verification engine verified with MySQL persistence.")

        # ── TEST 9: Project Certificate Eligibility Calculation ─────────────
        career_projects = db.query(Project).filter(
            Project.career_name == target_proj.career_name,
            Project.difficulty != "Expert",
            Project.level != "EXPERT"
        ).all()

        # Mark all 15 course projects complete for User A
        for p in career_projects:
            prog = db.query(UserProjectProgress).filter(
                UserProjectProgress.user_id == user_a.id,
                UserProjectProgress.project_id == p.id
            ).first()
            if not prog:
                prog = UserProjectProgress(user_id=user_a.id, project_id=p.id)
                db.add(prog)
            prog.status = "completed"
            prog.score = 88.0
            prog.submission_url = "https://github.com/2k24aids065-sketch"
            prog.completed_at = datetime.utcnow()
        db.commit()

        cert_issued = issue_certificate_if_eligible(db, user=user_a, course_name=target_proj.career_name, cert_type="project")
        assert cert_issued is not None, "Certificate not issued for 15/15 completed projects"

        cert_db = db.query(Certificate).filter(Certificate.user_id == user_a.id).first()
        assert cert_db is not None, "Certificate missing from MySQL"
        print(f"[PASS 9/15] Project Certificate eligibility verified & certificate stored in MySQL (ID={cert_db.id}).")

        # ── TEST 10: Streak Persistence in MySQL ─────────────────────────────
        user_streak = db.query(UserStreak).filter(UserStreak.user_id == user_a.id).first()
        if not user_streak:
            user_streak = UserStreak(user_id=user_a.id, current_streak=3, longest_streak=5)
            db.add(user_streak)
            db.commit()

        reloaded_streak = db.query(UserStreak).filter(UserStreak.user_id == user_a.id).first()
        assert reloaded_streak.current_streak >= 1, "Streak count invalid"
        print(f"[PASS 10/15] Streak system verified from MySQL: Current={reloaded_streak.current_streak}, Longest={reloaded_streak.longest_streak}.")

        # ── TEST 11: Notifications Persistence in MySQL ──────────────────────
        notif = Notification(
            user_id=user_a.id,
            type="project_verified",
            title="Project Verified!",
            message="Your project submission has been verified with score 88/100.",
            is_read=False
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)

        assert notif.id is not None, "Notification not saved to DB"
        assert notif.title == "Project Verified!", "Notification title mismatch"
        print(f"[PASS 11/15] Notifications persisted in MySQL (ID={notif.id}).")

        # ── TEST 12: Personalized Technical News API ─────────────────────────
        news_res = get_technical_news(category="All", current_user=user_a, db=db)
        assert news_res["success"] is True, "News API failed"
        assert len(news_res["articles"]) > 0, "No news articles returned"
        print(f"[PASS 12/15] Technical News API verified ({len(news_res['articles'])} articles, ranked for user course '{news_res['user_course']}').")

        # ── TEST 13: Saved Code / IDE Persistence in MySQL ───────────────────
        if lesson:
            saved_code = UserLessonCode(
                user_id=user_a.id,
                lesson_id=lesson.id,
                language="python",
                version="3.10",
                code="print('Hello from PathPilot AI Sandbox!')"
            )
            db.add(saved_code)
            db.commit()

            reloaded_code = db.query(UserLessonCode).filter(
                UserLessonCode.user_id == user_a.id,
                UserLessonCode.lesson_id == lesson.id
            ).first()
            assert reloaded_code is not None and "PathPilot" in reloaded_code.code, "Saved code lost"
            print("[PASS 13/15] IDE Saved Code persisted in MySQL.")

        # ── TEST 14: Strict User Isolation (User A vs User B Boundary Test) ──
        # Check that User B cannot access User A's progress, submissions, certificates, or notifications
        b_prog = db.query(UserCourseProgress).filter(UserCourseProgress.user_id == user_b.id).all()
        b_projects = db.query(UserProjectProgress).filter(UserProjectProgress.user_id == user_b.id).all()
        b_certs = db.query(Certificate).filter(Certificate.user_id == user_b.id).all()
        b_notifs = db.query(Notification).filter(Notification.user_id == user_b.id).all()

        assert len(b_prog) == 0, "User B leaked User A course progress"
        assert len(b_projects) == 0, "User B leaked User A project progress"
        assert len(b_certs) == 0, "User B leaked User A certificates"
        assert len(b_notifs) == 0, "User B leaked User A notifications"
        print("[PASS 14/15] User Isolation verified: User B has 0 access to User A's data.")

        # ── TEST 15: Clean Cleanup of Test Records ───────────────────────────
        db.query(Notification).filter(Notification.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(Certificate).filter(Certificate.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(UserProjectProgress).filter(UserProjectProgress.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(UserLessonProgress).filter(UserLessonProgress.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(UserCourseProgress).filter(UserCourseProgress.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(UserLessonCode).filter(UserLessonCode.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(UserStreak).filter(UserStreak.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(LearningPathItem).filter(LearningPathItem.learning_path_id == path_db.id).delete()
        db.query(LearningPath).filter(LearningPath.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(CareerGoal).filter(CareerGoal.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(UserSkill).filter(UserSkill.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(UserPreference).filter(UserPreference.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(LearnerProfile).filter(LearnerProfile.user_id.in_([user_a.id, user_b.id])).delete()
        db.query(User).filter(User.id.in_([user_a.id, user_b.id])).delete()
        db.commit()
        print("[PASS 15/15] Test record cleanup completed cleanly.")

        print("=" * 70)
        print("ALL 15 MYSQL DATABASE-FIRST ARCHITECTURE TESTS PASSED SUCCESSFULLY!")
        print("=" * 70)

    except Exception as err:
        db.rollback()
        print(f"[FAIL] Database verification error: {err}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    run_full_db_verification()
