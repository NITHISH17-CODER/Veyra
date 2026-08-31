import React from 'react';
import { useNavigate } from 'react-router-dom';
import { LandingNavbar } from '../components/layout/LandingNavbar';
import { LandingFooter } from '../components/layout/LandingFooter';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import {
  Sparkles,
  ArrowRight,
  User,
  Cpu,
  BarChart2,
  Compass,
  Map,
  FolderGit2,
  TrendingUp,
  Check,
  Shield,
  Code,
  Terminal,
  Brain,
  FileText,
  Award,
  CheckCircle2
} from 'lucide-react';

export const LandingPage = () => {
  const navigate = useNavigate();

  const scrollToSection = (id) => {
    const el = document.getElementById(id);
    if (el) {
      const navOffset = 70;
      const elementPosition = el.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - navOffset;
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  // 11 Real PathPilot Application Features
  const featuresList = [
    {
      icon: Compass,
      title: 'Personalized Career Path',
      description: 'Veyra analyzes your background, skills, interests, and goals to build a custom career path tailored to your ambitions.'
    },
    {
      icon: Cpu,
      title: 'AI Profile Analysis',
      description: 'Instant AI auditing of your resume, GitHub repositories, and LinkedIn profile to pinpoint existing strengths and growth areas.'
    },
    {
      icon: Map,
      title: 'Personalized Learning Roadmap',
      description: 'Structured step-by-step curriculum broken down into sequential phases, modules, video/text lessons, and skill checkpoints.'
    },
    {
      icon: BarChart2,
      title: 'Skill Gap Analysis',
      description: 'Automated evaluation identifying your current competencies versus industry expectations for your target role.'
    },
    {
      icon: TrendingUp,
      title: 'Learning Progress',
      description: 'Real-time progress tracking, activity heatmaps, streak monitoring, and milestone completion metrics.'
    },
    {
      icon: FolderGit2,
      title: 'Hands-on Projects',
      description: 'Practical Basic, Intermediate, and Advanced portfolio projects with real-world instructions and starter templates.'
    },
    {
      icon: CheckCircle2,
      title: 'Skill Assessments',
      description: 'Comprehensive interactive MCQ tests and coding challenges to measure and validate true technical comprehension.'
    },
    {
      icon: Terminal,
      title: 'GitHub / Colab Verification',
      description: 'Automated project submission verification via public GitHub repositories or Google Colab notebook links.'
    },
    {
      icon: Sparkles,
      title: 'AI Learning Assistant',
      description: 'Context-aware Veyra AI chatbot that understands your current page, active lesson, learning path, and progress.'
    },
    {
      icon: Award,
      title: 'Certificates',
      description: 'Formally issued verifiable certificates upon completing courses and capstone projects.'
    },
    {
      icon: FileText,
      title: 'Technical News',
      description: 'Curated daily technology news and industry updates personalized to your chosen career path.'
    }
  ];

  // 8 Real PathPilot Workflow Steps
  const howItWorksSteps = [
    {
      step: '01',
      title: 'Tell us about yourself',
      description: 'Share your educational background, current job search status, and learning preferences to customize your starting point.'
    },
    {
      step: '02',
      title: 'Define your goal',
      description: 'Specify your target role or career ambition in simple, natural language.'
    },
    {
      step: '03',
      title: 'Analyze your skills',
      description: 'Upload your resume or link GitHub/LinkedIn so AI can audit your current competencies and experience.'
    },
    {
      step: '04',
      title: 'Generate your personalized path',
      description: 'Receive an AI-generated phase-by-phase learning sequence engineered specifically for your skill level.'
    },
    {
      step: '05',
      title: 'Learn through roadmap + lessons',
      description: 'Master interactive video and text lessons with integrated code execution environments.'
    },
    {
      step: '06',
      title: 'Complete assessments',
      description: 'Validate your knowledge through module-level MCQ quizzes and coding evaluations.'
    },
    {
      step: '07',
      title: 'Build projects',
      description: 'Apply your skills by building hands-on portfolio projects with GitHub and Colab submission links.'
    },
    {
      step: '08',
      title: 'Earn certificates',
      description: 'Receive verifiable digital certificates upon completing your course and capstone projects.'
    }
  ];

  // Strictly 5 Core Career Paths Supported
  const careerPrograms = [
    {
      id: 'frontend',
      title: 'Frontend Developer',
      description: 'Learn to build responsive, accessible and modern web applications.',
      icon: Code,
      badge: 'Web Interfaces'
    },
    {
      id: 'backend',
      title: 'Backend Developer',
      description: 'Learn to build secure, scalable APIs, databases and server-side applications.',
      icon: Terminal,
      badge: 'Systems & APIs'
    },
    {
      id: 'cybersecurity',
      title: 'Cybersecurity',
      description: 'Learn security fundamentals, network defense, threat analysis and secure systems.',
      icon: Shield,
      badge: 'Security & Defense'
    },
    {
      id: 'sde',
      title: 'Software Development Engineer',
      description: 'Build strong programming, problem-solving, data structures and software engineering foundations.',
      icon: Cpu,
      badge: 'Core Engineering'
    },
    {
      id: 'ai',
      title: 'AI Engineer',
      description: 'Learn to build intelligent applications using machine learning, modern AI models and AI-powered systems.',
      icon: Brain,
      badge: 'AI & Models'
    }
  ];

  return (
    <div className="min-h-screen bg-white text-[#111827] flex flex-col font-sans selection:bg-[#146EF5] selection:text-white">
      {/* Sticky Top Navigation */}
      <LandingNavbar />

      {/* =========================================================================
          1. HERO SECTION (With Epic Mountain Path Background & Seamless Transparent Header)
         ========================================================================= */}
      <section className="relative min-h-screen flex flex-col justify-center items-center px-6 lg:px-12 border-b border-[#DCE6F2] overflow-hidden pt-24 pb-16 md:pt-32 md:pb-24">
        {/* Background Image Container */}
        <div className="absolute inset-0 z-0">
          <img
            src="/hero_mountain_bg.jpg"
            alt="Veyra Mountain Hero Path"
            className="w-full h-full object-cover object-center"
          />
          {/* Subtle lighting overlay for optimal contrast */}
          <div className="absolute inset-0 bg-gradient-to-r from-white/90 via-white/70 to-transparent lg:via-white/50" />
          <div className="absolute inset-0 bg-gradient-to-t from-white via-transparent to-white/40" />
        </div>

        <div className="max-w-7xl w-full mx-auto relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center my-auto">
          {/* Left Content Column */}
          <div className="lg:col-span-7 space-y-8 text-center lg:text-left">
            {/* Hero Headline */}
            <h1 className="hero-headline text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-[#111827] leading-[1.06]">
              Your Career Path,<br />
              <span className="bg-gradient-to-r from-[#111827] via-[#146EF5] to-[#0B5ED7] bg-clip-text text-transparent">
                Built Around You.
              </span>
            </h1>

            {/* Hero Description */}
            <p className="body-large max-w-2xl mx-auto lg:mx-0 font-medium text-[#475569] text-base sm:text-lg md:text-xl leading-relaxed">
              Veyra analyzes your goals, skills and experience to create a personalized roadmap for learning, projects and career growth.
            </p>

            {/* Hero CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
              <Button
                variant="primary"
                size="lg"
                icon={ArrowRight}
                iconPosition="right"
                onClick={() => navigate('/register')}
                className="shadow-xl shadow-blue-600/20"
              >
                Build My Path
              </Button>

              <Button
                variant="outline"
                size="lg"
                onClick={() => scrollToSection('how-it-works')}
                className="bg-white/80 backdrop-blur-md border-[#DCE6F2] text-[#111827] hover:bg-[#EAF3FF] hover:border-[#146EF5] hover:text-[#146EF5]"
              >
                Explore How It Works
              </Button>
            </div>
          </div>

          {/* Right Column: Floating Mountain Path Nodes */}
          <div className="lg:col-span-5 relative hidden lg:block h-[480px]">
            {/* Floating Badge 1: Career Growth */}
            <div className="absolute top-[8%] right-[5%] p-3.5 px-4 rounded-2xl bg-white/90 backdrop-blur-xl border border-[#DCE6F2] shadow-xl flex items-center gap-2.5 text-xs font-bold text-[#111827] animate-float transition-all hover:scale-105">
              <div className="w-6 h-6 rounded-xl bg-[#EAF3FF] text-[#146EF5] flex items-center justify-center">
                <TrendingUp className="w-3.5 h-3.5" />
              </div>
              <span>Career Growth</span>
            </div>

            {/* Floating Badge 2: Real Projects */}
            <div className="absolute top-[28%] right-[12%] p-3.5 px-4 rounded-2xl bg-white/90 backdrop-blur-xl border border-[#DCE6F2] shadow-xl flex items-center gap-2.5 text-xs font-bold text-[#111827] animate-float transition-all hover:scale-105" style={{ animationDelay: '1s' }}>
              <div className="w-6 h-6 rounded-xl bg-[#EAF3FF] text-[#146EF5] flex items-center justify-center">
                <FolderGit2 className="w-3.5 h-3.5" />
              </div>
              <span>Real Projects</span>
            </div>

            {/* Floating Badge 3: In-Demand Skills */}
            <div className="absolute top-[48%] right-[18%] p-3.5 px-4 rounded-2xl bg-white/90 backdrop-blur-xl border border-[#DCE6F2] shadow-xl flex items-center gap-2.5 text-xs font-bold text-[#111827] animate-float transition-all hover:scale-105" style={{ animationDelay: '2s' }}>
              <div className="w-6 h-6 rounded-xl bg-[#EAF3FF] text-[#146EF5] flex items-center justify-center">
                <Code className="w-3.5 h-3.5" />
              </div>
              <span>In-Demand Skills</span>
            </div>

            {/* Floating Badge 4: Personalized Roadmap */}
            <div className="absolute top-[68%] right-[24%] p-3.5 px-4 rounded-2xl bg-white/90 backdrop-blur-xl border border-[#DCE6F2] shadow-xl flex items-center gap-2.5 text-xs font-bold text-[#111827] animate-float transition-all hover:scale-105" style={{ animationDelay: '3s' }}>
              <div className="w-6 h-6 rounded-xl bg-[#EAF3FF] text-[#146EF5] flex items-center justify-center">
                <Map className="w-3.5 h-3.5" />
              </div>
              <span>Personalized Roadmap</span>
            </div>

            {/* Floating Badge 5: AI-Powered Insights */}
            <div className="absolute top-[88%] right-[30%] p-3.5 px-4 rounded-2xl bg-white/90 backdrop-blur-xl border border-[#DCE6F2] shadow-xl flex items-center gap-2.5 text-xs font-bold text-[#111827] animate-float transition-all hover:scale-105" style={{ animationDelay: '4s' }}>
              <div className="w-6 h-6 rounded-xl bg-[#EAF3FF] text-[#146EF5] flex items-center justify-center">
                <Sparkles className="w-3.5 h-3.5" />
              </div>
              <span>AI-Powered Insights</span>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          2. PATHPILOT INTELLIGENCE PIPELINE (Below Hero Viewport)
         ========================================================================= */}
      <section id="ai-pipeline" className="py-20 px-6 lg:px-12 bg-[#F5F9FF] border-b border-[#DCE6F2] scroll-mt-20">
        <div className="max-w-7xl mx-auto space-y-6">
          <div className="text-center space-y-2 max-w-2xl mx-auto">
            <span className="text-xs font-bold text-[#146EF5] uppercase tracking-wider">End-To-End Architecture</span>
            <h2 className="heading-section text-[#111827]">Veyra Intelligence Pipeline</h2>
            <p className="body-secondary text-[#475569]">
              How our AI engine transforms your profile into structured career growth.
            </p>
          </div>

          <div className="p-6 md:p-8 rounded-[32px] bg-white border border-[#DCE6F2] shadow-sm">
            <div className="flex items-center justify-between pb-6 mb-6 border-b border-[#DCE6F2]">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-[#146EF5]" />
                <span className="text-xs font-semibold text-[#111827] uppercase tracking-wider">Personalized Dynamic Flow</span>
              </div>
              <span className="text-xs text-[#64748B] font-mono">Live Auditing &amp; Execution</span>
            </div>

            {/* Responsive Visual Nodes Diagram */}
            <div className="grid grid-cols-2 md:grid-cols-7 gap-3 text-center">
              {/* Node 1 */}
              <div className="p-4 rounded-2xl bg-[#F5F9FF] border border-[#DCE6F2] flex flex-col items-center justify-center space-y-2">
                <User className="w-5 h-5 text-[#146EF5]" />
                <span className="text-xs font-bold text-[#111827]">User Profile</span>
              </div>

              {/* Node 2 */}
              <div className="p-4 rounded-2xl bg-[#F5F9FF] border border-[#DCE6F2] flex flex-col items-center justify-center space-y-2">
                <Cpu className="w-5 h-5 text-[#146EF5]" />
                <span className="text-xs font-bold text-[#111827]">AI Analysis</span>
              </div>

              {/* Node 3 */}
              <div className="p-4 rounded-2xl bg-[#F5F9FF] border border-[#DCE6F2] flex flex-col items-center justify-center space-y-2">
                <BarChart2 className="w-5 h-5 text-[#146EF5]" />
                <span className="text-xs font-bold text-[#111827]">Skill Gap</span>
              </div>

              {/* Node 4 */}
              <div className="p-4 rounded-2xl bg-[#F5F9FF] border border-[#DCE6F2] flex flex-col items-center justify-center space-y-2">
                <Compass className="w-5 h-5 text-[#146EF5]" />
                <span className="text-xs font-bold text-[#111827]">Career Path</span>
              </div>

              {/* Node 5 */}
              <div className="p-4 rounded-2xl bg-[#F5F9FF] border border-[#DCE6F2] flex flex-col items-center justify-center space-y-2">
                <Map className="w-5 h-5 text-[#146EF5]" />
                <span className="text-xs font-bold text-[#111827]">Learning Roadmap</span>
              </div>

              {/* Node 6 */}
              <div className="p-4 rounded-2xl bg-[#F5F9FF] border border-[#DCE6F2] flex flex-col items-center justify-center space-y-2">
                <FolderGit2 className="w-5 h-5 text-[#146EF5]" />
                <span className="text-xs font-bold text-[#111827]">Projects</span>
              </div>

              {/* Node 7 */}
              <div className="p-4 bg-[#146EF5] text-white rounded-2xl flex flex-col items-center justify-center space-y-2 col-span-2 md:col-span-1 shadow-md shadow-blue-500/20">
                <TrendingUp className="w-5 h-5 text-white" />
                <span className="text-xs font-bold text-white">Career Growth</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          3. FEATURES SECTION (#features)
         ========================================================================= */}
      <section id="features" className="py-24 px-6 lg:px-12 bg-white border-b border-[#DCE6F2] scroll-mt-20">
        <div className="max-w-7xl mx-auto space-y-16">
          <div className="max-w-2xl space-y-3">
            <span className="text-xs font-bold text-[#146EF5] uppercase tracking-wider">FEATURES</span>
            <h2 className="heading-section text-[#111827]">Everything you need to build your path.</h2>
            <p className="body-main text-[#475569]">
              Veyra combines intelligent profile auditing, personalized roadmaps, and practical execution into a unified career platform.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuresList.map((feat, idx) => {
              const IconComp = feat.icon;
              return (
                <div
                  key={idx}
                  className="p-6 rounded-2xl bg-white border border-[#DCE6F2] space-y-4 hover:border-[#146EF5] hover:-translate-y-1 hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-200 flex flex-col justify-between"
                >
                  <div className="space-y-3">
                    <div className="w-10 h-10 rounded-xl bg-[#EAF3FF] border border-[#146EF5]/20 flex items-center justify-center text-[#146EF5]">
                      <IconComp className="w-5 h-5" />
                    </div>
                    <h3 className="text-lg font-bold text-[#111827]">{feat.title}</h3>
                    <p className="body-secondary text-[#475569]">{feat.description}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* =========================================================================
          4. HOW IT WORKS SECTION (#how-it-works)
         ========================================================================= */}
      <section id="how-it-works" className="py-24 px-6 lg:px-12 bg-[#F5F9FF] border-b border-[#DCE6F2] scroll-mt-20">
        <div className="max-w-7xl mx-auto space-y-16">
          <div className="max-w-2xl space-y-3">
            <span className="text-xs font-bold text-[#146EF5] uppercase tracking-wider">METHODOLOGY</span>
            <h2 className="heading-section text-[#111827]">How Veyra Works</h2>
            <p className="body-main text-[#475569]">
              A structured 8-step methodology to turn your current experience into validated engineering expertise.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {howItWorksSteps.map((stepItem) => (
              <div
                key={stepItem.step}
                className="p-6 rounded-2xl bg-white border border-[#DCE6F2] space-y-4 flex flex-col justify-between hover:border-[#146EF5] hover:-translate-y-1 hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-200"
              >
                <div className="space-y-3">
                  <span className="text-3xl font-extrabold text-[#146EF5] block tracking-tight">{stepItem.step}</span>
                  <h3 className="text-base font-bold text-[#111827]">{stepItem.title}</h3>
                  <p className="body-secondary text-[#475569]">{stepItem.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* =========================================================================
          5. LEARNING PATHS SECTION (#learning-paths) - Clean White/Blue Grid
         ========================================================================= */}
      <section id="learning-paths" className="py-24 px-6 lg:px-12 bg-white border-b border-[#DCE6F2] scroll-mt-20">
        <div className="max-w-7xl mx-auto space-y-12">
          <div className="max-w-3xl space-y-3">
            <span className="text-xs font-bold text-[#146EF5] uppercase tracking-wider">SUPPORTED PROGRAMMING CAREERS</span>
            <h2 className="heading-section text-[#111827]">Available Learning Paths</h2>
            <p className="body-main text-[#475569]">
              Veyra supports five core specialized engineering programs. Your path will be personalized based on your background, skills, and target goals.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {careerPrograms.map((program) => {
              const IconComp = program.icon;
              return (
                <div
                  key={program.id}
                  className="p-6 rounded-2xl bg-white border border-[#DCE6F2] space-y-5 flex flex-col justify-between hover:border-[#146EF5] hover:-translate-y-1 hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-200"
                >
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="p-3 rounded-xl bg-[#EAF3FF] text-[#146EF5] border border-[#146EF5]/20">
                        <IconComp className="w-6 h-6 text-[#146EF5]" />
                      </div>
                      <Badge variant="blue">{program.badge}</Badge>
                    </div>

                    <div className="space-y-2">
                      <h3 className="text-lg font-bold text-[#111827]">{program.title}</h3>
                      <p className="body-secondary text-[#475569] text-xs leading-relaxed">{program.description}</p>
                    </div>
                  </div>

                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigate('/register')}
                    className="w-full mt-4 justify-center border-[#DCE6F2] hover:border-[#146EF5] hover:bg-[#EAF3FF] text-[#146EF5]"
                  >
                    Explore Path →
                  </Button>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* =========================================================================
          6. AI ANALYSIS SECTION (#ai-analysis)
         ========================================================================= */}
      <section id="ai-analysis" className="py-24 px-6 lg:px-12 bg-[#F5F9FF] border-b border-[#DCE6F2] scroll-mt-20">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <span className="text-xs font-bold text-[#146EF5] uppercase tracking-wider">AI INTELLIGENCE PIPELINE</span>
            <h2 className="heading-display text-[#111827]">
              Not another generic course list.
            </h2>
            <p className="body-large text-[#475569]">
              Veyra starts with you — understanding your complete background, skills, interests, and target career goals.
            </p>
            <div className="space-y-3 pt-2">
              <div className="flex items-center gap-3">
                <div className="w-5 h-5 rounded-full bg-[#146EF5] text-white flex items-center justify-center text-xs font-bold">✓</div>
                <span className="body-main font-semibold text-[#111827]">Analyzes background, skills, interests &amp; career goals</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-5 h-5 rounded-full bg-[#146EF5] text-white flex items-center justify-center text-xs font-bold">✓</div>
                <span className="body-main font-semibold text-[#111827]">Audits resume, GitHub repositories &amp; LinkedIn profiles</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-5 h-5 rounded-full bg-[#146EF5] text-white flex items-center justify-center text-xs font-bold">✓</div>
                <span className="body-main font-semibold text-[#111827]">Generates step-by-step roadmap with projects &amp; assessments</span>
              </div>
            </div>
            <div className="pt-4">
              <Button
                variant="primary"
                size="lg"
                icon={ArrowRight}
                iconPosition="right"
                onClick={() => navigate('/register')}
              >
                Analyze My Profile
              </Button>
            </div>
          </div>

          {/* Interactive AI Personalization Preview Card */}
          <div className="p-8 rounded-[32px] bg-white border border-[#DCE6F2] space-y-6 shadow-sm">
            <div className="flex items-center justify-between pb-4 border-b border-[#DCE6F2]">
              <span className="text-xs font-bold text-[#111827] uppercase tracking-wider">Profile Analysis Engine</span>
              <Badge variant="dark">AI Active</Badge>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-[#F5F9FF] border border-[#DCE6F2] space-y-1">
                <span className="text-xs font-semibold text-[#64748B]">Target Role</span>
                <p className="text-sm font-bold text-[#111827]">Backend Engineer</p>
              </div>
              <div className="p-4 rounded-xl bg-[#F5F9FF] border border-[#DCE6F2] space-y-1">
                <span className="text-xs font-semibold text-[#64748B]">Current Skills</span>
                <p className="text-sm font-bold text-[#111827]">Python, SQL, Git</p>
              </div>
              <div className="p-4 rounded-xl bg-[#F5F9FF] border border-[#DCE6F2] space-y-1">
                <span className="text-xs font-semibold text-[#64748B]">Audited Source</span>
                <p className="text-sm font-bold text-[#111827]">Resume ✓ GitHub ✓</p>
              </div>
              <div className="p-4 rounded-xl bg-[#F5F9FF] border border-[#DCE6F2] space-y-1">
                <span className="text-xs font-semibold text-[#64748B]">Identified Gap</span>
                <p className="text-sm font-bold text-[#111827]">FastAPI &amp; System Design</p>
              </div>
            </div>

            <div className="p-5 rounded-2xl bg-[#146EF5] text-white space-y-2 shadow-lg shadow-blue-500/20">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-white" />
                <span className="text-xs font-bold tracking-wider uppercase">Veyra Recommendation</span>
              </div>
              <p className="text-sm text-white/95 leading-relaxed">
                "Based on your Python foundation, we generated a 4-phase learning path focused on FastAPI microservices, MySQL database optimization, and capstone project deployment."
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          7. CALL TO ACTION - White & Soft Blue System
         ========================================================================= */}
      <section className="py-20 px-6 lg:px-12 bg-gradient-to-b from-[#F5F9FF] to-white text-[#111827] text-center border-b border-[#DCE6F2]">
        <div className="max-w-3xl mx-auto space-y-6">
          <h2 className="heading-display text-[#111827]">
            Ready to build your personalized career path?
          </h2>
          <p className="body-large text-[#475569]">
            Start your AI-powered learning journey today.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">
            <Button
              variant="primary"
              size="lg"
              icon={ArrowRight}
              iconPosition="right"
              onClick={() => navigate('/register')}
            >
              Get Started Now
            </Button>
          </div>
        </div>
      </section>

      {/* Premium Footer */}
      <LandingFooter />
    </div>
  );
};
