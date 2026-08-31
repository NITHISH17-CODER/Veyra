import api from './api';

export const feedbackService = {
  async submitFeedback(feedbackPayload) {
    const res = await api.post('/feedback', feedbackPayload);
    return res.data;
  }
};
