import React from 'react';

export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  icon: Icon,
  iconPosition = 'left',
  loading = false,
  className = '',
  disabled = false,
  onClick,
  type = 'button',
  ...props
}) => {
  const baseStyles = "inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-[#146EF5] cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed select-none";

  const variants = {
    primary: "bg-[#146EF5] hover:bg-[#0B5ED7] text-white border border-[#146EF5] shadow-sm hover:shadow-md hover:shadow-blue-500/20 active:scale-[0.98]",
    secondary: "bg-[#FFFFFF] hover:bg-[#EAF3FF] text-[#146EF5] border border-[#DCE6F2] hover:border-[#146EF5]",
    outline: "bg-[#FFFFFF] hover:bg-[#EAF3FF] text-[#111827] border border-[#DCE6F2] hover:border-[#146EF5] hover:text-[#146EF5]",
    "outline-light": "bg-transparent border border-white/40 text-white hover:bg-white hover:text-[#146EF5]",
    coral: "bg-[#146EF5] hover:bg-[#0B5ED7] text-white border border-[#146EF5]",
    magenta: "bg-[#146EF5] hover:bg-[#0B5ED7] text-white border border-[#146EF5]",
    blue: "bg-[#146EF5] hover:bg-[#0B5ED7] text-white border border-[#146EF5]",
    ghost: "bg-transparent hover:bg-[#EAF3FF] text-[#475569] hover:text-[#146EF5]",
    danger: "bg-rose-600 hover:bg-rose-700 text-white border border-rose-600"
  };

  const sizes = {
    xs: "px-3 py-1 text-xs gap-1",
    sm: "px-4 py-2 text-xs gap-1.5",
    md: "px-5.5 py-2.5 text-sm gap-2",
    lg: "px-6 py-3.5 text-base gap-2.5",
    xl: "px-8 py-4 text-base gap-3 font-semibold"
  };

  return (
    <button
      type={type}
      className={`${baseStyles} ${variants[variant] || variants.primary} ${sizes[size]} ${className}`}
      disabled={disabled || loading}
      onClick={onClick}
      {...props}
    >
      {loading ? (
        <>
          <svg className="animate-spin h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{children}</span>
        </>
      ) : (
        <>
          {Icon && iconPosition === 'left' && <Icon className="w-4 h-4" />}
          <span>{children}</span>
          {Icon && iconPosition === 'right' && <Icon className="w-4 h-4" />}
        </>
      )}
    </button>
  );
};
