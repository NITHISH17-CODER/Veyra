"""
ProjectSkill model — junction table linking projects to skills with importance.

importance:
    1 to 5 (1 = Supporting, 2 = Useful, 3 = Important, 4 = Key, 5 = Core / Essential)
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

IMPORTANCE_LEVELS = {
    1: "Supporting",
    2: "Useful",
    3: "Important",
    4: "Key",
    5: "Core / Essential",
}


class ProjectSkill(Base):
    __tablename__ = "project_skills"

    # ── Constraints applied at the table level ─────────────────────────
    __table_args__ = (
        UniqueConstraint("project_id", "skill_id", name="uq_project_skill"),
        CheckConstraint("importance >= 1 AND importance <= 5", name="ck_project_skill_importance"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id = Column(
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    importance = Column(Integer, nullable=False, default=3)

    # ── Relationships ──────────────────────────────────────────────────
    # Project -> Project Skills -> Skills
    project = relationship("Project", back_populates="project_skills")
    skill = relationship("Skill", back_populates="project_skills")

    # ── Validations ────────────────────────────────────────────────────
    @validates("importance")
    def validate_importance(self, key, value):
        if value is None or not isinstance(value, int) or value not in IMPORTANCE_LEVELS:
            raise ValueError(
                f"importance must be an integer between 1 and 5 (1=Supporting, 2=Useful, "
                f"3=Important, 4=Key, 5=Core / Essential). Got: {value}"
            )
        return value

    @property
    def importance_label(self) -> str:
        """Returns human-readable importance name (e.g. 'Core / Essential')."""
        return IMPORTANCE_LEVELS.get(self.importance, "Unknown")

    def __repr__(self) -> str:
        return (
            f"<ProjectSkill id={self.id} project_id={self.project_id} "
            f"skill_id={self.skill_id} importance={self.importance} ({self.importance_label})>"
        )
