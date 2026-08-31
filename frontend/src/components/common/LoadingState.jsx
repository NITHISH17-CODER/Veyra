import React from 'react';
import { Sparkles, Brain } from 'lucide-react';

export const LoadingState = ({ message = "Veyra AI is calculating recommendations...", type = "card" }) => {
  if (type === "ai") {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center space-y-4">
        <div className="relative">
          <div className="w-16 h-16 rounded-2xl bg-[#043873] flex items-center justify-center animate-pulse shadow-xl shadow-[#043873]/20">
            <Brain className="w-8 h-8 text-[#ffe492] animate-bounce" />
          </div>
          <div className="absolute -top-1 -right-1">
            <Sparkles className="w-5 h-5 text-[#4f9cf9] animate-spin" />
          </div>
        </div>
        <div>
          <h4 className="text-sm font-bold text-[#043873]">{message}</h4>
          <p className="text-xs text-slate-500 mt-1">Matching prerequisites, skills, and industry roadmaps...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4 w-full animate-pulse p-4">
      <div className="h-6 bg-slate-200 rounded-lg w-1/3"></div>
      <div className="h-24 bg-slate-100 rounded-2xl w-full border border-slate-200"></div>
      <div className="h-24 bg-slate-100 rounded-2xl w-full border border-slate-200"></div>
    </div>
  );
};
