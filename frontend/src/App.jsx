import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider, useApp } from './context/AppContext';
import { AppLayout } from './components/layout/AppLayout';
import { authService } from './services/authService';

import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { OnboardingWizard } from './pages/OnboardingWizard';
import { DashboardPage } from './pages/DashboardPage';
import { CareerAnalysisPage } from './pages/CareerAnalysisPage';
import { SkillGapPage } from './pages/SkillGapPage';
import { LearningPathPage } from './pages/LearningPathPage';
import { CoursesPage } from './pages/CoursesPage';
import { CourseDetailPage } from './pages/CourseDetailPage';
import { ModuleDetailPage } from './pages/ModuleDetailPage';
import { LessonLearningPage } from './pages/LessonLearningPage';
import { ModuleAssessmentPage } from './pages/ModuleAssessmentPage';
import { CourseFinalExamPage } from './pages/CourseFinalExamPage';
import { CourseCompletionPage } from './pages/CourseCompletionPage';
import { SkillDetailPage } from './pages/SkillDetailPage';
import { ProjectsPage } from './pages/ProjectsPage';
import { ProjectDetailPage } from './pages/ProjectDetailPage';
import { AssessmentsPage } from './pages/AssessmentsPage';
import { AssessmentTakePage } from './pages/AssessmentTakePage';
import { ProgressPage } from './pages/ProgressPage';
import { AiAssistantPage } from './pages/AiAssistantPage';
import { RecommendationsPage } from './pages/RecommendationsPage';
import { NewsPage } from './pages/NewsPage';
import { ProfilePage } from './pages/ProfilePage';
import { SettingsPage } from './pages/SettingsPage';
import { NotFoundPage } from './pages/NotFoundPage';

import { Sparkles } from 'lucide-react';

// Loading screen while verifying auth session with backend
const AuthLoadingScreen = () => (
  <div className="min-h-screen bg-[#0F172A] flex flex-col items-center justify-center p-6 text-white">
    <div className="flex flex-col items-center space-y-4">
      <img
        src="/veyra-logo.png"
        alt="Veyra Logo"
        className="w-14 h-14 rounded-2xl object-contain animate-pulse shadow-lg shadow-blue-500/30"
      />
      <div className="text-center space-y-1.5">
        <h3 className="text-lg font-bold text-white tracking-tight">Checking your session...</h3>
        <p className="text-xs text-white/50">Securing your Veyra AI workspace</p>
      </div>
      <div className="w-48 h-1 bg-white/10 rounded-full overflow-hidden mt-2">
        <div className="w-1/2 h-full bg-[#1456F0] rounded-full animate-indeterminate" />
      </div>
    </div>
  </div>
);

// Route guard for authenticated application routes
const RequireAuth = ({ children }) => {
  const { user, authLoading } = useApp();
  const isAuth = authService.isAuthenticated();

  if (authLoading) {
    return <AuthLoadingScreen />;
  }

  if (!isAuth || !user) {
    return <Navigate to="/login" replace />;
  }

  // If authenticated but profile/onboarding not complete, redirect to onboarding
  if (user.hasCompletedOnboarding === false) {
    return <Navigate to="/onboarding" replace />;
  }

  return children;
};

// Route guard for onboarding page
const RequireOnboardingAuth = ({ children }) => {
  const { user, authLoading } = useApp();
  const isAuth = authService.isAuthenticated();

  if (authLoading) {
    return <AuthLoadingScreen />;
  }

  if (!isAuth || !user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};


// Route guard for guest routes (Login, Register) — redirects already logged in users
const RequireGuest = ({ children }) => {
  const { user, authLoading } = useApp();
  const isAuth = authService.isAuthenticated();

  if (authLoading) {
    return <AuthLoadingScreen />;
  }

  if (isAuth && user) {
    const isCompleted = user.onboarding_completed ?? user.hasCompletedOnboarding;
    return <Navigate to={isCompleted ? "/dashboard" : "/onboarding"} replace />;
  }

  return children;
};

export function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Routes>
          {/* Public / Guest Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route
            path="/login"
            element={
              <RequireGuest>
                <LoginPage />
              </RequireGuest>
            }
          />
          <Route
            path="/register"
            element={
              <RequireGuest>
                <RegisterPage />
              </RequireGuest>
            }
          />

          {/* Onboarding Wizard Routes */}
          <Route
            path="/onboarding"
            element={
              <RequireOnboardingAuth>
                <OnboardingWizard />
              </RequireOnboardingAuth>
            }
          />
          <Route
            path="/onboarding/*"
            element={
              <RequireOnboardingAuth>
                <OnboardingWizard />
              </RequireOnboardingAuth>
            }
          />

          {/* Main SaaS App Routes Wrapped in AppLayout */}
          <Route
            element={
              <RequireAuth>
                <AppLayout />
              </RequireAuth>
            }
          >
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/career-analysis" element={<CareerAnalysisPage />} />
            <Route path="/skill-gap" element={<SkillGapPage />} />
            <Route path="/learning-path" element={<LearningPathPage />} />

            {/* Navigation Redirects */}
            <Route path="/my-learning" element={<Navigate to="/courses" replace />} />
            <Route path="/learn" element={<Navigate to="/courses" replace />} />

            {/* Course Learning Workflow Routes */}
            <Route path="/courses" element={<CoursesPage />} />
            <Route path="/courses/:id" element={<CourseDetailPage />} />
            <Route path="/courses/:slug/modules/:moduleId" element={<ModuleDetailPage />} />
            <Route path="/courses/:slug/modules/:moduleId/lessons/:lessonId" element={<LessonLearningPage />} />
            <Route path="/courses/:slug/modules/:moduleId/assessment" element={<ModuleAssessmentPage />} />
            <Route path="/courses/:slug/assessment/:assessmentId" element={<ModuleAssessmentPage />} />
            <Route path="/courses/:slug/final-assessment" element={<CourseFinalExamPage />} />
            <Route path="/courses/:slug/completion" element={<CourseCompletionPage />} />

            {/* Skill Detail Routes */}
            <Route path="/skills/:skillIdentifier" element={<SkillDetailPage />} />

            {/* Project & Quiz Routes */}
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/projects/:id" element={<ProjectDetailPage />} />
            <Route path="/quizzes" element={<AssessmentsPage />} />
            <Route path="/quizzes/:id" element={<AssessmentTakePage />} />
            <Route path="/assessments" element={<AssessmentsPage />} />
            <Route path="/assessments/:id" element={<AssessmentTakePage />} />
            <Route path="/progress" element={<ProgressPage />} />
            <Route path="/ai-assistant" element={<AiAssistantPage />} />
            <Route path="/recommendations" element={<RecommendationsPage />} />
            <Route path="/news" element={<NewsPage />} />
            <Route path="/news/:id" element={<NewsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>

          {/* Fallback Catch-All */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </BrowserRouter>
    </AppProvider>
  );
}

export default App;
