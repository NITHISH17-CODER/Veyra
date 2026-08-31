"""
Learning Path Router — GET /api/learning-path endpoint for fetching active roadmap,
POST /api/learning-path/generate for generating a new path,
GET /api/learning-path/next-action for the next best action.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from app.database.session import get_db
from app.models.user import User
from app.models.learning_path import LearningPath
from app.models.learning_path_item import LearningPathItem
from app.models.career import Career
from app.models.career_goal import CareerGoal
from app.models.learner_profile import LearnerProfile
from app.core.deps import get_current_user
from app.ai.skill_gap import calculate_skill_gap
from app.ai.roadmap_generator import generate_learning_path, get_next_best_action

router = APIRouter(prefix="/api/learning-path", tags=["Learning Path"])


class LearningPathGenerateRequest(BaseModel):
    career_id: int


def _resolve_user_career_id(db: Session, user_id: int) -> int:
    """Finds user's selected or identified career_id, or defaults to 1."""
    goal = (
        db.query(CareerGoal)
        .filter(CareerGoal.user_id == user_id, CareerGoal.identified_career_id.isnot(None))
        .order_by(CareerGoal.created_at.desc())
        .first()
    )
    if goal and goal.identified_career_id:
        return goal.identified_career_id

    c = db.query(Career).first()
    return c.id if c else 1


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get active learning path for current user",
    description="Retrieves the active learning path and items for the authenticated user. Generates one automatically if none exists.",
)
def get_active_learning_path(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    path = (
        db.query(LearningPath)
        .options(
            joinedload(LearningPath.target_career),
            joinedload(LearningPath.items),
        )
        .filter(
            LearningPath.user_id == current_user.id,
            LearningPath.status.in_(["active", "in_progress"]),
        )
        .order_by(LearningPath.created_at.desc())
        .first()
    )

    # Strict No-Default Rule: Check if user has completed onboarding / profile setup
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile or not (profile.career_goal_text or profile.current_level):
        return {
            "success": True,
            "data": None,
            "message": "Complete your profile to generate your personalized learning path.",
        }

    # Auto-generate roadmap if user completed onboarding but path not yet stored
    if not path:
        target_career_id = _resolve_user_career_id(db, current_user.id)
        gen_res = generate_learning_path(db, current_user.id, target_career_id)
        if "error" in gen_res:
            return {
                "success": True,
                "data": None,
                "message": "Complete your profile to generate your personalized learning path.",
            }
        
        path = (
            db.query(LearningPath)
            .options(
                joinedload(LearningPath.target_career),
                joinedload(LearningPath.items),
            )
            .filter(
                LearningPath.user_id == current_user.id,
                LearningPath.status.in_(["active", "in_progress"]),
            )
            .order_by(LearningPath.created_at.desc())
            .first()
        )

    career_name = path.target_career.name if path and path.target_career else "General"
    career_id = path.target_career_id if path else None

    # Resolve course track in database matching user career
    from app.models.course_learning import CourseTrack, CourseModule, CourseLesson, UserLessonProgress
    
    # Find matching course track by name or fallback
    c_lower = (career_name or "").lower()
    course_track = None
    if "front" in c_lower or "react" in c_lower:
        course_track = db.query(CourseTrack).filter(CourseTrack.slug == "frontend-developer").first()
    elif "back" in c_lower or "node" in c_lower or "python" in c_lower:
        course_track = db.query(CourseTrack).filter(CourseTrack.slug == "backend-developer").first()
    elif "cyber" in c_lower or "security" in c_lower:
        course_track = db.query(CourseTrack).filter(CourseTrack.slug == "cybersecurity").first()
    elif "sde" in c_lower or "software" in c_lower or "system" in c_lower:
        course_track = db.query(CourseTrack).filter(CourseTrack.slug == "software-development-engineer").first()
    elif "ai" in c_lower or "ml" in c_lower or "data" in c_lower:
        course_track = db.query(CourseTrack).filter(CourseTrack.slug == "ai-engineer").first()

    if not course_track:
        course_track = db.query(CourseTrack).first()

    weekly_hours = (profile.learning_hours_per_week if profile else 10) or 10

    # Build Phased sequence directly from MySQL course track modules and lessons
    modules = (
        db.query(CourseModule)
        .options(joinedload(CourseModule.lessons))
        .filter(CourseModule.course_id == course_track.id)
        .order_by(CourseModule.module_number.asc())
        .all()
    )

    completed_lesson_ids = set(
        row[0] for row in db.query(UserLessonProgress.lesson_id)
        .filter(UserLessonProgress.user_id == current_user.id, UserLessonProgress.is_completed == True)
        .all()
    )

    phases_dict = {}
    items_data = []
    seq_counter = 1
    first_uncompleted = False

    for mod in modules:
        phase = mod.phase_name or "Phase 1: Foundations"
        if phase not in phases_dict:
            phases_dict[phase] = {
                "phase_name": phase,
                "modules": []
            }
        
        topics_list = []
        for lsn in mod.lessons:
            is_done = lsn.id in completed_lesson_ids
            if is_done:
                status = "completed"
            elif not first_uncompleted:
                status = "current"
                first_uncompleted = True
            else:
                status = "locked"

            t_obj = {
                "id": lsn.id,
                "lesson_id": lsn.id,
                "module_id": mod.id,
                "course_slug": course_track.slug,
                "title": lsn.title,
                "description": lsn.description or f"Master {lsn.title}",
                "is_completed": is_done,
                "status": status,
                "video_duration": lsn.video_duration,
                "has_coding": bool(lsn.has_coding),
            }
            topics_list.append(t_obj)

        phases_dict[phase]["modules"].append({
            "module_id": mod.id,
            "module_number": mod.module_number,
            "title": mod.title,
            "description": mod.description,
            "estimated_hours": mod.estimated_hours,
            "topics": topics_list,
        })

        mod_completed = len(topics_list) > 0 and all(t["is_completed"] for t in topics_list)
        mod_current = any(t["status"] == "current" for t in topics_list)

        items_data.append({
            "id": mod.id,
            "sequence_number": f"{seq_counter:02d}",
            "title": mod.title,
            "description": mod.description,
            "status": "completed" if mod_completed else ("current" if mod_current else "locked"),
            "is_locked": not (mod_completed or mod_current),
            "estimated_hours": mod.estimated_hours,
            "topics": [t["title"] for t in topics_list],
            "topic_details": topics_list,
        })
        seq_counter += 1

    phases_list = list(phases_dict.values())

    # Recalculate progress readiness score based strictly on actual completed lessons in MySQL
    total_lessons_count = sum(len(m.lessons) for m in modules)
    completed_lessons_count = len(completed_lesson_ids)
    readiness_score = round((completed_lessons_count / total_lessons_count) * 100) if total_lessons_count > 0 else 0

    ready_skills = []
    if career_id:
        gap_data = calculate_skill_gap(db, current_user.id, career_id)
        if "error" not in gap_data:
            ready_skills = [s["skill"] for s in gap_data["skills"] if s["status"] == "ready"]

    return {
        "success": True,
        "data": {
            "learning_path_id": path.id if path else None,
            "title": f"Personalized Path: {course_track.title}",
            "description": f"Personalized sequence created for {course_track.title} based on your background and profile.",
            "career": course_track.career_name,
            "career_id": career_id,
            "course_slug": course_track.slug,
            "readiness_score": readiness_score,
            "estimated_months": round(sum(m.estimated_hours for m in modules) / max(weekly_hours * 4.33, 1), 1),
            "weekly_hours": weekly_hours,
            "status": path.status if path else "active",
            "total_items": len(items_data),
            "ready_skills": ready_skills,
            "phases": phases_list,
            "items": items_data,
        },
        "message": "Active learning path retrieved successfully.",
    }


@router.post(
    "/generate",
    status_code=status.HTTP_201_CREATED,
    summary="Generate a personalized learning path",
)
def generate_learning_path_route(
    payload: LearningPathGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = generate_learning_path(
        db=db,
        user_id=current_user.id,
        career_id=payload.career_id,
    )

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["error"],
        )

    return {
        "success": True,
        "data": result,
        "message": f"Learning path '{result['title']}' generated with {result['total_items']} items.",
    }


@router.get(
    "/next-action",
    status_code=status.HTTP_200_OK,
    summary="Get the next best action",
)
def get_next_action_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    action = get_next_best_action(db, current_user.id)
    return {
        "success": True,
        "data": action,
        "message": "Next best action retrieved successfully."
    }
