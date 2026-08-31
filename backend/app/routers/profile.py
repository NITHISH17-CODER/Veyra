"""
Profile Router — Learner Profile onboarding, photo management, evidence verification, and profile CRUD endpoints.
"""

import os
import re
import time
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.models.learner_profile import LearnerProfile
from app.models.user_preference import UserPreference
from app.core.deps import get_current_user
from app.schemas.learner_profile import (
    LearnerProfileCreate,
    LearnerProfileUpdate,
    LearnerProfileResponse,
)
from app.ai.github_analyzer import analyze_github_profile
from app.ai.resume_analyzer import extract_text_from_file_content, analyze_resume_text

router = APIRouter(prefix="/api/profile", tags=["Profile"])

LINKEDIN_URL_REGEX = re.compile(
    r"^https?://([a-z0-9]+\.)?linkedin\.com/in/[A-Za-z0-9_.-]+/?$",
    re.IGNORECASE
)


class GitHubVerificationRequest(BaseModel):
    github_url: str


class LinkedInVerificationRequest(BaseModel):
    linkedin_url: str


def _format_profile_response(profile: LearnerProfile, user: User) -> LearnerProfileResponse:
    """Helper to attach user-level attributes to profile response."""
    res_dict = LearnerProfileResponse.model_validate(profile).model_dump()
    res_dict["full_name"] = user.name
    res_dict["avatar_url"] = user.avatar_url
    res_dict["career_goal"] = profile.career_goal_text
    return LearnerProfileResponse(**res_dict)


