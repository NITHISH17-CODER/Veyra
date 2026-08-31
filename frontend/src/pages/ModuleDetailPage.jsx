import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { courseService } from '../services/courseService';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { ProgressBar } from '../components/common/ProgressBar';
import { LoadingState } from '../components/common/LoadingState';
import { ArrowLeft, Play, Check, Lock, FileCheck } from 'lucide-react';

export const ModuleDetailPage = () => {
  const { slug, moduleId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useApp();

  const [moduleData, setModuleData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchModule = async () => {
      setLoading(true);
      try {
        const data = await courseService.getModuleDetail(slug, moduleId);
        setModuleData(data);
      } catch (err) {
        console.error('Failed to load module:', err);
        showToast('Error loading module from database.', 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchModule();
  }, [slug, moduleId]);

  if (loading) return <LoadingState message="Loading module curriculum..." />;
  if (!moduleData) return (
    <Card radius="24" className="p-12 text-center space-y-4 max-w-md mx-auto my-12">
      <h2 className="text-xl font-bold text-[#0A0A0A]">Module Not Found</h2>
      <Button variant="primary" size="md" onClick={() => navigate(`/courses/${slug}`)}>
        Back to Course
      </Button>
    </Card>
  );

  const lessons = moduleData.lessons || [];
  const completedLessonsCount = lessons.filter((l) => l.is_completed).length;
  const allLessonsCompleted = completedLessonsCount === lessons.length && lessons.length > 0;
  const isAssessmentPassed = moduleData.assessment_passed;

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-5xl mx-auto">
      {/* Back link */}
      <button
        onClick={() => navigate(`/courses/${slug}`)}
        className="inline-flex items-center gap-2 text-xs font-bold text-[#8E8E93] hover:text-[#0A0A0A] transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Course Overview</span>
      </button>

      {/* Module Card */}
      <Card radius="24" className="p-8 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">
              Module {moduleData.module_number}
            </span>
            <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">{moduleData.title}</h1>
          </div>
          <Badge variant="dark">
            {completedLessonsCount} / {lessons.length} Lessons Completed
          </Badge>
        </div>

        <p className="text-sm text-[#45515E] leading-relaxed">{moduleData.description}</p>

        {/* Skills Chips */}
        {moduleData.skills && moduleData.skills.length > 0 && (
          <div className="space-y-2 pt-2 border-t border-[#E5E7EB]">
            <span className="text-xs font-semibold text-[#8E8E93] block">Skills:</span>
            <div className="flex flex-wrap gap-2">
              {moduleData.skills.map((sk) => (
                <Badge key={sk} variant="surface">{sk}</Badge>
              ))}
            </div>
          </div>
        )}

        <div className="pt-2">
          <ProgressBar value={moduleData.progress_percentage || 0} color="dark" showPercentage />
        </div>
      </Card>

      {/* Lessons Checklist & Assessment CTA */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-8 space-y-4">
          <h2 className="text-lg font-bold text-[#0A0A0A]">Lessons</h2>

          <div className="space-y-3">
            {lessons.map((lesson, idx) => {
              const isDone = lesson.is_completed;
              const isCurrent = !isDone && (idx === 0 || lessons[idx - 1]?.is_completed);
              const isLocked = !isDone && !isCurrent;

              return (
                <Card
                  key={lesson.id}
                  onClick={() => !isLocked && navigate(`/courses/${slug}/modules/${moduleId}/lessons/${lesson.id}`)}
                  className={`p-4 transition-all flex items-center justify-between gap-4 ${
                    isLocked ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-[#0A0A0A]'
                  }`}
                >
                  <div className="flex items-center gap-3.5">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs ${
                      isDone
                        ? 'bg-[#0A0A0A] text-white'
                        : isCurrent
                        ? 'bg-[#0A0A0A] text-white'
                        : 'bg-[#F2F3F5] text-[#8E8E93]'
                    }`}>
                      {isDone ? <Check className="w-4 h-4 text-white" /> : isCurrent ? '●' : '🔒'}
                    </div>

                    <div className="space-y-0.5">
                      <h4 className="text-sm font-bold text-[#0A0A0A]">{lesson.title}</h4>
                      <p className="text-xs text-[#8E8E93]">{lesson.description || 'Lesson Module'}</p>
                    </div>
                  </div>

                  <Button
                    size="sm"
                    variant={isDone ? 'outline' : isCurrent ? 'primary' : 'secondary'}
                    disabled={isLocked}
                    icon={isLocked ? Lock : Play}
                  >
                    {isDone ? 'Review' : isCurrent ? 'Start' : 'Locked'}
                  </Button>
                </Card>
              );
            })}
          </div>
        </div>

        <div className="lg:col-span-4 space-y-6">
          <Card radius="24" className="p-6 space-y-4">
            <div className="flex items-center gap-2">
              <FileCheck className="w-5 h-5 text-[#0A0A0A]" />
              <h3 className="text-base font-bold text-[#0A0A0A]">Module Assessment</h3>
            </div>
            <p className="text-xs text-[#45515E]">
              Test your understanding of the concepts covered in this module. Pass score is 70%.
            </p>

            {allLessonsCompleted ? (
              <Button
                variant={isAssessmentPassed ? "outline" : "primary"}
                size="lg"
                onClick={() => navigate(`/courses/${slug}/modules/${moduleId}/assessment`)}
                className="w-full justify-center"
              >
                {isAssessmentPassed ? 'Retake Assessment' : 'Take Assessment'}
              </Button>
            ) : (
              <div className="p-3 rounded-xl bg-[#F7F8FA] border border-[#E5E7EB] text-center text-xs text-[#8E8E93]">
                🔒 Complete all lessons to unlock assessment.
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
