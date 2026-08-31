import api from './api';

export const authService = {
  async login(credentials) {
    const normalizedEmail = (credentials.email || '').trim().toLowerCase();

    const response = await api.post('/auth/login', {
      email: normalizedEmail,
      password: credentials.password
    });
    
    const token = response.data?.access_token || response.data?.token;
    const user = response.data?.user;
    if (token) {
      localStorage.setItem('pathpilot_auth_token', token);
    }
    if (user) {
      localStorage.setItem('pathpilot_user', JSON.stringify(user));
    }
    
    return {
      token,
      user
    };
  },

  async register(userData) {
    const normalizedEmail = (userData.email || '').trim().toLowerCase();

    const response = await api.post('/auth/register', {
      name: (userData.name || '').trim(),
      email: normalizedEmail,
      password: userData.password,
      confirm_password: userData.confirmPassword || userData.confirm_password || userData.password
    });
    
    const token = response.data?.access_token || response.data?.token;
    const user = response.data?.user;
    if (token) {
      localStorage.setItem('pathpilot_auth_token', token);
    }
    if (user) {
      localStorage.setItem('pathpilot_user', JSON.stringify(user));
    }

    return {
      token,
      user
    };
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me');
    return response.data;
  },

  logout() {
    localStorage.removeItem('pathpilot_auth_token');
    localStorage.removeItem('pathpilot_user');
    localStorage.removeItem('pathpilot_profile');
    localStorage.removeItem('pathpilot_roadmap');
    localStorage.removeItem('pathpilot_progress');
    localStorage.removeItem('pathpilot_assessments');
    localStorage.removeItem('pathpilot_adaptations');
    sessionStorage.removeItem('pathpilot_session_expired');
  },

  isAuthenticated() {
    return !!localStorage.getItem('pathpilot_auth_token');
  }
};
