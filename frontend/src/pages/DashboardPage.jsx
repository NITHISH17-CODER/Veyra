import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { recommendationService } from '../services/recommendationService';
import { learningPathService } from '../services/learningPathService';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { Card } from '../components/common/Card';
import api from '../services/api';
import {
  Sparkles,
  ArrowRight,
  Compass,
  Map,
  BookOpen,
  FolderGit2,
  CheckSquare,
  BarChart2,
  Play,
  Award,
  Flame,
  Clock,
  TrendingUp,
  Newspaper,
  UserCheck
} from 'lucide-react';

/* ─── Modern SVG Circular Progress Gauge ─────────────────────────────── */
const CircularGauge = ({ percentage = 0, size = 150, stroke = 12 }) => {
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="relative inline-flex items-center justify-center shrink-0" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#F1F5F9"
          strokeWidth={stroke}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="url(#veyraGaugeGradient)"
          strokeWidth={stroke}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
        <defs>
          <linearGradient id="veyraGaugeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#1456F0" />
            <stop offset="100%" stopColor="#2563EB" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-black text-slate-900 tabular-nums">{percentage}%</span>
        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mt-0.5">Progress</span>
      </div>
    </div>
  );
};

export const DashboardPage = () => {
  const { user, roadmap } = useApp();
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState({ courses: [], projects: [] });
  const [nextAction, setNextAction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [streak, setStreak] = useState({ current_streak: 0, longest_streak: 0 });
  const [progressData, setProgressData] = useState({ percentage: 0, completedModules: 0, totalModules: 0 });

  const hasOnboarded = Boolean(
    user?.hasCompletedOnboarding || (roadmap?.items && roadmap.items.length > 0)
  );

  useEffect(() => {
    if (!hasOnboarded) {
      setLoading(false);
      return;
    }

    const loadDashboardData = async () => {
      setLoading(true);
      try {
        const [recsData, nextActionRes, streakRes] = await Promise.all([
          recommendationService.getRecommendations().catch(() => ({ courses: [], projects: [] })),
          learningPathService.getNextAction().catch(() => null),
          api.get('/streak').catch(() => ({ data: { current_streak: 0, longest_streak: 0 } })),
        ]);
        setRecommendations(recsData);
        if (nextActionRes && nextActionRes.data) {
          setNextAction(nextActionRes.data);
        }
        setStreak(streakRes.data);

        // Calculate progress from roadmap items
        if (roadmap?.items && roadmap.items.length > 0) {
          const completedItems = roadmap.items.filter(item => item.status === 'completed').length;
          const totalItems = roadmap.items.length;
          const pct = totalItems > 0 ? Math.round((completedItems / totalItems) * 100) : 0;
          setProgressData({ percentage: pct, completedModules: completedItems, totalModules: totalItems });
        }
      } catch (err) {
        console.warn("Error loading dashboard data:", err);
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, [hasOnboarded, roadmap]);

  const targetCareer = roadmap?.career || user?.targetGoal || "Frontend Developer";
  const progressPct = progressData.percentage || 0;
  const currentModule = nextAction?.title || "Course Fundamentals";

  // 7-Day Motivational Message System
  const MOTIVATIONAL_MESSAGES = {
    1: "Your journey starts with one step. Take it today.",
    2: "Consistency turns small efforts into remarkable progress.",
    3: "Every skill you learn today brings your career goal closer.",
    4: "Do not compare your progress. Build your own path.",
    5: "Keep learning. The version of you tomorrow will thank you.",
    6: "Progress is built one lesson, one challenge, and one step at a time.",
    7: "You made it this far. Keep going — your path is waiting for you."
  };

  const currentStreakVal = streak?.current_streak || 1;
  const activeDayNumber = ((Math.max(1, currentStreakVal) - 1) % 7) + 1;
  const dailyMotivationalQuote = MOTIVATIONAL_MESSAGES[activeDayNumber];

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-7xl mx-auto pb-12">
      {!hasOnboarded ? (
        /* Empty State */
        <Card radius="32" className="p-12 text-center max-w-2xl mx-auto my-12 space-y-6 bg-white border border-slate-200/80 shadow-xl">
          <div className="w-14 h-14 rounded-3xl bg-[#146EF5] text-white flex items-center justify-center mx-auto shadow-lg shadow-blue-500/20">
            <Compass className="w-7 h-7" />
          </div>
          <div className="space-y-2">
            <span className="text-xs font-bold text-[#146EF5] uppercase tracking-widest bg-blue-50 px-3 py-1 rounded-full border border-blue-100">
              Welcome to Veyra
            </span>
            <h1 className="text-3xl font-black text-slate-900">Build Your AI Learning Path</h1>
            <p className="text-sm text-slate-500 leading-relaxed">
              Tell us about your background and target career to generate your personalized learning roadmap.
            </p>
          </div>
          <Button
            variant="primary"
            size="lg"
            icon={Sparkles}
            iconPosition="right"
            onClick={() => navigate('/onboarding')}
            className="shadow-lg shadow-blue-500/20"
          >
            Start Onboarding
          </Button>
        </Card>
      ) : (
        <>
          {/* Daily Motivational Message Banner (Requirement 6, 7 & 8) */}
          <div className="p-4 rounded-2xl bg-[#F5F9FF] border border-[#DCE6F2] flex items-center justify-between gap-4 shadow-xs">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-[#EAF3FF] border border-[#146EF5]/20 flex items-center justify-center text-[#146EF5] shrink-0">
                <Sparkles className="w-4.5 h-4.5 text-[#146EF5]" />
              </div>
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#146EF5] block">
                  Day {activeDayNumber} &bull; Daily Motivational Message
                </span>
                <p className="text-xs font-semibold text-[#111827]">
                  "{dailyMotivationalQuote}"
                </p>
              </div>
            </div>
            <Badge variant="blue" className="hidden sm:inline-flex shrink-0">
              {currentStreakVal} Day Streak 🔥
            </Badge>
          </div>

          {/* Header Greeting matching reference image */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                Your path is waiting for you, {user?.name || "Learner"}.
              </h1>
              <p className="text-sm text-slate-500 font-medium">
                Here is your career progression overview for <strong className="text-slate-800">{targetCareer}</strong>.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                icon={Sparkles}
                onClick={() => navigate('/ai-assistant')}
                className="bg-white border-slate-200 shadow-sm"
              >
                Veyra AI Assistant
              </Button>
            </div>
          </div>

          {/* TOP SECTION: HERO ACTIVE PATH + ACTIVITY FEED (Reference layout style) */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Active Course Card (Spans 2 cols) */}
            <Card radius="32" className="lg:col-span-2 p-8 bg-white border border-slate-200/80 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] flex flex-col justify-between space-y-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-[#1456F0] uppercase tracking-widest bg-blue-50 px-3 py-1 rounded-full border border-blue-100">
                    Active Career Track
                  </span>
                </div>
                <span className="text-xs font-semibold text-slate-400 flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5" /> Updated recently
                </span>
              </div>

              <div className="flex flex-col md:flex-row md:items-center justify-between gap-8">
                <div className="space-y-4 flex-1">
                  <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">{targetCareer}</h2>
                  <div className="space-y-2 text-xs text-slate-600">
                    <div className="flex items-center gap-2.5 p-2.5 rounded-xl bg-slate-50 border border-slate-100">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shrink-0"></span>
                      <span>Next Lesson: <strong className="text-slate-900 font-bold">{currentModule}</strong></span>
                    </div>
                    <div className="flex items-center gap-2.5 p-2.5 rounded-xl bg-slate-50 border border-slate-100">
                      <TrendingUp className="w-4 h-4 text-[#1456F0] shrink-0" />
                      <span>Completed <strong className="text-slate-900 font-bold">{progressData.completedModules}</strong> / {progressData.totalModules || 12} milestones</span>
                    </div>
                  </div>
                </div>

                {/* Circular Gauge */}
                <CircularGauge percentage={progressPct} size={150} stroke={12} />
              </div>

              <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                <span className="text-xs text-slate-400 font-medium">Personalized AI Roadmap</span>
                <Button
                  variant="primary"
                  size="md"
                  icon={Play}
                  iconPosition="right"
                  onClick={() => navigate('/learning-path')}
                  className="shadow-md shadow-blue-500/20"
                >
                  Continue Learning
                </Button>
              </div>
            </Card>

            {/* Streak & Stats Feed Card (Spans 1 col) */}
            <Card radius="32" className="p-7 bg-white border border-slate-200/80 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] flex flex-col justify-between space-y-6">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Learning Activity</h3>
                <Flame className="w-4 h-4 text-orange-500 fill-orange-500" />
              </div>

              <div className="space-y-4">
                {/* Streak Metric */}
                <div className="p-4 rounded-2xl bg-gradient-to-br from-amber-50/80 to-orange-50/40 border border-orange-100/80 flex items-center justify-between">
                  <div>
                    <span className="text-[10px] font-bold text-orange-600 uppercase tracking-wider block">Current Streak</span>
                    <span className="text-2xl font-black text-slate-900 mt-0.5 block">{streak.current_streak} Days 🔥</span>
                  </div>
                  <div className="text-right">
                    <span className="text-[10px] font-semibold text-slate-400 block">Best Streak</span>
                    <span className="text-sm font-bold text-slate-700">{streak.longest_streak} Days</span>
                  </div>
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100">
                    <span className="text-[10px] font-semibold text-slate-400 uppercase block">Daily Goal</span>
                    <span className="text-sm font-bold text-slate-900 mt-0.5 block">10 hrs/wk</span>
                  </div>
                  <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100">
                    <span className="text-[10px] font-semibold text-slate-400 uppercase block">User Status</span>
                    <span className="text-sm font-bold text-emerald-600 mt-0.5 block">Active</span>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('/profile')}
                  className="w-full justify-center text-xs"
                >
                  View Profile & Certificates
                </Button>
              </div>
            </Card>
          </div>

          {/* DASHBOARD MODULE CARDS GRID */}
          <div className="space-y-4">
            <h2 className="text-lg font-bold text-slate-900">Platform Hub</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Card 1: Roadmap */}
              <Card radius="24" className="p-6 space-y-4 flex flex-col justify-between bg-white border border-slate-200/80 hover:border-[#1456F0] transition-all hover:shadow-md group">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="w-10 h-10 rounded-2xl bg-blue-50 text-[#1456F0] flex items-center justify-center">
                      <Map className="w-5 h-5" />
                    </div>
                    <Badge variant="surface">Roadmap</Badge>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 group-hover:text-[#1456F0] transition-colors">My Roadmap</h3>
                  <p className="text-xs text-slate-500 leading-relaxed">
                    Personalized AI sequence (Phase → Module → Topic → Lesson) for {targetCareer}.
                  </p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('/learning-path')}
                  className="w-full justify-center mt-4 border-slate-200"
                >
                  View Roadmap
                </Button>
              </Card>

              {/* Card 2: Learn */}
              <Card radius="24" className="p-6 space-y-4 flex flex-col justify-between bg-white border border-slate-200/80 hover:border-[#1456F0] transition-all hover:shadow-md group">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="w-10 h-10 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center">
                      <BookOpen className="w-5 h-5" />
                    </div>
                    <Badge variant="surface">5 Programs</Badge>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 group-hover:text-[#1456F0] transition-colors">Learn & Courses</h3>
                  <p className="text-xs text-slate-500 leading-relaxed">
                    Browse standard curriculum for Frontend, Backend, Cybersecurity, SDE, and AI.
                  </p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('/courses')}
                  className="w-full justify-center mt-4 border-slate-200"
                >
                  Explore Courses
                </Button>
              </Card>

              {/* Card 3: Quizzes */}
              <Card radius="24" className="p-6 space-y-4 flex flex-col justify-between bg-white border border-slate-200/80 hover:border-[#1456F0] transition-all hover:shadow-md group">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="w-10 h-10 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
                      <CheckSquare className="w-5 h-5" />
                    </div>
                    <Badge variant="surface">Quizzes</Badge>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 group-hover:text-[#1456F0] transition-colors">Course Quizzes</h3>
                  <p className="text-xs text-slate-500 leading-relaxed">
                    10-question course quizzes loaded from MySQL with detailed score evaluations.
                  </p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('/quizzes')}
                  className="w-full justify-center mt-4 border-slate-200"
                >
                  Take Quizzes
                </Button>
              </Card>

              {/* Card 4: Projects */}
              <Card radius="24" className="p-6 space-y-4 flex flex-col justify-between bg-white border border-slate-200/80 hover:border-[#1456F0] transition-all hover:shadow-md group">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="w-10 h-10 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
                      <FolderGit2 className="w-5 h-5" />
                    </div>
                    <Badge variant="surface">15 Projects</Badge>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 group-hover:text-[#1456F0] transition-colors">Project Catalog</h3>
                  <p className="text-xs text-slate-500 leading-relaxed">
                    15 hands-on projects (5 Basic, 5 Intermediate, 5 Advanced) with code evaluation.
                  </p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('/projects')}
                  className="w-full justify-center mt-4 border-slate-200"
                >
                  View Projects
                </Button>
              </Card>

              {/* Card 5: Skills */}
              <Card radius="24" className="p-6 space-y-4 flex flex-col justify-between bg-white border border-slate-200/80 hover:border-[#1456F0] transition-all hover:shadow-md group">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="w-10 h-10 rounded-2xl bg-blue-50 text-[#1456F0] flex items-center justify-center">
                      <BarChart2 className="w-5 h-5" />
                    </div>
                    <Badge variant="surface">Skill Tree</Badge>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 group-hover:text-[#1456F0] transition-colors">Interactive Skill Tree</h3>
                  <p className="text-xs text-slate-500 leading-relaxed">
                    Auto-updating skill hierarchy tracking your lesson, quiz, and project completion.
                  </p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('/skill-gap')}
                  className="w-full justify-center mt-4 border-slate-200"
                >
                  Inspect Skill Tree
                </Button>
              </Card>

              {/* Card 6: News */}
              <Card radius="24" className="p-6 space-y-4 flex flex-col justify-between bg-white border border-slate-200/80 hover:border-[#1456F0] transition-all hover:shadow-md group">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="w-10 h-10 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center">
                      <Newspaper className="w-5 h-5" />
                    </div>
                    <Badge variant="surface">Live News</Badge>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 group-hover:text-[#1456F0] transition-colors">Technical News</h3>
                  <p className="text-xs text-slate-500 leading-relaxed">
                    Moving ticker and internal news summaries personalized for {targetCareer}.
                  </p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('/news')}
                  className="w-full justify-center mt-4 border-slate-200"
                >
                  Read Tech News
                </Button>
              </Card>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
