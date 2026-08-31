import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { learningPathService } from '../services/learningPathService';
import { progressService } from '../services/progressService';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { LoadingState } from '../components/common/LoadingState';
import {
  Check,
  Lock,
  Sparkles,
  User,
  Compass,
  Trophy,
  ChevronRight,
  Clock,
  BookOpen,
  ArrowRight,
  Zap
} from 'lucide-react';

export const LearningPathPage = () => {
  const { roadmap, setRoadmap, user, generateNewPath, showToast } = useApp();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const fetchPath = async () => {
    setLoading(true);
    try {
      const res = await learningPathService.getLearningPath();
      if (res && res.data) {
        setRoadmap(res.data);
      }
    } catch (e) {
      console.warn("Failed to fetch path:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!roadmap || !roadmap.items) {
      fetchPath();
    }
  }, []);

  const handleRegenerate = async () => {
    setLoading(true);
    try {
      await generateNewPath(user?.targetGoal || roadmap?.career || "");
      await fetchPath();
      showToast("Personalized roadmap recalculated!", "success");
    } catch (e) {
      showToast("Error updating roadmap.", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleTopicClick = (topic) => {
    if (!topic) return;
    const courseSlug = topic.course_slug || roadmap?.course_slug || "frontend-developer";
    const moduleId = topic.module_id || 1;
    const lessonId = topic.lesson_id || topic.id || 1;
    navigate(`/courses/${courseSlug}/modules/${moduleId}/lessons/${lessonId}`);
  };

  const careerTitle = roadmap?.career || user?.targetGoal || "Career Goal";
  const weeklyHours = roadmap?.weekly_hours || user?.learning_hours_per_week || 10;
  const readinessScore = roadmap?.readiness_score !== undefined ? roadmap.readiness_score : 0;
  const phases = roadmap?.phases || [];
  const items = roadmap?.items || [];

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-5xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-[#E5E7EB]">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">MY ROADMAP</span>
            <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-[#1456F0] text-white flex items-center gap-1">
              <Zap className="w-3 h-3 text-yellow-300" /> {weeklyHours} Hours/Week Available
            </span>
          </div>
          <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">
            Personalized {careerTitle} Roadmap
          </h1>
          <p className="text-sm text-[#45515E]">
            AI-sequenced path tailored strictly to your skill gap, profile, and learning progress.
          </p>
        </div>

        <Button
          variant="outline"
          size="sm"
          icon={Sparkles}
          onClick={handleRegenerate}
          loading={loading}
          className="border-[#1456F0] text-[#1456F0] hover:bg-blue-50"
        >
          Recalculate Path
        </Button>
      </div>

      {/* ROADMAP VISUAL */}
      <Card radius="24" className="p-6 bg-gradient-to-br from-[#146EF5] via-[#0B5ED7] to-[#146EF5] text-white space-y-6 shadow-xl relative overflow-hidden">
        {/* Background glow */}
        <div className="absolute -top-24 -right-24 w-72 h-72 rounded-full bg-white/10 blur-3xl pointer-events-none" />

        <div className="flex items-center justify-between border-b border-white/20 pb-4">
          <div className="flex items-center gap-2">
            <Compass className="w-5 h-5 text-white" />
            <span className="text-xs font-bold uppercase tracking-wider text-blue-100">Career Growth Journey</span>
          </div>
          <div className="flex items-center gap-3 text-xs font-semibold">
            <span className="text-blue-100">Overall Progress:</span>
            <span className="px-2.5 py-1 rounded-full bg-white/20 text-white font-bold border border-white/30">
              {readinessScore}% Completed
            </span>
          </div>
        </div>

        {/* Visual Progress Line */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 relative z-10">
          {/* Node 1 */}
          <div className="p-4 rounded-2xl bg-white/15 border border-white/20 flex items-center gap-3 backdrop-blur-md">
            <div className="w-10 h-10 rounded-full bg-white/20 border border-white/40 text-white flex items-center justify-center font-bold">
              <User className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] text-blue-100 uppercase font-semibold block">Starting Point</span>
              <h4 className="text-sm font-bold text-white">{user?.name || "Learner"}</h4>
              <span className="text-[11px] text-blue-100 font-medium">Profile & Gaps Analyzed</span>
            </div>
          </div>

          {/* Node 2 */}
          <div className="p-4 rounded-2xl bg-white/15 border border-white/20 flex items-center gap-3 backdrop-blur-md">
            <div className="w-10 h-10 rounded-full bg-white/20 border border-white/40 text-white flex items-center justify-center font-bold">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] text-blue-100 uppercase font-semibold block">Active Execution</span>
              <h4 className="text-sm font-bold text-white">{items.length || 12} Modules Sequenced</h4>
              <span className="text-[11px] text-blue-100 font-medium">{weeklyHours} hrs/week pacing</span>
            </div>
          </div>

          {/* Node 3 */}
          <div className="p-4 rounded-2xl bg-white/15 border border-white/20 flex items-center gap-3 backdrop-blur-md">
            <div className="w-10 h-10 rounded-full bg-white/20 border border-white/40 text-white flex items-center justify-center font-bold">
              <Trophy className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] text-blue-100 uppercase font-semibold block">Target Career</span>
              <h4 className="text-sm font-bold text-white">{careerTitle}</h4>
              <span className="text-[11px] text-blue-100 font-medium">Job-Ready Competency</span>
            </div>
          </div>
        </div>
      </Card>

      {/* ROADMAP CONTENT */}
      {loading ? (
        <LoadingState message="Generating your personalized AI roadmap..." />
      ) : phases.length === 0 && items.length === 0 ? (
        /* Empty State */
        <Card radius="24" className="p-8 text-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-[#F2F3F5] text-[#0A0A0A] mx-auto flex items-center justify-center">
            <Compass className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold text-[#0A0A0A]">No Personalized Roadmap Found</h3>
          <p className="text-sm text-[#45515E] max-w-md mx-auto">
            Click below to let Veyra evaluate your profile data, goal, and available hours to generate your custom roadmap.
          </p>
          <Button variant="primary" icon={Sparkles} onClick={handleRegenerate}>
            Generate My Roadmap
          </Button>
        </Card>
      ) : (
        <div className="space-y-10">
          {/* PHASES RENDER */}
          {(phases.length > 0 ? phases : [{ phase_name: "Phased Learning Path", modules: items }]).map((phaseObj, pIdx) => (
            <div key={phaseObj.phase_name || pIdx} className="space-y-4">
              <div className="flex items-center gap-3">
                <span className="text-xs font-bold px-3 py-1 rounded-full bg-[#0A0A0A] text-white">
                  PHASE {pIdx + 1}
                </span>
                <h2 className="text-xl font-bold text-[#0A0A0A]">{phaseObj.phase_name}</h2>
              </div>

              <div className="relative pl-6 sm:pl-8 space-y-6 border-l-2 border-[#E5E7EB]">
                {(phaseObj.modules || []).map((modItem, mIdx) => {
                  const isCompleted = modItem.status === 'completed';
                  const isCurrent = modItem.status === 'current';
                  const isLocked = modItem.status === 'locked' || (!isCompleted && !isCurrent);

                  // Extract topic details
                  const topicDetails = modItem.topic_details || modItem.topics || [];

                  return (
                    <div key={modItem.module_id || modItem.id || mIdx} className="relative group">
                      {/* Node Bullet Circle */}
                      <div className={`absolute -left-[33px] sm:-left-[41px] top-4 w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all shadow-sm ${
                        isCompleted
                          ? 'bg-[#0A0A0A] text-white'
                          : isCurrent
                          ? 'bg-[#0A0A0A] text-white ring-4 ring-[#E5E7EB]'
                          : 'bg-white text-[#8E8E93] border-2 border-[#E5E7EB]'
                      }`}>
                        {isCompleted ? (
                          <Check className="w-3.5 h-3.5 text-white" />
                        ) : isLocked ? (
                          <Lock className="w-3 h-3 text-[#8E8E93]" />
                        ) : (
                          <span className="w-2 h-2 rounded-full bg-white animate-ping" />
                        )}
                      </div>

                      {/* Module Card */}
                      <Card radius="20" className={`p-6 space-y-4 border transition-all ${
                        isCurrent ? 'border-[#0A0A0A] shadow-md bg-white' : 'border-[#E5E7EB] bg-[#FAFAFA]'
                      }`}>
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                          <div className="flex items-center gap-3">
                            <span className="text-xs font-mono font-bold text-[#8E8E93]">
                              MODULE {modItem.module_number || mIdx + 1}
                            </span>
                            <h3 className="text-lg font-bold text-[#0A0A0A]">{modItem.title}</h3>
                          </div>
                          <Badge variant={isCompleted ? 'dark' : isCurrent ? 'blue' : 'slate'}>
                            {isCompleted ? 'Completed ✓' : isCurrent ? 'In Progress ●' : 'Locked 🔒'}
                          </Badge>
                        </div>

                        {modItem.description && (
                          <p className="text-xs text-[#45515E] leading-relaxed">{modItem.description}</p>
                        )}

                        {/* Interactive Topics List (Clickable to Lesson) */}
                        {topicDetails && topicDetails.length > 0 && (
                          <div className="space-y-2 pt-3 border-t border-[#E5E7EB]">
                            <span className="text-[10px] font-bold text-[#8E8E93] uppercase tracking-wider block">
                              Click any topic to start lesson:
                            </span>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                              {topicDetails.map((topic, tIdx) => {
                                const isTopicObj = typeof topic === 'object';
                                const topicTitle = isTopicObj ? topic.title : topic;
                                const topicDone = isTopicObj ? topic.is_completed : isCompleted;
                                const topicStatus = isTopicObj ? topic.status : (isCompleted ? 'completed' : 'locked');

                                return (
                                  <div
                                    key={isTopicObj ? topic.id : tIdx}
                                    onClick={() => handleTopicClick(isTopicObj ? topic : {
                                      course_slug: roadmap?.course_slug || "frontend-developer",
                                      module_id: modItem.module_id || modItem.id || 1,
                                      lesson_id: tIdx + 1,
                                      title: topicTitle
                                    })}
                                    className={`p-3 rounded-xl border flex items-center justify-between text-xs font-semibold cursor-pointer transition-all ${
                                      topicDone
                                        ? 'bg-emerald-50 border-emerald-200 text-[#0A0A0A] hover:border-emerald-400'
                                        : topicStatus === 'current'
                                        ? 'bg-white border-[#0A0A0A] text-[#0A0A0A] shadow-sm hover:bg-[#F7F8FA]'
                                        : 'bg-[#F7F8FA] border-[#E5E7EB] text-[#45515E] hover:border-[#0A0A0A] hover:bg-white'
                                    }`}
                                  >
                                    <div className="flex items-center gap-2 truncate">
                                      {topicDone ? (
                                        <Check className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                                      ) : (
                                        <BookOpen className="w-3.5 h-3.5 text-[#8E8E93] shrink-0" />
                                      )}
                                      <span className="truncate">{topicTitle}</span>
                                    </div>
                                    <ChevronRight className="w-3.5 h-3.5 text-[#8E8E93] shrink-0" />
                                  </div>
                                );
                              })}
                            </div>
                          </div>
                        )}
                      </Card>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
