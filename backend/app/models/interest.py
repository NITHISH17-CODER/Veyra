"""
Interest model — master catalogue of interest topics / domains.
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationship to user interests
    user_interests = relationship(
        "UserInterest",
        back_populates="interest",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Interest id={self.id} name={self.name!r}>"
