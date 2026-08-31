"""
User Skills Router — User-specific skill competencies & proficiency ratings.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session, joinedload

from app.database.session import get_db
from app.models.user import User
from app.models.skill import Skill
from app.models.user_skill import UserSkill
from app.core.deps import get_current_user
from app.schemas.user_skill import (
    UserSkillCreateRequest,
    UserSkillUpdateRequest,
    UserSkillResponse,
    UserSkillMessageResponse,
)

from app.models.course_learning import CourseModule, CourseLesson, UserLessonProgress, UserModuleProgress


def calculate_user_skill_progress(db: Session, user_id: int, skill_id: int, proficiency: int) -> int:
    """
    Calculates user-specific skill progress percentage (0-100%) based on:
    - Onboarding skill level: Basic=25%, Intermediate=50%, Advanced=75%, Expert=100%
    - Completed course activity in MySQL (lessons & assessments covering this skill)
    """
    if not proficiency or proficiency <= 0:
        base_pct = 0
    elif proficiency == 1:
        base_pct = 20
    elif proficiency == 2:
        base_pct = 25
    elif proficiency == 3:
        base_pct = 50
    elif proficiency == 4:
        base_pct = 75
    elif proficiency >= 5:
        base_pct = 100

    if base_pct >= 100:
        return 100

    skill_obj = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill_obj:
        return base_pct

    skill_name = skill_obj.name.lower()

    # Find modules covering this skill
    all_modules = db.query(CourseModule).filter(CourseModule.skills != None).all()
    relevant_module_ids = []
    for mod in all_modules:
        mod_skills = [s.lower() for s in (mod.skills or [])]
        if any(skill_name in s or s in skill_name for s in mod_skills):
            relevant_module_ids.append(mod.id)

    if not relevant_module_ids:
        return base_pct

    # Count completed lessons
    completed_lessons = (
        db.query(UserLessonProgress)
        .join(CourseLesson)
        .filter(
            UserLessonProgress.user_id == user_id,
            UserLessonProgress.is_completed == True,
            CourseLesson.module_id.in_(relevant_module_ids),
        )
        .count()
    )

    # Count passed assessments
    passed_assessments = (
        db.query(UserModuleProgress)
        .filter(
            UserModuleProgress.user_id == user_id,
            UserModuleProgress.assessment_passed == True,
            UserModuleProgress.module_id.in_(relevant_module_ids),
        )
        .count()
    )

    activity_boost = (completed_lessons * 10) + (passed_assessments * 15)
    return min(100, base_pct + activity_boost)


router = APIRouter(prefix="/api/user-skills", tags=["User Skills"])


@router.get(
    "",
    response_model=List[UserSkillResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all skills for the current user",
    description="Retrieves all skills and proficiency levels belonging to the authenticated user. User ID is extracted from the JWT token.",
)
def get_user_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    skills = (
        db.query(UserSkill)
        .options(joinedload(UserSkill.skill))
        .filter(UserSkill.user_id == current_user.id)
        .order_by(UserSkill.id.asc())
        .all()
    )

    for us in skills:
        us.progress_percentage = calculate_user_skill_progress(
            db, current_user.id, us.skill_id, us.proficiency
        )

    return skills


@router.post(
    "",
    response_model=UserSkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add or update a skill in current user's profile",
    description="Adds a skill with proficiency (1=Beginner to 5=Expert) to the authenticated user's profile.",
)
def add_user_skill(
    payload: UserSkillCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    skill = None
    if payload.skill_id:
        skill = db.query(Skill).filter(Skill.id == payload.skill_id).first()

    if not skill and payload.skill_name and payload.skill_name.strip():
        name_clean = payload.skill_name.strip()
        skill = db.query(Skill).filter(Skill.name.ilike(name_clean)).first()
        if not skill:
            skill = Skill(name=name_clean, category="General", description=f"Skill: {name_clean}")
            db.add(skill)
            db.flush()

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill name or valid skill_id must be provided.",
        )

    # Check if user already has this skill
    user_skill = (
        db.query(UserSkill)
        .filter(
            UserSkill.user_id == current_user.id,
            UserSkill.skill_id == skill.id,
        )
        .first()
    )

    if user_skill:
        user_skill.proficiency = payload.proficiency
    else:
        user_skill = UserSkill(
            user_id=current_user.id,
            skill_id=skill.id,
            proficiency=payload.proficiency,
        )
        db.add(user_skill)

    db.commit()
    db.refresh(user_skill)

    # Load relationship for proper Pydantic serialization
    user_skill = (
        db.query(UserSkill)
        .options(joinedload(UserSkill.skill))
        .filter(UserSkill.id == user_skill.id)
        .first()
    )

    return user_skill


@router.put(
    "/{id}",
    response_model=UserSkillResponse,
    status_code=status.HTTP_200_OK,
    summary="Update proficiency for a user skill",
    description="Updates proficiency rating (1=Beginner to 5=Expert) for a specific user skill belonging to the authenticated user.",
)
def update_user_skill(
    id: int = Path(..., description="ID of the user_skill record to update"),
    payload: UserSkillUpdateRequest = ...,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_skill = (
        db.query(UserSkill)
        .options(joinedload(UserSkill.skill))
        .filter(
            UserSkill.id == id,
            UserSkill.user_id == current_user.id,
        )
        .first()
    )

    if not user_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User skill not found or does not belong to you.",
        )

    user_skill.proficiency = payload.proficiency
    db.commit()
    db.refresh(user_skill)

    return user_skill


@router.delete(
    "/{id}",
    response_model=UserSkillMessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a user skill",
    description="Removes a skill from the authenticated user's profile.",
)
def delete_user_skill(
    id: int = Path(..., description="ID of the user_skill record to delete"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_skill = (
        db.query(UserSkill)
        .filter(
            UserSkill.id == id,
            UserSkill.user_id == current_user.id,
        )
        .first()
    )

    if not user_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User skill not found or does not belong to you.",
        )

    db.delete(user_skill)
    db.commit()

    return UserSkillMessageResponse(
        status="ok",
        message="User skill deleted successfully.",
    )
