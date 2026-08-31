"""
Models for User Learning Activity, Streak Tracking, Notifications, and Certificates.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    JSON,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class UserLearningActivity(Base):
    """Stores daily qualifying learning activity records (lesson completed, assessment passed, etc.)."""
    __tablename__ = "user_learning_activity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_date = Column(Date, nullable=False, index=True)
    activity_type = Column(String(50), nullable=False)  # lesson_completed, assessment_completed, project_completed
    reference_id = Column(String(100), nullable=True)
    completed_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="learning_activities")


class UserStreak(Base):
    """Tracks daily consecutive learning streak for a user."""
    __tablename__ = "user_streaks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    last_activity_date = Column(Date, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="streak")


class Notification(Base):
    """User notification center records."""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(50), default="info", nullable=False)  # streak, learning, assessment, project, certificate
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="notifications")


class Certificate(Base):
    """Official Course, Project, and Overall PathPilot Certificates."""
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    certificate_id = Column(String(100), unique=True, nullable=False, index=True)  # e.g. PP-2026-FE-000123
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_name = Column(String(255), nullable=False)
    certificate_type = Column(String(50), nullable=False)  # course, project, overall
    verification_code = Column(String(100), unique=True, nullable=False)
    issued_at = Column(DateTime, server_default=func.now(), nullable=False)
    metadata_json = Column(JSON, nullable=True)

    user = relationship("User", back_populates="certificates")
