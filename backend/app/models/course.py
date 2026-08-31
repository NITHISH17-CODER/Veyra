"""
Course model — represents external learning resources (free and paid courses).
"""

from decimal import Decimal
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Numeric,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, validates

from app.database.base import Base


class Course(Base):
    __tablename__ = "courses"

    __table_args__ = (
        CheckConstraint("rating IS NULL OR (rating >= 0.0 AND rating <= 5.0)", name="ck_course_rating_range"),
        CheckConstraint("duration_hours IS NULL OR duration_hours >= 0", name="ck_course_duration_positive"),
        CheckConstraint("price IS NULL OR price >= 0", name="ck_course_price_positive"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    provider = Column(String(100), nullable=True)  # e.g., Coursera, Udemy, YouTube, edX
    url = Column(String(500), nullable=True)
    external_purchase_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    course_type = Column(String(20), nullable=False, default="additional")  # core or additional
    career_name = Column(String(100), nullable=True, index=True)
    is_free = Column(Boolean, nullable=False, default=True)
    price = Column(Numeric(10, 2), nullable=True, default=0.00)
    currency = Column(String(10), nullable=True, default="USD")
    difficulty = Column(String(50), nullable=True)  # Beginner, Intermediate, Advanced
    duration_hours = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ── Relationships ──────────────────────────────────────────────────
    course_skills = relationship(
        "CourseSkill",
        back_populates="course",
        cascade="all, delete-orphan",
    )
    entitlements = relationship(
        "UserCourseEntitlement",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    # ── Validations ────────────────────────────────────────────────────
    @validates("title")
    def validate_title(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Course title cannot be empty.")
        return value.strip()

    @validates("rating")
    def validate_rating(self, key, value):
        if value is not None:
            if not isinstance(value, (int, float)) or not (0.0 <= value <= 5.0):
                raise ValueError("Rating must be between 0.0 and 5.0.")
            return float(value)
        return value

    @validates("price")
    def validate_price(self, key, value):
        if value is not None:
            if isinstance(value, (int, float, str, Decimal)):
                val = Decimal(str(value))
                if val < 0:
                    raise ValueError("Course price cannot be negative.")
                return val
        return value

    def __repr__(self) -> str:
        return f"<Course id={self.id} title={self.title!r} course_type={self.course_type!r} is_free={self.is_free} price={self.price}>"


class UserCourseEntitlement(Base):
    """Tracks user access and entitlement for external/paid courses."""
    __tablename__ = "user_course_entitlements"

    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="uq_user_course_entitlement"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    purchase_status = Column(String(50), default="purchased", nullable=False)  # pending, purchased, refunded
    payment_reference = Column(String(200), nullable=True)
    purchased_at = Column(DateTime, server_default=func.now(), nullable=False)
    access_status = Column(String(50), default="active", nullable=False)  # active, expired, revoked
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    course = relationship("Course", back_populates="entitlements")

