"""
Onboarding Schemas — Request and response validation for conversational onboarding workflow.
"""

from typing import List, Optional, Union, Any, Dict
from pydantic import BaseModel, Field


class OnboardingSkillItem(BaseModel):
    name: str = Field(..., description="Skill name, e.g. 'Python'")
    proficiency: Union[int, str] = Field(
        3,
        description="Proficiency level (1-5) or label ('Beginner', 'Basic', 'Intermediate', 'Advanced', 'Expert')",
    )
    source: Optional[str] = Field("manual", description="Source of skill evidence: 'manual', 'resume', 'github', 'linkedin', 'assessment'")
    evidence_text: Optional[str] = None
    confidence_score: Optional[float] = 1.0


class OnboardingInterestItem(BaseModel):
    name: str = Field(..., description="Interest domain or custom interest, e.g. 'Cybersecurity'")
    category: Optional[str] = None
    custom: Optional[bool] = False


class OnboardingRequest(BaseModel):
    current_level: Optional[str] = Field("graduation", description="'graduation' or 'job_seeker'")
    full_name: Optional[str] = Field(None, description="User full name")
    
    # Graduation Flow Fields
    education: Optional[str] = Field(None, description="Degree, e.g. B.Tech, BCA, MCA")
    education_level: Optional[str] = Field(None, description="Bachelor's, Master's, etc.")
    field_of_study: Optional[str] = Field(None, description="Branch/specialization e.g. Computer Science")
    college: Optional[str] = Field(None, description="College or University name")
    state: Optional[str] = Field(None, description="State of location")
    district: Optional[str] = Field(None, description="District of location")
    passed_out_year: Optional[int] = Field(None, description="Year of graduation")

    # Job Seeker Flow Fields & Evidence
    target_role: Optional[str] = Field(None, description="Target job role natural text")
    resume_url: Optional[str] = Field(None, description="Uploaded resume URL")
    resume_text: Optional[str] = Field(None, description="Extracted plain text from resume")
    github_url: Optional[str] = Field(None, description="GitHub profile URL")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    linkedin_text: Optional[str] = Field(None, description="Pasted LinkedIn experience/about text")

    # Goals, Interests & Preferences
    experience_level: Optional[str] = Field("Intermediate")
    career_goal: Optional[str] = Field(None, description="Natural language goal")
    objective: Optional[str] = Field(None, description="Optional goal objective")
    interests: List[Union[str, OnboardingInterestItem]] = Field(default=[])
    skills: List[Union[dict, OnboardingSkillItem]] = Field(default=[])
    learning_hours_per_week: Optional[int] = Field(10, ge=1, le=168)
    learning_style: Optional[str] = Field("Project-based")
    difficulty_preference: Optional[str] = Field("Intermediate")
    learning_mode: Optional[str] = Field("Self-paced")
    resource_preference: Optional[str] = Field("All")
    selected_career_id: Optional[int] = Field(None, description="Explicit selected career ID")


class OnboardingResponse(BaseModel):
    success: bool = True
    user_id: int
    profile_id: int
    career_goal: Optional[Dict[str, Any]] = None
    matched_careers: List[Dict[str, Any]] = []
    target_career: Optional[Dict[str, Any]] = None
    skill_gap: Optional[Dict[str, Any]] = None
    learning_path: Optional[Dict[str, Any]] = None
    next_best_action: Optional[Dict[str, Any]] = None
    message: str = "Onboarding completed successfully."
