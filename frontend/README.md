# PathPilot AI - Personalized Learning Path Recommender SaaS

> **Tagline:** "Your goal. Your skills. Your personalized path."

PathPilot AI is a production-quality, frontend prototype for an AI-powered personalized learning path recommender SaaS. It solves the issue of course overload by converting natural language career or learning goals into a prerequisite-aware, interactive roadmap of skills, courses, portfolio projects, and diagnostic assessments.

---

## 🚀 Key Features

1. **AI Goal Understanding:** Natural language processing interface that maps career goals (e.g., *"I want to become a Machine Learning Engineer"*) to industry competency benchmarks.
2. **Multi-Step Onboarding Wizard:** Interactive step-by-step onboarding for goal definition, skill assessment, proficiency tuning, and learning time preferences.
3. **AI Path Generation & Loading Animation:** Step-by-step checkmark visualizer simulating real-time graph building.
4. **Interactive Learning Path (Roadmap):** Connected multi-phase nodes graph visually representing skill dependencies, unlocked courses, projects, and assessments.
5. **Skill Gap Diagnostics & Career Analysis:** Comparative radar/bar metrics analyzing baseline readiness vs role requirements, along with career alternative matching.
6. **Adaptive Learning Engine:** Taking diagnostic assessments automatically recalculates the roadmap (e.g. scoring 82% fast-tracks statistics and unlocks Phase 3 Machine Learning).
7. **Personalized Recommendations with "Why This?" Rationale:** Every course, project, or assessment displays explicit AI rationale popups explaining why it was assigned.
8. **Context-Aware AI Assistant:** Conversational AI chat interface pre-loaded with contextual prompt suggestions, message history, copy/retry tools, and typing indicators.
9. **Progress Velocity Analytics:** 6 Recharts visualization panels tracking weekly learning hours, skill growth curves, and assessment scores.
10. **Feedback System:** Thumbs up/down feedback drawer for recommendation tuning.

---

## 🛠️ Tech Stack

- **Framework:** React.js (Vite)
- **Styling:** Tailwind CSS (v4) with custom glassmorphism design tokens & keyframe animations
- **Routing:** React Router v6
- **HTTP Client:** Axios (configured with token interceptor and mock fallback flag)
- **Iconography:** Lucide React
- **Data Visualization:** Recharts
- **State Management:** React Context API (`AppContext`) with automatic `localStorage` persistence

---

## 📂 Folder Structure

```
c:\Users\nithi\Desktop\HCL\
├── src/
│   ├── components/
│   │   ├── common/         # Reusable UI primitives (Button, Card, Badge, ProgressBar, SkillChip, WhyModal, FeedbackModal, Toast, etc.)
│   │   ├── layout/         # AppLayout, Sidebar, Topbar, LandingNavbar, LandingFooter
│   │   └── dashboard/      # GoalCard, NextActionCard, StreakWidget, ProgressOverview
│   ├── context/
│   │   └── AppContext.jsx  # Global state manager with localStorage persistence & adaptive triggers
│   ├── mock/               # Realistic mock datasets matching FastAPI schema specs
│   │   ├── mockUser.js
│   │   ├── mockSkills.js
│   │   ├── mockCareers.js
│   │   ├── mockCourses.js
│   │   ├── mockProjects.js
│   │   ├── mockRoadmap.js
│   │   ├── mockRecommendations.js
│   │   ├── mockAssessments.js
│   │   ├── mockProgress.js
│   │   └── mockChat.js
│   ├── services/           # Service layer wrapping Axios APIs with mock fallbacks
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── profileService.js
│   │   ├── skillService.js
│   │   ├── careerService.js
│   │   ├── learningPathService.js
│   │   ├── courseService.js
│   │   ├── projectService.js
│   │   ├── assessmentService.js
│   │   ├── progressService.js
│   │   ├── recommendationService.js
│   │   ├── chatService.js
│   │   └── feedbackService.js
│   ├── pages/              # 18 Application Screens
│   │   ├── LandingPage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   ├── OnboardingWizard.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── CareerAnalysisPage.jsx
│   │   ├── SkillGapPage.jsx
│   │   ├── LearningPathPage.jsx
│   │   ├── CoursesPage.jsx
│   │   ├── CourseDetailPage.jsx
│   │   ├── ProjectsPage.jsx
│   │   ├── ProjectDetailPage.jsx
│   │   ├── AssessmentsPage.jsx
│   │   ├── AssessmentTakePage.jsx
│   │   ├── ProgressPage.jsx
│   │   ├── AiAssistantPage.jsx
│   │   ├── RecommendationsPage.jsx
│   │   ├── ProfilePage.jsx
│   │   ├── SettingsPage.jsx
│   │   └── NotFoundPage.jsx
│   ├── App.jsx             # Router configuration & route declarations
│   ├── main.jsx
│   └── index.css           # Tailwind directives & CSS design system
├── package.json
├── vite.config.js
└── README.md
```

