"""
Roadmap Generator — Builds a sequenced learning path and identifies the next best action.

Responsibilities:
    1. Sequence skills by prerequisite/dependency order
    2. Map courses and projects onto the skill sequence
    3. Skip skills the user has already mastered
    4. Persist the learning path and items to MySQL
    5. Determine the single next best action
"""

from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from app.models.user import User
from app.models.learner_profile import LearnerProfile
from app.models.user_skill import UserSkill
from app.models.career import Career
from app.models.career_skill import CareerSkill
from app.models.course import Course
from app.models.course_skill import CourseSkill
from app.models.project import Project
from app.models.project_skill import ProjectSkill
from app.models.learning_path import LearningPath
from app.models.learning_path_item import LearningPathItem
from app.models.skill import Skill
from app.ai.skill_gap import calculate_skill_gap
from app.ai.course_recommender import recommend_courses
from app.ai.project_recommender import recommend_projects


# ── Skill dependency graph (approximate prerequisite order) ───────────────
# Higher-level skills generally depend on lower-level foundations.
# Categories are used to group: Programming → Data Science → AI/ML → Web Dev → etc.

_CATEGORY_ORDER: dict[str, int] = {
    "programming": 1,
    "data science": 2,
    "databases": 3,
    "web development": 4,
    "ai/ml": 5,
    "cloud": 6,
    "devops": 7,
    "cybersecurity": 8,
}

# Specific skill name-based prerequisites (skill_name -> list of prerequisite names)
_SKILL_PREREQUISITES: dict[str, list[str]] = {
    "pandas": ["python"],
    "numpy": ["python"],
    "scikit-learn": ["python", "statistics & probability"],
    "machine learning": ["python", "statistics & probability", "numpy"],
    "deep learning": ["python", "machine learning"],
    "pytorch": ["python", "deep learning"],
    "tensorflow & keras": ["python", "deep learning"],
    "natural language processing (nlp)": ["python", "machine learning"],
    "computer vision": ["python", "deep learning"],
    "large language models (llms)": ["python", "deep learning", "natural language processing (nlp)"],
    "rag systems": ["python", "large language models (llms)", "vector databases"],
    "mlops": ["python", "machine learning", "docker"],
    "fastapi": ["python"],
    "django": ["python"],
    "react": ["javascript", "html & css"],
    "next.js": ["javascript", "react"],
    "vue.js": ["javascript", "html & css"],
    "node.js": ["javascript"],
    "docker": ["bash & shell scripting"],
    "kubernetes": ["docker"],
    "ci/cd pipelines": ["git & github actions", "docker"],
    "data visualization": ["python", "pandas"],
    "exploratory data analysis (eda)": ["python", "pandas", "statistics & probability"],
    "feature engineering": ["python", "pandas", "machine learning"],
    "a/b testing": ["statistics & probability"],
}


def _topological_sort_skills(
    gap_skills: list[dict],
    all_skill_names: dict[int, str],
) -> list[dict]:
    """
    Sort skill gaps respecting prerequisite dependencies, then by
    category order, then by importance (descending).
    """

    # Build name -> skill dict for lookup
    name_to_skill: dict[str, dict] = {}
    for s in gap_skills:
        name_to_skill[s["skill"].lower()] = s

    # Simple topological approach: assign depth based on prerequisite chains
    def _depth(skill_name: str, visited: set | None = None) -> int:
        if visited is None:
            visited = set()
        if skill_name in visited:
            return 0  # Break cycles
        visited.add(skill_name)
        prereqs = _SKILL_PREREQUISITES.get(skill_name.lower(), [])
        if not prereqs:
            return 0
        return 1 + max(
            _depth(p, visited) for p in prereqs
        )

    # Decorate each skill with sort keys
    decorated = []
    for s in gap_skills:
        cat = (s.get("category") or "").lower()
        cat_order = _CATEGORY_ORDER.get(cat, 99)
        depth = _depth(s["skill"])
        decorated.append((depth, cat_order, -s["importance"], s))

    decorated.sort(key=lambda x: (x[0], x[1], x[2]))
    return [d[3] for d in decorated]


def _find_best_course_for_skill(
    skill_id: int,
    courses: list[Course],
    user_level: int,
) -> Course | None:
    """Find the single best course covering a specific skill."""
    best = None
    best_score = -1

    for course in courses:
        for cs in (course.course_skills or []):
            if cs.skill_id == skill_id:
                # Prefer courses whose coverage level matches the gap
                score = cs.coverage_level
                # Penalize if course difficulty doesn't match user
                if course.rating:
                    score += course.rating * 0.5
                if score > best_score:
                    best_score = score
                    best = course
    return best


