import React from 'react';
import { useApp } from '../../context/AppContext';
import { CheckCircle2, AlertCircle, Info } from 'lucide-react';

export const Toast = () => {
  const { toastMessage } = useApp();

  if (!toastMessage) return null;

  const icons = {
    success: <CheckCircle2 className="w-4 h-4 text-emerald-600" />,
    error: <AlertCircle className="w-4 h-4 text-rose-600" />,
    info: <Info className="w-4 h-4 text-[#4f9cf9]" />
  };

  const borders = {
    success: "border-emerald-200 bg-white text-emerald-900 shadow-emerald-500/10",
    error: "border-rose-200 bg-white text-rose-900 shadow-rose-500/10",
    info: "border-[#d0e1f9] bg-white text-[#043873] shadow-[#4f9cf9]/10"
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-bounce-in">
      <div className={`flex items-center gap-3 px-4 py-3 rounded-2xl border shadow-xl text-xs font-bold ${borders[toastMessage.type] || borders.info}`}>
        {icons[toastMessage.type] || icons.info}
        <span>{toastMessage.message}</span>
      </div>
    </div>
  );
};
