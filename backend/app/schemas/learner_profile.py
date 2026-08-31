"""
Pydantic schemas for LearnerProfile.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class LearnerProfileBase(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    education: Optional[str] = Field(None, max_length=200, description="Educational background / Degree")
    education_level: Optional[str] = Field(None, max_length=100, description="Highest degree attained")
    field_of_study: Optional[str] = Field(None, max_length=150, description="Field or major / Branch")
    college: Optional[str] = Field(None, max_length=255, description="College / Institution")
    state: Optional[str] = Field(None, max_length=100, description="State")
    district: Optional[str] = Field(None, max_length=100, description="District")
    passed_out_year: Optional[int] = Field(None, description="Graduation year")
    experience_level: Optional[str] = Field(None, max_length=50, description="Beginner, Intermediate, Advanced")
    career_goal: Optional[str] = Field(None, max_length=500, description="Target career role or objective")
    objective_text: Optional[str] = Field(None, description="Detailed learning objective")
    learning_hours_per_week: Optional[int] = Field(None, ge=0, le=168, description="Target weekly learning hours (0-168)")
    learning_preference: Optional[str] = Field(None, description="Preferred learning style")


class LearnerProfileCreate(LearnerProfileBase):
    pass


class LearnerProfileUpdate(LearnerProfileBase):
    pass


class LearnerProfileResponse(LearnerProfileBase):
    id: int
    user_id: int
    avatar_url: Optional[str] = None
    learning_preference: Optional[str] = None
    github_url: Optional[str] = None
    github_status: Optional[str] = "not_connected"
    github_error: Optional[str] = None
    github_repos_json: Optional[dict | list] = None
    linkedin_url: Optional[str] = None
    linkedin_status: Optional[str] = "not_connected"
    linkedin_error: Optional[str] = None
    resume_url: Optional[str] = None
    resume_status: Optional[str] = "not_uploaded"
    resume_error: Optional[str] = None
    resume_analysis_json: Optional[dict | list] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

