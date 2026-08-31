"""
Skill model — master catalogue of skills / technologies.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship, validates

from app.database.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # ── Relationships ──────────────────────────────────────────────────
    # One-to-many relationship with UserSkill
    user_skills = relationship(
        "UserSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )

    # One-to-many relationship with CareerSkill (Career -> Career Skills -> Skills)
    career_skills = relationship(
        "CareerSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )

    # One-to-many relationship with CourseSkill (Course -> Course Skills -> Skills)
    course_skills = relationship(
        "CourseSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )

    # One-to-many relationship with ProjectSkill (Project -> Project Skills -> Skills)
    project_skills = relationship(
        "ProjectSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )

    # ── Validations ────────────────────────────────────────────────────
    @validates("name")
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Skill name cannot be empty.")
        return value.strip()

    def __repr__(self) -> str:
        return f"<Skill id={self.id} name={self.name!r}>"
