import React from 'react';

export const getPasswordStrength = (pass) => {
  if (!pass) return { level: 0, label: 'Password strength', textClass: 'text-slate-400', bgClass: 'bg-slate-200' };

  let score = 0;
  const length = pass.length;
  const hasUpper = /[A-Z]/.test(pass);
  const hasLower = /[a-z]/.test(pass);
  const hasNum = /[0-9]/.test(pass);
  const hasSpec = /[^A-Za-z0-9]/.test(pass);
  const isSimple = /^[a-zA-Z]+$/.test(pass) || /^[0-9]+$/.test(pass);
  const hasRepeats = /(.)\1{2,}/.test(pass);

  if (length >= 8) score += 1;
  if (length >= 12) score += 1;
  if (hasUpper && hasLower) score += 1;
  if (hasNum) score += 0.5;
  if (hasSpec) score += 1;
  if (isSimple) score -= 1;
  if (hasRepeats) score -= 0.5;

  let level = 1;
  if (score < 2) level = 1;
  else if (score < 3.2) level = 2;
  else if (score < 4.2) level = 3;
  else level = 4;

  const states = {
    1: { label: 'Weak', textClass: 'text-rose-600', bgClass: 'bg-rose-500' },
    2: { label: 'Medium', textClass: 'text-amber-600', bgClass: 'bg-amber-500' },
    3: { label: 'Strong', textClass: 'text-blue-600', bgClass: 'bg-blue-600' },
    4: { label: 'Very Strong', textClass: 'text-emerald-600', bgClass: 'bg-emerald-500' },
  };

  return { level, ...states[level] };
};

export const PasswordStrengthMeter = ({ password }) => {
  if (!password) return null;

  const { level, label, textClass, bgClass } = getPasswordStrength(password);

  return (
    <div className="space-y-1.5 pt-1.5 animate-fadeIn">
      <div className="flex items-center justify-between text-xs font-semibold">
        <span className="text-[#8E8E93]">Password strength</span>
        <span className={`font-bold ${textClass}`}>{label}</span>
      </div>
      <div className="grid grid-cols-4 gap-1.5">
        {[1, 2, 3, 4].map((step) => (
          <div
            key={step}
            className={`h-1.5 rounded-full transition-all duration-300 ${
              step <= level ? bgClass : 'bg-[#E5E7EB]'
            }`}
          />
        ))}
      </div>
    </div>
  );
};
