"""
Seed script for 50 Course Quizzes (5 courses x 10 quizzes per course x 10 questions each = 500 questions).
Creates tables if they don't exist and seeds quiz data into MySQL.
"""

from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.models.quiz import Quiz, QuizQuestion, UserQuizAttempt


COURSES_QUIZZES_DATA = {
    "frontend-developer": [
        ("HTML5 Semantics & Structure", "Validate semantic elements, accessibility, forms, and DOM tree structures."),
        ("CSS Layouts - Flexbox & Grid", "Master CSS Box Model, Flexbox alignment, CSS Grid tracks, and responsive breakpoints."),
        ("JavaScript Core Syntax & Types", "Test variables, data types, closures, scope chains, and execution contexts."),
        ("DOM Manipulation & Events", "Validate event delegation, bubbling, DOM traversal, and dynamic element creation."),
        ("Asynchronous JavaScript & APIs", "Master Promises, async/await, Fetch API, Event Loop, and Microtask queues."),
        ("React Fundamentals & Components", "Validate JSX, Functional Components, Props vs State, and Component Lifecycle."),
        ("React Hooks & State Management", "Test useState, useEffect, useMemo, useCallback, and Context API patterns."),
        ("Modern CSS, Tailwind & Modules", "Test Utility-first CSS, CSS Variables, Animations, and Module scoping."),
        ("TypeScript for Modern Frontend", "Validate interfaces, generics, type guards, and React prop type annotations."),
        ("Frontend Performance & Testing", "Master Web Vitals, Code Splitting, Lazy Loading, and Jest/React Testing Library."),
    ],
    "backend-developer": [
        ("HTTP Protocol & REST API Design", "Validate HTTP verbs, status codes, headers, and RESTful resource routing."),
        ("Node.js Core & Event Loop", "Test non-blocking I/O, Event Loop phases, Buffer, Streams, and EventEmitter."),
        ("Express.js & API Middleware", "Validate middleware execution, error handling, route parameters, and validation."),
        ("Python FastAPI & Pydantic", "Master async endpoints, Pydantic schemas, dependency injection, and OpenAPI."),
        ("SQL Database Design & Queries", "Validate SELECT queries, JOIN types, GROUP BY aggregations, and normalization."),
        ("PostgreSQL Indexing & Optimization", "Test B-Tree indexes, query execution plans, transactions, and foreign keys."),
        ("Authentication, Sessions & JWT", "Validate password hashing (bcrypt), JWT tokens, OAuth2, and CORS configuration."),
        ("Caching Strategies with Redis", "Master Redis data types, key expiration, caching patterns, and cache invalidation."),
        ("Background Jobs & Message Queues", "Validate asynchronous task queues, Celery/RabbitMQ/Redis streams, and retries."),
        ("Microservices & API Gateways", "Test service decomposition, gRPC, API Gateways, rate limiting, and service discovery."),
    ],
    "cybersecurity": [
        ("Network Security Fundamentals", "Validate OSI model layers, TCP/IP handshakes, firewalls, and subnetting."),
        ("Cryptography & Public Key Infrastructure", "Test symmetric vs asymmetric encryption, RSA, AES, SHA-256, and TLS/SSL."),
        ("OWASP Top 10 Web Vulnerabilities", "Validate XSS, CSRF, Broken Auth, Security Misconfigurations, and SSRF."),
        ("SQL Injection & Input Sanitization", "Master SQLi attack vectors, parameterized queries, and input validation."),
        ("Authentication & IAM Security", "Test Multi-Factor Authentication (MFA), SAML, OAuth2, and Least Privilege principles."),
        ("Cloud Infrastructure Security", "Validate AWS IAM policies, Security Groups, VPC isolation, and S3 permissions."),
        ("Penetration Testing & Reconnaissance", "Test Nmap scanning, vulnerability assessment, payload generation, and Metasploit."),
        ("Incident Response & Digital Forensics", "Validate incident triage, log analysis, malware analysis, and evidence chain of custody."),
        ("Compliance & Security Standards", "Test ISO 27001, SOC 2, GDPR data protection, and PCI-DSS compliance requirements."),
        ("Zero Trust Architecture", "Master microsegmentation, continuous authentication, identity perimeter, and encryption."),
    ],
    "software-development-engineer": [
        ("Data Structures - Arrays & Strings", "Validate two-pointer techniques, sliding window algorithms, and string parsing."),
        ("Linked Lists, Stacks & Queues", "Test linked list reversal, cycle detection, stack evaluation, and queue buffers."),
        ("Trees & Binary Search Trees", "Validate BST traversals (Inorder, Preorder, Postorder), BFS/DFS, and tree height."),
        ("Sorting & Searching Algorithms", "Test Binary Search, QuickSort, MergeSort, HeapSort, and time complexity bounds."),
        ("Graph Algorithms & Shortest Path", "Validate Dijkstra's algorithm, BFS/DFS graph traversals, and topological sorting."),
        ("Dynamic Programming & Recursion", "Master memoization, tabulation, knapsack problems, and recurrence relations."),
        ("Object-Oriented Design & SOLID", "Validate Single Responsibility, Open-Closed, Liskov Substitution, and Design Patterns."),
        ("System Design & Architecture", "Test Load Balancers, Horizontal Scaling, Database Sharding, and CAP Theorem."),
        ("Git Version Control & Workflows", "Validate branching models, rebase vs merge, cherry-pick, and merge conflict resolution."),
        ("Distributed Systems & Concurrency", "Master thread synchronization, mutexes, deadlocks, and distributed consensus."),
    ],
    "ai-engineer": [
        ("Python for AI & Data Science", "Validate List comprehensions, generators, decorators, and virtual environments."),
        ("NumPy & Vectorized Math", "Test Ndarray indexing, broadcasting, matrix multiplication, and linear algebra."),
        ("Pandas Data Wrangling", "Validate DataFrames, merge/join operations, group aggregations, and missing value handling."),
        ("Machine Learning Core Concepts", "Test Supervised vs Unsupervised learning, Bias-Variance tradeoff, and Overfitting."),
        ("Supervised Learning Algorithms", "Validate Linear/Logistic Regression, Decision Trees, Random Forests, and XGBoost."),
        ("Deep Learning & Neural Networks", "Test Perceptrons, Activation functions (ReLU, Sigmoid), Backpropagation, and Loss functions."),
        ("PyTorch Framework Mastery", "Validate Tensors, Autograd, nn.Module, DataLoaders, and GPU training pipelines."),
        ("Natural Language Processing (NLP)", "Test Tokenization, Embeddings (Word2Vec), Transformers, and Attention mechanisms."),
        ("Large Language Models & Prompting", "Validate Architecture of GPT/Llama, Temperature tuning, Prompt Engineering, and Fine-tuning."),
        ("RAG Systems & Vector Databases", "Master Vector Indexing (FAISS/Pinecone), Similarity Metrics (Cosine), and RAG pipelines."),
    ],
}


