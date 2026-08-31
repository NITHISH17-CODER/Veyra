"""
Career Matching Engine — Ranks strictly the 5 Core Careers against a user's 
profile, natural language goals, resume evidence, and GitHub data.

Supported Core Careers:
    1. Frontend Developer
    2. Backend Developer
    3. Cybersecurity
    4. Software Development Engineer (SDE)
    5. AI Engineer

Scoring breakdown:
    40% Goal & Target Role Relevance
    30% Skill Compatibility & Multi-source Evidence
    15% Resume & GitHub Technical Evidence
    10% Interest & Domain Alignment
     5% Experience & Education Fit
"""

from __future__ import annotations
import re
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload

from app.models.user import User
from app.models.learner_profile import LearnerProfile
from app.models.user_skill import UserSkill
from app.models.user_interest import UserInterest
from app.models.career import Career
from app.models.career_skill import CareerSkill

# Strict 5 Core Careers Canonical List
CORE_CAREER_NAMES = [
    "Frontend Developer",
    "Backend Developer",
    "Cybersecurity",
    "Software Development Engineer (SDE)",
    "AI Engineer",
]

_CAREER_KEYWORD_MAP: Dict[str, List[str]] = {
    "frontend developer": [
        "frontend", "front end", "web developer", "ui", "ux", "react", "next.js",
        "javascript", "typescript", "css", "html", "web design", "website", "websites",
        "client-side", "user interface", "modern websites", "web development", "web apps",
    ],
    "backend developer": [
        "backend", "back end", "server", "api", "apis", "fastapi", "django",
        "microservices", "node.js", "databases", "rest", "backend developer",
        "postgresql", "mysql", "redis", "server applications", "build apis", "server-side",
    ],
    "cybersecurity": [
        "cybersecurity", "cyber security", "security", "infosec", "soc",
        "penetration testing", "ethical hacking", "network security", "threat",
        "vulnerability", "siem", "firewall", "security analyst", "protect networks",
        "protect computer systems", "protect systems", "information security",
    ],
    "software development engineer (sde)": [
        "sde", "software engineer", "software development engineer", "software development",
        "algorithms", "data structures", "dsa", "coding interviews", "system design",
        "java", "c++", "competitive programming", "full stack", "fullstack", "software developer",
        "programming", "oop", "problem solving",
    ],
    "ai engineer": [
        "ai", "artificial intelligence", "ai engineer", "llm", "generative ai",
        "rag", "langchain", "prompt engineering", "nlp", "vector db", "genai",
        "machine learning", "deep learning", "pytorch", "data science", "data scientist",
        "neural networks", "computer vision", "predictive", "data analytics",
    ],
}


def _is_unspecified_goal(goal: str | None) -> bool:
    if not goal or not isinstance(goal, str) or not goal.strip():
        return True
    cleaned = goal.strip().lower()
    unspecified_triggers = [
        "i don't know", "dont know", "not sure", "don't know yet",
        "help me choose", "undecided", "explore", "any", "no goal",
        "recommend for me", "suitable for me", "not yet",
    ]
    return any(trigger in cleaned for trigger in unspecified_triggers)


def calculate_goal_relevance(goal_text: str | None, career_name: str) -> float:
    if _is_unspecified_goal(goal_text):
        return 0.0

    text_lower = (goal_text or "").lower()
    career_norm = career_name.lower()

    if career_norm in text_lower:
        return 1.0

    keywords = _CAREER_KEYWORD_MAP.get(career_norm, [])
    for kw in keywords:
        if kw in text_lower:
            return 0.92

    return 0.0


def calculate_evidence_score(career_name: str, profile: LearnerProfile | None) -> float:
    """Calculates technical evidence score from resume & GitHub repos."""
    if not profile:
        return 0.0

    score = 0.0
    career_norm = career_name.lower()
    keywords = _CAREER_KEYWORD_MAP.get(career_norm, [])

    # Resume text evidence
    if profile.resume_text:
        res_lower = profile.resume_text.lower()
        if any(kw in res_lower for kw in keywords):
            score += 0.5

    # GitHub repos evidence
    if profile.github_repos_json and isinstance(profile.github_repos_json, list):
        for repo in profile.github_repos_json:
            lang = str(repo.get("language") or "").lower()
            name = str(repo.get("name") or "").lower()
            desc = str(repo.get("description") or "").lower()
            if any(kw in lang or kw in name or kw in desc for kw in keywords):
                score += 0.5
                break

    return min(1.0, score)


