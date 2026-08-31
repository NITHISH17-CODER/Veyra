"""
Project Recommendation Engine — Recommends projects that strengthen missing skills.

Scoring breakdown:
    50 %  skill-gap coverage
    20 %  difficulty compatibility
    15 %  career relevance
    15 %  estimated time compatibility
"""

from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.models.learner_profile import LearnerProfile
from app.models.project import Project
from app.models.project_skill import ProjectSkill
from app.models.career_skill import CareerSkill
from app.ai.skill_gap import calculate_skill_gap


# ── Difficulty mapping ────────────────────────────────────────────────────

_DIFFICULTY_ORDER: dict[str, int] = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3,
}

_EXPERIENCE_TO_DIFFICULTY: dict[str, str] = {
    "beginner": "beginner",
    "basic": "beginner",
    "intermediate": "intermediate",
    "advanced": "advanced",
    "expert": "advanced",
}


def _difficulty_compatibility(
    project_difficulty: str | None,
    user_experience: str | None,
    max_gap: int,
) -> float:
    """Score 0-1 based on how well project difficulty matches the user."""
    if not project_difficulty:
        return 0.5

    p_level = _DIFFICULTY_ORDER.get(project_difficulty.strip().lower(), 2)

    if user_experience:
        target = _EXPERIENCE_TO_DIFFICULTY.get(
            user_experience.strip().lower(), "intermediate"
        )
        t_level = _DIFFICULTY_ORDER.get(target, 2)
    else:
        t_level = 2 if max_gap < 3 else 1

    distance = abs(p_level - t_level)
    return max(1.0 - distance * 0.35, 0.0)


def _career_relevance(
    project_skill_ids: set[int],
    career_skill_ids: set[int],
) -> float:
    """How many of the project's skills are relevant to the target career."""
    if not project_skill_ids or not career_skill_ids:
        return 0.0
    overlap = project_skill_ids & career_skill_ids
    return len(overlap) / len(project_skill_ids) if project_skill_ids else 0.0


def _time_compatibility(
    estimated_hours: float | None,
    weekly_hours: int | None,
) -> float:
    """Prefer projects that fit a reasonable time window."""
    if not estimated_hours or not weekly_hours or weekly_hours <= 0:
        return 0.5

    weeks = estimated_hours / weekly_hours
    if weeks <= 1:
        return 1.0
    elif weeks <= 2:
        return 0.85
    elif weeks <= 4:
        return 0.6
    elif weeks <= 6:
        return 0.4
    return 0.2


def recommend_projects(
    db: Session,
    user_id: int,
    career_id: int,
    top_n: int = 5,
) -> list[dict]:
    """
    Recommend projects that strengthen missing skills for a career.
    Returns top N projects with scores and reason data.
    """

    # ── 1. Get skill gap data ─────────────────────────────────────────
    gap_data = calculate_skill_gap(db, user_id, career_id)
    if "error" in gap_data:
        return []

    gap_skills: dict[int, dict] = {}
    for s in gap_data["skills"]:
        if s["gap"] > 0:
            gap_skills[s["skill_id"]] = s

    if not gap_skills:
        return []

from app.models.career import Career
from app.models.project import UserProjectProgress


