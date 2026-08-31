"""
UserSkill model — junction table linking users to skills with proficiency and multi-source evidence tracking.

Proficiency levels:
    1 = Beginner
    2 = Basic
    3 = Intermediate
    4 = Advanced
    5 = Expert
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    ForeignKey,
    DateTime,
    CheckConstraint,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, validates

from app.database.base import Base

PROFICIENCY_LEVELS = {
    1: "Beginner",
    2: "Basic",
    3: "Intermediate",
    4: "Advanced",
    5: "Expert",
}


class UserSkill(Base):
    __tablename__ = "user_skills"

    # ── Constraints applied at the table level ─────────────────────────
    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill"),
        CheckConstraint("proficiency >= 1 AND proficiency <= 5", name="ck_proficiency_range"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id = Column(
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    proficiency = Column(Integer, nullable=False, default=1)
    
    # Skill Evidence Tracking
    source = Column(String(50), nullable=True, default="manual")  # 'manual', 'resume', 'github', 'linkedin', 'assessment'
    evidence_text = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True, default=1.0)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ── Relationships ──────────────────────────────────────────────────
    user = relationship("User", back_populates="user_skills")
    skill = relationship("Skill", back_populates="user_skills")

    # ── Validations ────────────────────────────────────────────────────
    @validates("proficiency")
    def validate_proficiency(self, key, value):
        if value is None or not isinstance(value, int) or value not in PROFICIENCY_LEVELS:
            raise ValueError(
                f"Proficiency must be an integer between 1 and 5 (1=Beginner, 2=Basic, "
                f"3=Intermediate, 4=Advanced, 5=Expert). Got: {value}"
            )
        return value

    @property
    def proficiency_label(self) -> str:
        """Returns human-readable proficiency name (e.g., 'Beginner')."""
        return PROFICIENCY_LEVELS.get(self.proficiency, "Unknown")

    @property
    def skill_name(self) -> str | None:
        """Returns name of related skill."""
        return self.skill.name if self.skill else None

    @property
    def skill_category(self) -> str | None:
        """Returns category of related skill."""
        return self.skill.category if self.skill else None

    def __repr__(self) -> str:
        return (
            f"<UserSkill id={self.id} user_id={self.user_id} "
            f"skill_id={self.skill_id} proficiency={self.proficiency} source={self.source!r}>"
        )
