import React from 'react';

export const ProgressBar = ({ value = 0, max = 100, color = 'dark', showPercentage = false, height = 'h-2', className = '' }) => {
  const percentage = Math.min(100, Math.max(0, Math.round((value / max) * 100)));

  const colors = {
    dark: "bg-[#0A0A0A]",
    blue: "bg-[#1456F0]",
    purple: "bg-[#A855F7]",
    coral: "bg-[#FF5530]",
    magenta: "bg-[#EA5EC1]",
    cyan: "bg-[#3DAEFF]",
    emerald: "bg-[#1BA673]"
  };

  return (
    <div className={`w-full ${className}`}>
      {showPercentage && (
        <div className="flex justify-between items-center text-xs mb-1.5 font-medium text-[#45515E]">
          <span>Progress</span>
          <span className="font-mono text-[#0A0A0A] font-semibold">{percentage}%</span>
        </div>
      )}
      <div className={`w-full bg-[#F2F3F5] rounded-full overflow-hidden ${height}`}>
        <div
          className={`${height} ${colors[color] || colors.dark} transition-all duration-500 ease-out rounded-full`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
