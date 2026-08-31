import React from 'react';

export const Card = ({ children, className = '', hover = false, glow = false, radius = '12', onClick, ...props }) => {
  const radiusMap = {
    '4': 'rounded-[4px]',
    '8': 'rounded-[8px]',
    '12': 'rounded-xl',
    '16': 'rounded-2xl',
    '24': 'rounded-3xl',
    '32': 'rounded-[32px]'
  };

  const radiusClass = radiusMap[radius] || 'rounded-xl';

  return (
    <div
      onClick={onClick}
      className={`bg-white border border-[#E5E7EB] ${radiusClass} p-6 transition-all duration-150 ${
        hover ? 'hover:border-[#0A0A0A] cursor-pointer' : ''
      } ${glow ? 'border-[#0A0A0A] ring-1 ring-[#0A0A0A]' : ''} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};
