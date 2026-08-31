import React, { useEffect, useState } from 'react';
import { progressService } from '../services/progressService';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { StatCard } from '../components/common/StatCard';
import { Badge } from '../components/common/Badge';
import { ProgressBar } from '../components/common/ProgressBar';
import { TrendingUp, Clock, Flame, Award } from 'lucide-react';

export const ProgressPage = () => {
  const { user } = useApp();
  const [progressData, setProgressData] = useState(null);

  useEffect(() => {
    progressService.getProgress().then(setProgressData);
  }, []);

  if (!progressData) return null;

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-5xl mx-auto">
      <div className="space-y-1">
        <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">ANALYTICS</span>
        <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">Recent Progress</h1>
        <p className="text-sm text-[#45515E]">
          Overview of your activity, study hours, and career readiness.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={TrendingUp}
          label="Learning Progress"
          value={`${user?.readinessScore || 0}%`}
          subtext="Course Completion"
        />

        <StatCard
          icon={Clock}
          label="Learning Hours"
          value={`${progressData.totalHoursLearned || 0} hrs`}
          subtext="Total duration"
        />

        <StatCard
          icon={Flame}
          label="Active Streak"
          value={`${user?.streakDays || 0} Days`}
          subtext="Daily momentum"
        />

        <StatCard
          icon={Award}
          label="Skills Mastered"
          value={`${progressData.skillsMastered || 0} Skills`}
          subtext="Verified"
        />
      </div>

      <Card radius="24" className="p-6 space-y-4">
        <h2 className="text-lg font-bold text-[#0A0A0A]">Learning Activity Breakdown</h2>
        <div className="space-y-4 text-xs text-[#45515E]">
          <div className="space-y-1">
            <div className="flex justify-between font-semibold">
              <span>Courses Completed</span>
              <span className="text-[#0A0A0A]">{progressData.coursesCompletedCount || 1} / 3</span>
            </div>
            <ProgressBar value={33} color="dark" height="h-2" />
          </div>

          <div className="space-y-1">
            <div className="flex justify-between font-semibold">
              <span>Projects Completed</span>
              <span className="text-[#0A0A0A]">{progressData.projectsCompletedCount || 1} / 2</span>
            </div>
            <ProgressBar value={50} color="dark" height="h-2" />
          </div>
        </div>
      </Card>
    </div>
  );
};
