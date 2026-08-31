import React from 'react';

export const Badge = ({ children, variant = 'dark', size = 'sm', className = '' }) => {
  const variants = {
    dark: "bg-[#146EF5] text-white border-transparent",
    surface: "bg-[#F5F9FF] text-[#111827] border-[#DCE6F2]",
    slate: "bg-[#EAF3FF] text-[#146EF5] border-[#DCE6F2]",
    blue: "bg-[#EAF3FF] text-[#146EF5] border-[#146EF5]/20",
    purple: "bg-[#EAF3FF] text-[#146EF5] border-[#146EF5]/20",
    cyan: "bg-[#EAF3FF] text-[#0B5ED7] border-[#146EF5]/20",
    coral: "bg-[#EAF3FF] text-[#146EF5] border-[#146EF5]/20",
    magenta: "bg-[#EAF3FF] text-[#146EF5] border-[#146EF5]/20",
    success: "bg-[#E8FFEA] text-[#1BA673] border-transparent"
  };

  const sizes = {
    xs: "px-2 py-0.5 text-[10px]",
    sm: "px-2.5 py-1 text-xs",
    md: "px-3.5 py-1.5 text-sm"
  };

  return (
    <span className={`inline-flex items-center font-medium border rounded-full ${variants[variant] || variants.dark} ${sizes[size]} ${className}`}>
      {children}
    </span>
  );
};
