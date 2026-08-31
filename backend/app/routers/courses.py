"""
Courses Router — Catalog browsing and course detail endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.database.session import get_db
from app.models.course import Course
from app.models.course_skill import CourseSkill

router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get catalog courses",
    description="Browse all available courses from the database catalog with optional filtering.",
)
def get_courses(
    skill: Optional[str] = Query(None, description="Filter by skill name"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    search: Optional[str] = Query(None, description="Search course title"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Course).options(
        joinedload(Course.course_skills).joinedload(CourseSkill.skill)
    )

    if difficulty and difficulty.lower() != "all":
        query = query.filter(Course.difficulty.ilike(f"%{difficulty.strip()}%"))

    if search:
        query = query.filter(Course.title.ilike(f"%{search.strip()}%"))

    courses = query.order_by(Course.id.asc()).offset(skip).limit(limit).all()

    results = []
    for c in courses:
        skill_names = [cs.skill.name for cs in (c.course_skills or []) if cs.skill]
        if skill and skill.lower() not in [s.lower() for s in skill_names]:
            continue

        results.append({
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "provider": c.provider,
            "url": c.url,
            "is_free": c.is_free,
            "price": float(c.price) if c.price is not None else 0.0,
            "currency": c.currency,
            "difficulty": c.difficulty,
            "duration_hours": c.duration_hours,
            "rating": c.rating,
            "skills": skill_names,
        })

    return results


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Get course detail by ID",
)
def get_course_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    course = (
        db.query(Course)
        .options(joinedload(Course.course_skills).joinedload(CourseSkill.skill))
        .filter(Course.id == id)
        .first()
    )
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {id} not found.",
        )

    skill_names = [cs.skill.name for cs in (course.course_skills or []) if cs.skill]

    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "provider": course.provider,
        "url": course.url,
        "is_free": course.is_free,
        "price": float(course.price) if course.price is not None else 0.0,
        "currency": course.currency,
        "difficulty": course.difficulty,
        "duration_hours": course.duration_hours,
        "rating": course.rating,
        "skills": skill_names,
    }
