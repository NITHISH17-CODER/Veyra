"""
Streak & Learning Activity Service — handles date-based streak increments, missed day resets, and automatic notifications.
"""

from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.models.user_streak import UserStreak, UserLearningActivity, Notification
from app.models.user import User


def get_or_create_streak(db: Session, user_id: int) -> UserStreak:
    """Retrieves or initializes the streak record for a user (brand new user starts at 0)."""
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    if not streak:
        streak = UserStreak(
            user_id=user_id,
            current_streak=0,
            longest_streak=0,
            last_activity_date=None,
        )
        db.add(streak)
        db.commit()
        db.refresh(streak)
    else:
        # Check missed calendar day evaluation on read
        today = date.today()
        if streak.last_activity_date:
            days_diff = (today - streak.last_activity_date).days
            if days_diff > 1:
                # Missed a calendar day — reset current streak to 0
                streak.current_streak = 0
                db.commit()
                db.refresh(streak)
    return streak


def record_learning_activity(
    db: Session,
    user_id: int,
    activity_type: str,
    reference_id: str | int | None = None,
) -> dict:
    """
    Records a qualifying completed learning activity.
    Increments streak ONLY IF this is the first qualifying activity for today.
    Returns streak status dictionary including earned_today flag.
    """
    today = date.today()

    # Log the specific activity entry
    act = UserLearningActivity(
        user_id=user_id,
        activity_date=today,
        activity_type=activity_type,
        reference_id=str(reference_id) if reference_id else None,
        completed_at=datetime.now(),
    )
    db.add(act)

    # Fetch streak record
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    if not streak:
        streak = UserStreak(
            user_id=user_id,
            current_streak=0,
            longest_streak=0,
            last_activity_date=None,
        )
        db.add(streak)
        db.flush()

    earned_today = False

    if streak.last_activity_date == today:
        # User already performed an activity today — streak remains same
        earned_today = False
    else:
        earned_today = True
        if streak.last_activity_date == today - timedelta(days=1):
            streak.current_streak += 1
        else:
            streak.current_streak = 1

        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak

        streak.last_activity_date = today

        # Auto-create a notification celebrating the milestone
        notif = Notification(
            user_id=user_id,
            type="streak",
            title=f"🔥 {streak.current_streak} Day Streak!",
            message=f"You completed today's learning activity! You're on a {streak.current_streak}-day streak.",
        )
        db.add(notif)

    db.commit()
    db.refresh(streak)

    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "earned_today": earned_today,
        "last_activity_date": streak.last_activity_date,
    }
