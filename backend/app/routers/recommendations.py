import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.models.learner_profile import LearnerProfile
from app.models.learning_path import LearningPath
from app.core.deps import get_current_user

from app.ai.skill_gap import calculate_skill_gap
from app.ai.career_matcher import match_careers
from app.ai.course_recommender import recommend_courses
from app.ai.project_recommender import recommend_projects
from app.ai.roadmap_generator import generate_learning_path, get_next_best_action

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Recommendations"])


# ── Request / Response Schemas ────────────────────────────────────────────

class CareerRecommendRequest(BaseModel):
    goal: str = Field(
        ...,
        min_length=1,
        description="User's career goal, e.g. 'I want to become a Machine Learning Engineer'",
    )


class LearningPathGenerateRequest(BaseModel):
    career_id: int = Field(..., description="ID of the target career")


class SuccessResponse(BaseModel):
    success: bool = True
    data: dict | list | None = None
    message: str = ""


class ErrorResponse(BaseModel):
    success: bool = False
    message: str = ""


# ── Helper ────────────────────────────────────────────────────────────────

from app.models.career_goal import CareerGoal


def _get_active_career_id(db: Session, user_id: int) -> int | None:
    """Get career_id from user's most recent active learning path."""
    path = (
        db.query(LearningPath)
        .filter(
            LearningPath.user_id == user_id,
            LearningPath.status.in_(["active", "in_progress"]),
        )
        .order_by(LearningPath.created_at.desc())
        .first()
    )
    return path.target_career_id if path else None


def _get_career_id_from_profile_or_path(db: Session, user_id: int) -> int | None:
    """
    Determine the best career_id for the user from:
    1. Active learning path
    2. Stored CareerGoal identified career
    """
    path_career_id = _get_active_career_id(db, user_id)
    if path_career_id:
        return path_career_id

    goal_entry = (
        db.query(CareerGoal)
        .filter(CareerGoal.user_id == user_id, CareerGoal.identified_career_id.isnot(None))
        .order_by(CareerGoal.created_at.desc())
        .first()
    )
    if goal_entry and goal_entry.identified_career_id:
        return goal_entry.identified_career_id

    return None



# ── Endpoints ─────────────────────────────────────────────────────────────

