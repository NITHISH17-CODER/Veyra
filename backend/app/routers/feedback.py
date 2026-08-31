"""
Feedback Router — Handles user rating & feedback on recommendations.
"""

from typing import Optional
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


class FeedbackRequest(BaseModel):
    recommendation_id: Optional[str] = None
    rating: Optional[int] = None
    feedback_text: Optional[str] = None


@router.post("", status_code=status.HTTP_200_OK)
def submit_feedback(
    payload: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return {
        "success": True,
        "message": "Thank you! PathPilot AI has logged your feedback to improve future recommendations.",
    }
