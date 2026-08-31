"""
Chat Router — Comprehensive AI Assistant endpoint backed by full user profile,
learning path, courses, progress, streaks, certificates and real-time DB context.
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
import re

from app.database.session import get_db
from app.models.user import User
from app.models.learner_profile import LearnerProfile
from app.models.learning_path import LearningPath
from app.models.learning_path_item import LearningPathItem
from app.models.user_skill import UserSkill
from app.models.skill import Skill
from app.models.course_learning import (
    CourseTrack, CourseModule, CourseLesson,
    UserLessonProgress, UserModuleProgress, UserCourseProgress,
    ModuleAssessmentAttempt,
)
from app.core.deps import get_current_user
from app.ai.roadmap_generator import get_next_best_action

router = APIRouter(prefix="/api/chat", tags=["AI Assistant"])


class ChatMessageRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None
    page_context: Optional[dict] = None  # Current page info from frontend


# ─── Context builder ────────────────────────────────────────────────────────

def _build_user_context(db: Session, user: User) -> dict:
    """Gather all relevant user data for contextual AI responses."""

    # Profile
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == user.id).first()
    career_goal = profile.career_goal if profile and profile.career_goal else "Software Engineering"
    career_goal_text = profile.career_goal_text if profile and profile.career_goal_text else career_goal
    experience_level = profile.experience_level if profile else "Intermediate"

    # Skills
    user_skills = (
        db.query(UserSkill)
        .join(Skill, UserSkill.skill_id == Skill.id)
        .filter(UserSkill.user_id == user.id)
        .all()
    )
    mastered_skills = [us.skill.name for us in user_skills if us.proficiency >= 4]
    learning_skills = [us.skill.name for us in user_skills if us.proficiency < 4]

    # Learning Path
    path = (
        db.query(LearningPath)
        .filter(LearningPath.user_id == user.id, LearningPath.status.in_(["active", "in_progress"]))
        .order_by(LearningPath.created_at.desc())
        .first()
    )
    path_items = []
    completed_items = []
    pending_items = []
    next_action_item = None

    if path:
        items = (
            db.query(LearningPathItem)
            .filter(LearningPathItem.learning_path_id == path.id)
            .order_by(LearningPathItem.sequence_number)
            .all()
        )
        path_items = items
        completed_items = [i for i in items if i.status == "completed"]
        pending_items = [i for i in items if i.status != "completed"]
        next_action_item = next((i for i in items if i.status in ["current", "unlocked"]), None)
        if not next_action_item:
            next_action_item = pending_items[0] if pending_items else None

    # Course Progress
    course_progress_list = (
        db.query(UserCourseProgress)
        .options(joinedload(UserCourseProgress.course))
        .filter(UserCourseProgress.user_id == user.id)
        .all()
    )
    active_courses = [cp for cp in course_progress_list if cp.status == "in_progress"]
    completed_courses = [cp for cp in course_progress_list if cp.status == "completed"]

    # Current course context
    active_course = active_courses[0] if active_courses else None
    current_module_title = None
    current_lesson_title = None
    current_module_progress = 0

    if active_course and active_course.current_module_id:
        module = db.query(CourseModule).filter(CourseModule.id == active_course.current_module_id).first()
        if module:
            current_module_title = module.title
        mod_prog = db.query(UserModuleProgress).filter(
            UserModuleProgress.user_id == user.id,
            UserModuleProgress.module_id == active_course.current_module_id
        ).first()
        if mod_prog:
            current_module_progress = round(mod_prog.progress_percentage or 0)

    if active_course and active_course.current_lesson_id:
        lesson = db.query(CourseLesson).filter(CourseLesson.id == active_course.current_lesson_id).first()
        if lesson:
            current_lesson_title = lesson.title

    # Assessment results
    assessment_attempts = (
        db.query(ModuleAssessmentAttempt)
        .filter(ModuleAssessmentAttempt.user_id == user.id)
        .order_by(ModuleAssessmentAttempt.created_at.desc())
        .limit(5)
        .all()
    )
    passed_assessments = [a for a in assessment_attempts if a.passed]
    failed_assessments = [a for a in assessment_attempts if not a.passed]

    # Lesson progress
    completed_lesson_count = (
        db.query(UserLessonProgress)
        .filter(UserLessonProgress.user_id == user.id, UserLessonProgress.is_completed == True)
        .count()
    )

    # Available course tracks
    available_tracks = db.query(CourseTrack).limit(10).all()

    return {
        "user_name": user.name,
        "career_goal": career_goal_text or career_goal,
        "experience_level": experience_level,
        "mastered_skills": mastered_skills,
        "learning_skills": learning_skills,
        "total_skills": len(user_skills),
        "path_exists": path is not None,
        "total_path_items": len(path_items),
        "completed_items": len(completed_items),
        "pending_items": len(pending_items),
        "next_action": {
            "title": next_action_item.title,
            "type": next_action_item.item_type,
            "estimated_hours": next_action_item.estimated_hours,
        } if next_action_item else None,
        "active_courses": [
            {
                "title": cp.course.title if cp.course else "Course",
                "progress": round(cp.progress_percentage or 0),
                "slug": cp.course.slug if cp.course else "",
            }
            for cp in active_courses
        ],
        "completed_courses": [cp.course.title if cp.course else "Course" for cp in completed_courses],
        "current_course_title": active_course.course.title if active_course and active_course.course else None,
        "current_module_title": current_module_title,
        "current_lesson_title": current_lesson_title,
        "current_module_progress": current_module_progress,
        "current_course_progress": round(active_course.progress_percentage or 0) if active_course else 0,
        "completed_lessons_total": completed_lesson_count,
        "assessments_passed": len(passed_assessments),
        "assessments_attempted": len(assessment_attempts),
        "latest_score": round(assessment_attempts[0].score, 1) if assessment_attempts else None,
        "available_tracks": [{"title": t.title, "slug": t.slug, "career": t.career_name} for t in available_tracks],
    }


# ─── Intent classifier ──────────────────────────────────────────────────────

def _classify_intent(msg: str) -> str:
    """Classify the user's message intent for routing to the right response handler."""
    m = msg.lower()

    if re.search(r'\b(hello|hi|hey|howdy|greet|good (morning|evening|afternoon))\b', m):
        return "greeting"
    if re.search(r'\b(next|what should|what to (do|learn|study)|where do i (go|start)|continue|proceed)\b', m):
        return "next_action"
    if re.search(r'\b(progress|how (am i|far|many)|completion|percent|done|finished|complet)\b', m):
        return "progress"
    if re.search(r'\b(course|module|lesson|class|track|enroll|start|learn|study)\b', m):
        return "course_info"
    if re.search(r'\b(skill|strength|weakness|proficien|mastered|expert|beginner)\b', m):
        return "skills"
    if re.search(r'\b(assess|quiz|test|exam|score|result|pass|fail|grade)\b', m):
        return "assessment"
    if re.search(r'\b(career|goal|job|path|roadmap|profession|role|target)\b', m):
        return "career"
    if re.search(r'\b(streak|daily|habit|consistent|day|practice|login)\b', m):
        return "streak"
    if re.search(r'\b(certificate|certif|credential|badge|award|earn|complet)\b', m):
        return "certificate"
    if re.search(r'\b(project|build|implement|develop|portfolio|submit|work on)\b', m):
        return "project"
    if re.search(r'\b(help|guide|how to|explain|what is|what are|tell me|show me|navigate|go to|take me|open|find)\b', m):
        return "help"
    if re.search(r'\b(tip|advice|recommend|suggest|should i|better|improve|focus|priorit)\b', m):
        return "advice"
    if re.search(r'\b(python|javascript|java|react|sql|node|html|css|data science|machine learning|ai|ml)\b', m):
        return "topic_specific"

    return "general"


