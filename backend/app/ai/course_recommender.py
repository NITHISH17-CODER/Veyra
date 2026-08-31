"""
Course Recommendation Engine — Recommends courses that close skill gaps.

Scoring breakdown:
    40 %  skill-gap coverage
    20 %  difficulty compatibility
    15 %  prerequisite compatibility
    15 %  learning preference compatibility
    10 %  time/duration compatibility
"""

from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.models.learner_profile import LearnerProfile
from app.models.course import Course
from app.models.course_skill import CourseSkill
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
    course_difficulty: str | None,
    user_experience: str | None,
    max_gap_level: int,
) -> float:
    """
    Score 0-1 based on how well the course difficulty matches the user.

    If the user has major gaps, beginner courses are fine.
    If the user is advanced, beginner courses score lower.
    """
    if not course_difficulty:
        return 0.5  # Unknown difficulty = neutral

    c_level = _DIFFICULTY_ORDER.get(course_difficulty.strip().lower(), 2)

    # Determine appropriate difficulty from experience or max gap
    if user_experience:
        target_diff = _EXPERIENCE_TO_DIFFICULTY.get(
            user_experience.strip().lower(), "intermediate"
        )
        t_level = _DIFFICULTY_ORDER.get(target_diff, 2)
    else:
        # If gaps are big, lower difficulty is fine
        if max_gap_level >= 3:
            t_level = 1
        elif max_gap_level >= 2:
            t_level = 2
        else:
            t_level = 2

    distance = abs(c_level - t_level)
    return max(1.0 - distance * 0.35, 0.0)


def _prerequisite_compatibility(
    course_skill_levels: dict[int, int],
    user_skill_map: dict[int, int],
) -> float:
    """
    Check if the user has enough baseline to handle the course.

    If a course teaches at level 4, the user should ideally be at 2-3.
    If a course teaches at level 1, anyone can take it.
    """
    if not course_skill_levels:
        return 0.5

    compatible_count = 0
    for skill_id, coverage_level in course_skill_levels.items():
        user_level = user_skill_map.get(skill_id, 0)
        # User should be at most 2 levels below the course coverage
        if coverage_level <= 2:
            compatible_count += 1  # Beginner courses are always OK
        elif user_level >= coverage_level - 2:
            compatible_count += 1
        # User already at or above coverage? Course is too easy for this skill
        elif user_level >= coverage_level:
            compatible_count += 0.5

    return compatible_count / len(course_skill_levels) if course_skill_levels else 0.5


def _preference_compatibility(
    course: Course,
    learning_preference: str | None,
) -> float:
    """
    Simple keyword match between the user's learning preference
    and the course metadata (provider, title, description).
    """
    if not learning_preference:
        return 0.5

    pref_lower = learning_preference.lower()
    corpus = " ".join(filter(None, [
        course.title,
        course.description,
        course.provider,
    ])).lower()

    pref_keywords = set(pref_lower.replace(",", " ").split())
    if not pref_keywords:
        return 0.5

    matches = sum(1 for kw in pref_keywords if kw in corpus)
    return min(matches / max(len(pref_keywords), 1), 1.0)


def _duration_compatibility(
    course_hours: float | None,
    weekly_hours: int | None,
) -> float:
    """
    Prefer courses that fit within a reasonable time frame
    given the user's weekly study budget.
    """
    if not course_hours or not weekly_hours or weekly_hours <= 0:
        return 0.5

    # A course taking fewer than 4 weeks at user's pace is ideal
    weeks_needed = course_hours / weekly_hours
    if weeks_needed <= 2:
        return 1.0
    elif weeks_needed <= 4:
        return 0.85
    elif weeks_needed <= 8:
        return 0.6
    elif weeks_needed <= 12:
        return 0.4
    return 0.2


