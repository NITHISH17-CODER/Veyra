"""
Course Learning Router — complete interactive endpoints for courses, roadmaps, lessons,
assessments, final exams, and summary export.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.services import course_learning_service as service

router = APIRouter(tags=["Course Learning"])


# ── Pydantic Request Models ───────────────────────────────────────────────────

class AssessmentSubmitRequest(BaseModel):
    answers: Dict[str, int] = Field(..., description="Map of question_id -> chosen option index (0-3)")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/api/courses", summary="Get all 5 core career learning courses")
def get_courses_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns the 5 structured career learning paths with user progress."""
    return service.get_all_courses(db, user_id=current_user.id)


@router.get("/api/courses/{slug_or_id}", summary="Get course overview by slug or ID")
def get_course_detail(
    slug_or_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    course = service.get_course_by_slug(db, slug_or_id, user_id=current_user.id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    return course


@router.get("/api/courses/{slug_or_id}/roadmap", summary="Get complete phased course roadmap")
def get_course_roadmap_endpoint(
    slug_or_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    roadmap = service.get_course_roadmap(db, slug_or_id, user_id=current_user.id)
    if not roadmap:
        raise HTTPException(status_code=404, detail="Course roadmap not found.")
    return roadmap


@router.get("/api/courses/{slug_or_id}/modules/{module_id}", summary="Get module details and lessons")
def get_module_detail_endpoint(
    slug_or_id: str,
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mod = service.get_module_detail(db, slug_or_id, module_id, user_id=current_user.id)
    if not mod:
        raise HTTPException(status_code=404, detail="Module not found.")
    return mod


@router.get("/api/courses/{slug_or_id}/modules/{module_id}/lessons/{lesson_id}", summary="Get lesson content")
def get_lesson_detail_endpoint(
    slug_or_id: str,
    module_id: int,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    lesson = service.get_lesson_detail(db, slug_or_id, module_id, lesson_id, user_id=current_user.id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found.")
    if "error" in lesson:
        raise HTTPException(status_code=403, detail=lesson["message"])
    return lesson


@router.post("/api/lessons/{lesson_id}/complete", summary="Mark lesson completed")
def mark_lesson_complete_endpoint(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = service.mark_lesson_completed(db, lesson_id, user_id=current_user.id)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("message", "Error completing lesson."))
    
    # Record daily learning activity for streak
    from app.services.streak_service import record_learning_activity
    streak_info = record_learning_activity(db, current_user.id, "lesson_completed", lesson_id)
    result["streak"] = streak_info
    return result


@router.get("/api/modules/{module_id}/assessment", summary="Get module assessment questions")
def get_module_assessment_endpoint(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = service.get_module_assessment_questions(db, module_id, user_id=current_user.id)
    if not data:
        raise HTTPException(status_code=404, detail="Assessment not found for this module.")
    if "error" in data:
        raise HTTPException(status_code=403, detail=data["message"])
    return data


@router.post("/api/assessments/{assessment_id}/submit", summary="Submit module assessment")
def submit_module_assessment_endpoint(
    assessment_id: int,
    payload: AssessmentSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = service.submit_module_assessment(db, assessment_id, payload.answers, user_id=current_user.id)
    if not result.get("success"):
        if result.get("error") == "LOCKED_MODULE":
            raise HTTPException(status_code=403, detail=result.get("message", "Module is locked."))
        raise HTTPException(status_code=400, detail=result.get("message", "Error submitting assessment."))
    
    if result.get("passed"):
        from app.services.streak_service import record_learning_activity
        streak_info = record_learning_activity(db, current_user.id, "assessment_completed", assessment_id)
        result["streak"] = streak_info
    return result


@router.get("/api/courses/{slug_or_id}/continue-action", summary="Get next incomplete lesson to continue")
def get_continue_action_endpoint(
    slug_or_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = service.get_continue_learning_target(db, slug_or_id, user_id=current_user.id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/api/courses/{slug_or_id}/completion-summary", summary="Get course completion summary")
def get_completion_summary_endpoint(
    slug_or_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    summary = service.get_course_completion_summary(db, slug_or_id, user_id=current_user.id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not available.")
    return summary


@router.get("/api/courses/{slug_or_id}/completion-summary/download", summary="Download course summary .txt file")
def download_completion_summary_endpoint(
    slug_or_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    content = service.generate_text_summary_file(db, slug_or_id, user_id=current_user.id)
    filename = f"{slug_or_id}-course-summary.txt"
    return Response(
        content=content,
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/api/courses/{slug_or_id}/final-assessment", summary="Get course final assessment")
def get_final_assessment_endpoint(
    slug_or_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    exam = service.get_final_assessment_questions(db, slug_or_id, user_id=current_user.id)
    if not exam:
        raise HTTPException(status_code=404, detail="Final assessment not found.")
    return exam


@router.post("/api/courses/{slug_or_id}/final-assessment/submit", summary="Submit course final assessment")
def submit_final_assessment_endpoint(
    slug_or_id: str,
    payload: AssessmentSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = service.submit_final_assessment(db, slug_or_id, payload.answers, user_id=current_user.id)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("message", "Error submitting final exam."))
    
    if result.get("passed"):
        from app.services.streak_service import record_learning_activity
        from app.routers.certificates import issue_certificate_if_eligible
        streak_info = record_learning_activity(db, current_user.id, "assessment_completed", slug_or_id)
        result["streak"] = streak_info
        
        course_name = slug_or_id.replace("-", " ").title()
        cert = issue_certificate_if_eligible(db, current_user, course_name, "course")
        result["certificate_id"] = cert.certificate_id

    return result


@router.get("/api/skills/{skill_identifier}", summary="Get skill details and courses teaching it")
def get_skill_detail_endpoint(
    skill_identifier: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    skill = service.get_skill_detail(db, skill_identifier, user_id=current_user.id)
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_identifier}' not found.")
    return skill
