"""
LearningPathItem model — ordered learning steps (courses, projects, assessments) within a path.

item_type:
    course
    project
    assessment

status:
    locked
    current
    completed
    skipped
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, validates

from app.database.base import Base

ITEM_TYPES = {"course", "project", "assessment"}
ITEM_STATUSES = {"locked", "current", "completed", "skipped"}


class LearningPathItem(Base):
    __tablename__ = "learning_path_items"

    __table_args__ = (
        UniqueConstraint("learning_path_id", "sequence_number", name="uq_path_sequence"),
        CheckConstraint("item_type IN ('course', 'project', 'assessment')", name="ck_item_type"),
        CheckConstraint("status IN ('locked', 'current', 'completed', 'skipped')", name="ck_item_status"),
        CheckConstraint("estimated_hours IS NULL OR estimated_hours >= 0", name="ck_item_estimated_hours_positive"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    learning_path_id = Column(
        Integer,
        ForeignKey("learning_paths.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_type = Column(String(50), nullable=False)  # 'course', 'project', 'assessment'
    item_id = Column(Integer, nullable=True)        # Reference to course.id, project.id, etc.
    sequence_number = Column(Integer, nullable=False, default=1)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="locked")  # 'locked', 'current', 'completed', 'skipped'
    is_locked = Column(Boolean, nullable=False, default=True)
    estimated_hours = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ── Relationships ──────────────────────────────────────────────────
    learning_path = relationship("LearningPath", back_populates="items")

    # ── Validations ────────────────────────────────────────────────────
    @validates("item_type")
    def validate_item_type(self, key, value):
        if not value or value.strip().lower() not in ITEM_TYPES:
            raise ValueError(
                f"Invalid item_type: {value}. Allowed values: {', '.join(sorted(ITEM_TYPES))}"
            )
        return value.strip().lower()

    @validates("status")
    def validate_status(self, key, value):
        if not value or value.strip().lower() not in ITEM_STATUSES:
            raise ValueError(
                f"Invalid status: {value}. Allowed values: {', '.join(sorted(ITEM_STATUSES))}"
            )
        val = value.strip().lower()
        if val == "locked":
            self.is_locked = True
        elif val in {"current", "completed", "skipped"}:
            self.is_locked = False
        return val

    @validates("title")
    def validate_title(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Item title cannot be empty.")
        return value.strip()

    @validates("sequence_number")
    def validate_sequence_number(self, key, value):
        if value is None or not isinstance(value, int) or value < 1:
            raise ValueError("sequence_number must be a positive integer >= 1.")
        return value

    def __repr__(self) -> str:
        return (
            f"<LearningPathItem id={self.id} path_id={self.learning_path_id} "
            f"seq={self.sequence_number} type={self.item_type!r} status={self.status!r}>"
        )
