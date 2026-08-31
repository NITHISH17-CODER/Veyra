"""
Projects Router — Catalog browsing, project details, submission validation, and AI analysis endpoints.
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from app.database.session import get_db
from app.models.project import Project, UserProjectProgress
from app.models.project_skill import ProjectSkill
from app.models.user import User
from app.core.deps import get_current_user
from app.ai.project_recommender import recommend_projects
from app.ai.project_analyzer import validate_submission_url, analyze_project_submission
from app.models.career_goal import CareerGoal
from app.models.learning_path import LearningPath

router = APIRouter(prefix="/api/projects", tags=["Projects"])


class SubmitProjectRequest(BaseModel):
    submission_url: str = Field(..., description="GitHub repository URL or Google Colab notebook URL")
    notes: Optional[str] = Field(None, description="Optional notes or notes for evaluator")


def _get_active_career_id(db: Session, user_id: int) -> Optional[int]:
    """Helper to determine target career_id for user."""
    path = (
        db.query(LearningPath)
        .filter(LearningPath.user_id == user_id, LearningPath.status.in_(["active", "in_progress"]))
        .order_by(LearningPath.created_at.desc())
        .first()
    )
    if path and path.target_career_id:
        return path.target_career_id

    goal = (
        db.query(CareerGoal)
        .filter(CareerGoal.user_id == user_id, CareerGoal.identified_career_id.isnot(None))
        .order_by(CareerGoal.created_at.desc())
        .first()
    )
    if goal and goal.identified_career_id:
        return goal.identified_career_id

    return 1  # Default to 1 (Frontend Developer) if none set


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get catalog projects",
    description="Browse available portfolio projects (Basic, Intermediate, Advanced) for personalized career tracks.",
)
def get_projects(
    category: Optional[str] = Query(None, description="Filter by difficulty/level (Basic, Intermediate, Advanced)"),
    search: Optional[str] = Query(None, description="Search project title"),
    career: Optional[str] = Query(None, description="Filter by exact career_name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Project).options(
        joinedload(Project.project_skills).joinedload(ProjectSkill.skill)
    )

    # Strictly exclude Expert level projects
    query = query.filter(
        Project.difficulty != "Expert",
        Project.level != "EXPERT"
    )

    # Determine user's active career if career parameter is not explicitly passed
    target_career_name = career
    if not target_career_name or target_career_name.lower() == "all":
        active_career_id = _get_active_career_id(db, current_user.id)
        from app.models.career import Career
        career_obj = db.query(Career).filter(Career.id == active_career_id).first()
        if career_obj:
            target_career_name = career_obj.name

    if target_career_name and target_career_name.lower() != "all":
        # Match course titles (e.g. SDE, Frontend, Backend, Cybersecurity, AI)
        if "frontend" in target_career_name.lower():
            query = query.filter(Project.career_name.ilike("%Frontend%"))
        elif "backend" in target_career_name.lower():
            query = query.filter(Project.career_name.ilike("%Backend%"))
        elif "cyber" in target_career_name.lower():
            query = query.filter(Project.career_name.ilike("%Cybersecurity%"))
        elif "ai" in target_career_name.lower():
            query = query.filter(Project.career_name.ilike("%AI%"))
        else:
            query = query.filter(Project.career_name.ilike("%Software%"))

    if category and category.lower() != "all":
        query = query.filter(
            (Project.difficulty.ilike(f"%{category.strip()}%")) |
            (Project.level.ilike(f"%{category.strip()}%"))
        )

    if search:
        query = query.filter(Project.title.ilike(f"%{search.strip()}%"))

    projects = query.order_by(Project.id.asc()).offset(skip).limit(limit).all()

    # Get user progress map for completion status
    user_progress_records = (
        db.query(UserProjectProgress)
        .filter(UserProjectProgress.user_id == current_user.id)
        .all()
    )
    progress_map = {up.project_id: up for up in user_progress_records}

    results = []
    for p in projects:
        skill_names = [ps.skill.name for ps in (p.project_skills or []) if ps.skill]
        up = progress_map.get(p.id)

        results.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "category": p.career_name or "Portfolio Project",
            "difficulty": p.difficulty or "Basic",
            "level": (p.difficulty or p.level or "BASIC").upper(),
            "career_name": p.career_name,
            "estimated_hours": p.estimated_hours,
            "estimatedHours": p.estimated_hours,
            "github_url": p.github_url,
            "dataset_url": p.dataset_url,
            "skills": skill_names,
            "matched_skills": skill_names,
            "status": up.status if up else "not_started",
            "verification_state": getattr(up, "verification_state", "VERIFIED") if (up and up.status == "completed") else ("NOT_SUBMITTED" if not up else "SUBMITTED"),
            "submission_url": up.submission_url if up else None,
            "score": up.score if up else None,
            "whyRecommended": f"Strengthens core skills for {p.career_name or 'career'}.",
            "problemStatement": p.description or f"Real-world application for {p.title}.",
            "objectives": p.objectives_json or [
                f"Structure and implement {p.title}",
                "Develop core business logic and API routing",
                "Verify test constraints and submit repository",
            ],
            "suggestedTechnologies": p.technologies_json or (skill_names if skill_names else ["Python", "JavaScript"]),
            "requirements": p.requirements_json or [],
        })

    return results


@router.get(
    "/recommended",
    status_code=status.HTTP_200_OK,
    summary="Get recommended unlocked projects",
)
def get_recommended_projects_endpoint(
    career_id: Optional[int] = Query(None, description="Optional target career ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target_career_id = career_id or _get_active_career_id(db, current_user.id)
    rec_projects = recommend_projects(db, user_id=current_user.id, career_id=target_career_id, top_n=18)
    return {
        "success": True,
        "data": rec_projects,
        "message": f"Retrieved {len(rec_projects)} catalog recommendations."
    }


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Get project detail by ID",
)
def get_project_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .options(joinedload(Project.project_skills).joinedload(ProjectSkill.skill))
        .filter(Project.id == id)
        .first()
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {id} not found.",
        )

    skill_names = [ps.skill.name for ps in (project.project_skills or []) if ps.skill]

    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "category": project.career_name or "Portfolio Project",
        "difficulty": project.difficulty or "Basic",
        "level": project.level or "BASIC",
        "career_name": project.career_name,
        "estimated_hours": project.estimated_hours,
        "estimatedHours": project.estimated_hours,
        "github_url": project.github_url,
        "dataset_url": project.dataset_url,
        "skills": skill_names,
        "matched_skills": skill_names,
        "whyRecommended": f"Builds practical competency in {', '.join(skill_names[:3]) if skill_names else 'engineering'}.",
        "problemStatement": project.description or f"Real-world application for {project.title}.",
        "objectives": project.objectives_json or [
            f"Develop core system architecture for {project.title}",
            "Implement business workflows and validations",
            "Test and submit project code repository",
        ],
        "suggestedTechnologies": project.technologies_json or (skill_names if skill_names else ["Python", "JavaScript"]),
        "requirements": project.requirements_json or [],
        "milestones": [
            {"step": "Architecture Setup & Initial Codebase", "status": "In Progress"},
            {"step": "Core Features Implementation & Logic", "status": "Pending"},
            {"step": "Testing & Output Validation", "status": "Pending"},
            {"step": "GitHub / Colab Submission & Code Review", "status": "Pending"}
        ]
    }


@router.get(
    "/{id}/progress",
    status_code=status.HTTP_200_OK,
    summary="Get user's progress and submission status for a single project",
)
def get_project_progress(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns the authenticated user's submission and evaluation data for a single project."""
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    prog = (
        db.query(UserProjectProgress)
        .filter(
            UserProjectProgress.user_id == current_user.id,
            UserProjectProgress.project_id == id,
        )
        .first()
    )

    if not prog:
        return {
            "success": True,
            "data": None,
            "message": "No submission found for this project."
        }

    return {
        "success": True,
        "data": {
            "project_id": prog.project_id,
            "submission_url": prog.submission_url,
            "status": prog.status,
            "verification_state": "VERIFIED" if prog.status == "completed" else ("REJECTED" if prog.score == 0 and prog.submission_url else "NOT_SUBMITTED"),
            "score": prog.score,
            "strengths": prog.strengths,
            "weaknesses": prog.weaknesses,
            "missing_requirements": prog.missing_requirements,
            "technical_feedback": prog.technical_feedback,
            "recommended_improvements": prog.recommended_improvements,
            "started_at": prog.started_at.isoformat() if prog.started_at else None,
            "completed_at": prog.completed_at.isoformat() if prog.completed_at else None,
        }
    }


