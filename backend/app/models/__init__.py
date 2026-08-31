"""
Models package — import all models here so that Alembic and Base.metadata
can discover them automatically.
"""

from app.models.user import User
from app.models.learner_profile import LearnerProfile
from app.models.interest import Interest
from app.models.user_interest import UserInterest
from app.models.user_preference import UserPreference
from app.models.career_goal import CareerGoal
from app.models.skill import Skill
from app.models.user_skill import UserSkill, PROFICIENCY_LEVELS
from app.models.career import Career
from app.models.career_skill import CareerSkill, REQUIRED_LEVELS
from app.models.course import Course, UserCourseEntitlement
from app.models.course_skill import CourseSkill, COVERAGE_LEVELS
from app.models.project import Project, UserProjectProgress
from app.models.project_skill import ProjectSkill, IMPORTANCE_LEVELS
from app.models.learning_path import LearningPath, LEARNING_PATH_STATUSES
from app.models.learning_path_item import LearningPathItem, ITEM_TYPES, ITEM_STATUSES
from app.models.course_learning import (
    CourseTrack,
    CourseModule,
    CourseLesson,
    ModuleAssessment,
    AssessmentQuestion,
    CourseFinalAssessment,
    CourseFinalQuestion,
    UserLessonProgress,
    UserModuleProgress,
    UserCourseProgress,
    ModuleAssessmentAttempt,
    CourseFinalAttempt,
    AssessmentAnswer,
)

from app.models.user_lesson_code import UserLessonCode

from app.models.user_streak import (
    UserLearningActivity,
    UserStreak,
    Notification,
    Certificate,
)

__all__ = [
    "User",
    "LearnerProfile",
    "Interest",
    "UserInterest",
    "UserPreference",
    "CareerGoal",
    "Skill",
    "UserSkill",
    "PROFICIENCY_LEVELS",
    "Career",
    "CareerSkill",
    "REQUIRED_LEVELS",
    "Course",
    "UserCourseEntitlement",
    "CourseSkill",
    "COVERAGE_LEVELS",
    "Project",
    "UserProjectProgress",
    "ProjectSkill",
    "IMPORTANCE_LEVELS",
    "LearningPath",
    "LEARNING_PATH_STATUSES",
    "LearningPathItem",
    "ITEM_TYPES",
    "ITEM_STATUSES",
    "CourseTrack",
    "CourseModule",
    "CourseLesson",
    "UserLessonCode",
    "ModuleAssessment",
    "AssessmentQuestion",
    "CourseFinalAssessment",
    "CourseFinalQuestion",
    "UserLessonProgress",
    "UserModuleProgress",
    "UserCourseProgress",
    "ModuleAssessmentAttempt",
    "CourseFinalAttempt",
    "AssessmentAnswer",
    "UserLearningActivity",
    "UserStreak",
    "Notification",
    "Certificate",
]

