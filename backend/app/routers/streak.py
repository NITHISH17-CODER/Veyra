"""
Streak Router — retrieves current streak, longest streak, and earned_today state.
"""

from datetime import date
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.enhancements import StreakResponse
from app.services.streak_service import get_or_create_streak

router = APIRouter(prefix="/api/streak", tags=["Streak & Activity"])


@router.get(
    "",
    response_model=StreakResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user streak state",
)
def get_streak(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    streak = get_or_create_streak(db, current_user.id)
    earned_today = streak.last_activity_date == date.today()

    msg = f"You are on a {streak.current_streak}-day learning streak!" if streak.current_streak > 0 else "Complete today's lesson to start your streak!"

    return StreakResponse(
        current_streak=streak.current_streak,
        longest_streak=streak.longest_streak,
        earned_today=earned_today,
        last_activity_date=streak.last_activity_date,
        message=msg,
    )
