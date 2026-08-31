"""
Diagnostic script for PathPilot AI recommendation pipeline.
Tests each step from database verification to career matching, skill gap,
course recommendations, project recommendations, and learning path generation.
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.connection import SessionLocal, engine
from app.models.user import User
from app.models.learner_profile import LearnerProfile
from app.models.skill import Skill
from app.models.user_skill import UserSkill
from app.models.career import Career
from app.models.career_skill import CareerSkill
from app.models.course import Course
from app.models.course_skill import CourseSkill
from app.models.project import Project
from app.models.project_skill import ProjectSkill
from app.models.interest import Interest
from app.models.user_interest import UserInterest
from app.models.user_preference import UserPreference
from app.models.career_goal import CareerGoal
from app.models.learning_path import LearningPath
from app.models.learning_path_item import LearningPathItem
from app.core.security import hash_password

from app.ai.career_matcher import match_careers
from app.ai.skill_gap import calculate_skill_gap
from app.ai.course_recommender import recommend_courses
from app.ai.project_recommender import recommend_projects
from app.ai.roadmap_generator import generate_learning_path, get_next_best_action


def run_diagnostics():
    print("=" * 70)
    print(" PATHPILOT AI — RECOMMENDATION PIPELINE DIAGNOSTIC REPORT")
    print("=" * 70)

    db: Session = SessionLocal()
    try:
        # ── STEP 2: CHECK DATABASE TABLES & COUNTS ────────────────────
        print("\n>>> STEP 2: CHECKING DATABASE DATA COUNTS IN MYSQL")
        tables_to_check = [
            ("users", User),
            ("learner_profiles", LearnerProfile),
            ("interests", Interest),
            ("user_interests", UserInterest),
            ("user_preferences", UserPreference),
            ("career_goals", CareerGoal),
            ("skills", Skill),
            ("user_skills", UserSkill),
            ("careers", Career),
            ("career_skills", CareerSkill),
            ("courses", Course),
            ("course_skills", CourseSkill),
            ("projects", Project),
            ("project_skills", ProjectSkill),
            ("learning_paths", LearningPath),
            ("learning_path_items", LearningPathItem),
        ]

        counts = {}
        for tbl_name, model in tables_to_check:
            c = db.query(model).count()
            counts[tbl_name] = c
            print(f"  - Table `{tbl_name}`: {c} rows")

        # ── STEP 3: CREATE / RETRIEVE TEST USER ────────────────────────
        print("\n>>> STEP 3: CREATING & RETRIEVING TEST USER (Full Stack Developer)")
        test_email = "fullstack_test_user@example.com"
        user = db.query(User).filter(User.email == test_email).first()
        if not user:
            user = User(
                name="Alex Turner",
                email=test_email,
                password_hash=hash_password("SecurePassword123!"),
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Upsert profile
        profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == user.id).first()
        if not profile:
            profile = LearnerProfile(
                user_id=user.id,
                education="B.S. in Computer Science",
                education_level="Bachelor's",
                field_of_study="Computer Science",
                experience_level="Intermediate",
                career_goal_text="I want to become a Full Stack Developer.",
                objective_text="Build full stack web apps with React, Node, and SQL.",
                learning_hours_per_week=10,
                learning_preference="Project-based",
            )
            db.add(profile)
        else:
            profile.career_goal_text = "I want to become a Full Stack Developer."
            profile.field_of_study = "Computer Science"
            profile.experience_level = "Intermediate"
            profile.learning_hours_per_week = 10
            profile.learning_preference = "Project-based"
        db.commit()
        db.refresh(profile)

        # Save preferences
        prefs = db.query(UserPreference).filter(UserPreference.user_id == user.id).first()
        if not prefs:
            prefs = UserPreference(
                user_id=user.id,
                learning_hours_per_week=10,
                learning_style="Project-based",
                difficulty_preference="Intermediate",
                learning_mode="Self-paced",
                resource_preference="All",
            )
            db.add(prefs)
        db.commit()

        # Save interests (Web Development, JavaScript, Software Development)
        db.query(UserInterest).filter(UserInterest.user_id == user.id).delete()
        for int_name in ["Web Development", "JavaScript", "Software Development"]:
            int_obj = db.query(Interest).filter(Interest.name.ilike(int_name)).first()
            db.add(UserInterest(
                user_id=user.id,
                interest_id=int_obj.id if int_obj else None,
                custom_interest=None if int_obj else int_name,
            ))
        db.commit()

        # Save skills (HTML L4, CSS L3, JavaScript L1, SQL L3)
        db.query(UserSkill).filter(UserSkill.user_id == user.id).delete()
        user_skills_data = [
            ("HTML & CSS", 4),
            ("JavaScript", 1),
            ("SQL", 3),
        ]
        for sk_name, prof in user_skills_data:
            sk_obj = db.query(Skill).filter(Skill.name.ilike(sk_name)).first()
            if sk_obj:
                db.add(UserSkill(user_id=user.id, skill_id=sk_obj.id, proficiency=prof))
        db.commit()

        print(f"  User: id={user.id}, name={user.name}, email={user.email}")
        print(f"  Goal: {profile.career_goal_text}")
        print(f"  Education: {profile.education_level} in {profile.field_of_study}")
        print(f"  Weekly Hours: {profile.learning_hours_per_week}")
        print(f"  Preferences: style={profile.learning_preference}, exp={profile.experience_level}")
        
        user_skills_list = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
        print(f"  User Skills ({len(user_skills_list)}):")
        for us in user_skills_list:
            print(f"    - {us.skill.name}: Level {us.proficiency}/5")

        # ── STEP 4: TEST CAREER MATCHING ──────────────────────────────
        print("\n>>> STEP 4: TESTING CAREER MATCHING FOR GOAL 'I want to become a Full Stack Developer.'")
        matched_careers = match_careers(
            db=db,
            user_id=user.id,
            goal="I want to become a Full Stack Developer.",
            top_n=5,
        )
        for idx, cm in enumerate(matched_careers):
            print(f"  #{idx+1}: {cm['career']} (id={cm['career_id']}) -> Match Score: {cm['match_score']}%")
            print(f"      Skill Match: {cm['reason_data']['skill_match_pct']}%, Goal Relevance: {cm['reason_data']['goal_relevance_pct']}%")
            print(f"      Matching Skills: {cm['reason_data']['matching_skills']}")
            print(f"      Skill Gaps: {cm['reason_data']['skill_gaps']}")

        top_career = matched_careers[0]
        assert "Full Stack" in top_career["career"] or "Frontend" in top_career["career"] or "Backend" in top_career["career"], "Top match is not web-related!"
        print(f"  [SUCCESS] Top match is '{top_career['career']}' (Score: {top_career['match_score']}%)")

        target_career_id = top_career["career_id"]

        # ── STEP 5: TEST SKILL GAP ANALYSIS ───────────────────────────
        print(f"\n>>> STEP 5: TESTING SKILL GAP ANALYSIS FOR CAREER ID {target_career_id} ({top_career['career']})")
        gap_res = calculate_skill_gap(db, user.id, target_career_id)
        print(f"  Career: {gap_res['career']}")
        print(f"  Readiness Score: {gap_res['readiness_score']}%")
        print(f"  Total Career Skills: {gap_res['total_skills']}, Gaps: {gap_res['gap_count']}")
        print(f"  Priority Skills to Learn: {gap_res['priority_skills']}")
        print(f"  Skills Breakdown:")
        for s in gap_res["skills"]:
            print(f"    - {s['skill']}: Current L{s['current_level']} -> Required L{s['required_level']} (Gap: {s['gap']}, Importance: {s['importance']}, Status: {s['status']})")

        # ── STEP 6: TEST COURSE RECOMMENDATIONS ───────────────────────
        print(f"\n>>> STEP 6: TESTING COURSE RECOMMENDATIONS FOR CAREER ID {target_career_id}")
        courses_res = recommend_courses(db, user.id, target_career_id, top_n=5)
        print(f"  Returned {len(courses_res)} courses:")
        for idx, c in enumerate(courses_res):
            print(f"  #{idx+1}: {c['title']} ({c['provider']}) - Score: {c['recommendation_score']}%")
            print(f"      Difficulty: {c['difficulty']}, Duration: {c['duration_hours']} hrs, Price: {c['price']}")
            print(f"      Matched Skills: {c['matched_skills']}")
            print(f"      Addresses Gaps: {c['reason_data']['addresses_gaps']}")

        # ── STEP 7: TEST PROJECT RECOMMENDATIONS ──────────────────────
        print(f"\n>>> STEP 7: TESTING PROJECT RECOMMENDATIONS FOR CAREER ID {target_career_id}")
        projects_res = recommend_projects(db, user.id, target_career_id, top_n=5)
        print(f"  Returned {len(projects_res)} projects:")
        for idx, p in enumerate(projects_res):
            print(f"  #{idx+1}: {p['title']} - Score: {p['recommendation_score']}%")
            print(f"      Difficulty: {p['difficulty']}, Est. Hours: {p['estimated_hours']} hrs")
            print(f"      Matched Skills: {p['matched_skills']}")
            print(f"      Primary Gap: {p['reason_data']['primary_gap']}")

        # ── STEP 8: TEST LEARNING PATH GENERATION ─────────────────────
        print(f"\n>>> STEP 8: TESTING LEARNING PATH GENERATION FOR CAREER ID {target_career_id}")
        path_res = generate_learning_path(db, user.id, target_career_id)
        print(f"  Path Title: {path_res['title']}")
        print(f"  Career: {path_res['career']}")
        print(f"  Readiness Score: {path_res['readiness_score']}%")
        print(f"  Estimated Months: {path_res['estimated_months']}")
        print(f"  Total Sequenced Items: {path_res['total_items']}")
        print("  Sequenced Items:")
        for it in path_res["items"]:
            print(f"    Step {it['sequence_number']}: [{it['item_type'].upper()}] {it['title']} ({it['status']}, est: {it['estimated_hours']} hrs)")

        # ── NEXT BEST ACTION ──────────────────────────────────────────
        print(f"\n>>> TESTING NEXT BEST ACTION")
        next_action = get_next_best_action(db, user.id)
        print(f"  Next Action: {next_action['title']}")
        print(f"  Type: {next_action['type']}, Priority: {next_action['priority']}")
        print(f"  Reason: {next_action['reason_data']}")

        print("\n" + "=" * 70)
        print(" DIAGNOSTIC COMPLETED SUCCESSFULLY WITH ZERO ERRORS!")
        print("=" * 70)

    finally:
        db.close()


if __name__ == "__main__":
    run_diagnostics()
