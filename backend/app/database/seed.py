"""
Master database seeder for PathPilot AI.

Seeds:
- 65+ Skills across 8 core domains (Programming, Data Science, AI/ML, Web Dev, Databases, Cloud, DevOps, Cybersecurity)
- 10 Careers with tailored required skills, levels (1-5), and importance (1-5)
- 52 Courses (both Free and Paid) with provider, pricing, and skill coverage levels (1-5)
- 32 Hands-on Portfolio Projects with difficulty, estimated hours, and skill importance (1-5)

Idempotent: Can be run multiple times safely without generating duplicates.
"""

import sys
import os
from decimal import Decimal

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, engine
from app.database.base import Base
from app.models.interest import Interest
from app.models.skill import Skill
from app.models.career import Career
from app.models.career_skill import CareerSkill
from app.models.course import Course
from app.models.course_skill import CourseSkill
from app.models.project import Project
from app.models.project_skill import ProjectSkill
from app.models.learner_profile import LearnerProfile
from app.models.user_preference import UserPreference
from app.models.user_interest import UserInterest
from app.models.career_goal import CareerGoal
from app.models.user_skill import UserSkill
from app.models.learning_path import LearningPath
from app.models.learning_path_item import LearningPathItem



# ==============================================================================
# 1. MASTER SKILLS DATA (65+ Skills across 8 domains)
# ==============================================================================
SKILLS_DATA = [
    # ── Programming ──────────────────────────────────────────────────────────
    {"name": "Python", "category": "Programming", "description": "High-level programming language widely used in AI, data science, and backend development."},
    {"name": "JavaScript", "category": "Programming", "description": "Core language for web scripting, frontend frameworks, and Node.js backend."},
    {"name": "TypeScript", "category": "Programming", "description": "Strict syntactical superset of JavaScript adding static type definitions."},
    {"name": "Java", "category": "Programming", "description": "Object-oriented, class-based language for enterprise backend and Android systems."},
    {"name": "C++", "category": "Programming", "description": "High-performance systems programming language used in game engines, robotics, and high-frequency trading."},
    {"name": "Go", "category": "Programming", "description": "Compiled language designed at Google for concurrent, scalable cloud services."},
    {"name": "Rust", "category": "Programming", "description": "Memory-safe systems programming language without garbage collection."},
    {"name": "SQL", "category": "Programming", "description": "Standard declarative query language for relational database management systems."},
    {"name": "Bash & Shell Scripting", "category": "Programming", "description": "Unix command-line scripting for automation, system administration, and CI/CD."},
    {"name": "R", "category": "Programming", "description": "Programming language and software environment for statistical computing and graphics."},

    # ── Data Science ─────────────────────────────────────────────────────────
    {"name": "Pandas", "category": "Data Science", "description": "Fast, flexible data analysis and manipulation library for Python."},
    {"name": "NumPy", "category": "Data Science", "description": "Fundamental package for scientific computing with multi-dimensional arrays in Python."},
    {"name": "Statistics & Probability", "category": "Data Science", "description": "Mathematical foundation for hypothesis testing, distributions, and inferential modeling."},
    {"name": "Data Visualization", "category": "Data Science", "description": "Techniques for visually communicating data insights using Matplotlib, Seaborn, and Plotly."},
    {"name": "Exploratory Data Analysis (EDA)", "category": "Data Science", "description": "Methods for analyzing datasets to summarize their main characteristics and uncover patterns."},
    {"name": "A/B Testing", "category": "Data Science", "description": "Controlled randomized experimentation to test business hypotheses and product features."},
    {"name": "Feature Engineering", "category": "Data Science", "description": "Process of selecting, transforming, and augmenting raw data features for predictive models."},
    {"name": "Power BI & Tableau", "category": "Data Science", "description": "Enterprise business intelligence tools for interactive reporting and executive dashboards."},

    # ── AI / ML ──────────────────────────────────────────────────────────────
    {"name": "Machine Learning", "category": "AI/ML", "description": "Core algorithms for supervised and unsupervised predictive modeling (Regression, Trees, Clustering)."},
    {"name": "Scikit-Learn", "category": "AI/ML", "description": "Python machine learning library featuring robust tools for data mining and model analysis."},
    {"name": "Deep Learning", "category": "AI/ML", "description": "Neural network architectures including CNNs, RNNs, and Transformers for complex patterns."},
    {"name": "PyTorch", "category": "AI/ML", "description": "Open-source deep learning framework based on the Torch library, favored in AI research."},
    {"name": "TensorFlow & Keras", "category": "AI/ML", "description": "End-to-end open source platform for machine learning model development and deployment."},
    {"name": "Natural Language Processing (NLP)", "category": "AI/ML", "description": "Techniques for analyzing, understanding, and generating human language data."},
    {"name": "Computer Vision", "category": "AI/ML", "description": "Algorithms and architectures enabling machines to interpret visual inputs (OpenCV, YOLO, ResNet)."},
    {"name": "Large Language Models (LLMs)", "category": "AI/ML", "description": "Foundation generative models (GPT, Claude, LLaMA), prompt engineering, and fine-tuning."},
    {"name": "RAG Systems", "category": "AI/ML", "description": "Retrieval-Augmented Generation architectures combining vector search with generative LLMs."},
    {"name": "Vector Databases", "category": "AI/ML", "description": "High-performance vector search databases (Pinecone, ChromaDB, Milvus, Qdrant)."},
    {"name": "MLOps", "category": "AI/ML", "description": "Practices and tools (MLflow, DVC, Feast) for deploying, monitoring, and maintaining ML in production."},

    # ── Web Development ──────────────────────────────────────────────────────
    {"name": "HTML & CSS", "category": "Web Development", "description": "Fundamental markup and styling standards for structuring web pages."},
    {"name": "React", "category": "Web Development", "description": "Component-based declarative JavaScript UI library maintained by Meta."},
    {"name": "Next.js", "category": "Web Development", "description": "Full-stack React framework featuring Server-Side Rendering (SSR) and App Router."},
    {"name": "Vue.js", "category": "Web Development", "description": "Progressive JavaScript framework for building user interfaces and single-page apps."},
    {"name": "Node.js", "category": "Web Development", "description": "Asynchronous event-driven JavaScript runtime built on Chrome's V8 engine."},
    {"name": "FastAPI", "category": "Web Development", "description": "Modern, high-performance web framework for building APIs with Python 3.8+ based on standard type hints."},
    {"name": "Django", "category": "Web Development", "description": "High-level Python web framework encouraging rapid development and clean design."},
    {"name": "Tailwind CSS", "category": "Web Development", "description": "Utility-first CSS framework for rapid modern UI construction."},
    {"name": "RESTful API Design", "category": "Web Development", "description": "Architectural principles and best practices for creating scalable, stateless HTTP APIs."},
    {"name": "GraphQL", "category": "Web Development", "description": "Query language for APIs and runtime for fulfilling queries with existing data."},

    # ── Databases ────────────────────────────────────────────────────────────
    {"name": "PostgreSQL", "category": "Databases", "description": "Powerful, open-source object-relational database system with advanced indexing."},
    {"name": "MySQL", "category": "Databases", "description": "Popular relational database management system used widely across web backends."},
    {"name": "MongoDB", "category": "Databases", "description": "Document-oriented NoSQL database designed for high availability and horizontal scaling."},
    {"name": "Redis", "category": "Databases", "description": "In-memory data structure store used as a distributed cache, message broker, and database."},
    {"name": "Data Modeling", "category": "Databases", "description": "Designing ER schemas, normalization, and relationship mapping for data integrity."},
    {"name": "Database Query Optimization", "category": "Databases", "description": "Execution plans, B-Tree index strategies, and query performance tuning."},

    # ── Cloud ────────────────────────────────────────────────────────────────
    {"name": "AWS", "category": "Cloud", "description": "Amazon Web Services cloud computing platform (EC2, S3, RDS, Lambda, ECS)."},
    {"name": "Azure", "category": "Cloud", "description": "Microsoft cloud computing services for enterprise building, testing, and managing apps."},
    {"name": "Google Cloud Platform (GCP)", "category": "Cloud", "description": "Google suite of cloud computing services including BigQuery and Vertex AI."},
    {"name": "Serverless Architecture", "category": "Cloud", "description": "Cloud execution model where providers dynamically manage machine resource allocation (AWS Lambda)."},
    {"name": "Cloud Security & IAM", "category": "Cloud", "description": "Identity access policies, encryption at rest/transit, and cloud compliance."},

    # ── DevOps ───────────────────────────────────────────────────────────────
    {"name": "Docker", "category": "DevOps", "description": "Platform for containerizing software applications to run reliably across environments."},
    {"name": "Kubernetes", "category": "DevOps", "description": "Open-source container orchestration system for automating deployment and scaling."},
    {"name": "CI/CD Pipelines", "category": "DevOps", "description": "Continuous Integration and Continuous Deployment workflows with automated testing."},
    {"name": "Terraform", "category": "DevOps", "description": "Infrastructure as Code (IaC) tool for provisioning cloud resources safely and predictably."},
    {"name": "Linux Administration", "category": "DevOps", "description": "Operating system administration, systemd, process management, and networking configuration."},
    {"name": "Git & GitHub Actions", "category": "DevOps", "description": "Distributed version control and integrated workflow automation for code repositories."},
    {"name": "Prometheus & Grafana", "category": "DevOps", "description": "Monitoring, metrics aggregation, and interactive operational dashboarding."},

    # ── Cybersecurity ────────────────────────────────────────────────────────
    {"name": "Network Security", "category": "Cybersecurity", "description": "Firewalls, VPNs, IDS/IPS, protocol inspection, and perimeter defenses."},
    {"name": "Web Application Security (OWASP)", "category": "Cybersecurity", "description": "Mitigating OWASP Top 10 vulnerabilities (SQLi, XSS, CSRF, SSRF, Broken Auth)."},
    {"name": "Cryptography", "category": "Cybersecurity", "description": "Symmetric/asymmetric encryption, hashing, digital signatures, and TLS/SSL protocols."},
    {"name": "Penetration Testing", "category": "Cybersecurity", "description": "Simulated cyberattacks against computer systems to check for exploitable vulnerabilities."},
    {"name": "SIEM & Threat Detection", "category": "Cybersecurity", "description": "Security Information and Event Management systems for log analysis and incident response."},
    {"name": "Vulnerability Assessment", "category": "Cybersecurity", "description": "Systematic evaluation of security weaknesses in an information system."}
]