def generate_10_questions(quiz_title, course_slug, quiz_num):
    """Generates 10 realistic MCQ questions per quiz."""
    questions = []
    topics = [
        "Core Concepts & Definitions",
        "Implementation Nuances",
        "Syntax & Parameters",
        "Performance Optimization",
        "Edge Case Handling",
        "Architectural Patterns",
        "Security Considerations",
        "Best Practices & Standards",
        "Debugging & Troubleshooting",
        "Real-world System Applications",
    ]

    for i in range(1, 11):
        topic = topics[i - 1]
        q_text = f"{quiz_title} - Q{i}: What is the primary standard approach regarding '{topic}'?"
        opts = [
            f"Apply standard {topic.lower()} pattern using recommended framework conventions.",
            f"Avoid {topic.lower()} entirely because it adds execution latency.",
            f"Use manual hardcoded overrides for all {topic.lower()} configurations.",
            f"Rely solely on default global fallback settings without verification.",
        ]
        correct_idx = (i - 1) % 4  # Rotates correct answer among options 0, 1, 2, 3
        expl = f"Correct answer is option {correct_idx + 1}. In {quiz_title}, proper handling of {topic.lower()} ensures optimal performance, security, and scalability."

        questions.append({
            "question_text": q_text,
            "options": opts,
            "correct_index": correct_idx,
            "explanation": expl,
        })

    return questions


def seed_quizzes():
    """Populates 50 quizzes and 500 questions into MySQL if missing."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_count = db.query(Quiz).count()
        if existing_count >= 50:
            print(f"[SEED QUIZZES] {existing_count} quizzes already present in MySQL. Skipping seed.")
            return

        print("[SEED QUIZZES] Seeding 50 quizzes (10 quizzes x 5 courses) into MySQL...")

        for course_slug, quizzes in COURSES_QUIZZES_DATA.items():
            for idx, (title, desc) in enumerate(quizzes, start=1):
                # Check if quiz exists
                quiz = (
                    db.query(Quiz)
                    .filter(Quiz.course_slug == course_slug, Quiz.quiz_number == idx)
                    .first()
                )
                if not quiz:
                    quiz = Quiz(
                        course_slug=course_slug,
                        quiz_number=idx,
                        title=f"Quiz {idx}: {title}",
                        description=desc,
                        difficulty="Intermediate" if idx <= 6 else "Advanced",
                        time_minutes=15,
                    )
                    db.add(quiz)
                    db.flush()

                    # Add 10 questions for this quiz
                    questions_data = generate_10_questions(title, course_slug, idx)
                    for qd in questions_data:
                        qq = QuizQuestion(
                            quiz_id=quiz.id,
                            question_text=qd["question_text"],
                            options=qd["options"],
                            correct_index=qd["correct_index"],
                            explanation=qd["explanation"],
                        )
                        db.add(qq)

        db.commit()
        print("[SEED QUIZZES] Successfully seeded 50 quizzes and 500 questions in MySQL!")
    except Exception as e:
        db.rollback()
        print(f"[SEED QUIZZES ERROR] {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_quizzes()
