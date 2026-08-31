import api from './api';

export const assessmentService = {
  async getAssessments() {
    const res = await api.get('/assessments');
    return res.data;
  },

  async getAssessmentById(id) {
    const res = await api.get(`/assessments/${id}`);
    return res.data;
  },

  async submitAssessment(id, userAnswers) {
    const res = await api.post(`/assessments/${id}/submit`, { answers: userAnswers });
    return res.data;
  }
};
