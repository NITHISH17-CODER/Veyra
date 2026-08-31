import api from './api';

export const projectService = {
  async getProjects(category = 'All', career = 'All') {
    const params = {};
    if (category && category !== 'All') params.category = category;
    if (career && career !== 'All') params.career = career;
    const res = await api.get('/projects', { params });
    return res.data;
  },

  async getRecommendedProjects(careerId) {
    const params = careerId ? { career_id: careerId } : {};
    const res = await api.get('/projects/recommended', { params });
    return res.data?.data || res.data;
  },

  async getProjectById(id) {
    const res = await api.get(`/projects/${id}`);
    return res.data;
  },

  async submitProject(id, submissionUrl, notes = '') {
    const res = await api.post(`/projects/${id}/submit`, {
      submission_url: submissionUrl,
      notes,
    });
    return res.data;
  },

  async getProjectProgress(id) {
    const res = await api.get(`/projects/${id}/progress`);
    return res.data?.data || res.data;
  }
};
