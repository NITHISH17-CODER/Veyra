"""
CourseSkill model — junction table linking courses to skills with coverage level.

coverage_level:
    1 to 5 (1 = Introductory, 2 = Basic, 3 = Moderate, 4 = Comprehensive, 5 = Deep Dive)
"""

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, validates

from app.database.base import Base

COVERAGE_LEVELS = {
    1: "Introductory",
    2: "Basic",
    3: "Moderate",
    4: "Comprehensive",
    5: "Deep Dive",
}


class CourseSkill(Base):
    __tablename__ = "course_skills"

    # ── Constraints applied at the table level ─────────────────────────
    __table_args__ = (
        UniqueConstraint("course_id", "skill_id", name="uq_course_skill"),
        CheckConstraint("coverage_level >= 1 AND coverage_level <= 5", name="ck_course_skill_coverage_level"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id = Column(
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    coverage_level = Column(Integer, nullable=False, default=1)

    # ── Relationships ──────────────────────────────────────────────────
    # Course -> Course Skills -> Skills
    course = relationship("Course", back_populates="course_skills")
    skill = relationship("Skill", back_populates="course_skills")

    # ── Validations ────────────────────────────────────────────────────
    @validates("coverage_level")
    def validate_coverage_level(self, key, value):
        if value is None or not isinstance(value, int) or value not in COVERAGE_LEVELS:
            raise ValueError(
                f"coverage_level must be an integer between 1 and 5 (1=Introductory, 2=Basic, "
                f"3=Moderate, 4=Comprehensive, 5=Deep Dive). Got: {value}"
            )
        return value

    @property
    def coverage_label(self) -> str:
        """Returns human-readable coverage label (e.g. 'Comprehensive')."""
        return COVERAGE_LEVELS.get(self.coverage_level, "Unknown")

    def __repr__(self) -> str:
        return (
            f"<CourseSkill id={self.id} course_id={self.course_id} "
            f"skill_id={self.skill_id} coverage_level={self.coverage_level} ({self.coverage_label})>"
        )
