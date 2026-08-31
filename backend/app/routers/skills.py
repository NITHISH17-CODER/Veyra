"""
Skills Router — Master skills catalogue endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillRead

router = APIRouter(prefix="/api/skills", tags=["Skills"])


@router.get(
    "",
    response_model=List[SkillRead],
    status_code=status.HTTP_200_OK,
    summary="List master catalog skills",
    description="Retrieves available skills from the master catalog with optional category filtering and search.",
)
def get_skills(
    category: Optional[str] = Query(None, description="Filter skills by domain/category"),
    search: Optional[str] = Query(None, description="Search skills by name (case-insensitive)"),
    skip: int = Query(0, ge=0, description="Pagination skip offset"),
    limit: int = Query(100, ge=1, le=500, description="Pagination limit"),
    db: Session = Depends(get_db),
):
    query = db.query(Skill)

    if category:
        query = query.filter(Skill.category.ilike(f"%{category.strip()}%"))

    if search:
        query = query.filter(Skill.name.ilike(f"%{search.strip()}%"))

    skills = query.order_by(Skill.name.asc()).offset(skip).limit(limit).all()
    return skills
