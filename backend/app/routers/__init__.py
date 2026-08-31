"""
Routers package — export all routers for easy inclusion in FastAPI app.
"""

from app.routers.auth import router as auth_router
from app.routers.onboarding import router as onboarding_router
from app.routers.profile import router as profile_router
from app.routers.skills import router as skills_router
from app.routers.user_skills import router as user_skills_router
from app.routers.recommendations import router as recommendations_router
from app.routers.learning_path import router as learning_path_router
from app.routers.courses import router as courses_router
from app.routers.projects import router as projects_router
from app.routers.progress import router as progress_router
from app.routers.assessments import router as assessments_router
from app.routers.chat import router as chat_router
from app.routers.feedback import router as feedback_router
from app.routers.course_learning import router as course_learning_router
from app.routers.streak import router as streak_router
from app.routers.notifications import router as notifications_router
from app.routers.certificates import router as certificates_router
from app.routers.code_execution import router as code_execution_router
from app.routers.news import router as news_router

__all__ = [
    "auth_router",
    "onboarding_router",
    "profile_router",
    "skills_router",
    "user_skills_router",
    "recommendations_router",
    "learning_path_router",
    "courses_router",
    "projects_router",
    "progress_router",
    "assessments_router",
    "chat_router",
    "feedback_router",
    "course_learning_router",
    "streak_router",
    "notifications_router",
    "certificates_router",
    "code_execution_router",
    "news_router",
]
