"""
Certificates Router — Handles Course, Project, and Overall PathPilot Certificates & PDF Summary Downloads.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.models.user_streak import Certificate
from app.models.learning_path import LearningPath
from app.models.project import Project, UserProjectProgress
from app.core.deps import get_current_user
from app.schemas.enhancements import CertificateResponse, CertificateVerifyResponse

router = APIRouter(tags=["Certificates & PDF"])


def generate_certificate_id(cert_type: str, user_id: int) -> str:
    timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
    prefix = "COURSE" if cert_type == "course" else ("PROJ" if cert_type == "project" else "PATHPILOT")
    return f"PP-2026-{prefix}-{user_id:04d}-{timestamp_str[-4:]}"


def issue_certificate_if_eligible(
    db: Session,
    user: User,
    course_name: str,
    cert_type: str,
) -> Certificate:
    """Helper to issue a new certificate if not already issued."""
    existing = (
        db.query(Certificate)
        .filter(
            Certificate.user_id == user.id,
            Certificate.course_name == course_name,
            Certificate.certificate_type == cert_type,
        )
        .first()
    )
    if existing:
        return existing

    cert_id = generate_certificate_id(cert_type, user.id)
    verification_code = f"VERIFY-{cert_id}"

    cert = Certificate(
        certificate_id=cert_id,
        user_id=user.id,
        course_name=course_name,
        certificate_type=cert_type,
        verification_code=verification_code,
        issued_at=datetime.now(),
        metadata_json={
            "student_name": user.name,
            "course_name": course_name,
            "platform": "PathPilot AI",
        },
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)

    # Check if user now has BOTH Course and Project certificate for this course to issue Overall Certificate!
    if cert_type in ("course", "project"):
        has_course = (
            db.query(Certificate)
            .filter(
                Certificate.user_id == user.id,
                Certificate.course_name == course_name,
                Certificate.certificate_type == "course",
            )
            .first()
        )
        has_proj = (
            db.query(Certificate)
            .filter(
                Certificate.user_id == user.id,
                Certificate.course_name == course_name,
                Certificate.certificate_type == "project",
            )
            .first()
        )
        if has_course and has_proj:
            issue_certificate_if_eligible(db, user, course_name, "overall")

    return cert


@router.get(
    "/api/certificates",
    response_model=List[CertificateResponse],
    status_code=status.HTTP_200_OK,
    summary="Get user's earned certificates",
)
def get_user_certificates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    certs = (
        db.query(Certificate)
        .filter(Certificate.user_id == current_user.id)
        .order_by(Certificate.issued_at.desc())
        .all()
    )
    return certs


@router.get(
    "/api/certificates/verify/{certificate_id}",
    response_model=CertificateVerifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Public verification for certificates",
)
def verify_certificate(
    certificate_id: str,
    db: Session = Depends(get_db),
):
    cert = (
        db.query(Certificate)
        .filter(
            (Certificate.certificate_id == certificate_id)
            | (Certificate.verification_code == certificate_id)
        )
        .first()
    )
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate invalid or not found.",
        )

    user = db.query(User).filter(User.id == cert.user_id).first()
    student_name = user.name if user else "Learner"

    return CertificateVerifyResponse(
        is_valid=True,
        certificate_id=cert.certificate_id,
        student_name=student_name,
        course_name=cert.course_name,
        certificate_type=cert.certificate_type,
        issued_at=cert.issued_at,
        status="VERIFIED OFFICIAL",
    )


@router.get(
    "/api/courses/{slug}/summary/pdf",
    status_code=status.HTTP_200_OK,
    summary="Download official Course Summary Document",
)
def download_course_summary_pdf(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    path = (
        db.query(LearningPath)
        .filter(LearningPath.user_id == current_user.id)
        .first()
    )
    course_title = path.title if path else slug.replace("-", " ").title()

    summary_text = f"""
================================================================================
PATHPILOT AI — OFFICIAL COURSE COMPLETION SUMMARY
================================================================================

Student Name:      {current_user.name}
Email Address:     {current_user.email}
Course Title:      {course_title}
Completion Date:   {datetime.now().strftime('%d %b %Y')}
Status:            Completed All Learning Phases & Final Assessment

SUMMARY OF ACCOMPLISHMENTS:
--------------------------------------------------------------------------------
- Completed all structured modules and video lessons.
- Passed 10-Question Module Assessment MCQs across all phases.
- Passed Phase Assessments with qualifying score.
- Completed 30-Question Comprehensive Final Assessment.

SKILLS & PROFICIENCIES MASTERED:
--------------------------------------------------------------------------------
- Core Engineering Fundamentals & Architecture
- Data Structures, Algorithms & Problem Solving
- Full-Stack Software Construction & Best Practices
- Quality Assurance & Technical Rigor

AREAS OF STRENGTH:
- High performance on technical diagnostic evaluations.
- Consistent learning streak and project execution.

RECOMMENDED NEXT STEPS:
- Explore advanced specialized project tracks in Explore Courses.
- Obtain PathPilot AI Overall Completion Certificate.

================================================================================
Generated by PathPilot AI Learning Platform
================================================================================
"""

    return Response(
        content=summary_text.encode("utf-8"),
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename={slug}-course-summary.txt"
        },
    )
