"""
Course Learning Models — complete interactive course learning workflow.
Includes course tracks, modules, lessons, assessments, questions, and user progress tables.
"""

from decimal import Decimal
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    JSON,
    func,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class CourseTrack(Base):
    """Represents a master career learning course program (e.g. Frontend Developer)."""
    __tablename__ = "course_tracks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    tagline = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    career_name = Column(String(100), nullable=False, index=True)
    difficulty = Column(String(50), default="Intermediate")
    estimated_duration = Column(String(50), default="12 Weeks")
    total_modules = Column(Integer, default=12)
    total_lessons = Column(Integer, default=36)
    total_projects = Column(Integer, default=4)
    total_assessments = Column(Integer, default=12)
    skills_covered = Column(JSON, nullable=True)  # List of skill strings
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    modules = relationship("CourseModule", back_populates="course", cascade="all, delete-orphan", order_by="CourseModule.module_number")
    final_assessment = relationship("CourseFinalAssessment", back_populates="course", uselist=False, cascade="all, delete-orphan")
    user_progress = relationship("UserCourseProgress", back_populates="course", cascade="all, delete-orphan")


class CourseModule(Base):
    """Represents a single module/chapter within a course."""
    __tablename__ = "course_modules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("course_tracks.id", ondelete="CASCADE"), nullable=False, index=True)
    module_number = Column(Integer, nullable=False)
    phase_name = Column(String(100), default="Phase 1: Foundations")
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    skills = Column(JSON, nullable=True)  # List of skill strings
    estimated_hours = Column(Float, default=4.0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    course = relationship("CourseTrack", back_populates="modules")
    lessons = relationship("CourseLesson", back_populates="module", cascade="all, delete-orphan", order_by="CourseLesson.lesson_number")
    assessment = relationship("ModuleAssessment", back_populates="module", uselist=False, cascade="all, delete-orphan")
    user_progress = relationship("UserModuleProgress", back_populates="module", cascade="all, delete-orphan")


class CourseLesson(Base):
    """Represents an interactive lesson with video, markdown content, and code snippets."""
    __tablename__ = "course_lessons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey("course_modules.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    video_url = Column(String(500), nullable=True)
    video_duration = Column(String(50), default="15 min")
    thumbnail_url = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)  # Rich educational text / markdown
    key_concepts = Column(JSON, nullable=True)  # List of key concept points
    code_snippet = Column(Text, nullable=True)  # Optional code example
    code_language = Column(String(50), default="javascript")
    has_coding = Column(Boolean, default=False, nullable=False)
    starter_code = Column(Text, nullable=True)
    default_language = Column(String(50), default="python", nullable=True)
    default_version = Column(String(50), nullable=True)
    coding_instructions = Column(Text, nullable=True)
    stdin_example = Column(Text, nullable=True)
    expected_output = Column(Text, nullable=True)
    resources = Column(JSON, nullable=True)  # List of dicts {title, url, type}
    learning_objectives = Column(JSON, nullable=True)  # List of objective strings
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    module = relationship("CourseModule", back_populates="lessons")
    user_progress = relationship("UserLessonProgress", back_populates="lesson", cascade="all, delete-orphan")


