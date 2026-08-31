import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { courseService } from '../services/courseService';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { LoadingState } from '../components/common/LoadingState';
import { CodeIDE } from '../components/ide/CodeIDE';
import {
  ArrowLeft,
  ArrowRight,
  Check,
  PlayCircle,
  Copy,
  ExternalLink,
  Code2,
  BookOpen,
  Monitor
} from 'lucide-react';

export const LessonLearningPage = () => {
  const { slug, moduleId, lessonId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useApp();

  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copiedCode, setCopiedCode] = useState(false);
  const [completing, setCompleting] = useState(false);
  const [mobileActiveTab, setMobileActiveTab] = useState('video'); // 'video' or 'ide' for mobile view

  useEffect(() => {
    const fetchLesson = async () => {
      setLoading(true);
      try {
        const data = await courseService.getLessonDetail(slug, moduleId, lessonId);
        setLesson(data);
      } catch (err) {
        console.error('Failed to load lesson:', err);
        showToast(err.response?.data?.detail || 'Error loading lesson.', 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchLesson();
  }, [slug, moduleId, lessonId]);

  const handleCopyCode = (codeText) => {
    navigator.clipboard.writeText(codeText);
    setCopiedCode(true);
    showToast('Code copied to clipboard!', 'success');
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const handleMarkComplete = async () => {
    if (!lesson) return;
    setCompleting(true);
    try {
      const res = await courseService.markLessonCompleted(lesson.id);
      showToast('Lesson completed!', 'success');
      setLesson((prev) => ({ ...prev, is_completed: true }));

      if (res.assessment_unlocked || res.module_lessons_completed) {
        navigate(`/courses/${slug}/modules/${moduleId}/assessment`);
      } else if (lesson.next_lesson_id) {
        navigate(`/courses/${slug}/modules/${moduleId}/lessons/${lesson.next_lesson_id}`);
      } else {
        navigate(`/courses/${slug}/modules/${moduleId}`);
      }
    } catch (err) {
      showToast('Error marking lesson complete.', 'error');
    } finally {
      setCompleting(false);
    }
  };

  if (loading) return <LoadingState message="Loading interactive lesson..." />;
  if (!lesson) return (
    <Card radius="24" className="p-12 text-center space-y-4 max-w-md mx-auto my-12">
      <h2 className="text-xl font-bold text-[#0A0A0A]">Lesson Not Found</h2>
      <Button variant="primary" size="md" onClick={() => navigate(`/courses/${slug}/modules/${moduleId}`)}>
        Back to Module
      </Button>
    </Card>
  );

  const getVideoEmbedUrl = (url) => {
    if (!url) return null;
    if (url.includes('youtube.com/watch?v=')) {
      const videoId = url.split('v=')[1]?.split('&')[0];
      return `https://www.youtube.com/embed/${videoId}`;
    }
    if (url.includes('youtu.be/')) {
      const videoId = url.split('youtu.be/')[1]?.split('?')[0];
      return `https://www.youtube.com/embed/${videoId}`;
    }
    return url;
  };

  const embedUrl = getVideoEmbedUrl(lesson.video_url);

  return (
    <div className="space-y-6 animate-fadeIn max-w-[1600px] mx-auto font-sans pb-12">

      {/* TOP LESSON BREADCRUMB HEADER */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#E5E7EB] pb-4">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate(`/courses/${slug}/modules/${moduleId}`)}
            className="inline-flex items-center gap-1.5 text-xs font-bold text-[#8E8E93] hover:text-[#0A0A0A] transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>{lesson.module_title || 'Back to Module'}</span>
          </button>
          <span className="text-[#8E8E93]">•</span>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-[#0A0A0A]">Lesson {lesson.lesson_number}:</span>
            <span className="text-xs font-semibold text-[#45515E]">{lesson.title}</span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Badge variant={lesson.is_completed ? 'success' : 'dark'}>
            {lesson.is_completed ? 'Completed ✓' : 'In Progress'}
          </Badge>

          {/* Mobile view switcher for coding lessons */}
          {lesson.has_coding && (
            <div className="lg:hidden flex items-center bg-[#F2F2F7] rounded-xl p-1 text-xs font-bold">
              <button
                onClick={() => setMobileActiveTab('video')}
                className={`px-3 py-1 rounded-lg flex items-center gap-1 transition-colors ${
                  mobileActiveTab === 'video' ? 'bg-white text-[#0A0A0A] shadow-sm' : 'text-[#8E8E93]'
                }`}
              >
                <Monitor className="w-3.5 h-3.5" />
                <span>Video</span>
              </button>
              <button
                onClick={() => setMobileActiveTab('ide')}
                className={`px-3 py-1 rounded-lg flex items-center gap-1 transition-colors ${
                  mobileActiveTab === 'ide' ? 'bg-[#0A0A0A] text-white shadow-sm' : 'text-[#8E8E93]'
                }`}
              >
                <Code2 className="w-3.5 h-3.5 text-blue-400" />
                <span>IDE Code</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* CONDITIONAL LAYOUT: CODING LESSON (SPLIT SCREEN) VS THEORY LESSON */}
      {lesson.has_coding ? (
        /* CODING LESSON SPLIT-SCREEN LAYOUT (~45% Video / ~55% Monaco Code IDE) */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

          {/* LEFT PANEL: Video Player & Lesson Explanation (~45% Desktop width) */}
          <div className={`lg:col-span-5 space-y-6 ${mobileActiveTab === 'ide' ? 'hidden lg:block' : 'block'}`}>
            
            {/* Video Container */}
            <div className="rounded-2xl overflow-hidden bg-[#0A0A0A] aspect-video relative border border-[#E5E7EB] shadow-md">
              {embedUrl ? (
                <iframe
                  src={embedUrl}
                  title={lesson.title}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="w-full h-full border-0"
                />
              ) : (
                <div className="w-full h-full flex flex-col items-center justify-center text-white space-y-2">
                  <PlayCircle className="w-12 h-12 text-white opacity-80" />
                  <span className="text-xs font-semibold">Interactive Video Lesson</span>
                </div>
              )}
            </div>

            {/* Lesson Explanation */}
            <Card radius="16" className="p-6 space-y-4">
              <h2 className="text-base font-bold text-[#0A0A0A]">Lesson Explanation</h2>
              <div className="text-xs text-[#222222] leading-relaxed whitespace-pre-line">
                {lesson.content}
              </div>

              {lesson.key_concepts && lesson.key_concepts.length > 0 && (
                <div className="space-y-2 pt-3 border-t border-[#E5E7EB]">
                  <span className="text-xs font-semibold text-[#8E8E93] block">Key Concepts:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {lesson.key_concepts.map((kc) => (
                      <Badge key={kc} variant="surface" size="xs">{kc}</Badge>
                    ))}
                  </div>
                </div>
              )}
            </Card>

            {/* Resources list */}
            {lesson.resources && lesson.resources.length > 0 && (
              <Card radius="16" className="p-4 space-y-2">
                <h3 className="text-xs font-bold text-[#0A0A0A]">Resources</h3>
                <div className="space-y-1.5">
                  {lesson.resources.map((res, idx) => (
                    <a
                      key={idx}
                      href={res.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-[#0A0A0A] hover:underline flex items-center justify-between font-medium"
                    >
                      <span className="truncate">{res.title}</span>
                      <ExternalLink className="w-3.5 h-3.5 shrink-0 text-[#8E8E93]" />
                    </a>
                  ))}
                </div>
              </Card>
            )}
          </div>

          {/* RIGHT PANEL: Online Coding IDE / Compiler (~55% Desktop width) */}
          <div className={`lg:col-span-7 h-full ${mobileActiveTab === 'video' ? 'hidden lg:block' : 'block'}`}>
            <CodeIDE
              lessonId={lesson.id}
              starterCode={lesson.starter_code || lesson.code_snippet}
              defaultLanguage={lesson.default_language || lesson.code_language || 'python'}
              defaultVersion={lesson.default_version}
              codingInstructions={lesson.coding_instructions}
            />
          </div>
        </div>
      ) : (
        /* STANDARD THEORY LESSON LAYOUT (100% Preserved) */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* LEFT COLUMN: Course Navigation */}
          <div className="lg:col-span-3 space-y-4">
            <Card radius="16" className="p-4 space-y-3">
              <button
                onClick={() => navigate(`/courses/${slug}/modules/${moduleId}`)}
                className="inline-flex items-center gap-2 text-xs font-bold text-[#8E8E93] hover:text-[#0A0A0A]"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Back to Module</span>
              </button>
              <div className="pt-2 border-t border-[#E5E7EB]">
                <span className="text-[10px] font-bold text-[#8E8E93] uppercase tracking-wider block">Module</span>
                <h3 className="text-sm font-bold text-[#0A0A0A] truncate">{lesson.module_title}</h3>
              </div>
            </Card>
          </div>

          {/* CENTER COLUMN: Video Player & Content */}
          <div className="lg:col-span-6 space-y-6">
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-xs font-semibold text-[#8E8E93]">
                <span>Lesson {lesson.lesson_number}</span>
                <span>•</span>
                <span>{lesson.video_duration || '15 mins'}</span>
              </div>
              <h1 className="text-2xl font-bold text-[#0A0A0A]">{lesson.title}</h1>
              <p className="text-sm text-[#45515E]">{lesson.description}</p>
            </div>

            <div className="rounded-2xl overflow-hidden bg-[#0A0A0A] aspect-video relative border border-[#E5E7EB]">
              {embedUrl ? (
                <iframe
                  src={embedUrl}
                  title={lesson.title}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="w-full h-full border-0"
                />
              ) : (
                <div className="w-full h-full flex flex-col items-center justify-center text-white space-y-2">
                  <PlayCircle className="w-12 h-12 text-white opacity-80" />
                  <span className="text-xs font-semibold">Interactive Video Lesson</span>
                </div>
              )}
            </div>

            <Card radius="16" className="p-6 space-y-4">
              <h2 className="text-lg font-bold text-[#0A0A0A]">Lesson Explanation</h2>
              <div className="text-sm text-[#222222] leading-relaxed whitespace-pre-line">
                {lesson.content}
              </div>
            </Card>

            {lesson.code_snippet && (
              <div className="rounded-2xl overflow-hidden bg-[#0A0A0A] text-white border border-[#0A0A0A]">
                <div className="px-4 py-2 bg-[#222222] flex items-center justify-between">
                  <span className="text-xs font-mono font-semibold">{lesson.code_language || 'Code Example'}</span>
                  <button
                    onClick={() => handleCopyCode(lesson.code_snippet)}
                    className="text-xs text-white/80 hover:text-white font-medium flex items-center gap-1"
                  >
                    {copiedCode ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                    <span>{copiedCode ? 'Copied' : 'Copy'}</span>
                  </button>
                </div>
                <pre className="p-4 text-xs font-mono text-white/90 overflow-x-auto">
                  {lesson.code_snippet}
                </pre>
              </div>
            )}
          </div>

          {/* RIGHT COLUMN: Progress & Resources */}
          <div className="lg:col-span-3 space-y-4">
            <Card radius="16" className="p-5 space-y-4">
              <h3 className="text-sm font-bold text-[#0A0A0A]">Lesson Progress</h3>
              <Badge variant={lesson.is_completed ? 'success' : 'dark'}>
                {lesson.is_completed ? 'Completed ✓' : 'In Progress'}
              </Badge>

              {lesson.key_concepts && lesson.key_concepts.length > 0 && (
                <div className="space-y-2 pt-3 border-t border-[#E5E7EB]">
                  <span className="text-xs font-semibold text-[#8E8E93] block">Key Concepts:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {lesson.key_concepts.map((kc) => (
                      <Badge key={kc} variant="surface" size="xs">{kc}</Badge>
                    ))}
                  </div>
                </div>
              )}
            </Card>

            {lesson.resources && lesson.resources.length > 0 && (
              <Card radius="16" className="p-5 space-y-3">
                <h3 className="text-sm font-bold text-[#0A0A0A]">Resources</h3>
                <div className="space-y-2">
                  {lesson.resources.map((res, idx) => (
                    <a
                      key={idx}
                      href={res.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-[#0A0A0A] hover:underline flex items-center justify-between font-medium"
                    >
                      <span className="truncate">{res.title}</span>
                      <ExternalLink className="w-3.5 h-3.5 shrink-0" />
                    </a>
                  ))}
                </div>
              </Card>
            )}
          </div>
        </div>
      )}

      {/* BOTTOM ACTION BAR */}
      <div className="p-4 rounded-full bg-white border border-[#E5E7EB] shadow-floating flex items-center justify-between max-w-4xl mx-auto">
        {lesson.prev_lesson ? (
          <Button
            variant="outline"
            size="sm"
            icon={ArrowLeft}
            onClick={() => navigate(`/courses/${slug}/modules/${moduleId}/lessons/${lesson.prev_lesson.id}`)}
          >
            Previous
          </Button>
        ) : (
          <div />
        )}

        <Button
          variant="primary"
          size="md"
          icon={Check}
          loading={completing}
          onClick={handleMarkComplete}
        >
          {lesson.is_completed ? 'Completed ✓' : 'Mark Complete'}
        </Button>

        {lesson.next_lesson ? (
          <Button
            variant="outline"
            size="sm"
            icon={ArrowRight}
            iconPosition="right"
            onClick={() => navigate(`/courses/${slug}/modules/${moduleId}/lessons/${lesson.next_lesson.id}`)}
          >
            Next Lesson
          </Button>
        ) : (
          <div />
        )}
      </div>
    </div>
  );
};
