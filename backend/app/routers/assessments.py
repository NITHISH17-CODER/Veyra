"""
Assessments / Quizzes Router — Personalized course-specific quizzes from MySQL DB.
Serves 10 quizzes per course x 10 questions per quiz.
"""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.database.session import get_db
from app.models.user import User
from app.models.quiz import Quiz, QuizQuestion, UserQuizAttempt
from app.models.learner_profile import LearnerProfile
from app.models.career_goal import CareerGoal
from app.models.career import Career
from app.models.skill import Skill
from app.models.user_skill import UserSkill
from app.core.deps import get_current_user

router = APIRouter(tags=["Quizzes"])


class SubmitQuizRequest(BaseModel):
    answers: Dict[str, int]  # question_id (as str) -> chosen_option_index (0-3)


def _resolve_user_course_slug(db: Session, user_id: int) -> str:
    """Finds user's active course slug based on profile/career goal."""
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == user_id).first()
    goal = db.query(CareerGoal).filter(CareerGoal.user_id == user_id).order_by(CareerGoal.created_at.desc()).first()

    raw_goal = ""
    if goal and goal.identified_career_id:
        c_obj = db.query(Career).filter(Career.id == goal.identified_career_id).first()
        if c_obj:
            raw_goal = c_obj.name
    elif profile:
        raw_goal = profile.target_role or profile.career_goal_text or ""

    g_lower = raw_goal.lower()
    if "front" in g_lower or "react" in g_lower:
        return "frontend-developer"
    elif "back" in g_lower or "node" in g_lower:
        return "backend-developer"
    elif "cyber" in g_lower or "security" in g_lower:
        return "cybersecurity"
    elif "sde" in g_lower or "software" in g_lower or "system" in g_lower:
        return "software-development-engineer"
    elif "ai" in g_lower or "ml" in g_lower or "data" in g_lower:
        return "ai-engineer"

    return "frontend-developer"


def _format_course_title(slug: str) -> str:
    mapping = {
        "frontend-developer": "Frontend Developer",
        "backend-developer": "Backend Developer",
        "cybersecurity": "Cybersecurity",
        "software-development-engineer": "Software Development Engineer (SDE)",
        "ai-engineer": "AI Engineer",
    }
    return mapping.get(slug, slug.replace("-", " ").title())


# ── GET ALL QUIZZES FOR USER'S COURSE ─────────────────────────────────────────

