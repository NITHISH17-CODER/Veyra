import React, { useState, useEffect, useRef } from 'react';
import { Bell, Menu, Flame, X, CheckCheck } from 'lucide-react';
import { useApp } from '../../context/AppContext';
import api from '../../services/api';

export const Topbar = ({ onOpenMobileMenu }) => {
  const { user } = useApp();
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [streak, setStreak] = useState({ current_streak: 0, longest_streak: 0, earned_today: false });
  const [showStreakPopup, setShowStreakPopup] = useState(false);
  const notifRef = useRef(null);

  // Fetch streak on mount
  useEffect(() => {
    api.get('/streak')
      .then(res => {
        setStreak(res.data);
        const sessionKey = `streak_popup_${new Date().toISOString().split('T')[0]}`;
        if (res.data.earned_today && !sessionStorage.getItem(sessionKey)) {
          setShowStreakPopup(true);
          sessionStorage.setItem(sessionKey, 'true');
          setTimeout(() => setShowStreakPopup(false), 4000);
        }
      })
      .catch(() => {});
  }, []);

  // Fetch notifications on mount and when panel opens
  useEffect(() => {
    if (showNotifications) {
      api.get('/notifications')
        .then(res => setNotifications(res.data))
        .catch(() => {});
    }
  }, [showNotifications]);

  // Close notification panel on outside click
  useEffect(() => {
    const handler = (e) => {
      if (notifRef.current && !notifRef.current.contains(e.target)) {
        setShowNotifications(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const markAllRead = () => {
    api.post('/notifications/read-all')
      .then(() => {
        setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
      })
      .catch(() => {});
  };

  const markSingleRead = (id) => {
    api.post(`/notifications/${id}/read`)
      .then(() => {
        setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
      })
      .catch(() => {});
  };

  const unreadCount = notifications.filter(n => !n.is_read).length;

  return (
    <>
      <header className="sticky top-0 z-30 h-18 bg-white/80 backdrop-blur-xl border-b border-slate-200/60 px-4 sm:px-8 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={onOpenMobileMenu}
            className="p-2 rounded-xl text-slate-700 hover:bg-slate-100 lg:hidden"
            aria-label="Toggle navigation"
          >
            <Menu className="w-5 h-5" />
          </button>
        </div>

        <div className="flex items-center gap-3">
          {/* Compact Streak Badge */}
          <div
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-gradient-to-r from-amber-50 to-orange-50 border border-orange-200/60 text-slate-900 text-xs font-bold cursor-default select-none transition-transform hover:scale-105 shadow-sm"
            title={`Longest streak: ${streak.longest_streak} days`}
          >
            <Flame className="w-4 h-4 text-orange-500 fill-orange-500" />
            <span>{streak.current_streak}</span>
          </div>

          {/* Notifications Dropdown */}
          <div className="relative" ref={notifRef}>
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2.5 rounded-2xl text-slate-700 bg-slate-100/80 hover:bg-slate-200/60 transition-colors"
              aria-label="Notifications"
            >
              <Bell className="w-4.5 h-4.5" />
              {unreadCount > 0 && (
                <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-[#1456F0] ring-2 ring-white"></span>
              )}
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-3xl border border-slate-200 shadow-2xl p-5 z-50 space-y-3 animate-fadeIn">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <span className="text-xs font-bold text-slate-900">Notifications ({notifications.length})</span>
                  {unreadCount > 0 && (
                    <button
                      onClick={markAllRead}
                      className="text-[10px] font-bold text-[#1456F0] hover:text-blue-700 flex items-center gap-1"
                    >
                      <CheckCheck className="w-3 h-3" /> Mark all read
                    </button>
                  )}
                </div>
                <div className="space-y-2 max-h-60 overflow-y-auto">
                  {notifications.length > 0 ? (
                    notifications.map((notif) => (
                      <div
                        key={notif.id}
                        onClick={() => !notif.is_read && markSingleRead(notif.id)}
                        className={`p-3 rounded-2xl border text-xs space-y-1 cursor-pointer transition-colors ${
                          notif.is_read
                            ? 'bg-slate-50/60 border-slate-100 opacity-60'
                            : 'bg-blue-50/60 border-blue-100'
                        }`}
                      >
                        <div className="flex items-center justify-between text-slate-900 font-bold text-[11px]">
                          <span>{notif.title}</span>
                          {!notif.is_read && <span className="w-2 h-2 rounded-full bg-[#1456F0] shrink-0"></span>}
                        </div>
                        <p className="text-slate-600 text-xs">{notif.message}</p>
                      </div>
                    ))
                  ) : (
                    <p className="text-xs text-slate-400 text-center py-4">No notifications yet.</p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Streak Celebration Popup */}
      {showStreakPopup && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-slate-900/40 backdrop-blur-sm animate-fadeIn">
          <div className="relative bg-white rounded-3xl p-8 shadow-2xl text-center max-w-sm mx-4 animate-bounceIn border border-slate-100">
            <button
              onClick={() => setShowStreakPopup(false)}
              className="absolute top-3 right-3 p-1.5 rounded-full hover:bg-slate-100"
            >
              <X className="w-4 h-4 text-slate-400" />
            </button>
            <div className="text-6xl mb-3 animate-pulse">🔥</div>
            <h2 className="text-2xl font-black text-slate-900 mb-1">STREAK +1!</h2>
            <p className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-amber-500 mb-2">
              {streak.current_streak} Day{streak.current_streak > 1 ? 's' : ''}
            </p>
            <p className="text-sm text-slate-600">{streak.message}</p>
            <div className="mt-4 flex gap-2 justify-center">
              {[...Array(Math.min(streak.current_streak, 7))].map((_, i) => (
                <span key={i} className="text-xl animate-bounce" style={{ animationDelay: `${i * 100}ms` }}>🔥</span>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  );
};
