import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { courseService } from '../services/courseService';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { ProgressBar } from '../components/common/ProgressBar';
import { LoadingState } from '../components/common/LoadingState';
import { ArrowLeft, Play, Lock, Check } from 'lucide-react';

export const CourseDetailPage = () => {
  const { id: courseSlugOrId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useApp();

  const [course, setCourse] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadCourseData = async () => {
      setLoading(true);
      try {
        const [courseData, roadmapData] = await Promise.all([
          courseService.getCourseOverview(courseSlugOrId),
          courseService.getCourseRoadmap(courseSlugOrId),
        ]);
        setCourse(courseData);
        setRoadmap(roadmapData);
      } catch (err) {
        console.error('Failed loading course details:', err);
        showToast('Error loading course details.', 'error');
      } finally {
        setLoading(false);
      }
    };

    loadCourseData();
  }, [courseSlugOrId]);

  if (loading) return <LoadingState message="Loading course details..." />;
  if (!course) return (
    <Card radius="24" className="p-12 text-center space-y-4 max-w-md mx-auto my-12">
      <h2 className="text-xl font-bold text-[#0A0A0A]">Course Not Found</h2>
      <Button variant="primary" size="md" onClick={() => navigate('/courses')}>
        Back to Courses
      </Button>
    </Card>
  );

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-5xl mx-auto">
      <button
        onClick={() => navigate('/courses')}
        className="inline-flex items-center gap-2 text-xs font-bold text-[#8E8E93] hover:text-[#0A0A0A]"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Course Catalog</span>
      </button>

      {/* Hero Card */}
      <Card radius="24" className="p-8 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <Badge variant="dark">{course.difficulty || 'Intermediate'}</Badge>
            <h1 className="text-3xl font-bold text-[#0A0A0A]">{course.title}</h1>
          </div>
          <Button
            variant="primary"
            size="lg"
            icon={Play}
            onClick={() => {
              if (roadmap?.phases?.[0]?.modules?.[0]) {
                const firstMod = roadmap.phases[0].modules[0];
                navigate(`/courses/${course.slug}/modules/${firstMod.id}`);
              } else {
                navigate(`/courses/${course.slug}/modules/1`);
              }
            }}
          >
            Start Course
          </Button>
        </div>

        <p className="text-sm text-[#45515E] leading-relaxed">{course.description}</p>

        <div className="pt-2">
          <ProgressBar value={course.progress_percentage || 0} color="dark" showPercentage />
        </div>
      </Card>

      {/* Syllabus / Phased Modules */}
      <div className="space-y-6">
        <h2 className="text-xl font-bold text-[#0A0A0A]">Syllabus &amp; Modules</h2>

        <div className="space-y-4">
          {(roadmap?.phases || []).map((phase, pIdx) => (
            <div key={pIdx} className="space-y-4">
              <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider block">
                Phase 0{pIdx + 1}: {phase.phase_name}
              </span>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {(phase.modules || []).map((mod) => {
                  const isDone = mod.status === 'completed' || mod.assessment_passed;
                  const isUnlocked = mod.status === 'unlocked' || mod.status === 'in_progress' || isDone;

                  return (
                    <Card
                      key={mod.id}
                      onClick={() => isUnlocked && navigate(`/courses/${course.slug}/modules/${mod.id}`)}
                      className={`p-6 space-y-4 transition-all ${
                        !isUnlocked ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-[#0A0A0A]'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-mono font-bold text-[#8E8E93]">Module {mod.module_number}</span>
                        <Badge variant={isDone ? 'success' : isUnlocked ? 'dark' : 'slate'}>
                          {isDone ? 'Completed ✓' : isUnlocked ? 'Unlocked' : 'Locked 🔒'}
                        </Badge>
                      </div>

                      <div className="space-y-1">
                        <h3 className="text-base font-bold text-[#0A0A0A]">{mod.title}</h3>
                        <p className="text-xs text-[#45515E] line-clamp-2">{mod.description}</p>
                      </div>

                      {mod.skills && (
                        <div className="flex flex-wrap gap-1 pt-2 border-t border-[#E5E7EB]">
                          {mod.skills.map(sk => <Badge key={sk} variant="slate" size="xs">{sk}</Badge>)}
                        </div>
                      )}
                    </Card>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
