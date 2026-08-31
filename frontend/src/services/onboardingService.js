import api from './api';

export const onboardingService = {
  /**
   * Submit complete onboarding payload to backend MySQL.
   */
  async submitOnboarding(payload) {
    const res = await api.post('/onboarding', payload);
    return res.data;
  },

  async getOnboardingStatus() {
    const res = await api.get('/onboarding/status');
    return res.data;
  },

  async saveOnboardingStep(payload) {
    const res = await api.post('/onboarding/step', payload);
    return res.data;
  },

  /**
   * Upload resume file for parsing and skill extraction.
   */
  async uploadResume(file) {
    const formData = new FormData();
    formData.append('file', file);

    const res = await api.post('/onboarding/resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  /**
   * Validate and analyze GitHub profile.
   */
  async analyzeGithub(githubUrl) {
    const res = await api.post('/onboarding/github', { github_url: githubUrl });
    return res.data;
  },

  /**
   * Fetch all master interests from catalogue.
   */
  async getMasterInterests() {
    try {
      const res = await api.get('/interests');
      return res.data?.data || [];
    } catch (e) {
      console.warn("Could not fetch master interests from backend:", e);
      return [
        { id: 1, name: "AI", category: "AI / Machine Learning" },
        { id: 2, name: "Data Science", category: "Data Science & Analytics" },
        { id: 3, name: "Web Development", category: "Software Engineering" },
        { id: 4, name: "Mobile Development", category: "Software Engineering" },
        { id: 5, name: "Cybersecurity", category: "Security & Networks" },
        { id: 6, name: "Cloud Computing", category: "Cloud & Infrastructure" },
        { id: 7, name: "Data Analytics", category: "Data Science & Analytics" },
        { id: 8, name: "UI/UX", category: "Design & Product" },
        { id: 9, name: "Software Development", category: "Software Engineering" },
        { id: 10, name: "Robotics", category: "Hardware & Systems" },
        { id: 11, name: "IoT", category: "Hardware & Systems" },
        { id: 12, name: "Business Analytics", category: "Data Science & Analytics" },
        { id: 13, name: "DevOps", category: "Cloud & Infrastructure" },
        { id: 14, name: "Database Engineering", category: "Databases & Systems" },
      ];
    }
  },

  /**
   * Fetch authenticated user's stored interests.
   */
  async getUserInterests() {
    try {
      const res = await api.get('/user-interests');
      return res.data?.data || [];
    } catch (e) {
      return [];
    }
  },

  /**
   * Fetch authenticated user's stored preferences.
   */
  async getUserPreferences() {
    try {
      const res = await api.get('/user-preferences');
      return res.data?.data || null;
    } catch (e) {
      return null;
    }
  },
};
