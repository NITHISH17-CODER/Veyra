"""
Pydantic schemas for User.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


class UserRead(UserBase):
    id: int
    onboarding_completed: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