def _find_best_project_for_skill(
    skill_id: int,
    projects: list[Project],
) -> Project | None:
    """Find a project that exercises a specific skill."""
    best = None
    best_importance = -1

    for project in projects:
        for ps in (project.project_skills or []):
            if ps.skill_id == skill_id and ps.importance > best_importance:
                best_importance = ps.importance
                best = project
    return best


def generate_learning_path(
    db: Session,
    user_id: int,
    career_id: int,
) -> dict:
    """
    Generate a complete, sequenced learning path for a user targeting a career.

    Steps:
        1. Calculate skill gaps
        2. Sort gaps by prerequisite order
        3. For each gap skill, find a course + optional project
        4. Skip skills the user has mastered
        5. Persist to learning_paths / learning_path_items
        6. Return the structured path

    If an active path for this career already exists, it is replaced.
    """

    # ── 1. Validate career ────────────────────────────────────────────
    career = db.query(Career).filter(Career.id == career_id).first()
    if not career:
        return {"error": f"Career with ID {career_id} not found."}

    # ── 2. Get profile ────────────────────────────────────────────────
    profile = (
        db.query(LearnerProfile)
        .filter(LearnerProfile.user_id == user_id)
        .first()
    )
    weekly_hours = (profile.learning_hours_per_week if profile else None) or 10

    # ── 3. Calculate skill gaps ───────────────────────────────────────
    gap_data = calculate_skill_gap(db, user_id, career_id)
    if "error" in gap_data:
        return gap_data

    # Separate ready skills from gap skills
    ready_skills = [s for s in gap_data["skills"] if s["status"] == "ready"]
    gap_skills = [s for s in gap_data["skills"] if s["gap"] > 0]

    # Build name map
    all_skill_names = {s["skill_id"]: s["skill"] for s in gap_data["skills"]}

    # Sort gap skills by prerequisite order
    sorted_gaps = _topological_sort_skills(gap_skills, all_skill_names)

    # ── 4. Load all courses and projects with skills ──────────────────
    courses = (
        db.query(Course)
        .options(joinedload(Course.course_skills).joinedload(CourseSkill.skill))
        .all()
    )
    projects = (
        db.query(Project)
        .options(joinedload(Project.project_skills).joinedload(ProjectSkill.skill))
        .all()
    )

    # ── 5. Build the sequence ─────────────────────────────────────────
    path_items_data = []
    seq = 1
    used_course_ids: set[int] = set()
    used_project_ids: set[int] = set()

    for skill_info in sorted_gaps:
        skill_id = skill_info["skill_id"]
        skill_name = skill_info["skill"]

        # Find best course for this skill
        course = _find_best_course_for_skill(skill_id, courses, skill_info["current_level"])
        if course and course.id not in used_course_ids:
            used_course_ids.add(course.id)
            path_items_data.append({
                "item_type": "course",
                "item_id": course.id,
                "sequence_number": seq,
                "title": course.title,
                "description": f"Build your {skill_name} skills",
                "status": "current" if seq == 1 else "locked",
                "is_locked": seq != 1,
                "estimated_hours": course.duration_hours,
            })
            seq += 1

        # Find best project for this skill (placed after the course)
        project = _find_best_project_for_skill(skill_id, projects)
        if project and project.id not in used_project_ids:
            used_project_ids.add(project.id)
            path_items_data.append({
                "item_type": "project",
                "item_id": project.id,
                "sequence_number": seq,
                "title": project.title,
                "description": f"Apply your {skill_name} knowledge",
                "status": "locked",
                "is_locked": True,
                "estimated_hours": project.estimated_hours,
            })
            seq += 1

    # ── 6. Calculate estimated duration ───────────────────────────────
    total_hours = sum(
        item["estimated_hours"] or 0 for item in path_items_data
    )
    estimated_months = round(total_hours / (weekly_hours * 4.33), 1) if weekly_hours > 0 else None

    # ── 7. Archive existing active paths for same career ──────────────
    existing_paths = (
        db.query(LearningPath)
        .filter(
            LearningPath.user_id == user_id,
            LearningPath.target_career_id == career_id,
            LearningPath.status.in_(["active", "in_progress", "draft"]),
        )
        .all()
    )
    for old_path in existing_paths:
        old_path.status = "archived"

    # ── 8. Create new learning path ───────────────────────────────────
    learning_path = LearningPath(
        user_id=user_id,
        target_career_id=career_id,
        title=f"Path to {career.name}",
        description=f"Personalized learning path to become a {career.name}. "
                     f"Focus areas: {', '.join(s['skill'] for s in sorted_gaps[:5])}",
        estimated_months=estimated_months,
        weekly_hours=float(weekly_hours),
        readiness_score=0.0,
        status="active",
    )
    db.add(learning_path)
    db.flush()  # Get the ID

    # Create learning path items
    for item_data in path_items_data:
        item = LearningPathItem(
            learning_path_id=learning_path.id,
            **item_data,
        )
        db.add(item)

    db.commit()
    db.refresh(learning_path)

    # ── 9. Build response ─────────────────────────────────────────────
    items_response = []
    for item_data in path_items_data:
        items_response.append({
            "sequence_number": item_data["sequence_number"],
            "item_type": item_data["item_type"],
            "item_id": item_data["item_id"],
            "title": item_data["title"],
            "description": item_data["description"],
            "status": item_data["status"],
            "is_locked": item_data["is_locked"],
            "estimated_hours": item_data["estimated_hours"],
        })

    return {
        "learning_path_id": learning_path.id,
        "title": learning_path.title,
        "description": learning_path.description,
        "career": career.name,
        "career_id": career.id,
        "readiness_score": 0.0,
        "estimated_months": estimated_months,
        "weekly_hours": weekly_hours,
        "total_items": len(items_response),
        "ready_skills": [s["skill"] for s in ready_skills],
        "items": items_response,
    }


