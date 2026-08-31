import React from 'react';
import { Play, Loader2, CheckCircle2, AlertCircle, Clock } from 'lucide-react';

export const ExecutionStatus = ({ status }) => {
  const statusConfig = {
    ready: { label: 'Ready', color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20', icon: Play },
    running: { label: 'Running...', color: 'bg-blue-500/10 text-blue-400 border-blue-500/20 animate-pulse', icon: Loader2 },
    completed: { label: 'Completed', color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20', icon: CheckCircle2 },
    error: { label: 'Error', color: 'bg-rose-500/10 text-rose-400 border-rose-500/20', icon: AlertCircle },
    timeout: { label: 'Timeout', color: 'bg-amber-500/10 text-amber-400 border-amber-500/20', icon: Clock }
  };

  const current = statusConfig[status] || statusConfig.ready;
  const IconComponent = current.icon;

  return (
    <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold border ${current.color}`}>
      <span className="w-1.5 h-1.5 rounded-full bg-current animate-ping" />
      <IconComponent className={`w-3.5 h-3.5 ${status === 'running' ? 'animate-spin' : ''}`} />
      <span>{current.label}</span>
    </div>
  );
};
