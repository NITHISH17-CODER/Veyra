import api from './api';

export const codeExecutionService = {
  /**
   * Fetches supported programming languages and versions from backend.
   */
  async getLanguages() {
    const response = await api.get('/code/languages');
    return response.data;
  },

  /**
   * Executes source code in an isolated sandbox.
   */
  async executeCode({ lessonId, language, version, sourceCode, stdin }) {
    const response = await api.post('/code/execute', {
      lessonId: lessonId ? parseInt(lessonId, 10) : null,
      language,
      version,
      sourceCode,
      stdin: stdin || ''
    });
    return response.data;
  },

  /**
   * Fetches saved draft code for a lesson.
   */
  async getSavedCode(lessonId) {
    const response = await api.get(`/code/lessons/${lessonId}/saved`);
    return response.data;
  },

  /**
   * Persists draft code for a lesson.
   */
  async saveCode(lessonId, { language, version, code, stdin }) {
    const response = await api.post(`/code/lessons/${lessonId}/save`, {
      language,
      version,
      code,
      stdin: stdin || ''
    });
    return response.data;
  }
};
