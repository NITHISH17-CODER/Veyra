"""
Pydantic schemas for Skill.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str | None = Field(None, max_length=100)
    description: str | None = None


class SkillCreate(SkillBase):
    pass


class SkillRead(SkillBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SkillUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    category: str | None = Field(None, max_length=100)
    description: str | None = None
