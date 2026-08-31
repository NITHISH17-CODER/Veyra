import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Bell, Shield, Sliders, Save } from 'lucide-react';

export const SettingsPage = () => {
  const { user, updateUserPreferences, showToast } = useApp();

  const [weeklyGoal, setWeeklyGoal] = useState(user?.weeklyGoalHours || 10);
  const [contentType, setContentType] = useState(user?.learningStyle || 'Project-based');
  const [difficulty, setDifficulty] = useState(user?.difficultyPreference || 'Intermediate');
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [streakReminders, setStreakReminders] = useState(true);

  const handleSave = () => {
    updateUserPreferences({
      weeklyGoalHours: weeklyGoal,
      learningStyle: contentType,
      difficultyPreference: difficulty
    });
    showToast("Settings updated successfully!", "success");
  };

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-4xl mx-auto">
      <div className="flex items-center justify-between border-b border-[#DCE6F2] pb-6">
        <div className="space-y-1">
          <span className="text-xs font-bold text-[#146EF5] uppercase tracking-wider">SETTINGS</span>
          <h1 className="text-3xl font-bold text-[#111827] tracking-tight">Application Settings</h1>
          <p className="text-sm text-[#475569]">
            Configure learning goals, notifications, and preferences.
          </p>
        </div>
        <Button variant="primary" size="md" icon={Save} onClick={handleSave}>
          Save Changes
        </Button>
      </div>

      <div className="space-y-6">
        <Card radius="16" className="p-6 space-y-4 border-[#DCE6F2]">
          <h2 className="text-lg font-bold text-[#111827] flex items-center gap-2">
            <Sliders className="w-5 h-5 text-[#146EF5]" />
            <span>Learning Preferences</span>
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-2">
            <div className="space-y-2">
              <label className="text-xs font-bold text-[#111827]">Weekly Goal ({weeklyGoal} hrs/wk)</label>
              <input
                type="range"
                min="2"
                max="30"
                step="1"
                value={weeklyGoal}
                onChange={(e) => setWeeklyGoal(parseInt(e.target.value))}
                className="w-full accent-[#146EF5] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-[#64748B] font-mono">
                <span>2 hrs</span>
                <span>15 hrs</span>
                <span>30 hrs</span>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-bold text-[#111827]">Preferred Content Format</label>
              <select
                value={contentType}
                onChange={(e) => setContentType(e.target.value)}
                className="input-flat w-full text-xs border-[#DCE6F2] focus:border-[#146EF5]"
              >
                <option value="Project-based">Project-based (Recommended)</option>
                <option value="Hands-on">Hands-on Code Exercises</option>
                <option value="Video">Video Tutorials</option>
                <option value="Reading">Documentation & Reading</option>
              </select>
            </div>
          </div>
        </Card>

        <Card radius="16" className="p-6 space-y-4 border-[#DCE6F2]">
          <h2 className="text-lg font-bold text-[#111827] flex items-center gap-2">
            <Bell className="w-5 h-5 text-[#146EF5]" />
            <span>Notifications &amp; Reminders</span>
          </h2>

          <div className="space-y-3 pt-2">
            <label className="flex items-center justify-between p-4 rounded-xl bg-[#F5F9FF] border border-[#DCE6F2] cursor-pointer">
              <div>
                <span className="text-xs font-bold text-[#111827] block">Daily Streak Reminders</span>
                <span className="text-[10px] text-[#64748B] block">Get reminded to maintain your learning streak.</span>
              </div>
              <input
                type="checkbox"
                checked={streakReminders}
                onChange={(e) => setStreakReminders(e.target.checked)}
                className="rounded border-[#DCE6F2] bg-white text-[#146EF5] focus:ring-[#146EF5]"
              />
            </label>

            <label className="flex items-center justify-between p-4 rounded-xl bg-[#F5F9FF] border border-[#DCE6F2] cursor-pointer">
              <div>
                <span className="text-xs font-bold text-[#111827] block">Path Recalculation Digest</span>
                <span className="text-[10px] text-[#64748B] block">Receive emails when AI recalculates your roadmap.</span>
              </div>
              <input
                type="checkbox"
                checked={emailNotifications}
                onChange={(e) => setEmailNotifications(e.target.checked)}
                className="rounded border-[#DCE6F2] bg-white text-[#146EF5] focus:ring-[#146EF5]"
              />
            </label>
          </div>
        </Card>

        <Card radius="16" className="p-6 space-y-4 border-[#DCE6F2]">
          <h2 className="text-lg font-bold text-[#111827] flex items-center gap-2">
            <Shield className="w-5 h-5 text-[#146EF5]" />
            <span>Privacy &amp; API</span>
          </h2>

          <div className="p-4 rounded-xl bg-[#F5F9FF] border border-[#DCE6F2] text-xs space-y-2">
            <span className="text-[#64748B] font-bold block">REST API Base URL</span>
            <input
              type="text"
              readOnly
              value="http://localhost:8000/api"
              className="input-flat w-full font-mono text-xs border-[#DCE6F2]"
            />
          </div>
        </Card>
      </div>
    </div>
  );
};
