import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { courseService } from '../services/courseService';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { ProgressBar } from '../components/common/ProgressBar';
import { LoadingState } from '../components/common/LoadingState';
import { ArrowRight, BookOpen, Sparkles, PlayCircle, CheckCircle2 } from 'lucide-react';

export const CoursesPage = () => {
  const navigate = useNavigate();
  const { user, roadmap } = useApp();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [navigatingAction, setNavigatingAction] = useState(false);

  useEffect(() => {
    const fetchCourses = async () => {
      setLoading(true);
      try {
        const data = await courseService.getCourses();
        if (Array.isArray(data)) {
          setCourses(data);
        }
      } catch (err) {
        console.warn('Failed to load courses:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, []);

  // Determine user's target goal string
  const userGoal = user?.targetGoal || roadmap?.career || '';

  // Match priority course dynamically based on authenticated user's target goal
  const findPriorityCourse = (allCourses, goalStr) => {
    if (!allCourses || allCourses.length === 0) return { priority: null, others: [] };
    if (!goalStr || !goalStr.trim()) return { priority: allCourses[0], others: allCourses.slice(1) };

    const cleanGoal = goalStr.toLowerCase().trim();

    let matchIndex = allCourses.findIndex((c) => {
      const titleLower = (c.title || c.career_name || '').toLowerCase();
      const slugLower = (c.slug || '').toLowerCase();

      if (cleanGoal.includes('sde') || cleanGoal.includes('software')) {
        return slugLower === 'sde' || titleLower.includes('software');
      }
      if (cleanGoal.includes('frontend')) {
        return slugLower.includes('frontend') || titleLower.includes('frontend');
      }
      if (cleanGoal.includes('backend')) {
        return slugLower.includes('backend') || titleLower.includes('backend');
      }
      if (cleanGoal.includes('cyber') || cleanGoal.includes('security')) {
        return slugLower.includes('cyber') || titleLower.includes('cybersecurity');
      }
      if (cleanGoal.includes('ai') || cleanGoal.includes('intelligence')) {
        return slugLower.includes('ai') || titleLower.includes('ai engineer');
      }

      return titleLower.includes(cleanGoal) || cleanGoal.includes(titleLower);
    });

    if (matchIndex === -1) matchIndex = 0;

    const priority = allCourses[matchIndex];
    const others = allCourses.filter((_, idx) => idx !== matchIndex);
    return { priority, others };
  };

  const { priority: priorityCourse, others: otherCourses } = findPriorityCourse(courses, userGoal);

  // Handle Continue Learning for Priority Course
  const handleContinueLearning = async (priority) => {
    if (!priority) return;
    setNavigatingAction(true);
    try {
      const targetSlug = priority.slug || priority.id;
      const actionRes = await courseService.getContinueAction(targetSlug).catch(() => null);

      if (actionRes && actionRes.lesson_id && actionRes.module_id) {
        navigate(`/courses/${targetSlug}/modules/${actionRes.module_id}/lessons/${actionRes.lesson_id}`);
      } else if (actionRes && actionRes.module_id) {
        navigate(`/courses/${targetSlug}/modules/${actionRes.module_id}`);
      } else {
        navigate(`/courses/${targetSlug}`);
      }
    } catch (err) {
      navigate(`/courses/${priority.slug || priority.id}`);
    } finally {
      setNavigatingAction(false);
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-6xl mx-auto pb-12">
      {/* Header Banner - Clean & Focused without Search Bar */}
      <div className="border-b border-[#E5E7EB] pb-6 space-y-1">
        <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">LEARNING CATALOG</span>
        <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">Personalized Learning Tracks</h1>
        <p className="text-sm text-[#45515E]">
          Structured core career programs matched directly to your career goal.
        </p>
      </div>

      {loading ? (
        <LoadingState message="Loading course catalog..." />
      ) : (
        <div className="space-y-10">
          {/* SECTION 1: YOUR PATH (User's Priority Course) */}
          {priorityCourse && (
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#1456F0]" />
                <h2 className="text-xs font-bold text-[#1456F0] uppercase tracking-wider">YOUR PATH</h2>
              </div>

              <Card radius="24" className="p-8 border-2 border-[#1456F0] bg-gradient-to-br from-white via-[#F8FAFC] to-[#F1F5F9] shadow-md relative overflow-hidden">
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                  <div className="space-y-3 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-[#1456F0] text-white">
                        Your Target Career
                      </span>
                      <span className="text-xs text-[#8E8E93] font-semibold">{priorityCourse.difficulty || 'Intermediate'}</span>
                    </div>

                    <h3 className="text-2xl font-extrabold text-[#0A0A0A] tracking-tight">
                      {priorityCourse.title}
                    </h3>
                    <p className="text-sm text-[#45515E] leading-relaxed max-w-2xl">
                      {priorityCourse.tagline || priorityCourse.description}
                    </p>

                    {priorityCourse.skills_covered && priorityCourse.skills_covered.length > 0 && (
                      <div className="flex flex-wrap gap-1.5 pt-2">
                        {priorityCourse.skills_covered.map((sk) => (
                          <Badge key={sk} variant="slate" size="xs">
                            {sk}
                          </Badge>
                        ))}
                      </div>
                    )}

                    <div className="pt-2 flex flex-wrap items-center gap-6 text-xs text-[#45515E]">
                      {priorityCourse.total_modules > 0 && <span><strong>{priorityCourse.total_modules}</strong> Modules</span>}
                      {priorityCourse.total_lessons > 0 && <span><strong>{priorityCourse.total_lessons}</strong> Lessons</span>}
                      {priorityCourse.total_projects > 0 && <span><strong>{priorityCourse.total_projects}</strong> Capstone Projects</span>}
                    </div>

                    {priorityCourse.progress_percentage > 0 && (
                      <div className="space-y-1.5 pt-2 max-w-md">
                        <div className="flex justify-between text-xs font-semibold">
                          <span className="text-[#0A0A0A]">Overall Progress</span>
                          <span className="font-mono text-[#1456F0]">{priorityCourse.progress_percentage}%</span>
                        </div>
                        <ProgressBar value={priorityCourse.progress_percentage} color="dark" height="h-2" />
                      </div>
                    )}
                  </div>

                  <div className="shrink-0 flex flex-col items-stretch lg:items-end gap-3 min-w-[200px]">
                    <Button
                      variant="primary"
                      size="lg"
                      icon={PlayCircle}
                      loading={navigatingAction}
                      onClick={() => handleContinueLearning(priorityCourse)}
                      className="justify-center shadow-md text-sm font-bold"
                    >
                      Continue Learning →
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      icon={ArrowRight}
                      iconPosition="right"
                      onClick={() => navigate(`/courses/${priorityCourse.slug || priorityCourse.id}`)}
                      className="justify-center"
                    >
                      Course Syllabus
                    </Button>
                  </div>
                </div>
              </Card>
            </div>
          )}

          {/* SECTION 2: EXPLORE OTHER COURSES */}
          {otherCourses.length > 0 && (
            <div className="space-y-4 pt-6 border-t border-[#E5E7EB]">
              <div className="space-y-1">
                <h2 className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">EXPLORE OTHER COURSES</h2>
                <p className="text-xs text-[#8E8E93]">Explore additional domain specialization tracks.</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {otherCourses.map((crs) => (
                  <Card key={crs.id} radius="20" className="p-6 space-y-4 flex flex-col justify-between hover:border-[#0A0A0A]/30 transition-all">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <Badge variant="surface">
                          {crs.difficulty || 'Intermediate'}
                        </Badge>
                        <span className="text-xs text-[#8E8E93] font-semibold">{crs.estimated_duration || '3 Months'}</span>
                      </div>

                      <h3 className="text-lg font-bold text-[#0A0A0A]">{crs.title}</h3>
                      <p className="text-xs text-[#45515E] line-clamp-2">{crs.tagline || crs.description}</p>

                      {crs.skills_covered && crs.skills_covered.length > 0 && (
                        <div className="flex flex-wrap gap-1 pt-1">
                          {crs.skills_covered.slice(0, 3).map((sk) => (
                            <Badge key={sk} variant="slate" size="xs">
                              {sk}
                            </Badge>
                          ))}
                        </div>
                      )}

                      {crs.progress_percentage > 0 && (
                        <div className="space-y-1 pt-1">
                          <div className="flex justify-between text-[11px] text-[#45515E]">
                            <span>Progress</span>
                            <span className="font-mono font-bold">{crs.progress_percentage}%</span>
                          </div>
                          <ProgressBar value={crs.progress_percentage} color="dark" height="h-1.5" />
                        </div>
                      )}
                    </div>

                    <Button
                      variant="outline"
                      size="sm"
                      icon={ArrowRight}
                      iconPosition="right"
                      onClick={() => navigate(`/courses/${crs.slug || crs.id}`)}
                      className="w-full justify-center mt-2"
                    >
                      Explore Track
                    </Button>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
