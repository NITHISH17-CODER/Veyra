import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  Map,
  BookOpen,
  CheckSquare,
  FolderGit2,
  BarChart2,
  Newspaper,
  User,
  Settings,
  LogOut,
  Sparkles,
  ChevronRight,
  ShieldAlert
} from 'lucide-react';
import { useApp } from '../../context/AppContext';

export const Sidebar = ({ mobileOpen, setMobileOpen }) => {
  const { user, logout } = useApp();
  const navigate = useNavigate();
  const [isHovered, setIsHovered] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { label: "Overview", path: "/dashboard", icon: LayoutDashboard },
    { label: "My Roadmap", path: "/learning-path", icon: Map },
    { label: "Learn", path: "/courses", icon: BookOpen },
    { label: "Quizzes", path: "/quizzes", icon: CheckSquare },
    { label: "Projects", path: "/projects", icon: FolderGit2 },
    { label: "Skills", path: "/skill-gap", icon: BarChart2 },
    { label: "News", path: "/news", icon: Newspaper },
    { label: "Profile", path: "/profile", icon: User },
    { label: "Settings", path: "/settings", icon: Settings },
  ];

  return (
    <>
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-sm lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className={`fixed top-0 bottom-0 left-0 z-50 bg-white/95 backdrop-blur-xl border-r border-slate-200/80 shadow-[4px_0_24px_rgba(0,0,0,0.04)] flex flex-col justify-between transition-all duration-300 ease-in-out lg:translate-x-0 ${
          mobileOpen ? 'translate-x-0 w-64' : '-translate-x-full lg:translate-x-0'
        } ${isHovered ? 'lg:w-64' : 'lg:w-20'}`}
      >
        <div className="flex flex-col h-full overflow-hidden">
          {/* Brand Header */}
          <div className="h-18 px-4 border-b border-slate-100 flex items-center justify-between shrink-0">
            <NavLink to="/dashboard" className="flex items-center gap-3 group">
              <img
                src="/veyra-logo.png"
                alt="Veyra Logo"
                className="w-10 h-10 rounded-xl object-contain shadow-sm border border-[#1456F0]/20 shrink-0 transition-transform duration-200 group-hover:scale-105"
              />
              <div className={`flex flex-col transition-opacity duration-200 ${
                isHovered || mobileOpen ? 'opacity-100' : 'lg:opacity-0 lg:hidden'
              }`}>
                <span className="text-lg font-extrabold text-[#1456F0] tracking-tight font-sans">
                  Veyra
                </span>
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">AI Platform</span>
              </div>
            </NavLink>
          </div>

          {/* Active Goal Pill (Visible when expanded) */}
          {user?.targetGoal && (isHovered || mobileOpen) && (
            <div className="mx-3 my-3 p-3 rounded-2xl bg-blue-50/80 border border-blue-100/60 transition-all">
              <span className="text-[10px] font-bold text-[#1456F0] uppercase tracking-wider block">Target Track</span>
              <span className="text-xs font-bold text-slate-900 truncate block mt-0.5">{user.targetGoal}</span>
            </div>
          )}

          {/* Navigation Items */}
          <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto overflow-x-hidden">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileOpen(false)}
                  title={!isHovered && !mobileOpen ? item.label : undefined}
                  className={({ isActive }) =>
                    `relative flex items-center gap-3.5 px-3.5 py-3 rounded-2xl text-sm font-semibold transition-all duration-200 group ${
                      isActive
                        ? 'bg-[#1456F0] text-white shadow-lg shadow-blue-500/20'
                        : 'text-slate-600 hover:bg-blue-50/80 hover:text-[#1456F0]'
                    }`
                  }
                >
                  <Icon className="w-5 h-5 shrink-0 transition-transform duration-200 group-hover:scale-110" />
                  <span className={`whitespace-nowrap transition-opacity duration-200 ${
                    isHovered || mobileOpen ? 'opacity-100' : 'lg:opacity-0 lg:hidden'
                  }`}>
                    {item.label}
                  </span>

                  {/* Tooltip for collapsed view */}
                  {!isHovered && !mobileOpen && (
                    <div className="absolute left-full ml-3 px-3 py-1.5 bg-slate-900 text-white text-xs font-bold rounded-xl whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity duration-150 shadow-xl z-50">
                      {item.label}
                    </div>
                  )}
                </NavLink>
              );
            })}
          </nav>

          {/* Bottom User Bar */}
          <div className="p-3 border-t border-slate-100 bg-slate-50/50 shrink-0">
            <div className="flex items-center justify-between">
              <NavLink
                to="/profile"
                onClick={() => setMobileOpen(false)}
                className="flex items-center gap-3 overflow-hidden hover:opacity-80 transition-opacity"
              >
                <div className="w-9 h-9 rounded-2xl bg-[#146EF5] text-white font-bold flex items-center justify-center text-xs shadow-sm shrink-0">
                  {user?.name ? user.name.substring(0, 2).toUpperCase() : "VR"}
                </div>
                <div className={`truncate transition-opacity duration-200 ${
                  isHovered || mobileOpen ? 'opacity-100' : 'lg:opacity-0 lg:hidden'
                }`}>
                  <span className="text-xs font-bold text-slate-900 block truncate">{user?.name || "User Profile"}</span>
                  <span className="text-[10px] text-slate-500 block truncate">{user?.email || "user@veyra.ai"}</span>
                </div>
              </NavLink>

              <button
                onClick={handleLogout}
                className={`p-2 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors shrink-0 ${
                  !isHovered && !mobileOpen ? 'hidden' : 'block'
                }`}
                title="Log Out"
              >
                <LogOut className="w-4.5 h-4.5" />
              </button>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};
