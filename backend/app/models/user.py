"""
User model — core account table.
"""

import re
from sqlalchemy import Column, Integer, String, DateTime, Boolean, text, func
from sqlalchemy.orm import relationship, validates

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    onboarding_completed = Column(Boolean, default=False, server_default=text("0"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ── Relationships ──────────────────────────────────────────────────
    # One-to-one relationship with LearnerProfile
    learner_profile = relationship(
        "LearnerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # One-to-one relationship with UserPreference
    user_preference = relationship(
        "UserPreference",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # One-to-many relationship with UserSkill
    user_skills = relationship(
        "UserSkill",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # One-to-many relationship with UserInterest
    user_interests = relationship(
        "UserInterest",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # One-to-many relationship with CareerGoal
    career_goals = relationship(
        "CareerGoal",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # One-to-many relationship with LearningPath
    learning_paths = relationship(
        "LearningPath",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Streak & Learning Activity relationships
    learning_activities = relationship(
        "UserLearningActivity",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    streak = relationship(
        "UserStreak",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    certificates = relationship(
        "Certificate",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # ── Validations ────────────────────────────────────────────────────
    @validates("email")
    def validate_email(self, key, address):
        if not address or not isinstance(address, str):
            raise ValueError("Email address cannot be empty.")
        cleaned = address.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", cleaned):
            raise ValueError(f"Invalid email address format: {address}")
        return cleaned

    @validates("name")
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("User name cannot be empty.")
        return value.strip()

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"