class ModuleAssessment(Base):
    """Represents a module MCQ diagnostic assessment."""
    __tablename__ = "module_assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey("course_modules.id", ondelete="CASCADE"), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    time_minutes = Column(Integer, default=15)
    passing_score = Column(Float, default=70.0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    module = relationship("CourseModule", back_populates="assessment")
    questions = relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")
    attempts = relationship("ModuleAssessmentAttempt", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentQuestion(Base):
    """Represents an interactive question (MCQ, multiple_select, scenario, coding) for a module assessment."""
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(Integer, ForeignKey("module_assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    question_type = Column(String(30), default="mcq", nullable=False)  # mcq, multiple_select, true_false, scenario, coding
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)  # List of string options (null for coding)
    correct_index = Column(Integer, nullable=True)  # 0-3 (for single select)
    correct_indices = Column(JSON, nullable=True)  # [0, 2] (for multiple select)
    starter_code = Column(Text, nullable=True)  # starter code for coding questions
    code_language = Column(String(50), default="python", nullable=True)
    test_cases_json = Column(JSON, nullable=True)  # list of {input, expected_output, is_hidden}
    related_lesson_id = Column(Integer, ForeignKey("course_lessons.id", ondelete="SET NULL"), nullable=True, index=True)
    related_skill_name = Column(String(100), nullable=True)
    difficulty = Column(String(30), default="medium", nullable=True)
    explanation = Column(Text, nullable=True)

    assessment = relationship("ModuleAssessment", back_populates="questions")
    related_lesson = relationship("CourseLesson", foreign_keys=[related_lesson_id])
    question_answers = relationship("AssessmentAnswer", back_populates="question", cascade="all, delete-orphan")


class CourseFinalAssessment(Base):
    """Represents a comprehensive final exam across all modules of a course."""
    __tablename__ = "course_final_assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("course_tracks.id", ondelete="CASCADE"), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    time_minutes = Column(Integer, default=45)
    passing_score = Column(Float, default=70.0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    course = relationship("CourseTrack", back_populates="final_assessment")
    questions = relationship("CourseFinalQuestion", back_populates="final_assessment", cascade="all, delete-orphan")
    attempts = relationship("CourseFinalAttempt", back_populates="final_assessment", cascade="all, delete-orphan")


class CourseFinalQuestion(Base):
    """Represents an MCQ question for the final course exam."""
    __tablename__ = "course_final_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    final_assessment_id = Column(Integer, ForeignKey("course_final_assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    correct_index = Column(Integer, nullable=False)
    topic = Column(String(100), nullable=True)
    explanation = Column(Text, nullable=True)

    final_assessment = relationship("CourseFinalAssessment", back_populates="questions")


# ── User Progress Tracking Tables ─────────────────────────────────────────────

class UserLessonProgress(Base):
    """Tracks a user's completion of individual lessons."""
    __tablename__ = "user_lesson_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("course_lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    lesson = relationship("CourseLesson", back_populates="user_progress")


class UserModuleProgress(Base):
    """Tracks a user's status and progress across modules."""
    __tablename__ = "user_module_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("course_modules.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="locked")  # locked, unlocked, in_progress, completed
    progress_percentage = Column(Float, default=0.0)
    assessment_passed = Column(Boolean, default=False)
    assessment_best_score = Column(Float, default=0.0)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    module = relationship("CourseModule", back_populates="user_progress")


class UserCourseProgress(Base):
    """Tracks a user's overall progress across a course program."""
    __tablename__ = "user_course_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("course_tracks.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="not_started")  # not_started, in_progress, completed
    progress_percentage = Column(Float, default=0.0)
    current_module_id = Column(Integer, nullable=True)
    current_lesson_id = Column(Integer, nullable=True)
    final_assessment_passed = Column(Boolean, default=False)
    final_score = Column(Float, default=0.0)
    final_grade = Column(String(10), nullable=True)
    started_at = Column(DateTime, server_default=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    course = relationship("CourseTrack", back_populates="user_progress")


class ModuleAssessmentAttempt(Base):
    """Records each attempt at a module test."""
    __tablename__ = "module_assessment_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = Column(Integer, ForeignKey("module_assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    passed = Column(Boolean, nullable=False)
    submitted_answers = Column(JSON, nullable=True)  # Dict question_id -> answer value
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    assessment = relationship("ModuleAssessment", back_populates="attempts")
    answers = relationship("AssessmentAnswer", back_populates="attempt", cascade="all, delete-orphan")


class AssessmentAnswer(Base):
    """Tracks individual question answers per attempt for detailed mistakes analysis."""
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    attempt_id = Column(Integer, ForeignKey("module_assessment_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("assessment_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_answer = Column(JSON, nullable=True)  # selected index, array of indices, or submitted code
    is_correct = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    attempt = relationship("ModuleAssessmentAttempt", back_populates="answers")
    question = relationship("AssessmentQuestion", back_populates="question_answers")



class CourseFinalAttempt(Base):
    """Records each attempt at the final comprehensive course exam."""
    __tablename__ = "course_final_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    final_assessment_id = Column(Integer, ForeignKey("course_final_assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("course_tracks.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    passed = Column(Boolean, nullable=False)
    grade = Column(String(10), default="F")
    submitted_answers = Column(JSON, nullable=True)
    skills_analysis = Column(JSON, nullable=True)  # Breakdown of strong vs weak topics
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    final_assessment = relationship("CourseFinalAssessment", back_populates="attempts")
