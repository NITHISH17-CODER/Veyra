import React from 'react';
import { Modal } from './Modal';
import { Sparkles, CheckCircle2, TrendingUp, Target, ArrowRight } from 'lucide-react';
import { Button } from './Button';
import { useApp } from '../../context/AppContext';

export const WhyModal = () => {
  const { whyModalData, closeWhyModal, user } = useApp();

  if (!whyModalData) return null;

  return (
    <Modal isOpen={!!whyModalData} onClose={closeWhyModal} title="Why This Recommendation?">
      <div className="space-y-6">
        <div className="flex items-start gap-4 p-4 rounded-2xl bg-[#043873] text-white">
          <div className="p-3 rounded-xl bg-white/15 text-[#ffe492]">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-bold tracking-wider text-[#ffe492] uppercase">AI Recommendation Rationale</span>
            <h4 className="text-base font-bold text-white mt-0.5">{whyModalData.title}</h4>
            <p className="text-xs text-slate-200 mt-1">{whyModalData.subtitle || whyModalData.provider}</p>
          </div>
        </div>

        <div className="space-y-3">
          <div className="text-xs font-semibold text-slate-500 flex items-center gap-1.5">
            <Target className="w-4 h-4 text-[#4f9cf9]" />
            <span>Target Goal: <strong className="text-[#043873]">{user?.targetGoal}</strong></span>
          </div>

          <div className="p-4 rounded-2xl bg-[#f4f9ff] border border-[#d0e1f9] space-y-3">
            <h5 className="text-xs font-bold text-[#043873] uppercase tracking-wider">Why this recommendation?</h5>
            <ul className="space-y-2.5 text-xs text-slate-700">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span><strong>Matches your goal:</strong> Directly aligns with becoming a <strong>{user?.targetGoal || "your target role"}</strong>.</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span><strong>Addresses your skill gap:</strong> Focuses on your active gap in <strong>{whyModalData.skills?.[0] || 'Core Prerequisite'}</strong>.</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span><strong>Fits your current level:</strong> Prerequisite baseline met ({user?.skills?.[0]?.name || 'Python'} verified).</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span><strong>Fits your weekly learning time:</strong> Designed to complete within your <strong>{user?.weeklyGoalHours || 10} hrs/week</strong> schedule.</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="flex items-center justify-between p-4 rounded-2xl bg-[#e8f2ff] border border-[#d0e1f9]">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-[#4f9cf9]" />
            <div>
              <span className="text-xs text-slate-500 block font-medium">Estimated Goal Impact</span>
              <span className="text-sm font-bold text-[#043873]">{whyModalData.impact || "+15% Career Readiness"}</span>
            </div>
          </div>
          <Button
            size="sm"
            variant="primary"
            icon={ArrowRight}
            iconPosition="right"
            onClick={closeWhyModal}
            className="bg-[#4f9cf9] hover:bg-[#3882e0] font-bold text-white shadow-md shadow-[#4f9cf9]/20"
          >
            Start Learning
          </Button>
        </div>
      </div>
    </Modal>
  );
};
