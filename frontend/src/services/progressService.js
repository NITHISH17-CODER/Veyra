import api from './api';

export const progressService = {
  async getProgress() {
    try {
      const res = await api.get('/progress');
      return res.data;
    } catch (err) {
      if (err.response && err.response.status === 404) {
        return null;
      }
      throw err;
    }
  },

  async logLearningSession(sessionDetails) {
    const res = await api.post('/progress', sessionDetails);
    return res.data;
  }
};
