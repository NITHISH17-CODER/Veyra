import api from './api';

export const recommendationService = {
  async getRecommendations() {
    const [coursesRes, projectsRes] = await Promise.all([
      api.get('/courses/recommended').catch(() => ({ data: [] })),
      api.get('/projects/recommended').catch(() => ({ data: [] }))
    ]);
    return {
      courses: coursesRes.data?.data || coursesRes.data || [],
      projects: projectsRes.data?.data || projectsRes.data || []
    };
  }
};