def get_next_best_action(
    db: Session,
    user_id: int,
) -> dict | None:
    """
    Identify the single next best action for a user based on their
    active learning path.

    Looks at the active learning path and finds the first
    non-completed / non-skipped item.
    """

    # Find the most recent active learning path
    learning_path = (
        db.query(LearningPath)
        .filter(
            LearningPath.user_id == user_id,
            LearningPath.status.in_(["active", "in_progress"]),
        )
        .order_by(LearningPath.created_at.desc())
        .first()
    )

    if not learning_path:
        return None

    # Find the first actionable item
    items = (
        db.query(LearningPathItem)
        .filter(LearningPathItem.learning_path_id == learning_path.id)
        .order_by(LearningPathItem.sequence_number.asc())
        .all()
    )

    next_item = None
    for item in items:
        if item.status in ("current", "locked"):
            next_item = item
            break

    if not next_item:
        return {
            "title": "All items completed!",
            "type": "milestone",
            "item_id": None,
            "estimated_hours": 0,
            "priority": "low",
            "learning_path_id": learning_path.id,
            "reason_data": {
                "message": "You have completed all items in your learning path.",
                "career": learning_path.title,
            },
        }

    # Determine priority based on position
    total = len(items)
    position = next_item.sequence_number
    if position <= 2:
        priority = "high"
    elif position <= total * 0.5:
        priority = "medium"
    else:
        priority = "normal"

    # Get career skill gap context if available
    reason_data: dict = {
        "item_type": next_item.item_type,
        "sequence": f"{position}/{total}",
        "learning_path": learning_path.title,
    }

    # Try to provide skill gap context
    if learning_path.target_career_id:
        gap_data = calculate_skill_gap(db, user_id, learning_path.target_career_id)
        if "error" not in gap_data:
            # Find which skill this item addresses
            if next_item.item_id and next_item.item_type == "course":
                course_skills = (
                    db.query(CourseSkill)
                    .options(joinedload(CourseSkill.skill))
                    .filter(CourseSkill.course_id == next_item.item_id)
                    .all()
                )
                gap_skill_ids = {
                    s["skill_id"] for s in gap_data["skills"] if s["gap"] > 0
                }
                for cs in course_skills:
                    if cs.skill_id in gap_skill_ids:
                        gap_info = next(
                            s for s in gap_data["skills"]
                            if s["skill_id"] == cs.skill_id
                        )
                        reason_data["skill"] = gap_info["skill"]
                        reason_data["current_level"] = gap_info["current_level"]
                        reason_data["required_level"] = gap_info["required_level"]
                        reason_data["is_prerequisite"] = True
                        break

    return {
        "title": next_item.title,
        "type": next_item.item_type,
        "item_id": next_item.item_id,
        "estimated_hours": next_item.estimated_hours,
        "priority": priority,
        "learning_path_id": learning_path.id,
        "reason_data": reason_data,
    }
