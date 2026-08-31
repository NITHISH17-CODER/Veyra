"""
LearnerProfile model — extended profile data for personalization, background, resume, and GitHub evidence.
"""

from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, validates

from app.database.base import Base


class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    # Background fields
    current_level = Column(String(50), nullable=True)  # 'graduation' or 'job_seeker'
    education = Column(String(200), nullable=True)
    education_level = Column(String(100), nullable=True)
    field_of_study = Column(String(150), nullable=True)
    college = Column(String(255), nullable=True)
    state = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    passed_out_year = Column(Integer, nullable=True)
    
    # Experience & Goal
    experience_level = Column(String(50), nullable=True)
    career_goal_text = Column(Text, nullable=True)
    objective_text = Column(Text, nullable=True)
    target_role = Column(String(255), nullable=True)

    # Job seeker proof & evidence
    resume_url = Column(String(500), nullable=True)
    resume_text = Column(Text, nullable=True)
    resume_analysis_json = Column(JSON, nullable=True)
    resume_status = Column(String(50), default="not_uploaded", nullable=True)
    resume_error = Column(Text, nullable=True)

    github_url = Column(String(500), nullable=True)
    github_repos_json = Column(JSON, nullable=True)
    github_status = Column(String(50), default="not_connected", nullable=True)
    github_error = Column(Text, nullable=True)

    linkedin_url = Column(String(500), nullable=True)
    linkedin_text = Column(Text, nullable=True)
    linkedin_status = Column(String(50), default="not_connected", nullable=True)
    linkedin_error = Column(Text, nullable=True)

    # Preferences
    learning_hours_per_week = Column(Integer, nullable=True)
    learning_preference = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ── Relationships ──────────────────────────────────────────────────
    user = relationship("User", back_populates="learner_profile")

    # ── Validations ────────────────────────────────────────────────────
    @validates("learning_hours_per_week")
    def validate_learning_hours(self, key, hours):
        if hours is not None:
            if not isinstance(hours, int) or hours < 0 or hours > 168:
                raise ValueError("Learning hours per week must be between 0 and 168.")
        return hours

    @property
    def career_goal(self) -> str | None:
        return self.career_goal_text

    @career_goal.setter
    def career_goal(self, value: str | None):
        self.career_goal_text = value

    def __repr__(self) -> str:
        return f"<LearnerProfile id={self.id} user_id={self.user_id} current_level={self.current_level!r}>"