@router.post(
    "/{id}/submit",
    status_code=status.HTTP_200_OK,
    summary="Submit project URL for AI analysis",
)
def submit_project(
    id: int,
    payload: SubmitProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {id} not found."
        )

    # 1. Strict Submission URL Validation
    is_valid, platform, error_msg = validate_submission_url(payload.submission_url)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg or "Invalid submission URL. Please submit a valid GitHub repository URL or Google Colab URL."
        )

    skill_names = [ps.skill.name for ps in (project.project_skills or []) if ps.skill]
    project_dict = {
        "id": project.id,
        "title": project.title,
        "level": project.level,
        "career_name": project.career_name,
        "objectives": project.objectives_json or [],
        "technologies": project.technologies_json or skill_names,
        "requirements": project.requirements_json or [],
        "skills": skill_names,
    }

    # 2. Run AI Analysis
    try:
        analysis_res = analyze_project_submission(
            db=db,
            project_dict=project_dict,
            submission_url=payload.submission_url,
            notes=payload.notes or ""
        )
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )

    # 3. Store Result in MySQL Table (user_project_progress)
    user_prog = (
        db.query(UserProjectProgress)
        .filter(
            UserProjectProgress.user_id == current_user.id,
            UserProjectProgress.project_id == project.id,
        )
        .first()
    )

    if not user_prog:
        user_prog = UserProjectProgress(
            user_id=current_user.id,
            project_id=project.id,
            started_at=datetime.utcnow()
        )
        db.add(user_prog)

    user_prog.submission_url = payload.submission_url.strip()
    user_prog.notes = payload.notes
    user_prog.score = analysis_res["score"]
    user_prog.status = analysis_res["status"]
    user_prog.progress_percentage = 100.0 if analysis_res["status"] == "completed" else 50.0
    user_prog.strengths = analysis_res["strengths"]
    user_prog.weaknesses = analysis_res["weaknesses"]
    user_prog.missing_requirements = analysis_res["missing_requirements"]
    user_prog.technical_feedback = analysis_res["technical_feedback"]
    user_prog.recommended_improvements = analysis_res["recommended_improvements"]
    if analysis_res["status"] == "completed":
        user_prog.completed_at = datetime.utcnow()

    db.commit()

    # Record learning activity for streak
    if analysis_res["status"] == "completed":
        from app.services.streak_service import record_learning_activity
        record_learning_activity(db, current_user.id, "project_completed", project.id)

        # Check if user completed all 20 projects for this career -> issue Project Certificate
        career_name = project.career_name
        if career_name:
            total_required_projects = (
                db.query(Project)
                .filter(Project.career_name == career_name, Project.difficulty != "Expert", Project.level != "EXPERT")
                .count()
            )
            completed_career_projects = (
                db.query(UserProjectProgress)
                .join(Project, Project.id == UserProjectProgress.project_id)
                .filter(
                    UserProjectProgress.user_id == current_user.id,
                    Project.career_name == career_name,
                    Project.difficulty != "Expert",
                    Project.level != "EXPERT",
                    UserProjectProgress.status == "completed",
                )
                .count()
            )
            if completed_career_projects >= total_required_projects and total_required_projects > 0:
                from app.routers.certificates import issue_certificate_if_eligible
                issue_certificate_if_eligible(db, current_user, career_name, "project")

    ver_state = analysis_res.get("verification_state", "VERIFIED" if user_prog.status == "completed" else "REJECTED")

    return {
        "success": True,
        "message": f"Project '{project.title}' submission evaluation complete ({ver_state}).",
        "data": {
            "project_id": project.id,
            "submission_url": user_prog.submission_url,
            "status": user_prog.status,
            "verification_state": ver_state,
            "score": user_prog.score,
            "strengths": user_prog.strengths,
            "weaknesses": user_prog.weaknesses,
            "missing_requirements": user_prog.missing_requirements,
            "technical_feedback": user_prog.technical_feedback,
            "recommended_improvements": user_prog.recommended_improvements,
        }
    }


@router.get(
    "/{id}/progress",
    status_code=status.HTTP_200_OK,
    summary="Get user submission progress and feedback",
)
def get_project_progress(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_prog = (
        db.query(UserProjectProgress)
        .filter(
            UserProjectProgress.user_id == current_user.id,
            UserProjectProgress.project_id == id,
        )
        .first()
    )

    if not user_prog:
        return {
            "success": True,
            "data": None,
            "message": "No submission record found for this project."
        }

    return {
        "success": True,
        "data": {
            "project_id": user_prog.project_id,
            "status": user_prog.status,
            "submission_url": user_prog.submission_url,
            "score": user_prog.score,
            "strengths": user_prog.strengths or [],
            "weaknesses": user_prog.weaknesses or [],
            "missing_requirements": user_prog.missing_requirements or [],
            "technical_feedback": user_prog.technical_feedback or "",
            "recommended_improvements": user_prog.recommended_improvements or [],
            "completed_at": user_prog.completed_at,
        }
    }