@router.get(
    "",
    response_model=LearnerProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user's learner profile",
    description="Retrieves the onboarding/learner profile of the authenticated user. If missing, creates a default profile.",
)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearnerProfile(
            user_id=current_user.id,
            current_level="graduation",
            learning_hours_per_week=10,
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return _format_profile_response(profile, current_user)


@router.post(
    "",
    response_model=LearnerProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create learner profile for current user",
)
def create_profile(
    payload: LearnerProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_profile = (
        db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    )
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user. Use PUT /api/profile to update.",
        )

    if payload.full_name and payload.full_name.strip():
        current_user.name = payload.full_name.strip()

    new_profile = LearnerProfile(
        user_id=current_user.id,
        education=payload.education,
        field_of_study=payload.field_of_study,
        college=payload.college,
        state=payload.state,
        district=payload.district,
        passed_out_year=payload.passed_out_year,
        experience_level=payload.experience_level,
        career_goal_text=payload.career_goal,
        objective_text=payload.objective_text,
        learning_hours_per_week=payload.learning_hours_per_week,
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return _format_profile_response(new_profile, current_user)


@router.put(
    "",
    response_model=LearnerProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update current user's learner profile",
)
def update_profile(
    payload: LearnerProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id)
        db.add(profile)

    # Update full_name on User model if provided
    if payload.full_name is not None and payload.full_name.strip():
        current_user.name = payload.full_name.strip()

    # Update LearnerProfile fields
    if payload.education is not None: profile.education = payload.education.strip()
    if payload.field_of_study is not None: profile.field_of_study = payload.field_of_study.strip()
    if payload.college is not None: profile.college = payload.college.strip()
    if payload.state is not None: profile.state = payload.state.strip()
    if payload.district is not None: profile.district = payload.district.strip()
    if payload.passed_out_year is not None: profile.passed_out_year = payload.passed_out_year
    if payload.experience_level is not None: profile.experience_level = payload.experience_level.strip()
    if payload.career_goal is not None: profile.career_goal_text = payload.career_goal.strip()
    if payload.objective_text is not None: profile.objective_text = payload.objective_text.strip()
    if payload.learning_preference is not None: profile.learning_preference = payload.learning_preference.strip()

    if payload.learning_hours_per_week is not None:
        profile.learning_hours_per_week = payload.learning_hours_per_week
        # Sync with UserPreference table as single source of truth
        user_pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
        if not user_pref:
            user_pref = UserPreference(
                user_id=current_user.id,
                learning_hours_per_week=payload.learning_hours_per_week,
            )
            db.add(user_pref)
        else:
            user_pref.learning_hours_per_week = payload.learning_hours_per_week

    db.commit()
    db.refresh(profile)
    db.refresh(current_user)

    return _format_profile_response(profile, current_user)


# ── Profile Photo Endpoints ──────────────────────────────────────────────────

@router.post(
    "/photo",
    response_model=LearnerProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload profile photo",
)
async def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    allowed_exts = (".jpg", ".jpeg", ".png", ".webp", ".gif")
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail="Invalid image format. Allowed formats: JPG, PNG, WebP, GIF."
        )

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:  # 5MB limit
        raise HTTPException(status_code=400, detail="Image size exceeds 5MB limit.")

    os.makedirs("uploads/avatars", exist_ok=True)
    filename = f"avatar_{current_user.id}_{int(time.time())}{ext}"
    filepath = os.path.join("uploads/avatars", filename)

    with open(filepath, "wb") as f:
        f.write(content)

    avatar_url = f"/uploads/avatars/{filename}"
    current_user.avatar_url = avatar_url
    db.commit()

    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return _format_profile_response(profile, current_user)


@router.delete(
    "/photo",
    response_model=LearnerProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Remove profile photo",
)
def remove_photo(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.avatar_url = None
    db.commit()

    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return _format_profile_response(profile, current_user)


# ── Evidence Verification Endpoints ──────────────────────────────────────────

@router.post(
    "/github",
    response_model=LearnerProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify and analyze GitHub profile evidence",
)
def verify_github(
    payload: GitHubVerificationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    clean_url = payload.github_url.strip()
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id)
        db.add(profile)

    analysis = analyze_github_profile(clean_url)
    if not analysis.get("valid"):
        profile.github_url = clean_url
        profile.github_status = "failed"
        profile.github_error = analysis.get("error", "Invalid GitHub profile URL.")
        db.commit()
        return _format_profile_response(profile, current_user)

    profile.github_url = clean_url
    profile.github_status = "connected"
    profile.github_error = None
    profile.github_repos_json = analysis.get("repos", [])
    db.commit()
    db.refresh(profile)

    return _format_profile_response(profile, current_user)


@router.post(
    "/linkedin",
    response_model=LearnerProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify LinkedIn profile evidence",
)
def verify_linkedin(
    payload: LinkedInVerificationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    clean_url = payload.linkedin_url.strip()
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id)
        db.add(profile)

    if not LINKEDIN_URL_REGEX.match(clean_url):
        profile.linkedin_url = clean_url
        profile.linkedin_status = "failed"
        profile.linkedin_error = "Invalid LinkedIn profile URL. Must be in format: https://www.linkedin.com/in/username"
        db.commit()
        return _format_profile_response(profile, current_user)

    profile.linkedin_url = clean_url
    profile.linkedin_status = "connected"
    profile.linkedin_error = None
    db.commit()
    db.refresh(profile)

    return _format_profile_response(profile, current_user)


@router.post(
    "/resume",
    response_model=LearnerProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload and analyze resume evidence",
)
async def verify_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    allowed_exts = (".pdf", ".docx", ".doc", ".txt")
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a PDF, DOCX, or TXT file."
        )

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=400, detail="File size exceeds maximum 10MB limit.")

    os.makedirs("uploads/resumes", exist_ok=True)
    filename = f"resume_{current_user.id}_{int(time.time())}{ext}"
    filepath = os.path.join("uploads/resumes", filename)

    with open(filepath, "wb") as f:
        f.write(content)

    extracted_text = extract_text_from_file_content(content, file.filename)
    analysis = analyze_resume_text(extracted_text)

    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id)
        db.add(profile)

    if not extracted_text or not extracted_text.strip():
        profile.resume_url = f"/uploads/resumes/{filename}"
        profile.resume_status = "failed"
        profile.resume_error = "Could not extract readable text from resume file."
        db.commit()
        return _format_profile_response(profile, current_user)

    profile.resume_url = f"/uploads/resumes/{filename}"
    profile.resume_text = extracted_text
    profile.resume_analysis_json = analysis
    profile.resume_status = "verified"
    profile.resume_error = None
    db.commit()
    db.refresh(profile)

    return _format_profile_response(profile, current_user)
