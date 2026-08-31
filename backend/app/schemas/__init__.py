"""
Schemas package — re-export all schemas for convenience.
"""

from app.schemas.user import UserBase, UserCreate, UserRead, UserUpdate
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse,
)
from app.schemas.learner_profile import (
    LearnerProfileBase,
    LearnerProfileCreate,
    LearnerProfileUpdate,
    LearnerProfileResponse,
)
from app.schemas.skill import SkillBase, SkillCreate, SkillRead, SkillUpdate
from app.schemas.user_skill import (
    UserSkillBase,
    UserSkillCreateRequest,
    UserSkillUpdateRequest,
    UserSkillResponse,
    UserSkillMessageResponse,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UserRegisterRequest",
    "UserLoginRequest",
    "UserResponse",
    "TokenResponse",
    "LearnerProfileBase",
    "LearnerProfileCreate",
    "LearnerProfileUpdate",
    "LearnerProfileResponse",
    "SkillBase",
    "SkillCreate",
    "SkillRead",
    "SkillUpdate",
    "UserSkillBase",
    "UserSkillCreateRequest",
    "UserSkillUpdateRequest",
    "UserSkillResponse",
    "UserSkillMessageResponse",
]
