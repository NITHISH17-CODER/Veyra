"""
AI package — Deterministic recommendation engines for PathPilot AI.

Modules:
    skill_gap           – Skill Gap Engine + Career Readiness Score
    career_matcher      – Career Matching Engine
    course_recommender  – Course Recommendation Engine
    project_recommender – Project Recommendation Engine
    roadmap_generator   – Learning Sequence + Next Best Action
"""

from app.ai.skill_gap import calculate_skill_gap
from app.ai.career_matcher import match_careers
from app.ai.course_recommender import recommend_courses
from app.ai.project_recommender import recommend_projects
from app.ai.roadmap_generator import generate_learning_path, get_next_best_action

__all__ = [
    "calculate_skill_gap",
    "match_careers",
    "recommend_courses",
    "recommend_projects",
    "generate_learning_path",
    "get_next_best_action",
]
