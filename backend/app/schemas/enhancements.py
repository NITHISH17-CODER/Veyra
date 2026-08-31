"""
Pydantic schemas for Streak, Notifications, and Certificates.
"""

from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class StreakResponse(BaseModel):
    current_streak: int = 0
    longest_streak: int = 0
    earned_today: bool = False
    last_activity_date: Optional[date] = None
    message: str = "Keep learning daily to build your streak!"


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CertificateResponse(BaseModel):
    id: int
    certificate_id: str
    user_id: int
    course_name: str
    certificate_type: str
    verification_code: str
    issued_at: datetime
    metadata_json: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class CertificateVerifyResponse(BaseModel):
    is_valid: bool
    certificate_id: str
    student_name: str
    course_name: str
    certificate_type: str
    issued_at: datetime
    status: str = "VERIFIED"