@router.post(
    "/api/careers/recommend",
    status_code=status.HTTP_200_OK,
    summary="Get top career recommendations",
    description=(
        "Compares the authenticated user's skills, profile, and stated goal "
        "against all available careers and returns the top 5 matches with "
        "deterministic scoring."
    ),
)
def recommend_careers_endpoint(
    payload: CareerRecommendRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logger.info("[career_match] user_id=%s goal=%r", current_user.id, payload.goal)
    try:
        results = match_careers(
            db=db,
            user_id=current_user.id,
            goal=payload.goal,
            top_n=5,
        )
        top = results[0] if results else None
        logger.info(
            "[career_match] user_id=%s → top_career=%r career_id=%s score=%s",
            current_user.id,
            top.get("career") if top else None,
            top.get("career_id") if top else None,
            top.get("match_score") if top else None,
        )
        return {
            "success": True,
            "data": results,
            "message": f"Top {len(results)} career recommendations generated.",
        }
    except Exception as e:
        logger.exception("[career_match] FAILED user_id=%s: %s", current_user.id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate career recommendations: {str(e)}",
        )


@router.get(
    "/api/careers/{career_id}/skill-gap",
    status_code=status.HTTP_200_OK,
    summary="Get skill gap analysis for a career",
    description=(
        "Compares the authenticated user's current skills against the "
        "requirements of a specific career. Returns per-skill gaps, "
        "readiness score, and priority skills."
    ),
)
def get_skill_gap_endpoint(
    career_id: int = Path(..., description="ID of the target career"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = calculate_skill_gap(db, current_user.id, career_id)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["error"],
        )

    return {
        "success": True,
        "data": result,
        "message": f"Skill gap analysis for {result['career']} complete.",
    }


@router.get(
    "/api/courses/recommended",
    status_code=status.HTTP_200_OK,
    summary="Get personalized course recommendations",
    description=(
        "Recommends courses that close the authenticated user's skill gaps "
        "for their active career target. Requires an active learning path "
        "or a career_id query parameter."
    ),
)
def get_recommended_courses_endpoint(
    career_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Determine career_id
    effective_career_id = career_id or _get_career_id_from_profile_or_path(
        db, current_user.id
    )
    if not effective_career_id:
        logger.warning("[courses] user_id=%s has no active career_id", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "No active career target found. Please provide career_id "
                "as a query parameter or generate a learning path first."
            ),
        )

    logger.info("[courses] user_id=%s career_id=%s", current_user.id, effective_career_id)
    try:
        results = recommend_courses(
            db=db,
            user_id=current_user.id,
            career_id=effective_career_id,
            top_n=10,
        )
        logger.info("[courses] user_id=%s → %d courses returned", current_user.id, len(results))
        return {
            "success": True,
            "data": results,
            "message": f"{len(results)} courses recommended.",
        }
    except Exception as e:
        logger.exception("[courses] FAILED user_id=%s: %s", current_user.id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate course recommendations: {str(e)}",
        )


@router.get(
    "/api/projects/recommended",
    status_code=status.HTTP_200_OK,
    summary="Get personalized project recommendations",
    description=(
        "Recommends projects that strengthen the authenticated user's "
        "missing skills for their active career target."
    ),
)
def get_recommended_projects_endpoint(
    career_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    effective_career_id = career_id or _get_career_id_from_profile_or_path(
        db, current_user.id
    )
    if not effective_career_id:
        logger.warning("[projects] user_id=%s has no active career_id", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "No active career target found. Please provide career_id "
                "as a query parameter or generate a learning path first."
            ),
        )

    logger.info("[projects] user_id=%s career_id=%s", current_user.id, effective_career_id)
    try:
        results = recommend_projects(
            db=db,
            user_id=current_user.id,
            career_id=effective_career_id,
            top_n=5,
        )
        logger.info("[projects] user_id=%s → %d projects returned", current_user.id, len(results))
        return {
            "success": True,
            "data": results,
            "message": f"{len(results)} projects recommended.",
        }
    except Exception as e:
        logger.exception("[projects] FAILED user_id=%s: %s", current_user.id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate project recommendations: {str(e)}",
        )


@router.post(
    "/api/learning-path/generate",
    status_code=status.HTTP_201_CREATED,
    summary="Generate a personalized learning path",
    description=(
        "Generates a sequenced learning path for the authenticated user "
        "targeting a specific career. Analyzes skill gaps, orders courses "
        "and projects by prerequisite dependencies, and persists the path "
        "to MySQL. Replaces any existing active path for the same career."
    ),
)
def generate_learning_path_endpoint(
    payload: LearningPathGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate learning path: {str(e)}",
        )


@router.get(
    "/api/learning-path/next-action",
    status_code=status.HTTP_200_OK,
    summary="Get the next best action",
    description=(
        "Returns the single next best action for the authenticated user "
        "based on their active learning path."
    ),
)
def get_next_action_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = get_next_best_action(db, current_user.id)

    if not result:
        return {
            "success": True,
            "data": None,
            "message": "No active learning path found. Generate one first.",
        }

    logger.info(
        "[next_action] user_id=%s → title=%r type=%s priority=%s",
        current_user.id, result.get("title"), result.get("type"), result.get("priority")
    )
    return {
        "success": True,
        "data": result,
        "message": f"Next action: {result['title']}",
    }


# ── DEV-ONLY: Debug endpoint ──────────────────────────────────────────────────

from app.models.user_skill import UserSkill
from app.models.career_skill import CareerSkill
from app.models.course import Course
from app.models.project import Project
from app.models.career import Career


@router.get(
    "/api/debug/recommendation-state",
    status_code=status.HTTP_200_OK,
    summary="[DEV ONLY] Recommendation pipeline state",
    description=(
        "Development-only endpoint. Returns a safe summary of the recommendation "
        "pipeline state for the authenticated user. Does NOT return passwords, "
        "tokens, or any sensitive information."
    ),
    tags=["Debug"],
)
def debug_recommendation_state(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """DEV-ONLY: safe summary of the recommendation pipeline state."""
    profile = (
        db.query(LearnerProfile)
        .filter(LearnerProfile.user_id == current_user.id)
        .first()
    )
    career_id = _get_career_id_from_profile_or_path(db, current_user.id)
    career_name = None
    if career_id:
        c = db.query(Career).filter(Career.id == career_id).first()
        career_name = c.name if c else None

    user_skill_count = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).count()
    career_skill_count = (
        db.query(CareerSkill).filter(CareerSkill.career_id == career_id).count()
        if career_id else 0
    )

    gap_count = None
    course_candidate_count = None
    project_candidate_count = None
    if career_id:
        gap_data = calculate_skill_gap(db, current_user.id, career_id)
        if "error" not in gap_data:
            gap_count = gap_data["gap_count"]
        courses = recommend_courses(db, current_user.id, career_id, top_n=50)
        course_candidate_count = len(courses)
        projects = recommend_projects(db, current_user.id, career_id, top_n=20)
        project_candidate_count = len(projects)

    return {
        "_note": "DEV-ONLY endpoint. Do not expose in production.",
        "user_id": current_user.id,
        "user_name": current_user.name,
        "goal": profile.career_goal_text if profile else None,
        "has_profile": profile is not None,
        "career_id": career_id,
        "career": career_name,
        "user_skill_count": user_skill_count,
        "career_skill_count": career_skill_count,
        "skill_gap_count": gap_count,
        "course_candidate_count": course_candidate_count,
        "project_candidate_count": project_candidate_count,
    }
