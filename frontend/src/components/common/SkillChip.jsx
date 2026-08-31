import React from 'react';

export const SkillChip = ({ name, proficiency, level, onRemove, onClick, selected = false, className = '' }) => {
  const displayName = name || 'Skill';
  const displayProficiency = proficiency || level || 'Intermediate';

  return (
    <div
      onClick={onClick}
      className={`inline-flex items-center gap-2.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all duration-150 cursor-pointer border shadow-sm ${
        selected
          ? 'bg-[#0A0A0A] text-white border-[#0A0A0A]'
          : 'bg-white hover:bg-[#F9FAFB] text-[#0A0A0A] border-[#E5E7EB] hover:border-[#D1D5DB]'
      } ${className}`}
    >
      <span className="font-bold text-[#0A0A0A]">{displayName}</span>
      <span className={`text-[11px] px-2 py-0.5 rounded-md font-medium tracking-wide ${
        selected
          ? 'bg-white/20 text-white'
          : 'bg-[#F3F4F6] text-[#45515E] border border-[#E5E7EB]'
      }`}>
        {displayProficiency}
      </span>

      {onRemove && (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          title={`Remove ${displayName}`}
          className="text-[#9CA3AF] hover:text-rose-600 transition-colors ml-1 p-0.5 rounded-full hover:bg-rose-50 font-bold text-sm leading-none"
        >
          ×
        </button>
      )}
    </div>
  );
};
