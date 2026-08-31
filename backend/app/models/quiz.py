"""
Quiz Models — 5 courses x 10 quizzes x 10 questions per quiz.
Includes Quiz, QuizQuestion, and UserQuizAttempt tables.
"""

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


class Quiz(Base):
    """Represents a course-specific quiz (10 quizzes per course)."""
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_slug = Column(String(100), nullable=False, index=True)  # frontend-developer, backend-developer, cybersecurity, software-development-engineer, ai-engineer
    quiz_number = Column(Integer, nullable=False)  # 1 to 10
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(String(50), default="Intermediate")
    time_minutes = Column(Integer, default=15)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("UserQuizAttempt", back_populates="quiz", cascade="all, delete-orphan")


class QuizQuestion(Base):
    """Represents a question within a quiz (10 questions per quiz)."""
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # List of 4 option strings
    correct_index = Column(Integer, nullable=False)  # 0 to 3
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    quiz = relationship("Quiz", back_populates="questions")


class UserQuizAttempt(Base):
    """Records a user's attempt at a quiz."""
    __tablename__ = "user_quiz_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, default=10, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    passed = Column(Boolean, nullable=False)
    submitted_answers = Column(JSON, nullable=True)  # Map question_id -> chosen index
    mistakes = Column(JSON, nullable=True)  # List of mistake dicts
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User")
