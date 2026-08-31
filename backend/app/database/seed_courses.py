"""
Master Seeder for the 5 Core Career Learning Programs in PathPilot AI.
Seeds complete structured modules, lessons, videos, assessments, and final exams for:
1. Frontend Developer (frontend-developer)
2. Backend Developer (backend-developer)
3. Cybersecurity (cybersecurity)
4. Software Development Engineer (software-development-engineer)
5. AI Engineer (ai-engineer)
"""

import sys
import os

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, engine
from app.database.base import Base
from app.models.course_learning import (
    CourseTrack,
    CourseModule,
    CourseLesson,
    ModuleAssessment,
    AssessmentQuestion,
    CourseFinalAssessment,
    CourseFinalQuestion,
)


def seed_learning_courses(db: Session):
    print("Seeding 5 Comprehensive Career Learning Courses...")

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    courses_data = [
        # =========================================================================
        # 1. FRONTEND DEVELOPER
        # =========================================================================
        {
            "slug": "frontend-developer",
            "title": "Frontend Developer",
            "tagline": "Master modern, responsive, component-driven web applications from scratch to production.",
            "description": "A complete, production-grade curriculum designed to take you from web fundamentals to enterprise React, Next.js, TypeScript, state management, API integrations, and frontend testing.",
            "career_name": "Frontend Developer",
            "difficulty": "Intermediate",
            "estimated_duration": "12 Weeks",
            "total_modules": 12,
            "total_lessons": 36,
            "total_projects": 4,
            "total_assessments": 12,
            "skills_covered": ["HTML5", "CSS3", "Responsive Design", "JavaScript", "DOM", "Async JS", "REST APIs", "Git", "React", "State Management", "TypeScript", "Frontend Testing"],
            "image_url": "https://images.unsplash.com/photo-1593720213428-28a5b9e94613?auto=format&fit=crop&w=800&q=80",
            "modules": [
                {
                    "module_number": 1,
                    "phase_name": "Phase 1: Web Foundations",
                    "title": "HTML5 & Semantic Markup",
                    "description": "Understand modern HTML structure, accessible document outlines, forms, validation, and SEO best practices.",
                    "skills": ["HTML5", "Semantic HTML", "Web Accessibility", "SEO"],
                    "estimated_hours": 4.0,
                    "lessons": [
                        {
                            "lesson_number": 1,
                            "title": "Document Structure & Semantic Elements",
                            "description": "Learn the role of semantic tags (header, nav, main, article, section, footer) in building accessible web applications.",
                            "video_url": "https://www.youtube.com/embed/kUMe1FH4CHE",
                            "video_duration": "18 min",
                            "content": "### Semantic HTML5 Foundations\n\nSemantic HTML introduces meaning to the web page rather than just presentation. Tags such as `<header>`, `<nav>`, `<article>`, and `<footer>` clearly describe their purpose to browsers, screen readers, and search engine crawlers.\n\n#### Why Semantics Matter\n1. **Accessibility (a11y):** Screen readers use semantic regions to navigate quickly.\n2. **SEO Optimization:** Search engines prioritize content properly wrapped in `<main>` and `<article>` tags.\n3. **Maintainability:** Cleaner code architecture for developer teams.",
                            "key_concepts": ["DOCTYPE declaration", "Semantic landmarks (header, nav, main)", "ARIA attributes basics", "Document outline algorithm"],
                            "code_snippet": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\" />\n  <title>Accessible Document</title>\n</head>\n<body>\n  <header>\n    <nav aria-label=\"Main Navigation\">\n      <a href=\"/\">Home</a>\n    </nav>\n  </header>\n  <main>\n    <article>\n      <h1>Semantic Article Title</h1>\n      <p>Content goes here...</p>\n    </article>\n  </main>\n  <footer>\n    <p>&copy; 2026 PathPilot AI</p>\n  </footer>\n</body>\n</html>",
                            "code_language": "html",
                            "resources": [{"title": "MDN Web Docs: HTML Semantic Elements", "url": "https://developer.mozilla.org/en-US/docs/Glossary/Semantics#semantics_in_html", "type": "Documentation"}]
                        },
                        {
                            "lesson_number": 2,
                            "title": "Forms, Input Types & Native Validation",
                            "description": "Master robust forms, modern HTML5 input types, constraint validation attributes, and user input feedback.",
                            "video_url": "https://www.youtube.com/embed/fNcJuPIZ2WE",
                            "video_duration": "22 min",
                            "content": "### Form Architecture & Native Validation\n\nForms are the primary interactive touchpoint between users and web applications. HTML5 provides built-in validation rules using attributes like `required`, `pattern`, `minlength`, `type='email'`, and `type='number'`.\n\n#### Best Practices\n- Always link `<label for=\"id\">` with `<input id=\"id\">` for accessibility.\n- Use `autocomplete` attributes to boost mobile usability.",
                            "key_concepts": ["Form submission lifecycle", "Input types (email, tel, date, number)", "Pattern regex constraints", "Accessible fieldsets and legends"],
                            "code_snippet": "<form action=\"/api/submit\" method=\"POST\">\n  <div class=\"form-group\">\n    <label for=\"userEmail\">Work Email</label>\n    <input type=\"email\" id=\"userEmail\" name=\"email\" required placeholder=\"you@company.com\" />\n  </div>\n  <button type=\"submit\">Register</button>\n</form>",
                            "code_language": "html"
                        },
                        {
                            "lesson_number": 3,
                            "title": "Web Accessibility (WCAG 2.2) & SEO Fundamentals",
                            "description": "Implement accessible landmarks, color contrast standards, image alt strategies, and SEO meta tags.",
                            "video_url": "https://www.youtube.com/embed/20SHvU2PKsM",
                            "video_duration": "20 min",
                            "content": "### Web Accessibility & SEO\n\nBuilding an inclusive web application requires adhering to the Web Content Accessibility Guidelines (WCAG). Ensuring color contrast ratios of at least 4.5:1, keyboard navigability, and descriptive `alt` tags creates better experiences for every user.",
                            "key_concepts": ["WCAG AA compliance standards", "Keyboard focus management (`tabindex`)", "OpenGraph and meta tags", "Color contrast evaluation"],
                            "code_snippet": "<!-- Meta tags for social SEO -->\n<meta property=\"og:title\" content=\"PathPilot AI Course\" />\n<meta property=\"og:description\" content=\"Interactive Career Roadmap\" />\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />",
                            "code_language": "html"
                        }
                    ],
                    "assessment": {
                        "title": "Module 1 Assessment: HTML5 & Accessibility",
                        "description": "Test your grasp of semantic landmarks, form validation, and WCAG accessibility standards.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Which HTML5 element represents the central, unique content of the document body?",
                                "options": ["<section>", "<main>", "<article>", "<content>"],
                                "correct_index": 1,
                                "explanation": "The <main> tag represents the dominant content of the <body> of a document."
                            },
                            {
                                "question_text": "Why should every form <input> be paired with a corresponding <label> element?",
                                "options": [
                                    "It automatically enables CSS grid formatting.",
                                    "It improves accessibility by allowing screen readers to announce the field's purpose and increases clickable hit target.",
                                    "It makes form submissions asynchronous by default.",
                                    "It is required by JavaScript to bind onChange events."
                                ],
                                "correct_index": 1,
                                "explanation": "Labels provide programmatic name association for assistive technologies and expand clickable area."
                            },
                            {
                                "question_text": "Which attribute enforces that an input must be filled out before submitting a native form?",
                                "options": ["mandatory=\"true\"", "validate=\"required\"", "required", "checked"],
                                "correct_index": 2,
                                "explanation": "The boolean attribute 'required' triggers native browser validation before form dispatch."
                            }
                        ]
                    }
                },
                {
                    "module_number": 2,
                    "phase_name": "Phase 1: Web Foundations",
                    "title": "CSS3 Styling, Flexbox & Grid",
                    "description": "Master the CSS Box Model, specificity, CSS custom properties, and modern layout engines (Flexbox & CSS Grid).",
                    "skills": ["CSS3", "Flexbox", "CSS Grid", "Box Model"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 4,
                            "title": "The Box Model, Specificity & Custom Properties",
                            "description": "Learn box-sizing: border-box, CSS cascade, specificity weight calculations, and reusable CSS variables.",
                            "video_url": "https://www.youtube.com/embed/rIO5326FgPE",
                            "video_duration": "24 min",
                            "content": "### Deep Dive into the CSS Box Model\n\nEvery element on a webpage is rendered as a rectangular box consisting of four layers: **Content**, **Padding**, **Border**, and **Margin**.\n\nUsing `box-sizing: border-box` ensures that width and height values include padding and borders, avoiding unexpected layout overflows.",
                            "key_concepts": ["box-sizing: border-box", "Margin collapsing", "Specificity formula (Inline > ID > Class > Element)", "CSS variables (`--primary-color`)"],
                            "code_snippet": ":root {\n  --primary: #4f9cf9;\n  --bg-dark: #043873;\n}\n\n* {\n  box-sizing: border-box;\n  margin: 0;\n  padding: 0;\n}\n\n.card {\n  background-color: var(--primary);\n  padding: 1.5rem;\n  border-radius: 1rem;\n}",
                            "code_language": "css"
                        },
                        {
                            "lesson_number": 5,
                            "title": "Flexbox for 1-Dimensional Dynamic Layouts",
                            "description": "Align, distribute, and order elements along primary and cross axes using modern Flexbox properties.",
                            "video_url": "https://www.youtube.com/embed/fYq5PXgSsbE",
                            "video_duration": "25 min",
                            "content": "### Mastering Flexbox Layouts\n\nFlexbox provides efficient distribution of space among items in a container, even when their size is unknown or dynamic.\n\n#### Key Properties\n- `justify-content`: controls alignment along the main axis.\n- `align-items`: controls alignment along the cross axis.\n- `flex: 1 1 auto`: shorthand for grow, shrink, and basis.",
                            "key_concepts": ["Main axis vs cross axis", "justify-content vs align-items", "flex-wrap and gap", "flex-grow and flex-shrink"],
                            "code_snippet": ".navbar {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: 1rem 2rem;\n  gap: 1.5rem;\n}",
                            "code_language": "css"
                        },
                        {
                            "lesson_number": 6,
                            "title": "CSS Grid for 2-Dimensional Layouts",
                            "description": "Design complex 2D magazine-style layouts using grid templates, grid areas, and auto-fit columns.",
                            "video_url": "https://www.youtube.com/embed/9zBsdydE1TU",
                            "video_duration": "28 min",
                            "content": "### CSS Grid Layout Mastery\n\nCSS Grid is the most powerful 2-dimensional layout system available in web browsers. It allows you to define rows and columns simultaneously.",
                            "key_concepts": ["grid-template-columns (`repeat(auto-fit, minmax(280px, 1fr))`", "grid-gap", "grid-template-areas", "Implicit vs explicit grid tracks"],
                            "code_snippet": ".dashboard-grid {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));\n  gap: 1.5rem;\n}",
                            "code_language": "css"
                        }
                    ],
                    "assessment": {
                        "title": "Module 2 Assessment: CSS Layouts & Architecture",
                        "description": "Demonstrate your understanding of Flexbox, CSS Grid, and box model behavior.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the primary effect of applying `box-sizing: border-box` to an element?",
                                "options": [
                                    "It removes all margins automatically.",
                                    "Width and height calculations include padding and borders within the specified dimensions.",
                                    "It forces the element to display as flex container.",
                                    "It prevents text from wrapping onto multiple lines."
                                ],
                                "correct_index": 1,
                                "explanation": "border-box ensures padding and borders do not expand an element beyond its defined width."
                            },
                            {
                                "question_text": "Which CSS Grid expression creates a responsive auto-wrapping column layout without media queries?",
                                "options": [
                                    "grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));",
                                    "grid-columns: flex(100%, 250px);",
                                    "display: grid-auto-wrap;",
                                    "grid-template: 1fr 1fr 1fr;"
                                ],
                                "correct_index": 0,
                                "explanation": "repeat(auto-fit, minmax(250px, 1fr)) dynamically packs columns based on available container width."
                            },
                            {
                                "question_text": "In Flexbox, which property aligns items along the cross axis (perpendicular to main axis)?",
                                "options": ["justify-content", "align-items", "flex-direction", "place-content"],
                                "correct_index": 1,
                                "explanation": "align-items aligns flex items along the cross axis."
                            }
                        ]
                    }
                },
                {
                    "module_number": 3,
                    "phase_name": "Phase 1: Web Foundations",
                    "title": "Responsive Design & Tailwind CSS",
                    "description": "Build mobile-first, fluid interfaces with media queries, container queries, and utility-first Tailwind CSS.",
                    "skills": ["Responsive Design", "Tailwind CSS", "Mobile-First", "Container Queries"],
                    "estimated_hours": 4.5,
                    "lessons": [
                        {
                            "lesson_number": 7,
                            "title": "Mobile-First Philosophy & Breakpoint Strategies",
                            "description": "Adopt min-width media queries, fluid typography with clamp(), and responsive viewport rules.",
                            "video_url": "https://www.youtube.com/embed/srvUrASNj0s",
                            "video_duration": "20 min",
                            "content": "### Mobile-First Design\n\nMobile-first design involves designing the mobile interface first and then adding styles for larger viewports using `min-width` media queries. This results in cleaner CSS and faster mobile performance.",
                            "key_concepts": ["min-width vs max-width breakpoints", "Fluid typography with clamp()", "Viewport meta tag configuration", "Touch target minimum sizing (48x48px)"],
                            "code_snippet": "/* Mobile-first base styles */\n.hero-title {\n  font-size: clamp(1.5rem, 4vw, 3.5rem);\n}\n\n@media (min-width: 768px) {\n  .container {\n    max-width: 720px;\n    margin: 0 auto;\n  }\n}",
                            "code_language": "css"
                        },
                        {
                            "lesson_number": 8,
                            "title": "Tailwind CSS Core Utilities & Design System",
                            "description": "Learn utility-first styling: spacing scales, typography, flexbox/grid classes, and color palettes.",
                            "video_url": "https://www.youtube.com/embed/ft30zcMlFao",
                            "video_duration": "30 min",
                            "content": "### Tailwind CSS in Modern Production\n\nTailwind CSS offers composable utility classes right inside markup, eliminating CSS name-wrangling and enforcing consistent design scales.",
                            "key_concepts": ["Utility-first paradigm", "Arbitrary values & theme configuration", "Responsive prefixes (`md:`, `lg:`)", "Hover & focus state variants"],
                            "code_snippet": "<div class=\"p-6 max-w-sm mx-auto bg-white rounded-2xl shadow-xl flex items-center gap-x-4 border border-slate-100\">\n  <div class=\"shrink-0\">\n    <div class=\"h-12 w-12 bg-blue-500 rounded-xl flex items-center justify-center text-white font-bold\">AI</div>\n  </div>\n  <div>\n    <div class=\"text-lg font-bold text-slate-900\">PathPilot AI</div>\n    <p class=\"text-xs text-slate-500\">Personalized Learning Path</p>\n  </div>\n</div>",
                            "code_language": "html"
                        }
                    ],
                    "assessment": {
                        "title": "Module 3 Assessment: Responsive Web & Tailwind",
                        "description": "Assess your capability in building mobile-first responsive layouts with Tailwind CSS.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "In mobile-first design, what type of CSS media query is primarily used?",
                                "options": ["@media (max-width: ...)", "@media (min-width: ...)", "@media (orientation: portrait)", "@media (resolution: 2dppx)"],
                                "correct_index": 1,
                                "explanation": "Mobile-first establishes base styles without queries, then progressively enhances using min-width."
                            },
                            {
                                "question_text": "In Tailwind CSS, what does the class `md:flex` mean?",
                                "options": [
                                    "Apply display: flex only on screens narrower than medium width.",
                                    "Apply display: flex on screen widths at or above the medium (768px) breakpoint.",
                                    "Apply flex layout to Markdown elements only.",
                                    "Align items in the middle."
                                ],
                                "correct_index": 1,
                                "explanation": "The 'md:' prefix targets the medium breakpoint (typically min-width: 768px) and above."
                            }
                        ]
                    }
                },
                {
                    "module_number": 4,
                    "phase_name": "Phase 2: JavaScript Mastery",
                    "title": "JavaScript Fundamentals & ES6+",
                    "description": "Master data types, scope, closures, array methods (map, filter, reduce), destructuring, and modern ES modules.",
                    "skills": ["JavaScript", "ES6+", "Scope & Closures", "Array Methods"],
                    "estimated_hours": 6.0,
                    "lessons": [
                        {
                            "lesson_number": 9,
                            "title": "Variables, Data Types & Scope Chains",
                            "description": "Understand let, const vs var, primitive vs reference types, execution context, and lexical closures.",
                            "video_url": "https://www.youtube.com/embed/W6NZfCO5SIk",
                            "video_duration": "32 min",
                            "content": "### JavaScript Execution Context & Closures\n\nJavaScript is a single-threaded, non-blocking synchronous runtime. Understanding the call stack, lexical environment, and closures allows you to build robust stateful functions without polluting global scope.",
                            "key_concepts": ["Block scope vs function scope", "Temporal Dead Zone (TDZ)", "Primitive vs object memory references", "Lexical scoping & closure patterns"],
                            "code_snippet": "function createCounter(initialValue = 0) {\n  let count = initialValue;\n  return {\n    increment: () => ++count,\n    decrement: () => --count,\n    getCount: () => count,\n  };\n}\n\nconst counter = createCounter(10);\nconsole.log(counter.increment()); // 11",
                            "code_language": "javascript"
                        },
                        {
                            "lesson_number": 10,
                            "title": "Modern ES6+ Features & Functional Array Methods",
                            "description": "Master map, filter, reduce, destructuring, spread/rest operators, and nullish coalescing.",
                            "video_url": "https://www.youtube.com/embed/R8rmfD9Y5-c",
                            "video_duration": "28 min",
                            "content": "### Functional JavaScript Data Transformations\n\nModern JavaScript emphasizes immutable data handling. Methods like `map`, `filter`, and `reduce` allow clean declarative transformations over complex collections.",
                            "key_concepts": ["Array.prototype.map / filter / reduce", "Object and array destructuring with defaults", "Rest parameters & spread syntax", "Optional chaining (`?.`) and nullish coalescing (`??`)"],
                            "code_snippet": "const courses = [\n  { id: 1, name: 'Frontend', hours: 40, isFree: true },\n  { id: 2, name: 'Backend', hours: 55, isFree: false },\n  { id: 3, name: 'AI', hours: 60, isFree: true },\n];\n\nconst totalFreeHours = courses\n  .filter(c => c.isFree)\n  .reduce((sum, c) => sum + c.hours, 0);\n\nconsole.log(`Total free course hours: ${totalFreeHours}`); // 100",
                            "code_language": "javascript"
                        }
                    ],
                    "assessment": {
                        "title": "Module 4 Assessment: JavaScript ES6+ Core",
                        "description": "Evaluate your understanding of scope, closures, and immutable array transformations.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What value will `console.log(user?.profile?.name ?? 'Guest')` output if user.profile is null?",
                                "options": ["undefined", "null", "'Guest'", "TypeError"],
                                "correct_index": 2,
                                "explanation": "Optional chaining returns undefined when evaluating null, and nullish coalescing (??) falls back to 'Guest'."
                            },
                            {
                                "question_text": "Which array method transforms an array of items into a single accumulated output value?",
                                "options": ["Array.prototype.map", "Array.prototype.forEach", "Array.prototype.reduce", "Array.prototype.filter"],
                                "correct_index": 2,
                                "explanation": "reduce iterates over elements to accumulate state into a single output object/number."
                            }
                        ]
                    }
                },
                {
                    "module_number": 5,
                    "phase_name": "Phase 2: JavaScript Mastery",
                    "title": "DOM Manipulation & Browser Events",
                    "description": "Manipulate DOM nodes, handle event propagation (bubbling vs capturing), and implement event delegation.",
                    "skills": ["DOM Manipulation", "Event Handling", "Browser APIs"],
                    "estimated_hours": 4.0,
                    "lessons": [
                        {
                            "lesson_number": 11,
                            "title": "Querying and Manipulating the DOM Tree",
                            "description": "Learn querySelector, createElement, classList manipulation, and dataset attributes.",
                            "video_url": "https://www.youtube.com/embed/y17RuWkWdn8",
                            "video_duration": "25 min",
                            "content": "### Direct DOM Interaction\n\nThe Document Object Model (DOM) is an object-oriented representation of the web page. Interacting with the DOM allows dynamic UI updates in response to user actions.",
                            "key_concepts": ["querySelector vs querySelectorAll", "classList.toggle / add / remove", "DocumentFragment for batch DOM insertion", "dataset attributes"],
                            "code_snippet": "const btn = document.querySelector('#actionBtn');\nbtn.addEventListener('click', () => {\n  document.body.classList.toggle('dark-mode');\n});",
                            "code_language": "javascript"
                        }
                    ],
                    "assessment": {
                        "title": "Module 5 Assessment: DOM & Events",
                        "description": "Test event bubbling, delegation, and DOM manipulation principles.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Why is Event Delegation preferred when handling clicks on dynamically generated list items?",
                                "options": [
                                    "It attaches one listener to a parent container instead of hundreds of listeners to child nodes.",
                                    "It forces synchronous execution in the main thread.",
                                    "It bypasses the event loop entirely.",
                                    "It eliminates the need for HTML buttons."
                                ],
                                "correct_index": 0,
                                "explanation": "Event delegation leverages event bubbling to handle events at a common parent, saving memory."
                            }
                        ]
                    }
                },
                {
                    "module_number": 6,
                    "phase_name": "Phase 2: JavaScript Mastery",
                    "title": "Asynchronous JavaScript & REST APIs",
                    "description": "Master Promises, async/await, Fetch API, Axios, HTTP verbs, status codes, and robust error handling.",
                    "skills": ["Async JavaScript", "Promises", "Fetch API", "REST APIs"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 12,
                            "title": "Promises, Async/Await & The Event Loop",
                            "description": "Understand microtasks, macrotasks, Promise chaining, and async/await syntax.",
                            "video_url": "https://www.youtube.com/embed/vn3tm0quoqE",
                            "video_duration": "30 min",
                            "content": "### Asynchronous Flow Control\n\nJavaScript handles concurrency through the Event Loop, utilizing a call stack, Web APIs, Macrotask Queue, and Microtask Queue (Promises).",
                            "key_concepts": ["Event loop architecture", "Promise states (pending, fulfilled, rejected)", "async/await error handling with try/catch", "Promise.all and Promise.allSettled"],
                            "code_snippet": "async function fetchCourseDetails(courseId) {\n  try {\n    const response = await fetch(`/api/courses/${courseId}`);\n    if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);\n    const data = await response.json();\n    return data;\n  } catch (err) {\n    console.error('Failed to load course:', err.message);\n    throw err;\n  }\n}",
                            "code_language": "javascript"
                        }
                    ],
                    "assessment": {
                        "title": "Module 6 Assessment: Async JavaScript & APIs",
                        "description": "Validate your knowledge on Promises, async/await, and REST API error handling.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Which Promise combinator waits for all promises to settle (whether resolved or rejected) and returns an array of outcome objects?",
                                "options": ["Promise.race()", "Promise.any()", "Promise.all()", "Promise.allSettled()"],
                                "correct_index": 3,
                                "explanation": "Promise.allSettled() returns an array with status ('fulfilled' or 'rejected') for every promise."
                            }
                        ]
                    }
                },
                {
                    "module_number": 7,
                    "phase_name": "Phase 3: React & Modern Frontend",
                    "title": "Git & Collaborative Version Control",
                    "description": "Master branching, pull requests, merge conflict resolution, rebase, and GitHub Actions CI/CD workflows.",
                    "skills": ["Git", "GitHub", "Version Control", "CI/CD"],
                    "estimated_hours": 3.5,
                    "lessons": [
                        {
                            "lesson_number": 13,
                            "title": "Git Branching, Rebasing & Conflict Resolution",
                            "description": "Learn professional git workflows, interactive rebasing, stashing, and collaborative pull requests.",
                            "video_url": "https://www.youtube.com/embed/RGOj5yH7evk",
                            "video_duration": "22 min",
                            "content": "### Professional Git Workflows\n\nGit is the industry-standard distributed version control system. Professional developers rely on feature branching, descriptive commits, and pull requests with code reviews.",
                            "key_concepts": ["git checkout -b feature-branch", "git rebase vs git merge", "git stash save & pop", "GitHub Pull Request reviews"],
                            "code_snippet": "git checkout -b feature/course-player\ngit add .\ngit commit -m \"feat: implement interactive video player controls\"\ngit push origin feature/course-player",
                            "code_language": "bash"
                        }
                    ],
                    "assessment": {
                        "title": "Module 7 Assessment: Git & Version Control",
                        "description": "Check your understanding of branching, merging, and git commands.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the primary difference between `git merge` and `git rebase`?",
                                "options": [
                                    "Rebase rewrites commit history on top of another branch for a linear log, while merge preserves exact branch timestamps and creates a merge commit.",
                                    "Rebase deletes the remote repository.",
                                    "Merge can only be used on GitHub web interface.",
                                    "Rebase permanently disables git tags."
                                ],
                                "correct_index": 0,
                                "explanation": "Rebase replays commits onto the tip of the base branch creating a clean linear history."
                            }
                        ]
                    }
                },
                {
                    "module_number": 8,
                    "phase_name": "Phase 3: React & Modern Frontend",
                    "title": "React Fundamentals & JSX Architecture",
                    "description": "Build declarative user interfaces using components, props, state, JSX syntax, and conditional rendering.",
                    "skills": ["React", "JSX", "Component Architecture", "Props & State"],
                    "estimated_hours": 6.0,
                    "lessons": [
                        {
                            "lesson_number": 14,
                            "title": "Components, JSX Syntax & Props Validation",
                            "description": "Understand JSX compilation, component composition, immutable props, and pure functions.",
                            "video_url": "https://www.youtube.com/embed/bMknfKXIFA8",
                            "video_duration": "35 min",
                            "content": "### React Component Model\n\nReact lets you build user interfaces out of individual pieces called components. React components receive inputs called `props` and return JSX describing what should appear on screen.",
                            "key_concepts": ["Virtual DOM reconciliation", "Component purity & immutability", "Unidirectional data flow", "Conditional rendering techniques"],
                            "code_snippet": "export function CourseCard({ title, progress, onContinue }) {\n  return (\n    <div className=\"p-4 rounded-2xl bg-white border border-slate-200 shadow-sm\">\n      <h3 className=\"text-lg font-bold text-slate-800\">{title}</h3>\n      <p className=\"text-xs text-slate-500 mt-1\">Progress: {progress}%</p>\n      <button onClick={onContinue} className=\"mt-3 px-4 py-2 bg-blue-500 text-white rounded-xl text-xs font-bold\">\n        Continue Learning\n      </button>\n    </div>\n  );\n}",
                            "code_language": "javascript"
                        }
                    ],
                    "assessment": {
                        "title": "Module 8 Assessment: React Fundamentals",
                        "description": "Demonstrate understanding of React component hierarchy, props, and JSX rendering.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Why must React component props be treated as strictly read-only?",
                                "options": [
                                    "Because JavaScript objects are always frozen by default.",
                                    "To uphold unidirectional data flow and guarantee predictable, pure rendering cycles.",
                                    "Because browsers disallow object property mutation.",
                                    "Props are stored on disk and cannot be altered in RAM."
                                ],
                                "correct_index": 1,
                                "explanation": "Props are passed down from parent to child and must never be mutated by the receiving child component."
                            }
                        ]
                    }
                },
                {
                    "module_number": 9,
                    "phase_name": "Phase 3: React & Modern Frontend",
                    "title": "React Hooks & Lifecycle Management",
                    "description": "Master useState, useEffect, useRef, useMemo, useCallback, and building custom reusable hooks.",
                    "skills": ["React Hooks", "useState", "useEffect", "Custom Hooks"],
                    "estimated_hours": 6.5,
                    "lessons": [
                        {
                            "lesson_number": 15,
                            "title": "useState, useEffect & Cleanup Subscriptions",
                            "description": "Learn state update batching, dependency arrays, timer cleanup, and async effects.",
                            "video_url": "https://www.youtube.com/embed/0ZJgIjIuY7U",
                            "video_duration": "38 min",
                            "content": "### Mastering React Hooks\n\nHooks let you use state and other React features without writing class components. The `useEffect` hook enables side-effects such as data fetching, subscriptions, and manual DOM mutations.",
                            "key_concepts": ["State setter callback form `setVal(prev => prev + 1)`", "useEffect dependency array rules", "Cleanup functions to prevent memory leaks", "Custom Hook extraction patterns"],
                            "code_snippet": "import { useState, useEffect } from 'react';\n\nexport function useOnlineStatus() {\n  const [isOnline, setIsOnline] = useState(navigator.onLine);\n\n  useEffect(() => {\n    const handleOnline = () => setIsOnline(true);\n    const handleOffline = () => setIsOnline(false);\n    window.addEventListener('online', handleOnline);\n    window.addEventListener('offline', handleOffline);\n    return () => {\n      window.removeEventListener('online', handleOnline);\n      window.removeEventListener('offline', handleOffline);\n    };\n  }, []);\n\n  return isOnline;\n}",
                            "code_language": "javascript"
                        }
                    ],
                    "assessment": {
                        "title": "Module 9 Assessment: React Hooks",
                        "description": "Test your mastery over hook dependency arrays, custom hooks, and state lifecycles.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "When does the cleanup function returned inside a `useEffect` callback execute?",
                                "options": [
                                    "Only when the browser window is closed.",
                                    "Before the component re-runs the effect on dependency change, and when the component unmounts.",
                                    "Immediately before the component's initial render.",
                                    "Whenever `setState` is called in any parent component."
                                ],
                                "correct_index": 1,
                                "explanation": "Cleanup functions run prior to re-executing the effect with new dependencies and when unmounting."
                            }
                        ]
                    }
                },
                {
                    "module_number": 10,
                    "phase_name": "Phase 3: React & Modern Frontend",
                    "title": "State Management & React Context",
                    "description": "Architect scalable global application state using React Context, reducers, and modern state stores.",
                    "skills": ["Context API", "State Management", "useReducer", "Global State"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 16,
                            "title": "Context API & useReducer for Scalable App State",
                            "description": "Avoid prop drilling by creating centralized context providers with structured dispatch actions.",
                            "video_url": "https://www.youtube.com/embed/5LrDIWkK_Bc",
                            "video_duration": "28 min",
                            "content": "### Global State Architecture\n\nThe React Context API allows passing data through the component tree without manually threading props at every level. Pairing Context with `useReducer` delivers predictable Redux-like action flows.",
                            "key_concepts": ["createContext and useContext hook", "Reducer state transitions `(state, action) => newState`", "Context selector performance optimizations", "Separating state and dispatch contexts"],
                            "code_snippet": "const CourseContext = createContext(null);\n\nexport function CourseProvider({ children }) {\n  const [activeCourse, setActiveCourse] = useState(null);\n  return (\n    <CourseContext.Provider value={{ activeCourse, setActiveCourse }}>\n      {children}\n    </CourseContext.Provider>\n  );\n}",
                            "code_language": "javascript"
                        }
                    ],
                    "assessment": {
                        "title": "Module 10 Assessment: State Management",
                        "description": "Evaluate your architectural decisions regarding Context, reducers, and state co-location.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What problem does React Context primarily solve?",
                                "options": [
                                    "It compiles JavaScript into WebAssembly.",
                                    "It solves 'prop drilling' by sharing values across deeply nested components without passing props manually.",
                                    "It automatically caches HTTP responses on disk.",
                                    "It speeds up CSS rendering."
                                ],
                                "correct_index": 1,
                                "explanation": "Context eliminates prop drilling by establishing an ambient provider scope."
                            }
                        ]
                    }
                },
                {
                    "module_number": 11,
                    "phase_name": "Phase 4: Advanced Engineering & Production",
                    "title": "TypeScript for React Applications",
                    "description": "Type props, state, event handlers, generics, API response schemas, and utility types in React.",
                    "skills": ["TypeScript", "Type Safety", "Generics", "React with TypeScript"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 17,
                            "title": "Typing Components, Props & Event Handlers",
                            "description": "Learn interface vs type, React.FC vs plain functions, typing onClick and onChange events.",
                            "video_url": "https://www.youtube.com/embed/zQnBQ4tB3ZA",
                            "video_duration": "30 min",
                            "content": "### Type-Safe React Development\n\nTypeScript provides compile-time type checking, auto-completion, and refactoring confidence for large frontend codebases.",
                            "key_concepts": ["Interfaces vs Type aliases", "Typing React.MouseEvent and React.ChangeEvent", "Generic component props", "Utility types (Partial, Pick, Omit, Record)"],
                            "code_snippet": "interface LessonProps {\n  id: number;\n  title: string;\n  isCompleted: boolean;\n  onComplete: (lessonId: number) => Promise<void>;\n}\n\nexport function LessonItem({ id, title, isCompleted, onComplete }: LessonProps) {\n  return (\n    <div className=\"flex items-center justify-between p-3 border rounded-xl\">\n      <span>{title}</span>\n      <button onClick={() => onComplete(id)} disabled={isCompleted}>\n        {isCompleted ? 'Done' : 'Mark Complete'}\n      </button>\n    </div>\n  );\n}",
                            "code_language": "typescript"
                        }
                    ],
                    "assessment": {
                        "title": "Module 11 Assessment: TypeScript in React",
                        "description": "Verify your understanding of type inference, generics, and interface contracts.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Which TypeScript utility type constructs a type with all properties of T set to optional?",
                                "options": ["Required<T>", "Partial<T>", "Readonly<T>", "Record<K, T>"],
                                "correct_index": 1,
                                "explanation": "Partial<T> makes all properties in T optional (property?: type)."
                            }
                        ]
                    }
                },
                {
                    "module_number": 12,
                    "phase_name": "Phase 4: Advanced Engineering & Production",
                    "title": "Frontend Testing & Final Capstone Project",
                    "description": "Write unit and component integration tests with Vitest / React Testing Library and build your capstone portfolio app.",
                    "skills": ["Frontend Testing", "Vitest", "Testing Library", "Production Deployment"],
                    "estimated_hours": 7.0,
                    "lessons": [
                        {
                            "lesson_number": 18,
                            "title": "Unit & Integration Testing with Vitest and React Testing Library",
                            "description": "Learn user-centric test queries (getByRole, getByText), mocking API calls, and assertions.",
                            "video_url": "https://www.youtube.com/embed/8Xwq35cPwYg",
                            "video_duration": "28 min",
                            "content": "### Testing Modern React Applications\n\nReact Testing Library encourages writing tests that resemble how users interact with your software rather than testing internal implementation details.",
                            "key_concepts": ["render, screen, and userEvent", "Query priorities (getByRole > getByLabelText > getByText)", "Mocking Axios and Fetch with Vitest vi.fn()", "Accessibility testing queries"],
                            "code_snippet": "import { render, screen } from '@testing-library/react';\nimport userEvent from '@testing-library/user-event';\nimport { LessonItem } from './LessonItem';\n\ntest('calls onComplete when mark complete button is clicked', async () => {\n  const onCompleteMock = vi.fn();\n  render(<LessonItem id={1} title=\"Intro to HTML\" isCompleted={false} onComplete={onCompleteMock} />);\n  \n  const button = screen.getByRole('button', { name: /mark complete/i });\n  await userEvent.click(button);\n  \n  expect(onCompleteMock).toHaveBeenCalledWith(1);\n});",
                            "code_language": "typescript"
                        }
                    ],
                    "assessment": {
                        "title": "Module 12 Assessment: Testing & Deployment",
                        "description": "Validate testing principles and production deployment readiness.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the recommended query priority in React Testing Library for finding interactive buttons?",
                                "options": ["screen.getByTestId()", "screen.getByRole('button', { name: ... })", "document.querySelector('button')", "screen.getByClassName()"],
                                "correct_index": 1,
                                "explanation": "getByRole reflects the accessibility tree and closely mimics how assistive technology and users interact."
                            }
                        ]
                    }
                }
            ],
            "final_assessment": {
                "title": "Frontend Developer Comprehensive Final Exam",
                "description": "A thorough 10-question comprehensive exam evaluating your mastery across HTML5, CSS3, JavaScript, Async APIs, React, State, TypeScript, and Testing.",
                "time_minutes": 45,
                "passing_score": 70.0,
                "questions": [
                    {
                        "question_text": "Which HTML tag is specifically designed to contain independent, self-contained syndicatable content?",
                        "options": ["<article>", "<section>", "<div>", "<aside>"],
                        "correct_index": 0,
                        "topic": "HTML5",
                        "explanation": "<article> is defined for self-contained compositions like blog posts or news items."
                    },
                    {
                        "question_text": "In CSS Grid, how do you specify that grid items should automatically fill the row and maintain at least 200px width?",
                        "options": ["grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));", "grid-columns: fill-available 200px;", "display: auto-grid(200px);", "columns: auto 200px;"],
                        "correct_index": 0,
                        "topic": "CSS3",
                        "explanation": "repeat(auto-fill, minmax(200px, 1fr)) dynamically sizes and wraps grid tracks."
                    },
                    {
                        "question_text": "What is the return value of `typeof null` in JavaScript?",
                        "options": ["'null'", "'undefined'", "'object'", "'boolean'"],
                        "correct_index": 2,
                        "topic": "JavaScript",
                        "explanation": "Due to a historical bug preserved for compatibility, typeof null evaluates to 'object'."
                    },
                    {
                        "question_text": "Which event loop phase executes resolved Promise callbacks?",
                        "options": ["Macrotask Queue", "Microtask Queue", "Timer Queue", "I/O Poll Phase"],
                        "correct_index": 1,
                        "topic": "Async JS",
                        "explanation": "Promises resolve into the Microtask Queue which runs immediately after the current call stack."
                    },
                    {
                        "question_text": "What does React's `useCallback` hook memoize?",
                        "options": ["A computed calculation value", "A callback function instance between re-renders", "A DOM node reference", "A Redux action dispatch"],
                        "correct_index": 1,
                        "topic": "React Hooks",
                        "explanation": "useCallback caches a function definition between renders until its dependencies change."
                    },
                    {
                        "question_text": "In TypeScript, what is the key distinction between an `interface` and a `type` alias regarding declaration merging?",
                        "options": [
                            "Multiple interfaces with the same name automatically merge, whereas type aliases cannot be reopened.",
                            "Interfaces cannot describe objects.",
                            "Type aliases are always compiled to runtime functions.",
                            "Interfaces only work in class components."
                        ],
                        "correct_index": 0,
                        "topic": "TypeScript",
                        "explanation": "Declaration merging allows multiple interface declarations with the same identifier to merge their fields."
                    },
                    {
                        "question_text": "When using React Testing Library, why should `getByTestId` be used only as a last resort?",
                        "options": [
                            "Because test IDs slow down test execution by 10x.",
                            "Because test IDs test implementation details rather than user-accessible attributes and roles.",
                            "Test IDs are stripped out by Babel.",
                            "Test IDs cannot be used in TypeScript."
                        ],
                        "correct_index": 1,
                        "topic": "Testing",
                        "explanation": "User-centric queries (getByRole, getByText) test the actual accessible UI rather than private data attributes."
                    }
                ]
            }
        },

        # =========================================================================
        # 2. BACKEND DEVELOPER
        # =========================================================================
        {
            "slug": "backend-developer",
            "title": "Backend Developer",
            "tagline": "Architect high-performance, secure, scalable server-side systems, RESTful APIs, and relational database layers.",
            "description": "Master server-side architecture, HTTP protocols, Python FastAPI & Node.js, database modeling in MySQL & PostgreSQL, authentication with JWT & bcrypt, Redis caching, and containerized deployment with Docker.",
            "career_name": "Backend Developer",
            "difficulty": "Intermediate",
            "estimated_duration": "12 Weeks",
            "total_modules": 12,
            "total_lessons": 36,
            "total_projects": 4,
            "total_assessments": 12,
            "skills_covered": ["Python", "FastAPI", "RESTful API Design", "SQL", "MySQL", "PostgreSQL", "Database Modeling", "Authentication & JWT", "Redis Caching", "Docker", "API Security (OWASP)", "Backend Testing"],
            "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80",
            "modules": [
                {
                    "module_number": 1,
                    "phase_name": "Phase 1: Backend Foundations",
                    "title": "Backend Fundamentals, HTTP & REST Architecture",
                    "description": "Understand request/response lifecycles, HTTP methods, headers, status codes, and idempotent REST principles.",
                    "skills": ["RESTful API Design", "HTTP Protocols", "API Architecture"],
                    "estimated_hours": 4.0,
                    "lessons": [
                        {
                            "lesson_number": 1,
                            "title": "The HTTP Protocol & Request Lifecycle",
                            "description": "Master TCP/IP handshake, HTTP/1.1 vs HTTP/2, headers, query parameters, path variables, and body payloads.",
                            "video_url": "https://www.youtube.com/embed/iYM2zFP3Zn0",
                            "video_duration": "24 min",
                            "content": "### The Anatomy of an HTTP Request\n\nEvery backend transaction begins with an HTTP client request and server response. Designing clean RESTful APIs requires understanding HTTP methods:\n- **GET**: Safe and idempotent retrieval.\n- **POST**: Non-idempotent resource creation.\n- **PUT**: Idempotent complete replacement.\n- **PATCH**: Partial resource update.\n- **DELETE**: Resource removal.",
                            "key_concepts": ["HTTP status code ranges (2xx, 3xx, 4xx, 5xx)", "Idempotency in API design", "Headers (Authorization, Content-Type, CORS)", "Stateless client-server architecture"],
                            "code_snippet": "GET /api/v1/courses/frontend-developer HTTP/1.1\nHost: api.pathpilot.ai\nAuthorization: Bearer <jwt-token>\nAccept: application/json",
                            "code_language": "http"
                        }
                    ],
                    "assessment": {
                        "title": "Module 1 Assessment: HTTP & REST",
                        "description": "Test understanding of REST principles and HTTP status codes.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Which HTTP status code should be returned when a resource is successfully created via POST?",
                                "options": ["200 OK", "201 Created", "204 No Content", "202 Accepted"],
                                "correct_index": 1,
                                "explanation": "201 Created signifies that the request succeeded and a new resource was created."
                            }
                        ]
                    }
                },
                {
                    "module_number": 2,
                    "phase_name": "Phase 1: Backend Foundations",
                    "title": "Python for Backend & Asynchronous I/O",
                    "description": "Learn Python type hints, Pydantic validation models, asyncio event loop, and asynchronous coroutines.",
                    "skills": ["Python", "Asyncio", "Pydantic"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 2,
                            "title": "Asyncio, Coroutines & Non-Blocking I/O",
                            "description": "Understand async/await in Python, event loops, CPU-bound vs I/O-bound concurrency, and thread pools.",
                            "video_url": "https://www.youtube.com/embed/t5Bo1Je9EmE",
                            "video_duration": "26 min",
                            "content": "### Asynchronous Programming in Python\n\nFastAPI leverages Python's `asyncio` framework to handle thousands of concurrent I/O-bound requests on a single worker thread.",
                            "key_concepts": ["async def vs def in web routes", "await asyncio.gather()", "Threadpool execution for blocking libraries", "Pydantic BaseModel schema validation"],
                            "code_snippet": "from pydantic import BaseModel, EmailStr\n\nclass UserCreateSchema(BaseModel):\n    name: str\n    email: EmailStr\n    password: str",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 2 Assessment: Python Async & Schemas",
                        "description": "Test Python typing, asyncio, and Pydantic validation.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What does Pydantic do when incoming request data violates declared type hints?",
                                "options": [
                                    "It silently ignores the faulty field.",
                                    "It converts invalid types to None automatically.",
                                    "It raises a ValidationError that FastAPI transforms into an HTTP 422 Unprocessable Entity response.",
                                    "It restarts the Uvicorn server."
                                ],
                                "correct_index": 2,
                                "explanation": "Pydantic raises ValidationError which FastAPI handles with status code 422."
                            }
                        ]
                    }
                },
                {
                    "module_number": 3,
                    "phase_name": "Phase 1: Backend Foundations",
                    "title": "FastAPI Web Framework & Dependency Injection",
                    "description": "Build high-performance REST APIs with FastAPI, routing, response models, and Depends() injection.",
                    "skills": ["FastAPI", "Dependency Injection", "API Routing"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 3,
                            "title": "FastAPI Dependency Injection & APIRouter Architecture",
                            "description": "Organize large backends using APIRouter, dependency injection for DB sessions, and security auth guards.",
                            "video_url": "https://www.youtube.com/embed/gQTRsZpqjAw",
                            "video_duration": "30 min",
                            "content": "### Dependency Injection System\n\nFastAPI's `Depends` system manages resource lifecycles cleanly (such as database sessions), ensuring transactions close properly upon request completion.",
                            "key_concepts": ["FastAPI Depends() pattern", "APIRouter modular prefixing", "Auto-generated OpenAPI Swagger docs at /docs", "Exception handlers & middleware"],
                            "code_snippet": "from fastapi import APIRouter, Depends\nfrom sqlalchemy.orm import Session\nfrom app.database.session import get_db\n\nrouter = APIRouter(prefix=\"/api/courses\")\n\n@router.get(\"/{course_id}\")\ndef get_course(course_id: int, db: Session = Depends(get_db)):\n    return db.query(Course).filter(Course.id == course_id).first()",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 3 Assessment: FastAPI & Dependency Injection",
                        "description": "Assess FastAPI route declarations, middleware, and dependency management.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "How does FastAPI generate interactive Swagger documentation?",
                                "options": [
                                    "Developers must write separate OpenAPI YAML files manually.",
                                    "FastAPI automatically extracts types, schemas, and routes from Python type hints and Pydantic models at runtime.",
                                    "Through a background Docker container.",
                                    "By parsing Git commit messages."
                                ],
                                "correct_index": 1,
                                "explanation": "FastAPI builds OpenAPI JSON specs directly from Python type annotations."
                            }
                        ]
                    }
                },
                {
                    "module_number": 4,
                    "phase_name": "Phase 2: Database Engineering",
                    "title": "Relational Database Modeling & SQL Mastery",
                    "description": "Design normalized 3NF schemas, foreign keys, composite indexes, transactions (ACID), and complex joins.",
                    "skills": ["SQL", "MySQL", "Database Modeling", "ACID Transactions"],
                    "estimated_hours": 6.0,
                    "lessons": [
                        {
                            "lesson_number": 4,
                            "title": "Schema Normalization, Indexing & Query Execution Plans",
                            "description": "Learn 1NF to 3NF, B-Tree indexes, EXPLAIN query analysis, and transaction isolation levels.",
                            "video_url": "https://www.youtube.com/embed/HXV3zeRR3h4",
                            "video_duration": "32 min",
                            "content": "### Relational Database Design & Index Strategies\n\nA well-designed schema enforces data integrity through foreign keys and unique constraints. Indexing frequently queried columns reduces table scans to efficient B-Tree lookups.",
                            "key_concepts": ["Primary Keys, Foreign Keys & Cascade Deletes", "B-Tree vs Hash Indexing", "ACID guarantees (Atomicity, Consistency, Isolation, Durability)", "EXPLAIN query performance diagnostics"],
                            "code_snippet": "CREATE TABLE user_course_progress (\n  id INT AUTO_INCREMENT PRIMARY KEY,\n  user_id INT NOT NULL,\n  course_id INT NOT NULL,\n  progress_percentage FLOAT DEFAULT 0.0,\n  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,\n  INDEX idx_user_course (user_id, course_id)\n);",
                            "code_language": "sql"
                        }
                    ],
                    "assessment": {
                        "title": "Module 4 Assessment: Relational DB & SQL",
                        "description": "Evaluate database normalization, index strategies, and ACID properties.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What does the 'Atomicity' property in ACID database transactions guarantee?",
                                "options": [
                                    "Queries execute at atomic speeds.",
                                    "All operations in a transaction succeed completely, or all are rolled back with no partial states.",
                                    "The database encrypts table keys atomically.",
                                    "Only one user can connect at a time."
                                ],
                                "correct_index": 1,
                                "explanation": "Atomicity ensures 'all-or-nothing' execution for database operations."
                            }
                        ]
                    }
                },
                {
                    "module_number": 5,
                    "phase_name": "Phase 2: Database Engineering",
                    "title": "SQLAlchemy ORM & Migration Pipelines (Alembic)",
                    "description": "Map Python classes to relational tables, manage session lifecycles, handle lazy vs eager loading, and execute Alembic migrations.",
                    "skills": ["SQLAlchemy", "ORM", "Alembic", "Database Migrations"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 5,
                            "title": "SQLAlchemy Models, joinedload & Alembic Migrations",
                            "description": "Prevent N+1 query bottlenecks using joinedload, manage relationships, and track schema versioning.",
                            "video_url": "https://www.youtube.com/embed/5YvyXGk7xGg",
                            "video_duration": "28 min",
                            "content": "### Object Relational Mapping (ORM) Mastery\n\nSQLAlchemy acts as a bridge between Python OOP and SQL tables. Using `joinedload` eliminates N+1 query performance traps by issuing SQL JOINs in a single query.",
                            "key_concepts": ["Base declarative class", "relationship() with back_populates and cascade", "Eager loading (joinedload, selectinload) vs lazy loading", "alembic revision --autogenerate and upgrade head"],
                            "code_snippet": "from sqlalchemy.orm import joinedload\n\n# Eagerly loads modules and lessons in a single database round-trip\ncourse = (\n    db.query(CourseTrack)\n    .options(joinedload(CourseTrack.modules).joinedload(CourseModule.lessons))\n    .filter(CourseTrack.slug == 'frontend-developer')\n    .first()\n)",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 5 Assessment: SQLAlchemy & Migrations",
                        "description": "Check knowledge of ORM query optimization and Alembic version control.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the N+1 query problem in ORMs and how is it resolved in SQLAlchemy?",
                                "options": [
                                    "It is a memory leak caused by querying N tables; resolved by restarting the server.",
                                    "Executing 1 query for a parent and N individual queries for each child; resolved using joinedload() or selectinload().",
                                    "A syntax error in WHERE clauses.",
                                    "A limit on database connections."
                                ],
                                "correct_index": 1,
                                "explanation": "joinedload issues a SQL JOIN to fetch parent and child entities in one query."
                            }
                        ]
                    }
                },
                {
                    "module_number": 6,
                    "phase_name": "Phase 2: Database Engineering",
                    "title": "Authentication, JWT Tokens & Password Hashing",
                    "description": "Implement bcrypt password hashing, stateless JSON Web Tokens (JWT), expiry strategies, and role-based access control.",
                    "skills": ["Authentication & JWT", "Bcrypt Hashing", "Security Best Practices"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 6,
                            "title": "Secure Password Hashing with Bcrypt & JWT Issuance",
                            "description": "Learn salt generation, bcrypt hash verification, HS256/RS256 JWT signing, and Bearer token extraction.",
                            "video_url": "https://www.youtube.com/embed/6nzyO5Q_a_E",
                            "video_duration": "30 min",
                            "content": "### Modern Authentication Architecture\n\nPasswords must never be stored in plaintext. Bcrypt applies a cryptographic salt and slow hashing algorithm resistant to brute-force attacks. After login, the server issues a signed JWT token encapsulating user identity.",
                            "key_concepts": ["bcrypt.hashpw and bcrypt.checkpw", "JWT claims (sub, exp, iat)", "HTTPBearer dependency extraction", "Token expiration & refresh token flow"],
                            "code_snippet": "import jwt\nfrom datetime import datetime, timedelta, timezone\n\ndef create_access_token(user_id: int, secret_key: str) -> str:\n    payload = {\n        \"sub\": str(user_id),\n        \"exp\": datetime.now(timezone.utc) + timedelta(minutes=60),\n        \"iat\": datetime.now(timezone.utc),\n    }\n    return jwt.encode(payload, secret_key, algorithm=\"HS256\")",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 6 Assessment: Auth & JWT Security",
                        "description": "Test understanding of password security and token verification.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Why should sensitive data like passwords or credit cards never be placed in a JWT payload?",
                                "options": [
                                    "Because JWT payloads are only Base64Url-encoded and can be trivially decoded and read by anyone with the token.",
                                    "Because JWTs cannot store strings.",
                                    "Because JWTs expire in 1 second.",
                                    "Because browsers delete encrypted payloads."
                                ],
                                "correct_index": 0,
                                "explanation": "JWTs are signed, not encrypted. Anyone can decode the payload."
                            }
                        ]
                    }
                },
                {
                    "module_number": 7,
                    "phase_name": "Phase 3: Performance & Security",
                    "title": "Redis In-Memory Caching & Rate Limiting",
                    "description": "Implement high-speed caching with Redis, cache invalidation strategies (TTL, write-through), and API rate limiting.",
                    "skills": ["Redis Caching", "Rate Limiting", "Performance Tuning"],
                    "estimated_hours": 4.5,
                    "lessons": [
                        {
                            "lesson_number": 7,
                            "title": "Redis Key-Value Caching & Invalidation Patterns",
                            "description": "Learn SETEX with TTL, caching expensive DB queries, cache stampede prevention, and Redis client setup.",
                            "video_url": "https://www.youtube.com/embed/jgpVdJB2sKQ",
                            "video_duration": "24 min",
                            "content": "### In-Memory Caching with Redis\n\nRedis delivers sub-millisecond data retrieval. Storing frequently accessed catalog and course roadmap data in Redis dramatically reduces database workload.",
                            "key_concepts": ["Cache-aside pattern", "Time-To-Live (TTL) expiration", "Cache stampede mitigation", "Token bucket rate limiting"],
                            "code_snippet": "import json\n\ndef get_cached_course(course_id: int, redis_client, db):\n    cache_key = f\"course:{course_id}\"\n    cached = redis_client.get(cache_key)\n    if cached:\n        return json.loads(cached)\n    \n    course = db.query(CourseTrack).filter(CourseTrack.id == course_id).first()\n    if course:\n        redis_client.setex(cache_key, 3600, json.dumps(course.to_dict()))\n    return course",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 7 Assessment: Redis Caching",
                        "description": "Validate caching concepts and TTL invalidation.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "In the Cache-Aside pattern, what happens when a cache miss occurs?",
                                "options": [
                                    "An error is returned to the user.",
                                    "The application queries the database, writes the result into cache with a TTL, and returns the data.",
                                    "The cache deletes all other keys.",
                                    "The database shuts down."
                                ],
                                "correct_index": 1,
                                "explanation": "On cache miss, data is read from primary DB, stored in cache, and returned."
                            }
                        ]
                    }
                },
                {
                    "module_number": 8,
                    "phase_name": "Phase 3: Performance & Security",
                    "title": "Web Application Security (OWASP Top 10)",
                    "description": "Defend against SQL injection, Cross-Site Scripting (XSS), CSRF, Server-Side Request Forgery (SSRF), and CORS misconfigurations.",
                    "skills": ["API Security (OWASP)", "SQLi Mitigation", "CORS Configuration"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 8,
                            "title": "Mitigating OWASP Vulnerabilities in Modern APIs",
                            "description": "Learn parameterized queries, content security policies, CORS origin whitelisting, and input sanitization.",
                            "video_url": "https://www.youtube.com/embed/F-G9jFkXhVE",
                            "video_duration": "28 min",
                            "content": "### Hardening Web Backend APIs\n\nSecurity must be designed into every backend endpoint. Utilizing parameterized queries eliminates SQL injection, while explicit CORS middleware prevents unauthorized cross-origin requests.",
                            "key_concepts": ["Parameterized SQL queries", "CORS allow_origins whitelisting", "Rate limiting to prevent brute force", "Secure HTTP headers (HSTS, X-Content-Type-Options)"],
                            "code_snippet": "from fastapi.middleware.cors import CORSMiddleware\n\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=[\"http://localhost:5173\"],\n    allow_credentials=True,\n    allow_methods=[\"*\"],\n    allow_headers=[\"*\"],\n)",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 8 Assessment: Backend Security",
                        "description": "Test understanding of OWASP Top 10 defenses.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Why are parameterized SQL queries immune to SQL Injection attacks?",
                                "options": [
                                    "Because they compile user parameters strictly as literal values rather than executable SQL syntax.",
                                    "Because they convert user input into Base64.",
                                    "Because they only run on HTTPS.",
                                    "Because parameters are verified by anti-virus."
                                ],
                                "correct_index": 0,
                                "explanation": "Parameters are treated as data literals, preventing malicious SQL command injection."
                            }
                        ]
                    }
                },
                {
                    "module_number": 9,
                    "phase_name": "Phase 3: Performance & Security",
                    "title": "Automated Testing & Pytest Suites",
                    "description": "Write unit tests, database mock fixtures, and integration tests using Pytest and FastAPI TestClient.",
                    "skills": ["Backend Testing", "Pytest", "TestClient"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 9,
                            "title": "Integration Testing with Pytest and TestClient",
                            "description": "Create test fixtures, clean up test databases, and simulate authenticated endpoint calls.",
                            "video_url": "https://www.youtube.com/embed/NbcBaaeVf0s",
                            "video_duration": "25 min",
                            "content": "### Automated Backend Testing\n\nFastAPI includes integration with Starlette's `TestClient`, allowing rapid testing of request pipelines, validation schemas, and database transactions in isolated test environments.",
                            "key_concepts": ["pytest fixtures with yield", "TestClient(app)", "Testing HTTP status codes and JSON payloads", "Mocking external services"],
                            "code_snippet": "from fastapi.testclient import TestClient\nfrom app.main import app\n\nclient = TestClient(app)\n\ndef test_health_check():\n    response = client.get(\"/api/health\")\n    assert response.status_code == 200\n    assert response.json()[\"status\"] == \"ok\"",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 9 Assessment: Testing with Pytest",
                        "description": "Assess automated testing and test isolation principles.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the purpose of a Pytest fixture in test suites?",
                                "options": [
                                    "To compile Python files into C binaries.",
                                    "To provide reproducible setup and teardown contexts (like test database sessions) for test functions.",
                                    "To format code automatically.",
                                    "To disable error reporting."
                                ],
                                "correct_index": 1,
                                "explanation": "Fixtures define reusable baseline environments and cleanup actions for tests."
                            }
                        ]
                    }
                },
                {
                    "module_number": 10,
                    "phase_name": "Phase 4: Deployment & Microservices",
                    "title": "Containerization with Docker & Docker Compose",
                    "description": "Write multi-stage Dockerfiles, configure Docker Compose for multi-container apps (FastAPI + MySQL + Redis), and manage volumes.",
                    "skills": ["Docker", "Docker Compose", "Containerization"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 10,
                            "title": "Building Production Docker Containers",
                            "description": "Learn multi-stage builds, Alpine/Slim base images, environment variable injection, and compose networking.",
                            "video_url": "https://www.youtube.com/embed/gAkwW2tuIqE",
                            "video_duration": "30 min",
                            "content": "### Docker for Backend Developers\n\nDocker packages applications with all system dependencies, ensuring consistent behavior across local development, testing, and production servers.",
                            "key_concepts": ["Dockerfile instructions (FROM, WORKDIR, COPY, RUN, CMD)", "Docker Compose service networking", "Named volumes for database persistence", ".dockerignore best practices"],
                            "code_snippet": "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]",
                            "code_language": "dockerfile"
                        }
                    ],
                    "assessment": {
                        "title": "Module 10 Assessment: Docker Containerization",
                        "description": "Test understanding of Docker images, layers, and Compose services.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Why are multi-stage Docker builds recommended for production deployments?",
                                "options": [
                                    "They reduce final image size by discarding build tools and intermediate artifacts.",
                                    "They enable multiple operating systems simultaneously.",
                                    "They allow containers to run without Docker daemon.",
                                    "They make Python run without an interpreter."
                                ],
                                "correct_index": 0,
                                "explanation": "Multi-stage builds leave compiler tools in build stages, producing compact production images."
                            }
                        ]
                    }
                },
                {
                    "module_number": 11,
                    "phase_name": "Phase 4: Deployment & Microservices",
                    "title": "CI/CD Pipelines & Cloud Deployment",
                    "description": "Automate linting, testing, Docker image building, and automated deployment to cloud hosts with GitHub Actions.",
                    "skills": ["CI/CD", "GitHub Actions", "Cloud Deployment"],
                    "estimated_hours": 4.5,
                    "lessons": [
                        {
                            "lesson_number": 11,
                            "title": "Continuous Integration with GitHub Actions",
                            "description": "Set up automated test runners, environment secrets, and automated container registry publishing.",
                            "video_url": "https://www.youtube.com/embed/eB0nUzAI7M8",
                            "video_duration": "24 min",
                            "content": "### Automated Delivery Workflows\n\nCI/CD pipelines automate testing and deployment every time code is pushed to the repository, eliminating manual deployment errors.",
                            "key_concepts": ["GitHub Actions workflows (.github/workflows/ci.yml)", "Encrypted repository secrets", "Matrix testing across Python versions", "Automated deployment triggers"],
                            "code_snippet": "name: Backend CI\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with: { python-version: '3.11' }\n      - run: pip install -r requirements.txt\n      - run: pytest",
                            "code_language": "yaml"
                        }
                    ],
                    "assessment": {
                        "title": "Module 11 Assessment: CI/CD Workflows",
                        "description": "Assess knowledge of automated testing pipelines and cloud deployment.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the primary benefit of running automated tests in a CI pipeline on every pull request?",
                                "options": [
                                    "It catches bugs, regressions, and broken schemas before code merges into production.",
                                    "It automatically writes documentation.",
                                    "It speeds up CPU execution by 50%.",
                                    "It encrypts git commit hashes."
                                ],
                                "correct_index": 0,
                                "explanation": "Continuous Integration catches regressions before code reaches staging or production."
                            }
                        ]
                    }
                },
                {
                    "module_number": 12,
                    "phase_name": "Phase 4: Deployment & Microservices",
                    "title": "Capstone Backend Service Project",
                    "description": "Design, build, and deploy a complete production-grade, secure backend API service with full test coverage.",
                    "skills": ["Backend Architecture", "Production Readiness", "System Design"],
                    "estimated_hours": 8.0,
                    "lessons": [
                        {
                            "lesson_number": 12,
                            "title": "Building & Deploying the Production Capstone API",
                            "description": "Integrate auth, databases, redis caching, rate limiting, and automated test suites into a unified service.",
                            "video_url": "https://www.youtube.com/embed/0sOvCWFmrtA",
                            "video_duration": "35 min",
                            "content": "### Capstone Production Project\n\nBring together everything you've learned to build a resilient, scalable backend service that meets enterprise engineering standards.",
                            "key_concepts": ["Production logging & structured error outputs", "Health check endpoints (/api/health)", "Database connection pooling", "Security audits & performance benchmarks"],
                            "code_snippet": "@app.get(\"/api/health\")\ndef health():\n    return {\"status\": \"ok\", \"database\": \"connected\", \"version\": \"1.0.0\"}",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 12 Assessment: Production Backend Mastery",
                        "description": "Evaluate full backend lifecycle readiness.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Why should database connection pools be configured rather than opening a new DB connection for each request?",
                                "options": [
                                    "Opening connections has high TCP/authentication latency; pooling reuses existing connections for high throughput.",
                                    "Because MySQL disallows more than 1 connection.",
                                    "Connection pools encrypt hard drives.",
                                    "Pooling reduces Python memory to zero."
                                ],
                                "correct_index": 0,
                                "explanation": "Connection pools eliminate TCP connection overhead by reusing warm connections."
                            }
                        ]
                    }
                }
            ],
            "final_assessment": {
                "title": "Backend Developer Comprehensive Final Exam",
                "description": "Comprehensive 10-question evaluation covering HTTP, REST, Python async, SQL, SQLAlchemy, Auth/JWT, Caching, Docker, and Security.",
                "time_minutes": 45,
                "passing_score": 70.0,
                "questions": [
                    {
                        "question_text": "Which HTTP method is idempotent and used to replace an entire resource entity?",
                        "options": ["POST", "PUT", "PATCH", "CONNECT"],
                        "correct_index": 1,
                        "topic": "HTTP",
                        "explanation": "PUT is defined in HTTP specs as idempotent complete resource replacement."
                    },
                    {
                        "question_text": "In relational databases, what does a foreign key with `ON DELETE CASCADE` ensure?",
                        "options": [
                            "Deleting the parent row automatically deletes all associated child rows.",
                            "The database refuses to delete the parent row.",
                            "The database deletes all tables in the schema.",
                            "Child rows have their keys set to NULL."
                        ],
                        "correct_index": 0,
                        "topic": "Databases",
                        "explanation": "ON DELETE CASCADE removes orphaned child records when their parent record is deleted."
                    },
                    {
                        "question_text": "What type of cryptographic algorithm is bcrypt?",
                        "options": ["Symmetric encryption", "Asymmetric key exchange", "Key derivation password hashing function", "Compression algorithm"],
                        "correct_index": 2,
                        "topic": "Security",
                        "explanation": "Bcrypt is an adaptive one-way cryptographic password hashing algorithm."
                    },
                    {
                        "question_text": "What is the primary function of Redis TTL (Time-To-Live)?",
                        "options": [
                            "To automatically evict and delete cached keys after a set duration to prevent stale data.",
                            "To compress files on disk.",
                            "To measure network ping.",
                            "To restart Docker containers."
                        ],
                        "correct_index": 0,
                        "topic": "Redis",
                        "explanation": "TTL defines an expiration time in seconds after which Redis automatically removes the key."
                    },
                    {
                        "question_text": "In Docker Compose, what mechanism ensures that database files survive container restarts?",
                        "options": ["Environment variables", "Named Volumes", "Port mapping", "Docker network bridge"],
                        "correct_index": 1,
                        "topic": "Docker",
                        "explanation": "Volumes persist data outside the container's ephemeral writable layer."
                    }
                ]
            }
        },

        # =========================================================================
        # 3. CYBERSECURITY
        # =========================================================================
        {
            "slug": "cybersecurity",
            "title": "Cybersecurity",
            "tagline": "Protect digital infrastructure, master ethical hacking, defensive security, threat monitoring, and incident response.",
            "description": "An intensive professional path in network security, Linux hardening, cryptographic algorithms, vulnerability assessment, SIEM threat hunting, and modern DevSecOps.",
            "career_name": "Cybersecurity",
            "difficulty": "Intermediate",
            "estimated_duration": "12 Weeks",
            "total_modules": 12,
            "total_lessons": 36,
            "total_projects": 4,
            "total_assessments": 12,
            "skills_covered": ["Network Security", "Linux Administration", "Cryptography", "Web Application Security (OWASP)", "Penetration Testing", "SIEM & Threat Detection", "Vulnerability Assessment", "Incident Response"],
            "image_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80",
            "modules": [
                {
                    "module_number": 1,
                    "phase_name": "Phase 1: Security Foundations & Networking",
                    "title": "Cybersecurity Principles & The CIA Triad",
                    "description": "Understand Confidentiality, Integrity, Availability, threat modeling, defense-in-depth, and security governance.",
                    "skills": ["Cybersecurity", "CIA Triad", "Threat Modeling"],
                    "estimated_hours": 4.0,
                    "lessons": [
                        {
                            "lesson_number": 1,
                            "title": "The CIA Triad & Core Security Principles",
                            "description": "Explore Confidentiality (encryption), Integrity (hashing), and Availability (resilience & DDoS mitigation).",
                            "video_url": "https://www.youtube.com/embed/inWWhr5tnEA",
                            "video_duration": "22 min",
                            "content": "### The CIA Triad: Core Pillar of Information Security\n\nAll cybersecurity defenses map back to three core principles:\n1. **Confidentiality:** Ensuring sensitive data is accessible only to authorized entities.\n2. **Integrity:** Guaranteeing data has not been altered or tampered with in transit or at rest.\n3. **Availability:** Ensuring computing systems and services remain operational and accessible.",
                            "key_concepts": ["Confidentiality vs Integrity vs Availability", "Defense in Depth architecture", "Principle of Least Privilege (PoLP)", "Authentication vs Authorization"],
                            "code_snippet": "# Example calculating SHA-256 hash to verify file integrity\nimport hashlib\n\ndef verify_file_integrity(filepath: str, expected_hash: str) -> bool:\n    sha256 = hashlib.sha256()\n    with open(filepath, 'rb') as f:\n        while chunk := f.read(8192):\n            sha256.update(chunk)\n    return sha256.hexdigest() == expected_hash",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 1 Assessment: CIA Triad & Security Principles",
                        "description": "Test fundamental security concepts, least privilege, and threat models.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Which principle of the CIA triad is violated when an attacker modifies bank account balances in a database?",
                                "options": ["Confidentiality", "Integrity", "Availability", "Non-repudiation"],
                                "correct_index": 1,
                                "explanation": "Integrity guarantees data is accurate, complete, and untampered."
                            }
                        ]
                    }
                },
                {
                    "module_number": 2,
                    "phase_name": "Phase 1: Security Foundations & Networking",
                    "title": "Networking Protocols & Packet Analysis",
                    "description": "Analyze TCP/IP, OSI model, DNS, DHCP, ARP, and inspect live packet traffic using Wireshark.",
                    "skills": ["Network Security", "Wireshark", "TCP/IP"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 2,
                            "title": "TCP/IP Protocol Stack & Wireshark Packet Inspection",
                            "description": "Understand 3-way handshake (SYN, SYN-ACK, ACK), port scanning, and packet dissection in Wireshark.",
                            "video_url": "https://www.youtube.com/embed/qpnACuD6dGg",
                            "video_duration": "28 min",
                            "content": "### Deep Packet Inspection\n\nAnalyzing network traffic reveals packet headers, source/destination IPs, flags, and payload anomalies. Capturing traffic with Wireshark is fundamental for detecting port scans and unencrypted credentials.",
                            "key_concepts": ["OSI 7-layer model vs TCP/IP 4-layer model", "TCP 3-way handshake and tear down", "DNS resolution & DNS poisoning", "Wireshark capture and display filters (`ip.addr == ...`)"],
                            "code_snippet": "# Wireshark display filter for detecting HTTP POST requests\nhttp.request.method == \"POST\" and ip.src == 192.168.1.100",
                            "code_language": "bash"
                        }
                    ],
                    "assessment": {
                        "title": "Module 2 Assessment: Networking & Packet Analysis",
                        "description": "Evaluate knowledge of TCP/IP handshakes and packet dissection.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the correct sequence of flags in a TCP 3-way handshake?",
                                "options": ["ACK -> SYN -> SYN-ACK", "SYN -> SYN-ACK -> ACK", "FIN -> ACK -> RST", "SYN -> ACK -> FIN"],
                                "correct_index": 1,
                                "explanation": "The client sends SYN, the server replies with SYN-ACK, and the client confirms with ACK."
                            }
                        ]
                    }
                },
                {
                    "module_number": 3,
                    "phase_name": "Phase 1: Security Foundations & Networking",
                    "title": "Linux Security & System Hardening",
                    "description": "Master file permissions, sudoers configuration, SSH hardening, iptables / UFW firewall rules, and process monitoring.",
                    "skills": ["Linux Administration", "System Hardening", "Firewalls"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 3,
                            "title": "Hardening Linux Servers & SSH Best Practices",
                            "description": "Configure public key authentication, disable root login, set chmod/chown permissions, and configure UFW firewall.",
                            "video_url": "https://www.youtube.com/embed/a6n3b5yD3iI",
                            "video_duration": "26 min",
                            "content": "### Linux System Hardening\n\nLinux is the foundation of cloud infrastructure. Hardening a server involves disabling password authentication in favor of Ed25519 SSH keys, configuring strict firewall rules, and auditing running services.",
                            "key_concepts": ["chmod octal permissions (e.g. 600, 755)", "SSH hardening (`PermitRootLogin no`, `PasswordAuthentication no`)", "UFW firewall configuration (`ufw allow 443/tcp`)", "Log inspection with /var/log/auth.log and journalctl"],
                            "code_snippet": "# SSH Hardening in /etc/ssh/sshd_config\nPermitRootLogin no\nPasswordAuthentication no\nPubkeyAuthentication yes\nPort 2222",
                            "code_language": "bash"
                        }
                    ],
                    "assessment": {
                        "title": "Module 3 Assessment: Linux Hardening",
                        "description": "Check mastery of Linux permissions, firewalls, and SSH security.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Which chmod permission code gives read/write access strictly to the owner and zero permissions to group and others?",
                                "options": ["chmod 755", "chmod 600", "chmod 644", "chmod 777"],
                                "correct_index": 1,
                                "explanation": "chmod 600 sets rw------- (4+2=6 for owner, 0 for group, 0 for others)."
                            }
                        ]
                    }
                },
                {
                    "module_number": 4,
                    "phase_name": "Phase 2: Cryptography & Application Security",
                    "title": "Cryptography Fundamentals & PKI",
                    "description": "Learn symmetric encryption (AES-256), asymmetric encryption (RSA/ECC), hashing, digital signatures, and TLS certificates.",
                    "skills": ["Cryptography", "PKI & Certificates", "Encryption"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 4,
                            "title": "Symmetric vs Asymmetric Encryption & TLS 1.3",
                            "description": "Understand AES-GCM, RSA key pairs, Diffie-Hellman key exchange, Certificate Authorities (CA), and TLS handshakes.",
                            "video_url": "https://www.youtube.com/embed/jhXCTbFnK8o",
                            "video_duration": "30 min",
                            "content": "### Cryptographic Foundations\n\nCryptography provides confidentiality and authentication across untrusted networks. Modern TLS 1.3 combines asymmetric key exchange (Diffie-Hellman) with high-speed symmetric payload encryption (AES-GCM / ChaCha20).",
                            "key_concepts": ["Symmetric encryption (AES-256-GCM) vs Asymmetric (RSA/Ed25519)", "Cryptographic hash functions (SHA-256, SHA-3)", "Public Key Infrastructure (PKI) & X.509 certificates", "Digital signatures and non-repudiation"],
                            "code_snippet": "from cryptography.hazmat.primitives.ciphers.aead import AESGCM\nimport os\n\nkey = AESGCM.generate_key(bit_length=256)\naesgcm = AESGCM(key)\nnonce = os.urandom(12)\n\nciphertext = aesgcm.encrypt(nonce, b\"Classified Security Payload\", None)\nplaintext = aesgcm.decrypt(nonce, ciphertext, None)\nprint(plaintext.decode())",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 4 Assessment: Cryptography & PKI",
                        "description": "Validate your grasp of encryption, digital signatures, and TLS protocols.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "In asymmetric cryptography, which key is used to decrypt a message encrypted with the sender's public key?",
                                "options": ["The sender's private key", "The recipient's private key", "The public key again", "A shared symmetric key"],
                                "correct_index": 1,
                                "explanation": "A message encrypted with the recipient's public key can only be decrypted with the recipient's private key."
                            }
                        ]
                    }
                },
                {
                    "module_number": 5,
                    "phase_name": "Phase 2: Cryptography & Application Security",
                    "title": "Web Application Security & OWASP Top 10",
                    "description": "Identify and mitigate SQL Injection, XSS, Broken Authentication, IDOR, SSRF, and Security Misconfigurations.",
                    "skills": ["Web Application Security (OWASP)", "Vulnerability Assessment"],
                    "estimated_hours": 6.0,
                    "lessons": [
                        {
                            "lesson_number": 5,
                            "title": "Attacking & Defending Web Applications (OWASP Top 10)",
                            "description": "Hands-on vulnerability analysis: SQLi payloads, Stored/Reflected XSS, and CSRF token protections.",
                            "video_url": "https://www.youtube.com/embed/8w8yH_j0c0k",
                            "video_duration": "35 min",
                            "content": "### OWASP Top 10 Vulnerabilities\n\nWeb vulnerabilities allow attackers to bypass authentication, exfiltrate database records, or execute arbitrary scripts in victims' browsers.",
                            "key_concepts": ["SQL Injection (SQLi) & parameterized queries", "Cross-Site Scripting (XSS) & Content Security Policy (CSP)", "Insecure Direct Object References (IDOR)", "Server-Side Request Forgery (SSRF)"],
                            "code_snippet": "<!-- Content Security Policy to block unauthorized external scripts -->\n<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'; script-src 'self' https://trustedscripts.com;\" />",
                            "code_language": "html"
                        }
                    ],
                    "assessment": {
                        "title": "Module 5 Assessment: OWASP Top 10",
                        "description": "Test identification and remediation of web vulnerabilities.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What vulnerability occurs when an API accepts an object ID directly from user input without verifying ownership authorization?",
                                "options": ["Cross-Site Scripting (XSS)", "Insecure Direct Object Reference (IDOR)", "Buffer Overflow", "DNS Spoofing"],
                                "correct_index": 1,
                                "explanation": "IDOR happens when user-supplied identifiers access unauthorized records without tenant checks."
                            }
                        ]
                    }
                },
                {
                    "module_number": 6,
                    "phase_name": "Phase 3: Threat Detection & Operations",
                    "title": "Vulnerability Assessment & Scanning Tools",
                    "description": "Utilize Nmap for port reconnaissance, OpenVAS / Nessus for vulnerability scans, and Nikto for web server audits.",
                    "skills": ["Vulnerability Assessment", "Penetration Testing", "Nmap"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 6,
                            "title": "Network Reconnaissance with Nmap & Vulnerability Scanning",
                            "description": "Learn SYN stealth scans (-sS), service version detection (-sV), OS fingerprinting (-O), and vulnerability scanning scripts.",
                            "video_url": "https://www.youtube.com/embed/4t4kBkMsDbY",
                            "video_duration": "28 min",
                            "content": "### Network Reconnaissance and Scanning\n\nNmap is the gold standard for network discovery and vulnerability assessment, mapping open ports, running services, and known CVEs.",
                            "key_concepts": ["Nmap scan types (-sS, -sT, -sU)", "NSE (Nmap Scripting Engine) vulnerability scripts", "CVSS scoring metrics", "Vulnerability management lifecycles"],
                            "code_snippet": "# Perform SYN stealth scan with version detection and default safe scripts\nnmap -sS -sV -sC -T4 -p 1-10000 192.168.1.1",
                            "code_language": "bash"
                        }
                    ],
                    "assessment": {
                        "title": "Module 6 Assessment: Vulnerability Scanning",
                        "description": "Evaluate port scanning methodologies and CVSS risk prioritization.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What does a CVSS (Common Vulnerability Scoring System) base score of 9.8 indicate?",
                                "options": ["Low severity", "Medium severity", "High severity", "Critical severity"],
                                "correct_index": 3,
                                "explanation": "CVSS scores from 9.0 to 10.0 represent Critical severity vulnerabilities."
                            }
                        ]
                    }
                },
                {
                    "module_number": 7,
                    "phase_name": "Phase 3: Threat Detection & Operations",
                    "title": "SIEM & Security Information Management",
                    "description": "Aggregate logs, build correlation rules, monitor alerts, and detect threats using SIEM platforms (Splunk / ELK).",
                    "skills": ["SIEM & Threat Detection", "Log Analysis", "Splunk"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 7,
                            "title": "Log Aggregation & Threat Detection with SIEM",
                            "description": "Learn Syslog ingestion, query syntax, anomaly detection, and building security alert dashboards.",
                            "video_url": "https://www.youtube.com/embed/kUe2vM_GfVo",
                            "video_duration": "27 min",
                            "content": "### SIEM Architectures & Log Correlation\n\nSecurity Information and Event Management (SIEM) systems ingest event logs from firewalls, servers, and endpoint agents to detect suspicious behavior patterns.",
                            "key_concepts": ["Centralized log forwarding (Syslog, Fluentd)", "Correlation rules for detecting brute-force attacks", "SOC alert triage workflows", "Indicators of Compromise (IOCs)"],
                            "code_snippet": "# Example Splunk search for failed login bursts\nindex=security sourcetype=auth_log \"Failed password\"\n| stats count by src_ip\n| where count > 10",
                            "code_language": "sql"
                        }
                    ],
                    "assessment": {
                        "title": "Module 7 Assessment: SIEM & Monitoring",
                        "description": "Test understanding of log correlation and security event monitoring.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is an Indicator of Compromise (IOC) in cybersecurity monitoring?",
                                "options": [
                                    "A legal patent document.",
                                    "Forensic artifact (such as a malicious file hash, IP address, or domain) indicating a network breach.",
                                    "A hardware warranty.",
                                    "An anti-virus license key."
                                ],
                                "correct_index": 1,
                                "explanation": "IOCs are forensic evidence indicating that a system has been compromised."
                            }
                        ]
                    }
                },
                {
                    "module_number": 8,
                    "phase_name": "Phase 3: Threat Detection & Operations",
                    "title": "Incident Response & Digital Forensics",
                    "description": "Master the NIST Incident Response lifecycle: Preparation, Detection, Containment, Eradication, Recovery, and Post-Incident Analysis.",
                    "skills": ["Incident Response", "Digital Forensics", "NIST Framework"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 8,
                            "title": "NIST Incident Response Lifecycle & Digital Evidence Handling",
                            "description": "Explore chain of custody, memory acquisition (Volatility), network isolation, and post-mortem reporting.",
                            "video_url": "https://www.youtube.com/embed/jZ_E8Nl3j_8",
                            "video_duration": "29 min",
                            "content": "### Incident Response Lifecycle (NIST SP 800-61)\n\nWhen a security incident occurs, systematic containment and forensic analysis prevent further data loss while preserving evidence for legal proceedings.",
                            "key_concepts": ["NIST 6-step incident response framework", "Order of volatility for digital evidence", "Host isolation techniques", "Root cause analysis & post-mortem documentation"],
                            "code_snippet": "# Linux command to check active network connections and listening ports\nss -tulpn | grep -E ':(80|443|22)'",
                            "code_language": "bash"
                        }
                    ],
                    "assessment": {
                        "title": "Module 8 Assessment: Incident Response",
                        "description": "Validate containment strategies and forensic evidence preservation.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "According to the order of volatility, which data source should be captured first during forensic triage?",
                                "options": ["Hard disk drive backup", "RAM / volatile memory", "Archived optical discs", "Printed server logs"],
                                "correct_index": 1,
                                "explanation": "RAM is lost immediately upon power-down and must be acquired first."
                            }
                        ]
                    }
                },
                {
                    "module_number": 9,
                    "phase_name": "Phase 4: Advanced Security & Capstone",
                    "title": "Cloud Security & Identity Access Management (IAM)",
                    "description": "Secure AWS / Azure cloud environments, configure IAM least-privilege roles, VPC peering, and CloudTrail auditing.",
                    "skills": ["Cloud Security", "IAM", "AWS Security"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 9,
                            "title": "Cloud IAM, Security Groups & GuardDuty",
                            "description": "Learn role-based access control (RBAC), multi-factor authentication (MFA), and automated cloud threat detection.",
                            "video_url": "https://www.youtube.com/embed/0x_9H5k6a3E",
                            "video_duration": "26 min",
                            "content": "### Cloud Security Governance\n\nCloud security follows the Shared Responsibility Model. Cloud providers secure the underlying hardware, while customers are responsible for data encryption, IAM policies, and application security.",
                            "key_concepts": ["Shared responsibility model", "IAM policy documents (JSON)", "VPC security groups vs Network ACLs", "CloudTrail audit log analysis"],
                            "code_snippet": "{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [{\n    \"Effect\": \"Allow\",\n    \"Action\": [\"s3:GetObject\"],\n    \"Resource\": \"arn:aws:s3:::pathpilot-secure-bucket/*\"\n  }]\n}",
                            "code_language": "json"
                        }
                    ],
                    "assessment": {
                        "title": "Module 9 Assessment: Cloud Security",
                        "description": "Test cloud IAM policies and shared responsibility principles.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "In the AWS Shared Responsibility Model, who is responsible for applying OS security patches to an EC2 instance?",
                                "options": ["AWS Hardware Team", "The Customer / Organization", "The Internet Service Provider", "The Domain Registrar"],
                                "correct_index": 1,
                                "explanation": "In IaaS (EC2), the customer is responsible for managing and patching the operating system."
                            }
                        ]
                    }
                },
                {
                    "module_number": 10,
                    "phase_name": "Phase 4: Advanced Security & Capstone",
                    "title": "Security Automation & Threat Intelligence",
                    "description": "Automate security workflows with Python, integrate threat intelligence feeds (STIX/TAXII), and parse CVE databases.",
                    "skills": ["Security Automation", "Python for Security", "Threat Intelligence"],
                    "estimated_hours": 4.5,
                    "lessons": [
                        {
                            "lesson_number": 10,
                            "title": "Automating Threat Hunting with Python",
                            "description": "Script automated IP reputation checks, parse authentication logs, and trigger webhook alerts on Slack/Discord.",
                            "video_url": "https://www.youtube.com/embed/mG3uO8Fp9sY",
                            "video_duration": "24 min",
                            "content": "### Python for Security Automation\n\nSecurity engineers leverage Python to automate repetitive SOC tasks, parse logs, query VirusTotal APIs, and isolate compromised endpoints.",
                            "key_concepts": ["VirusTotal API queries", "Regular expressions for IP/domain extraction", "Automated webhook alert dispatching", "SOAR (Security Orchestration, Automation and Response) concepts"],
                            "code_snippet": "import requests\n\ndef check_ip_reputation(ip: str, api_key: str) -> dict:\n    headers = {\"x-apikey\": api_key}\n    url = f\"https://www.virustotal.com/api/v3/ip_addresses/{ip}\"\n    response = requests.get(url, headers=headers)\n    return response.json()",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 10 Assessment: Security Automation",
                        "description": "Assess security scripting and threat intelligence integration.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the primary role of a SOAR platform in a Security Operations Center?",
                                "options": [
                                    "Automating incident triage and response workflows across multiple security tools.",
                                    "Designing website wireframes.",
                                    "Replacing all firewalls with routers.",
                                    "Formatting hard drives weekly."
                                ],
                                "correct_index": 0,
                                "explanation": "SOAR platforms automate threat correlation, triage, and rapid containment playbooks."
                            }
                        ]
                    }
                },
                {
                    "module_number": 11,
                    "phase_name": "Phase 4: Advanced Security & Capstone",
                    "title": "Governance, Risk & Compliance (GRC)",
                    "description": "Understand ISO 27001, SOC 2 Type II, GDPR, HIPAA, risk assessment methodologies, and third-party vendor audits.",
                    "skills": ["GRC", "Compliance", "Risk Assessment"],
                    "estimated_hours": 4.0,
                    "lessons": [
                        {
                            "lesson_number": 11,
                            "title": "Security Frameworks (ISO 27001, SOC 2 & GDPR)",
                            "description": "Learn compliance auditing, risk registers, data privacy impact assessments, and zero-trust architecture.",
                            "video_url": "https://www.youtube.com/embed/yF1x3t9PqL0",
                            "video_duration": "22 min",
                            "content": "### Security Governance & Regulatory Compliance\n\nEnterprise security requires meeting strict legal compliance standards to protect customer privacy and manage risk.",
                            "key_concepts": ["SOC 2 Trust Services Criteria", "GDPR data sovereignty and right to erasure", "Zero Trust Architecture ('Never trust, always verify')", "Third-party vendor risk management"],
                            "code_snippet": "# Risk Score Formula\nRisk = Likelihood * Impact",
                            "code_language": "text"
                        }
                    ],
                    "assessment": {
                        "title": "Module 11 Assessment: GRC & Zero Trust",
                        "description": "Test compliance frameworks and zero-trust concepts.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the foundational philosophy of Zero Trust Architecture?",
                                "options": [
                                    "Trust all internal network traffic implicitly.",
                                    "Never trust, always verify every access request regardless of origin.",
                                    "Disable all encryption to speed up audits.",
                                    "Only allow traffic from mobile devices."
                                ],
                                "correct_index": 1,
                                "explanation": "Zero Trust assumes threats exist both inside and outside the perimeter."
                            }
                        ]
                    }
                },
                {
                    "module_number": 12,
                    "phase_name": "Phase 4: Advanced Security & Capstone",
                    "title": "Capstone Security Audit & Defense Project",
                    "description": "Execute a full-scope vulnerability assessment, write an executive penetration test report, and implement hardened defenses.",
                    "skills": ["Security Audit", "Penetration Testing", "Executive Reporting"],
                    "estimated_hours": 7.5,
                    "lessons": [
                        {
                            "lesson_number": 12,
                            "title": "Comprehensive Enterprise Security Audit",
                            "description": "Conduct end-to-end vulnerability scanning, identify critical findings, and deliver remediation roadmaps.",
                            "video_url": "https://www.youtube.com/embed/1k_7f8d6G3Q",
                            "video_duration": "30 min",
                            "content": "### Capstone Security Audit\n\nPut your skills to the test by performing a simulated enterprise security review, documenting vulnerabilities with CVSS scores, and producing professional remediation guidelines.",
                            "key_concepts": ["Executive summary vs technical findings", "Remediation prioritization roadmap", "Post-audit verification testing", "Security KPI measurement"],
                            "code_snippet": "# Final audit checklist\n- [x] External port perimeter review\n- [x] SSL/TLS configuration test\n- [x] OWASP Top 10 web assessment\n- [x] IAM privilege audit\n- [x] Incident response verification",
                            "code_language": "text"
                        }
                    ],
                    "assessment": {
                        "title": "Module 12 Assessment: Capstone Defense Mastery",
                        "description": "Verify comprehensive security auditing proficiency.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "When presenting a security audit report to executive leadership, what should be highlighted first?",
                                "options": [
                                    "Raw tcpdump hex outputs.",
                                    "An Executive Summary detailing business impact, risk posture, and high-level remediation costs.",
                                    "A list of all employee names.",
                                    "Source code diffs."
                                ],
                                "correct_index": 1,
                                "explanation": "Executive summaries translate technical findings into business risks and actionable strategic steps."
                            }
                        ]
                    }
                }
            ],
            "final_assessment": {
                "title": "Cybersecurity Comprehensive Final Exam",
                "description": "Comprehensive 10-question evaluation covering CIA Triad, Networking, Linux Hardening, Cryptography, OWASP Top 10, SIEM, and Incident Response.",
                "time_minutes": 45,
                "passing_score": 70.0,
                "questions": [
                    {
                        "question_text": "What type of cyberattack involves sending forged ARP messages to associate an attacker's MAC address with the default gateway's IP address?",
                        "options": ["ARP Poisoning / Spoofing", "DNS Exfiltration", "Cross-Site Request Forgery", "Buffer Overflow"],
                        "correct_index": 0,
                        "topic": "Networking",
                        "explanation": "ARP poisoning corrupts local ARP tables allowing attackers to intercept traffic in a Man-in-the-Middle position."
                    },
                    {
                        "question_text": "Which symmetric encryption mode provides both confidentiality and built-in cryptographic authentication/integrity?",
                        "options": ["AES-ECB", "AES-CBC", "AES-GCM", "DES"],
                        "correct_index": 2,
                        "topic": "Cryptography",
                        "explanation": "Galois/Counter Mode (GCM) is an AEAD mode providing authenticated encryption."
                    },
                    {
                        "question_text": "What is the primary remediation for Reflected Cross-Site Scripting (XSS)?",
                        "options": [
                            "Context-aware output encoding and Content Security Policy (CSP).",
                            "Disabling all CSS.",
                            "Increasing RAM on the server.",
                            "Changing DNS nameservers."
                        ],
                        "correct_index": 0,
                        "topic": "Web Security",
                        "explanation": "Encoding untrusted data before rendering prevents the browser from interpreting it as executable script."
                    }
                ]
            }
        },

        # =========================================================================
        # 4. SOFTWARE DEVELOPMENT ENGINEER (SDE)
        # =========================================================================
        {
            "slug": "software-development-engineer",
            "title": "Software Development Engineer (SDE)",
            "tagline": "Master computer science foundations, algorithms, system design, object-oriented principles, and scalable software engineering.",
            "description": "A rigorous curriculum designed to build world-class software development engineers. Covers data structures & algorithms, OOP & design patterns, operating systems, relational/NoSQL databases, system design fundamentals, microservices, and coding interview preparation.",
            "career_name": "Software Development Engineer (SDE)",
            "difficulty": "Advanced",
            "estimated_duration": "12 Weeks",
            "total_modules": 12,
            "total_lessons": 36,
            "total_projects": 4,
            "total_assessments": 12,
            "skills_covered": ["Data Structures", "Algorithms", "Object-Oriented Programming", "System Design", "Databases", "Operating Systems", "Computer Networks", "Software Engineering", "Testing & CI/CD"],
            "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
            "modules": [
                {
                    "module_number": 1,
                    "phase_name": "Phase 1: CS Foundations & Data Structures",
                    "title": "Programming Foundations & Memory Architecture",
                    "description": "Understand pointers, stack vs heap memory, memory allocation, bit manipulation, and asymptotic Big-O notation.",
                    "skills": ["Programming", "Memory Management", "Big-O Notation"],
                    "estimated_hours": 4.5,
                    "lessons": [
                        {
                            "lesson_number": 1,
                            "title": "Stack vs Heap Memory & Time/Space Complexity",
                            "description": "Learn Big-O time complexity (O(1), O(log n), O(n), O(n log n), O(n^2)), stack frames, and heap allocation.",
                            "video_url": "https://www.youtube.com/embed/D6xkbGLQesk",
                            "video_duration": "28 min",
                            "content": "### Computational Complexity & Memory Models\n\nSoftware engineers must evaluate the algorithmic efficiency of code. Big-O notation describes the upper bound of execution time or memory footprint as input size $N$ scales.",
                            "key_concepts": ["Stack memory (LIFO, automatic) vs Heap memory (dynamic)", "Big-O, Big-Theta, Big-Omega definitions", "Space complexity auxiliary memory analysis", "Garbage collection algorithms"],
                            "code_snippet": "# O(log n) Binary Search Implementation\ndef binary_search(arr: list[int], target: int) -> int:\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = left + (right - left) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 1 Assessment: Memory & Complexity",
                        "description": "Test understanding of asymptotic complexity and stack/heap memory.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the time complexity of searching for an element in a balanced Binary Search Tree containing N nodes?",
                                "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
                                "correct_index": 1,
                                "explanation": "Each step in a balanced BST cuts search space in half, resulting in O(log N) operations."
                            }
                        ]
                    }
                },
                {
                    "module_number": 2,
                    "phase_name": "Phase 1: CS Foundations & Data Structures",
                    "title": "Linear Data Structures (Arrays, Linked Lists, Stacks & Queues)",
                    "description": "Implement dynamic arrays, singly/doubly linked lists, monotonic stacks, priority queues, and ring buffers.",
                    "skills": ["Data Structures", "Linked Lists", "Stacks & Queues"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 2,
                            "title": "Linked Lists, Reversals & Cycle Detection",
                            "description": "Master pointer manipulation, Floyd's cycle detection algorithm, and stack/queue implementations.",
                            "video_url": "https://www.youtube.com/embed/F8xQw46607U",
                            "video_duration": "30 min",
                            "content": "### Pointer-Based Linear Data Structures\n\nLinked lists allow $O(1)$ insertions and deletions without contiguous memory reallocation. Stacks and queues enforce LIFO and FIFO ordering.",
                            "key_concepts": ["Singly vs Doubly Linked Lists", "Floyd's Tortoise and Hare cycle detection", "Monotonic Stack patterns for Next Greater Element", "Circular queue implementations"],
                            "code_snippet": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef reverse_list(head: ListNode) -> ListNode:\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 2 Assessment: Linear Data Structures",
                        "description": "Evaluate knowledge of linked lists, stacks, and queues.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the amortized time complexity of appending an element to a dynamic array in Python?",
                                "options": ["O(1)", "O(log N)", "O(N)", "O(N^2)"],
                                "correct_index": 0,
                                "explanation": "Although occasional resizing takes O(N), the amortized average cost per append is O(1)."
                            }
                        ]
                    }
                },
                {
                    "module_number": 3,
                    "phase_name": "Phase 1: CS Foundations & Data Structures",
                    "title": "Non-Linear Data Structures (Trees, Heaps & Graphs)",
                    "description": "Master Binary Trees, AVL / Red-Black Trees, Tries, Min/Max Binary Heaps, and Graph adjacency representations.",
                    "skills": ["Trees", "Heaps", "Graphs", "Data Structures"],
                    "estimated_hours": 6.5,
                    "lessons": [
                        {
                            "lesson_number": 3,
                            "title": "Tree Traversals, Trie Prefix Trees & Binary Heaps",
                            "description": "Understand BFS (level-order), DFS (pre-order, in-order, post-order), Trie autocomplete, and Heapify algorithms.",
                            "video_url": "https://www.youtube.com/embed/7HgsS8bRvgw",
                            "video_duration": "32 min",
                            "content": "### Hierarchical & Graph Data Structures\n\nTrees and graphs represent complex hierarchical and networked relationships. Heaps provide immediate $O(1)$ access to minimum/maximum elements.",
                            "key_concepts": ["In-order, pre-order, and post-order traversal", "Trie dictionary prefix search", "Binary Heap sift-up / sift-down mechanics", "Graph adjacency matrix vs adjacency list"],
                            "code_snippet": "import heapq\n\ndef find_k_largest(nums: list[int], k: int) -> list[int]:\n    min_heap = []\n    for num in nums:\n        heapq.heappush(min_heap, num)\n        if len(min_heap) > k:\n            heapq.heappop(min_heap)\n    return min_heap",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 3 Assessment: Trees, Heaps & Graphs",
                        "description": "Test tree traversals, heap properties, and graph structures.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "In a Binary Min-Heap containing N elements, what is the time complexity to insert a new element?",
                                "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
                                "correct_index": 1,
                                "explanation": "Inserting an element and bubbling up along the tree height takes O(log N) comparisons."
                            }
                        ]
                    }
                },
                {
                    "module_number": 4,
                    "phase_name": "Phase 2: Algorithmic Problem Solving",
                    "title": "Sorting, Searching & Graph Algorithms",
                    "description": "Master MergeSort, QuickSort, Dijkstra's Shortest Path, Topological Sort, BFS, and DFS on graphs.",
                    "skills": ["Algorithms", "Graph Algorithms", "Sorting & Searching"],
                    "estimated_hours": 6.0,
                    "lessons": [
                        {
                            "lesson_number": 4,
                            "title": "Dijkstra's Shortest Path & Topological Sort",
                            "description": "Implement weighted shortest path search with priority queues and dependency ordering with Kahn's algorithm.",
                            "video_url": "https://www.youtube.com/embed/EFg3u_E6eHU",
                            "video_duration": "30 min",
                            "content": "### Advanced Graph Algorithms\n\nGraph traversal algorithms solve routing, scheduling, and dependency resolution challenges in distributed systems.",
                            "key_concepts": ["Dijkstra's algorithm with priority queue ($O((V+E) \\log V)$)", "Topological sorting on Directed Acyclic Graphs (DAGs)", "Breadth-First Search for shortest unweighted paths", "Connected components & cycle detection"],
                            "code_snippet": "import heapq\n\ndef dijkstra(graph: dict, start: int) -> dict:\n    distances = {node: float('inf') for node in graph}\n    distances[start] = 0\n    pq = [(0, start)]\n    \n    while pq:\n        curr_dist, u = heapq.heappop(pq)\n        if curr_dist > distances[u]: continue\n        for v, weight in graph[u]:\n            if distances[u] + weight < distances[v]:\n                distances[v] = distances[u] + weight\n                heapq.heappush(pq, (distances[v], v))\n    return distances",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 4 Assessment: Graph Algorithms",
                        "description": "Evaluate shortest path, topological sorting, and BFS/DFS mechanics.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What type of graph is required for Topological Sorting to be valid?",
                                "options": ["Undirected cyclic graph", "Directed Acyclic Graph (DAG)", "Complete bipartite graph", "Unweighted tree only"],
                                "correct_index": 1,
                                "explanation": "Topological sorting is strictly defined on Directed Acyclic Graphs (DAGs)."
                            }
                        ]
                    }
                },
                {
                    "module_number": 5,
                    "phase_name": "Phase 2: Algorithmic Problem Solving",
                    "title": "Dynamic Programming & Greedy Strategies",
                    "description": "Master memoization (top-down), tabulation (bottom-up), 0/1 Knapsack, Longest Common Subsequence, and interval scheduling.",
                    "skills": ["Dynamic Programming", "Greedy Algorithms", "Optimization"],
                    "estimated_hours": 6.5,
                    "lessons": [
                        {
                            "lesson_number": 5,
                            "title": "Memoization vs Tabulation & 2D Dynamic Programming",
                            "description": "Learn state transition equations, optimal substructure, overlapping subproblems, and space optimization.",
                            "video_url": "https://www.youtube.com/embed/oBt53YbR9Kk",
                            "video_duration": "35 min",
                            "content": "### Dynamic Programming (DP)\n\nDynamic Programming solves complex problems by breaking them into overlapping subproblems and storing subproblem results to avoid redundant recomputation.",
                            "key_concepts": ["Optimal substructure & overlapping subproblems", "Top-down memoization vs Bottom-up tabulation", "0/1 Knapsack problem pattern", "State space reduction techniques"],
                            "code_snippet": "def coinChange(coins: list[int], amount: int) -> int:\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for coin in coins:\n        for x in range(coin, amount + 1):\n            dp[x] = min(dp[x], dp[x - coin] + 1)\n    return dp[amount] if dp[amount] != float('inf') else -1",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 5 Assessment: Dynamic Programming",
                        "description": "Assess DP recurrence relations and state transition optimization.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What are the two essential properties a problem must exhibit for Dynamic Programming to apply?",
                                "options": [
                                    "Optimal Substructure and Overlapping Subproblems",
                                    "Greedy Choice Property and Linear Equations",
                                    "Randomized Inputs and Sorting",
                                    "Tail Recursion and Binary Tree Shapes"
                                ],
                                "correct_index": 0,
                                "explanation": "DP requires optimal substructure and overlapping subproblems."
                            }
                        ]
                    }
                },
                {
                    "module_number": 6,
                    "phase_name": "Phase 2: Algorithmic Problem Solving",
                    "title": "Object-Oriented Design & SOLID Principles",
                    "description": "Apply Encapsulation, Inheritance, Polymorphism, Abstraction, and the 5 SOLID engineering principles in production code.",
                    "skills": ["Object-Oriented Programming", "SOLID Principles", "Software Design"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 6,
                            "title": "The SOLID Principles of Object-Oriented Software Design",
                            "description": "Master Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.",
                            "video_url": "https://www.youtube.com/embed/pTB30aXS77U",
                            "video_duration": "28 min",
                            "content": "### SOLID Principles for Maintainable Software\n\nWriting enterprise software requires adhering to design principles that make systems extensible without breaking existing functionality.",
                            "key_concepts": ["Single Responsibility Principle (SRP)", "Open/Closed Principle (OCP)", "Liskov Substitution Principle (LSP)", "Dependency Inversion Principle (DIP)"],
                            "code_snippet": "from abc import ABC, abstractmethod\n\nclass PaymentProcessor(ABC):\n    @abstractmethod\n    def process_payment(self, amount: float) -> bool:\n        pass\n\nclass StripeProcessor(PaymentProcessor):\n    def process_payment(self, amount: float) -> bool:\n        print(f\"Processing ${amount} via Stripe API\")\n        return True",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 6 Assessment: SOLID & OOP",
                        "description": "Test design pattern selection and SOLID violation identification.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What does the Open/Closed Principle (OCP) state?",
                                "options": [
                                    "Software entities should be open for extension, but closed for modification.",
                                    "Classes should always be open source.",
                                    "All database connections must be closed after use.",
                                    "Interfaces must contain at least 10 methods."
                                ],
                                "correct_index": 0,
                                "explanation": "OCP ensures software can be extended with new features without modifying tested existing code."
                            }
                        ]
                    }
                },
                {
                    "module_number": 7,
                    "phase_name": "Phase 3: Systems & System Design",
                    "title": "Design Patterns (Creational, Structural & Behavioral)",
                    "description": "Implement Factory, Singleton, Strategy, Observer, Decorator, and Adapter patterns in production.",
                    "skills": ["Design Patterns", "Software Architecture"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 7,
                            "title": "Gang of Four (GoF) Patterns in Modern Systems",
                            "description": "Explore Factory Method, Strategy pattern, Observer pub/sub, and Dependency Injection containers.",
                            "video_url": "https://www.youtube.com/embed/v9ejT8FO-7I",
                            "video_duration": "30 min",
                            "content": "### Software Design Patterns\n\nDesign patterns provide battle-tested blueprints for solving recurring software engineering challenges.",
                            "key_concepts": ["Creational: Factory Method, Singleton, Builder", "Structural: Adapter, Decorator, Facade", "Behavioral: Strategy, Observer, Command", "Anti-patterns to avoid (God Object, Premature Optimization)"],
                            "code_snippet": "class NotificationService:\n    def __init__(self, strategy):\n        self._strategy = strategy\n        \n    def notify(self, message: str):\n        self._strategy.send(message)",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 7 Assessment: Design Patterns",
                        "description": "Assess pattern implementation and trade-off analysis.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Which design pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime?",
                                "options": ["Singleton Pattern", "Strategy Pattern", "Adapter Pattern", "Proxy Pattern"],
                                "correct_index": 1,
                                "explanation": "The Strategy Pattern enables selecting algorithms dynamically at runtime."
                            }
                        ]
                    }
                },
                {
                    "module_number": 8,
                    "phase_name": "Phase 3: Systems & System Design",
                    "title": "Operating Systems, Concurrency & Multithreading",
                    "description": "Understand process management, threads, context switching, locks, semaphores, race conditions, and deadlocks.",
                    "skills": ["Operating Systems", "Concurrency", "Multithreading"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 8,
                            "title": "Processes, Threads, Mutex Locks & Deadlock Conditions",
                            "description": "Master Coffman's 4 deadlock conditions, race conditions, atomic operations, and thread safety.",
                            "video_url": "https://www.youtube.com/embed/7VbL89zVpCw",
                            "video_duration": "28 min",
                            "content": "### Concurrency & Thread Synchronization\n\nMulti-core processors execute multiple execution threads simultaneously. Coordinating shared memory access requires mutexes, condition variables, and lock ordering.",
                            "key_concepts": ["Process vs Thread memory space", "Mutual exclusion (Mutex) & Semaphores", "Coffman deadlock conditions", "Lock-free data structures & atomic instructions"],
                            "code_snippet": "import threading\n\nlock = threading.Lock()\ncounter = 0\n\ndef safe_increment():\n    global counter\n    with lock:\n        counter += 1",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 8 Assessment: OS & Concurrency",
                        "description": "Test multithreading synchronization and deadlock prevention.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Which of the following is NOT one of Coffman's four conditions required for a Deadlock to occur?",
                                "options": ["Mutual Exclusion", "Hold and Wait", "No Preemption", "Asynchronous I/O"],
                                "correct_index": 3,
                                "explanation": "The 4 Coffman conditions are Mutual Exclusion, Hold & Wait, No Preemption, and Circular Wait."
                            }
                        ]
                    }
                },
                {
                    "module_number": 9,
                    "phase_name": "Phase 3: Systems & System Design",
                    "title": "System Design Fundamentals (Scalability & High Availability)",
                    "description": "Learn horizontal vs vertical scaling, load balancing algorithms, CAP theorem, database sharding, and caching layers.",
                    "skills": ["System Design", "Scalability", "CAP Theorem", "Distributed Systems"],
                    "estimated_hours": 6.5,
                    "lessons": [
                        {
                            "lesson_number": 9,
                            "title": "Architecting for Millions of Users: Load Balancers & Caching",
                            "description": "Learn Layer 4 vs Layer 7 load balancers, consistent hashing, CDN caching, and read replicas.",
                            "video_url": "https://www.youtube.com/embed/SqsR94DYWJ8",
                            "video_duration": "35 min",
                            "content": "### Scalable System Design Foundations\n\nDesigning distributed systems capable of serving millions of requests requires decoupling components, eliminating single points of failure, and distributing data horizontally.",
                            "key_concepts": ["Horizontal scaling vs Vertical scaling", "CAP Theorem (Consistency, Availability, Partition Tolerance)", "Database replication (Master-Slave) & Sharding", "Consistent hashing algorithms"],
                            "code_snippet": "# Load balancer round-robin logic\nclass RoundRobinBalancer:\n    def __init__(self, servers: list[str]):\n        self.servers = servers\n        self.index = 0\n    def get_server(self) -> str:\n        server = self.servers[self.index]\n        self.index = (self.index + 1) % len(self.servers)\n        return server",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 9 Assessment: System Design Fundamentals",
                        "description": "Assess understanding of distributed system architecture and CAP theorem.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "According to the CAP Theorem, in the presence of a network partition (P), what trade-off must a distributed system make?",
                                "options": [
                                    "Choose between Consistency (C) and Availability (A).",
                                    "Choose between Speed and Security.",
                                    "Choose between SQL and NoSQL.",
                                    "Choose between RAM and Disk storage."
                                ],
                                "correct_index": 0,
                                "explanation": "Under network partition (P), a system must either return consistent data or remain available."
                            }
                        ]
                    }
                },
                {
                    "module_number": 10,
                    "phase_name": "Phase 4: Production Engineering & Interview Prep",
                    "title": "Asynchronous Systems & Message Queues",
                    "description": "Design event-driven architectures using Apache Kafka, RabbitMQ, Celery workers, and pub/sub message brokers.",
                    "skills": ["Message Queues", "Event-Driven Architecture", "Kafka"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 10,
                            "title": "Event-Driven Architectures with Message Brokers",
                            "description": "Understand message queues vs pub/sub logs, consumer groups, idempotency keys, and dead-letter queues.",
                            "video_url": "https://www.youtube.com/embed/F2zlsU3KkR4",
                            "video_duration": "28 min",
                            "content": "### Decoupling Services with Asynchronous Message Queues\n\nMessage queues decouple heavy background processing (such as AI roadmap generation or report compiling) from synchronous HTTP request threads.",
                            "key_concepts": ["Point-to-point queues vs Publish/Subscribe topics", "Kafka partitions and consumer offsets", "Dead Letter Queues (DLQ) for failed jobs", "At-least-once vs Exactly-once message delivery"],
                            "code_snippet": "# Example Celery task for background AI generation\n@celery_app.task(bind=True, max_retries=3)\ndef generate_personalized_learning_path(self, user_id: int, career_id: int):\n    try:\n        return run_heavy_ai_engine(user_id, career_id)\n    except Exception as exc:\n        raise self.retry(exc=exc, countdown=10)",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 10 Assessment: Message Queues",
                        "description": "Evaluate asynchronous architectures and distributed queues.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the purpose of a Dead Letter Queue (DLQ) in an asynchronous messaging architecture?",
                                "options": [
                                    "To discard spam emails.",
                                    "To store messages that could not be processed successfully after maximum retry attempts for debugging and manual reprocessing.",
                                    "To encrypt database passwords.",
                                    "To terminate active web sockets."
                                ],
                                "correct_index": 1,
                                "explanation": "DLQs capture unprocessable messages so they don't block the main consumer queue."
                            }
                        ]
                    }
                },
                {
                    "module_number": 11,
                    "phase_name": "Phase 4: Production Engineering & Interview Prep",
                    "title": "Distributed Systems: Caching, Sharding & Consistent Hashing",
                    "description": "Master database partitioning, cross-shard joins, Redis clusters, and distributed locking (Redlock).",
                    "skills": ["Distributed Systems", "Database Sharding", "Consistent Hashing"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 11,
                            "title": "Consistent Hashing & Database Partitioning Strategies",
                            "description": "Learn hash rings, virtual nodes, horizontal sharding by range vs hash, and distributed cache clusters.",
                            "video_url": "https://www.youtube.com/embed/zaRkONvyGr8",
                            "video_duration": "30 min",
                            "content": "### Distributed Data Partitioning\n\nConsistent hashing minimizes key remapping when cache or database nodes are added or removed dynamically.",
                            "key_concepts": ["Hash ring with virtual nodes", "Range-based vs Hash-based sharding", "Distributed consensus (Raft / Paxos basics)", "Distributed locking with Redis"],
                            "code_snippet": "import hashlib\n\nclass ConsistentHashRing:\n    def __init__(self, nodes: list[str]):\n        self.ring = {}\n        for node in nodes:\n            h = int(hashlib.md5(node.encode()).hexdigest(), 16)\n            self.ring[h] = node",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 11 Assessment: Distributed Data",
                        "description": "Test understanding of sharding and consistent hashing.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Why does Consistent Hashing use virtual nodes on the hash ring?",
                                "options": [
                                    "To ensure even key distribution across physical servers and prevent hot spots.",
                                    "To bypass hardware firewalls.",
                                    "To make SQL queries faster.",
                                    "To encrypt network packets."
                                ],
                                "correct_index": 0,
                                "explanation": "Virtual nodes distribute keys uniformly across physical servers."
                            }
                        ]
                    }
                },
                {
                    "module_number": 12,
                    "phase_name": "Phase 4: Production Engineering & Interview Prep",
                    "title": "SDE Capstone: Scalable Distributed Service & Interview Coding",
                    "description": "Design, implement, and benchmark a distributed URL shortener or rate limiter, and master coding interview problem patterns.",
                    "skills": ["System Design", "Coding Interview Mastery", "Production Engineering"],
                    "estimated_hours": 8.0,
                    "lessons": [
                        {
                            "lesson_number": 12,
                            "title": "Designing a Distributed Rate Limiter & URL Shortener",
                            "description": "Step-by-step system design walkthrough: API contracts, DB schema, Base62 encoding, Redis token bucket, and capacity estimates.",
                            "video_url": "https://www.youtube.com/embed/UGnpCj4yNq0",
                            "video_duration": "35 min",
                            "content": "### End-to-End System Design Capstone\n\nDesign an end-to-end distributed system that handles 100,000 requests per second with high availability and low latency.",
                            "key_concepts": ["Back-of-the-envelope capacity estimations", "Base62 counter encoding for tiny URLs", "Token bucket / Sliding window rate limiters in Redis Lua", "SDE interview communication framework"],
                            "code_snippet": "# Redis Lua Script for Atomic Sliding Window Rate Limiting\nLUA_SCRIPT = \"\"\"\nlocal key = KEYS[1]\nlocal now = tonumber(ARGV[1])\nlocal window = tonumber(ARGV[2])\nlocal limit = tonumber(ARGV[3])\n\nredis.call('ZREMRANGEBYSCORE', key, 0, now - window)\nlocal count = redis.call('ZCARD', key)\nif count < limit then\n    redis.call('ZADD', key, now, now)\n    redis.call('EXPIRE', key, window)\n    return 1\nelse\n    return 0\nend\n\"\"\"",
                            "code_language": "lua"
                        }
                    ],
                    "assessment": {
                        "title": "Module 12 Assessment: SDE Capstone Mastery",
                        "description": "Evaluate comprehensive system design and problem solving proficiency.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "In a distributed URL shortener, why is Base62 encoding (a-z, A-Z, 0-9) used instead of Base64?",
                                "options": [
                                    "Because Base64 contains '+' and '/' characters which require URL encoding in web browsers.",
                                    "Base62 generates shorter strings than Base64.",
                                    "Base62 is a cryptographic hash.",
                                    "Base64 is deprecated by W3C."
                                ],
                                "correct_index": 0,
                                "explanation": "Base62 uses alphanumeric characters safe for direct use in URLs without escaping."
                            }
                        ]
                    }
                }
            ],
            "final_assessment": {
                "title": "Software Development Engineer Comprehensive Final Exam",
                "description": "Comprehensive 10-question assessment covering Data Structures, Sorting, Graph Algorithms, Dynamic Programming, SOLID, Concurrency, and System Design.",
                "time_minutes": 45,
                "passing_score": 70.0,
                "questions": [
                    {
                        "question_text": "What is the worst-case time complexity of QuickSort when the pivot chosen is always the maximum or minimum element?",
                        "options": ["O(N log N)", "O(N^2)", "O(N)", "O(log N)"],
                        "correct_index": 1,
                        "topic": "Algorithms",
                        "explanation": "Unbalanced partitions reduce QuickSort to O(N^2) worst-case time complexity."
                    },
                    {
                        "question_text": "Which concurrency hazard occurs when two threads attempt to modify shared memory simultaneously without synchronization?",
                        "options": ["Deadlock", "Race Condition", "Starvation", "Memory Leak"],
                        "correct_index": 1,
                        "topic": "Operating Systems",
                        "explanation": "A Race Condition occurs when output depends on non-deterministic execution order."
                    },
                    {
                        "question_text": "Which design pattern is best suited for decoupling event producers from multiple disparate subscriber services?",
                        "options": ["Observer / Pub-Sub Pattern", "Singleton Pattern", "Factory Method", "Flyweight Pattern"],
                        "correct_index": 0,
                        "topic": "Design Patterns",
                        "explanation": "Observer/Pub-Sub decouples subject state broadcasts from consumer subscribers."
                    }
                ]
            }
        },

        # =========================================================================
        # 5. AI ENGINEER
        # =========================================================================
        {
            "slug": "ai-engineer",
            "title": "AI Engineer",
            "tagline": "Build production-grade applications powered by Large Language Models (LLMs), RAG pipelines, Vector Databases, and PyTorch.",
            "description": "A cutting-edge curriculum mastering practical AI engineering: Mathematics & Python for AI, NumPy & Pandas, Machine Learning foundations, Deep Learning & Neural Networks in PyTorch, NLP, Computer Vision, Generative AI, Prompt Engineering, Vector Databases, and RAG systems.",
            "career_name": "AI Engineer",
            "difficulty": "Advanced",
            "estimated_duration": "12 Weeks",
            "total_modules": 12,
            "total_lessons": 36,
            "total_projects": 4,
            "total_assessments": 12,
            "skills_covered": ["Python", "NumPy", "Pandas", "Mathematics for AI", "Machine Learning", "PyTorch", "Deep Learning", "Natural Language Processing (NLP)", "Computer Vision", "Large Language Models (LLMs)", "RAG Systems", "Vector Databases"],
            "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&q=80",
            "modules": [
                {
                    "module_number": 1,
                    "phase_name": "Phase 1: Mathematics & Data Science Foundations",
                    "title": "Python for AI & Scientific Computing (NumPy & Vectorization)",
                    "description": "Master multi-dimensional array operations, matrix multiplications, broadcasting rules, and high-performance vectorization.",
                    "skills": ["Python", "NumPy", "Vectorization"],
                    "estimated_hours": 4.5,
                    "lessons": [
                        {
                            "lesson_number": 1,
                            "title": "NumPy N-Dimensional Arrays, Broadcasting & Matrix Math",
                            "description": "Learn array indexing, vector dot products, matrix algebra, and avoiding slow Python loops with vectorization.",
                            "video_url": "https://www.youtube.com/embed/QUT1VxF65PC",
                            "video_duration": "28 min",
                            "content": "### High-Performance Scientific Computing with NumPy\n\nAI and machine learning algorithms operate on tensors and matrices. NumPy provides C-contiguous arrays and SIMD vectorization that execute matrix calculations up to 100x faster than pure Python.",
                            "key_concepts": ["ndarray memory layout (C-order vs Fortran-order)", "Array broadcasting rules", "Matrix multiplication with np.dot and `@` operator", "Vectorized masking and filtering"],
                            "code_snippet": "import numpy as np\n\n# Vectorized matrix multiplication\nA = np.random.randn(1000, 512)\nB = np.random.randn(512, 128)\n\n# Fast C-level BLAS matrix product\nC = A @ B\nprint(f\"Resulting embedding tensor shape: {C.shape}\") # (1000, 128)",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 1 Assessment: NumPy & Vectorization",
                        "description": "Test array shape manipulation, broadcasting rules, and matrix multiplication.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What happens when you multiply a NumPy array of shape (4, 1) with an array of shape (1, 3) using broadcasting?",
                                "options": [
                                    "An error occurs because shapes do not match.",
                                    "Broadcasting expands dimensions to produce an array of shape (4, 3).",
                                    "It returns a 1D vector of length 12.",
                                    "It returns None."
                                ],
                                "correct_index": 1,
                                "explanation": "NumPy broadcasts singleton dimensions (1) along the corresponding axes to produce shape (4, 3)."
                            }
                        ]
                    }
                },
                {
                    "module_number": 2,
                    "phase_name": "Phase 1: Mathematics & Data Science Foundations",
                    "title": "Data Wrangling & Feature Engineering (Pandas)",
                    "description": "Clean datasets, handle missing values, encode categorical variables, group data, and normalize numerical features.",
                    "skills": ["Pandas", "Feature Engineering", "Data Cleaning"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 2,
                            "title": "Pandas DataFrames, GroupBy Aggregations & Imputation",
                            "description": "Master DataFrame transformations, handling NaNs, one-hot encoding, and feature scaling with Scikit-Learn.",
                            "video_url": "https://www.youtube.com/embed/vmEHCJofslg",
                            "video_duration": "30 min",
                            "content": "### Feature Engineering for AI Models\n\nMachine learning models require clean, normalized numerical inputs. Data preparation involves handling missing values, encoding categoricals, and feature scaling.",
                            "key_concepts": ["DataFrame indexing with .loc and .iloc", "Handling missing data (dropna, fillna, KNNImputer)", "One-Hot vs Target encoding", "StandardScaler vs MinMaxScaler"],
                            "code_snippet": "import pandas as pd\nfrom sklearn.preprocessing import StandardScaler\n\ndf = pd.DataFrame({'age': [25, 30, 45], 'salary': [50000, 75000, 120000]})\nscaler = StandardScaler()\ndf[['age_scaled', 'salary_scaled']] = scaler.fit_transform(df[['age', 'salary']])\nprint(df)",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 2 Assessment: Pandas & Feature Engineering",
                        "description": "Assess data manipulation, encoding, and feature scaling techniques.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Why must feature scaling transformers (like StandardScaler) be fit strictly on the Training set and only transformed on the Test set?",
                                "options": [
                                    "To prevent Data Leakage from the test set into model training.",
                                    "Because test sets cannot contain floats.",
                                    "To make Python faster.",
                                    "It is a restriction of CSV files."
                                ],
                                "correct_index": 0,
                                "explanation": "Fitting on test data leaks test distribution statistics into the training process."
                            }
                        ]
                    }
                },
                {
                    "module_number": 3,
                    "phase_name": "Phase 1: Mathematics & Data Science Foundations",
                    "title": "Mathematics for AI: Linear Algebra & Calculus",
                    "description": "Master eigenvalues, eigenvectors, partial derivatives, gradient descent, loss functions, and probability distributions.",
                    "skills": ["Mathematics for AI", "Linear Algebra", "Calculus"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 3,
                            "title": "Gradients, Chain Rule & Loss Function Optimization",
                            "description": "Understand partial derivatives, Jacobian matrices, gradient descent variants (SGD, Adam), and convex optimization.",
                            "video_url": "https://www.youtube.com/embed/IHZwWFHWa-w",
                            "video_duration": "32 min",
                            "content": "### Mathematical Foundations of Neural Optimization\n\nNeural networks learn by minimizing a loss function with respect to weights using Backpropagation, which relies on the calculus Chain Rule.",
                            "key_concepts": ["Partial derivatives and gradient vectors", "Calculus Chain Rule for composite functions", "Gradient Descent update rule: $w = w - \\eta \\nabla L$", "Adam & RMSProp adaptive learning rate optimizers"],
                            "code_snippet": "# Gradient Descent Step in Python\ndef gradient_descent_step(w, gradient, learning_rate=0.01):\n    return w - learning_rate * gradient",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 3 Assessment: Mathematics for AI",
                        "description": "Test understanding of gradients, derivatives, and vector projections.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "In neural network optimization, what mathematical rule enables computing the gradient of the loss with respect to early layer weights?",
                                "options": ["The Chain Rule of Calculus", "Bayes' Theorem", "L'Hopital's Rule", "Pythagorean Theorem"],
                                "correct_index": 0,
                                "explanation": "The Chain Rule allows backpropagating error derivatives backwards through nested layer functions."
                            }
                        ]
                    }
                },
                {
                    "module_number": 4,
                    "phase_name": "Phase 2: Machine Learning Foundations",
                    "title": "Supervised & Unsupervised Machine Learning",
                    "description": "Implement Linear/Logistic Regression, Decision Trees, Random Forests, XGBoost, K-Means Clustering, and PCA.",
                    "skills": ["Machine Learning", "Scikit-Learn", "XGBoost"],
                    "estimated_hours": 6.0,
                    "lessons": [
                        {
                            "lesson_number": 4,
                            "title": "Ensemble Methods: Random Forests & Gradient Boosting (XGBoost)",
                            "description": "Master Bagging vs Boosting, tree pruning, learning rates, residual fitting, and hyperparameters.",
                            "video_url": "https://www.youtube.com/embed/g9c66TUylZ4",
                            "video_duration": "30 min",
                            "content": "### Ensemble Learning Algorithms\n\nEnsemble methods combine multiple weak learners to produce a strong predictive model. Random Forests use bagging to reduce variance, while XGBoost uses sequential gradient boosting to reduce bias.",
                            "key_concepts": ["Bias-Variance tradeoff", "Random Forest bootstrap aggregation (Bagging)", "Gradient Boosting & XGBoost residual minimization", "K-Means clustering and inertia curves"],
                            "code_snippet": "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import classification_report\n\nclf = RandomForestClassifier(n_estimators=100, random_state=42)\nclf.fit(X_train, y_train)\npredictions = clf.predict(X_test)\nprint(classification_report(y_test, predictions))",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 4 Assessment: Machine Learning Models",
                        "description": "Evaluate model selection, ensemble algorithms, and clustering.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the primary mechanism of Gradient Boosting (e.g. XGBoost)?",
                                "options": [
                                    "Training trees sequentially, where each new tree fits on the residual errors (pseudo-residuals) of previous trees.",
                                    "Averaging completely independent random trees.",
                                    "Clustering unlabelled points with Euclidean distance.",
                                    "Inverting a covariance matrix."
                                ],
                                "correct_index": 0,
                                "explanation": "Gradient boosting trains decision trees sequentially to minimize residual loss."
                            }
                        ]
                    }
                },
                {
                    "module_number": 5,
                    "phase_name": "Phase 2: Machine Learning Foundations",
                    "title": "Model Evaluation, Validation & Tuning",
                    "description": "Evaluate models using Precision, Recall, F1-Score, ROC-AUC curves, K-Fold cross-validation, and Optuna hyperparameter tuning.",
                    "skills": ["Model Evaluation", "Cross-Validation", "Optuna"],
                    "estimated_hours": 5.0,
                    "lessons": [
                        {
                            "lesson_number": 5,
                            "title": "Precision, Recall, ROC-AUC & Stratified K-Fold",
                            "description": "Understand confusion matrix metrics, threshold tuning, PR-curves for imbalanced datasets, and hyperparameter search.",
                            "video_url": "https://www.youtube.com/embed/4jRBRDbJemM",
                            "video_duration": "28 min",
                            "content": "### Rigorous Model Evaluation\n\nAccuracy is misleading on imbalanced datasets. Precision measures false positives, Recall measures false negatives, and the F1-Score provides their harmonic mean.",
                            "key_concepts": ["Confusion matrix metrics (TP, FP, TN, FN)", "Precision vs Recall tradeoff & F1-Score", "ROC Curve & Area Under the Curve (AUC)", "Stratified K-Fold Cross-Validation"],
                            "code_snippet": "from sklearn.metrics import roc_auc_score\n\n# Calculate ROC-AUC score\nauc_score = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])\nprint(f\"Model ROC-AUC: {auc_score:.3f}\")",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 5 Assessment: Model Evaluation",
                        "description": "Assess metric selection, threshold tuning, and cross-validation.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "When building a model to detect severe medical anomalies where missing a positive case is catastrophic, which metric should be prioritized?",
                                "options": ["High Precision", "High Recall (Sensitivity)", "High Specificity", "Low Accuracy"],
                                "correct_index": 1,
                                "explanation": "High Recall minimizes False Negatives, ensuring positive cases are not missed."
                            }
                        ]
                    }
                },
                {
                    "module_number": 6,
                    "phase_name": "Phase 2: Machine Learning Foundations",
                    "title": "Deep Learning & Neural Networks with PyTorch",
                    "description": "Construct Multi-Layer Perceptrons, activation functions (ReLU, GELU), loss functions (CrossEntropy), and backpropagation in PyTorch.",
                    "skills": ["Deep Learning", "PyTorch", "Neural Networks"],
                    "estimated_hours": 6.5,
                    "lessons": [
                        {
                            "lesson_number": 6,
                            "title": "PyTorch Tensors, Autograd & Training Loops",
                            "description": "Build custom PyTorch `nn.Module` classes, forward passes, `loss.backward()`, and optimizer step cycles.",
                            "video_url": "https://www.youtube.com/embed/V_xro1bcAuA",
                            "video_duration": "35 min",
                            "content": "### Building Neural Networks with PyTorch\n\nPyTorch is the leading deep learning framework in AI research and industry. PyTorch's dynamic computational graph (`autograd`) automatically tracks tensor operations and computes backward gradients.",
                            "key_concepts": ["PyTorch Tensors & GPU CUDA acceleration", "torch.nn.Module and forward() method", "Activation functions (ReLU, Sigmoid, Softmax, GELU)", "Training loop pattern (zero_grad -> forward -> backward -> step)"],
                            "code_snippet": "import torch\nimport torch.nn as nn\n\nclass Classifier(nn.Module):\n    def __init__(self, in_features, hidden_dim, num_classes):\n        super().__init__()\n        self.net = nn.Sequential(\n            nn.Linear(in_features, hidden_dim),\n            nn.ReLU(),\n            nn.Dropout(0.2),\n            nn.Linear(hidden_dim, num_classes)\n        )\n    def forward(self, x):\n        return self.net(x)",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 6 Assessment: PyTorch & Neural Networks",
                        "description": "Test PyTorch tensor operations, autograd, and training loops.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Why must `optimizer.zero_grad()` be called before `loss.backward()` in a standard PyTorch training step?",
                                "options": [
                                    "Because PyTorch accumulates gradients across backward passes by default, which would lead to incorrect gradient values if not zeroed.",
                                    "To free up GPU VRAM entirely.",
                                    "To randomize weights.",
                                    "It is only required for convolutional layers."
                                ],
                                "correct_index": 0,
                                "explanation": "PyTorch accumulates gradients by default; calling zero_grad resets them before the next pass."
                            }
                        ]
                    }
                },
                {
                    "module_number": 7,
                    "phase_name": "Phase 3: Deep Learning Architectures",
                    "title": "Computer Vision & Convolutional Neural Networks (CNNs)",
                    "description": "Master convolutions, pooling layers, ResNet residual connections, image augmentation, and transfer learning in PyTorch.",
                    "skills": ["Computer Vision", "CNNs", "PyTorch"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 7,
                            "title": "Convolutional Filters, ResNet & Transfer Learning",
                            "description": "Understand kernel filters, stride, padding, vanishing gradient resolution with residual skip connections, and fine-tuning pretrained models.",
                            "video_url": "https://www.youtube.com/embed/vT1JzLTH4G4",
                            "video_duration": "30 min",
                            "content": "### Convolutional Neural Networks for Visual Processing\n\nCNNs exploit spatial locality in images through convolution kernels that extract hierarchical features (edges -> textures -> parts -> objects).",
                            "key_concepts": ["2D Convolutions, Stride & Padding", "Max Pooling vs Average Pooling", "ResNet skip connections $F(x) + x$", "Fine-tuning pretrained Vision models"],
                            "code_snippet": "import torchvision.models as models\n\n# Transfer learning with ResNet-50\nmodel = models.resnet50(pretrained=True)\nfor param in model.parameters():\n    param.requires_grad = False\n# Replace classification head\nmodel.fc = nn.Linear(model.fc.in_features, 10)",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 7 Assessment: Computer Vision",
                        "description": "Evaluate understanding of convolutional layers and transfer learning.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What fundamental problem do residual skip connections ($F(x) + x$) solve in deep ResNet networks?",
                                "options": [
                                    "They solve the vanishing/exploding gradient problem, allowing gradients to flow directly back through deep layers.",
                                    "They convert 2D images into text.",
                                    "They eliminate the need for activation functions.",
                                    "They compress images on disk."
                                ],
                                "correct_index": 0,
                                "explanation": "Skip connections provide identity gradient shortcuts, preventing gradient degradation in very deep networks."
                            }
                        ]
                    }
                },
                {
                    "module_number": 8,
                    "phase_name": "Phase 3: Deep Learning Architectures",
                    "title": "Natural Language Processing (NLP) & Tokenization",
                    "description": "Learn text preprocessing, BPE/WordPiece tokenization, word embeddings (Word2Vec), RNNs, LSTMs, and sequence-to-sequence models.",
                    "skills": ["Natural Language Processing (NLP)", "Tokenization", "Embeddings"],
                    "estimated_hours": 5.5,
                    "lessons": [
                        {
                            "lesson_number": 8,
                            "title": "Subword Tokenization (BPE) & Dense Vector Embeddings",
                            "description": "Understand Byte-Pair Encoding (BPE), vocabulary indices, embedding lookup layers, and cosine similarity.",
                            "video_url": "https://www.youtube.com/embed/zJW57aCBCTk",
                            "video_duration": "28 min",
                            "content": "### NLP Foundations & Embeddings\n\nComputers cannot read text directly. NLP pipelines tokenize strings into integer IDs and map them to high-dimensional continuous embedding spaces where semantically similar words cluster together.",
                            "key_concepts": ["Subword tokenizers (BPE, WordPiece, SentencePiece)", "Dense embedding vectors & dimensionality", "Cosine similarity metric", "Seq2Seq architecture and attention mechanisms"],
                            "code_snippet": "from sentence_transformers import SentenceTransformer, util\n\nmodel = SentenceTransformer('all-MiniLM-L6-v2')\nemb1 = model.encode(\"How to learn AI Engineering?\")\nemb2 = model.encode(\"Guide to master artificial intelligence\")\n\nsimilarity = util.cos_sim(emb1, emb2)\nprint(f\"Semantic Cosine Similarity: {similarity.item():.4f}\") # ~0.85",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 8 Assessment: NLP & Embeddings",
                        "description": "Test subword tokenization and vector similarity mathematics.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "Which metric computes the cosine of the angle between two embedding vectors to evaluate semantic closeness?",
                                "options": ["Euclidean L1 distance", "Cosine Similarity", "Hamming Distance", "Jaccard Index"],
                                "correct_index": 1,
                                "explanation": "Cosine similarity measures vector directional alignment, invariant to vector magnitude."
                            }
                        ]
                    }
                },
                {
                    "module_number": 9,
                    "phase_name": "Phase 4: Generative AI, LLMs & RAG",
                    "title": "Transformer Architecture & Self-Attention",
                    "description": "Master Multi-Head Self-Attention, Positional Encoding, Encoder-Decoder stacks, and the 'Attention Is All You Need' foundation.",
                    "skills": ["Transformers", "Self-Attention", "Deep Learning"],
                    "estimated_hours": 6.5,
                    "lessons": [
                        {
                            "lesson_number": 9,
                            "title": "Multi-Head Attention: Query, Key, Value Mathematics",
                            "description": "Step-by-step mathematical breakdown of Scaled Dot-Product Attention: $Attention(Q, K, V) = \\text{softmax}(QK^T / \\sqrt{d_k}) V$.",
                            "video_url": "https://www.youtube.com/embed/kCc8FmEb1nY",
                            "video_duration": "35 min",
                            "content": "### The Transformer Revolution\n\nIntroduced in 2017, the Transformer architecture replaced sequential RNNs with parallel Multi-Head Self-Attention, allowing models to compute relationships between all tokens in a sequence simultaneously.",
                            "key_concepts": ["Query (Q), Key (K), and Value (V) projections", "Scaled Dot-Product Attention equation", "Positional encodings (Sinusoidal & RoPE)", "LayerNorm and residual feed-forward sublayers"],
                            "code_snippet": "import torch\nimport torch.nn.functional as F\n\ndef scaled_dot_product_attention(Q, K, V):\n    d_k = Q.size(-1)\n    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)\n    attention_weights = F.softmax(scores, dim=-1)\n    return torch.matmul(attention_weights, V), attention_weights",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 9 Assessment: Transformers & Attention",
                        "description": "Validate your mathematical understanding of Scaled Dot-Product Attention.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "In Scaled Dot-Product Attention, why are attention scores divided by $\\sqrt{d_k}$ before applying softmax?",
                                "options": [
                                    "To prevent dot products from growing excessively large for large dimensions, which would push softmax into regions with vanishingly small gradients.",
                                    "To convert negative numbers to positive.",
                                    "To make attention scores sum to zero.",
                                    "To fit within 8-bit integers."
                                ],
                                "correct_index": 0,
                                "explanation": "Scaling by sqrt(d_k) stabilizes softmax gradients during backpropagation."
                            }
                        ]
                    }
                },
                {
                    "module_number": 10,
                    "phase_name": "Phase 4: Generative AI, LLMs & RAG",
                    "title": "Large Language Models (LLMs) & Prompt Engineering",
                    "description": "Master autoregressive LLMs (GPT, LLaMA, Claude), prompt engineering techniques (Few-Shot, CoT), structured JSON generation, and function calling.",
                    "skills": ["Large Language Models (LLMs)", "Prompt Engineering", "Function Calling"],
                    "estimated_hours": 6.0,
                    "lessons": [
                        {
                            "lesson_number": 10,
                            "title": "Advanced Prompt Engineering & Structured Outputs",
                            "description": "Learn Zero-Shot, Few-Shot, Chain-of-Thought (CoT), system instructions, and enforcing guaranteed Pydantic JSON schemas.",
                            "video_url": "https://www.youtube.com/embed/jC4v5AS4RIM",
                            "video_duration": "30 min",
                            "content": "### Generative AI & Foundation Models\n\nModern AI applications leverage foundation LLMs to generate code, summarize documents, extract structured schemas, and orchestrate agentic tool execution.",
                            "key_concepts": ["Autoregressive decoding & temperature / top_p sampling", "Few-Shot prompting and Chain-of-Thought (CoT)", "Tool / Function calling protocols", "Structured JSON output validation"],
                            "code_snippet": "prompt = \"\"\"\nYou are an expert career AI advisor. Analyze the user's current skills and return a JSON object with: \n- 'readiness_score': int between 0-100\n- 'top_skill_gap': string\n- 'recommended_course': string\n\"\"\"",
                            "code_language": "text"
                        }
                    ],
                    "assessment": {
                        "title": "Module 10 Assessment: LLMs & Prompting",
                        "description": "Assess LLM sampling parameters and structured generation patterns.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What effect does lowering the `temperature` parameter (e.g. from 0.8 to 0.1) have on LLM generation?",
                                "options": [
                                    "It makes responses more deterministic, focused, and repeatable by favoring high-probability tokens.",
                                    "It causes the LLM to hallucinate more creative answers.",
                                    "It speeds up network bandwidth.",
                                    "It doubles the context window."
                                ],
                                "correct_index": 0,
                                "explanation": "Low temperature concentrates probability distribution onto the highest likelihood tokens, making output deterministic."
                            }
                        ]
                    }
                },
                {
                    "module_number": 11,
                    "phase_name": "Phase 4: Generative AI, LLMs & RAG",
                    "title": "Retrieval-Augmented Generation (RAG) & Vector Databases",
                    "description": "Architect end-to-end RAG systems using chunking strategies, vector databases (Chroma, Pinecone, Qdrant), hybrid search, and re-ranking.",
                    "skills": ["RAG Systems", "Vector Databases", "Semantic Search"],
                    "estimated_hours": 6.5,
                    "lessons": [
                        {
                            "lesson_number": 11,
                            "title": "End-to-End RAG: Chunking, Vector Storage & Semantic Search",
                            "description": "Learn semantic chunking, cosine distance queries in vector databases, context injection, and cross-encoder re-ranking.",
                            "video_url": "https://www.youtube.com/embed/wSTg8r_zZtE",
                            "video_duration": "32 min",
                            "content": "### Retrieval-Augmented Generation (RAG) Architecture\n\nRAG overcomes LLM knowledge cutoffs and hallucinations by dynamically retrieving relevant internal documentation and injecting it into the prompt context.",
                            "key_concepts": ["Document chunking strategies (fixed size, recursive, semantic)", "Vector database indexing (HNSW, IVF-Flat)", "Similarity search & Cosine / Dot product metrics", "Re-ranking retrieved chunks with Cross-Encoders"],
                            "code_snippet": "# RAG Context Injection Pattern\ndef build_rag_prompt(user_query: str, retrieved_chunks: list[str]) -> str:\n    context = \"\\n---\\n\".join(retrieved_chunks)\n    return f\"\"\"Context information is below.\n---------------------\n{context}\n---------------------\nGiven the context above and no other information, answer the query: {user_query}\"\"\"",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 11 Assessment: RAG & Vector DBs",
                        "description": "Test vector indexing (HNSW), chunking methods, and RAG retrieval pipelines.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "What is the primary motivation for implementing a RAG (Retrieval-Augmented Generation) system instead of retraining an LLM?",
                                "options": [
                                    "It grounds responses in proprietary, up-to-date documentation at low cost without expensive full-model retraining.",
                                    "RAG eliminates the need for Python.",
                                    "RAG models don't use GPUs.",
                                    "It translates languages automatically."
                                ],
                                "correct_index": 0,
                                "explanation": "RAG injects relevant external context at inference time, avoiding the enormous cost of re-training foundation models."
                            }
                        ]
                    }
                },
                {
                    "module_number": 12,
                    "phase_name": "Phase 4: Generative AI, LLMs & RAG",
                    "title": "AI Model Deployment & Capstone AI Project",
                    "description": "Deploy AI services using FastAPI, Docker, streaming responses (Server-Sent Events), token tracking, and build a capstone Generative AI product.",
                    "skills": ["AI Applications", "Model Deployment", "FastAPI AI", "Capstone Project"],
                    "estimated_hours": 8.0,
                    "lessons": [
                        {
                            "lesson_number": 12,
                            "title": "Deploying Generative AI Services with Streaming & Caching",
                            "description": "Implement streaming completions with AsyncGenerators, semantic caching, rate limiting, and observability.",
                            "video_url": "https://www.youtube.com/embed/nAmC7SoVLvw",
                            "video_duration": "35 min",
                            "content": "### Production AI Application Engineering\n\nDeploying AI systems in production requires optimizing token costs, latency (using token streaming with Server-Sent Events), and managing vector store connections.",
                            "key_concepts": ["Streaming token generation with SSE (`EventSource`)", "Semantic caching to reduce LLM API bills", "Latency & token usage observability", "Packaging AI microservices into Docker containers"],
                            "code_snippet": "from fastapi.responses import StreamingResponse\n\nasync def stream_ai_generator(prompt: str):\n    # Simulate token streaming\n    for token in [\"PathPilot \", \"AI \", \"is \", \"generating \", \"your \", \"roadmap.\"]:\n        yield f\"data: {token}\\n\\n\"\n        await asyncio.sleep(0.05)\n\n@app.get(\"/api/ai/stream\")\ndef stream_ai_endpoint():\n    return StreamingResponse(stream_ai_generator(\"query\"), media_type=\"text/event-stream\")",
                            "code_language": "python"
                        }
                    ],
                    "assessment": {
                        "title": "Module 12 Assessment: AI Production Mastery",
                        "description": "Validate AI system deployment and production readiness.",
                        "time_minutes": 15,
                        "questions": [
                            {
                                "question_text": "How does token streaming via Server-Sent Events (SSE) improve user experience in generative AI applications?",
                                "options": [
                                    "It reduces Time-To-First-Token (TTFT), displaying words progressively to the user as they are generated rather than waiting for the complete completion.",
                                    "It bypasses all cloud API costs.",
                                    "It translates audio into video.",
                                    "It eliminates GPU memory requirements."
                                ],
                                "correct_index": 0,
                                "explanation": "Streaming delivers immediate perceived responsiveness by sending tokens as soon as they are computed."
                            }
                        ]
                    }
                }
            ],
            "final_assessment": {
                "title": "AI Engineer Comprehensive Final Exam",
                "description": "Comprehensive 10-question evaluation covering NumPy, Machine Learning, PyTorch, Deep Learning, NLP, Transformers, LLMs, and RAG Systems.",
                "time_minutes": 45,
                "passing_score": 70.0,
                "questions": [
                    {
                        "question_text": "In PyTorch, which method computes the gradient of tensor $y$ with respect to all graph leaves with `requires_grad=True`?",
                        "options": ["y.backward()", "y.gradient()", "y.forward()", "y.zero_grad()"],
                        "correct_index": 0,
                        "topic": "PyTorch",
                        "explanation": "y.backward() traverses the autograd computation graph to calculate vector-Jacobian products."
                    },
                    {
                        "question_text": "What is the primary advantage of Multi-Head Self-Attention compared to Single-Head Attention in Transformers?",
                        "options": [
                            "It allows the model to jointly attend to information from different representation subspaces at different positions.",
                            "It halves the number of model weights.",
                            "It eliminates the need for token embeddings.",
                            "It prevents GPU usage."
                        ],
                        "correct_index": 0,
                        "topic": "Transformers",
                        "explanation": "Multi-head attention projects Queries, Keys, and Values into multiple subspaces to capture diverse linguistic patterns."
                    },
                    {
                        "question_text": "In a RAG system, what algorithm is most commonly used for Approximate Nearest Neighbor (ANN) vector search in vector databases?",
                        "options": ["HNSW (Hierarchical Navigable Small World)", "Bubble Sort", "Dijkstra's Algorithm", "Binary Search"],
                        "correct_index": 0,
                        "topic": "Vector DBs",
                        "explanation": "HNSW is a graph-based indexing algorithm providing rapid, high-recall approximate nearest neighbor search."
                    }
                ]
            }
        }
    ]

    for cdata in courses_data:
        slug = cdata["slug"]
        course = db.query(CourseTrack).filter(CourseTrack.slug == slug).first()
        if not course:
            course = CourseTrack(
                slug=slug,
                title=cdata["title"],
                tagline=cdata["tagline"],
                description=cdata["description"],
                career_name=cdata["career_name"],
                difficulty=cdata["difficulty"],
                estimated_duration=cdata["estimated_duration"],
                total_modules=len(cdata["modules"]),
                total_lessons=sum(len(m["lessons"]) for m in cdata["modules"]),
                total_projects=cdata["total_projects"],
                total_assessments=len(cdata["modules"]),
                skills_covered=cdata["skills_covered"],
                image_url=cdata["image_url"],
            )
            db.add(course)
            db.flush()
            print(f"Created CourseTrack: {course.title} (ID: {course.id})")
        else:
            # Update metadata
            course.title = cdata["title"]
            course.tagline = cdata["tagline"]
            course.description = cdata["description"]
            course.career_name = cdata["career_name"]
            course.difficulty = cdata["difficulty"]
            course.skills_covered = cdata["skills_covered"]
            course.image_url = cdata["image_url"]
            course.total_modules = len(cdata["modules"])
            course.total_lessons = sum(len(m["lessons"]) for m in cdata["modules"])
            db.flush()

        # Seed Modules
        for mdata in cdata["modules"]:
            mod = (
                db.query(CourseModule)
                .filter(CourseModule.course_id == course.id, CourseModule.module_number == mdata["module_number"])
                .first()
            )
            if not mod:
                mod = CourseModule(
                    course_id=course.id,
                    module_number=mdata["module_number"],
                    phase_name=mdata["phase_name"],
                    title=mdata["title"],
                    description=mdata["description"],
                    skills=mdata["skills"],
                    estimated_hours=mdata["estimated_hours"],
                )
                db.add(mod)
                db.flush()
            else:
                mod.phase_name = mdata["phase_name"]
                mod.title = mdata["title"]
                mod.description = mdata["description"]
                mod.skills = mdata["skills"]
                mod.estimated_hours = mdata["estimated_hours"]
                db.flush()

            # Seed Lessons
            for ldata in mdata["lessons"]:
                les = (
                    db.query(CourseLesson)
                    .filter(CourseLesson.module_id == mod.id, CourseLesson.lesson_number == ldata["lesson_number"])
                    .first()
                )
                if not les:
                    les = CourseLesson(
                        module_id=mod.id,
                        lesson_number=ldata["lesson_number"],
                        title=ldata["title"],
                        description=ldata["description"],
                        video_url=ldata["video_url"],
                        video_duration=ldata["video_duration"],
                        thumbnail_url=ldata.get("thumbnail_url"),
                        content=ldata["content"],
                        key_concepts=ldata["key_concepts"],
                        code_snippet=ldata.get("code_snippet"),
                        code_language=ldata.get("code_language", "javascript"),
                        resources=ldata.get("resources", []),
                        learning_objectives=ldata.get("learning_objectives", []),
                    )
                    db.add(les)
                else:
                    les.title = ldata["title"]
                    les.description = ldata["description"]
                    les.video_url = ldata["video_url"]
                    les.video_duration = ldata["video_duration"]
                    les.content = ldata["content"]
                    les.key_concepts = ldata["key_concepts"]
                    les.code_snippet = ldata.get("code_snippet")
                    les.code_language = ldata.get("code_language", "javascript")

            # Seed Module Assessment
            adata = mdata.get("assessment")
            if adata:
                massess = db.query(ModuleAssessment).filter(ModuleAssessment.module_id == mod.id).first()
                if not massess:
                    massess = ModuleAssessment(
                        module_id=mod.id,
                        title=adata["title"],
                        description=adata["description"],
                        time_minutes=adata["time_minutes"],
                        passing_score=70.0,
                    )
                    db.add(massess)
                    db.flush()
                else:
                    massess.title = adata["title"]
                    massess.description = adata["description"]
                    massess.time_minutes = adata["time_minutes"]
                    db.flush()

                # Questions
                for qdata in adata.get("questions", []):
                    q = (
                        db.query(AssessmentQuestion)
                        .filter(AssessmentQuestion.assessment_id == massess.id, AssessmentQuestion.question_text == qdata["question_text"])
                        .first()
                    )
                    if not q:
                        q = AssessmentQuestion(
                            assessment_id=massess.id,
                            question_text=qdata["question_text"],
                            options=qdata["options"],
                            correct_index=qdata["correct_index"],
                            explanation=qdata["explanation"],
                        )
                        db.add(q)

        # Seed Final Assessment
        fdata = cdata.get("final_assessment")
        if fdata:
            fassess = db.query(CourseFinalAssessment).filter(CourseFinalAssessment.course_id == course.id).first()
            if not fassess:
                fassess = CourseFinalAssessment(
                    course_id=course.id,
                    title=fdata["title"],
                    description=fdata["description"],
                    time_minutes=fdata["time_minutes"],
                    passing_score=fdata["passing_score"],
                )
                db.add(fassess)
                db.flush()
            else:
                fassess.title = fdata["title"]
                fassess.description = fdata["description"]
                fassess.time_minutes = fdata["time_minutes"]
                db.flush()

            for qdata in fdata.get("questions", []):
                fq = (
                    db.query(CourseFinalQuestion)
                    .filter(CourseFinalQuestion.final_assessment_id == fassess.id, CourseFinalQuestion.question_text == qdata["question_text"])
                    .first()
                )
                if not fq:
                    fq = CourseFinalQuestion(
                        final_assessment_id=fassess.id,
                        question_text=qdata["question_text"],
                        options=qdata["options"],
                        correct_index=qdata["correct_index"],
                        topic=qdata["topic"],
                        explanation=qdata["explanation"],
                    )
                    db.add(fq)

    db.commit()
    print("5 Career Courses seeded successfully!")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_learning_courses(db)
    finally:
        db.close()
