import api from './api';

export const chatService = {
  async sendMessage(userMessage, conversationHistory = [], pageContext = {}) {
    const res = await api.post('/chat', {
      message: userMessage,
      history: conversationHistory,
      page_context: pageContext,
    });
    return res.data;
  },

  async getContext() {
    const res = await api.get('/chat/context');
    return res.data;
  },
};