# ─── Response generators ────────────────────────────────────────────────────

def _response_greeting(ctx: dict) -> tuple[str, list, str | None]:
    name = ctx["user_name"]
    goal = ctx["career_goal"]
    course = ctx["current_course_title"]
    progress = ctx["current_course_progress"]

    if course:
        msg = (
            f"Hello {name}! 👋 Great to see you back!\n\n"
            f"You're currently working on **{course}** — {progress}% complete. "
            f"Your goal is to become a **{goal}** and you're making solid progress!\n\n"
            f"What can I help you with today?"
        )
    else:
        msg = (
            f"Hello {name}! 👋 Welcome to your PathPilot AI Assistant!\n\n"
            f"Your career goal is **{goal}**. I can help you navigate your learning path, "
            f"understand courses, check your progress, or plan your next steps.\n\n"
            f"What would you like to know?"
        )
    suggestions = ["What should I learn next?", "Show my progress", "What courses are available?"]
    return msg, suggestions, None


def _response_next_action(ctx: dict) -> tuple[str, list, str | None]:
    na = ctx["next_action"]
    if not na:
        msg = (
            f"Your learning path doesn't have a defined next step yet, {ctx['user_name']}.\n\n"
            f"I recommend heading to your **Dashboard** to generate a personalized path for "
            f"your goal of becoming a **{ctx['career_goal']}**!"
        )
        return msg, ["Go to Dashboard", "Explore Courses"], "/dashboard"

    course = ctx["current_course_title"]
    progress = ctx["current_course_progress"]
    lesson = ctx["current_lesson_title"]
    module = ctx["current_module_title"]

    if course and lesson:
        msg = (
            f"Your next step is to continue **{lesson}** in the **{module}** module of **{course}** "
            f"(currently {progress}% done).\n\n"
            f"📌 **Recommended Action**: {na['title']} ({na['type']} — est. {na['estimated_hours']:.1f} hrs)\n\n"
            f"Keep going — you're building toward your goal of becoming a **{ctx['career_goal']}**!"
        )
    else:
        msg = (
            f"Your next recommended action is:\n\n"
            f"📌 **{na['title']}** ({na['type']} — est. {na['estimated_hours']:.1f} hrs)\n\n"
            f"This is the most impactful next step toward your goal of **{ctx['career_goal']}**. "
            f"Head to your learning path to dive in!"
        )
    suggestions = ["Show my progress", "What skills am I missing?", "Open my courses"]
    nav = "/learning-path"
    return msg, suggestions, nav


