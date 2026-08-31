"""
Pydantic schemas for UserSkill.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserSkillBase(BaseModel):
    skill_id: Optional[int] = Field(None, description="ID of the skill from master catalogue")
    skill_name: Optional[str] = Field(None, description="Name of skill to add/find")
    proficiency: int = Field(
        3,
        ge=1,
        le=5,
        description="Proficiency level: 1=Beginner, 2=Basic, 3=Intermediate, 4=Advanced, 5=Expert",
    )


class UserSkillCreateRequest(UserSkillBase):
    """Payload for adding a skill to current authenticated user's profile."""
    pass


class UserSkillUpdateRequest(BaseModel):
    """Payload for updating proficiency level of an existing user skill."""
    proficiency: int = Field(
        ...,
        ge=1,
        le=5,
        description="Proficiency level: 1=Beginner, 2=Basic, 3=Intermediate, 4=Advanced, 5=Expert",
    )


class UserSkillResponse(BaseModel):
    """Clean JSON response representing a user's skill."""
    id: int
    user_id: int
    skill_id: int
    skill_name: Optional[str] = None
    skill_category: Optional[str] = None
    proficiency: int
    proficiency_label: Optional[str] = None
    progress_percentage: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserSkillMessageResponse(BaseModel):
    """Generic status message response."""
    status: str = "ok"
    message: str
