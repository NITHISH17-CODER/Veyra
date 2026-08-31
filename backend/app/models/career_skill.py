"""
CareerSkill model — junction table mapping skills required for a career path.

required_level:
    1 = Beginner
    2 = Basic
    3 = Intermediate
    4 = Advanced
    5 = Expert

importance:
    1 to 5 (1 = Nice to have, 5 = Critical / Core requirement)
"""

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    CheckConstraint,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, validates

from app.database.base import Base

REQUIRED_LEVELS = {
    1: "Beginner",
    2: "Basic",
    3: "Intermediate",
    4: "Advanced",
    5: "Expert",
}


class CareerSkill(Base):
    __tablename__ = "career_skills"

    # ── Constraints applied at the table level ─────────────────────────
    __table_args__ = (
        UniqueConstraint("career_id", "skill_id", name="uq_career_skill"),
        CheckConstraint("required_level >= 1 AND required_level <= 5", name="ck_career_skill_required_level"),
        CheckConstraint("importance >= 1 AND importance <= 5", name="ck_career_skill_importance"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    career_id = Column(
        Integer,
        ForeignKey("careers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id = Column(
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    required_level = Column(Integer, nullable=False, default=1)
    importance = Column(Integer, nullable=False, default=3)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # ── Relationships ──────────────────────────────────────────────────
    # Career -> Career Skills -> Skills
    career = relationship("Career", back_populates="career_skills")
    skill = relationship("Skill", back_populates="career_skills")

    # ── Validations ────────────────────────────────────────────────────
    @validates("required_level")
    def validate_required_level(self, key, value):
        if value is None or not isinstance(value, int) or value not in REQUIRED_LEVELS:
            raise ValueError(
                f"required_level must be an integer between 1 and 5 (1=Beginner, 2=Basic, "
                f"3=Intermediate, 4=Advanced, 5=Expert). Got: {value}"
            )
        return value

    @validates("importance")
    def validate_importance(self, key, value):
        if value is None or not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError(
                f"importance must be an integer between 1 and 5 (1=Low, 5=High/Critical). Got: {value}"
            )
        return value

    @property
    def required_level_label(self) -> str:
        """Returns human-readable required level name (e.g. 'Advanced')."""
        return REQUIRED_LEVELS.get(self.required_level, "Unknown")

    def __repr__(self) -> str:
        return (
            f"<CareerSkill id={self.id} career_id={self.career_id} "
            f"skill_id={self.skill_id} required_level={self.required_level} "
            f"({self.required_level_label}) importance={self.importance}>"
        )