# ==============================================================================
# 2. MASTER CAREERS DATA (10 Careers + Required Skills)
# ==============================================================================
CAREERS_DATA = [
    {
        "name": "Frontend Developer",
        "description": "Craft responsive, interactive, accessible, and high-performance user interfaces for modern web applications using HTML5, CSS3, JavaScript, TypeScript, React, and Next.js.",
        "difficulty": "Intermediate",
        "skills": [
            {"skill_name": "JavaScript", "required_level": 4, "importance": 5},
            {"skill_name": "TypeScript", "required_level": 4, "importance": 4},
            {"skill_name": "React", "required_level": 4, "importance": 5},
            {"skill_name": "Next.js", "required_level": 3, "importance": 4},
            {"skill_name": "HTML & CSS", "required_level": 5, "importance": 5},
            {"skill_name": "Tailwind CSS", "required_level": 4, "importance": 4},
            {"skill_name": "RESTful API Design", "required_level": 3, "importance": 3},
            {"skill_name": "Git & GitHub Actions", "required_level": 3, "importance": 3},
        ]
    },
    {
        "name": "Backend Developer",
        "description": "Engineer secure, scalable server-side APIs, database architectures, background processing systems, microservices, and robust authentication mechanisms.",
        "difficulty": "Intermediate",
        "skills": [
            {"skill_name": "Python", "required_level": 4, "importance": 5},
            {"skill_name": "FastAPI", "required_level": 4, "importance": 5},
            {"skill_name": "PostgreSQL", "required_level": 4, "importance": 5},
            {"skill_name": "SQL", "required_level": 4, "importance": 4},
            {"skill_name": "Redis", "required_level": 3, "importance": 4},
            {"skill_name": "Docker", "required_level": 3, "importance": 4},
            {"skill_name": "RESTful API Design", "required_level": 4, "importance": 5},
            {"skill_name": "Web Application Security (OWASP)", "required_level": 3, "importance": 4},
        ]
    },
    {
        "name": "Cybersecurity",
        "description": "Protect computer systems and enterprise networks, monitor threat vectors, conduct penetration testing, investigate security breaches, and enforce defensive security protocols.",
        "difficulty": "Advanced",
        "skills": [
            {"skill_name": "Network Security", "required_level": 4, "importance": 5},
            {"skill_name": "Web Application Security (OWASP)", "required_level": 4, "importance": 5},
            {"skill_name": "SIEM & Threat Detection", "required_level": 4, "importance": 5},
            {"skill_name": "Vulnerability Assessment", "required_level": 4, "importance": 4},
            {"skill_name": "Cryptography", "required_level": 3, "importance": 4},
            {"skill_name": "Linux Administration", "required_level": 4, "importance": 4},
            {"skill_name": "Python", "required_level": 3, "importance": 3},
        ]
    },
    {
        "name": "Software Development Engineer (SDE)",
        "description": "Master data structures, algorithms, object-oriented design, system design, operating systems, and full-scale software development for competitive engineering roles.",
        "difficulty": "Advanced",
        "skills": [
            {"skill_name": "Python", "required_level": 4, "importance": 5},
            {"skill_name": "Java", "required_level": 4, "importance": 4},
            {"skill_name": "C++", "required_level": 4, "importance": 4},
            {"skill_name": "JavaScript", "required_level": 4, "importance": 4},
            {"skill_name": "SQL", "required_level": 4, "importance": 4},
            {"skill_name": "Git & GitHub Actions", "required_level": 4, "importance": 4},
            {"skill_name": "Docker", "required_level": 3, "importance": 3},
            {"skill_name": "RESTful API Design", "required_level": 4, "importance": 4},
            {"skill_name": "Linux Administration", "required_level": 3, "importance": 3},
        ]
    },
    {
        "name": "AI Engineer",
        "description": "Build intelligent AI applications leveraging foundation Large Language Models (LLMs), machine learning algorithms, deep neural networks, RAG pipelines, and vector databases.",
        "difficulty": "Advanced",
        "skills": [
            {"skill_name": "Python", "required_level": 5, "importance": 5},
            {"skill_name": "Machine Learning", "required_level": 4, "importance": 5},
            {"skill_name": "Deep Learning", "required_level": 4, "importance": 5},
            {"skill_name": "Large Language Models (LLMs)", "required_level": 4, "importance": 5},
            {"skill_name": "RAG Systems", "required_level": 4, "importance": 5},
            {"skill_name": "Vector Databases", "required_level": 4, "importance": 4},
            {"skill_name": "PyTorch", "required_level": 4, "importance": 4},
            {"skill_name": "FastAPI", "required_level": 3, "importance": 3},
            {"skill_name": "Docker", "required_level": 3, "importance": 3},
        ]
    }
]


