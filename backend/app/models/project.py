"""
Project model — represents hands-on portfolio projects for skill application.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    JSON,
    CheckConstraint,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, validates

from app.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    __table_args__ = (
        CheckConstraint("estimated_hours IS NULL OR estimated_hours >= 0", name="ck_project_estimated_hours_positive"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    difficulty = Column(String(50), nullable=True)  # Beginner, Intermediate, Advanced
    level = Column(String(50), nullable=True, default="BEGINNER")  # BEGINNER, INTERMEDIATE, ADVANCED, CAPSTONE
    career_name = Column(String(100), nullable=True, index=True)  # Associated career (e.g. Frontend Developer)
    prerequisites_json = Column(JSON, nullable=True)  # list of {skill_name, min_proficiency}
    learning_outcomes = Column(JSON, nullable=True)  # list of strings
    milestones_json = Column(JSON, nullable=True)  # list of {step, description}
    objectives_json = Column(JSON, nullable=True)  # list of objectives
    technologies_json = Column(JSON, nullable=True)  # list of technologies
    requirements_json = Column(JSON, nullable=True)  # list of requirements
    estimated_hours = Column(Float, nullable=True)
    github_url = Column(String(500), nullable=True)
    dataset_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ── Relationships ──────────────────────────────────────────────────
    project_skills = relationship(
        "ProjectSkill",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    user_progress = relationship(
        "UserProjectProgress",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    # ── Validations ────────────────────────────────────────────────────
    @validates("title")
    def validate_title(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Project title cannot be empty.")
        return value.strip()

    @validates("estimated_hours")
    def validate_estimated_hours(self, key, value):
        if value is not None:
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError("Estimated hours must be a positive number.")
            return float(value)
        return value

    def __repr__(self) -> str:
        return f"<Project id={self.id} title={self.title!r} level={self.level!r} career_name={self.career_name!r}>"


class UserProjectProgress(Base):
    """Tracks a user's progress on hands-on portfolio projects."""
    __tablename__ = "user_project_progress"

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_user_project"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="available", nullable=False)  # locked, available, in_progress, completed
    progress_percentage = Column(Float, default=0.0, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    submission_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    missing_requirements = Column(JSON, nullable=True)
    technical_feedback = Column(Text, nullable=True)
    recommended_improvements = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("Project", back_populates="user_progress")

