"""
Pydantic schemas for Authentication (Register, Login, Token, and Auth Response).
"""

import re
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    """Payload for user registration."""
    name: str = Field(..., max_length=100, description="Full name of the user")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=128, description="Password (min 8 characters)")
    confirm_password: Optional[str] = Field(None, description="Confirmation password")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        trimmed = v.strip()
        if len(trimmed) < 2:
            raise ValueError("Full Name must be at least 2 characters and cannot be only whitespace.")
        return trimmed

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if (
            len(v) < 8
            or not re.search(r"[A-Z]", v)
            or not re.search(r"[a-z]", v)
            or not re.search(r"\d", v)
            or not re.search(r"[^A-Za-z0-9]", v)
        ):
            raise ValueError("Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character.")
        return v


class UserLoginRequest(BaseModel):
    """Payload for user login."""
    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., min_length=1, max_length=128, description="Account password")


class UserResponse(BaseModel):
    """User profile information returned in auth responses."""
    id: int
    name: str
    email: EmailStr
    onboarding_completed: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """JWT Access Token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class AuthErrorResponse(BaseModel):
    """Standardized error response format."""
    success: bool = False
    code: str
    message: str
    errors: Optional[Dict[str, str]] = None