def _response_progress(ctx: dict) -> tuple[str, list, str | None]:
    completed = ctx["completed_items"]
    total = ctx["total_path_items"]
    lessons = ctx["completed_lessons_total"]
    assessments = ctx["assessments_passed"]
    course_progress = ctx["current_course_progress"]
    course_name = ctx["current_course_title"]
    pct = round(completed / total * 100) if total > 0 else 0

    parts = [f"Here's your learning progress summary, **{ctx['user_name']}**:\n"]
    if course_name:
        parts.append(f"📚 **Current Course**: {course_name} — **{course_progress}%** complete")
    parts.append(f"✅ **Lessons Completed**: {lessons}")
    parts.append(f"🏆 **Assessments Passed**: {assessments}")
    parts.append(f"🗺️ **Learning Path**: {completed}/{total} items done ({pct}%)")

    if ctx["mastered_skills"]:
        parts.append(f"⭐ **Skills Mastered**: {', '.join(ctx['mastered_skills'][:5])}")

    if ctx["latest_score"] is not None:
        parts.append(f"📊 **Latest Assessment Score**: {ctx['latest_score']}%")

    msg = "\n".join(parts)
    if pct >= 80:
        msg += "\n\n🎉 You're very close to completing your learning path! Keep pushing!"
    elif pct >= 50:
        msg += "\n\n💪 Great momentum! You're more than halfway through!"
    else:
        msg += "\n\n🌱 Every lesson counts — keep going!"

    suggestions = ["What should I learn next?", "Show my courses", "Check my skills"]
    return msg, suggestions, "/progress"


def _response_course_info(ctx: dict) -> tuple[str, list, str | None]:
    active = ctx["active_courses"]
    completed = ctx["completed_courses"]
    available = ctx["available_tracks"]

    parts = [f"Here's an overview of your courses, **{ctx['user_name']}**:\n"]

    if active:
        parts.append("📖 **Active Courses**:")
        for c in active:
            parts.append(f"   • {c['title']} — {c['progress']}% complete")
    else:
        parts.append("You haven't enrolled in any courses yet.")

    if completed:
        parts.append(f"\n🎓 **Completed Courses**: {', '.join(completed)}")

    if available:
        parts.append(f"\n🌐 **Available Courses** ({len(available)} total):")
        for t in available[:4]:
            parts.append(f"   • {t['title']} (for {t['career']})")

    msg = "\n".join(parts)
    suggestions = ["Continue my current course", "What should I learn next?", "Show my progress"]
    return msg, suggestions, "/courses"


