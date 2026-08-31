"""
Notifications Router — Notification Center endpoints for user alerts and reminders.
"""

from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.models.user_streak import Notification, UserLearningActivity
from app.core.deps import get_current_user
from app.schemas.enhancements import NotificationResponse

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get(
    "",
    response_model=List[NotificationResponse],
    status_code=status.HTTP_200_OK,
    summary="Get user notifications",
)
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if user has performed activity today. If not, auto-generate reminder notification
    today = date.today()
    activity_today = (
        db.query(UserLearningActivity)
        .filter(
            UserLearningActivity.user_id == current_user.id,
            UserLearningActivity.activity_date == today,
        )
        .first()
    )

    if not activity_today:
        # Check if reminder already sent today
        existing_reminder = (
            db.query(Notification)
            .filter(
                Notification.user_id == current_user.id,
                Notification.type == "reminder",
                Notification.title == "Your learning progress is incomplete for today.",
            )
            .first()
        )
        if not existing_reminder:
            rem = Notification(
                user_id=current_user.id,
                type="reminder",
                title="Your learning progress is incomplete for today.",
                message="Complete a lesson or assessment today to keep your streak going!",
            )
            db.add(rem)
            db.commit()

    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(20)
        .all()
    )
    return notifications


@router.post(
    "/{notification_id}/read",
    status_code=status.HTTP_200_OK,
    summary="Mark single notification as read",
)
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notif = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found.")

    notif.is_read = True
    db.commit()
    return {"success": True, "message": "Notification marked as read."}


@router.post(
    "/read-all",
    status_code=status.HTTP_200_OK,
    summary="Mark all user notifications as read",
)
def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False,
    ).update({"is_read": True})
    db.commit()
    return {"success": True, "message": "All notifications marked as read."}
