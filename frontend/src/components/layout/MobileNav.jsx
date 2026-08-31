import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Map, Compass, BarChart3, Bot } from 'lucide-react';

export const MobileNav = () => {
  const items = [
    { label: 'Home', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Path', path: '/learning-path', icon: Map },
    { label: 'Explore', path: '/courses', icon: Compass },
    { label: 'Progress', path: '/progress', icon: BarChart3 },
    { label: 'AI', path: '/ai-assistant', icon: Bot, badge: 'AI' },
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-xl border-t border-slate-200 lg:hidden shadow-lg">
      <nav className="flex items-center justify-around py-2 px-1">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex flex-col items-center gap-1 py-1 px-3 rounded-xl transition-all relative ${
                  isActive
                    ? 'text-[#1456F0] font-bold'
                    : 'text-slate-500 hover:text-slate-800'
                }`
              }
            >
              <div className="relative">
                <Icon className="w-5 h-5" />
                {item.badge && (
                  <span className="absolute -top-1 -right-2 px-1 py-0.2 text-[8px] font-extrabold bg-blue-100 text-[#1456F0] rounded-full">
                    {item.badge}
                  </span>
                )}
              </div>
              <span className="text-[10px] tracking-tight">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </div>
  );
};
