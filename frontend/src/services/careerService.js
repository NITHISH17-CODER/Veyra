import api from './api';

export const careerService = {
  async getCareerAnalysis(goal) {
    const res = await api.post('/careers/recommend', { goal });
    return res.data;
  },

  async getSkillGap(careerId) {
    const res = await api.get(`/careers/${careerId}/skill-gap`);
    return res.data;
  }
};
