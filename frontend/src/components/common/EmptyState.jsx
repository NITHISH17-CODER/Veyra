import React from 'react';
import { Inbox, RefreshCw, AlertTriangle } from 'lucide-react';
import { Button } from './Button';

export const EmptyState = ({ title = "No Recommendations Yet", description = "Complete your skill profile to unlock personalized recommendations.", actionText, onAction }) => {
  return (
    <div className="text-center p-10 rounded-3xl bg-white border border-slate-200 shadow-sm space-y-4">
      <div className="w-12 h-12 rounded-2xl bg-[#f4f9ff] text-[#4f9cf9] border border-[#d0e1f9] mx-auto flex items-center justify-center">
        <Inbox className="w-6 h-6" />
      </div>
      <div>
        <h4 className="text-base font-bold text-[#043873]">{title}</h4>
        <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">{description}</p>
      </div>
      {actionText && (
        <Button variant="outline" size="sm" onClick={onAction} className="border-[#d0e1f9] text-[#043873] hover:bg-[#f4f9ff]">
          {actionText}
        </Button>
      )}
    </div>
  );
};

export const ErrorState = ({ title = "Unable to load data", message = "Backend connection unavailable. Falling back to demo mock mode.", onRetry }) => {
  return (
    <div className="text-center p-8 rounded-3xl bg-white border border-rose-200 shadow-sm space-y-3">
      <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 border border-rose-200 mx-auto flex items-center justify-center">
        <AlertTriangle className="w-5 h-5" />
      </div>
      <h4 className="text-sm font-bold text-[#043873]">{title}</h4>
      <p className="text-xs text-slate-500 max-w-md mx-auto">{message}</p>
      {onRetry && (
        <Button variant="secondary" size="sm" icon={RefreshCw} onClick={onRetry} className="bg-[#043873] text-white hover:bg-[#064a96]">
          Try Again
        </Button>
      )}
    </div>
  );
};
