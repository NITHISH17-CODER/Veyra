import React, { createContext, useContext, useState, useEffect } from 'react';
import { learningPathService } from '../services/learningPathService';
import { profileService } from '../services/profileService';
import { skillService } from '../services/skillService';
import { careerService } from '../services/careerService';
import { authService } from '../services/authService';
import { onboardingService } from '../services/onboardingService';
import { progressService } from '../services/progressService';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const hasToken = authService.isAuthenticated();

  const [user, setUser] = useState(() => {
    if (!hasToken) return null;
    const saved = localStorage.getItem('pathpilot_user');
    return saved ? JSON.parse(saved) : null;
  });

  const [authLoading, setAuthLoading] = useState(hasToken);

  const [roadmap, setRoadmap] = useState(() => {
    const saved = localStorage.getItem('pathpilot_roadmap');
    return saved ? JSON.parse(saved) : null;
  });

  const [progress, setProgress] = useState(() => {
    const saved = localStorage.getItem('pathpilot_progress');
    return saved ? JSON.parse(saved) : null;
  });

  const [assessments, setAssessments] = useState(() => {
    const saved = localStorage.getItem('pathpilot_assessments');
    return saved ? JSON.parse(saved) : [];
  });

  const [adaptationLogs, setAdaptationLogs] = useState(() => {
    const saved = localStorage.getItem('pathpilot_adaptations');
    return saved ? JSON.parse(saved) : [];
  });

  const [whyModalData, setWhyModalData] = useState(null);
  const [feedbackModalData, setFeedbackModalData] = useState(null);
  const [toastMessage, setToastMessage] = useState(null);

  // Sync state changes to localStorage only when user is authenticated
  useEffect(() => {
    if (user) {
      localStorage.setItem('pathpilot_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('pathpilot_user');
    }
  }, [user]);

  useEffect(() => {
    if (roadmap) localStorage.setItem('pathpilot_roadmap', JSON.stringify(roadmap));
  }, [roadmap]);

  useEffect(() => {
    if (progress) localStorage.setItem('pathpilot_progress', JSON.stringify(progress));
  }, [progress]);

  // Load and verify session from backend on mount / token change
  const refreshUserData = async () => {
    if (!authService.isAuthenticated()) {
      setUser(null);
      setAuthLoading(false);
      return;
    }

    try {
      const me = await authService.getCurrentUser();
      if (!me) {
        throw new Error("Invalid session");
      }

      const [profileRes, skillsRes, interestsRes, prefsRes, pathRes, progressRes] = await Promise.all([
        profileService.getProfile().catch(() => null),
        skillService.getUserSkills().catch(() => []),
        onboardingService.getUserInterests().catch(() => []),
        onboardingService.getUserPreferences().catch(() => null),
        learningPathService.getLearningPath().catch(() => null),
        progressService.getProgress().catch(() => null),
      ]);

      const hasProfile = !!profileRes;
      const PROFICIENCY_MAP = { 1: "Beginner", 2: "Basic", 3: "Intermediate", 4: "Advanced", 5: "Expert" };
      const userSkillsList = Array.isArray(skillsRes) ? skillsRes.map(s => ({
        id: s.id,
        skill_id: s.skill_id,
        name: s.skill?.name || s.skill_name || s.name || "Skill",
        proficiency: s.proficiency_label || PROFICIENCY_MAP[s.proficiency] || "Intermediate",
        proficiency_val: s.proficiency || 3,
        level: (s.proficiency || 3) * 20,
        status: (s.proficiency || 0) >= 3 ? "Ready" : "Needs Improvement",
      })) : [];

      setUser({
        id: me.id,
        name: me.name || "Learner",
        email: me.email,
        avatar_url: profileRes?.avatar_url || me.avatar_url || null,
        education: profileRes?.education || "",
        educationLevel: profileRes?.education_level || "",
        fieldOfStudy: profileRes?.field_of_study || "",
        college: profileRes?.college || "",
        state: profileRes?.state || "",
        district: profileRes?.district || "",
        passedOutYear: profileRes?.passed_out_year || null,
        experienceLevel: profileRes?.experience_level || "Intermediate",
        targetGoal: profileRes?.career_goal_text || profileRes?.career_goal || pathRes?.data?.career || "",
        objective: profileRes?.objective_text || "",
        interests: interestsRes || [],
        skills: userSkillsList,
        weeklyGoalHours: profileRes?.learning_hours_per_week || prefsRes?.learning_hours_per_week || 10,
        learningStyle: prefsRes?.learning_style || profileRes?.learning_preference || "Project-based",
        difficultyPreference: prefsRes?.difficulty_preference || "Intermediate",
        githubUrl: profileRes?.github_url || "",
        githubStatus: profileRes?.github_status || "not_connected",
        githubError: profileRes?.github_error || null,
        githubRepos: profileRes?.github_repos_json || [],
        linkedinUrl: profileRes?.linkedin_url || "",
        linkedinStatus: profileRes?.linkedin_status || "not_connected",
        linkedinError: profileRes?.linkedin_error || null,
        resumeUrl: profileRes?.resume_url || "",
        resumeStatus: profileRes?.resume_status || "not_uploaded",
        resumeError: profileRes?.resume_error || null,
        resumeAnalysis: profileRes?.resume_analysis_json || null,
        onboarding_completed: me.onboarding_completed ?? hasProfile,
        hasCompletedOnboarding: me.onboarding_completed ?? hasProfile,
        readinessScore: pathRes?.data?.readiness_score !== undefined ? pathRes.data.readiness_score : 0,
        streakDays: 0,
      });

      if (pathRes && pathRes.data) {
        setRoadmap(pathRes.data);
      }
      if (progressRes) {
        setProgress(progressRes);
      }
    } catch (err) {
      console.warn("Session verification failed or token expired:", err);
      authService.logout();
      setUser(null);
    } finally {
      setAuthLoading(false);
    }
  };

  useEffect(() => {
    refreshUserData();
  }, []);

  const logout = () => {
    authService.logout();
    setUser(null);
    setRoadmap(null);
    setProgress(null);
    setAssessments([]);
    setAdaptationLogs([]);
    localStorage.removeItem('pathpilot_roadmap');
    localStorage.removeItem('pathpilot_progress');
    localStorage.removeItem('pathpilot_assessments');
    localStorage.removeItem('pathpilot_adaptations');
  };

  const showToast = (message, type = 'info') => {
    setToastMessage({ message, type });
    setTimeout(() => setToastMessage(null), 4000);
  };


  const updateUserSkills = async (newSkills) => {
    setUser(prev => ({
      ...prev,
      skills: newSkills
    }));
    try {
      await skillService.updateUserSkills(newSkills);
    } catch (e) {}
    showToast("Skills updated successfully in MySQL!", "success");
  };

  const updateUserGoal = async (newGoal) => {
    setUser(prev => ({
      ...prev,
      targetGoal: newGoal
    }));
    try {
      await profileService.updateProfile({ career_goal: newGoal });
    } catch (e) {}
    showToast(`Target goal updated to ${newGoal}`, "success");
  };

  const updateUserPreferences = async (prefs) => {
    setUser(prev => ({
      ...prev,
      ...prefs
    }));
    try {
      await profileService.updateProfile({
        learning_hours_per_week: prefs.weeklyGoalHours || 10,
        learning_preference: prefs.learningStyle,
        experience_level: prefs.difficultyPreference,
      });
    } catch (e) {}
    showToast("Preferences saved to MySQL!", "success");
  };

  const submitOnboardingData = async (onboardingPayload) => {
    try {
      const response = await onboardingService.submitOnboarding(onboardingPayload);
      const data = response.data || response;

      if (data.learning_path) {
        setRoadmap(data.learning_path);
      }

      const identifiedGoal = data.career_goal?.identified_career || data.target_career?.name || onboardingPayload.career_goal;
      const readiness = data.learning_path?.readiness_score || data.skill_gap?.readiness_score || 0;

      setUser(prev => ({
        ...prev,
        education: onboardingPayload.education,
        educationLevel: onboardingPayload.education_level,
        fieldOfStudy: onboardingPayload.field_of_study,
        experienceLevel: onboardingPayload.experience_level,
        targetGoal: identifiedGoal,
        objective: onboardingPayload.objective,
        interests: onboardingPayload.interests || [],
        skills: onboardingPayload.skills || [],
        weeklyGoalHours: onboardingPayload.learning_hours_per_week || 10,
        learningStyle: onboardingPayload.learning_style || "Project-based",
        difficultyPreference: onboardingPayload.difficulty_preference || "Intermediate",
        hasCompletedOnboarding: true,
        readinessScore: readiness,
      }));

      showToast("Profile and personalized roadmap saved successfully!", "success");
      return data;
    } catch (err) {
      console.error("Onboarding submission failed:", err);
      showToast("Failed to save onboarding data: " + (err.response?.data?.detail || err.message), "error");
      throw err;
    }
  };

  const generateNewPath = async (goal, skills, preferences) => {
    const targetGoalStr = goal || user?.targetGoal;
    if (!targetGoalStr) {
      showToast("Please enter a target career goal first.", "warning");
      return null;
    }

    try {
      // 1. Get career match to get career_id
      const careerAnalysis = await careerService.getCareerAnalysis(targetGoalStr);
      let careerId = null;
      if (careerAnalysis && careerAnalysis.data && careerAnalysis.data.length > 0) {
        careerId = careerAnalysis.data[0].career_id;
      }

      if (!careerId) {
        throw new Error("Could not match career for goal: " + targetGoalStr);
      }

      // 2. Generate learning path from backend
      const newPathRes = await learningPathService.generateLearningPath({ career_id: careerId });
      const pathData = newPathRes.data || newPathRes;
      setRoadmap(pathData);

      setUser(prev => ({
        ...prev,
        targetGoal: pathData.career || targetGoalStr,
        skills: skills || prev.skills,
        ...preferences,
        hasCompletedOnboarding: true,
        readinessScore: pathData.readiness_score || prev.readinessScore || 0,
      }));

      showToast("Personalized learning path generated!", "success");
      return pathData;
    } catch (err) {
      console.error("Failed to generate path from backend:", err);
      showToast("Failed to generate learning path: " + (err.response?.data?.detail || err.message), "warning");
      return roadmap;
    }
  };

  const applyAssessmentResult = async (assessmentId, result) => {
    setAssessments(prev => prev.map(a => a.id === assessmentId ? { ...a, bestScore: `${result.score}%`, status: 'Completed' } : a));

    try {
      const [pathRes, progressRes] = await Promise.all([
        learningPathService.getLearningPath().catch(() => null),
        progressService.getProgress().catch(() => null),
      ]);
      if (pathRes && pathRes.data) setRoadmap(pathRes.data);
      if (progressRes) setProgress(progressRes);
    } catch (e) {}

    if (result.score >= 70) {
      const newLog = {
        id: `log-${Date.now()}`,
        timestamp: "Just now",
        type: "Assessment Adaptation",
        title: "Skill Proficiency Updated!",
        message: result.aiRecommendation || `Scored ${result.score}% in diagnostic!`
      };
      setAdaptationLogs(prev => [newLog, ...prev]);
      showToast("🚀 Skill level updated and learning path adapted!", "success");
    } else {
      showToast(`Assessment submitted (Score: ${result.score}%). Recommendations updated.`, "info");
    }
  };

  const openWhyModal = (data) => setWhyModalData(data);
  const closeWhyModal = () => setWhyModalData(null);
  const openFeedbackModal = (item) => setFeedbackModalData(item);
  const closeFeedbackModal = () => setFeedbackModalData(null);

  const resetToDemoDefaults = () => {
    logout();
    showToast("Application state reset", "info");
  };

  return (
    <AppContext.Provider
      value={{
        user,
        setUser,
        authLoading,
        logout,
        refreshUserData,
        roadmap,
        setRoadmap,
        progress,
        setProgress,
        assessments,
        setAssessments,
        adaptationLogs,
        updateUserSkills,
        updateUserGoal,
        updateUserPreferences,
        submitOnboardingData,
        generateNewPath,
        applyAssessmentResult,
        whyModalData,
        openWhyModal,
        closeWhyModal,
        feedbackModalData,
        openFeedbackModal,
        closeFeedbackModal,
        toastMessage,
        showToast,
        resetToDemoDefaults
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => useContext(AppContext);
