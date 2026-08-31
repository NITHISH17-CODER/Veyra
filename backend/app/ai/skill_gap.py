"""
Skill Gap Engine — Compares user skills against career requirements.

Calculates:
- Per-skill gap (required_level - current_level)
- Gap status (ready, small_gap, medium_gap, major_gap)
- Weighted career readiness score (0-100)
"""

from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.models.user_skill import UserSkill
from app.models.career import Career
from app.models.career_skill import CareerSkill
from app.models.skill import Skill


def _gap_status(gap: int) -> str:
    """Classify a skill gap into a human-readable status."""
    if gap <= 0:
        return "ready"
    if gap == 1:
        return "small_gap"
    if gap == 2:
        return "medium_gap"
    return "major_gap"


def calculate_skill_gap(db: Session, user_id: int, career_id: int) -> dict:
    """
    Compare a user's current skills against the requirements of a specific career.

    Returns a dict with:
        career          – career name
        career_id       – career id
        readiness_score – weighted readiness percentage (0-100)
        total_skills    – number of required skills
        ready_count     – skills already at required level
        gap_count       – skills with gaps
        skills          – list of per-skill analysis dicts
        priority_skills – top skills to focus on (sorted by gap * importance)
    """

    # ── 1. Fetch career + required skills in one query ────────────────
    career = db.query(Career).filter(Career.id == career_id).first()
    if not career:
        return {"error": f"Career with ID {career_id} not found."}

    career_skills = (
        db.query(CareerSkill)
        .options(joinedload(CareerSkill.skill))
        .filter(CareerSkill.career_id == career_id)
        .all()
    )

    if not career_skills:
        return {
            "career": career.name,
            "career_id": career.id,
            "readiness_score": 100,
            "total_skills": 0,
            "ready_count": 0,
            "gap_count": 0,
            "skills": [],
            "priority_skills": [],
        }

    # ── 2. Fetch user skills as a lookup dict {skill_id: proficiency} ─
    user_skills = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == user_id)
        .all()
    )
    user_skill_map: dict[int, int] = {
        us.skill_id: us.proficiency for us in user_skills
    }

    # ── 3. Calculate per-skill gap ────────────────────────────────────
    skill_results = []
    weighted_score_sum = 0.0
    importance_sum = 0

    for cs in career_skills:
        skill_name = cs.skill.name if cs.skill else f"Skill #{cs.skill_id}"
        skill_category = cs.skill.category if cs.skill else None
        current_level = user_skill_map.get(cs.skill_id, 0)
        required_level = cs.required_level
        gap = required_level - current_level
        status = _gap_status(gap)

        # Weighted readiness: min(current / required, 1.0) × importance
        skill_score = min(current_level / required_level, 1.0) if required_level > 0 else 1.0
        weighted_score_sum += skill_score * cs.importance
        importance_sum += cs.importance

        skill_results.append({
            "skill_id": cs.skill_id,
            "skill": skill_name,
            "category": skill_category,
            "current_level": current_level,
            "required_level": required_level,
            "gap": max(gap, 0),
            "status": status,
            "importance": cs.importance,
        })

    # ── 4. Calculate overall readiness score ──────────────────────────
    readiness_score = round(
        (weighted_score_sum / importance_sum * 100) if importance_sum > 0 else 0
    )

    ready_count = sum(1 for s in skill_results if s["status"] == "ready")
    gap_count = len(skill_results) - ready_count

    # ── 5. Priority skills (sorted by gap × importance, descending) ──
    priority_skills = sorted(
        [s for s in skill_results if s["gap"] > 0],
        key=lambda s: s["gap"] * s["importance"],
        reverse=True,
    )

    return {
        "career": career.name,
        "career_id": career.id,
        "readiness_score": readiness_score,
        "total_skills": len(skill_results),
        "ready_count": ready_count,
        "gap_count": gap_count,
        "skills": skill_results,
        "priority_skills": priority_skills[:5],
    }
