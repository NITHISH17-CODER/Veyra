"""
Onboarding Router — Transactional onboarding API, interest catalogue, resume parsing, 
GitHub profile analysis, and user preferences.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from app.database.session import get_db
from app.models.user import User
from app.models.learner_profile import LearnerProfile
from app.models.user_preference import UserPreference
from app.models.interest import Interest
from app.models.user_interest import UserInterest
from app.models.skill import Skill
from app.models.user_skill import UserSkill, PROFICIENCY_LEVELS
from app.models.career import Career
from app.models.career_goal import CareerGoal
from app.models.learning_path import LearningPath
from app.core.deps import get_current_user
from app.schemas.onboarding import OnboardingRequest, OnboardingResponse
from app.ai.career_matcher import match_careers, _is_unspecified_goal
from app.ai.skill_gap import calculate_skill_gap
from app.ai.roadmap_generator import generate_learning_path, get_next_best_action
from app.ai.resume_analyzer import extract_text_from_file_content, analyze_resume_text
from app.ai.github_analyzer import analyze_github_profile

router = APIRouter(tags=["Onboarding & Profile"])

_PROFICIENCY_LABEL_MAP = {
    "beginner": 1,
    "basic": 2,
    "intermediate": 3,
    "advanced": 4,
    "expert": 5,
}


def _parse_proficiency(val: int | str | None) -> int:
    if isinstance(val, int):
        return max(1, min(5, val))
    if isinstance(val, str):
        cleaned = val.strip().lower()
        if cleaned in _PROFICIENCY_LABEL_MAP:
            return _PROFICIENCY_LABEL_MAP[cleaned]
        try:
            num = int(cleaned)
            return max(1, min(5, num))
        except ValueError:
            pass
    return 3


class GitHubAnalysisRequest(BaseModel):
    github_url: str


# ── 1. Resume Upload & Analysis Endpoint ───────────────────────────────────

@router.post(
    "/api/onboarding/resume",
    status_code=status.HTTP_200_OK,
    summary="Upload and analyze resume text",
)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    allowed_exts = (".pdf", ".docx", ".doc", ".txt")
    if not file.filename.lower().endswith(allowed_exts):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a PDF or DOCX file."
        )

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=400, detail="File size exceeds maximum 10MB limit.")

    extracted_text = extract_text_from_file_content(content, file.filename)
    analysis = analyze_resume_text(extracted_text)

    # Save to user profile
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id)
        db.add(profile)

    profile.resume_url = f"/uploads/resumes/{file.filename}"
    profile.resume_text = extracted_text
    profile.resume_analysis_json = analysis
    db.commit()

    return {
        "success": True,
        "filename": file.filename,
        "analysis": analysis,
        "message": "Resume uploaded and analyzed successfully."
    }


# ── 2. GitHub Profile Analysis Endpoint ─────────────────────────────────────

@router.post(
    "/api/onboarding/github",
    status_code=status.HTTP_200_OK,
    summary="Validate and analyze GitHub profile",
)
def analyze_github(
    payload: GitHubAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analysis = analyze_github_profile(payload.github_url)
    if not analysis.get("valid"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=analysis.get("error", "Invalid GitHub profile URL.")
        )

    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id)
        db.add(profile)

    profile.github_url = payload.github_url.strip()
    profile.github_repos_json = analysis.get("repos", [])
    db.commit()

    return {
        "success": True,
        "data": analysis,
        "message": analysis.get("message", "GitHub profile analyzed successfully.")
    }


class StepSaveRequest(BaseModel):
    step: int
    full_name: Optional[str] = None
    current_level: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    college: Optional[str] = None
    passed_out_year: Optional[int] = None
    natural_goal: Optional[str] = None
    target_role: Optional[str] = None
    skills: Optional[List[Dict[str, Any]]] = None


@router.get(
    "/api/onboarding/status",
    status_code=status.HTTP_200_OK,
    summary="Get user onboarding progress and current allowed step",
)
def get_onboarding_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    
    # Calculate highest valid completed step
    current_step = 1
    if current_user.name and len(current_user.name.strip()) >= 2:
        current_step = 2
    if profile and profile.current_level in ["graduation", "job_seeker"]:
        current_step = 3
    if profile and (
        (profile.current_level == "graduation" and profile.education and profile.field_of_study) or
        (profile.current_level == "job_seeker" and profile.target_role)
    ):
        current_step = 4
    
    user_skills_count = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).count()
    if current_step == 4 and user_skills_count > 0:
        current_step = 5

    if current_user.onboarding_completed:
        current_step = 5

    return {
        "success": True,
        "onboarding_completed": current_user.onboarding_completed,
        "max_allowed_step": current_step,
        "profile": {
            "full_name": current_user.name,
            "current_level": profile.current_level if profile else "graduation",
            "degree": profile.education if profile else "",
            "branch": profile.field_of_study if profile else "",
            "college": profile.college if profile else "",
            "passed_out_year": profile.passed_out_year if profile else None,
            "target_role": profile.target_role if profile else "",
            "career_goal": profile.career_goal_text if profile else "",
        } if profile else {"full_name": current_user.name}
    }


@router.post(
    "/api/onboarding/step",
    status_code=status.HTTP_200_OK,
    summary="Validate and save progress for a specific onboarding step",
)
def save_onboarding_step(
    payload: StepSaveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id, current_level="graduation")
        db.add(profile)

    # Validate Step 1: Full Name
    if payload.step >= 1:
        if payload.full_name is not None:
            name_val = payload.full_name.strip()
            if not name_val or len(name_val) < 2:
                raise HTTPException(status_code=400, detail="Step 1 Invalid: Full Name must be at least 2 characters.")
            current_user.name = name_val

    # Validate Step 2: Journey / Current Level
    if payload.step >= 2:
        if not current_user.name or len(current_user.name.strip()) < 2:
            raise HTTPException(status_code=400, detail="Cannot proceed to Step 2 before completing Step 1 (Full Name).")
        if payload.current_level:
            if payload.current_level not in ["graduation", "job_seeker"]:
                raise HTTPException(status_code=400, detail="Step 2 Invalid: Select Graduation or Job Seeker.")
            profile.current_level = payload.current_level

    # Validate Step 3: Flow Details
    if payload.step >= 3:
        if not profile.current_level:
            raise HTTPException(status_code=400, detail="Cannot proceed to Step 3 before completing Step 2 (Journey background).")
        if profile.current_level == "graduation":
            if payload.degree: profile.education = payload.degree.strip()
            if payload.branch: profile.field_of_study = payload.branch.strip()
            if payload.college: profile.college = payload.college.strip()
            if payload.passed_out_year: profile.passed_out_year = payload.passed_out_year
            if payload.natural_goal: profile.career_goal_text = payload.natural_goal.strip()
        else:
            if payload.target_role: profile.target_role = payload.target_role.strip()

    db.commit()
    return {"success": True, "message": f"Step {payload.step} data validated and saved."}


# ── 3. Comprehensive Onboarding Endpoint ───────────────────────────────────

@router.post(
    "/api/onboarding",
    response_model=OnboardingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Save all onboarding information and generate personalized path",
)
def complete_onboarding(
    payload: OnboardingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        # Update user name if provided
        if payload.full_name and payload.full_name.strip():
            current_user.name = payload.full_name.strip()

        # Step A: Save / Upsert LearnerProfile
        profile = (
            db.query(LearnerProfile)
            .filter(LearnerProfile.user_id == current_user.id)
            .first()
        )
        if not profile:
            profile = LearnerProfile(
                user_id=current_user.id,
                current_level=payload.current_level or "graduation",
                education=payload.education,
                education_level=payload.education_level,
                field_of_study=payload.field_of_study,
                college=payload.college,
                state=payload.state,
                district=payload.district,
                passed_out_year=payload.passed_out_year,
                experience_level=payload.experience_level,
                career_goal_text=payload.career_goal,
                objective_text=payload.objective,
                target_role=payload.target_role,
                resume_url=payload.resume_url,
                resume_text=payload.resume_text,
                github_url=payload.github_url,
                linkedin_url=payload.linkedin_url,
                linkedin_text=payload.linkedin_text,
                learning_hours_per_week=payload.learning_hours_per_week,
                learning_preference=payload.learning_style,
            )
            db.add(profile)
        else:
            profile.current_level = payload.current_level or profile.current_level or "graduation"
            profile.education = payload.education or profile.education
            profile.education_level = payload.education_level or profile.education_level
            profile.field_of_study = payload.field_of_study or profile.field_of_study
            profile.college = payload.college or profile.college
            profile.state = payload.state or profile.state
            profile.district = payload.district or profile.district
            profile.passed_out_year = payload.passed_out_year or profile.passed_out_year
            profile.experience_level = payload.experience_level or profile.experience_level
            profile.career_goal_text = payload.career_goal or profile.career_goal_text
            profile.objective_text = payload.objective or profile.objective_text
            profile.target_role = payload.target_role or profile.target_role
            profile.resume_url = payload.resume_url or profile.resume_url
            profile.resume_text = payload.resume_text or profile.resume_text
            profile.github_url = payload.github_url or profile.github_url
            profile.linkedin_url = payload.linkedin_url or profile.linkedin_url
            profile.linkedin_text = payload.linkedin_text or profile.linkedin_text
            profile.learning_hours_per_week = payload.learning_hours_per_week or profile.learning_hours_per_week
            profile.learning_preference = payload.learning_style or profile.learning_preference

        db.flush()

        # Step B: Save / Upsert UserPreferences
        prefs = (
            db.query(UserPreference)
            .filter(UserPreference.user_id == current_user.id)
            .first()
        )
        if not prefs:
            prefs = UserPreference(
                user_id=current_user.id,
                learning_hours_per_week=payload.learning_hours_per_week or 10,
                learning_style=payload.learning_style or "Project-based",
                difficulty_preference=payload.difficulty_preference or "Intermediate",
                learning_mode=payload.learning_mode or "Self-paced",
                resource_preference=payload.resource_preference or "All",
            )
            db.add(prefs)
        else:
            prefs.learning_hours_per_week = payload.learning_hours_per_week or prefs.learning_hours_per_week
            prefs.learning_style = payload.learning_style or prefs.learning_style
            prefs.difficulty_preference = payload.difficulty_preference or prefs.difficulty_preference

        db.flush()

        # Step C: Save User Interests
        db.query(UserInterest).filter(UserInterest.user_id == current_user.id).delete()
        processed_interest_names: list[str] = []
        for int_item in payload.interests:
            int_name = int_item.name if hasattr(int_item, "name") else str(int_item)
            if not int_name or not int_name.strip():
                continue
            int_name = int_name.strip()
            processed_interest_names.append(int_name)

            matched_interest = (
                db.query(Interest)
                .filter(Interest.name.ilike(int_name))
                .first()
            )
            if matched_interest:
                db.add(UserInterest(user_id=current_user.id, interest_id=matched_interest.id, custom_interest=None))
            else:
                db.add(UserInterest(user_id=current_user.id, interest_id=None, custom_interest=int_name))

        db.flush()

        # Step D: Save User Skills (Multi-source evidence preserved)
        db.query(UserSkill).filter(UserSkill.user_id == current_user.id).delete()

        for sk_item in payload.skills:
            if isinstance(sk_item, dict):
                sk_name = sk_item.get("name") or sk_item.get("skill_name") or ""
                sk_prof = sk_item.get("proficiency", 3)
                sk_src = sk_item.get("source", "manual")
                sk_ev = sk_item.get("evidence_text")
                sk_conf = sk_item.get("confidence_score", 1.0)
            else:
                sk_name = sk_item.name
                sk_prof = sk_item.proficiency
                sk_src = getattr(sk_item, "source", "manual")
                sk_ev = getattr(sk_item, "evidence_text", None)
                sk_conf = getattr(sk_item, "confidence_score", 1.0)

            if not sk_name or not sk_name.strip():
                continue

            sk_name = sk_name.strip()
            prof_int = _parse_proficiency(sk_prof)

            matched_skill = (
                db.query(Skill)
                .filter(Skill.name.ilike(sk_name))
                .first()
            )
            if not matched_skill:
                matched_skill = Skill(name=sk_name, category="General", description=f"Skill: {sk_name}")
                db.add(matched_skill)
                db.flush()

            db.add(UserSkill(
                user_id=current_user.id,
                skill_id=matched_skill.id,
                proficiency=prof_int,
                source=sk_src,
                evidence_text=sk_ev,
                confidence_score=sk_conf,
            ))

        db.flush()

        # Step E: AI Career Matching (strictly 5 core careers)
        matched_careers = match_careers(
            db=db,
            user_id=current_user.id,
            goal=payload.career_goal,
            target_role=payload.target_role,
            interests=processed_interest_names,
            education_field=payload.field_of_study,
            experience=payload.experience_level,
            top_n=5,
        )

        target_career_id = payload.selected_career_id
        target_career_obj = None

        if target_career_id:
            target_career_obj = db.query(Career).filter(Career.id == target_career_id).first()

        if not target_career_obj and matched_careers:
            top_match = matched_careers[0]
            target_career_id = top_match["career_id"]
            target_career_obj = db.query(Career).filter(Career.id == target_career_id).first()

        # Step F: Save CareerGoal Record
        confidence = matched_careers[0]["match_score"] / 100.0 if matched_careers else 0.85
        career_goal_entry = CareerGoal(
            user_id=current_user.id,
            raw_goal=payload.career_goal or payload.target_role or (target_career_obj.name if target_career_obj else "Undecided"),
            identified_career_id=target_career_id,
            confidence_score=confidence,
        )
        db.add(career_goal_entry)
        db.flush()

        # Step G: Calculate Skill Gaps & Generate Learning Path
        skill_gap_result = None
        learning_path_result = None
        next_action_result = None

        if target_career_id:
            skill_gap_result = calculate_skill_gap(db, current_user.id, target_career_id)
            learning_path_result = generate_learning_path(db, current_user.id, target_career_id)
            next_action_result = get_next_best_action(db, current_user.id)

        current_user.onboarding_completed = True
        db.add(current_user)
        db.commit()
        db.refresh(profile)

        target_career_data = None
        if target_career_obj:
            target_career_data = {
                "id": target_career_obj.id,
                "name": target_career_obj.name,
                "description": target_career_obj.description,
                "difficulty": target_career_obj.difficulty,
            }

        return OnboardingResponse(
            success=True,
            user_id=current_user.id,
            profile_id=profile.id,
            career_goal={
                "raw_goal": career_goal_entry.raw_goal,
                "identified_career": target_career_obj.name if target_career_obj else None,
                "confidence_score": confidence,
            },
            matched_careers=matched_careers,
            target_career=target_career_data,
            skill_gap=skill_gap_result,
            learning_path=learning_path_result,
            next_best_action=next_action_result,
            message="Onboarding profile saved and personalized learning path generated successfully.",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete onboarding: {str(e)}",
        )


@router.get("/api/interests", summary="Get all available interest domains")
def get_master_interests(db: Session = Depends(get_db)):
    interests = db.query(Interest).order_by(Interest.name.asc()).all()
    return {
        "success": True,
        "data": [{"id": i.id, "name": i.name, "category": i.category} for i in interests],
    }


@router.get("/api/user-interests", summary="Get user selected interests")
def get_user_interests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(UserInterest).options(joinedload(UserInterest.interest)).filter(UserInterest.user_id == current_user.id).all()
    return {
        "success": True,
        "data": [
            {
                "id": r.id,
                "interest_id": r.interest_id,
                "name": r.interest.name if r.interest else r.custom_interest,
                "category": r.interest.category if r.interest else "Custom",
                "custom": r.interest_id is None,
            }
            for r in records
        ],
    }


@router.get("/api/user-preferences", summary="Get user learning preferences")
def get_user_preferences(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    prefs = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not prefs:
        return {
            "success": True,
            "data": {
                "learning_hours_per_week": 10,
                "learning_style": "Project-based",
                "difficulty_preference": "Intermediate",
                "learning_mode": "Self-paced",
                "resource_preference": "All",
            },
        }

    return {
        "success": True,
        "data": {
            "id": prefs.id,
            "learning_hours_per_week": prefs.learning_hours_per_week,
            "learning_style": prefs.learning_style,
            "difficulty_preference": prefs.difficulty_preference,
            "learning_mode": prefs.learning_mode,
            "resource_preference": prefs.resource_preference,
        },
    }