def _response_skills(ctx: dict) -> tuple[str, list, str | None]:
    mastered = ctx["mastered_skills"]
    learning = ctx["learning_skills"]

    parts = [f"Here's your skill profile, **{ctx['user_name']}**:\n"]
    if mastered:
        parts.append(f"⭐ **Mastered Skills** ({len(mastered)}):\n   {', '.join(mastered)}")
    else:
        parts.append("You haven't mastered any skills yet — that's what the journey is for!")

    if learning:
        parts.append(f"\n📈 **Skills In Progress** ({len(learning)}):\n   {', '.join(learning[:8])}")

    parts.append(f"\n🎯 **Target Career**: {ctx['career_goal']}")
    parts.append(f"📊 **Experience Level**: {ctx['experience_level']}")

    msg = "\n".join(parts)
    if mastered:
        msg += f"\n\nYou're on track! Focus on your learning path to grow your skill set further."
    else:
        msg += f"\n\nHead to the **Skill Gap Analysis** page to understand what you need to learn for {ctx['career_goal']}!"

    suggestions = ["Check my skill gap", "What skills do I need?", "Show my learning path"]
    return msg, suggestions, "/skill-gap"


def _response_assessment(ctx: dict) -> tuple[str, list, str | None]:
    attempted = ctx["assessments_attempted"]
    passed = ctx["assessments_passed"]
    score = ctx["latest_score"]

    parts = [f"Here's your assessment summary, **{ctx['user_name']}**:\n"]
    parts.append(f"📝 **Assessments Attempted**: {attempted}")
    parts.append(f"✅ **Assessments Passed**: {passed}")
    if score is not None:
        parts.append(f"📊 **Latest Score**: {score}%")
        if score >= 80:
            parts.append("🎉 Excellent performance!")
        elif score >= 70:
            parts.append("👍 Good job — you passed!")
        else:
            parts.append("💡 Tip: Review the module content and retry for a higher score.")

    if attempted == 0:
        parts = [
            f"You haven't taken any assessments yet, **{ctx['user_name']}**.\n\n"
            f"Assessments test your understanding after each module. They're a great way to "
            f"solidify your knowledge and move toward **{ctx['career_goal']}**!"
        ]

    msg = "\n".join(parts)
    suggestions = ["Show my courses", "What should I learn next?", "Check my progress"]
    return msg, suggestions, "/assessments"


def _response_career(ctx: dict) -> tuple[str, list, str | None]:
    goal = ctx["career_goal"]
    mastered = ctx["mastered_skills"]
    learning = ctx["learning_skills"]
    pct_done = round(ctx["completed_items"] / ctx["total_path_items"] * 100) if ctx["total_path_items"] > 0 else 0

    msg = (
        f"Your target career is **{goal}**, {ctx['user_name']}! 🎯\n\n"
        f"**Current Readiness**: {pct_done}% of your personalized learning path complete.\n\n"
    )
    if mastered:
        msg += f"✅ **Skills You Already Have**: {', '.join(mastered[:5])}\n"
    if learning:
        msg += f"📈 **Skills You're Building**: {', '.join(learning[:5])}\n"

    msg += (
        f"\nTo become job-ready as a **{goal}**, focus on completing your learning path, "
        f"building portfolio projects, and passing your module assessments!"
    )

    suggestions = ["What should I learn next?", "Show my skill gap", "View career analysis"]
    return msg, suggestions, "/career-analysis"


def _response_streak(ctx: dict) -> tuple[str, list, str | None]:
    name = ctx["user_name"]
    msg = (
        f"Learning streaks keep you consistent, **{name}**! 🔥\n\n"
        f"Log in every day and complete at least one lesson to maintain your streak. "
        f"The more consistent you are, the faster you'll reach your goal of becoming a **{ctx['career_goal']}**.\n\n"
        f"Head to your **Dashboard** to see your current streak and daily targets!"
    )
    suggestions = ["Go to Dashboard", "What should I study today?", "Show my progress"]
    return msg, suggestions, "/dashboard"


