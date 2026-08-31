"""
LearningPath model — personalized career-aligned roadmap generated for a user.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import relationship, validates

from app.database.base import Base

LEARNING_PATH_STATUSES = {"draft", "active", "in_progress", "completed", "archived"}


class LearningPath(Base):
    __tablename__ = "learning_paths"

    __table_args__ = (
        CheckConstraint("readiness_score IS NULL OR (readiness_score >= 0.0 AND readiness_score <= 100.0)", name="ck_path_readiness_score"),
        CheckConstraint("estimated_months IS NULL OR estimated_months >= 0", name="ck_path_estimated_months_positive"),
        CheckConstraint("weekly_hours IS NULL OR weekly_hours >= 0", name="ck_path_weekly_hours_positive"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_career_id = Column(
        Integer,
        ForeignKey("careers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    estimated_months = Column(Float, nullable=True)
    weekly_hours = Column(Float, nullable=True)
    readiness_score = Column(Float, nullable=True)  # e.g., 0.0 to 100.0 (%)
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ── Relationships ──────────────────────────────────────────────────
    user = relationship("User", back_populates="learning_paths")
    target_career = relationship("Career", back_populates="learning_paths")
    items = relationship(
        "LearningPathItem",
        back_populates="learning_path",
        order_by="LearningPathItem.sequence_number",
        cascade="all, delete-orphan",
    )

    # ── Validations ────────────────────────────────────────────────────
    @validates("title")
    def validate_title(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Learning path title cannot be empty.")
        return value.strip()

    @validates("status")
    def validate_status(self, key, value):
        if value is not None:
            val = value.strip().lower()
            if val not in LEARNING_PATH_STATUSES:
                raise ValueError(
                    f"Invalid status: {value}. Allowed values: {', '.join(sorted(LEARNING_PATH_STATUSES))}"
                )
            return val
        return "active"

    @validates("readiness_score")
    def validate_readiness_score(self, key, value):
        if value is not None:
            if not isinstance(value, (int, float)) or not (0.0 <= value <= 100.0):
                raise ValueError("Readiness score must be between 0.0 and 100.0.")
            return float(value)
        return value

    def __repr__(self) -> str:
        return f"<LearningPath id={self.id} user_id={self.user_id} title={self.title!r} status={self.status!r}>"