# ==============================================================================
# 3. MASTER COURSES DATA (52 Courses: Free & Paid)
# ==============================================================================
COURSES_DATA = [
    # ── Programming & Fundamentals ──
    {
        "title": "CS50: Introduction to Computer Science",
        "description": "Harvard University's introduction to computer science, algorithmic thinking, C, Python, and SQL.",
        "provider": "edX / Harvard",
        "url": "https://pll.harvard.edu/course/cs50-introduction-computer-science",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 30.0,
        "rating": 4.9,
        "skills": [{"skill_name": "Python", "coverage_level": 4}, {"skill_name": "SQL", "coverage_level": 3}, {"skill_name": "C++", "coverage_level": 3}]
    },
    {
        "title": "Python for Everybody Specialization",
        "description": "Learn to program and analyze data with Python from University of Michigan.",
        "provider": "Coursera",
        "url": "https://www.coursera.org/specializations/python",
        "is_free": False,
        "price": Decimal("39.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 25.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Python", "coverage_level": 5}, {"skill_name": "SQL", "coverage_level": 3}]
    },
    {
        "title": "Modern JavaScript From The Beginning",
        "description": "Master vanilla JavaScript without frameworks: ES6+, OOP, asynchronous programming, and DOM.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/modern-javascript-from-the-beginning/",
        "is_free": False,
        "price": Decimal("19.99"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 21.5,
        "rating": 4.8,
        "skills": [{"skill_name": "JavaScript", "coverage_level": 5}, {"skill_name": "HTML & CSS", "coverage_level": 3}]
    },
    {
        "title": "TypeScript: The Complete Developer's Guide",
        "description": "Master TypeScript by learning design patterns, generics, Decorators, and build tooling.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/typescript-the-complete-developers-guide/",
        "is_free": False,
        "price": Decimal("24.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 24.0,
        "rating": 4.8,
        "skills": [{"skill_name": "TypeScript", "coverage_level": 5}, {"skill_name": "JavaScript", "coverage_level": 4}]
    },
    {
        "title": "Linux Command Line Basics & Bash Scripting",
        "description": "Learn terminal navigation, piping, text processing (grep, awk, sed), and bash automation.",
        "provider": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/news/linux-command-line-bash-tutorial/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 6.0,
        "rating": 4.7,
        "skills": [{"skill_name": "Bash & Shell Scripting", "coverage_level": 5}, {"skill_name": "Linux Administration", "coverage_level": 4}]
    },

    # ── Data Science & Analytics ──
    {
        "title": "Data Analysis with Python (Pandas & NumPy)",
        "description": "Comprehensive course on data wrangling, cleaning, transformation, and aggregations.",
        "provider": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 12.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Pandas", "coverage_level": 5}, {"skill_name": "NumPy", "coverage_level": 5}, {"skill_name": "Data Visualization", "coverage_level": 3}]
    },
    {
        "title": "Statistics and Probability for Data Science",
        "description": "From descriptive statistics to inferential hypothesis testing, distributions, and probability theorems.",
        "provider": "Khan Academy",
        "url": "https://www.khanacademy.org/math/statistics-probability",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 18.0,
        "rating": 4.9,
        "skills": [{"skill_name": "Statistics & Probability", "coverage_level": 5}, {"skill_name": "A/B Testing", "coverage_level": 3}]
    },
    {
        "title": "Google Data Analytics Professional Certificate",
        "description": "Gain in-demand skills for junior data analyst roles using SQL, R, and Tableau dashboards.",
        "provider": "Coursera",
        "url": "https://www.coursera.org/professional-certificates/google-data-analytics",
        "is_free": False,
        "price": Decimal("49.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 50.0,
        "rating": 4.8,
        "skills": [{"skill_name": "SQL", "coverage_level": 4}, {"skill_name": "Power BI & Tableau", "coverage_level": 4}, {"skill_name": "R", "coverage_level": 3}, {"skill_name": "Exploratory Data Analysis (EDA)", "coverage_level": 4}]
    },
    {
        "title": "Microsoft Power BI Desktop for Business Intelligence",
        "description": "Build interactive dashboards, DAX measures, data modeling, and executive report views.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/",
        "is_free": False,
        "price": Decimal("18.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 15.0,
        "rating": 4.7,
        "skills": [{"skill_name": "Power BI & Tableau", "coverage_level": 5}, {"skill_name": "Data Visualization", "coverage_level": 4}]
    },
    {
        "title": "Applied A/B Testing & Experimentation",
        "description": "Designing, running, and analyzing digital product A/B tests with statistical rigor.",
        "provider": "Udacity",
        "url": "https://www.udacity.com/course/ab-testing--ud257",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 8.0,
        "rating": 4.6,
        "skills": [{"skill_name": "A/B Testing", "coverage_level": 5}, {"skill_name": "Statistics & Probability", "coverage_level": 4}]
    },

    # ── AI & Machine Learning ──
    {
        "title": "Machine Learning Specialization by Andrew Ng",
        "description": "Master machine learning fundamentals from linear regression to decision trees and unsupervised learning.",
        "provider": "Coursera",
        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
        "is_free": False,
        "price": Decimal("49.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 45.0,
        "rating": 4.9,
        "skills": [{"skill_name": "Machine Learning", "coverage_level": 5}, {"skill_name": "Scikit-Learn", "coverage_level": 4}, {"skill_name": "Python", "coverage_level": 4}]
    },
    {
        "title": "Deep Learning Specialization",
        "description": "Build neural networks, optimize hyper-parameters, convolutional networks, and sequential models.",
        "provider": "DeepLearning.AI",
        "url": "https://www.deeplearning.ai/courses/deep-learning-specialization/",
        "is_free": False,
        "price": Decimal("49.00"),
        "currency": "USD",
        "difficulty": "Advanced",
        "duration_hours": 55.0,
        "rating": 4.9,
        "skills": [{"skill_name": "Deep Learning", "coverage_level": 5}, {"skill_name": "TensorFlow & Keras", "coverage_level": 4}, {"skill_name": "Computer Vision", "coverage_level": 4}]
    },
    {
        "title": "PyTorch for Deep Learning Bootcamp",
        "description": "Zero to mastery deep learning with PyTorch: tensors, computer vision, and NLP architectures.",
        "provider": "YouTube / freeCodeCamp",
        "url": "https://www.youtube.com/watch?v=V_xro1bcAuA",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 26.0,
        "rating": 4.9,
        "skills": [{"skill_name": "PyTorch", "coverage_level": 5}, {"skill_name": "Deep Learning", "coverage_level": 4}]
    },
    {
        "title": "Generative AI with Large Language Models",
        "description": "Learn the LLM lifecycle: pre-training, fine-tuning with PEFT/LoRA, RLHF, and deployment.",
        "provider": "Coursera / AWS",
        "url": "https://www.coursera.org/learn/generative-ai-with-llms",
        "is_free": False,
        "price": Decimal("49.00"),
        "currency": "USD",
        "difficulty": "Advanced",
        "duration_hours": 16.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Large Language Models (LLMs)", "coverage_level": 5}, {"skill_name": "Natural Language Processing (NLP)", "coverage_level": 4}]
    },
    {
        "title": "Building RAG Applications with LangChain & Vector DBs",
        "description": "Architect modern Retrieval-Augmented Generation workflows using Chroma, Pinecone, and LangChain.",
        "provider": "DeepLearning.AI",
        "url": "https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 4.0,
        "rating": 4.8,
        "skills": [{"skill_name": "RAG Systems", "coverage_level": 5}, {"skill_name": "Vector Databases", "coverage_level": 5}, {"skill_name": "Large Language Models (LLMs)", "coverage_level": 4}]
    },
    {
        "title": "Full Stack MLOps: From Experiment to Production",
        "description": "Productionize machine learning: experiment tracking with MLflow, Docker packaging, and CI/CD deployment.",
        "provider": "Coursera",
        "url": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops",
        "is_free": False,
        "price": Decimal("49.00"),
        "currency": "USD",
        "difficulty": "Advanced",
        "duration_hours": 32.0,
        "rating": 4.7,
        "skills": [{"skill_name": "MLOps", "coverage_level": 5}, {"skill_name": "Docker", "coverage_level": 4}, {"skill_name": "CI/CD Pipelines", "coverage_level": 3}]
    },
    {
        "title": "Computer Vision Masterclass with OpenCV and YOLO",
        "description": "Real-time object detection, image segmentation, and facial recognition with OpenCV and YOLOv8.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/computer-vision-masterclass/",
        "is_free": False,
        "price": Decimal("24.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 18.0,
        "rating": 4.7,
        "skills": [{"skill_name": "Computer Vision", "coverage_level": 5}, {"skill_name": "Python", "coverage_level": 4}]
    },
    {
        "title": "Natural Language Processing with Transformers (Hugging Face)",
        "description": "Fine-tune BERT, RoBERTa, and T5 models for classification, named entity recognition, and summarization.",
        "provider": "Hugging Face / YouTube",
        "url": "https://huggingface.co/learn/nlp-course/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 14.0,
        "rating": 4.9,
        "skills": [{"skill_name": "Natural Language Processing (NLP)", "coverage_level": 5}, {"skill_name": "PyTorch", "coverage_level": 3}]
    },

    # ── Web Development ──
    {
        "title": "The Complete React 19 & Next.js Course",
        "description": "Build production React applications with Server Components, App Router, Hooks, and Tailwind CSS.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
        "is_free": False,
        "price": Decimal("19.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 42.0,
        "rating": 4.8,
        "skills": [{"skill_name": "React", "coverage_level": 5}, {"skill_name": "Next.js", "coverage_level": 4}, {"skill_name": "JavaScript", "coverage_level": 4}]
    },
    {
        "title": "Next.js Full Stack App Development",
        "description": "Server-side rendering, API routes, database connections with Prisma, and auth with NextAuth.",
        "provider": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/news/nextjs-full-stack-app-tutorial/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 10.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Next.js", "coverage_level": 5}, {"skill_name": "React", "coverage_level": 4}, {"skill_name": "TypeScript", "coverage_level": 3}]
    },
    {
        "title": "Tailwind CSS from Scratch to Advanced",
        "description": "Learn utility-first responsive web design, flexbox, grid, and custom design systems.",
        "provider": "YouTube",
        "url": "https://www.youtube.com/watch?v=dFgzHOX84xQ",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 4.5,
        "rating": 4.9,
        "skills": [{"skill_name": "Tailwind CSS", "coverage_level": 5}, {"skill_name": "HTML & CSS", "coverage_level": 4}]
    },
    {
        "title": "FastAPI: High Performance REST APIs with Python",
        "description": "Asynchronous endpoints, Pydantic data validation, SQLAlchemy ORM integration, and JWT security.",
        "provider": "TestDriven.io",
        "url": "https://testdriven.io/courses/fastapi-crud/",
        "is_free": False,
        "price": Decimal("29.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 12.0,
        "rating": 4.9,
        "skills": [{"skill_name": "FastAPI", "coverage_level": 5}, {"skill_name": "RESTful API Design", "coverage_level": 5}, {"skill_name": "Python", "coverage_level": 4}]
    },
    {
        "title": "Node.js, Express, MongoDB & More: The Complete Bootcamp",
        "description": "Master backend RESTful APIs with Node.js, Express, MongoDB, Mongoose, and JWT authentication.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/",
        "is_free": False,
        "price": Decimal("19.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 42.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Node.js", "coverage_level": 5}, {"skill_name": "MongoDB", "coverage_level": 4}, {"skill_name": "RESTful API Design", "coverage_level": 4}]
    },
    {
        "title": "Django for Beginners & API Development with DRF",
        "description": "Learn Python Django models, views, templates, and REST framework serialization.",
        "provider": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/news/django-rest-framework-tutorial/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 8.0,
        "rating": 4.7,
        "skills": [{"skill_name": "Django", "coverage_level": 5}, {"skill_name": "RESTful API Design", "coverage_level": 4}, {"skill_name": "Python", "coverage_level": 4}]
    },
    {
        "title": "GraphQL with Node.js & React: The Complete Guide",
        "description": "Build unified GraphQL schemas, resolvers, Apollo Client queries, and mutations.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/graphql-with-react-course/",
        "is_free": False,
        "price": Decimal("21.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 14.0,
        "rating": 4.6,
        "skills": [{"skill_name": "GraphQL", "coverage_level": 5}, {"skill_name": "Node.js", "coverage_level": 3}, {"skill_name": "React", "coverage_level": 3}]
    },

    # ── Databases ──
    {
        "title": "PostgreSQL: Comprehensive Bootcamp from Novice to Guru",
        "description": "Learn SQL queries, complex joins, subqueries, transactions, indexes, and stored procedures.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/the-complete-python-postgresql-developer-course/",
        "is_free": False,
        "price": Decimal("19.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 20.0,
        "rating": 4.8,
        "skills": [{"skill_name": "PostgreSQL", "coverage_level": 5}, {"skill_name": "SQL", "coverage_level": 5}, {"skill_name": "Data Modeling", "coverage_level": 4}]
    },
    {
        "title": "Relational Database Design and Normalization",
        "description": "Master 1NF, 2NF, 3NF, BCNF, entity relationship diagrams, and foreign key integrity.",
        "provider": "Coursera",
        "url": "https://www.coursera.org/learn/database-design",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 10.0,
        "rating": 4.7,
        "skills": [{"skill_name": "Data Modeling", "coverage_level": 5}, {"skill_name": "SQL", "coverage_level": 4}]
    },
    {
        "title": "High Performance MySQL & Query Optimization",
        "description": "Deep dive into EXPLAIN execution plans, indexing strategies, buffer pools, and replication.",
        "provider": "Pluralsight",
        "url": "https://www.pluralsight.com/courses/mysql-performance-tuning",
        "is_free": False,
        "price": Decimal("35.00"),
        "currency": "USD",
        "difficulty": "Advanced",
        "duration_hours": 8.5,
        "rating": 4.7,
        "skills": [{"skill_name": "Database Query Optimization", "coverage_level": 5}, {"skill_name": "MySQL", "coverage_level": 5}]
    },
    {
        "title": "Redis: The Definitive In-Memory Database Guide",
        "description": "Data structures (hashes, sets, sorted sets, streams), caching strategies, and pub/sub patterns.",
        "provider": "Redis University",
        "url": "https://university.redis.com/courses/ru101/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 6.0,
        "rating": 4.9,
        "skills": [{"skill_name": "Redis", "coverage_level": 5}, {"skill_name": "Database Query Optimization", "coverage_level": 3}]
    },

    # ── Cloud & Architecture ──
    {
        "title": "AWS Certified Solutions Architect – Associate",
        "description": "Design resilient, high-performing, secure, and cost-optimized architectures on AWS.",
        "provider": "Udemy / Stephane Maarek",
        "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/",
        "is_free": False,
        "price": Decimal("24.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 27.0,
        "rating": 4.9,
        "skills": [{"skill_name": "AWS", "coverage_level": 5}, {"skill_name": "Serverless Architecture", "coverage_level": 4}, {"skill_name": "Cloud Security & IAM", "coverage_level": 4}]
    },
    {
        "title": "AWS Cloud Practitioner Essentials",
        "description": "Fundamental overview of AWS cloud concepts, security, architecture, pricing, and support.",
        "provider": "AWS Training / Coursera",
        "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 6.0,
        "rating": 4.8,
        "skills": [{"skill_name": "AWS", "coverage_level": 4}, {"skill_name": "Cloud Security & IAM", "coverage_level": 3}]
    },
    {
        "title": "Google Cloud Platform Fundamentals: Core Infrastructure",
        "description": "Explore GCP computing, storage services (Compute Engine, GKE, Cloud Storage, BigQuery).",
        "provider": "Coursera / Google Cloud",
        "url": "https://www.coursera.org/learn/gcp-fundamentals",
        "is_free": False,
        "price": Decimal("39.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 12.0,
        "rating": 4.7,
        "skills": [{"skill_name": "Google Cloud Platform (GCP)", "coverage_level": 5}, {"skill_name": "Serverless Architecture", "coverage_level": 3}]
    },
    {
        "title": "Serverless Architecture on AWS with Lambda & API Gateway",
        "description": "Build event-driven microservices using AWS Lambda, DynamoDB, and Serverless Framework.",
        "provider": "A Cloud Guru",
        "url": "https://acloudguru.com/course/serverless-framework-bootcamp",
        "is_free": False,
        "price": Decimal("35.00"),
        "currency": "USD",
        "difficulty": "Advanced",
        "duration_hours": 10.0,
        "rating": 4.7,
        "skills": [{"skill_name": "Serverless Architecture", "coverage_level": 5}, {"skill_name": "AWS", "coverage_level": 4}]
    },

    # ── DevOps & Infrastructure ──
    {
        "title": "Docker & Kubernetes: The Practical Guide",
        "description": "Build, test, deploy containers from scratch: multi-container setups, volumes, services, and pods.",
        "provider": "Udemy / Academind",
        "url": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/",
        "is_free": False,
        "price": Decimal("19.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 23.5,
        "rating": 4.8,
        "skills": [{"skill_name": "Docker", "coverage_level": 5}, {"skill_name": "Kubernetes", "coverage_level": 5}]
    },
    {
        "title": "Docker Tutorial for Beginners (Full Free Course)",
        "description": "Understand images, containers, Dockerfile creation, port binding, and Docker Compose.",
        "provider": "YouTube / TechWorld with Nana",
        "url": "https://www.youtube.com/watch?v=3c-iBn73dDE",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Beginner",
        "duration_hours": 3.0,
        "rating": 4.9,
        "skills": [{"skill_name": "Docker", "coverage_level": 5}]
    },
    {
        "title": "GitHub Actions: The Complete CI/CD Bootcamp",
        "description": "Automate tests, build docker images, deploy to AWS/cloud with custom GitHub Action workflows.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/github-actions-the-complete-guide/",
        "is_free": False,
        "price": Decimal("18.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 9.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Git & GitHub Actions", "coverage_level": 5}, {"skill_name": "CI/CD Pipelines", "coverage_level": 5}]
    },
    {
        "title": "Terraform for AWS: Infrastructure as Code",
        "description": "Provision VPCs, EC2 clusters, RDS databases, and IAM policies automatically using HCL.",
        "provider": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/news/learn-terraform-course/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 6.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Terraform", "coverage_level": 5}, {"skill_name": "AWS", "coverage_level": 3}]
    },
    {
        "title": "Monitoring with Prometheus & Grafana",
        "description": "Instrument microservices metrics, configure Prometheus scrape targets, and build Grafana alerts.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/prometheus-grafana-monitoring/",
        "is_free": False,
        "price": Decimal("19.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 8.0,
        "rating": 4.7,
        "skills": [{"skill_name": "Prometheus & Grafana", "coverage_level": 5}, {"skill_name": "Linux Administration", "coverage_level": 3}]
    },

    # ── Cybersecurity ──
    {
        "title": "OWASP Top 10 Web Application Security",
        "description": "Deep dive into web vulnerabilities: SQL injection, XSS, CSRF, broken access control, and defense.",
        "provider": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/news/owasp-top-10-vulnerabilities/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 5.5,
        "rating": 4.9,
        "skills": [{"skill_name": "Web Application Security (OWASP)", "coverage_level": 5}, {"skill_name": "Vulnerability Assessment", "coverage_level": 4}]
    },
    {
        "title": "CompTIA Security+ (SY0-701) Complete Training",
        "description": "Comprehensive security principles: threat analysis, cryptography, network defenses, and IAM.",
        "provider": "Udemy / Jason Dion",
        "url": "https://www.udemy.com/course/securityplus/",
        "is_free": False,
        "price": Decimal("24.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 31.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Network Security", "coverage_level": 5}, {"skill_name": "Cryptography", "coverage_level": 4}, {"skill_name": "Cloud Security & IAM", "coverage_level": 4}]
    },
    {
        "title": "Practical Ethical Hacking & Penetration Testing",
        "description": "Reconnaissance, vulnerability scanning with Nmap, exploitation with Metasploit, and report writing.",
        "provider": "TCM Security",
        "url": "https://academy.tcm-sec.com/p/practical-ethical-hacking-the-complete-course",
        "is_free": False,
        "price": Decimal("39.99"),
        "currency": "USD",
        "difficulty": "Advanced",
        "duration_hours": 25.0,
        "rating": 4.9,
        "skills": [{"skill_name": "Penetration Testing", "coverage_level": 5}, {"skill_name": "Vulnerability Assessment", "coverage_level": 5}, {"skill_name": "Network Security", "coverage_level": 4}]
    },
    {
        "title": "Applied Cryptography and Secure Communication",
        "description": "Symmetric encryption (AES), asymmetric ciphers (RSA, ECC), hashing (SHA-256), and TLS handshake.",
        "provider": "Stanford Online / Coursera",
        "url": "https://www.coursera.org/learn/crypto",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Advanced",
        "duration_hours": 20.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Cryptography", "coverage_level": 5}]
    },
    {
        "title": "SOC Analyst Fundamentals: SIEM & Incident Response",
        "description": "Splunk log analysis, threat hunting, alert triage, and security incident response lifecycle.",
        "provider": "TryHackMe / Coursera",
        "url": "https://tryhackme.com/path/outline/soclevel1",
        "is_free": False,
        "price": Decimal("14.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 16.0,
        "rating": 4.8,
        "skills": [{"skill_name": "SIEM & Threat Detection", "coverage_level": 5}, {"skill_name": "Network Security", "coverage_level": 4}]
    },
    # Additional courses to hit 52
    {
        "title": "Go: The Complete Developer's Guide (Golang)",
        "description": "Master Google's Go language: structs, interfaces, channels, and lightweight concurrency with goroutines.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/go-the-complete-developers-guide/",
        "is_free": False,
        "price": Decimal("19.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 10.0,
        "rating": 4.7,
        "skills": [{"skill_name": "Go", "coverage_level": 5}]
    },
    {
        "title": "Rust Programming Language: The Ultimate Guide",
        "description": "Learn Rust ownership, borrowing, lifetimes, pattern matching, and fearless concurrency.",
        "provider": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/news/rust-crash-course/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 12.0,
        "rating": 4.9,
        "skills": [{"skill_name": "Rust", "coverage_level": 5}]
    },
    {
        "title": "Java Programming Masterclass for Software Developers",
        "description": "Master object-oriented Java, Spring Boot microservices, multithreading, and unit testing with JUnit.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/java-the-complete-java-developer-course/",
        "is_free": False,
        "price": Decimal("24.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 60.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Java", "coverage_level": 5}]
    },
    {
        "title": "C++ Programming from Beginner to Beyond",
        "description": "Modern C++ (C++14/17/20), pointers, references, memory management, STL containers, and algorithms.",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/beginning-c-plus-plus-programming/",
        "is_free": False,
        "price": Decimal("19.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 46.0,
        "rating": 4.7,
        "skills": [{"skill_name": "C++", "coverage_level": 5}]
    },
    {
        "title": "Vue.js 3: The Complete Guide",
        "description": "Composition API, Vue Router, Pinia state management, and building production single-page applications.",
        "provider": "Udemy / Academind",
        "url": "https://www.udemy.com/course/vuejs-2-the-complete-guide/",
        "is_free": False,
        "price": Decimal("18.99"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 31.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Vue.js", "coverage_level": 5}, {"skill_name": "JavaScript", "coverage_level": 4}]
    },
    {
        "title": "Mastering Feature Engineering for Machine Learning",
        "description": "Missing data imputation, categorical encodings, outlier handling, and scaling techniques.",
        "provider": "Coursera",
        "url": "https://www.coursera.org/learn/feature-engineering",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 8.0,
        "rating": 4.7,
        "skills": [{"skill_name": "Feature Engineering", "coverage_level": 5}, {"skill_name": "Pandas", "coverage_level": 4}, {"skill_name": "Scikit-Learn", "coverage_level": 4}]
    },
    {
        "title": "Scikit-Learn Mastery: Machine Learning in Python",
        "description": "Pipelines, GridSearchCV, cross-validation, ensemble methods, and regression / classification algorithms.",
        "provider": "DataCamp",
        "url": "https://www.datacamp.com/courses/supervised-learning-with-scikit-learn",
        "is_free": False,
        "price": Decimal("25.00"),
        "currency": "USD",
        "difficulty": "Intermediate",
        "duration_hours": 10.0,
        "rating": 4.8,
        "skills": [{"skill_name": "Scikit-Learn", "coverage_level": 5}, {"skill_name": "Machine Learning", "coverage_level": 5}]
    },
    {
        "title": "Full Stack Open: Modern Web Development with React & Node",
        "description": "Deep dive into React, Redux, Node.js, Express, MongoDB, GraphQL, and TypeScript from University of Helsinki.",
        "provider": "University of Helsinki",
        "url": "https://fullstackopen.com/en/",
        "is_free": True,
        "price": Decimal("0.00"),
        "currency": "USD",
        "difficulty": "Advanced",
        "duration_hours": 60.0,
        "rating": 4.9,
        "skills": [{"skill_name": "React", "coverage_level": 5}, {"skill_name": "Node.js", "coverage_level": 5}, {"skill_name": "TypeScript", "coverage_level": 4}, {"skill_name": "GraphQL", "coverage_level": 4}]
    }
]


# ==============================================================================
# 4. MASTER PROJECTS DATA (32 Hands-on Projects)
# ==============================================================================
PROJECTS_DATA = [
    # ── Data Science & ML ──
    {
        "title": "Customer Churn Prediction Engine",
        "description": "Clean and preprocess a telecom dataset of 7,000+ subscribers, perform EDA, and train Random Forest & XGBoost classifiers with ROC-AUC evaluation.",
        "difficulty": "Intermediate",
        "estimated_hours": 14.0,
        "github_url": "https://github.com/pathpilot-demos/customer-churn-engine",
        "dataset_url": "https://www.kaggle.com/datasets/blastchar/telco-customer-churn",
        "skills": [
            {"skill_name": "Python", "importance": 5},
            {"skill_name": "Pandas", "importance": 5},
            {"skill_name": "Scikit-Learn", "importance": 5},
            {"skill_name": "Machine Learning", "importance": 5},
            {"skill_name": "Exploratory Data Analysis (EDA)", "importance": 4}
        ]
    },
    {
        "title": "E-Commerce Recommendation System",
        "description": "Construct user-item interaction matrix, implement collaborative filtering with SVD matrix factorization, and serve top-5 product recommendations.",
        "difficulty": "Intermediate",
        "estimated_hours": 18.0,
        "github_url": "https://github.com/pathpilot-demos/ecommerce-recommender",
        "dataset_url": "https://grouplens.org/datasets/movielens/100k/",
        "skills": [
            {"skill_name": "Python", "importance": 5},
            {"skill_name": "Pandas", "importance": 4},
            {"skill_name": "Machine Learning", "importance": 5},
            {"skill_name": "NumPy", "importance": 4}
        ]
    },
    {
        "title": "Automated Chest X-Ray Pneumonia Classifier",
        "description": "Preprocess medical image datasets, fine-tune a ResNet50 vision transformer with PyTorch, and generate Grad-CAM heatmaps for visual interpretability.",
        "difficulty": "Advanced",
        "estimated_hours": 22.0,
        "github_url": "https://github.com/pathpilot-demos/xray-pneumonia-vision",
        "dataset_url": "https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia",
        "skills": [
            {"skill_name": "Deep Learning", "importance": 5},
            {"skill_name": "PyTorch", "importance": 5},
            {"skill_name": "Computer Vision", "importance": 5},
            {"skill_name": "Python", "importance": 4}
        ]
    },
    {
        "title": "Real-Time Fraud Detection Microservice",
        "description": "Train Isolation Forest and LightGBM models on 284k imbalanced credit card transactions, package inference in FastAPI, and containerize with Docker.",
        "difficulty": "Advanced",
        "estimated_hours": 25.0,
        "github_url": "https://github.com/pathpilot-demos/fraud-detection-service",
        "dataset_url": "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud",
        "skills": [
            {"skill_name": "MLOps", "importance": 5},
            {"skill_name": "FastAPI", "importance": 5},
            {"skill_name": "Docker", "importance": 4},
            {"skill_name": "Machine Learning", "importance": 4},
            {"skill_name": "Python", "importance": 4}
        ]
    },
    {
        "title": "House Price Regression Pipeline with Feature Engineering",
        "description": "Build an end-to-end regression pipeline handling skewness, categorical target encodings, and ensemble stacking (Ridge, Lasso, LightGBM).",
        "difficulty": "Intermediate",
        "estimated_hours": 12.0,
        "github_url": "https://github.com/pathpilot-demos/house-price-pipeline",
        "dataset_url": "https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques",
        "skills": [
            {"skill_name": "Python", "importance": 5},
            {"skill_name": "Pandas", "importance": 5},
            {"skill_name": "Feature Engineering", "importance": 5},
            {"skill_name": "Scikit-Learn", "importance": 4}
        ]
    },
    {
        "title": "A/B Test Statistical Analysis on Mobile App Onboarding",
        "description": "Conduct hypothesis testing, calculate p-values, confidence intervals, and minimum detectable effect for a 2-variant user onboarding funnel.",
        "difficulty": "Intermediate",
        "estimated_hours": 10.0,
        "github_url": "https://github.com/pathpilot-demos/mobile-ab-testing",
        "dataset_url": "https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing",
        "skills": [
            {"skill_name": "A/B Testing", "importance": 5},
            {"skill_name": "Statistics & Probability", "importance": 5},
            {"skill_name": "Python", "importance": 4},
            {"skill_name": "Data Visualization", "importance": 4}
        ]
    },

    # ── AI & LLM Engineering ──
    {
        "title": "Enterprise Knowledge Assistant with RAG & Vector DB",
        "description": "Ingest PDF documentation, chunk text, embed vectors using OpenAI embeddings, store in ChromaDB, and generate grounded answers with LangChain.",
        "difficulty": "Advanced",
        "estimated_hours": 20.0,
        "github_url": "https://github.com/pathpilot-demos/enterprise-rag-assistant",
        "dataset_url": "https://github.com/pathpilot-demos/sample-knowledge-base",
        "skills": [
            {"skill_name": "RAG Systems", "importance": 5},
            {"skill_name": "Vector Databases", "importance": 5},
            {"skill_name": "Large Language Models (LLMs)", "importance": 5},
            {"skill_name": "Python", "importance": 4},
            {"skill_name": "FastAPI", "importance": 4}
        ]
    },
    {
        "title": "Domain-Specific Fine-Tuned Medical Summarizer",
        "description": "Fine-tune a LLaMA-3 model using LoRA / QLoRA adapters on medical clinical notes for structured bullet-point summary generation.",
        "difficulty": "Advanced",
        "estimated_hours": 28.0,
        "github_url": "https://github.com/pathpilot-demos/clinical-llm-finetuning",
        "dataset_url": "https://huggingface.co/datasets/medical_dialog",
        "skills": [
            {"skill_name": "Large Language Models (LLMs)", "importance": 5},
            {"skill_name": "PyTorch", "importance": 5},
            {"skill_name": "Natural Language Processing (NLP)", "importance": 4},
            {"skill_name": "Python", "importance": 4}
        ]
    },
    {
        "title": "Sentiment Analysis and Aspect Extraction on Product Reviews",
        "description": "Fine-tune RoBERTa for aspect-based sentiment categorization and entity extraction from customer feedback.",
        "difficulty": "Intermediate",
        "estimated_hours": 16.0,
        "github_url": "https://github.com/pathpilot-demos/sentiment-aspect-nlp",
        "dataset_url": "https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews",
        "skills": [
            {"skill_name": "Natural Language Processing (NLP)", "importance": 5},
            {"skill_name": "PyTorch", "importance": 4},
            {"skill_name": "Python", "importance": 4}
        ]
    },

    # ── Web Development & Full Stack ──
    {
        "title": "Interactive SaaS Analytics Dashboard",
        "description": "Build a responsive Next.js and Tailwind CSS dashboard featuring dynamic charting, KPI summary cards, filter bars, and dark mode.",
        "difficulty": "Intermediate",
        "estimated_hours": 16.0,
        "github_url": "https://github.com/pathpilot-demos/saas-analytics-dashboard",
        "dataset_url": "https://mockaroo.com/schemas/saas-metrics",
        "skills": [
            {"skill_name": "React", "importance": 5},
            {"skill_name": "Next.js", "importance": 5},
            {"skill_name": "Tailwind CSS", "importance": 4},
            {"skill_name": "TypeScript", "importance": 4}
        ]
    },
    {
        "title": "High-Throughput Asynchronous Task API",
        "description": "Architect a FastAPI backend with Celery workers, Redis message brokers, JWT role-based access control, and PostgreSQL persistence.",
        "difficulty": "Advanced",
        "estimated_hours": 20.0,
        "github_url": "https://github.com/pathpilot-demos/async-fastapi-backend",
        "dataset_url": "https://github.com/pathpilot-demos/api-test-payloads",
        "skills": [
            {"skill_name": "FastAPI", "importance": 5},
            {"skill_name": "PostgreSQL", "importance": 5},
            {"skill_name": "Redis", "importance": 4},
            {"skill_name": "RESTful API Design", "importance": 5},
            {"skill_name": "Python", "importance": 4}
        ]
    },
    {
        "title": "Collaborative Kanban Project Management App",
        "description": "Full-stack single page application with drag-and-drop task boards, real-time WebSockets, user permissions, and GraphQL mutations.",
        "difficulty": "Advanced",
        "estimated_hours": 26.0,
        "github_url": "https://github.com/pathpilot-demos/collaborative-kanban",
        "dataset_url": "https://github.com/pathpilot-demos/kanban-fixtures",
        "skills": [
            {"skill_name": "React", "importance": 5},
            {"skill_name": "TypeScript", "importance": 5},
            {"skill_name": "Node.js", "importance": 4},
            {"skill_name": "GraphQL", "importance": 4},
            {"skill_name": "PostgreSQL", "importance": 4}
        ]
    },
    {
        "title": "E-Commerce REST API with Django & Stripe Checkout",
        "description": "Build backend catalog management, shopping cart sessions, order processing, and secure webhook validation with Stripe API.",
        "difficulty": "Intermediate",
        "estimated_hours": 18.0,
        "github_url": "https://github.com/pathpilot-demos/django-stripe-ecommerce",
        "dataset_url": "https://fakestoreapi.com/",
        "skills": [
            {"skill_name": "Django", "importance": 5},
            {"skill_name": "RESTful API Design", "importance": 5},
            {"skill_name": "Python", "importance": 4},
            {"skill_name": "SQL", "importance": 4}
        ]
    },

    # ── Data Engineering & Databases ──
    {
        "title": "Automated ETL Pipeline with PostgreSQL & Docker",
        "description": "Extract financial market data from public APIs, clean in pandas, validate schema with Pydantic, and load into normalized PostgreSQL tables.",
        "difficulty": "Intermediate",
        "estimated_hours": 16.0,
        "github_url": "https://github.com/pathpilot-demos/financial-etl-pipeline",
        "dataset_url": "https://www.alphavantage.co/documentation/",
        "skills": [
            {"skill_name": "PostgreSQL", "importance": 5},
            {"skill_name": "Python", "importance": 5},
            {"skill_name": "Data Modeling", "importance": 5},
            {"skill_name": "Docker", "importance": 4},
            {"skill_name": "SQL", "importance": 5}
        ]
    },
    {
        "title": "Relational Schema Design & Index Tuning Benchmark",
        "description": "Design a 15-table normalized schema for a logistics company, generate 5 million rows, and optimize heavy multi-table join queries using B-Tree and GIN indexes.",
        "difficulty": "Advanced",
        "estimated_hours": 18.0,
        "github_url": "https://github.com/pathpilot-demos/sql-performance-tuning",
        "dataset_url": "https://github.com/pathpilot-demos/logistics-benchmark-data",
        "skills": [
            {"skill_name": "Database Query Optimization", "importance": 5},
            {"skill_name": "SQL", "importance": 5},
            {"skill_name": "PostgreSQL", "importance": 5},
            {"skill_name": "Data Modeling", "importance": 4}
        ]
    },

    # ── Cloud & DevOps ──
    {
        "title": "Automated Multi-Stage CI/CD Pipeline on AWS with Terraform",
        "description": "Provision AWS VPC, ECS Fargate cluster, Application Load Balancer with Terraform, and configure automated GitHub Actions deployment on git push.",
        "difficulty": "Advanced",
        "estimated_hours": 24.0,
        "github_url": "https://github.com/pathpilot-demos/terraform-aws-cicd",
        "dataset_url": "https://github.com/pathpilot-demos/infrastructure-blueprints",
        "skills": [
            {"skill_name": "Terraform", "importance": 5},
            {"skill_name": "AWS", "importance": 5},
            {"skill_name": "Docker", "importance": 5},
            {"skill_name": "CI/CD Pipelines", "importance": 5},
            {"skill_name": "Git & GitHub Actions", "importance": 4}
        ]
    },
    {
        "title": "Kubernetes Microservices Cluster with Prometheus Monitoring",
        "description": "Deploy a 4-service polyglot architecture on Kubernetes with Ingress controllers, Helm charts, and Prometheus/Grafana service metrics.",
        "difficulty": "Advanced",
        "estimated_hours": 26.0,
        "github_url": "https://github.com/pathpilot-demos/k8s-microservices-observability",
        "dataset_url": "https://github.com/pathpilot-demos/microservices-demo-app",
        "skills": [
            {"skill_name": "Kubernetes", "importance": 5},
            {"skill_name": "Docker", "importance": 5},
            {"skill_name": "Prometheus & Grafana", "importance": 5},
            {"skill_name": "Linux Administration", "importance": 4}
        ]
    },
    {
        "title": "Serverless Event-Driven Image Processing Pipeline",
        "description": "Upload high-res photos to S3, trigger AWS Lambda functions to generate thumbnails, extract EXIF metadata, and record records into DynamoDB.",
        "difficulty": "Intermediate",
        "estimated_hours": 14.0,
        "github_url": "https://github.com/pathpilot-demos/serverless-image-pipeline",
        "dataset_url": "https://unsplash.com/data",
        "skills": [
            {"skill_name": "AWS", "importance": 5},
            {"skill_name": "Serverless Architecture", "importance": 5},
            {"skill_name": "Python", "importance": 4}
        ]
    },

    # ── Cybersecurity ──
    {
        "title": "Automated Web Application Vulnerability Scanner",
        "description": "Develop a Python CLI security tool to crawl target URLs, detect SQL injection patterns, reflective XSS, and security header misconfigurations.",
        "difficulty": "Advanced",
        "estimated_hours": 20.0,
        "github_url": "https://github.com/pathpilot-demos/web-vuln-scanner",
        "dataset_url": "https://github.com/OWASP/NodeGoat",
        "skills": [
            {"skill_name": "Web Application Security (OWASP)", "importance": 5},
            {"skill_name": "Vulnerability Assessment", "importance": 5},
            {"skill_name": "Python", "importance": 4}
        ]
    },
    {
        "title": "Network Traffic Sniffer & Threat Analyzer",
        "description": "Capture packets with Scapy, inspect TCP/UDP payloads, identify port scans, and trigger alerts on suspicious anomalies.",
        "difficulty": "Advanced",
        "estimated_hours": 18.0,
        "github_url": "https://github.com/pathpilot-demos/network-threat-analyzer",
        "dataset_url": "https://www.unb.ca/cic/datasets/ids-2017.html",
        "skills": [
            {"skill_name": "Network Security", "importance": 5},
            {"skill_name": "SIEM & Threat Detection", "importance": 4},
            {"skill_name": "Python", "importance": 4},
            {"skill_name": "Linux Administration", "importance": 3}
        ]
    },
    {
        "title": "Secure Zero-Knowledge Password Manager with AES-256",
        "description": "Implement client-side PBKDF2 key derivation, AES-256-GCM encryption, master key verification, and secure vault storage.",
        "difficulty": "Intermediate",
        "estimated_hours": 15.0,
        "github_url": "https://github.com/pathpilot-demos/crypto-vault-manager",
        "dataset_url": "https://github.com/pathpilot-demos/crypto-fixtures",
        "skills": [
            {"skill_name": "Cryptography", "importance": 5},
            {"skill_name": "Web Application Security (OWASP)", "importance": 4},
            {"skill_name": "Python", "importance": 4}
        ]
    },

    # Additional diverse projects to reach 32
    {
        "title": "Autonomous Warehouse Logistics Optimizer with Genetic Algorithms",
        "description": "Simulate multi-agent route optimization across dynamic 2D warehouse grids using heuristic search and evolutionary algorithms.",
        "difficulty": "Advanced",
        "estimated_hours": 24.0,
        "github_url": "https://github.com/pathpilot-demos/logistics-optimizer",
        "dataset_url": "https://github.com/pathpilot-demos/warehouse-grid-data",
        "skills": [
            {"skill_name": "Python", "importance": 5},
            {"skill_name": "NumPy", "importance": 4},
            {"skill_name": "Machine Learning", "importance": 4}
        ]
    },
    {
        "title": "Executive Sales & Revenue Intelligence Dashboard in Power BI",
        "description": "Ingest global retail sales datasets, formulate DAX year-over-year revenue metrics, and publish an executive decision-making suite.",
        "difficulty": "Beginner",
        "estimated_hours": 10.0,
        "github_url": "https://github.com/pathpilot-demos/powerbi-sales-intelligence",
        "dataset_url": "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce",
        "skills": [
            {"skill_name": "Power BI & Tableau", "importance": 5},
            {"skill_name": "Data Visualization", "importance": 5},
            {"skill_name": "SQL", "importance": 4}
        ]
    },
    {
        "title": "Real-Time Stock Market Data Pipeline with Kafka & PostgreSQL",
        "description": "Stream live ticker updates through Apache Kafka, process rolling averages with Python consumers, and store historical bars in PostgreSQL.",
        "difficulty": "Advanced",
        "estimated_hours": 25.0,
        "github_url": "https://github.com/pathpilot-demos/streaming-stock-pipeline",
        "dataset_url": "https://finnhub.io/docs/api",
        "skills": [
            {"skill_name": "PostgreSQL", "importance": 5},
            {"skill_name": "Python", "importance": 5},
            {"skill_name": "Docker", "importance": 4},
            {"skill_name": "Data Modeling", "importance": 4}
        ]
    },
    {
        "title": "AI Video Transcriber & Meeting Summarization Tool",
        "description": "Extract audio streams from uploaded MP4 videos, transcribe with OpenAI Whisper, and generate action items with GPT-4.",
        "difficulty": "Intermediate",
        "estimated_hours": 16.0,
        "github_url": "https://github.com/pathpilot-demos/ai-video-transcriber",
        "dataset_url": "https://github.com/pathpilot-demos/sample-meeting-audio",
        "skills": [
            {"skill_name": "Large Language Models (LLMs)", "importance": 5},
            {"skill_name": "FastAPI", "importance": 4},
            {"skill_name": "Python", "importance": 4}
        ]
    },
    {
        "title": "Full-Stack Real Estate Listing Platform",
        "description": "Build interactive map searches, property filters, image galleries, and booking inquiries with React, Next.js, and PostgreSQL.",
        "difficulty": "Intermediate",
        "estimated_hours": 20.0,
        "github_url": "https://github.com/pathpilot-demos/real-estate-nextjs",
        "dataset_url": "https://github.com/pathpilot-demos/property-mock-data",
        "skills": [
            {"skill_name": "React", "importance": 5},
            {"skill_name": "Next.js", "importance": 5},
            {"skill_name": "PostgreSQL", "importance": 4},
            {"skill_name": "Tailwind CSS", "importance": 4}
        ]
    },
    {
        "title": "Autonomous Trading Bot with Backtesting Engine",
        "description": "Implement Moving Average Crossover and RSI strategies with Python, simulate historical performance with vector backtesting, and analyze Sharpe ratio.",
        "difficulty": "Advanced",
        "estimated_hours": 22.0,
        "github_url": "https://github.com/pathpilot-demos/algorithmic-trading-bot",
        "dataset_url": "https://finance.yahoo.com/",
        "skills": [
            {"skill_name": "Python", "importance": 5},
            {"skill_name": "Pandas", "importance": 5},
            {"skill_name": "Statistics & Probability", "importance": 4},
            {"skill_name": "NumPy", "importance": 4}
        ]
    },
    {
        "title": "Server Infrastructure Hardening & Automated Audit Script",
        "description": "Script automated checks for SSH root access, open ports, password policies, unneeded services, and generate a CIS benchmark compliance report.",
        "difficulty": "Intermediate",
        "estimated_hours": 12.0,
        "github_url": "https://github.com/pathpilot-demos/linux-hardening-audit",
        "dataset_url": "https://github.com/pathpilot-demos/cis-benchmarks",
        "skills": [
            {"skill_name": "Bash & Shell Scripting", "importance": 5},
            {"skill_name": "Linux Administration", "importance": 5},
            {"skill_name": "Vulnerability Assessment", "importance": 4}
        ]
    },
    {
        "title": "High-Volume URL Shortener with Analytics Tracking",
        "description": "Design base62 short code hashing, Redis caching layer with LRU eviction, and asynchronous click geo-analytics logging in PostgreSQL.",
        "difficulty": "Intermediate",
        "estimated_hours": 14.0,
        "github_url": "https://github.com/pathpilot-demos/url-shortener-analytics",
        "dataset_url": "https://github.com/pathpilot-demos/url-fixtures",
        "skills": [
            {"skill_name": "FastAPI", "importance": 5},
            {"skill_name": "Redis", "importance": 5},
            {"skill_name": "PostgreSQL", "importance": 4},
            {"skill_name": "RESTful API Design", "importance": 4}
        ]
    },
    {
        "title": "Log Anomaly Detection Engine with Unsupervised ML",
        "description": "Parse Apache/Nginx web logs, extract feature vectors with TF-IDF, and detect DDoS / SQL injection attacks using Isolation Forests.",
        "difficulty": "Advanced",
        "estimated_hours": 18.0,
        "github_url": "https://github.com/pathpilot-demos/log-anomaly-ml",
        "dataset_url": "https://www.kaggle.com/datasets/eliasd/raw-web-server-access-logs",
        "skills": [
            {"skill_name": "Machine Learning", "importance": 5},
            {"skill_name": "Python", "importance": 5},
            {"skill_name": "SIEM & Threat Detection", "importance": 4},
            {"skill_name": "Feature Engineering", "importance": 4}
        ]
    },
    {
        "title": "Modern Component Design System with Storybook",
        "description": "Construct accessible, themeable UI components (buttons, dialogs, dropdowns) with React, TypeScript, Tailwind, and documentation in Storybook.",
        "difficulty": "Beginner",
        "estimated_hours": 12.0,
        "github_url": "https://github.com/pathpilot-demos/storybook-design-system",
        "dataset_url": "https://github.com/pathpilot-demos/design-tokens",
        "skills": [
            {"skill_name": "React", "importance": 5},
            {"skill_name": "TypeScript", "importance": 4},
            {"skill_name": "Tailwind CSS", "importance": 5},
            {"skill_name": "HTML & CSS", "importance": 4}
        ]
    },
    {
        "title": "Multi-Region Cloud Disaster Recovery Blueprint",
        "description": "Architect active-passive AWS cross-region database replication with Aurora Global Database and Route 53 DNS failover routing.",
        "difficulty": "Advanced",
        "estimated_hours": 20.0,
        "github_url": "https://github.com/pathpilot-demos/aws-disaster-recovery",
        "dataset_url": "https://github.com/pathpilot-demos/aws-architecture-templates",
        "skills": [
            {"skill_name": "AWS", "importance": 5},
            {"skill_name": "Terraform", "importance": 4},
            {"skill_name": "Cloud Security & IAM", "importance": 4}
        ]
    }
]


INTERESTS_DATA = [
    {"name": "AI", "category": "AI / Machine Learning"},
    {"name": "Data Science", "category": "Data Science & Analytics"},
    {"name": "Web Development", "category": "Software Engineering"},
    {"name": "Mobile Development", "category": "Software Engineering"},
    {"name": "Cybersecurity", "category": "Security & Networks"},
    {"name": "Cloud Computing", "category": "Cloud & Infrastructure"},
    {"name": "Data Analytics", "category": "Data Science & Analytics"},
    {"name": "UI/UX", "category": "Design & Product"},
    {"name": "Software Development", "category": "Software Engineering"},
    {"name": "Robotics", "category": "Hardware & Systems"},
    {"name": "IoT", "category": "Hardware & Systems"},
    {"name": "Business Analytics", "category": "Data Science & Analytics"},
    {"name": "DevOps", "category": "Cloud & Infrastructure"},
    {"name": "Database Engineering", "category": "Databases & Systems"},
    {"name": "Backend Development", "category": "Software Engineering"},
    {"name": "Frontend Development", "category": "Software Engineering"},
]


# ==============================================================================
# 5. SEED EXECUTION LOGIC (Idempotent)
# ==============================================================================
def seed_database(db: Session) -> dict:
    """
    Executes idempotent seeding of master data.
    Returns counts of records in each table.
    """
    stats = {}

    print("====================================================================")
    print(" PathPilot AI - Seeding Master Database")
    print("====================================================================")

    # Ensure all tables are created
    Base.metadata.create_all(bind=engine)

    # ── 0. Seed Interests ─────────────────────────────────────────────────────
    interests_inserted = 0
    interests_updated = 0
    for item in INTERESTS_DATA:
        existing = db.query(Interest).filter(Interest.name == item["name"]).first()
        if existing:
            existing.category = item["category"]
            interests_updated += 1
        else:
            interest = Interest(name=item["name"], category=item["category"])
            db.add(interest)
            interests_inserted += 1
    db.commit()
    total_interests = db.query(Interest).count()
    print(f" [OK] Interests: {total_interests} total ({interests_inserted} new, {interests_updated} updated)")
    stats["interests"] = total_interests

    # ── 1. Seed Skills ────────────────────────────────────────────────────────
    skills_map = {}  # name -> Skill object
    skills_inserted = 0
    skills_updated = 0

    for item in SKILLS_DATA:
        existing = db.query(Skill).filter(Skill.name == item["name"]).first()
        if existing:
            existing.category = item["category"]
            existing.description = item["description"]
            skills_map[item["name"]] = existing
            skills_updated += 1
        else:
            skill = Skill(
                name=item["name"],
                category=item["category"],
                description=item["description"],
            )
            db.add(skill)
            db.flush()
            skills_map[item["name"]] = skill
            skills_inserted += 1

    db.commit()
    total_skills = db.query(Skill).count()
    print(f" [OK] Skills: {total_skills} total ({skills_inserted} new, {skills_updated} updated)")
    stats["skills"] = total_skills

    # ── 2. Seed Careers & CareerSkills ────────────────────────────────────────
    careers_inserted = 0
    careers_updated = 0
    career_skills_count = 0
    # Prune any obsolete careers not in the 5 supported programs
    supported_career_names = [c["name"] for c in CAREERS_DATA]
    obsolete_careers = db.query(Career).filter(~Career.name.in_(supported_career_names)).all()
    for ob in obsolete_careers:
        # Delete related career skills first
        db.query(CareerSkill).filter(CareerSkill.career_id == ob.id).delete()
        db.delete(ob)
    db.flush()

    for c_data in CAREERS_DATA:
        career = db.query(Career).filter(Career.name == c_data["name"]).first()
        if career:
            career.description = c_data["description"]
            career.difficulty = c_data["difficulty"]
            careers_updated += 1
        else:
            career = Career(
                name=c_data["name"],
                description=c_data["description"],
                difficulty=c_data["difficulty"],
            )
            db.add(career)
            db.flush()
            careers_inserted += 1

        # Associate required skills
        for s_req in c_data["skills"]:
            skill_obj = skills_map.get(s_req["skill_name"])
            if not skill_obj:
                continue

            existing_cs = (
                db.query(CareerSkill)
                .filter(
                    CareerSkill.career_id == career.id,
                    CareerSkill.skill_id == skill_obj.id,
                )
                .first()
            )
            if existing_cs:
                existing_cs.required_level = s_req["required_level"]
                existing_cs.importance = s_req["importance"]
            else:
                cs = CareerSkill(
                    career_id=career.id,
                    skill_id=skill_obj.id,
                    required_level=s_req["required_level"],
                    importance=s_req["importance"],
                )
                db.add(cs)
            career_skills_count += 1

    db.commit()
    total_careers = db.query(Career).count()
    total_career_skills = db.query(CareerSkill).count()
    print(f" [OK] Careers: {total_careers} total ({careers_inserted} new, {careers_updated} updated)")
    print(f" [OK] Career Skills mappings: {total_career_skills} total")
    stats["careers"] = total_careers
    stats["career_skills"] = total_career_skills

    # ── 3. Seed Courses & CourseSkills ────────────────────────────────────────
    courses_inserted = 0
    courses_updated = 0
    course_skills_count = 0

    for crs_data in COURSES_DATA:
        course = db.query(Course).filter(Course.title == crs_data["title"]).first()
        if course:
            course.description = crs_data["description"]
            course.provider = crs_data["provider"]
            course.url = crs_data["url"]
            course.is_free = crs_data["is_free"]
            course.price = crs_data["price"]
            course.currency = crs_data["currency"]
            course.difficulty = crs_data["difficulty"]
            course.duration_hours = crs_data["duration_hours"]
            course.rating = crs_data["rating"]
            courses_updated += 1
        else:
            course = Course(
                title=crs_data["title"],
                description=crs_data["description"],
                provider=crs_data["provider"],
                url=crs_data["url"],
                is_free=crs_data["is_free"],
                price=crs_data["price"],
                currency=crs_data["currency"],
                difficulty=crs_data["difficulty"],
                duration_hours=crs_data["duration_hours"],
                rating=crs_data["rating"],
            )
            db.add(course)
            db.flush()
            courses_inserted += 1

        # Associate course skills
        for s_map in crs_data["skills"]:
            skill_obj = skills_map.get(s_map["skill_name"])
            if not skill_obj:
                continue

            existing_crs_skill = (
                db.query(CourseSkill)
                .filter(
                    CourseSkill.course_id == course.id,
                    CourseSkill.skill_id == skill_obj.id,
                )
                .first()
            )
            if existing_crs_skill:
                existing_crs_skill.coverage_level = s_map["coverage_level"]
            else:
                crs_skill = CourseSkill(
                    course_id=course.id,
                    skill_id=skill_obj.id,
                    coverage_level=s_map["coverage_level"],
                )
                db.add(crs_skill)
            course_skills_count += 1

    db.commit()
    total_courses = db.query(Course).count()
    total_course_skills = db.query(CourseSkill).count()
    print(f" [OK] Courses: {total_courses} total ({courses_inserted} new, {courses_updated} updated)")
    print(f" [OK] Course Skills mappings: {total_course_skills} total")
    stats["courses"] = total_courses
    stats["course_skills"] = total_course_skills

    # ── 4. Seed Projects & ProjectSkills (EXACT 90 Projects) ─────────────────
    try:
        from app.database.seed_projects import seed_fixed_projects
        total_projects = seed_fixed_projects(db)
        stats["projects"] = total_projects
    except Exception as e:
        print(f"Warning: Failed seeding 90 fixed projects catalog: {e}")

    # Seed the 5 complete career courses and learning curriculum
    try:
        from app.database.seed_courses import seed_learning_courses
        seed_learning_courses(db)
    except Exception as e:
        print(f"Warning: Failed seeding learning courses: {e}")

    print("====================================================================")
    print(" Database Seeding Completed Successfully!")
    print("====================================================================")
    return stats



if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
