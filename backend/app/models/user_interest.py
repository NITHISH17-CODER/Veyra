"""
UserInterest model — junction table linking users to selected interests or custom interests.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class UserInterest(Base):
    __tablename__ = "user_interests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    interest_id = Column(
        Integer,
        ForeignKey("interests.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    custom_interest = Column(String(150), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="user_interests")
    interest = relationship("Interest", back_populates="user_interests")

    @property
    def name(self) -> str:
        """Returns the interest name (master catalog name or custom interest string)."""
        if self.interest and self.interest.name:
            return self.interest.name
        return self.custom_interest or ""

    def __repr__(self) -> str:
        return f"<UserInterest id={self.id} user_id={self.user_id} interest={self.name!r}>"
