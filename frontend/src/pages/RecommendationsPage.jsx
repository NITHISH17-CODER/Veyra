import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { recommendationService } from '../services/recommendationService';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { LoadingState } from '../components/common/LoadingState';
import { ArrowRight, Sparkles } from 'lucide-react';

export const RecommendationsPage = () => {
  const { user } = useApp();
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    recommendationService.getRecommendations()
      .then((data) => {
        // Only accept real API data — no inline mock fallback
        const apiCourses = data?.courses || [];
        setCourses(apiCourses);
      })
      .catch((err) => {
        console.error('Recommendations API failed:', err);
        setError('Could not load recommendations. Please try again.');
        setCourses([]);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingState message="Loading your personalized recommendations..." />;

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-4xl mx-auto">
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">MY LEARNING</span>
          {user?.targetGoal && (
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-[#0A0A0A] text-white flex items-center gap-1">
              <Sparkles className="w-3 h-3" /> {user.targetGoal}
            </span>
          )}
        </div>
        <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">Recommended for your path</h1>
        <p className="text-sm text-[#45515E]">
          Courses curated from your career goal, personalized roadmap, and identified skill gaps.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-sm text-rose-700">{error}</div>
      )}

      {courses.length === 0 && !error && (
        <Card radius="16" className="p-8 text-center space-y-3">
          <p className="text-sm font-semibold text-[#0A0A0A]">No recommendations available yet.</p>
          <p className="text-xs text-[#8E8E93]">Complete your onboarding and learning path to unlock personalized recommendations.</p>
          <Button variant="primary" size="md" onClick={() => navigate('/learning-path')}>View My Roadmap</Button>
        </Card>
      )}

      <div className="space-y-4">
        {courses.map((course) => (
          <Card key={course.id} radius="16" className="p-6 space-y-4 bg-white border border-[#E5E7EB]">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge variant={course.isPaid ? 'dark' : 'surface'}>
                    {course.isPaid ? `Paid • ${course.price || '$29'}` : 'Free'}
                  </Badge>
                  <span className="text-xs text-[#8E8E93]">{course.difficulty || 'Intermediate'}</span>
                </div>
                <h3 className="text-lg font-bold text-[#0A0A0A]">{course.title}</h3>
                <p className="text-xs text-[#8E8E93]">Provider: {course.provider || 'PathPilot'}</p>
              </div>

              <Button
                variant={course.isPaid ? "secondary" : "primary"}
                size="md"
                icon={ArrowRight}
                iconPosition="right"
                onClick={() => navigate(`/courses/${course.id}`)}
              >
                {course.isPaid ? 'Buy Course' : 'View Course'}
              </Button>
            </div>

            {(course.whyRecommended || course.reason) && (
              <div className="p-3 rounded-xl bg-[#F7F8FA] border border-[#E5E7EB] text-xs space-y-1">
                <span className="font-semibold text-[#0A0A0A]">Why recommended:</span>
                <p className="text-[#45515E]">{course.whyRecommended || course.reason}</p>
              </div>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
};
