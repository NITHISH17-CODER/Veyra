"""
User Lesson Code Model — Stores saved code snippets per user and lesson.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base import Base


class UserLessonCode(Base):
    """Tracks saved draft/submitted code for interactive coding lessons."""
    __tablename__ = "user_lesson_code"
    __table_args__ = (
        UniqueConstraint('user_id', 'lesson_id', name='uq_user_lesson_code'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("course_lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    language = Column(String(50), nullable=False, default="python")
    version = Column(String(50), nullable=True)
    code = Column(Text, nullable=False)
    stdin = Column(Text, nullable=True, default="")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User")
    lesson = relationship("CourseLesson")
