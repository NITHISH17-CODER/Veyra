"""
Career model — represents career tracks / paths (e.g. AI Engineer, Full Stack Developer).
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship, validates

from app.database.base import Base


class Career(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    difficulty = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ── Relationships ──────────────────────────────────────────────────
    # One-to-many relationship with CareerSkill (Career -> Career Skills -> Skills)
    career_skills = relationship(
        "CareerSkill",
        back_populates="career",
        cascade="all, delete-orphan",
    )

    # One-to-many relationship with LearningPath
    learning_paths = relationship(
        "LearningPath",
        back_populates="target_career",
    )

    # ── Validations ────────────────────────────────────────────────────
    @validates("name")
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Career name cannot be empty.")
        return value.strip()

    def __repr__(self) -> str:
        return f"<Career id={self.id} name={self.name!r}>"