def _response_certificate(ctx: dict) -> tuple[str, list, str | None]:
    completed = ctx["completed_courses"]
    name = ctx["user_name"]

    if completed:
        msg = (
            f"Great news, **{name}**! 🎓\n\n"
            f"You've completed {len(completed)} course(s): **{', '.join(completed)}**\n\n"
            f"You can find and download your certificates from the **Certificates** section "
            f"in your profile or the sidebar. Keep completing courses to earn more!"
        )
    else:
        msg = (
            f"You haven't earned any certificates yet, **{name}**. 🎓\n\n"
            f"Complete a full course (including the final exam) to earn your certificate! "
            f"Start with your current course and work through each module and assessment.\n\n"
            f"You're working toward your goal of **{ctx['career_goal']}** — keep going!"
        )
    suggestions = ["Show my courses", "Check my progress", "View my profile"]
    return msg, suggestions, "/profile"


def _response_project(ctx: dict) -> tuple[str, list, str | None]:
    name = ctx["user_name"]
    goal = ctx["career_goal"]
    msg = (
        f"Projects are the best way to build your portfolio, **{name}**! 💻\n\n"
        f"For your goal of becoming a **{goal}**, hands-on projects demonstrate your skills to employers.\n\n"
        f"Head to the **Projects** section to browse available projects, submit your work, "
        f"and get AI-powered feedback on your implementation!"
    )
    suggestions = ["Browse Projects", "Show my learning path", "Check my progress"]
    return msg, suggestions, "/projects"


def _response_advice(ctx: dict) -> tuple[str, list, str | None]:
    na = ctx["next_action"]
    goal = ctx["career_goal"]
    mastered = ctx["mastered_skills"]
    learning = ctx["learning_skills"]
    pct_done = round(ctx["completed_items"] / ctx["total_path_items"] * 100) if ctx["total_path_items"] > 0 else 0

    tips = []
    if pct_done < 30:
        tips.append("🚀 **Start strong** — aim to complete at least one lesson every day.")
    elif pct_done < 70:
        tips.append("⚡ **Maintain momentum** — you're past the early stages, consistency is key now.")
    else:
        tips.append("🏁 **Sprint to the finish** — you're almost there! Push through the final modules.")

    if na:
        tips.append(f"📌 **Next focus**: {na['title']} ({na['type']})")

    if learning:
        tips.append(f"🎯 **Priority skills to build**: {', '.join(learning[:3])}")

    if not mastered:
        tips.append(f"💡 **Tip**: Focus on the fundamentals first. Strong foundations in {learning[0] if learning else 'core skills'} will speed up everything else.")

    tips.append(f"🧠 **Career goal**: Every hour you invest brings you closer to **{goal}**.")

    msg = f"Here's my personalized advice for you, **{ctx['user_name']}**:\n\n" + "\n".join(tips)
    suggestions = ["What should I learn next?", "Show my progress", "View my career path"]
    return msg, suggestions, "/learning-path"


def _response_topic_specific(msg_lower: str, ctx: dict) -> tuple[str, list, str | None]:
    goal = ctx["career_goal"]
    name = ctx["user_name"]
    mastered = ctx["mastered_skills"]
    learning = ctx["learning_skills"]

    topic = "this topic"
    if "python" in msg_lower:
        topic = "Python"
    elif "javascript" in msg_lower or "js" in msg_lower:
        topic = "JavaScript"
    elif "react" in msg_lower:
        topic = "React"
    elif "sql" in msg_lower or "database" in msg_lower:
        topic = "SQL/Databases"
    elif "machine learning" in msg_lower or "ml" in msg_lower:
        topic = "Machine Learning"
    elif "data science" in msg_lower:
        topic = "Data Science"
    elif "html" in msg_lower or "css" in msg_lower:
        topic = "HTML/CSS"
    elif "node" in msg_lower:
        topic = "Node.js"
    elif "java" in msg_lower:
        topic = "Java"

    is_mastered = any(topic.lower() in s.lower() for s in mastered)
    is_learning = any(topic.lower() in s.lower() for s in learning)

    if is_mastered:
        msg = (
            f"Great news, **{name}** — you've already mastered **{topic}**! ⭐\n\n"
            f"You can use this as a strength when applying for **{goal}** roles. "
            f"Consider building a portfolio project that showcases your {topic} skills!"
        )
    elif is_learning:
        msg = (
            f"**{topic}** is currently in your learning plan, **{name}**! 📈\n\n"
            f"It's an important skill for **{goal}**. Focus on completing the relevant lessons "
            f"and try the associated hands-on exercises to solidify your understanding."
        )
    else:
        msg = (
            f"**{topic}** is a valuable skill, **{name}**! 💡\n\n"
            f"While it may not be the highest priority for your current goal of **{goal}**, "
            f"it could be a useful complementary skill. Check your learning path to see how "
            f"it fits into your personalized roadmap."
        )

    suggestions = ["Show my learning path", "What should I focus on?", "Check my skills"]
    return msg, suggestions, "/courses"


