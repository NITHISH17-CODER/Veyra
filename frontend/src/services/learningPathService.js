import api from './api';

export const learningPathService = {
  async getLearningPath() {
    try {
      const res = await api.get('/learning-path');
      return res.data;
    } catch (err) {
      if (err.response && err.response.status === 404) {
        return null;
      }
      throw err;
    }
  },

  async generateLearningPath(payload) {
    const careerId = payload.career_id || payload.careerId;
    if (!careerId) {
      throw new Error("Target career ID is required to generate learning path.");
    }
    const res = await api.post('/learning-path/generate', { career_id: careerId });
    return res.data;
  },

  async getNextAction() {
    const res = await api.get('/learning-path/next-action');
    return res.data;
  }
};