@router.get("/api/quizzes", status_code=status.HTTP_200_OK)
@router.get("/api/assessments", status_code=status.HTTP_200_OK)
def get_user_course_quizzes(
    course_slug: Optional[str] = Query(None, description="Optional course slug override"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target_slug = course_slug or _resolve_user_course_slug(db, current_user.id)
    course_title = _format_course_title(target_slug)

    quizzes = (
        db.query(Quiz)
        .options(joinedload(Quiz.questions))
        .filter(Quiz.course_slug == target_slug)
        .order_by(Quiz.quiz_number.asc())
        .all()
    )

    # Fetch user's previous attempts for these quizzes
    user_attempts = (
        db.query(UserQuizAttempt)
        .filter(UserQuizAttempt.user_id == current_user.id)
        .all()
    )
    attempt_map = {}
    for att in user_attempts:
        if att.quiz_id not in attempt_map or att.score > attempt_map[att.quiz_id].score:
            attempt_map[att.quiz_id] = att

    results = []
    for q in quizzes:
        att = attempt_map.get(q.id)
        results.append({
            "id": str(q.id),
            "quiz_id": q.id,
            "quiz_number": q.quiz_number,
            "course_slug": q.course_slug,
            "course_title": course_title,
            "title": q.title,
            "skillName": q.title.split(":")[-1].strip() if ":" in q.title else q.title,
            "category": course_title,
            "description": q.description,
            "timeMinutes": q.time_minutes or 15,
            "questionCount": len(q.questions) or 10,
            "difficulty": q.difficulty or "Intermediate",
            "status": "Completed" if (att and att.passed) else ("Attempted" if att else "Available"),
            "best_score": round(att.score, 1) if att else None,
            "passed": att.passed if att else False,
            "attempted_at": att.created_at.isoformat() if att else None,
        })

    return {
        "success": True,
        "course_slug": target_slug,
        "course_title": course_title,
        "total_quizzes": len(results),
        "quizzes": results,
    }


# ── GET SINGLE QUIZ BY ID (WITHOUT PRE-EXPOSING ANSWERS) ──────────────────────

@router.get("/api/quizzes/{quiz_id}", status_code=status.HTTP_200_OK)
@router.get("/api/assessments/{quiz_id}", status_code=status.HTTP_200_OK)
def get_quiz_detail(
    quiz_id: str = Path(..., description="Quiz ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Parse ID
    parsed_id = None
    if quiz_id.isdigit():
        parsed_id = int(quiz_id)
    elif quiz_id.startswith("asm-") and quiz_id[4:].isdigit():
        parsed_id = int(quiz_id[4:])

    quiz = None
    if parsed_id:
        quiz = (
            db.query(Quiz)
            .options(joinedload(Quiz.questions))
            .filter(Quiz.id == parsed_id)
            .first()
        )

    if not quiz:
        target_slug = _resolve_user_course_slug(db, current_user.id)
        quiz = (
            db.query(Quiz)
            .options(joinedload(Quiz.questions))
            .filter(Quiz.course_slug == target_slug)
            .order_by(Quiz.id.asc())
            .first()
        )

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    # Questions returned WITHOUT exposing correct_index or explanation to client
    questions_sanitized = []
    for q in quiz.questions:
        questions_sanitized.append({
            "id": str(q.id),
            "questionText": q.question_text,
            "options": q.options,
        })

    return {
        "id": str(quiz.id),
        "quiz_id": quiz.id,
        "quiz_number": quiz.quiz_number,
        "title": quiz.title,
        "course_slug": quiz.course_slug,
        "course_title": _format_course_title(quiz.course_slug),
        "skillName": quiz.title.split(":")[-1].strip() if ":" in quiz.title else quiz.title,
        "category": _format_course_title(quiz.course_slug),
        "description": quiz.description,
        "timeMinutes": quiz.time_minutes or 15,
        "questionCount": len(questions_sanitized),
        "difficulty": quiz.difficulty or "Intermediate",
        "questions": questions_sanitized,
    }


# ── SUBMIT QUIZ & EVALUATE SCORE ─────────────────────────────────────────────

@router.post("/api/quizzes/{quiz_id}/submit", status_code=status.HTTP_200_OK)
@router.post("/api/assessments/{quiz_id}/submit", status_code=status.HTTP_200_OK)
def submit_quiz_attempt(
    payload: SubmitQuizRequest,
    quiz_id: str = Path(..., description="Quiz ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    parsed_id = int(quiz_id) if quiz_id.isdigit() else 1
    quiz = (
        db.query(Quiz)
        .options(joinedload(Quiz.questions))
        .filter(Quiz.id == parsed_id)
        .first()
    )

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    questions = quiz.questions
    total_q = len(questions)
    correct_count = 0
    mistakes = []
    questions_review = []

    from app.services.course_learning_service import evaluate_question_answer

    for q in questions:
        q_key = str(q.id)
        chosen_val = payload.answers.get(q_key)
        if chosen_val is None:
            chosen_val = payload.answers.get(f"q{q.id}")
        if chosen_val is None:
            chosen_val = payload.answers.get(q.id)

        eval_res = evaluate_question_answer(
            raw_user_answer=chosen_val,
            raw_correct_answer=q.correct_index,
            options=q.options,
            question_id=q.id,
            question_text=q.question_text,
            explanation=q.explanation,
        )

        if eval_res["is_correct"]:
            correct_count += 1
        else:
            mistakes.append({
                "question_id": q.id,
                "question_text": q.question_text,
                "user_answer": eval_res["user_answer_text"],
                "correct_answer": eval_res["correct_answer_text"],
                "explanation": eval_res["explanation"],
            })

        questions_review.append(eval_res)

    score_pct = round((correct_count / max(total_q, 1)) * 100, 1)
    passed = score_pct >= 60.0

    # Save UserQuizAttempt to MySQL DB
    attempt = UserQuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=score_pct,
        total_questions=total_q,
        correct_answers=correct_count,
        passed=passed,
        submitted_answers=payload.answers,
        mistakes=mistakes,
    )
    db.add(attempt)

    # AUTOMATIC SKILL UPDATE IN MYSQL: update or insert UserSkill
    skill_name = quiz.title.split(":")[-1].strip() if ":" in quiz.title else quiz.title
    proficiency_rating = 5 if score_pct >= 90 else 4 if score_pct >= 75 else 3 if score_pct >= 60 else 2
    
    skill_obj = db.query(Skill).filter(Skill.name.ilike(f"%{skill_name}%")).first()
    if not skill_obj:
        skill_obj = Skill(name=skill_name, category=_format_course_title(quiz.course_slug), description=f"Skill: {skill_name}")
        db.add(skill_obj)
        db.flush()

    user_skill = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == current_user.id, UserSkill.skill_id == skill_obj.id)
        .first()
    )
    if user_skill:
        if proficiency_rating > user_skill.proficiency:
            user_skill.proficiency = proficiency_rating
    else:
        user_skill = UserSkill(
            user_id=current_user.id,
            skill_id=skill_obj.id,
            proficiency=proficiency_rating,
        )
        db.add(user_skill)

    db.commit()

    # Record daily activity for streak
    from app.services.streak_service import record_learning_activity
    record_learning_activity(db, current_user.id, "quiz_completed", quiz.id)

    return {
        "success": True,
        "quiz_id": quiz.id,
        "quiz_title": quiz.title,
        "course_title": _format_course_title(quiz.course_slug),
        "score": score_pct,
        "total_questions": total_q,
        "correct_answers": correct_count,
        "incorrect_answers": total_q - correct_count,
        "passed": passed,
        "skill_level": "Expert" if score_pct >= 90 else "Advanced" if score_pct >= 75 else "Intermediate" if score_pct >= 60 else "Basic",
        "mistakes": mistakes,
        "questions_review": questions_review,
        "message": f"Quiz submitted successfully! Score: {score_pct}%. Skill level updated in database.",
    }
