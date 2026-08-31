"""
UserPreference model — stores personalized learning preferences.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, validates

from app.database.base import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    learning_hours_per_week = Column(Integer, nullable=False, default=10)
    learning_style = Column(String(50), nullable=False, default="Project-based")
    difficulty_preference = Column(String(50), nullable=False, default="Intermediate")
    learning_mode = Column(String(50), nullable=True, default="Self-paced")
    resource_preference = Column(String(100), nullable=True, default="All")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationship to user
    user = relationship("User", back_populates="user_preference")

    @validates("learning_hours_per_week")
    def validate_hours(self, key, hours):
        if hours is not None:
            if not isinstance(hours, int) or hours < 1 or hours > 168:
                raise ValueError("Learning hours per week must be between 1 and 168.")
        return hours

    def __repr__(self) -> str:
        return f"<UserPreference id={self.id} user_id={self.user_id} hours={self.learning_hours_per_week}>"
