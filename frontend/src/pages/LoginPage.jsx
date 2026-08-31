import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { Sparkles, ArrowRight, Lock, Mail, Eye, EyeOff, AlertCircle, Check } from 'lucide-react';
import { Button } from '../components/common/Button';
import { PasswordStrengthMeter } from '../components/common/PasswordStrengthMeter';
import { authService } from '../services/authService';
import { profileService } from '../services/profileService';
import { useApp } from '../context/AppContext';

export const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [successBanner, setSuccessBanner] = useState(null);

  const navigate = useNavigate();
  const location = useLocation();
  const { showToast, refreshUserData } = useApp();

  useEffect(() => {
    if (location.state?.registeredMessage) {
      setSuccessBanner(location.state.registeredMessage);
    }
  }, [location]);

  const validateLoginForm = () => {
    const newErrors = {};
    const trimmedEmail = email.trim().toLowerCase();

    if (!trimmedEmail) {
      newErrors.email = "Email address is required.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmedEmail)) {
      newErrors.email = "Enter a valid email address.";
    }

    if (!password) {
      newErrors.password = "Password is required.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessBanner(null);

    if (!validateLoginForm()) {
      return;
    }

    setLoading(true);
    try {
      const normalizedEmail = email.trim().toLowerCase();
      const loginRes = await authService.login({ email: normalizedEmail, password });
      await refreshUserData();

      let hasCompleted = false;
      if (loginRes?.user?.onboarding_completed !== undefined) {
        hasCompleted = Boolean(loginRes.user.onboarding_completed);
      } else {
        try {
          const prof = await profileService.getProfile();
          if (prof) {
            hasCompleted = true;
          }
        } catch (e) {}
      }

      showToast("Signed in successfully!", "success");

      if (hasCompleted) {
        navigate('/dashboard');
      } else {
        navigate('/onboarding');
      }
    } catch (err) {
      let detail = "Invalid email or password.";
      if (!err.response) {
        detail = "Unable to connect to the server. Please try again.";
      } else if (err.response.status === 401) {
        detail = "Invalid email or password.";
      } else {
        detail = err.response?.data?.message || err.response?.data?.detail || "Invalid email or password.";
      }
      showToast(detail, "error");
      setErrors({ form: detail });
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
                Intelligence built around you.
              </h3>
              <p className="text-xs text-blue-100 leading-relaxed">
                Log in to access your personalized learning roadmap, skill quizzes, and project evaluations.
              </p>
            </div>
          </div>

          <div className="pt-8 text-[11px] text-blue-200 border-t border-white/20">
            &copy; 2026 Veyra Inc. All rights reserved.
          </div>
        </div>

        {/* Right Side Form */}
        <div className="md:col-span-7 p-8 sm:p-10 flex flex-col justify-center space-y-6 bg-white">
          <div className="space-y-1">
            <h2 className="text-2xl font-bold text-[#0A0A0A]">Sign In</h2>
            <p className="text-xs text-[#45515E]">Enter your account credentials to continue</p>
          </div>

          {successBanner && (
            <div className="p-3 rounded-xl bg-[#E8FFEA] border border-[#1BA673]/30 flex items-center gap-2.5">
              <Check className="w-4 h-4 text-[#1BA673] shrink-0" />
              <p className="text-xs font-medium text-[#1BA673]">{successBanner}</p>
            </div>
          )}

          {errors.form && (
            <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 flex items-center gap-2.5">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              <p className="text-xs font-medium text-rose-900">{errors.form}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} noValidate className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-[#0A0A0A]">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-[#8E8E93] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none z-10" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    if (errors.email || errors.form) setErrors(prev => ({ ...prev, email: null, form: null }));
                  }}
                  placeholder="name@example.com"
                  className="input-flat input-icon-left w-full"
                />
              </div>
              {errors.email && (
                <p className="text-xs text-rose-500 font-medium">{errors.email}</p>
              )}
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-[#0A0A0A]">Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-[#8E8E93] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none z-10" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    if (errors.password || errors.form) setErrors(prev => ({ ...prev, password: null, form: null }));
                  }}
                  placeholder="••••••••"
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
              {errors.password && (
                <p className="text-xs text-rose-500 font-medium">{errors.password}</p>
              )}
              <PasswordStrengthMeter password={password} />
            </div>

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
              {loading ? "Signing In..." : "Sign In"}
            </Button>
          </form>

          <div className="pt-4 border-t border-[#E5E7EB] text-center text-xs text-[#45515E]">
            Don't have an account?{' '}
            <NavLink to="/register" className="font-semibold text-[#1456F0] hover:underline">
              Create account
            </NavLink>
          </div>
        </div>
      </div>
    </div>
  );
};
