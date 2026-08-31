"""
News Router — Technical News API with personalized course ranking.
Fetches and ranks technical news (AI, Frontend, Backend, Cybersecurity, SDE, Cloud, DevOps)
tailored to the user's active personalized career path.
"""

from typing import Optional, List, Dict, Any
import urllib.request
import json
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.models.learner_profile import LearnerProfile
from app.models.career import Career
from app.models.career_goal import CareerGoal

router = APIRouter(prefix="/api/news", tags=["News"])

# Fallback curated technical news feed in case external network requests time out
CURATED_TECH_NEWS = [
    {
        "id": "tn-1",
        "title": "Next-Generation Transformer Architectures: Efficiency and Scalability in AI Engineering",
        "description": "Exploration of sparse attention mechanisms, flash attention updates, and real-time model quantization techniques for AI engineers.",
        "url": "https://dev.to/t/ai",
        "source": "AI Engineering Journal",
        "publishedAt": "2026-08-30T10:00:00Z",
        "category": "AI",
        "tags": ["AI", "Machine Learning", "Transformers", "Python"]
    },
    {
        "id": "tn-2",
        "title": "React 19 Server Components and Performance Optimizations in Modern Web Apps",
        "description": "Deep dive into automatic memoization, concurrent rendering, and zero-bundle-size server components for frontend engineers.",
        "url": "https://react.dev/blog",
        "source": "React Core Team",
        "publishedAt": "2026-08-30T08:30:00Z",
        "category": "Frontend",
        "tags": ["Frontend", "React", "JavaScript", "Web Dev"]
    },
    {
        "id": "tn-3",
        "title": "High-Throughput Microservices: Building Resilient REST & gRPC APIs with FastAPI & Go",
        "description": "Architectural strategies for connection pooling, asynchronous task queues, and zero-downtime database migrations.",
        "url": "https://dev.to/t/backend",
        "source": "Backend Engineering Monthly",
        "publishedAt": "2026-08-29T18:15:00Z",
        "category": "Backend",
        "tags": ["Backend", "FastAPI", "Python", "APIs", "Databases"]
    },
    {
        "id": "tn-4",
        "title": "Zero-Trust Cloud Security & Automated Threat Intelligence in 2026",
        "description": "Analyzing modern IAM enforcement, container vulnerability scanning, and eBPF kernel security monitoring.",
        "url": "https://dev.to/t/security",
        "source": "Cybersecurity Review",
        "publishedAt": "2026-08-29T14:20:00Z",
        "category": "Cybersecurity",
        "tags": ["Cybersecurity", "Cloud Security", "DevSecOps", "Linux"]
    },
    {
        "id": "tn-5",
        "title": "Software Systems Design: Distributed Caching and Low-Latency Storage Architecture",
        "description": "How modern tech companies scale distributed datastores to handle millions of requests per second.",
        "url": "https://github.com/topics/software-engineering",
        "source": "Systems Engineering Quarterly",
        "publishedAt": "2026-08-29T11:00:00Z",
        "category": "SDE",
        "tags": ["SDE", "Software Architecture", "System Design", "Cloud"]
    },
    {
        "id": "tn-6",
        "title": "PyTorch 2.5 Released: Compiler Accelerations and Multi-GPU Training Support",
        "description": "New features enabling faster LLM fine-tuning and reduced VRAM consumption for deep learning workloads.",
        "url": "https://pytorch.org/blog",
        "source": "PyTorch Official",
        "publishedAt": "2026-08-28T16:00:00Z",
        "category": "AI",
        "tags": ["AI", "PyTorch", "Deep Learning", "Python"]
    },
    {
        "id": "tn-7",
        "title": "Vite 6 and Tailwind CSS v4: The New Standard for Lightning Fast Web Build Tooling",
        "description": "Benchmarking Rust-powered bundlers, instant HMR, and CSS engine improvements in modern web development.",
        "url": "https://vite.dev/blog",
        "source": "Web Dev Weekly",
        "publishedAt": "2026-08-28T09:45:00Z",
        "category": "Frontend",
        "tags": ["Frontend", "Vite", "CSS", "TypeScript"]
    },
    {
        "id": "tn-[#8]",
        "title": "PostgreSQL 17 Performance Features: Parallel Query Execution & Index Optimizations",
        "description": "Detailed benchmark analysis of query optimizer enhancements, JSONB improvements, and replication safety.",
        "url": "https://www.postgresql.org/about/news",
        "source": "Database Systems Digest",
        "publishedAt": "2026-08-27T20:10:00Z",
        "category": "Backend",
        "tags": ["Backend", "PostgreSQL", "SQL", "Databases"]
    }
]


