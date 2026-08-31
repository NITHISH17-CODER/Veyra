import api from './api';

export const profileService = {
  async getProfile() {
    try {
      const res = await api.get('/profile');
      return res.data;
    } catch (err) {
      if (err.response && err.response.status === 404) {
        return null;
      }
      throw err;
    }
  },

  async createProfile(profileData) {
    const res = await api.post('/profile', profileData);
    return res.data;
  },

  async updateProfile(profileData) {
    const res = await api.put('/profile', profileData);
    return res.data;
  },

  async uploadPhoto(formData) {
    const res = await api.post('/profile/photo', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  async removePhoto() {
    const res = await api.delete('/profile/photo');
    return res.data;
  },

  async verifyGithub(github_url) {
    const res = await api.post('/profile/github', { github_url });
    return res.data;
  },

  async verifyLinkedin(linkedin_url) {
    const res = await api.post('/profile/linkedin', { linkedin_url });
    return res.data;
  },

  async uploadResume(formData) {
    const res = await api.post('/profile/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },
};