def recommend_courses(
    db: Session,
    user_id: int,
    career_id: int,
    top_n: int = 10,
) -> list[dict]:
    """
    Recommend courses that close the user's skill gaps for a career.

    Returns top N courses with scores and reason data.
    """

    # ── 1. Get skill gap data ─────────────────────────────────────────
    gap_data = calculate_skill_gap(db, user_id, career_id)
    if "error" in gap_data:
        return []

    # Build a dict of {skill_id: gap} for skills that have a gap
    gap_skills: dict[int, dict] = {}
    user_skill_map: dict[int, int] = {}
    for s in gap_data["skills"]:
        user_skill_map[s["skill_id"]] = s["current_level"]
        if s["gap"] > 0:
            gap_skills[s["skill_id"]] = s

    if not gap_skills:
        return []  # No gaps — no courses needed

    # ── 2. Fetch user profile ─────────────────────────────────────────
    profile = (
        db.query(LearnerProfile)
        .filter(LearnerProfile.user_id == user_id)
        .first()
    )
    experience_level = profile.experience_level if profile else None
    learning_preference = profile.learning_preference if profile else None
    weekly_hours = profile.learning_hours_per_week if profile else None

    max_gap = max(s["gap"] for s in gap_skills.values()) if gap_skills else 0

    # ── 3. Load all courses with their skills ─────────────────────────
    courses = (
        db.query(Course)
        .options(joinedload(Course.course_skills).joinedload(CourseSkill.skill))
        .all()
    )

    # ── 4. Score each course ──────────────────────────────────────────
    results = []

    for course in courses:
        cs_list = course.course_skills or []
        course_skill_ids = {cs.skill_id for cs in cs_list}
        course_skill_levels = {cs.skill_id: cs.coverage_level for cs in cs_list}

        # Which gap skills does this course cover?
        matched_gap_ids = course_skill_ids & set(gap_skills.keys())
        if not matched_gap_ids:
            continue  # Course doesn't address any gaps

        # Skill-gap coverage: weighted by importance of the gap skills covered
        gap_importance_covered = sum(
            gap_skills[sid]["importance"] * gap_skills[sid]["gap"]
            for sid in matched_gap_ids
        )
        total_gap_importance = sum(
            s["importance"] * s["gap"] for s in gap_skills.values()
        )
        coverage_score = (
            gap_importance_covered / total_gap_importance
            if total_gap_importance > 0 else 0.0
        )

        # Difficulty compatibility
        diff_score = _difficulty_compatibility(
            course.difficulty, experience_level, max_gap
        )

        # Prerequisite compatibility
        prereq_score = _prerequisite_compatibility(
            course_skill_levels, user_skill_map
        )

        # Learning preference compatibility
        pref_score = _preference_compatibility(course, learning_preference)

        # Duration compatibility
        dur_score = _duration_compatibility(
            course.duration_hours, weekly_hours
        )

        # Weighted total (0-100)
        total = (
            coverage_score * 40
            + diff_score * 20
            + prereq_score * 15
            + pref_score * 15
            + dur_score * 10
        )
        recommendation_score = round(total)

        # Build matched skill names
        matched_skill_names = []
        for cs in cs_list:
            if cs.skill_id in matched_gap_ids:
                matched_skill_names.append(
                    cs.skill.name if cs.skill else f"Skill #{cs.skill_id}"
                )

        results.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "provider": course.provider,
            "url": course.url,
            "is_free": course.is_free,
            "price": float(course.price) if course.price is not None else None,
            "currency": course.currency,
            "difficulty": course.difficulty,
            "duration_hours": course.duration_hours,
            "rating": course.rating,
            "matched_skills": matched_skill_names,
            "recommendation_score": recommendation_score,
            "reason_data": {
                "gap_coverage_pct": round(coverage_score * 100),
                "difficulty_fit_pct": round(diff_score * 100),
                "prereq_fit_pct": round(prereq_score * 100),
                "preference_fit_pct": round(pref_score * 100),
                "duration_fit_pct": round(dur_score * 100),
                "addresses_gaps": [
                    gap_skills[sid]["skill"] for sid in matched_gap_ids
                ],
            },
        })

    # ── 5. Sort and return top N ──────────────────────────────────────
    results.sort(key=lambda r: r["recommendation_score"], reverse=True)
    return results[:top_n]