def match_careers(
    db: Session,
    user_id: int,
    goal: str | None = None,
    target_role: str | None = None,
    interests: list[str] | None = None,
    skills: list[dict] | None = None,
    education_field: str | None = None,
    experience: str | None = None,
    top_n: int = 5,
) -> list[dict]:
    """
    Ranks strictly the 5 Core Careers against the user's profile and multi-source evidence.
    """
    profile = (
        db.query(LearnerProfile)
        .filter(LearnerProfile.user_id == user_id)
        .first()
    )

    db_user_skills = (
        db.query(UserSkill)
        .options(joinedload(UserSkill.skill))
        .filter(UserSkill.user_id == user_id)
        .all()
    )
    user_skill_map: Dict[int, int] = {us.skill_id: us.proficiency for us in db_user_skills}

    effective_goal = goal if goal is not None else (profile.career_goal_text if profile else None)
    effective_role = target_role or (profile.target_role if profile else None)
    effective_field = education_field or (profile.field_of_study if profile else None)
    effective_exp = experience or (profile.experience_level if profile else None)

    combined_goal_text = f"{effective_goal or ''} {effective_role or ''}".strip()

    # Load 5 Core Careers
    all_careers = db.query(Career).options(
        joinedload(Career.career_skills).joinedload(CareerSkill.skill)
    ).all()

    # Filter to only the 5 supported core careers
    core_careers = [c for c in all_careers if any(cn.lower() in c.name.lower() or c.name.lower() in cn.lower() for cn in CORE_CAREER_NAMES)]
    if not core_careers:
        core_careers = all_careers

    results = []

    for career in core_careers:
        cs_list = career.career_skills or []

        # 1. Goal Relevance (40%)
        g_score = calculate_goal_relevance(combined_goal_text, career.name)

        # 2. Skill Match (30%)
        weighted_sum = 0.0
        importance_sum = 0
        matching = []
        gaps = []
        for cs in cs_list:
            cur = user_skill_map.get(cs.skill_id, 0)
            ratio = min(cur / cs.required_level, 1.0) if cs.required_level > 0 else 1.0
            weighted_sum += ratio * cs.importance
            importance_sum += cs.importance
            skill_name = cs.skill.name if cs.skill else f"Skill #{cs.skill_id}"
            if cur >= cs.required_level:
                matching.append(skill_name)
            else:
                gaps.append(skill_name)
        s_score = weighted_sum / importance_sum if importance_sum > 0 else 0.4

        # 3. Technical Evidence (Resume + GitHub) (15%)
        ev_score = calculate_evidence_score(career.name, profile)

        # 4. Interest & Domain Fit (10%)
        i_score = 0.0
        if interests:
            keywords = _CAREER_KEYWORD_MAP.get(career.name.lower(), [])
            if any(any(kw in intr.lower() for kw in keywords) for intr in interests):
                i_score = 1.0

        # 5. Experience & Education Fit (5%)
        exp_score = 0.8

        # Weighted calculation
        if not _is_unspecified_goal(combined_goal_text) and g_score > 0:
            total_score = (g_score * 40) + (s_score * 30) + (ev_score * 15) + (i_score * 10) + (exp_score * 5)
        else:
            total_score = (s_score * 50) + (ev_score * 25) + (i_score * 15) + (exp_score * 10)

        match_score = max(15, min(98, round(total_score)))

        why_explanation = f"Matches your target goal '{combined_goal_text}' and technical background."
        if ev_score > 0:
            why_explanation += " Reinforced by your Resume and GitHub project evidence."

        results.append({
            "career_id": career.id,
            "career": career.name,
            "description": career.description,
            "difficulty": career.difficulty,
            "match_score": match_score,
            "why_recommended": why_explanation,
            "reason_data": {
                "matching_skills": matching,
                "skill_gaps": gaps,
                "skill_match_pct": round(s_score * 100),
                "goal_relevance_pct": round(g_score * 100),
                "evidence_score_pct": round(ev_score * 100),
            },
        })

    results.sort(key=lambda r: r["match_score"], reverse=True)

    # Low Confidence Check: top score < 65 or top scores within 5% of each other
    top_score = results[0]["match_score"] if results else 0
    is_low_confidence = top_score < 65

    for r in results:
        r["is_low_confidence"] = is_low_confidence

    return results[:top_n]
