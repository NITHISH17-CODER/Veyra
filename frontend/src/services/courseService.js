import api, { API_BASE_URL } from './api';

export const courseService = {
  // Get 5 core career learning courses with user progress from DB
  async getCourses() {
    const res = await api.get('/courses');
    return res.data;
  },

  // Get recommended external resources or career courses
  async getRecommendedCourses(careerId) {
    try {
      const params = careerId ? { career_id: careerId } : {};
      const res = await api.get('/recommendations', { params });
      return res.data?.courses || res.data?.data || res.data;
    } catch (err) {
      const fallback = await this.getCourses();
      return fallback;
    }
  },

  // Get course overview by slug or ID
  async getCourseOverview(slugOrId) {
    const res = await api.get(`/courses/${slugOrId}`);
    return res.data;
  },

  // Backward-compat alias for getCourseById
  async getCourseById(slugOrId) {
    return this.getCourseOverview(slugOrId);
  },

  // Get full phased interactive roadmap
  async getCourseRoadmap(slugOrId) {
    const res = await api.get(`/courses/${slugOrId}/roadmap`);
    return res.data;
  },

  // Get module detail with lessons list
  async getModuleDetail(slugOrId, moduleId) {
    const res = await api.get(`/courses/${slugOrId}/modules/${moduleId}`);
    return res.data;
  },

  // Get individual lesson content, video URL, code snippet, resources
  async getLessonDetail(slugOrId, moduleId, lessonId) {
    const res = await api.get(`/courses/${slugOrId}/modules/${moduleId}/lessons/${lessonId}`);
    return res.data;
  },

  // Mark lesson completed in MySQL and update progression
  async markLessonCompleted(lessonId) {
    const res = await api.post(`/lessons/${lessonId}/complete`);
    return res.data;
  },

  // Get module assessment questions
  async getModuleAssessment(moduleId) {
    const res = await api.get(`/modules/${moduleId}/assessment`);
    return res.data;
  },

  // Submit module assessment answers for server-side grading
  async submitModuleAssessment(assessmentId, answers) {
    const res = await api.post(`/assessments/${assessmentId}/submit`, { answers });
    return res.data;
  },

  // Get Continue Learning action (returns latest incomplete lesson/assessment)
  async getContinueAction(slugOrId) {
    const res = await api.get(`/courses/${slugOrId}/continue-action`);
    return res.data;
  },

  // Get course completion summary
  async getCompletionSummary(slugOrId) {
    const res = await api.get(`/courses/${slugOrId}/completion-summary`);
    return res.data;
  },

  // Download course completion summary as a .txt file
  async downloadCompletionSummary(slugOrId) {
    const token = localStorage.getItem('pathpilot_auth_token');
    const response = await fetch(`${API_BASE_URL}/courses/${slugOrId}/completion-summary/download`, {
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
    });
    if (!response.ok) {
      throw new Error('Failed to download course summary.');
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${slugOrId}-course-summary.txt`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  },

  // Get final comprehensive exam questions
  async getFinalAssessment(slugOrId) {
    const res = await api.get(`/courses/${slugOrId}/final-assessment`);
    return res.data;
  },

  // Submit final exam answers
  async submitFinalAssessment(slugOrId, answers) {
    const res = await api.post(`/courses/${slugOrId}/final-assessment/submit`, { answers });
    return res.data;
  },

  // Get skill info, user level, and modules teaching it
  async getSkillDetail(skillIdentifier) {
    const res = await api.get(`/skills/${skillIdentifier}`);
    return res.data;
  },
};