def fetch_live_tech_articles() -> List[Dict[str, Any]]:
    """Fetches real tech articles from Dev.to API."""
    try:
        req = urllib.request.Request(
            "https://dev.to/api/articles?top=7&per_page=15",
            headers={"User-Agent": "PathPilot-News-Fetcher/1.0"}
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status == 200:
                raw_articles = json.loads(response.read().decode())
                articles = []
                for item in raw_articles:
                    tags = [t.lower() for t in item.get("tag_list", [])]
                    category = "General Tech"
                    if any(t in tags for t in ["ai", "machinelearning", "python", "datascience", "llm"]):
                        category = "AI"
                    elif any(t in tags for t in ["react", "frontend", "javascript", "css", "webdev", "vue", "angular"]):
                        category = "Frontend"
                    elif any(t in tags for t in ["node", "backend", "python", "java", "sql", "api", "database", "golang"]):
                        category = "Backend"
                    elif any(t in tags for t in ["security", "cybersecurity", "cyber", "infosec", "hacking"]):
                        category = "Cybersecurity"
                    elif any(t in tags for t in ["architecture", "systemdesign", "sde", "programming", "devops", "cloud"]):
                        category = "SDE"

                    articles.append({
                        "id": f"devto-{item.get('id')}",
                        "title": item.get("title"),
                        "description": item.get("description") or "Latest technical updates and engineering deep dive.",
                        "url": item.get("url"),
                        "source": item.get("user", {}).get("name") or "Dev.to Tech",
                        "publishedAt": item.get("published_at"),
                        "category": category,
                        "tags": item.get("tag_list", ["Tech"]),
                        "cover_image": item.get("cover_image"),
                    })
                if articles:
                    return articles
    except Exception:
        pass
    return CURATED_TECH_NEWS


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get personalized technical news",
)
def get_technical_news(
    category: Optional[str] = Query(None, description="Optional category filter"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == current_user.id).first()
    goal = db.query(CareerGoal).filter(CareerGoal.user_id == current_user.id).order_by(CareerGoal.created_at.desc()).first()

    # Determine user's primary course category
    user_course = "Software Development Engineer"
    if goal and goal.identified_career_id:
        c_obj = db.query(Career).filter(Career.id == goal.identified_career_id).first()
        if c_obj: user_course = c_obj.name
    elif profile:
        user_course = profile.target_role or profile.career_goal_text or user_course

    user_cat = "SDE"
    uc_lower = user_course.lower()
    if "ai" in uc_lower or "machine" in uc_lower:
        user_cat = "AI"
    elif "frontend" in uc_lower or "web" in uc_lower:
        user_cat = "Frontend"
    elif "backend" in uc_lower:
        user_cat = "Backend"
    elif "cyber" in uc_lower or "security" in uc_lower:
        user_cat = "Cybersecurity"

    all_articles = fetch_live_tech_articles()

    # Priority sorting: articles matching user's course category first
    personalized_articles = [a for a in all_articles if a.get("category") == user_cat]
    other_articles = [a for a in all_articles if a.get("category") != user_cat]

    if category and category.lower() != "all" and category.lower() != "for you":
        filtered = [a for a in all_articles if a.get("category", "").lower() == category.lower()]
        return {
            "success": True,
            "user_category": user_cat,
            "user_course": user_course,
            "articles": filtered,
            "personalized_articles": filtered,
            "other_articles": [],
        }

    return {
        "success": True,
        "user_category": user_cat,
        "user_course": user_course,
        "articles": personalized_articles + other_articles,
        "personalized_articles": personalized_articles,
        "other_articles": other_articles,
    }


@router.get(
    "/{article_id}",
    status_code=status.HTTP_200_OK,
    summary="Get single technical news article detail",
)
def get_single_news_article(
    article_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    all_articles = fetch_live_tech_articles()
    matched = None
    for a in all_articles:
        if str(a.get("id")) == article_id or article_id in str(a.get("id")):
            matched = a
            break

    if not matched:
        # Fallback to searching curated news
        for a in CURATED_TECH_NEWS:
            if str(a.get("id")) == article_id:
                matched = a
                break

    if not matched:
        matched = all_articles[0] if all_articles else CURATED_TECH_NEWS[0]

    return {
        "success": True,
        "article": matched,
    }
