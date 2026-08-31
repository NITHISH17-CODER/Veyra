import React from 'react';

/**
 * Official Veyra Brand Logo Component
 * Renders the official uploaded Veyra logo asset with preserve-aspect-ratio and object-contain.
 */
export const Logo = ({
  size = 'md',
  showText = true,
  textClassName = 'text-xl font-extrabold text-[#0A0A0A] tracking-tight font-sans',
  className = '',
  imgClassName = '',
  onClick,
}) => {
  const sizeClasses = {
    xs: 'w-5 h-5 min-w-[20px]',
    sm: 'w-6.5 h-6.5 min-w-[26px]',
    md: 'w-8 h-8 min-w-[32px]',
    lg: 'w-10 h-10 min-w-[40px]',
    xl: 'w-12 h-12 min-w-[48px]',
    '2xl': 'w-16 h-16 min-w-[64px]',
  };

  const currentSizeClass = sizeClasses[size] || sizeClasses.md;

  return (
    <div
      onClick={onClick}
      className={`flex items-center gap-2.5 ${onClick ? 'cursor-pointer' : ''} ${className}`}
    >
      <img
        src="/veyra-logo.png"
        alt="Veyra Logo"
        className={`${currentSizeClass} rounded-xl object-contain shadow-sm border border-[#1456F0]/20 shrink-0 transition-transform duration-200 hover:scale-105 ${imgClassName}`}
      />
      {showText && (
        <span className={textClassName}>Veyra</span>
      )}
    </div>
  );
};

export default Logo;
