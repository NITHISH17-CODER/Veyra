import React, { useState } from 'react';
import { Modal } from './Modal';
import { ThumbsDown, Send, Check } from 'lucide-react';
import { Button } from './Button';
import { useApp } from '../../context/AppContext';
import { feedbackService } from '../../services/feedbackService';

export const FeedbackModal = () => {
  const { feedbackModalData, closeFeedbackModal, showToast } = useApp();
  const [selectedReason, setSelectedReason] = useState('');
  const [comments, setComments] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  if (!feedbackModalData) return null;

  const reasons = [
    "Too difficult",
    "Too easy",
    "Not relevant to my goal",
    "Already know this topic",
    "Too time-consuming"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    await feedbackService.submitFeedback({
      recommendationId: feedbackModalData.id,
      reason: selectedReason,
      comments
    });
    setSubmitting(false);
    setSubmitted(true);
    showToast("Feedback submitted! AI engine adjusted recommendations.", "success");
    setTimeout(() => {
      setSubmitted(false);
      setSelectedReason('');
      setComments('');
      closeFeedbackModal();
    }, 1200);
  };

  return (
    <Modal isOpen={!!feedbackModalData} onClose={closeFeedbackModal} title="Recommendation Feedback">
      {submitted ? (
        <div className="text-center py-8 space-y-3">
          <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 mx-auto flex items-center justify-center">
            <Check className="w-6 h-6" />
          </div>
          <h4 className="text-base font-bold text-[#043873]">Thank You!</h4>
          <p className="text-xs text-slate-500">Veyra AI has logged your feedback and recalculated recommendations.</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="flex items-center gap-3 p-3.5 rounded-2xl bg-[#f4f9ff] border border-[#d0e1f9]">
            <ThumbsDown className="w-5 h-5 text-amber-500 shrink-0" />
            <div>
              <span className="text-xs text-slate-500 block font-bold">Item:</span>
              <h5 className="text-xs font-bold text-[#043873]">{feedbackModalData.title}</h5>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-[#043873]">What was wrong with this recommendation?</label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {reasons.map((r) => (
                <button
                  key={r}
                  type="button"
                  onClick={() => setSelectedReason(r)}
                  className={`p-2.5 rounded-xl text-xs font-semibold border text-left transition-all ${
                    selectedReason === r
                      ? 'bg-[#e8f2ff] text-[#043873] border-[#4f9cf9] font-bold shadow-sm'
                      : 'bg-white text-slate-600 border-slate-200 hover:border-[#4f9cf9]'
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-[#043873]">Tell us more (optional)</label>
            <textarea
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              placeholder="Suggest what you'd prefer to learn instead..."
              rows={3}
              className="w-full bg-[#f4f9ff] border border-[#d0e1f9] rounded-xl p-3 text-xs text-[#043873] placeholder-slate-400 focus:outline-none focus:border-[#4f9cf9]"
            />
          </div>

          <div className="flex justify-end gap-3 pt-2">
            <Button variant="ghost" size="sm" onClick={closeFeedbackModal}>
              Cancel
            </Button>
            <Button
              variant="primary"
              size="sm"
              loading={submitting}
              icon={Send}
              type="submit"
              disabled={!selectedReason}
              className="bg-[#4f9cf9] hover:bg-[#3882e0] font-bold text-white shadow-md shadow-[#4f9cf9]/20"
            >
              Submit Feedback
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
};
