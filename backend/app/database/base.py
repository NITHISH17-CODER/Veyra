"""
Declarative Base for all SQLAlchemy ORM models.

Every model file should import Base from here:

    from app.database.base import Base

    class User(Base):
        __tablename__ = "users"
        ...
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
