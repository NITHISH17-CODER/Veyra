import React from 'react';

export const StatCard = ({ icon: Icon, label, value, subtext, trend, iconColor = 'text-[#0A0A0A]', iconBg = 'bg-[#F7F8FA]' }) => {
  return (
    <div className="bg-white border border-[#E5E7EB] rounded-2xl p-5 hover:border-[#0A0A0A] transition-all">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-[#8E8E93] uppercase tracking-wider">{label}</span>
        {Icon && (
          <div className={`p-2.5 rounded-xl border border-[#EAECF0] ${iconBg} ${iconColor}`}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>
      <div className="mt-3 flex items-baseline justify-between">
        <div className="text-2xl font-bold text-[#0A0A0A] tracking-tight">{value}</div>
        {trend && (
          <span className={`text-xs font-semibold ${trend.startsWith('+') || trend.includes('up') ? 'text-[#1BA673]' : 'text-[#45515E]'}`}>
            {trend}
          </span>
        )}
      </div>
      {subtext && <p className="text-xs text-[#45515E] mt-1">{subtext}</p>}
    </div>
  );
};
