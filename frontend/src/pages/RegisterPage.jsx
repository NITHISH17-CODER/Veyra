import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight, User, Mail, Lock, Eye, EyeOff, AlertCircle } from 'lucide-react';
import { Button } from '../components/common/Button';
import { PasswordStrengthMeter } from '../components/common/PasswordStrengthMeter';
import { authService } from '../services/authService';
import { useApp } from '../context/AppContext';

export const RegisterPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [duplicateError, setDuplicateError] = useState(null);

  const navigate = useNavigate();
  const { showToast, refreshUserData } = useApp();

  const passRules = {
    minLength: password.length >= 8,
    hasUpper: /[A-Z]/.test(password),
    hasLower: /[a-z]/.test(password),
    hasNumber: /[0-9]/.test(password),
    hasSpecial: /[^A-Za-z0-9]/.test(password),
  };

  const rulesPassedCount = Object.values(passRules).filter(Boolean).length;
  const isStrongPassword = rulesPassedCount === 5;

  const validateForm = () => {
    const newErrors = {};
    const trimmedName = name.trim();
    const trimmedEmail = email.trim().toLowerCase();

    if (!trimmedName) {
      newErrors.name = "Full Name is required.";
    } else if (trimmedName.length < 2) {
      newErrors.name = "Full Name must be at least 2 characters.";
    }

    if (!trimmedEmail) {
      newErrors.email = "Email address is required.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmedEmail)) {
      newErrors.email = "Enter a valid email address.";
    }

    if (!password) {
      newErrors.password = "Password is required.";
    } else if (!isStrongPassword) {
      newErrors.password = "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character.";
    }

    if (!confirmPassword) {
      newErrors.confirmPassword = "Confirm password is required.";
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setDuplicateError(null);

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      const normalizedEmail = email.trim().toLowerCase();
      await authService.register({
        name: name.trim(),
        email: normalizedEmail,
        password,
        confirmPassword
      });

      await refreshUserData();
      showToast("Account created successfully! Welcome to Veyra.", "success");
      navigate('/onboarding');
    } catch (err) {
      const status = err.response?.status;
      const data = err.response?.data;

      if (!err.response) {
        const netMsg = "Unable to connect to the server. Please try again.";
        setErrors(prev => ({ ...prev, form: netMsg }));
        showToast(netMsg, "error");
      } else if (status === 409 || data?.code === 'EMAIL_ALREADY_EXISTS' || (typeof data?.detail === 'string' && data?.detail?.includes?.('already exists'))) {
        const msg = "An account with this email already exists. Please log in.";
        setDuplicateError(msg);
        showToast(msg, "warning");
      } else if (status === 422) {
        let msg = "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character.";
        if (Array.isArray(data?.detail)) {
          msg = data.detail.map(d => d.msg.replace('Value error, ', '')).join('. ');
        } else if (typeof data?.detail === 'string') {
          msg = data.detail;
        } else if (data?.message) {
          msg = data.message;
        }
        setErrors(prev => ({ ...prev, form: msg }));
        showToast(msg, "error");
      } else if (status >= 500) {
        const dbMsg = "Unable to create your account right now. Please try again.";
        setErrors(prev => ({ ...prev, form: dbMsg }));
        showToast(dbMsg, "error");
      } else {
        const errorMsg = typeof data?.detail === 'string' ? data.detail : (data?.message || err.message || "Registration failed. Please check your details.");
        setErrors(prev => ({ ...prev, form: errorMsg }));
        showToast(errorMsg, "error");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F7F8FA] flex items-center justify-center p-4 sm:p-8 font-sans">
      <div className="w-full max-w-4xl bg-white rounded-[24px] border border-[#E5E7EB] overflow-hidden grid grid-cols-1 md:grid-cols-12">
        {/* Left Side Branding */}
        <div className="md:col-span-5 bg-[#146EF5] text-white p-8 sm:p-10 flex flex-col justify-between border-r border-[#0B5ED7]">
          <div className="space-y-6">
            <NavLink to="/" className="flex items-center gap-2 group">
              <img
                src="/veyra-logo.png"
                alt="Veyra Logo"
                className="w-7 h-7 rounded-lg object-contain shadow-sm border border-white/30 shrink-0 group-hover:scale-105 transition-transform"
              />
              <span className="text-lg font-extrabold text-white tracking-tight">Veyra</span>
            </NavLink>

            <div className="space-y-3 pt-6">
              <h3 className="text-2xl font-bold text-white leading-tight">
                Start your tailored learning journey.
              </h3>
              <p className="text-xs text-blue-100 leading-relaxed">
                Define your career goals and let AI construct your personalized roadmap.
              </p>
            </div>
          </div>

          <div className="pt-8 text-[11px] text-blue-200 border-t border-white/20">
            &copy; 2026 Veyra Inc. All rights reserved.
          </div>
        </div>

        {/* Right Side Form */}
        <div className="md:col-span-7 p-8 sm:p-10 flex flex-col justify-center space-y-5 bg-white">
          <div className="space-y-1">
            <h2 className="text-2xl font-bold text-[#0A0A0A]">Create Account</h2>
            <p className="text-xs text-[#45515E]">Enter your information to get started</p>
          </div>

          {duplicateError && (
            <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 flex items-center gap-2.5">
              <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
              <div className="flex-1 flex items-center justify-between">
                <p className="text-xs font-medium text-amber-900">{duplicateError}</p>
                <button
                  type="button"
                  onClick={() => navigate('/login')}
                  className="text-xs font-bold underline text-amber-900 ml-2"
                >
                  Sign In
                </button>
              </div>
            </div>
          )}

          {errors.form && (
            <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 flex items-center gap-2.5">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              <p className="text-xs font-medium text-rose-900">{errors.form}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} noValidate className="space-y-3.5">
            <div className="space-y-1">
              <label className="text-xs font-semibold text-[#0A0A0A]">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-[#8E8E93] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none z-10" />
                <input
                  type="text"
                  placeholder="Full Name"
                  value={name}
                  onChange={(e) => {
                    setName(e.target.value);
                    if (errors.name || errors.form) setErrors(prev => ({ ...prev, name: null, form: null }));
                  }}
                  className="input-flat input-icon-left w-full"
                />
              </div>
              {errors.name && <p className="text-xs text-rose-500 font-medium">{errors.name}</p>}
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-[#0A0A0A]">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-[#8E8E93] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none z-10" />
                <input
                  type="email"
                  placeholder="name@example.com"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    setDuplicateError(null);
                    if (errors.email || errors.form) setErrors(prev => ({ ...prev, email: null, form: null }));
                  }}
                  className="input-flat input-icon-left w-full"
                />
              </div>
              {errors.email && <p className="text-xs text-rose-500 font-medium">{errors.email}</p>}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-[#0A0A0A]">Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-[#8E8E93] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none z-10" />
                  <input
                    type={showPassword ? "text" : "password"}
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => {
                      setPassword(e.target.value);
                      if (errors.password || errors.form) setErrors(prev => ({ ...prev, password: null, form: null }));
                    }}
                    className="input-flat input-icon-left input-icon-right w-full"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#8E8E93] hover:text-[#0A0A0A] z-10"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {errors.password && <p className="text-xs text-rose-500 font-medium">{errors.password}</p>}
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-[#0A0A0A]">Confirm Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-[#8E8E93] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none z-10" />
                  <input
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="••••••••"
                    value={confirmPassword}
                    onChange={(e) => {
                      setConfirmPassword(e.target.value);
                      if (errors.confirmPassword || errors.form) setErrors(prev => ({ ...prev, confirmPassword: null, form: null }));
                    }}
                    className="input-flat input-icon-left input-icon-right w-full"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#8E8E93] hover:text-[#0A0A0A] z-10"
                  >
                    {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {errors.confirmPassword && <p className="text-xs text-rose-500 font-medium">{errors.confirmPassword}</p>}
              </div>
            </div>

            {/* Password Strength Meter */}
            <PasswordStrengthMeter password={password} />

            <Button
              type="submit"
              variant="primary"
              size="lg"
              loading={loading}
              disabled={loading}
              icon={ArrowRight}
              iconPosition="right"
              className="w-full mt-2 justify-center"
            >
              {loading ? "Creating Account..." : "Create Account"}
            </Button>
          </form>

          <p className="text-center text-xs text-[#45515E] pt-2 border-t border-[#E5E7EB]">
            Already have an account?{' '}
            <NavLink to="/login" className="font-semibold text-[#0A0A0A] hover:underline">
              Sign In
            </NavLink>
          </p>
        </div>
      </div>
    </div>
  );
};