---

## 📦 How to Install and Run

1. **Clone or Open Workspace:**
   ```bash
   cd c:\Users\nithi\Desktop\HCL
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Start Development Server:**
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

4. **Build Production Bundle:**
   ```bash
   npm run build
   ```

---

## ⚡ Environment Variables & Mock Mode

The application operates in **Mock Mode** by default for standalone demo execution without a backend.

Create a `.env` file in the root directory if connecting to a live backend:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_USE_MOCK=false
```

When `VITE_USE_MOCK=false`, the service layer in `src/services/` delegates requests directly to FastAPI endpoints using Axios.

---

## 🔄 FastAPI REST Backend Integration

The service layer is structured to match the following FastAPI REST routes:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/login` | User authentication |
| `POST` | `/api/auth/register` | Account creation |
| `GET / PUT` | `/api/profile` | Learner profile fetch & update |
| `POST` | `/api/recommend/careers` | Career match analysis |
| `GET` | `/api/skill-gap/{career_id}` | Skill gap matrix |
| `POST` | `/api/learning-path/generate` | AI path generation |
| `GET` | `/api/learning-path` | Multi-phase roadmap graph |
| `GET` | `/api/courses` | Filterable courses list |
| `GET` | `/api/projects` | Filterable project list |
| `POST` | `/api/assessments/{id}/submit` | Diagnostic assessment evaluation |
| `POST` | `/api/chat` | Contextual AI chat prompt |
| `POST` | `/api/feedback` | Recommendation rating logger |

---

## 🎬 Complete Hackathon Demo Workflow

1. **Landing Page (`/`):** View SaaS Hero section, problem/solution cards, 5-step process, and click **"Build My Learning Path"**.
2. **Register/Login (`/register`):** Enter name and credentials to create session token.
3. **Onboarding Wizard (`/onboarding`):**
   - Step 1: Goal entry (*"I want to become a Machine Learning Engineer"*).
   - Step 2: Select skills (Python — Advanced, SQL — Intermediate, Statistics — Beginner).
   - Step 3: Set 10 hrs/week pace and project-based style.
   - Step 4: Summary review and click **"Generate My Personalized Path"**.
   - Step 5: Watch step-by-step AI analysis checkmarks and launch path.
4. **Dashboard (`/dashboard`):**
   - Check **72% Career Readiness** score banner.
   - View **Next Best Action** (*"Complete Classification Algorithms"* - 2 hrs).
   - Preview horizontal roadmap nodes track.
   - Click **"Why this?"** on any recommendation card to inspect AI rationale.
5. **Career Analysis & Skill Gap (`/career-analysis`, `/skill-gap`):**
   - Inspect radar chart and compare alternative career paths (Data Scientist, AI Engineer).
   - View gap table identifying Statistics as top priority gap.
6. **Interactive Roadmap (`/learning-path`):**
   - Explore 6 connected nodes. Click Phase 2 Statistics or Phase 3 Machine Learning to view syllabus items.
7. **Take Assessment & Trigger Adaptive Adaptation (`/assessments/asm-301`):**
   - Take the 5-question **Statistics Diagnostic Test**.
   - Select answers and click **"Submit & Calculate Result"**.
   - Score **82%** -> Observe real-time toast notification: *"🚀 Path Adapted! Statistics completed & Machine Learning unlocked!"*
8. **View Progress Analytics (`/progress`):**
   - Observe Recharts charts showing weekly hours velocity and score history.
9. **Conversational AI Assistant (`/ai-assistant`):**
   - Open AI Assistant and click prompt chip *"What should I learn today?"* or type custom queries.
   - Experience context-aware AI answers with copy button and typing indicator.