def _response_greeting(ctx: dict) -> tuple[str, list, str | None]:
    name = ctx["user_name"]
    goal = ctx["career_goal"]
    course = ctx["current_course_title"]
    progress = ctx["current_course_progress"]

    if course:
        msg = (
            f"Hello {name}! 👋 Great to see you back on Veyra!\n\n"
            f"You're currently working on **{course}** — {progress}% complete. "
            f"Your goal is to become a **{goal}** and you're making solid progress!\n\n"
            f"What can I help you with today?"
        )
    else:
        msg = (
            f"Hello {name}! 👋 Welcome to your Veyra AI Assistant!\n\n"
            f"Your career goal is **{goal}**. I can help you navigate your learning path, "
            f"understand courses, check your progress, or plan your next steps.\n\n"
            f"What would you like to know?"
        )
    suggestions = ["What should I learn next?", "Show my progress", "What courses are available?"]
    return msg, suggestions, None


def _response_help(msg_lower: str, ctx: dict) -> tuple[str, list, str | None]:
    nav_map = {
        "dashboard": "/dashboard",
        "course": "/courses",
        "lesson": "/courses",
        "module": "/courses",
        "project": "/projects",
        "assessment": "/assessments",
        "profile": "/profile",
        "skill": "/skill-gap",
        "progress": "/progress",
        "certificate": "/profile",
        "roadmap": "/learning-path",
        "path": "/learning-path",
        "career": "/career-analysis",
        "ai assistant": "/ai-assistant",
        "setting": "/settings",
        "explore": "/courses",
    }

    for keyword, route in nav_map.items():
        if keyword in msg_lower:
            friendly = keyword.replace("-", " ").title()
            msg = (
                f"I can help you navigate to **{friendly}**, **{ctx['user_name']}**! 🧭\n\n"
                f"Click the button below or use the sidebar navigation to go there."
            )
            return msg, ["Show my progress", "What should I do next?"], route

    # Generic help
    msg = (
        f"I'm your Veyra AI Assistant, **{ctx['user_name']}**! 🤖\n\n"
        f"Here's what I can help with:\n"
        f"• 📚 Course & lesson navigation\n"
        f"• 📈 Progress tracking & analytics\n"
        f"• 🎯 Career goal guidance\n"
        f"• 🧠 Skill gap analysis\n"
        f"• 🗺️ Learning path recommendations\n"
        f"• 📝 Assessment tips\n"
        f"• 💼 Project guidance\n"
        f"• 🎓 Certificate information\n\n"
        f"Just ask me anything about your learning journey!"
    )
    suggestions = ["What should I learn next?", "Show my progress", "Check my skills"]
    return msg, suggestions, None


