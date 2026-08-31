"""
Master Seeder for the EXACT 90 Fixed Projects Catalog across 5 Career Programs.

Careers:
1. Frontend Developer (18 projects: 5 Basic, 5 Intermediate, 5 Advanced, 3 Expert)
2. Backend Developer (18 projects: 5 Basic, 5 Intermediate, 5 Advanced, 3 Expert)
3. Cybersecurity (18 projects: 5 Basic, 5 Intermediate, 5 Advanced, 3 Expert)
4. Software Development Engineer (SDE) (18 projects: 5 Basic, 5 Intermediate, 5 Advanced, 3 Expert)
5. AI Engineer (18 projects: 5 Basic, 5 Intermediate, 5 Advanced, 3 Expert)

Total: 90 Projects
"""

import sys
import os
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.models.project import Project
from app.models.project_skill import ProjectSkill
from app.models.skill import Skill

FIXED_PROJECTS_CATALOG = [
    # =========================================================================
    # 1. FRONTEND DEVELOPER (18 Projects)
    # =========================================================================
    # BASIC (5)
    {
        "career_name": "Frontend Developer",
        "title": "Personal Portfolio Website",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Build a responsive personal portfolio website showcasing projects, skills, and contact form.",
        "estimated_hours": 10.0,
        "objectives": ["Structure responsive layout with HTML5 & CSS3", "Implement interactive project showcase and modal", "Add contact form with client-side validation"],
        "suggested_technologies": ["HTML & CSS", "JavaScript", "Tailwind CSS"],
        "requirements": ["Responsive design across mobile/desktop", "Clean Semantic HTML5", "Working contact form validation"],
        "skills": [{"skill_name": "HTML & CSS", "importance": 5}, {"skill_name": "JavaScript", "importance": 5}, {"skill_name": "Tailwind CSS", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Responsive Landing Page",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Design and implement a modern mobile-first landing page with Flexbox/Grid and smooth CSS animations.",
        "estimated_hours": 8.0,
        "objectives": ["Build hero section with call-to-action buttons", "Use CSS Flexbox/Grid for responsive cards", "Integrate CSS transitions for interactive elements"],
        "suggested_technologies": ["HTML & CSS", "JavaScript", "Tailwind CSS"],
        "requirements": ["Mobile-first responsive layout", "Cross-browser compatibility", "Smooth micro-animations"],
        "skills": [{"skill_name": "HTML & CSS", "importance": 5}, {"skill_name": "Tailwind CSS", "importance": 5}, {"skill_name": "JavaScript", "importance": 3}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Interactive To-Do App",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Create a dynamic task management application with filter, search, local storage persistence, and drag-and-drop.",
        "estimated_hours": 12.0,
        "objectives": ["State management for adding, editing, and deleting tasks", "Filter tasks by active/completed status", "Persist task data in browser LocalStorage"],
        "suggested_technologies": ["JavaScript", "React", "HTML & CSS"],
        "requirements": ["LocalStorage persistence", "Filter and search capability", "Zero console errors"],
        "skills": [{"skill_name": "JavaScript", "importance": 5}, {"skill_name": "React", "importance": 5}, {"skill_name": "HTML & CSS", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Weather Dashboard",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Build a real-time weather forecasting dashboard fetching live weather data from open REST APIs.",
        "estimated_hours": 10.0,
        "objectives": ["Fetch current weather and 5-day forecast via OpenWeather API", "Display dynamic weather icons and metrics", "Search weather by city name with error handling"],
        "suggested_technologies": ["JavaScript", "React", "RESTful API Design"],
        "requirements": ["Asynchronous API fetching", "Dynamic weather charts", "Graceful API error state handling"],
        "skills": [{"skill_name": "JavaScript", "importance": 5}, {"skill_name": "React", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Expense Tracker",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Develop an interactive personal budget and expense tracking application with dynamic chart visualizer.",
        "estimated_hours": 14.0,
        "objectives": ["Log transactions with category and date tags", "Calculate total income, expenses, and net balance", "Visualize monthly spending breakdowns using Chart.js"],
        "suggested_technologies": ["JavaScript", "React", "HTML & CSS"],
        "requirements": ["Accurate financial balance math", "Interactive pie/bar charts", "Local storage or state state management"],
        "skills": [{"skill_name": "JavaScript", "importance": 5}, {"skill_name": "React", "importance": 5}, {"skill_name": "HTML & CSS", "importance": 4}]
    },
    # INTERMEDIATE (5)
    {
        "career_name": "Frontend Developer",
        "title": "E-Commerce Frontend",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Build a modern online shopping user interface with product catalog, category filtering, cart management, and checkout flows.",
        "estimated_hours": 20.0,
        "objectives": ["Implement global cart state management", "Multi-criteria product search and price filtering", "Step-by-step interactive checkout form"],
        "suggested_technologies": ["React", "TypeScript", "Tailwind CSS"],
        "requirements": ["Reusable UI component structure", "Persistent shopping cart state", "Responsive grid layout"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 4}, {"skill_name": "Tailwind CSS", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Job Search Portal",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Create an interactive job portal UI featuring multi-criteria filter, job application modal, and bookmarking.",
        "estimated_hours": 18.0,
        "objectives": ["Filter job postings by role, location, and salary", "Bookmark favorite jobs for user profile", "Modal drawer with detailed job description and application upload"],
        "suggested_technologies": ["React", "JavaScript", "Tailwind CSS"],
        "requirements": ["Dynamic filtering algorithms", "Clean modal state drawer", "Accessible UI components"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "JavaScript", "importance": 5}, {"skill_name": "Tailwind CSS", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Food Delivery Interface",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Design a fast food ordering UI with restaurant listing, menu customization, cart drawer, and live order tracking UI.",
        "estimated_hours": 22.0,
        "objectives": ["Browse restaurant menus by category and dietary preferences", "Customize item options and add-ons in cart", "Simulated real-time order tracking progress bar"],
        "suggested_technologies": ["React", "TypeScript", "Tailwind CSS"],
        "requirements": ["Smooth cart drawer transitions", "Optimized image rendering", "Clean component modularity"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 4}, {"skill_name": "Tailwind CSS", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Real-Time Chat Interface",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Build a messaging frontend component supporting channels, direct messages, emojis, typing indicators, and message threads.",
        "estimated_hours": 20.0,
        "objectives": ["Render message threads with auto-scroll to latest", "Support emoji selection and media previews", "Display live online status and typing indicators"],
        "suggested_technologies": ["React", "TypeScript", "RESTful API Design"],
        "requirements": ["Efficient list rendering for messages", "Responsive chat sidebar", "Clean state updates"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 5}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Learning Management Dashboard",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Construct an educational platform UI with course progression, video player, quiz components, and student stats.",
        "estimated_hours": 24.0,
        "objectives": ["Interactive course roadmap with progress indicators", "Embedded video player with lesson completion status", "Multiple choice quiz drawer with instant grading feedback"],
        "suggested_technologies": ["React", "Next.js", "TypeScript"],
        "requirements": ["Accessible media controls", "Progress state calculations", "Modular page routes"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "Next.js", "importance": 4}, {"skill_name": "TypeScript", "importance": 4}]
    },
    # ADVANCED (5)
    {
        "career_name": "Frontend Developer",
        "title": "Full-Featured E-Commerce Platform",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Architect a full-featured e-commerce frontend with state management, client-side routing, payment integration, and order history.",
        "estimated_hours": 32.0,
        "objectives": ["Build full SSR application with Next.js App Router", "Integrate Stripe Payment Sheet checkout", "Manage optimistic UI updates and order tracking history"],
        "suggested_technologies": ["Next.js", "React", "TypeScript", "Tailwind CSS"],
        "requirements": ["Server-Side Rendering (SSR) optimization", "Stripe payment SDK integration", "SEO meta tag structure"],
        "skills": [{"skill_name": "Next.js", "importance": 5}, {"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 5}, {"skill_name": "Tailwind CSS", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Real-Time Collaboration App",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Build a real-time collaborative document or canvas application using WebSockets and optimistic UI updates.",
        "estimated_hours": 35.0,
        "objectives": ["Establish WebSocket client connection with reconnect retry", "Render live collaborative presence indicators", "Optimistic state synchronization for document edits"],
        "suggested_technologies": ["React", "TypeScript", "Next.js"],
        "requirements": ["WebSocket event handling", "Optimistic state management", "Zero race conditions on edit"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 5}, {"skill_name": "Next.js", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Project Management SaaS Dashboard",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Develop a Kanban-style SaaS dashboard with drag-and-drop task boards, sprint tracking, and team analytics charts.",
        "estimated_hours": 30.0,
        "objectives": ["Implement smooth HTML5 drag and drop Kanban columns", "Build interactive velocity and burn-down charts", "Manage complex multi-view state (Board, List, Timeline)"],
        "suggested_technologies": ["React", "TypeScript", "Tailwind CSS"],
        "requirements": ["Fluid drag-and-drop performance", "Complex component state architecture", "Responsive analytics layout"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 5}, {"skill_name": "Tailwind CSS", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Video Streaming Platform UI",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Create a media streaming interface with adaptive video playback, custom player controls, playlists, and recommendations grid.",
        "estimated_hours": 28.0,
        "objectives": ["Custom HTML5 video controls (quality, speed, pip)", "Lazy-loading media thumbnail grid", "Keyboard shortcut support for playback"],
        "suggested_technologies": ["Next.js", "React", "TypeScript"],
        "requirements": ["Custom video control bar", "Lazy loading & skeleton loaders", "Lighthouse performance score >= 90"],
        "skills": [{"skill_name": "Next.js", "importance": 5}, {"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Multi-Tenant Admin Dashboard",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Build a multi-tenant administration interface with dynamic permission roles, data tables, export capabilities, and audit logs.",
        "estimated_hours": 34.0,
        "objectives": ["Role-based UI access control (Admin, Editor, Viewer)", "Server-paginated data table with column sorting and export", "Dynamic theme switching and custom domain branding"],
        "suggested_technologies": ["React", "TypeScript", "Next.js", "Tailwind CSS"],
        "requirements": ["RBAC route protection", "Virtualized high-volume data tables", "Clean design system tokens"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 5}, {"skill_name": "Next.js", "importance": 4}, {"skill_name": "Tailwind CSS", "importance": 4}]
    },
    # EXPERT (3)
    {
        "career_name": "Frontend Developer",
        "title": "Production-Grade SaaS Platform",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Engineer an enterprise production SaaS frontend application with micro-frontend architecture, internationalization, and end-to-end performance optimizations.",
        "estimated_hours": 50.0,
        "objectives": ["Micro-frontend integration using Module Federation", "Multi-language i18n support with RTL layout support", "Automated Lighthouse performance tuning and code splitting"],
        "suggested_technologies": ["Next.js", "React", "TypeScript", "Tailwind CSS"],
        "requirements": ["Sub-1 second First Contentful Paint (FCP)", "Full i18n localization", "Comprehensive Cypress/Playwright test suite"],
        "skills": [{"skill_name": "Next.js", "importance": 5}, {"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 5}, {"skill_name": "Tailwind CSS", "importance": 5}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Real-Time Collaborative Workspace",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Architect a high-performance collaborative workspace supporting operational transformation/CRDTs, rich-text editing, and live presence cursors.",
        "estimated_hours": 60.0,
        "objectives": ["Integrate Yjs / CRDT algorithms for concurrent editing", "Render high-frequency live remote cursor positions", "Custom rich text editor extensions and block rendering"],
        "suggested_technologies": ["React", "TypeScript", "Next.js"],
        "requirements": ["Conflict-free replicated data type (CRDT) synchronization", "60 FPS cursor animation rendering", "Offline-first sync capabilities"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 5}, {"skill_name": "Next.js", "importance": 5}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Enterprise Frontend Architecture",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Design and deploy a scalable enterprise frontend design system, component library, CI/CD automated visual regression testing, and monorepo structure.",
        "estimated_hours": 55.0,
        "objectives": ["Publish zero-dependency React component design system", "Set up TurboRepo monorepo with Storybook documentation", "Automate visual regression tests in GitHub Actions"],
        "suggested_technologies": ["React", "TypeScript", "Git & GitHub Actions", "Next.js"],
        "requirements": ["100% WCAG AA accessibility compliance", "Storybook documentation suite", "Automated package publishing workflow"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 5}, {"skill_name": "Git & GitHub Actions", "importance": 5}, {"skill_name": "Next.js", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "Enterprise Micro-Frontend Architecture",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Architect a scalable micro-frontend ecosystem using Module Federation, shared state, and dynamic bundle loading.",
        "estimated_hours": 45.0,
        "objectives": ["Implement Module Federation across independent React apps", "Build shared design tokens and global state bridge", "Optimize code-splitting and asset caching"],
        "suggested_technologies": ["React", "TypeScript", "Next.js"],
        "requirements": ["Independent deployment capability", "Shared auth state", "Sub-100ms LCP metric"],
        "skills": [{"skill_name": "React", "importance": 5}, {"skill_name": "TypeScript", "importance": 5}, {"skill_name": "Next.js", "importance": 4}]
    },
    {
        "career_name": "Frontend Developer",
        "title": "WebGL 3D Data Visualizer",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Develop an interactive 3D globe and geospatial data visualizer using Three.js and custom Shaders.",
        "estimated_hours": 50.0,
        "objectives": ["Render high-volume 3D data points with WebGL", "Implement custom GLSL shaders for glowing arcs", "Build accessible controls and fallback 2D view"],
        "suggested_technologies": ["React", "TypeScript", "JavaScript"],
        "requirements": ["60 FPS rendering under heavy data load", "Custom shader effects", "Cross-device WebGL fallback"],
        "skills": [{"skill_name": "JavaScript", "importance": 5}, {"skill_name": "TypeScript", "importance": 5}, {"skill_name": "React", "importance": 4}]
    },

    # =========================================================================
    # 2. BACKEND DEVELOPER (18 Projects)
    # =========================================================================
    # BASIC (5)
    {
        "career_name": "Backend Developer",
        "title": "Student Management REST API",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Build a CRUD RESTful API to manage student records, courses, and enrollment data using SQL database persistence.",
        "estimated_hours": 10.0,
        "objectives": ["Implement CRUD endpoints for students and courses", "Data validation with Pydantic / ORM schemas", "Relational foreign key constraints and join queries"],
        "suggested_technologies": ["Python", "FastAPI", "PostgreSQL", "SQL"],
        "requirements": ["RESTful status codes (200, 201, 404)", "SQLAlchemy ORM integration", "Clean API documentation via Swagger"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 4}, {"skill_name": "SQL", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Library Management API",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Implement an API system for cataloging books, handling checkouts/returns, and calculating overdue fines.",
        "estimated_hours": 12.0,
        "objectives": ["Manage book inventory and availability status", "Track user checkout dates and return timestamps", "Calculate overdue fine logic on API query"],
        "suggested_technologies": ["Python", "FastAPI", "PostgreSQL", "RESTful API Design"],
        "requirements": ["Transaction isolation for checkout status", "Structured error responses", "Automated Pytest unit tests"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Expense Management API",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Create a backend service for tracking income and expenses with category grouping and monthly analytics aggregation.",
        "estimated_hours": 10.0,
        "objectives": ["Store categorized financial records", "Execute SQL aggregate queries (SUM, AVG, GROUP BY)", "Export expense summaries in CSV or JSON format"],
        "suggested_technologies": ["Python", "FastAPI", "SQL", "PostgreSQL"],
        "requirements": ["Optimized aggregate query execution", "Input parameter sanitization", "Comprehensive test endpoints"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "SQL", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Blog Backend",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Develop a blogging platform backend with posts, comments, tags, and user authentication.",
        "estimated_hours": 14.0,
        "objectives": ["User registration and password hashing", "CRUD operations for blog posts and nested comments", "Tag-based post indexing and searching"],
        "suggested_technologies": ["Python", "FastAPI", "PostgreSQL", "Web Application Security (OWASP)"],
        "requirements": ["Bcrypt password security", "One-to-many & Many-to-many ORM mappings", "Swagger UI endpoint test coverage"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 4}, {"skill_name": "Web Application Security (OWASP)", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Task Management API",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Construct a REST API for task workflows, priority tags, due dates, and user assignment.",
        "estimated_hours": 12.0,
        "objectives": ["Task lifecycle state transitions (Pending, In Progress, Completed)", "Filter tasks by priority, category, and due date", "User task assignment and authorization checks"],
        "suggested_technologies": ["Python", "FastAPI", "RESTful API Design", "PostgreSQL"],
        "requirements": ["Clean RESTful route parameters", "Pydantic validation schemas", "Database transaction safety"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "RESTful API Design", "importance": 4}, {"skill_name": "PostgreSQL", "importance": 4}]
    },
    # INTERMEDIATE (5)
    {
        "career_name": "Backend Developer",
        "title": "E-Commerce Backend",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Build an e-commerce backend service with product inventory, cart management, checkout workflow, and order processing.",
        "estimated_hours": 24.0,
        "objectives": ["Product stock reservation and inventory decrementing", "Shopping cart persistence per session / user", "Order creation with transaction rollback protection"],
        "suggested_technologies": ["Python", "FastAPI", "PostgreSQL", "Redis"],
        "requirements": ["ACID Compliant DB transactions", "Redis session caching", "JWT bearer token authorization"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 5}, {"skill_name": "Redis", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Job Portal Backend",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Develop an API service for posting jobs, managing applicant resumes, matching candidates, and tracking application status.",
        "estimated_hours": 22.0,
        "objectives": ["Employer job post publishing and expiration", "Candidate resume attachment upload and storage", "Application workflow state transitions"],
        "suggested_technologies": ["Python", "FastAPI", "PostgreSQL", "RESTful API Design"],
        "requirements": ["Secure file upload validation", "Role-based authorization (Employer vs Applicant)", "Full-text search queries"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Food Delivery Backend",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Build a backend system for restaurant menus, order dispatching, driver location updates, and rating workflows.",
        "estimated_hours": 26.0,
        "objectives": ["Hierarchical menu management (Category -> Item -> Modifiers)", "Order dispatch matching algorithm", "Geospatial queries for nearby restaurant delivery zones"],
        "suggested_technologies": ["Python", "FastAPI", "PostgreSQL", "Redis"],
        "requirements": ["PostGIS / Spatial SQL indexing", "Redis key-value caching", "Clean service-oriented backend structure"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 4}, {"skill_name": "Redis", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "URL Shortener Service",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Construct a high-performance URL shortening API with hash encoding, redirect analytics, and expiration policies.",
        "estimated_hours": 18.0,
        "objectives": ["Base62 encoding for compact unique key generation", "Sub-millisecond HTTP 302 redirects with Redis cache", "Analytics aggregation (click count, referrer, geo location)"],
        "suggested_technologies": ["Python", "FastAPI", "Redis", "PostgreSQL"],
        "requirements": ["Redis cache-aside pattern", "High read throughput optimization", "Collision-free hash generation"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "Redis", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Authentication & Authorization Service",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Architect a centralized Auth microservice providing JWT access/refresh tokens, OAuth2 integration, password hashing, and RBAC middleware.",
        "estimated_hours": 20.0,
        "objectives": ["JWT issuance, verification, and rotation with secret key", "Password hashing with Argon2 / Bcrypt", "Role-Based Access Control (RBAC) middleware decorator"],
        "suggested_technologies": ["Python", "FastAPI", "Web Application Security (OWASP)", "PostgreSQL"],
        "requirements": ["Secure HTTP-Only cookie handling", "Token blacklisting in Redis", "Protection against brute-force and timing attacks"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "Web Application Security (OWASP)", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 4}]
    },
    # ADVANCED (5)
    {
        "career_name": "Backend Developer",
        "title": "Scalable E-Commerce Backend",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Build a distributed e-commerce backend with database indexing, Redis caching, transaction isolation, and inventory concurrency controls.",
        "estimated_hours": 36.0,
        "objectives": ["Prevent double-booking stock under high concurrency", "Distributed lock pattern using Redis Redlock", "Database read-replica distribution"],
        "suggested_technologies": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
        "requirements": ["Pessimistic / Optimistic locking mechanism", "Containerized setup with Docker Compose", "Load-tested under simulated concurrent requests"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 5}, {"skill_name": "Redis", "importance": 4}, {"skill_name": "Docker", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Real-Time Notification Service",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Engineer an event-driven notification engine delivering push, email, and SMS alerts using message queues (RabbitMQ/Kafka) and WebSockets.",
        "estimated_hours": 34.0,
        "objectives": ["Publish-subscribe event message processing", "Asynchronous email/SMS dispatch worker pool", "WebSocket client connection pool management"],
        "suggested_technologies": ["Python", "FastAPI", "Redis", "Docker"],
        "requirements": ["Asynchronous queue consumer decoupling", "At-least-once message delivery guarantee", "Graceful worker shutdown"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "Redis", "importance": 5}, {"skill_name": "Docker", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Payment Processing Backend",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Implement a resilient payment processing API with Stripe/PayPal webhooks, idempotent transaction handling, and audit logging.",
        "estimated_hours": 32.0,
        "objectives": ["Webhook signature verification and event dispatch", "Idempotency key header enforcement to prevent duplicate charges", "Immutable transaction audit log database schema"],
        "suggested_technologies": ["Python", "FastAPI", "PostgreSQL", "Web Application Security (OWASP)"],
        "requirements": ["Strict HMAC SHA256 webhook verification", "Idempotency key enforcement", "Detailed audit logging"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 5}, {"skill_name": "Web Application Security (OWASP)", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Distributed Job Scheduler",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Develop a distributed background job scheduling system supporting cron syntax, retry backoff strategies, and worker heartbeat monitoring.",
        "estimated_hours": 38.0,
        "objectives": ["Parse cron expressions for scheduled execution", "Exponential backoff retry policy for failed jobs", "Distributed worker node heartbeats and failover"],
        "suggested_technologies": ["Python", "FastAPI", "Redis", "Docker"],
        "requirements": ["Cron expression evaluation engine", "Distributed lock protection against duplicate runs", "Worker health check telemetry"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "Redis", "importance": 5}, {"skill_name": "Docker", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "API Gateway",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Construct a custom API gateway microservice providing reverse proxying, rate limiting, request validation, and routing policies.",
        "estimated_hours": 35.0,
        "objectives": ["Token bucket rate limiting algorithm via Redis", "Reverse proxy HTTP request forwarding to downstream services", "Centralized JWT validation and header injection"],
        "suggested_technologies": ["Python", "FastAPI", "Redis", "RESTful API Design"],
        "requirements": ["Sub-10ms proxy overhead", "Distributed rate limiting", "Dynamic service route configuration"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "Redis", "importance": 5}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    # EXPERT (3)
    {
        "career_name": "Backend Developer",
        "title": "Distributed E-Commerce System",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Engineer a high-throughput microservices e-commerce ecosystem with saga pattern distributed transactions and event sourcing.",
        "estimated_hours": 55.0,
        "objectives": ["Implement Saga Pattern for multi-service transactions (Order, Payment, Inventory)", "Event Sourcing architecture for complete system state audit", "gRPC inter-service communication"],
        "suggested_technologies": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
        "requirements": ["Event-driven saga orchestration / choreography", "Distributed tracing support", "Fault isolation & circuit breakers"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 5}, {"skill_name": "Redis", "importance": 5}, {"skill_name": "Docker", "importance": 5}]
    },
    {
        "career_name": "Backend Developer",
        "title": "High-Scale Social Media Backend",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Architect a social media backend capable of handling high write throughput, newsfeed fan-out algorithms, and distributed caching.",
        "estimated_hours": 60.0,
        "objectives": ["Fan-out on write vs fan-out on read newsfeed algorithm", "Distributed caching for high-traffic user timelines", "Graph query algorithms for mutual friend suggestions"],
        "suggested_technologies": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
        "requirements": ["Sub-50ms newsfeed retrieval", "Sharded database design pattern", "Benchmarked under 10k RPS synthetic load"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 5}, {"skill_name": "Redis", "importance": 5}, {"skill_name": "Docker", "importance": 5}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Production-Grade Cloud Backend",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Build and deploy a production cloud backend infrastructure using Kubernetes, terraform IaC, blue-green deployment pipelines, and zero-downtime database migrations.",
        "estimated_hours": 65.0,
        "objectives": ["Provision cloud infrastructure with Terraform IaC", "Deploy microservices on Kubernetes cluster with horizontal pod autoscaling", "Automate blue-green zero-downtime deployment pipeline"],
        "suggested_technologies": ["Docker", "Python", "FastAPI", "PostgreSQL", "Redis"],
        "requirements": ["Terraform IaC configuration", "Kubernetes manifests and Helm chart", "Zero-downtime schema migration script"],
        "skills": [{"skill_name": "Docker", "importance": 5}, {"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 5}, {"skill_name": "Redis", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Distributed Event Broker Engine",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Build a high-throughput pub-sub event streaming broker with WAL persistence and consumer group offset management.",
        "estimated_hours": 50.0,
        "objectives": ["Write disk-backed Write-Ahead-Log storage engine", "Handle TCP consumer connections with binary protocol", "Manage partition rebalancing across consumer groups"],
        "suggested_technologies": ["Python", "FastAPI", "Docker"],
        "requirements": ["Sub-millisecond event dispatch latency", "At-least-once delivery guarantee", "WAL crash recovery"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "Docker", "importance": 4}]
    },
    {
        "career_name": "Backend Developer",
        "title": "Real-Time Distributed Transaction Manager",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Implement a Two-Phase Commit (2PC) and Saga pattern orchestrator for distributed financial transactions.",
        "estimated_hours": 48.0,
        "objectives": ["Orchestrate Saga pattern workflow with compensating actions", "Implement distributed locking via Redis/Etcd", "Build idempotent API endpoints with idempotency keys"],
        "suggested_technologies": ["Python", "PostgreSQL", "Redis"],
        "requirements": ["Zero transaction leakage under node crash", "Strict idempotency validation", "Comprehensive audit log"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "PostgreSQL", "importance": 5}, {"skill_name": "Redis", "importance": 4}]
    },

    # =========================================================================
    # 3. CYBERSECURITY (18 Projects)
    # =========================================================================
    # BASIC (5)
    {
        "career_name": "Cybersecurity",
        "title": "Password Strength Analyzer",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Create a tool that evaluates password complexity, entropy, common dictionary matches, and provides security recommendations.",
        "estimated_hours": 8.0,
        "objectives": ["Calculate mathematical bit entropy of password strings", "Check against HaveIBeenPwned API or common dictionary wordlists", "Provide actionable feedback to improve credential security"],
        "suggested_technologies": ["Python", "Cryptography", "Web Application Security (OWASP)"],
        "requirements": ["Accurate entropy calculation formula", "Zero plain-text password logging", "Clean command-line or Web interface"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Cryptography", "importance": 5}, {"skill_name": "Web Application Security (OWASP)", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "File Integrity Monitor",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Develop a system script that computes cryptographic hashes (SHA-256) of critical system files and alerts on unauthorized modifications.",
        "estimated_hours": 10.0,
        "objectives": ["Generate baseline SHA-256 hashes for target directory files", "Recursively scan files and compare against saved baseline", "Trigger alerts on file modifications, additions, or deletions"],
        "suggested_technologies": ["Python", "Cryptography", "Linux Administration"],
        "requirements": ["SHA-256 checksum computation", "Automated baseline verification", "Clear logging of file tampered events"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Cryptography", "importance": 5}, {"skill_name": "Linux Administration", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Secure Login System",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Build a login authentication module implementing bcrypt password hashing, account lockout after failed attempts, and rate limiting.",
        "estimated_hours": 12.0,
        "objectives": ["Implement Argon2 / Bcrypt secure password hashing with salt", "Track failed login attempts and trigger exponential lockout time", "Set up rate limiting headers to prevent brute-force attacks"],
        "suggested_technologies": ["Python", "Web Application Security (OWASP)", "Cryptography"],
        "requirements": ["Defense against timing and brute-force attacks", "Secure session cookie flags (HttpOnly, Secure, SameSite)", "Clean audit logs"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Web Application Security (OWASP)", "importance": 5}, {"skill_name": "Cryptography", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Network Traffic Visualizer",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Create a network analysis utility that parses packet captures (pcap) and visualizes protocols, ports, and bandwidth usage statistics.",
        "estimated_hours": 14.0,
        "objectives": ["Parse pcap files using Scapy / Wireshark libraries", "Aggregate bandwidth usage by source IP and protocol (TCP/UDP/ICMP)", "Display interactive traffic summary dashboard"],
        "suggested_technologies": ["Python", "Network Security", "Linux Administration"],
        "requirements": ["PCAP parsing accuracy", "Protocol breakdown visualization", "CLI/Web dashboard output"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Network Security", "importance": 5}, {"skill_name": "Linux Administration", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Security Log Analyzer",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Implement a log parser that scans server access logs for suspicious activity like brute-force attempts and SQL injection patterns.",
        "estimated_hours": 12.0,
        "objectives": ["Parse Apache/Nginx access logs for suspicious query parameters", "Detect regex patterns for SQLi, XSS, and directory traversal", "Generate summary report of top offending IP addresses"],
        "suggested_technologies": ["Python", "Web Application Security (OWASP)", "SIEM & Threat Detection"],
        "requirements": ["Regex security signature matching", "Log format parsing robustness", "Executive summary report output"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Web Application Security (OWASP)", "importance": 5}, {"skill_name": "SIEM & Threat Detection", "importance": 4}]
    },
    # INTERMEDIATE (5)
    {
        "career_name": "Cybersecurity",
        "title": "Vulnerability Assessment Dashboard",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Construct a dashboard to aggregate, categorize, and prioritize CVE vulnerability scan results across network assets.",
        "estimated_hours": 20.0,
        "objectives": ["Import OpenVAS / Nmap XML vulnerability scan outputs", "Categorize vulnerabilities by CVSS v3 score and severity level", "Track remediation progress and target fix SLA dates"],
        "suggested_technologies": ["Python", "Vulnerability Assessment", "Network Security"],
        "requirements": ["CVSS score calculation & grouping", "Asset risk score calculation", "Filterable vulnerability grid"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Vulnerability Assessment", "importance": 5}, {"skill_name": "Network Security", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Secure File Sharing System",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Build an encrypted file sharing application utilizing end-to-end symmetric encryption (AES-256) and time-decaying download links.",
        "estimated_hours": 22.0,
        "objectives": ["Encrypt uploaded files client-side / server-side with AES-256-GCM", "Generate single-use or time-expiring signed download URLs", "Securely wipe expired files from storage disk"],
        "suggested_technologies": ["Python", "Cryptography", "Web Application Security (OWASP)"],
        "requirements": ["AES-256-GCM encryption with random IV", "Signed URL expiration enforcement", "Zero file leak window"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Cryptography", "importance": 5}, {"skill_name": "Web Application Security (OWASP)", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Security Event Monitoring System",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Develop a real-time event monitor that ingests security telemetry, triggers alert rules, and generates incident notifications.",
        "estimated_hours": 24.0,
        "objectives": ["Stream syslog/event logs into processing engine", "Define custom threshold rules (e.g. >5 failed logins in 1 min)", "Send instant webhook alerts for critical security triggers"],
        "suggested_technologies": ["Python", "SIEM & Threat Detection", "Network Security"],
        "requirements": ["Real-time event processing stream", "Custom rule engine evaluation", "Webhook notification integration"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "SIEM & Threat Detection", "importance": 5}, {"skill_name": "Network Security", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Phishing Awareness Simulator",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Build an educational simulation platform to launch controlled phishing campaigns and track organizational security awareness metrics.",
        "estimated_hours": 18.0,
        "objectives": ["Template email generator with tracking pixels and landing page links", "Track email open rates and simulated credential submits", "Generate security risk metrics by department"],
        "suggested_technologies": ["Python", "Web Application Security (OWASP)", "Network Security"],
        "requirements": ["Controlled simulation isolation", "Detailed tracking telemetry", "Educational remediation landing page"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Web Application Security (OWASP)", "importance": 5}, {"skill_name": "Network Security", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Web Security Testing Lab",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Set up a controlled web vulnerability lab demonstrating OWASP Top 10 vulnerabilities (SQLi, XSS, CSRF) with fix remediations.",
        "estimated_hours": 22.0,
        "objectives": ["Build intentionally vulnerable test endpoints for SQLi, XSS, CSRF", "Write exploit proof-of-concept (PoC) scripts", "Implement secure code patches and verify fix efficacy"],
        "suggested_technologies": ["Python", "Web Application Security (OWASP)", "Penetration Testing"],
        "requirements": ["OWASP Top 10 vulnerability demonstrations", "Executable exploit PoC scripts", "Remediated safe code implementation"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Web Application Security (OWASP)", "importance": 5}, {"skill_name": "Penetration Testing", "importance": 4}]
    },
    # ADVANCED (5)
    {
        "career_name": "Cybersecurity",
        "title": "Mini SIEM Platform",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Engineer a Security Information and Event Management platform with centralized log ingestion, correlation rules, and threat dashboards.",
        "estimated_hours": 36.0,
        "objectives": ["Centralized log collector supporting Syslog and JSON telemetry", "Complex multi-stage event correlation engine", "Real-time threat detection timeline dashboard"],
        "suggested_technologies": ["Python", "SIEM & Threat Detection", "Network Security", "Linux Administration"],
        "requirements": ["Multi-source log normalization", "Custom rule correlation engine", "High-performance search query engine"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "SIEM & Threat Detection", "importance": 5}, {"skill_name": "Network Security", "importance": 4}, {"skill_name": "Linux Administration", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Intrusion Detection Dashboard",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Construct a real-time Intrusion Detection System (IDS) dashboard monitoring Snort/Suricata alerts and anomaly signatures.",
        "estimated_hours": 32.0,
        "objectives": ["Parse EVE.json Suricata log streams in real-time", "Group alerts by attack classification and severity level", "Interactive geographic IP threat mapping"],
        "suggested_technologies": ["Python", "Network Security", "SIEM & Threat Detection"],
        "requirements": ["Suricata/Snort log stream integration", "Live alert feed updates", "Geographic threat visualization"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Network Security", "importance": 5}, {"skill_name": "SIEM & Threat Detection", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Security Incident Response Platform",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Develop an automated Security Orchestration, Automation, and Response (SOAR) playbook engine for isolating infected endpoints and revoking credentials.",
        "estimated_hours": 38.0,
        "objectives": ["Automated incident response playbook execution", "API integrations for firewall rule blocking and account disablement", "Incident timeline tracking and forensic evidence storage"],
        "suggested_technologies": ["Python", "SIEM & Threat Detection", "Network Security", "Linux Administration"],
        "requirements": ["Automated playbook execution engine", "Audit-trailed mitigation actions", "Forensic artifact storage"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "SIEM & Threat Detection", "importance": 5}, {"skill_name": "Network Security", "importance": 4}, {"skill_name": "Linux Administration", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Secure API Gateway",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Implement an API security gateway featuring web application firewall (WAF) rules, bot detection, OAuth2 enforcement, and request sanitization.",
        "estimated_hours": 34.0,
        "objectives": ["WAF rule inspection for SQLi, XSS, and command injection", "Client fingerprinting and automated bot detection", "OAuth2 JWT token validation and scope enforcement"],
        "suggested_technologies": ["Python", "Web Application Security (OWASP)", "Network Security", "Cryptography"],
        "requirements": ["Sub-millisecond WAF payload inspection", "Zero false positives on standard requests", "Complete request sanitization layer"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Web Application Security (OWASP)", "importance": 5}, {"skill_name": "Network Security", "importance": 4}, {"skill_name": "Cryptography", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Threat Intelligence Dashboard",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Build a dashboard aggregating threat intelligence feeds (STIX/TAXII), IP reputation scores, and IOC correlation graphs.",
        "estimated_hours": 30.0,
        "objectives": ["Ingest external STIX/TAXII threat feeds", "Calculate dynamic IP/Domain reputation risk scores", "Cross-reference enterprise logs against Indicators of Compromise (IOCs)"],
        "suggested_technologies": ["Python", "SIEM & Threat Detection", "Network Security"],
        "requirements": ["STIX/TAXII feed parsing", "IOC correlation engine", "Interactive threat visualizer"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "SIEM & Threat Detection", "importance": 5}, {"skill_name": "Network Security", "importance": 4}]
    },
    # EXPERT (3)
    {
        "career_name": "Cybersecurity",
        "title": "Enterprise Security Monitoring Platform",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Architect an enterprise security monitoring platform with distributed log collectors, machine-learning anomaly detection, and automated threat hunting.",
        "estimated_hours": 55.0,
        "objectives": ["Deploy distributed log collector agents", "Train ML Isolation Forest for network traffic anomaly detection", "Automated threat hunting query execution"],
        "suggested_technologies": ["Python", "SIEM & Threat Detection", "Network Security", "Cryptography", "Linux Administration"],
        "requirements": ["ML-powered anomaly detection model", "Distributed log collector agents", "Threat hunting query framework"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "SIEM & Threat Detection", "importance": 5}, {"skill_name": "Network Security", "importance": 5}, {"skill_name": "Cryptography", "importance": 4}, {"skill_name": "Linux Administration", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Security Operations Center Dashboard",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Construct a full SOC operations center dashboard integrating SIEM, SOAR, vulnerability scanners, and real-time incident triage metrics.",
        "estimated_hours": 60.0,
        "objectives": ["Unified SOC analyst command center UI", "Real-time incident triage and analyst ticket assignment", "MTTD (Mean Time to Detect) & MTTR (Mean Time to Respond) telemetry"],
        "suggested_technologies": ["Python", "SIEM & Threat Detection", "Vulnerability Assessment", "Network Security"],
        "requirements": ["Unified multi-tool data integration", "Real-time incident triage pipeline", "Executive SOC performance metrics"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "SIEM & Threat Detection", "importance": 5}, {"skill_name": "Vulnerability Assessment", "importance": 5}, {"skill_name": "Network Security", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Zero-Trust Security Architecture Lab",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Design and deploy a zero-trust network environment implementing micro-segmentation, continuous identity verification, mTLS encryption, and explicit trust boundaries.",
        "estimated_hours": 65.0,
        "objectives": ["mTLS mutual authentication between all microservices", "Continuous identity and device posture verification", "Micro-segmentation firewall rules and policy enforcement"],
        "suggested_technologies": ["Network Security", "Cryptography", "Linux Administration", "Web Application Security (OWASP)"],
        "requirements": ["Strict mTLS certificate authority setup", "Continuous identity evaluation engine", "Zero trust boundary validation"],
        "skills": [{"skill_name": "Network Security", "importance": 5}, {"skill_name": "Cryptography", "importance": 5}, {"skill_name": "Linux Administration", "importance": 5}, {"skill_name": "Web Application Security (OWASP)", "importance": 4}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Automated Threat Hunting & SIEM Engine",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Build an enterprise SIEM log analysis engine with real-time Sigma rule matching and automated containment hooks.",
        "estimated_hours": 55.0,
        "objectives": ["Parse sysmon and network logs at 10k logs/sec", "Evaluate Sigma detection rules against stream", "Trigger automated firewall isolate actions upon critical breach"],
        "suggested_technologies": ["Python", "Linux Administration", "Network Security"],
        "requirements": ["Real-time log ingestion pipeline", "Sigma rule parser & evaluator", "Automated SOAR response playbooks"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Linux Administration", "importance": 5}, {"skill_name": "Network Security", "importance": 5}]
    },
    {
        "career_name": "Cybersecurity",
        "title": "Cloud Zero-Trust Mesh & Identity Guard",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Deploy a Zero-Trust service mesh with mTLS certificate rotation, SPIFFE/SPIRE identity, and micro-segmentation.",
        "estimated_hours": 50.0,
        "objectives": ["Configure SPIFFE identity issuance for workloads", "Enforce dynamic mTLS policy between microservices", "Audit network traffic against zero-trust policy"],
        "suggested_technologies": ["Linux Administration", "Network Security", "Docker"],
        "requirements": ["Automated mTLS cert renewal", "Zero plaintext inter-service traffic", "Strict policy enforcement"],
        "skills": [{"skill_name": "Linux Administration", "importance": 5}, {"skill_name": "Network Security", "importance": 5}, {"skill_name": "Docker", "importance": 4}]
    },

    # =========================================================================
    # 4. SOFTWARE DEVELOPMENT ENGINEER (SDE) (18 Projects)
    # =========================================================================
    # BASIC (5)
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Student Management System",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Develop an object-oriented software system managing student records, grade calculations, and academic report generation.",
        "estimated_hours": 10.0,
        "objectives": ["OOP class hierarchy (Person -> Student, Teacher)", "GPA and course grade calculation algorithms", "Persist student records to SQL database / file storage"],
        "suggested_technologies": ["Java", "Python", "SQL"],
        "requirements": ["Clean Object-Oriented Design principles", "Data persistence layer", "Unit tests for GPA calculation logic"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 4}, {"skill_name": "SQL", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Banking Console Application",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Build a secure console banking application handling accounts, deposits, withdrawals, fund transfers, and transaction logs.",
        "estimated_hours": 12.0,
        "objectives": ["Account creation, PIN verification, and balance tracking", "Atomic fund transfer between accounts with validation checks", "Formatted transaction ledger export"],
        "suggested_technologies": ["Java", "C++", "Python"],
        "requirements": ["Thread-safe account balance operations", "Input validation against negative amounts", "Transaction ledger audit log"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "C++", "importance": 4}, {"skill_name": "Python", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Library Management System",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Implement a desktop/console library application for cataloging items, tracking borrowers, and managing reservation queues.",
        "estimated_hours": 10.0,
        "objectives": ["Book search using HashMaps / Indexed lists", "Borrower queue management using Data Structures (FIFO Queue)", "Overdue calculation algorithms"],
        "suggested_technologies": ["Java", "Python", "SQL"],
        "requirements": ["Efficient Data Structures selection", "Clean CLI or GUI interface", "Search lookup complexity O(1) or O(log N)"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 4}, {"skill_name": "SQL", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Inventory Management System",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Create an inventory control application tracking stock levels, reorder thresholds, suppliers, and transaction histories.",
        "estimated_hours": 12.0,
        "objectives": ["Track stock quantity, SKU numbers, and reorder alerts", "Supplier relationship database mapping", "CSV report generation for low stock inventory"],
        "suggested_technologies": ["Java", "Python", "SQL"],
        "requirements": ["Accurate stock calculations", "SQL database persistence", "Clean error handling"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 4}, {"skill_name": "SQL", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Expense Tracker",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Build a clean software application to record personal financial transactions, analyze spending trends, and export summary reports.",
        "estimated_hours": 10.0,
        "objectives": ["Record income and spending entries with dates and categories", "Monthly spending breakdown by category", "Data visualization or formatted summary report"],
        "suggested_technologies": ["Python", "Java", "SQL"],
        "requirements": ["Data validation rules", "Clean class structure", "Persistent database/file storage"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Java", "importance": 4}, {"skill_name": "SQL", "importance": 4}]
    },
    # INTERMEDIATE (5)
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Online Book Store",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Build an online bookstore platform with catalog browsing, shopping cart state management, checkout, and order receipt generation.",
        "estimated_hours": 20.0,
        "objectives": ["Implement multi-layer architecture (Controller, Service, Repository)", "Shopping cart state management", "Order processing with receipt generation"],
        "suggested_technologies": ["Java", "Python", "SQL", "RESTful API Design"],
        "requirements": ["Layered enterprise design pattern", "Database transaction management", "REST API integration"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 4}, {"skill_name": "SQL", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Employee Management Platform",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Develop an enterprise employee management portal with HR workflows, department hierarchies, payroll calculations, and attendance tracking.",
        "estimated_hours": 22.0,
        "objectives": ["Tree data structure for organization hierarchy", "Automated monthly payroll calculations with tax deductions", "Attendance logging and leave request approval workflow"],
        "suggested_technologies": ["Java", "SQL", "RESTful API Design"],
        "requirements": ["Tree traversal algorithms for org chart", "Accurate tax math calculations", "Role-based HR privileges"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "SQL", "importance": 5}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Ride Booking System",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Architect a ride matching system with fare estimation, driver dispatch algorithm, route tracking, and trip history.",
        "estimated_hours": 24.0,
        "objectives": ["Driver matching based on Euclidean / Manhattan distance", "Dynamic fare calculation algorithm (base rate + distance + surge)", "Trip state machine (Requested, Accepted, In Progress, Completed)"],
        "suggested_technologies": ["Java", "Python", "SQL", "RESTful API Design"],
        "requirements": ["Geospatial distance sorting algorithm", "State machine pattern implementation", "Thread-safe driver dispatch"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 4}, {"skill_name": "SQL", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Food Ordering System",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Create a food ordering management application with menu management, order state machine, and delivery status tracking.",
        "estimated_hours": 22.0,
        "objectives": ["Manage restaurant menus and dish availability", "Order placement with concurrency protection", "Delivery status notification state updates"],
        "suggested_technologies": ["Java", "Python", "SQL", "RESTful API Design"],
        "requirements": ["State machine order lifecycle", "Database transaction handling", "Clean API interface"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 4}, {"skill_name": "SQL", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Online Examination System",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Construct an automated examination platform supporting timed tests, randomized question banks, auto-grading, and performance analytics.",
        "estimated_hours": 24.0,
        "objectives": ["Randomized question selector algorithm from bank", "Countdown timer thread with auto-submit on expiry", "Auto-grading engine and percentile calculation"],
        "suggested_technologies": ["Java", "Python", "SQL", "RESTful API Design"],
        "requirements": ["Concurrent timer management", "Randomization fairness algorithms", "Result analytics aggregation"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 4}, {"skill_name": "SQL", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    # ADVANCED (5)
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Scalable E-Commerce System",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Design and build a scalable full-stack e-commerce system featuring decoupled components, database optimization, and high availability.",
        "estimated_hours": 36.0,
        "objectives": ["Microservices / decoupled component architecture", "Database indexing and query execution plan optimization", "Redis caching strategy for high-frequency reads"],
        "suggested_technologies": ["Java", "Python", "SQL", "Docker", "RESTful API Design"],
        "requirements": ["High-throughput query optimization", "Dockerized container deployment", "Clean system design documentation"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 4}, {"skill_name": "SQL", "importance": 5}, {"skill_name": "Docker", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Real-Time Chat Application",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Build a high-concurrency real-time chat application with WebSocket connection pooling, message persistence, and group channels.",
        "estimated_hours": 34.0,
        "objectives": ["High-concurrency Netty / WebSocket server framework", "Message ordering and delivery acknowledgement protocol", "Group chat room broadcast fan-out"],
        "suggested_technologies": ["Java", "C++", "Docker", "RESTful API Design"],
        "requirements": ["Non-blocking I/O event loop", "Message persistence layer", "Sub-20ms message broadcast latency"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "C++", "importance": 4}, {"skill_name": "Docker", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Job Recommendation Platform",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Implement an automated candidate-job matching engine using scoring algorithms, skill similarity indexing, and application tracking.",
        "estimated_hours": 32.0,
        "objectives": ["Cosine similarity scoring algorithm between candidate skills and job requirements", "Inverted index for fast skill keyword matching", "Asynchronous job notification worker pool"],
        "suggested_technologies": ["Java", "Python", "SQL", "RESTful API Design"],
        "requirements": ["Vector similarity calculation accuracy", "Inverted index lookup efficiency", "Scalable batch processing"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 5}, {"skill_name": "SQL", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Distributed URL Shortener",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Architect a distributed URL shortening service handling high read/write loads with key generation service (KGS) and caching layers.",
        "estimated_hours": 38.0,
        "objectives": ["Design Key Generation Service (KGS) to prevent hash collisions", "Cache popular shortened links in memory", "Distributed load balancing across API nodes"],
        "suggested_technologies": ["Java", "Python", "Docker", "SQL", "RESTful API Design"],
        "requirements": ["Collision-free pre-generated key ring", "Read/Write throughput ratio optimization (100:1)", "High availability setup"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 4}, {"skill_name": "Docker", "importance": 4}, {"skill_name": "SQL", "importance": 4}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Online Code Judge",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Build an online coding assessment platform executing code safely in sandboxed containers (Docker), measuring execution time and memory against test cases.",
        "estimated_hours": 40.0,
        "objectives": ["Isolated Docker sandbox execution with CPU/Memory limits", "Test case verification runner (Accepted, Time Limit Exceeded, Wrong Answer)", "Security sandboxing against system call exploitation"],
        "suggested_technologies": ["Java", "Python", "Docker", "Linux Administration"],
        "requirements": ["Secure Docker container isolation", "Strict memory & timeout limits", "Accurate runtime measurement"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 5}, {"skill_name": "Docker", "importance": 5}, {"skill_name": "Linux Administration", "importance": 4}]
    },
    # EXPERT (3)
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Distributed Social Media Platform",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Design and implement a high-scale distributed social network backend supporting newsfeed generation, media uploads, and follow graphs.",
        "estimated_hours": 60.0,
        "objectives": ["Graph database / follow network traversal algorithm", "Distributed newsfeed fan-out pipeline", "High-throughput timeline cache sharding"],
        "suggested_technologies": ["Java", "Python", "Docker", "SQL", "Linux Administration"],
        "requirements": ["Sharded database architecture", "Sub-50ms newsfeed generation", "Complete System Design document"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 5}, {"skill_name": "Docker", "importance": 5}, {"skill_name": "SQL", "importance": 5}, {"skill_name": "Linux Administration", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "High-Scale Ride Sharing Platform",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Architect a distributed ride-sharing system with geospatial indexing (H3/S2), real-time location streaming, dynamic surge pricing, and trip routing.",
        "estimated_hours": 65.0,
        "objectives": ["Geospatial index partitioning (Uber H3 / Google S2)", "Real-time WebSockets driver location ingestion (100k updates/sec)", "Dynamic supply/demand surge pricing algorithm"],
        "suggested_technologies": ["Java", "Python", "Docker", "SQL", "RESTful API Design"],
        "requirements": ["H3/S2 Spatial indexing execution", "High-throughput location ingestion pipeline", "Low-latency driver matching"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 5}, {"skill_name": "Docker", "importance": 5}, {"skill_name": "SQL", "importance": 5}, {"skill_name": "RESTful API Design", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Cloud-Based E-Commerce Architecture",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Engineer a cloud-native enterprise e-commerce platform using microservices, event-driven architecture, resilient fault isolation, and auto-scaling.",
        "estimated_hours": 70.0,
        "objectives": ["Microservice decomposition with gRPC & REST APIs", "Event-driven asynchronous messaging infrastructure", "Cloud deployment automation with CI/CD and monitoring"],
        "suggested_technologies": ["Java", "Python", "Docker", "Git & GitHub Actions", "Linux Administration"],
        "requirements": ["Cloud-native microservices architecture", "Automated CI/CD build pipeline", "Comprehensive chaos fault testing"],
        "skills": [{"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 5}, {"skill_name": "Docker", "importance": 5}, {"skill_name": "Git & GitHub Actions", "importance": 5}, {"skill_name": "Linux Administration", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Distributed Key-Value Database Engine",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Design and build a Raft-consensus replicated key-value storage engine with LSM-tree storage and MVCC snapshot isolation.",
        "estimated_hours": 60.0,
        "objectives": ["Implement Raft consensus leader election and log replication", "Build LSM-tree engine with MemTable and SSTable compaction", "Provide ACID multi-version concurrency control (MVCC)"],
        "suggested_technologies": ["C++", "Java", "Linux Administration"],
        "requirements": ["Partition fault tolerance via Raft", "LSM-tree background compaction", "MVCC read isolation"],
        "skills": [{"skill_name": "C++", "importance": 5}, {"skill_name": "Java", "importance": 5}, {"skill_name": "Linux Administration", "importance": 4}]
    },
    {
        "career_name": "Software Development Engineer (SDE)",
        "title": "Low-Latency Algorithmic Order Matching Engine",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Engineer an ultra-fast limit order book matching engine with LMAX Disruptor pattern and zero-allocation data structures.",
        "estimated_hours": 55.0,
        "objectives": ["Build price-time priority order matching algorithms", "Utilize ring buffers and off-heap memory for sub-microsecond latency", "Generate real-time FIX protocol market data feed"],
        "suggested_technologies": ["C++", "Java", "Python"],
        "requirements": ["Deterministic sub-microsecond match latency", "Zero garbage collection pauses during execution", "Full order audit trail"],
        "skills": [{"skill_name": "C++", "importance": 5}, {"skill_name": "Java", "importance": 5}, {"skill_name": "Python", "importance": 4}]
    },

    # =========================================================================
    # 5. AI ENGINEER (18 Projects)
    # =========================================================================
    # BASIC (5)
    {
        "career_name": "AI Engineer",
        "title": "Student Performance Predictor",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Build a machine learning regression model to predict student academic scores based on study hours, attendance, and historical performance.",
        "estimated_hours": 10.0,
        "objectives": ["Exploratory Data Analysis (EDA) and feature correlation matrix", "Train Linear Regression and Decision Tree Regressor", "Evaluate models using MSE, RMSE, and R2 score"],
        "suggested_technologies": ["Python", "Pandas", "Scikit-Learn", "Machine Learning"],
        "requirements": ["Data cleaning and feature scaling", "Model evaluation metrics report", "Clean Jupyter Notebook or script"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Pandas", "importance": 5}, {"skill_name": "Scikit-Learn", "importance": 5}, {"skill_name": "Machine Learning", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "House Price Prediction",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Develop an end-to-end house price prediction model utilizing linear regression and feature scaling techniques on tabular datasets.",
        "estimated_hours": 12.0,
        "objectives": ["Handle missing data and categorical one-hot encoding", "Feature scaling with StandardScaler / MinMaxScaler", "Train Ridge/Lasso regression with cross-validation"],
        "suggested_technologies": ["Python", "Pandas", "Scikit-Learn", "Machine Learning"],
        "requirements": ["Feature engineering pipeline", "5-Fold Cross-Validation evaluation", "Serializing model with joblib/pickle"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Pandas", "importance": 5}, {"skill_name": "Scikit-Learn", "importance": 5}, {"skill_name": "Machine Learning", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Customer Churn Predictor",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Create a binary classification model (Logistic Regression, Decision Trees) to identify customers likely to cancel subscription services.",
        "estimated_hours": 14.0,
        "objectives": ["Handle class imbalance using SMOTE or class weights", "Train Logistic Regression and Random Forest classifiers", "Evaluate Precision, Recall, F1-Score, and ROC-AUC curve"],
        "suggested_technologies": ["Python", "Pandas", "Scikit-Learn", "Machine Learning"],
        "requirements": ["Confusion matrix visualization", "ROC-AUC score >= 0.82", "Feature importance ranking chart"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Pandas", "importance": 5}, {"skill_name": "Scikit-Learn", "importance": 5}, {"skill_name": "Machine Learning", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Spam Message Classifier",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Implement a Naive Bayes / NLP text classifier to detect spam SMS and email messages using TF-IDF feature extraction.",
        "estimated_hours": 10.0,
        "objectives": ["Preprocess raw text (lowercasing, stopword removal, stemming)", "Transform text to numerical vectors using TF-IDF Vectorizer", "Train Multinomial Naive Bayes text classifier"],
        "suggested_technologies": ["Python", "Natural Language Processing (NLP)", "Scikit-Learn", "Machine Learning"],
        "requirements": ["NLP text tokenization pipeline", "Confusion matrix evaluation", "Inference CLI for custom text input"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Natural Language Processing (NLP)", "importance": 5}, {"skill_name": "Scikit-Learn", "importance": 4}, {"skill_name": "Machine Learning", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Movie Recommendation System",
        "level": "BASIC",
        "difficulty": "Basic",
        "description": "Build a content-based recommendation engine matching users with movies based on genres, overview text embeddings, and ratings.",
        "estimated_hours": 12.0,
        "objectives": ["Combine metadata attributes into TF-IDF / embedding vectors", "Compute Cosine Similarity matrix across movie dataset", "Return top-N recommended movies for any given input title"],
        "suggested_technologies": ["Python", "Pandas", "Scikit-Learn", "Machine Learning"],
        "requirements": ["Cosine similarity matrix computation", "Top 5 recommendations function", "Clean Jupyter Notebook output"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Pandas", "importance": 5}, {"skill_name": "Scikit-Learn", "importance": 4}, {"skill_name": "Machine Learning", "importance": 4}]
    },
    # INTERMEDIATE (5)
    {
        "career_name": "AI Engineer",
        "title": "Credit Risk Prediction",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Develop a financial credit scoring model using XGBoost and LightGBM to evaluate loan default risk with ROC-AUC optimization.",
        "estimated_hours": 20.0,
        "objectives": ["Feature engineering on financial credit histories", "Hyperparameter tuning via Optuna / GridSearchCV", "Model interpretation using SHAP values"],
        "suggested_technologies": ["Python", "Scikit-Learn", "Machine Learning", "Pandas"],
        "requirements": ["XGBoost / LightGBM implementation", "SHAP feature explainability plot", "ROC-AUC score >= 0.86"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Scikit-Learn", "importance": 5}, {"skill_name": "Machine Learning", "importance": 5}, {"skill_name": "Pandas", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Customer Segmentation System",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Apply unsupervised machine learning (K-Means clustering, PCA) to segment customers based on purchasing behavior and RFM analysis.",
        "estimated_hours": 18.0,
        "objectives": ["Compute Recency, Frequency, Monetary (RFM) metrics", "Dimensionality reduction using Principal Component Analysis (PCA)", "Optimum cluster detection using Elbow Method and Silhouette Score"],
        "suggested_technologies": ["Python", "Machine Learning", "Scikit-Learn", "Pandas"],
        "requirements": ["RFM score calculation", "Silhouette analysis visualization", "Cluster profiling summary report"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Machine Learning", "importance": 5}, {"skill_name": "Scikit-Learn", "importance": 4}, {"skill_name": "Pandas", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Sentiment Analysis Platform",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Build an end-to-end NLP sentiment analysis platform classifying product reviews and social media feedback using fine-tuned transformer models.",
        "estimated_hours": 22.0,
        "objectives": ["Fine-tune DistilBERT / RoBERTa model on review dataset", "Aspect-based sentiment extraction (Positive, Neutral, Negative)", "API inference wrapper for streaming text evaluation"],
        "suggested_technologies": ["Python", "Natural Language Processing (NLP)", "PyTorch", "Large Language Models (LLMs)"],
        "requirements": ["HuggingFace Transformers integration", "PyTorch fine-tuning loop", "Accuracy >= 90%"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Natural Language Processing (NLP)", "importance": 5}, {"skill_name": "PyTorch", "importance": 4}, {"skill_name": "Large Language Models (LLMs)", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Resume Skill Extraction System",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Develop a Named Entity Recognition (NER) system to parse resumes and automatically extract candidate skills, experience, and education.",
        "estimated_hours": 20.0,
        "objectives": ["Parse PDF and DOCX document formats", "Train custom spaCy NER model to extract SKILL, DEGREE, and ROLE entities", "Export structured candidate JSON profile"],
        "suggested_technologies": ["Python", "Natural Language Processing (NLP)", "Scikit-Learn"],
        "requirements": ["Document text extraction pipeline", "Custom spaCy NER entity training", "Structured JSON output validation"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Natural Language Processing (NLP)", "importance": 5}, {"skill_name": "Scikit-Learn", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Sales Forecasting System",
        "level": "INTERMEDIATE",
        "difficulty": "Intermediate",
        "description": "Construct a time-series forecasting model (Prophet, ARIMA, LSTM) to predict future store sales and inventory demand.",
        "estimated_hours": 22.0,
        "objectives": ["Decompose time series into trend, seasonality, and noise", "Train Facebook Prophet and LSTM neural networks", "Evaluate forecast accuracy using MAPE and MAE"],
        "suggested_technologies": ["Python", "Machine Learning", "Pandas", "PyTorch"],
        "requirements": ["Time-series stationarity testing", "Multi-step ahead forecast output", "MAPE score calculation"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "Machine Learning", "importance": 5}, {"skill_name": "Pandas", "importance": 4}, {"skill_name": "PyTorch", "importance": 4}]
    },
    # ADVANCED (5)
    {
        "career_name": "AI Engineer",
        "title": "Document Question Answering System",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Build an intelligent document QA pipeline using RAG (Retrieval-Augmented Generation), vector databases, and LLM text generation.",
        "estimated_hours": 32.0,
        "objectives": ["PDF document ingestion and recursive text chunking", "Generate vector embeddings and store in ChromaDB / Pinecone", "Query vector index and synthesize grounded answers with LLM"],
        "suggested_technologies": ["RAG Systems", "Vector Databases", "Large Language Models (LLMs)", "Python"],
        "requirements": ["Dense vector similarity retrieval", "Grounded source attribution quotes", "Sub-2 second query latency"],
        "skills": [{"skill_name": "RAG Systems", "importance": 5}, {"skill_name": "Vector Databases", "importance": 5}, {"skill_name": "Large Language Models (LLMs)", "importance": 5}, {"skill_name": "Python", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "AI Resume Analyzer",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Create an AI-powered resume analysis system comparing candidate resumes against job descriptions to score skill compatibility and suggest improvements.",
        "estimated_hours": 30.0,
        "objectives": ["Extract semantic embeddings for resume and job requirements", "Compute detailed gap analysis score across technical skills", "Generate specific resume enhancement suggestions via LLM"],
        "suggested_technologies": ["Large Language Models (LLMs)", "Natural Language Processing (NLP)", "Python", "RAG Systems"],
        "requirements": ["Semantic embedding match score", "Detailed skill gap classification", "Actionable LLM feedback summary"],
        "skills": [{"skill_name": "Large Language Models (LLMs)", "importance": 5}, {"skill_name": "Natural Language Processing (NLP)", "importance": 5}, {"skill_name": "Python", "importance": 4}, {"skill_name": "RAG Systems", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Image Classification Platform",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Train and deploy a Convolutional Neural Network (CNN / ResNet) for multi-class image classification with web inference API.",
        "estimated_hours": 34.0,
        "objectives": ["Fine-tune ResNet50 / EfficientNet on custom image dataset", "Apply data augmentation (rotation, flipping, color jitter)", "Deploy inference API with FastAPI and ONNX runtime"],
        "suggested_technologies": ["Deep Learning", "PyTorch", "Computer Vision", "Python"],
        "requirements": ["PyTorch / Torchvision implementation", "ONNX runtime acceleration", "Web inference endpoint"],
        "skills": [{"skill_name": "Deep Learning", "importance": 5}, {"skill_name": "PyTorch", "importance": 5}, {"skill_name": "Computer Vision", "importance": 5}, {"skill_name": "Python", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Intelligent Recommendation Engine",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Architect a hybrid recommendation system combining collaborative filtering, neural matrix factorization, and deep learning embeddings.",
        "estimated_hours": 35.0,
        "objectives": ["Build Neural Collaborative Filtering (NCF) model in PyTorch", "Combine explicit ratings with implicit user behavior signals", "Serve real-time personalized recommendations"],
        "suggested_technologies": ["Machine Learning", "Deep Learning", "PyTorch", "Python"],
        "requirements": ["Neural Matrix Factorization architecture", "Cold-start fallback handling", "Evaluation via NDCG@10 & HR@10"],
        "skills": [{"skill_name": "Machine Learning", "importance": 5}, {"skill_name": "Deep Learning", "importance": 5}, {"skill_name": "PyTorch", "importance": 5}, {"skill_name": "Python", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "AI Customer Support Assistant",
        "level": "ADVANCED",
        "difficulty": "Advanced",
        "description": "Build an automated customer support chatbot leveraging LLM function calling, conversation memory, and knowledge base integration.",
        "estimated_hours": 36.0,
        "objectives": ["Implement tool / function calling for API actions (Check Order Status, Refund)", "Manage multi-turn conversation memory window", "RAG fallback for unstructured FAQ queries"],
        "suggested_technologies": ["Large Language Models (LLMs)", "RAG Systems", "Vector Databases", "Python"],
        "requirements": ["Function calling execution accuracy", "Stateful conversation session management", "Safety guardrails against prompt injection"],
        "skills": [{"skill_name": "Large Language Models (LLMs)", "importance": 5}, {"skill_name": "RAG Systems", "importance": 5}, {"skill_name": "Vector Databases", "importance": 4}, {"skill_name": "Python", "importance": 4}]
    },
    # EXPERT (3)
    {
        "career_name": "AI Engineer",
        "title": "Production RAG Knowledge Platform",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Engineer an enterprise-grade production RAG platform featuring hybrid search (dense + sparse), reranking models, evaluation metrics, and guardrails.",
        "estimated_hours": 60.0,
        "objectives": ["Hybrid Search combining BM25 sparse vectors and dense embeddings", "Cross-Encoder reranking model optimization", "Automated RAG evaluation using Ragas framework (Faithfulness, Answer Relevance)"],
        "suggested_technologies": ["RAG Systems", "Vector Databases", "Large Language Models (LLMs)", "MLOps", "Python"],
        "requirements": ["Dense + Sparse hybrid search engine", "Cross-encoder reranker stage", "Ragas evaluation score >= 0.88"],
        "skills": [{"skill_name": "RAG Systems", "importance": 5}, {"skill_name": "Vector Databases", "importance": 5}, {"skill_name": "Large Language Models (LLMs)", "importance": 5}, {"skill_name": "MLOps", "importance": 5}, {"skill_name": "Python", "importance": 5}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Multi-Agent AI Research Assistant",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Construct an autonomous multi-agent AI system (using LangGraph/AutoGPT framework) where specialized agents collaborate to perform complex web research, code execution, and report writing.",
        "estimated_hours": 65.0,
        "objectives": ["Multi-agent state graph graph routing (Researcher, Coder, Critic, Writer)", "Autonomous web browsing and document synthesis", "Self-correcting code execution loop"],
        "suggested_technologies": ["Large Language Models (LLMs)", "RAG Systems", "Python", "MLOps"],
        "requirements": ["Multi-agent graph workflow execution", "Loop detection and cycle prevention", "Comprehensive research report generation"],
        "skills": [{"skill_name": "Large Language Models (LLMs)", "importance": 5}, {"skill_name": "RAG Systems", "importance": 5}, {"skill_name": "Python", "importance": 5}, {"skill_name": "MLOps", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "End-to-End AI Platform",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Architect and deploy a complete AI platform encompassing automated ML pipelines, continuous model monitoring, vector search infrastructure, and LLM orchestration.",
        "estimated_hours": 70.0,
        "objectives": ["End-to-end MLOps pipeline (MLflow + DVC + FastAPI)", "Real-time model data drift monitoring and automated retraining", "Scalable vector search backend with load balancing"],
        "suggested_technologies": ["MLOps", "Large Language Models (LLMs)", "RAG Systems", "Vector Databases", "PyTorch", "Python"],
        "requirements": ["Continuous model tracking & monitoring", "Automated retraining triggers", "Production cloud deployment architecture"],
        "skills": [{"skill_name": "MLOps", "importance": 5}, {"skill_name": "Large Language Models (LLMs)", "importance": 5}, {"skill_name": "RAG Systems", "importance": 5}, {"skill_name": "Vector Databases", "importance": 5}, {"skill_name": "PyTorch", "importance": 4}, {"skill_name": "Python", "importance": 5}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Multi-Modal Autonomous Agent Orchestrator",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Build an autonomous agent framework featuring ReAct reasoning loops, long-term memory, tool calling, and human-in-the-loop fallback.",
        "estimated_hours": 50.0,
        "objectives": ["Implement ReAct planning loop with self-correction", "Integrate vector database for episodic memory retrieval", "Create safe sandboxed execution environment for agent tool execution"],
        "suggested_technologies": ["Python", "FastAPI", "Docker"],
        "requirements": ["Self-healing reasoning loops", "Long-term vector memory recall", "Sandboxed execution safety"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "Docker", "importance": 4}]
    },
    {
        "career_name": "AI Engineer",
        "title": "Enterprise RAG Intelligence Engine",
        "level": "EXPERT",
        "difficulty": "Expert",
        "description": "Develop an enterprise-grade Retrieval Augmented Generation (RAG) system with hybrid dense-sparse search, reranking, and citation provenance.",
        "estimated_hours": 48.0,
        "objectives": ["Build hybrid BM25 + Vector embedding search engine", "Integrate Cohere/Cross-Encoder reranking pipeline", "Enforce strict document access control and hallucination validation"],
        "suggested_technologies": ["Python", "FastAPI", "RESTful API Design"],
        "requirements": ["Sub-second hybrid search latency", "Source document inline citations", "Hallucination score guardrail"],
        "skills": [{"skill_name": "Python", "importance": 5}, {"skill_name": "FastAPI", "importance": 5}, {"skill_name": "RESTful API Design", "importance": 4}]
    }
]


def seed_fixed_projects(db: Session):
    """
    Seeds the exact 100 projects catalog into the database.
    Deletes any legacy projects that are not in this list to ensure strict adherence.
    """
    print(f"Seeding exact 100-project catalog across 5 career tracks...")

    # Build skill lookup map
    skills = db.query(Skill).all()
    skills_map = {s.name.lower(): s for s in skills}

    valid_keys = {(p["title"], p["career_name"]) for p in FIXED_PROJECTS_CATALOG}

    # 1. Purge projects not in official catalog
    legacy_projects = db.query(Project).all()
    deleted_count = 0
    for lp in legacy_projects:
        if (lp.title, lp.career_name) not in valid_keys:
            db.delete(lp)
            deleted_count += 1
    if deleted_count > 0:
        db.commit()
        print(f" Cleaned up {deleted_count} non-catalog legacy projects.")

    inserted_count = 0
    updated_count = 0

    for prj_data in FIXED_PROJECTS_CATALOG:
        project = (
            db.query(Project)
            .filter(
                Project.title == prj_data["title"],
                Project.career_name == prj_data["career_name"],
            )
            .first()
        )
        if not project:
            project = Project(
                title=prj_data["title"],
                description=prj_data["description"],
                difficulty=prj_data["difficulty"],
                level=prj_data["level"],
                career_name=prj_data["career_name"],
                estimated_hours=prj_data["estimated_hours"],
                objectives_json=prj_data["objectives"],
                technologies_json=prj_data["suggested_technologies"],
                requirements_json=prj_data["requirements"],
            )
            db.add(project)
            db.flush()
            inserted_count += 1
        else:
            project.description = prj_data["description"]
            project.difficulty = prj_data["difficulty"]
            project.level = prj_data["level"]
            project.career_name = prj_data["career_name"]
            project.estimated_hours = prj_data["estimated_hours"]
            project.objectives_json = prj_data["objectives"]
            project.technologies_json = prj_data["suggested_technologies"]
            project.requirements_json = prj_data["requirements"]
            updated_count += 1

        # Map project skills
        for s_map in prj_data["skills"]:
            skill_name = s_map["skill_name"]
            skill_obj = skills_map.get(skill_name.lower())
            if not skill_obj:
                for sk_key, sk_val in skills_map.items():
                    if skill_name.lower() in sk_key or sk_key in skill_name.lower():
                        skill_obj = sk_val
                        break
            if not skill_obj:
                continue

            existing_ps = (
                db.query(ProjectSkill)
                .filter(
                    ProjectSkill.project_id == project.id,
                    ProjectSkill.skill_id == skill_obj.id,
                )
                .first()
            )
            if existing_ps:
                existing_ps.importance = s_map["importance"]
            else:
                ps = ProjectSkill(
                    project_id=project.id,
                    skill_id=skill_obj.id,
                    importance=s_map["importance"],
                )
                db.add(ps)

    db.commit()
    total_projects = db.query(Project).count()
    print(f" [OK] Projects Catalog seeded: {total_projects} total projects in database.")
    return total_projects


if __name__ == "__main__":
    from app.database.connection import SessionLocal
    db = SessionLocal()
    try:
        seed_fixed_projects(db)
    finally:
        db.close()
