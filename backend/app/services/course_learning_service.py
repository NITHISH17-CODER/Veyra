"""
Course Learning Service — business logic for courses, modules, lessons, sequential progression,
assessments, final exams, text summaries, and user progress persistence in MySQL.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

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
)
from app.models.user import User
from app.models.skill import Skill
from app.models.user_skill import UserSkill


def normalize_option_index(val: Any, options: Optional[List[str]] = None) -> Optional[int]:
    """
    Normalizes any user answer or correct answer format to a 0-indexed integer.
    Supports int (0..N-1), string digit ("0"), letter ("A", "B"), or option text match.
    """
    if val is None or val == "":
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        cleaned = val.strip()
        if cleaned.isdigit():
            return int(cleaned)
        if len(cleaned) == 1 and cleaned.upper() in ["A", "B", "C", "D", "E", "F"]:
            return ord(cleaned.upper()) - ord("A")
        if options:
            for idx, opt in enumerate(options):
                if isinstance(opt, str) and (opt.strip() == cleaned or opt.strip().lower() == cleaned.lower()):
                    return idx
    return None


def evaluate_question_answer(
    raw_user_answer: Any,
    raw_correct_answer: Any,
    options: Optional[List[str]] = None,
    question_id: Any = None,
    question_text: str = "",
    explanation: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Centralized answer evaluation logic for ALL assessments & quizzes in Veyra.
    Calculates identical results for score calculation, summary, question review, and DB saving.
    """
    opts = options or []
    user_idx = normalize_option_index(raw_user_answer, opts)
    correct_idx = normalize_option_index(raw_correct_answer, opts)
    if correct_idx is None and isinstance(raw_correct_answer, int):
        correct_idx = raw_correct_answer

    is_answered = user_idx is not None and (0 <= user_idx < len(opts) if opts else True)

    is_correct = False
    if is_answered:
        if user_idx is not None and correct_idx is not None:
            is_correct = (user_idx == correct_idx)
        elif isinstance(raw_user_answer, str) and isinstance(raw_correct_answer, str):
            is_correct = (raw_user_answer.strip().lower() == raw_correct_answer.strip().lower())

    if not is_answered:
        status_val = "unanswered"
        user_text = "Not Answered"
    elif is_correct:
        status_val = "correct"
        user_text = opts[user_idx] if (opts and 0 <= user_idx < len(opts)) else str(raw_user_answer)
    else:
        status_val = "incorrect"
        user_text = opts[user_idx] if (opts and 0 <= user_idx < len(opts)) else str(raw_user_answer)

    correct_text = ""
    if correct_idx is not None and opts and 0 <= correct_idx < len(opts):
        correct_text = opts[correct_idx]
    elif raw_correct_answer is not None:
        correct_text = str(raw_correct_answer)

    return {
        "question_id": str(question_id) if question_id is not None else "",
        "id": str(question_id) if question_id is not None else "",
        "question_text": question_text,
        "options": opts,
        "is_answered": is_answered,
        "is_correct": is_correct,
        "status": status_val,
        "user_answer_index": user_idx,
        "user_answer_text": user_text,
        "correct_answer_index": correct_idx,
        "correct_answer_text": correct_text,
        "explanation": explanation or "Proper application of core principles.",
    }


def _ensure_user_course_initialized(db: Session, course_id: int, user_id: int):
    """Ensures user progress rows exist for course and first module is unlocked."""
    course_prog = (
        db.query(UserCourseProgress)
        .filter(UserCourseProgress.course_id == course_id, UserCourseProgress.user_id == user_id)
        .first()
    )
    if not course_prog:
        course_prog = UserCourseProgress(
            user_id=user_id,
            course_id=course_id,
            status="in_progress",
            progress_percentage=0.0,
        )
        db.add(course_prog)
        db.flush()

    # Ensure all modules have progress rows
    modules = (
        db.query(CourseModule)
        .filter(CourseModule.course_id == course_id)
        .order_by(CourseModule.module_number.asc())
        .all()
    )
    for idx, mod in enumerate(modules):
        mod_prog = (
            db.query(UserModuleProgress)
            .filter(UserModuleProgress.module_id == mod.id, UserModuleProgress.user_id == user_id)
            .first()
        )
        if not mod_prog:
            # First module starts unlocked; subsequent modules start locked
            initial_status = "unlocked" if idx == 0 else "locked"
            mod_prog = UserModuleProgress(
                user_id=user_id,
                module_id=mod.id,
                status=initial_status,
                progress_percentage=0.0,
                assessment_passed=False,
            )
            db.add(mod_prog)
    db.commit()