def _response_general(user_msg: str, ctx: dict) -> tuple[str, list, str | None]:
    goal = ctx["career_goal"]
    name = ctx["user_name"]
    na = ctx["next_action"]
    pct_done = round(ctx["completed_items"] / ctx["total_path_items"] * 100) if ctx["total_path_items"] > 0 else 0

    # Check active page context for context prioritization
    page = (ctx.get("current_page") or "").lower()
    page_context_prefix = ""
    nav_suggestion = None

    if "learning-path" in page or "roadmap" in page:
        page_context_prefix = f"Looking at your **Roadmap** toward **{goal}** ({pct_done}% complete):\n\n"
        nav_suggestion = "/learning-path"
    elif "course" in page or "learn" in page:
        curr_c = ctx.get("current_course_title") or "your course"
        page_context_prefix = f"Regarding your current course **{curr_c}** ({ctx.get('current_course_progress', 0)}% done):\n\n"
        nav_suggestion = "/courses"
    elif "assessment" in page or "quiz" in page:
        page_context_prefix = f"Regarding your assessments ({ctx.get('assessments_passed', 0)} passed):\n\n"
        nav_suggestion = "/assessments"
    elif "project" in page:
        page_context_prefix = f"Regarding your practical projects for **{goal}**:\n\n"
        nav_suggestion = "/projects"
    elif "skill" in page:
        mastered_cnt = len(ctx.get("mastered_skills", []))
        page_context_prefix = f"Regarding your skill inventory ({mastered_cnt} mastered):\n\n"
        nav_suggestion = "/skill-gap"
    elif "profile" in page:
        page_context_prefix = f"Regarding your profile and career goal **{goal}**:\n\n"
        nav_suggestion = "/profile"

    msg = (
        f"{page_context_prefix}"
        f"I analyzed your question about **\"{user_msg}\"** for your **{goal}** path, {name}.\n\n"
        f"Your current learning path is **{pct_done}%** complete. "
    )
    if na:
        msg += f"Your next recommended action is **{na['title']}** ({na['type']}).\n\n"
    msg += (
        f"Veyra AI is designed to guide you step-by-step toward becoming a **{goal}**. "
        f"If you have a specific question about your courses, progress, skills, or career path — ask away!"
    )
    suggestions = ["What should I learn next?", "Show my progress", "Give me learning advice"]
    return msg, suggestions, None


# ─── Main endpoint ───────────────────────────────────────────────────────────

@router.post("", status_code=status.HTTP_200_OK)
def chat_with_assistant(
    payload: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_msg = payload.message.strip()
    msg_lower = user_msg.lower()
    page_ctx = payload.page_context or {}

    # Build full user context from DB
    ctx = _build_user_context(db, current_user)

    # Enrich context with page context from frontend
    ctx["current_page"] = page_ctx.get("page", "")
    ctx["current_url"] = page_ctx.get("url", "")

    # Classify intent
    intent = _classify_intent(user_msg)

    # Route to appropriate handler
    if intent == "greeting":
        reply, suggestions, nav = _response_greeting(ctx)
    elif intent == "next_action":
        reply, suggestions, nav = _response_next_action(ctx)
    elif intent == "progress":
        reply, suggestions, nav = _response_progress(ctx)
    elif intent == "course_info":
        reply, suggestions, nav = _response_course_info(ctx)
    elif intent == "skills":
        reply, suggestions, nav = _response_skills(ctx)
    elif intent == "assessment":
        reply, suggestions, nav = _response_assessment(ctx)
    elif intent == "career":
        reply, suggestions, nav = _response_career(ctx)
    elif intent == "streak":
        reply, suggestions, nav = _response_streak(ctx)
    elif intent == "certificate":
        reply, suggestions, nav = _response_certificate(ctx)
    elif intent == "project":
        reply, suggestions, nav = _response_project(ctx)
    elif intent == "advice":
        reply, suggestions, nav = _response_advice(ctx)
    elif intent == "topic_specific":
        reply, suggestions, nav = _response_topic_specific(msg_lower, ctx)
    elif intent == "help":
        reply, suggestions, nav = _response_help(msg_lower, ctx)
    else:
        reply, suggestions, nav = _response_general(user_msg, ctx)

    import time
    return {
        "id": f"msg-{int(time.time() * 1000)}",
        "sender": "ai",
        "timestamp": "Just now",
        "content": reply,
        "suggestions": suggestions,
        "navigateTo": nav,
    }


@router.get("/context", status_code=status.HTTP_200_OK)
def get_chat_context(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns a summary of user context for the chatbot widget."""
    ctx = _build_user_context(db, current_user)
    return {
        "user_name": ctx["user_name"],
        "career_goal": ctx["career_goal"],
        "current_course": ctx["current_course_title"],
        "current_module": ctx["current_module_title"],
        "current_lesson": ctx["current_lesson_title"],
        "progress_pct": ctx["current_course_progress"],
        "next_action": ctx["next_action"],
        "mastered_skills_count": len(ctx["mastered_skills"]),
        "completed_lessons": ctx["completed_lessons_total"],
    }
