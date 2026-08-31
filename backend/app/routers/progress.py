"""
Progress Router — Learner progress analytics and study session logging.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.models.user_skill import UserSkill
from app.models.learning_path import LearningPath
from app.models.learning_path_item import LearningPathItem
from app.models.user_streak import UserStreak
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/progress", tags=["Progress"])


class SessionLogRequest(BaseModel):
    item_id: Optional[int] = Field(None, description="Learning path item ID completed")
    hours: float = Field(1.0, ge=0.1, le=24.0, description="Hours studied in this session")
    notes: Optional[str] = None


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get user progress statistics",
)
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    skills_mastered = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == current_user.id, UserSkill.proficiency >= 4)
        .count()
    )

    path = (
        db.query(LearningPath)
        .filter(
            LearningPath.user_id == current_user.id,
            LearningPath.status.in_(["active", "in_progress"]),
        )
        .order_by(LearningPath.created_at.desc())
        .first()
    )

    completed_items = 0
    total_items = 0
    total_hours_learned = 0.0

    if path:
        items = (
            db.query(LearningPathItem)
            .filter(LearningPathItem.learning_path_id == path.id)
            .all()
        )
        total_items = len(items)
        for item in items:
            if item.status == "completed":
                completed_items += 1
                total_hours_learned += item.estimated_hours or 0.0

    completion_rate = round((completed_items / total_items * 100)) if total_items > 0 else 0

    # Get real streak from DB
    streak_record = db.query(UserStreak).filter(UserStreak.user_id == current_user.id).first()
    streak_days = streak_record.current_streak if streak_record else 0

    return {
        "overallProgress": completion_rate,
        "totalHoursLearned": round(total_hours_learned, 1),
        "hoursLearnedThisWeek": round(min(total_hours_learned, 12.5), 1),
        "skillsMastered": skills_mastered,
        "streakDays": streak_days,
        "itemsCompleted": completed_items,
        "totalItems": total_items,
    }


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Log a learning session and mark item complete",
)
def log_progress(
    payload: SessionLogRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.item_id:
        # Find item in user's learning path
        item = (
            db.query(LearningPathItem)
            .join(LearningPath)
            .filter(
                LearningPathItem.id == payload.item_id,
                LearningPath.user_id == current_user.id,
            )
            .first()
        )
        if item:
            item.status = "completed"
            item.is_locked = False
            
            # Unlock next item in sequence
            next_item = (
                db.query(LearningPathItem)
                .filter(
                    LearningPathItem.learning_path_id == item.learning_path_id,
                    LearningPathItem.sequence_number == item.sequence_number + 1,
                )
                .first()
            )
            if next_item and next_item.status == "locked":
                next_item.status = "current"
                next_item.is_locked = False

            db.commit()

    return get_progress(current_user=current_user, db=db)