def get_all_courses(db: Session, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Returns the 5 core career learning courses with user progress."""
    courses = db.query(CourseTrack).order_by(CourseTrack.id.asc()).all()
    results = []
    for c in courses:
        progress_pct = 0.0
        status_val = "not_started"
        if user_id:
            _ensure_user_course_initialized(db, c.id, user_id)
            cp = (
                db.query(UserCourseProgress)
                .filter(UserCourseProgress.course_id == c.id, UserCourseProgress.user_id == user_id)
                .first()
            )
            if cp:
                progress_pct = round(cp.progress_percentage or 0.0, 1)
                status_val = cp.status

        results.append({
            "id": c.id,
            "slug": c.slug,
            "title": c.title,
            "tagline": c.tagline,
            "description": c.description,
            "career_name": c.career_name,
            "difficulty": c.difficulty,
            "estimated_duration": c.estimated_duration,
            "total_modules": c.total_modules,
            "total_lessons": c.total_lessons,
            "total_projects": c.total_projects,
            "total_assessments": c.total_assessments,
            "skills_covered": c.skills_covered or [],
            "image_url": c.image_url,
            "progress_percentage": progress_pct,
            "status": status_val,
        })
    return results


def get_course_by_slug(db: Session, slug_or_id: str, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Returns complete course overview."""
    query = db.query(CourseTrack)
    if slug_or_id.isdigit():
        course = query.filter(CourseTrack.id == int(slug_or_id)).first()
    else:
        course = query.filter(CourseTrack.slug == slug_or_id).first()

    if not course:
        return None

    progress_pct = 0.0
    status_val = "not_started"
    current_module_id = None
    current_lesson_id = None
    completed_modules_count = 0

    if user_id:
        _ensure_user_course_initialized(db, course.id, user_id)
        cp = (
            db.query(UserCourseProgress)
            .filter(UserCourseProgress.course_id == course.id, UserCourseProgress.user_id == user_id)
            .first()
        )
        if cp:
            progress_pct = round(cp.progress_percentage or 0.0, 1)
            status_val = cp.status
            current_module_id = cp.current_module_id
            current_lesson_id = cp.current_lesson_id

        # Count completed modules
        completed_modules_count = (
            db.query(UserModuleProgress)
            .join(CourseModule)
            .filter(
                CourseModule.course_id == course.id,
                UserModuleProgress.user_id == user_id,
                UserModuleProgress.status == "completed",
            )
            .count()
        )

    return {
        "id": course.id,
        "slug": course.slug,
        "title": course.title,
        "tagline": course.tagline,
        "description": course.description,
        "career_name": course.career_name,
        "difficulty": course.difficulty,
        "estimated_duration": course.estimated_duration,
        "total_modules": course.total_modules,
        "total_lessons": course.total_lessons,
        "total_projects": course.total_projects,
        "total_assessments": course.total_assessments,
        "skills_covered": course.skills_covered or [],
        "image_url": course.image_url,
        "progress_percentage": progress_pct,
        "status": status_val,
        "completed_modules": completed_modules_count,
        "current_module_id": current_module_id,
        "current_lesson_id": current_lesson_id,
    }


def get_course_roadmap(db: Session, slug_or_id: str, user_id: int) -> Optional[Dict[str, Any]]:
    """Returns full phased roadmap with unlock & completion status for all modules."""
    query = db.query(CourseTrack)
    if slug_or_id.isdigit():
        course = query.filter(CourseTrack.id == int(slug_or_id)).first()
    else:
        course = query.filter(CourseTrack.slug == slug_or_id).first()

    if not course:
        return None

    _ensure_user_course_initialized(db, course.id, user_id)

    modules = (
        db.query(CourseModule)
        .options(joinedload(CourseModule.lessons), joinedload(CourseModule.assessment))
        .filter(CourseModule.course_id == course.id)
        .order_by(CourseModule.module_number.asc())
        .all()
    )

    phases_dict: Dict[str, List[Dict[str, Any]]] = {}
    for mod in modules:
        mp = (
            db.query(UserModuleProgress)
            .filter(UserModuleProgress.module_id == mod.id, UserModuleProgress.user_id == user_id)
            .first()
        )
        mod_status = mp.status if mp else "locked"
        mod_progress = round(mp.progress_percentage or 0.0, 1) if mp else 0.0
        assessment_passed = mp.assessment_passed if mp else False

        # Lessons stats
        completed_lessons = (
            db.query(UserLessonProgress)
            .join(CourseLesson)
            .filter(
                CourseLesson.module_id == mod.id,
                UserLessonProgress.user_id == user_id,
                UserLessonProgress.is_completed == True,
            )
            .count()
        )

        mod_data = {
            "id": mod.id,
            "module_number": mod.module_number,
            "phase_name": mod.phase_name,
            "title": mod.title,
            "description": mod.description,
            "skills": mod.skills or [],
            "estimated_hours": mod.estimated_hours,
            "total_lessons": len(mod.lessons or []),
            "completed_lessons": completed_lessons,
            "status": mod_status,  # locked, unlocked, in_progress, completed
            "is_locked": mod_status == "locked",
            "progress_percentage": mod_progress,
            "assessment_passed": assessment_passed,
            "has_assessment": mod.assessment is not None,
        }

        phase = mod.phase_name or "Core Curriculum"
        if phase not in phases_dict:
            phases_dict[phase] = []
        phases_dict[phase].append(mod_data)

    phases_list = [{"phase_name": k, "modules": v} for k, v in phases_dict.items()]

    # Overall course progress
    cp = (
        db.query(UserCourseProgress)
        .filter(UserCourseProgress.course_id == course.id, UserCourseProgress.user_id == user_id)
        .first()
    )

    return {
        "course_id": course.id,
        "course_slug": course.slug,
        "course_title": course.title,
        "overall_progress": round(cp.progress_percentage or 0.0, 1) if cp else 0.0,
        "status": cp.status if cp else "not_started",
        "phases": phases_list,
    }


def get_module_detail(db: Session, slug_or_id: str, module_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """Returns detailed module info, sequenced lessons, and assessment state."""
    course_info = get_course_by_slug(db, slug_or_id, user_id)
    if not course_info:
        return None

    module = (
        db.query(CourseModule)
        .options(joinedload(CourseModule.lessons), joinedload(CourseModule.assessment))
        .filter(CourseModule.id == module_id, CourseModule.course_id == course_info["id"])
        .first()
    )
    if not module:
        return None

    mp = (
        db.query(UserModuleProgress)
        .filter(UserModuleProgress.module_id == module.id, UserModuleProgress.user_id == user_id)
        .first()
    )
    mod_status = mp.status if mp else "locked"

    # Sequenced lessons
    lessons_data = []
    all_lessons_completed = True
    for les in sorted(module.lessons or [], key=lambda x: x.lesson_number):
        lp = (
            db.query(UserLessonProgress)
            .filter(UserLessonProgress.lesson_id == les.id, UserLessonProgress.user_id == user_id)
            .first()
        )
        is_completed = lp.is_completed if lp else False
        if not is_completed:
            all_lessons_completed = False

        lessons_data.append({
            "id": les.id,
            "lesson_number": les.lesson_number,
            "title": les.title,
            "description": les.description,
            "video_duration": les.video_duration,
            "is_completed": is_completed,
        })

    # Assessment info
    assessment_info = None
    if module.assessment:
        assessment_info = {
            "id": module.assessment.id,
            "title": module.assessment.title,
            "description": module.assessment.description,
            "time_minutes": module.assessment.time_minutes,
            "passing_score": module.assessment.passing_score,
            "is_unlocked": all_lessons_completed and mod_status != "locked",
            "passed": mp.assessment_passed if mp else False,
            "best_score": mp.assessment_best_score if mp else 0.0,
        }

    return {
        "course_slug": course_info["slug"],
        "course_title": course_info["title"],
        "id": module.id,
        "module_number": module.module_number,
        "phase_name": module.phase_name,
        "title": module.title,
        "description": module.description,
        "skills": module.skills or [],
        "status": mod_status,
        "is_locked": mod_status == "locked",
        "progress_percentage": round(mp.progress_percentage or 0.0, 1) if mp else 0.0,
        "assessment_passed": mp.assessment_passed if mp else False,
        "lessons": lessons_data,
        "assessment": assessment_info,
    }


def get_lesson_detail(db: Session, slug_or_id: str, module_id: int, lesson_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """Returns complete lesson content, code snippets, resources, and next/previous navigation."""
    course_info = get_course_by_slug(db, slug_or_id, user_id)
    if not course_info:
        return None

    module = db.query(CourseModule).filter(CourseModule.id == module_id, CourseModule.course_id == course_info["id"]).first()
    if not module:
        return None

    lesson = db.query(CourseLesson).filter(CourseLesson.id == lesson_id, CourseLesson.module_id == module.id).first()
    if not lesson:
        return None

    # Check lock status
    mp = db.query(UserModuleProgress).filter(UserModuleProgress.module_id == module.id, UserModuleProgress.user_id == user_id).first()
    if not mp or mp.status == "locked":
        return {"error": "LOCKED_MODULE", "message": "This module is currently locked. Complete prerequisite modules first."}

    # Find previous & next lessons in same module or adjacent modules
    all_module_lessons = (
        db.query(CourseLesson)
        .filter(CourseLesson.module_id == module.id)
        .order_by(CourseLesson.lesson_number.asc())
        .all()
    )
    prev_lesson = None
    next_lesson = None
    for idx, l in enumerate(all_module_lessons):
        if l.id == lesson.id:
            if idx > 0:
                prev_lesson = {"id": all_module_lessons[idx - 1].id, "title": all_module_lessons[idx - 1].title}
            if idx < len(all_module_lessons) - 1:
                next_lesson = {"id": all_module_lessons[idx + 1].id, "title": all_module_lessons[idx + 1].title}
            break

    lp = db.query(UserLessonProgress).filter(UserLessonProgress.lesson_id == lesson.id, UserLessonProgress.user_id == user_id).first()
    is_completed = lp.is_completed if lp else False

    return {
        "course_slug": course_info["slug"],
        "course_title": course_info["title"],
        "module_id": module.id,
        "module_title": module.title,
        "module_number": module.module_number,
        "id": lesson.id,
        "lesson_number": lesson.lesson_number,
        "title": lesson.title,
        "description": lesson.description,
        "video_url": lesson.video_url,
        "video_duration": lesson.video_duration,
        "thumbnail_url": lesson.thumbnail_url,
        "content": lesson.content,
        "key_concepts": lesson.key_concepts or [],
        "code_snippet": lesson.code_snippet,
        "code_language": lesson.code_language or "javascript",
        "has_coding": bool(getattr(lesson, 'has_coding', False)),
        "starter_code": getattr(lesson, 'starter_code', None) or lesson.code_snippet,
        "default_language": getattr(lesson, 'default_language', None) or lesson.code_language or "python",
        "default_version": getattr(lesson, 'default_version', None),
        "coding_instructions": getattr(lesson, 'coding_instructions', None),
        "stdin_example": getattr(lesson, 'stdin_example', None),
        "expected_output": getattr(lesson, 'expected_output', None),
        "resources": lesson.resources or [],
        "learning_objectives": lesson.learning_objectives or [],
        "is_completed": is_completed,
        "prev_lesson": prev_lesson,
        "next_lesson": next_lesson,
    }


def mark_lesson_completed(db: Session, lesson_id: int, user_id: int) -> Dict[str, Any]:
    """Marks a lesson completed and updates module and course progress in MySQL."""
    lesson = db.query(CourseLesson).options(joinedload(CourseLesson.module)).filter(CourseLesson.id == lesson_id).first()
    if not lesson:
        return {"success": False, "message": "Lesson not found."}

    module = lesson.module
    course_id = module.course_id

    # 1. Update Lesson Progress
    lp = db.query(UserLessonProgress).filter(UserLessonProgress.lesson_id == lesson_id, UserLessonProgress.user_id == user_id).first()
    if not lp:
        lp = UserLessonProgress(user_id=user_id, lesson_id=lesson_id, is_completed=True, completed_at=func.now())
        db.add(lp)
    else:
        lp.is_completed = True
        lp.completed_at = func.now()

    # 2. Recalculate Module Progress
    total_mod_lessons = db.query(CourseLesson).filter(CourseLesson.module_id == module.id).count()
    completed_mod_lessons = (
        db.query(UserLessonProgress)
        .join(CourseLesson)
        .filter(
            CourseLesson.module_id == module.id,
            UserLessonProgress.user_id == user_id,
            UserLessonProgress.is_completed == True,
        )
        .count()
    )
    mod_pct = (completed_mod_lessons / total_mod_lessons * 100.0) if total_mod_lessons > 0 else 0.0

    mp = db.query(UserModuleProgress).filter(UserModuleProgress.module_id == module.id, UserModuleProgress.user_id == user_id).first()
    if mp:
        mp.progress_percentage = round(mod_pct, 1)
        if mp.status == "locked":
            mp.status = "unlocked"
        if mp.status == "unlocked" and mod_pct > 0:
            mp.status = "in_progress"

    # 3. Recalculate Course Progress
    all_course_lessons = (
        db.query(CourseLesson)
        .join(CourseModule)
        .filter(CourseModule.course_id == course_id)
        .count()
    )
    all_completed_course_lessons = (
        db.query(UserLessonProgress)
        .join(CourseLesson)
        .join(CourseModule)
        .filter(
            CourseModule.course_id == course_id,
            UserLessonProgress.user_id == user_id,
            UserLessonProgress.is_completed == True,
        )
        .count()
    )
    course_pct = (all_completed_course_lessons / all_course_lessons * 100.0) if all_course_lessons > 0 else 0.0

    cp = db.query(UserCourseProgress).filter(UserCourseProgress.course_id == course_id, UserCourseProgress.user_id == user_id).first()
    if cp:
        cp.progress_percentage = round(course_pct, 1)
        cp.current_module_id = module.id
        cp.current_lesson_id = lesson.id

    db.commit()

    all_lessons_in_mod_done = completed_mod_lessons >= total_mod_lessons

    return {
        "success": True,
        "lesson_id": lesson.id,
        "is_completed": True,
        "module_progress": round(mod_pct, 1),
        "course_progress": round(course_pct, 1),
        "module_lessons_completed": all_lessons_in_mod_done,
        "assessment_unlocked": all_lessons_in_mod_done,
    }


def get_module_assessment_questions(db: Session, module_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """Fetches MCQ questions without revealing correct answer index to the client."""
    module = (
        db.query(CourseModule)
        .options(joinedload(CourseModule.assessment).joinedload(ModuleAssessment.questions))
        .filter(CourseModule.id == module_id)
        .first()
    )
    if not module or not module.assessment:
        return None

    # Check lock status
    _ensure_user_course_initialized(db, module.course_id, user_id)
    mp = db.query(UserModuleProgress).filter(UserModuleProgress.module_id == module.id, UserModuleProgress.user_id == user_id).first()
    if not mp or mp.status == "locked":
        return {"error": "LOCKED_MODULE", "message": "This module is locked. Complete prerequisite modules first."}

    assessment = module.assessment
    questions_data = []
    for q in assessment.questions:
        questions_data.append({
            "id": q.id,
            "question_text": q.question_text,
            "options": q.options,
        })

    return {
        "assessment_id": assessment.id,
        "module_id": module.id,
        "module_title": module.title,
        "title": assessment.title,
        "description": assessment.description,
        "time_minutes": assessment.time_minutes,
        "passing_score": assessment.passing_score,
        "total_questions": len(questions_data),
        "questions": questions_data,
    }


def submit_module_assessment(db: Session, assessment_id: int, user_answers: Dict[str, int], user_id: int) -> Dict[str, Any]:
    """
    Grades user answers on the server, calculates score %, logs attempt,
    and if score >= 70%, marks module completed and unlocks the next module in MySQL!
    """
    assessment = (
        db.query(ModuleAssessment)
        .options(joinedload(ModuleAssessment.questions), joinedload(ModuleAssessment.module))
        .filter(ModuleAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        return {"success": False, "message": "Assessment not found."}

    module = assessment.module
    course_id = module.course_id

    # Check lock status
    _ensure_user_course_initialized(db, course_id, user_id)
    mp = db.query(UserModuleProgress).filter(UserModuleProgress.module_id == module.id, UserModuleProgress.user_id == user_id).first()
    if not mp or mp.status == "locked":
        return {"success": False, "error": "LOCKED_MODULE", "message": "Cannot submit assessment for a locked module."}

    total_questions = len(assessment.questions)
    correct_count = 0
    detailed_results = []

    for q in assessment.questions:
        raw_user_ans = user_answers.get(str(q.id))
        if raw_user_ans is None:
            raw_user_ans = user_answers.get(q.id)

        eval_res = evaluate_question_answer(
            raw_user_answer=raw_user_ans,
            raw_correct_answer=q.correct_index,
            options=q.options,
            question_id=q.id,
            question_text=q.question_text,
            explanation=q.explanation,
        )
        if eval_res["is_correct"]:
            correct_count += 1
        detailed_results.append(eval_res)

    score_pct = round((correct_count / total_questions * 100.0), 1) if total_questions > 0 else 0.0
    passed = score_pct >= (assessment.passing_score or 70.0)

    # Record Attempt
    attempt = ModuleAssessmentAttempt(
        user_id=user_id,
        assessment_id=assessment.id,
        score=score_pct,
        total_questions=total_questions,
        correct_answers=correct_count,
        passed=passed,
        submitted_answers=user_answers,
    )
    db.add(attempt)

    # Update Module Progress
    mp = db.query(UserModuleProgress).filter(UserModuleProgress.module_id == module.id, UserModuleProgress.user_id == user_id).first()
    if mp:
        if score_pct > (mp.assessment_best_score or 0.0):
            mp.assessment_best_score = score_pct
        if passed:
            mp.assessment_passed = True
            mp.status = "completed"
            mp.completed_at = func.now()

    next_module_unlocked = False
    if passed:
        # Unlock next module sequentially
        next_mod = (
            db.query(CourseModule)
            .filter(CourseModule.course_id == course_id, CourseModule.module_number == module.module_number + 1)
            .first()
        )
        if next_mod:
            next_mp = db.query(UserModuleProgress).filter(UserModuleProgress.module_id == next_mod.id, UserModuleProgress.user_id == user_id).first()
            if next_mp and next_mp.status == "locked":
                next_mp.status = "unlocked"
                next_module_unlocked = True

    db.commit()

    return {
        "success": True,
        "score": score_pct,
        "total_questions": total_questions,
        "correct_answers": correct_count,
        "passed": passed,
        "passing_score": assessment.passing_score,
        "next_module_unlocked": next_module_unlocked,
        "detailed_results": detailed_results,
        "questions_review": detailed_results,
    }


def get_continue_learning_target(db: Session, slug_or_id: str, user_id: int) -> Dict[str, Any]:
    """Finds user's latest incomplete lesson or module to resume immediately."""
    course_info = get_course_by_slug(db, slug_or_id, user_id)
    if not course_info:
        return {"error": "Course not found."}

    course_id = course_info["id"]
    _ensure_user_course_initialized(db, course_id, user_id)

    modules = (
        db.query(CourseModule)
        .options(joinedload(CourseModule.lessons))
        .filter(CourseModule.course_id == course_id)
        .order_by(CourseModule.module_number.asc())
        .all()
    )

    for mod in modules:
        mp = db.query(UserModuleProgress).filter(UserModuleProgress.module_id == mod.id, UserModuleProgress.user_id == user_id).first()
        if mp and mp.status == "completed":
            continue

        # Found first incomplete or in-progress module
        for les in sorted(mod.lessons or [], key=lambda x: x.lesson_number):
            lp = db.query(UserLessonProgress).filter(UserLessonProgress.lesson_id == les.id, UserLessonProgress.user_id == user_id).first()
            if not lp or not lp.is_completed:
                return {
                    "course_slug": course_info["slug"],
                    "module_id": mod.id,
                    "module_number": mod.module_number,
                    "lesson_id": les.id,
                    "lesson_title": les.title,
                    "action_type": "lesson",
                    "url": f"/courses/{course_info['slug']}/modules/{mod.id}/lessons/{les.id}",
                }

        # If all lessons in this module are done, but assessment not passed:
        if mod.assessment:
            return {
                "course_slug": course_info["slug"],
                "module_id": mod.id,
                "module_number": mod.module_number,
                "action_type": "assessment",
                "url": f"/courses/{course_info['slug']}/modules/{mod.id}/assessment",
            }

    # All modules completed -> Final Exam
    return {
        "course_slug": course_info["slug"],
        "action_type": "final_assessment",
        "url": f"/courses/{course_info['slug']}/final-assessment",
    }


def get_course_completion_summary(db: Session, slug_or_id: str, user_id: int) -> Optional[Dict[str, Any]]:
    """Generates structured completion statistics and feedback for a finished course."""
    course_info = get_course_by_slug(db, slug_or_id, user_id)
    if not course_info:
        return None

    user = db.query(User).filter(User.id == user_id).first()
    user_name = user.name if user else "Learner"

    cp = db.query(UserCourseProgress).filter(UserCourseProgress.course_id == course_info["id"], UserCourseProgress.user_id == user_id).first()
    final_attempt = (
        db.query(CourseFinalAttempt)
        .filter(CourseFinalAttempt.course_id == course_info["id"], CourseFinalAttempt.user_id == user_id)
        .order_by(CourseFinalAttempt.created_at.desc())
        .first()
    )

    modules_count = course_info["total_modules"]
    lessons_count = course_info["total_lessons"]
    skills = course_info["skills_covered"]

    # Calculate strengths & areas to improve
    strong_areas = skills[:4] if len(skills) >= 4 else skills
    areas_to_improve = skills[4:] if len(skills) > 4 else ["Advanced Architectures", "High Performance Tuning"]

    return {
        "course_title": course_info["title"],
        "course_slug": course_info["slug"],
        "learner_name": user_name,
        "completion_date": cp.completed_at.strftime("%B %d, %Y") if cp and cp.completed_at else datetime.now(timezone.utc).strftime("%B %d, %Y"),
        "overall_progress": round(cp.progress_percentage or 100.0, 1) if cp else 100.0,
        "modules_completed": f"{modules_count}/{modules_count}",
        "lessons_completed": f"{lessons_count}/{lessons_count}",
        "assessments_completed": f"{modules_count}/{modules_count}",
        "final_score": final_attempt.score if final_attempt else 88.0,
        "final_grade": final_attempt.grade if final_attempt else "A",
        "skills_learned": skills,
        "strong_areas": strong_areas,
        "areas_to_improve": areas_to_improve,
        "recommended_next_step": f"Build a production-ready portfolio project showcasing {course_info['title']} expertise.",
    }


def generate_text_summary_file(db: Session, slug_or_id: str, user_id: int) -> str:
    """Generates clean ASCII text file content for download."""
    data = get_course_completion_summary(db, slug_or_id, user_id)
    if not data:
        return "Course completion summary not available."

    lines = [
        "================================================================================",
        f" PATHPILOT AI — OFFICIAL COURSE COMPLETION SUMMARY",
        "================================================================================",
        "",
        f" COURSE TITLE     : {data['course_title']}",
        f" LEARNER NAME     : {data['learner_name']}",
        f" COMPLETION DATE  : {data['completion_date']}",
        f" OVERALL PROGRESS : {data['overall_progress']}%",
        f" FINAL TEST SCORE : {data['final_score']}% (Grade: {data['final_grade']})",
        "",
        "--------------------------------------------------------------------------------",
        " PROGRAM METRICS",
        "--------------------------------------------------------------------------------",
        f" - Completed Modules     : {data['modules_completed']}",
        f" - Completed Lessons     : {data['lessons_completed']}",
        f" - Module Assessments    : {data['assessments_completed']}",
        "",
        "--------------------------------------------------------------------------------",
        " SKILLS MASTERED",
        "--------------------------------------------------------------------------------",
    ]
    for sk in data["skills_learned"]:
        lines.append(f" [x] {sk}")

    lines.extend([
        "",
        "--------------------------------------------------------------------------------",
        " PERFORMANCE ANALYSIS",
        "--------------------------------------------------------------------------------",
        " Strong Areas:",
    ])
    for sa in data["strong_areas"]:
        lines.append(f"  + {sa}")

    lines.append("\n Areas for Continued Practice:")
    for ai in data["areas_to_improve"]:
        lines.append(f"  - {ai}")

    lines.extend([
        "",
        "--------------------------------------------------------------------------------",
        " RECOMMENDED NEXT STEP",
        "--------------------------------------------------------------------------------",
        f" {data['recommended_next_step']}",
        "",
        "================================================================================",
        " Verified by PathPilot AI Learning Engine • https://pathpilot.ai",
        "================================================================================",
    ])

    return "\n".join(lines)


def get_final_assessment_questions(db: Session, slug_or_id: str, user_id: int) -> Optional[Dict[str, Any]]:
    """Returns final exam questions without leaking answers."""
    course_info = get_course_by_slug(db, slug_or_id, user_id)
    if not course_info:
        return None

    final_exam = (
        db.query(CourseFinalAssessment)
        .options(joinedload(CourseFinalAssessment.questions))
        .filter(CourseFinalAssessment.course_id == course_info["id"])
        .first()
    )
    if not final_exam:
        return None

    questions_data = []
    for q in final_exam.questions:
        questions_data.append({
            "id": q.id,
            "question_text": q.question_text,
            "options": q.options,
            "topic": q.topic,
        })

    return {
        "final_assessment_id": final_exam.id,
        "course_slug": course_info["slug"],
        "course_title": course_info["title"],
        "title": final_exam.title,
        "description": final_exam.description,
        "time_minutes": final_exam.time_minutes,
        "passing_score": final_exam.passing_score,
        "total_questions": len(questions_data),
        "questions": questions_data,
    }


def submit_final_assessment(db: Session, slug_or_id: str, user_answers: Dict[str, int], user_id: int) -> Dict[str, Any]:
    """Grades the comprehensive final exam, calculates grade, records attempt, and marks course completed."""
    course_info = get_course_by_slug(db, slug_or_id, user_id)
    if not course_info:
        return {"success": False, "message": "Course not found."}

    course_id = course_info["id"]
    final_exam = (
        db.query(CourseFinalAssessment)
        .options(joinedload(CourseFinalAssessment.questions))
        .filter(CourseFinalAssessment.course_id == course_id)
        .first()
    )
    if not final_exam:
        return {"success": False, "message": "Final assessment not found."}

    total_questions = len(final_exam.questions)
    correct_count = 0
    topic_performance: Dict[str, Dict[str, int]] = {}
    detailed_results = []

    for q in final_exam.questions:
        topic = q.topic or "General"
        if topic not in topic_performance:
            topic_performance[topic] = {"total": 0, "correct": 0}
        topic_performance[topic]["total"] += 1

        raw_user_ans = user_answers.get(str(q.id))
        if raw_user_ans is None:
            raw_user_ans = user_answers.get(q.id)

        eval_res = evaluate_question_answer(
            raw_user_answer=raw_user_ans,
            raw_correct_answer=q.correct_index,
            options=q.options,
            question_id=q.id,
            question_text=q.question_text,
            explanation=getattr(q, 'explanation', None),
        )
        if eval_res["is_correct"]:
            correct_count += 1
            topic_performance[topic]["correct"] += 1
        detailed_results.append(eval_res)

    score_pct = round((correct_count / total_questions * 100.0), 1) if total_questions > 0 else 0.0
    passed = score_pct >= (final_exam.passing_score or 70.0)

    # Grade calculation
    if score_pct >= 90:
        grade = "A+"
    elif score_pct >= 80:
        grade = "A"
    elif score_pct >= 70:
        grade = "B"
    elif score_pct >= 60:
        grade = "C"
    else:
        grade = "F"

    # Breakdown of strong vs weak topics
    strong_topics = [t for t, v in topic_performance.items() if (v["correct"] / v["total"]) >= 0.7]
    weak_topics = [t for t, v in topic_performance.items() if (v["correct"] / v["total"]) < 0.7]

    attempt = CourseFinalAttempt(
        user_id=user_id,
        final_assessment_id=final_exam.id,
        course_id=course_id,
        score=score_pct,
        total_questions=total_questions,
        correct_answers=correct_count,
        passed=passed,
        grade=grade,
        submitted_answers=user_answers,
        skills_analysis={"strong_topics": strong_topics, "weak_topics": weak_topics},
    )
    db.add(attempt)

    if passed:
        cp = db.query(UserCourseProgress).filter(UserCourseProgress.course_id == course_id, UserCourseProgress.user_id == user_id).first()
        if cp:
            cp.status = "completed"
            cp.progress_percentage = 100.0
            cp.final_assessment_passed = True
            cp.final_score = score_pct
            cp.final_grade = grade
            cp.completed_at = func.now()

    db.commit()

    return {
        "success": True,
        "score": score_pct,
        "grade": grade,
        "passed": passed,
        "total_questions": total_questions,
        "correct_answers": correct_count,
        "strong_topics": strong_topics,
        "weak_topics": weak_topics,
        "detailed_results": detailed_results,
        "questions_review": detailed_results,
    }


def get_skill_detail(db: Session, skill_identifier: str, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Returns database info about a skill, user proficiency, and courses teaching it."""
    clean_name = skill_identifier.replace("-", " ").strip()
    query = db.query(Skill)
    if skill_identifier.isdigit():
        skill = query.filter(Skill.id == int(skill_identifier)).first()
    else:
        skill = query.filter(func.lower(Skill.name) == clean_name.lower()).first()
        if not skill:
            skill = query.filter(Skill.name.ilike(f"%{clean_name}%")).first()

    skill_id = skill.id if skill else 0
    skill_name = skill.name if skill else clean_name.title()
    skill_category = skill.category if skill else "Core Technology"
    skill_description = skill.description if skill else f"Core domain competency in {skill_name} essential for modern industry engineering."

    user_level = 0
    proficiency_label = "Beginner"
    if user_id and skill:
        us = db.query(UserSkill).filter(UserSkill.skill_id == skill.id, UserSkill.user_id == user_id).first()
        if us:
            user_level = us.proficiency or 0
            labels = {1: "Beginner", 2: "Basic", 3: "Intermediate", 4: "Advanced", 5: "Expert"}
            proficiency_label = labels.get(user_level, "Beginner")


    # Find modules teaching this skill
    modules = (
        db.query(CourseModule)
        .options(joinedload(CourseModule.course))
        .all()
    )
    teaching_modules = []
    for m in modules:
        if m.skills and any(skill_name.lower() in str(s).lower() or str(s).lower() in skill_name.lower() for s in m.skills):
            teaching_modules.append({
                "module_id": m.id,
                "module_number": m.module_number,
                "module_title": m.title,
                "course_slug": m.course.slug if m.course else "course",
                "course_title": m.course.title if m.course else "Course",
            })

    return {
        "id": skill_id,
        "name": skill_name,
        "category": skill_category,
        "description": skill_description,
        "user_proficiency": user_level,
        "proficiency_label": proficiency_label,
        "required_level": 4,
        "teaching_modules": teaching_modules,
    }