def recommend_projects(
    db: Session,
    user_id: int,
    career_id: int,
    top_n: int = 18,
) -> list[dict]:
    """
    Select and recommend projects exclusively from the 90 fixed projects catalog.
    Enforces progressive unlock logic (Basic -> Intermediate -> Advanced -> Expert)
    based on career selection, skills, assessment results, and completed projects.
    """
    # Target career lookup
    career_obj = db.query(Career).filter(Career.id == career_id).first()
    target_career_name = career_obj.name if career_obj else None

    # Fetch user profile & user progress
    profile = (
        db.query(LearnerProfile)
        .filter(LearnerProfile.user_id == user_id)
        .first()
    )
    user_experience = (profile.experience_level if profile else "beginner").lower()
    weekly_hours = profile.learning_hours_per_week if profile else 10

    # User completed projects
    user_progress_rows = (
        db.query(UserProjectProgress)
        .filter(UserProjectProgress.user_id == user_id)
        .all()
    )
    completed_project_ids = {
        up.project_id for up in user_progress_rows if up.status == "completed"
    }

    # Skill gap data
    gap_data = calculate_skill_gap(db, user_id, career_id)
    gap_skills: dict[int, dict] = {}
    if "skills" in gap_data:
        for s in gap_data["skills"]:
            if s.get("gap", 0) > 0:
                gap_skills[s["skill_id"]] = s

    max_gap = max((s["gap"] for s in gap_skills.values()), default=0)

    career_skills_rows = (
        db.query(CareerSkill)
        .filter(CareerSkill.career_id == career_id)
        .all()
    )
    career_skill_ids = {cs.skill_id for cs in career_skills_rows}

    # Query projects matching target career (or all 90 projects)
    query = db.query(Project).options(
        joinedload(Project.project_skills).joinedload(ProjectSkill.skill)
    )
    if target_career_name:
        # Match exact career or fallback to all
        career_projects = query.filter(Project.career_name == target_career_name).all()
        projects = career_projects if len(career_projects) >= 18 else query.all()
    else:
        projects = query.all()

    # Track completed counts per level for progressive unlock
    completed_basic_count = sum(
        1 for p in projects if p.id in completed_project_ids and (p.level or "").upper() == "BASIC"
    )
    completed_intermediate_count = sum(
        1 for p in projects if p.id in completed_project_ids and (p.level or "").upper() == "INTERMEDIATE"
    )
    completed_advanced_count = sum(
        1 for p in projects if p.id in completed_project_ids and (p.level or "").upper() == "ADVANCED"
    )

    results = []

    for project in projects:
        level_upper = (project.level or "BASIC").upper()
        
        # Determine Lock/Unlock status
        is_completed = project.id in completed_project_ids
        is_unlocked = False
        lock_reason = ""

        if level_upper == "BASIC":
            is_unlocked = True
        elif level_upper == "INTERMEDIATE":
            if user_experience in ["intermediate", "advanced", "expert"] or completed_basic_count >= 1:
                is_unlocked = True
            else:
                lock_reason = "Complete at least 1 Basic project or achieve Intermediate skill level to unlock."
        elif level_upper == "ADVANCED":
            if user_experience in ["advanced", "expert"] or completed_intermediate_count >= 1:
                is_unlocked = True
            else:
                lock_reason = "Complete at least 1 Intermediate project or achieve Advanced skill level to unlock."
        elif level_upper == "EXPERT":
            if user_experience == "expert" or completed_advanced_count >= 1:
                is_unlocked = True
            else:
                lock_reason = "Complete at least 1 Advanced project or achieve Expert skill level to unlock."

        status_str = "completed" if is_completed else ("available" if is_unlocked else "locked")

        ps_list = project.project_skills or []
        project_skill_ids = {ps.skill_id for ps in ps_list}
        skill_names = [ps.skill.name for ps in ps_list if ps.skill]

        # Scoring
        matched_gap_ids = project_skill_ids & set(gap_skills.keys())
        gap_imp_covered = sum(
            gap_skills[sid]["importance"] * gap_skills[sid]["gap"]
            for sid in matched_gap_ids
        )
        total_gap_imp = sum(s["importance"] * s["gap"] for s in gap_skills.values())
        coverage_score = gap_imp_covered / total_gap_imp if total_gap_imp > 0 else 0.5
        diff_score = _difficulty_compatibility(project.difficulty, user_experience, max_gap)
        career_score = _career_relevance(project_skill_ids, career_skill_ids)
        time_score = _time_compatibility(project.estimated_hours, weekly_hours)

        total = coverage_score * 50 + diff_score * 20 + career_score * 15 + time_score * 15
        recommendation_score = round(total)

        why_text = f"Strengthens core competency for {project.career_name or 'career'}."
        if matched_gap_ids:
            primary_skill = ps_list[0].skill.name if ps_list and ps_list[0].skill else "skill gap"
            why_text = f"Targeted at closing your skill gap in {primary_skill}."

        results.append({
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "category": project.career_name or "Portfolio Project",
            "difficulty": project.difficulty or "Basic",
            "level": project.level or "BASIC",
            "career_name": project.career_name,
            "estimated_hours": project.estimated_hours,
            "estimatedHours": project.estimated_hours,
            "status": status_str,
            "is_unlocked": is_unlocked,
            "lock_reason": lock_reason,
            "skills": skill_names,
            "matched_skills": skill_names,
            "recommendation_score": recommendation_score,
            "whyRecommended": why_text,
            "problemStatement": project.description,
            "objectives": project.objectives_json or [
                f"Develop {project.title} core components",
                "Implement database & API business logic",
                "Deploy and verify submission requirements",
            ],
            "suggestedTechnologies": project.technologies_json or skill_names,
            "requirements": project.requirements_json or [],
            "reason_data": {
                "gap_coverage_pct": round(coverage_score * 100),
                "difficulty_fit_pct": round(diff_score * 100),
                "career_relevance_pct": round(career_score * 100),
                "time_fit_pct": round(time_score * 100),
            },
        })

    # Sort results: Unlocked & Available first, then higher recommendation score
    results.sort(key=lambda r: (1 if r["status"] == "completed" else (2 if r["is_unlocked"] else 3), -r["recommendation_score"]))
    return results[:top_n]

