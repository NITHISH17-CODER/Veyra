"""
CareerGoal model — preserves user's raw natural language goal and AI interpretation.
"""

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class CareerGoal(Base):
    __tablename__ = "career_goals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    raw_goal = Column(Text, nullable=False)
    identified_career_id = Column(
        Integer,
        ForeignKey("careers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="career_goals")
    identified_career = relationship("Career")

    def __repr__(self) -> str:
        return f"<CareerGoal id={self.id} user_id={self.user_id} raw_goal={self.raw_goal[:30]!r}>"
