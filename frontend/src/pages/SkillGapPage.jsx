import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { careerService } from '../services/careerService';
import api from '../services/api';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';
import { LoadingState } from '../components/common/LoadingState';
import { Target, Zap, TrendingUp, Award, BookOpen, ChevronDown, ChevronRight } from 'lucide-react';

const PROFICIENCY_LABELS = {
  1: { label: 'Beginner', color: '#8E8E93', bg: '#F2F3F5', border: '#E5E7EB' },
  2: { label: 'Basic', color: '#D97706', bg: '#FEF3C7', border: '#FCD34D' },
  3: { label: 'Intermediate', color: '#2563EB', bg: '#DBEAFE', border: '#93C5FD' },
  4: { label: 'Advanced', color: '#7C3AED', bg: '#EDE9FE', border: '#C4B5FD' },
  5: { label: 'Expert', color: '#059669', bg: '#D1FAE5', border: '#6EE7B7' },
};

const SkillNode = ({ skill, depth = 0, isLast = false }) => {
  const [expanded, setExpanded] = useState(depth < 2);
  const level = skill.proficiency !== undefined ? skill.proficiency : (skill.current_level || 0);
  const maxLevel = skill.required_level || 5;

  let progress = 0;
  if (skill.progress_percentage !== undefined && skill.progress_percentage !== null) {
    progress = skill.progress_percentage;
  } else if (level === 0) {
    progress = 0;
  } else if (level === 1) {
    progress = 20;
  } else if (level === 2) {
    progress = 25;
  } else if (level === 3) {
    progress = 50;
  } else if (level === 4) {
    progress = 75;
  } else if (level >= 5) {
    progress = 100;
  }

  const prof = PROFICIENCY_LABELS[Math.min(Math.max(level, 1), 5)] || PROFICIENCY_LABELS[1];
  const hasChildren = skill.children && skill.children.length > 0;

  const isCompleted = progress >= 100;
  const isLearning = progress > 0 && progress < 100;

  return (
    <div className="relative">
      {/* Connecting line */}
      {depth > 0 && (
        <div className="absolute -left-6 top-0 w-6 border-l-2 border-b-2 border-[#E5E7EB] h-6 rounded-bl-lg" />
      )}

      <div
        className={`group p-4 rounded-2xl border transition-all cursor-pointer hover:shadow-md ${
          isCompleted
            ? 'bg-emerald-50/60 border-emerald-200 hover:border-emerald-400'
            : isLearning
            ? 'bg-blue-50/40 border-blue-200 hover:border-blue-400'
            : 'bg-white border-[#E5E7EB] hover:border-[#0A0A0A]'
        }`}
        onClick={() => hasChildren && setExpanded(!expanded)}
      >
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-3 min-w-0">
            {hasChildren && (
              <div className="shrink-0">
                {expanded
                  ? <ChevronDown className="w-4 h-4 text-[#8E8E93]" />
                  : <ChevronRight className="w-4 h-4 text-[#8E8E93]" />}
              </div>
            )}
            {!hasChildren && (
              <div className={`w-3 h-3 rounded-full shrink-0 ${
                isCompleted ? 'bg-emerald-500' : isLearning ? 'bg-blue-500' : 'bg-[#E5E7EB]'
              }`} />
            )}
            <div className="min-w-0">
              <h4 className="text-sm font-bold text-[#0A0A0A] truncate">{skill.skill || skill.name}</h4>
              {skill.category && (
                <span className="text-[10px] text-[#8E8E93] font-semibold uppercase">{skill.category}</span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            {/* Proficiency Badge */}
            <span
              className="text-[10px] font-bold px-2 py-0.5 rounded-full border"
              style={{
                color: prof.color,
                backgroundColor: prof.bg,
                borderColor: prof.border,
              }}
            >
              {level === 0 ? 'Not Started' : isCompleted ? '✓ Completed' : isLearning ? '● Learning' : prof.label}
            </span>

            {/* Progress Ring */}
            <div className="relative w-9 h-9 shrink-0">
              <svg className="w-9 h-9 -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="15" fill="none" stroke="#E5E7EB" strokeWidth="3" />
                <circle
                  cx="18" cy="18" r="15" fill="none"
                  stroke={isCompleted ? '#059669' : isLearning ? '#2563EB' : '#D1D5DB'}
                  strokeWidth="3"
                  strokeDasharray={`${progress * 0.942} 100`}
                  strokeLinecap="round"
                  className="transition-all duration-500"
                />
              </svg>
              <span className="absolute inset-0 flex items-center justify-center text-[9px] font-bold text-[#0A0A0A]">
                {progress}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Children (tree branches) */}
      {hasChildren && expanded && (
        <div className="pl-8 mt-2 space-y-2 relative">
          {skill.children.map((child, idx) => (
            <SkillNode
              key={child.skill_id || child.name || idx}
              skill={child}
              depth={depth + 1}
              isLast={idx === skill.children.length - 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export const SkillGapPage = () => {
  const { user, roadmap } = useApp();
  const navigate = useNavigate();
  const [gapData, setGapData] = useState(null);
  const [userSkills, setUserSkills] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSkillData = async () => {
      setLoading(true);
      let careerId = roadmap?.career_id;
      if (!careerId && user?.targetGoal) {
        try {
          const analysisRes = await careerService.getCareerAnalysis(user.targetGoal);
          if (analysisRes?.data?.length > 0) {
            careerId = analysisRes.data[0].career_id;
          }
        } catch (e) {}
      }

      // Fetch skill gap data
      if (careerId) {
        try {
          const res = await careerService.getSkillGap(careerId);
          if (res && res.data) {
            setGapData(res.data);
          }
        } catch (err) {
          console.warn("Failed to fetch skill gap:", err);
        }
      }

      // Fetch actual user skills from MySQL
      try {
        const skillsRes = await api.get('/user-skills');
        if (Array.isArray(skillsRes.data)) {
          setUserSkills(skillsRes.data);
        }
      } catch (e) {}

      setLoading(false);
    };

    fetchSkillData();
  }, [roadmap, user?.targetGoal]);

  // Build skill tree structure
  const buildSkillTree = useCallback(() => {
    const rawSkills = gapData?.skills || [];
    const userSkillMap = {};
    const userSkillProgressMap = {};

    userSkills.forEach(us => {
      const name = (us.skill?.name || '').toLowerCase();
      if (name) {
        userSkillMap[name] = us.proficiency;
        if (us.progress_percentage !== undefined) {
          userSkillProgressMap[name] = us.progress_percentage;
        }
      }
    });

    // Group by category
    const categoryMap = {};
    rawSkills.forEach(s => {
      const cat = s.category || 'General';
      if (!categoryMap[cat]) categoryMap[cat] = [];

      const skillKey = (s.skill || '').toLowerCase();
      const realProf = userSkillMap[skillKey];
      const realProg = userSkillProgressMap[skillKey];

      categoryMap[cat].push({
        ...s,
        proficiency: realProf !== undefined ? realProf : (s.current_level || 0),
        progress_percentage: realProg,
        name: s.skill,
      });
    });

    // Build tree: Career Goal -> Categories -> Skills
    const careerName = roadmap?.career || user?.targetGoal || "Career Goal";
    const categoryNodes = Object.entries(categoryMap).map(([cat, skills]) => {
      const avgProf = skills.reduce((sum, s) => sum + (s.proficiency || 0), 0) / Math.max(skills.length, 1);
      return {
        skill: cat,
        name: cat,
        category: null,
        proficiency: Math.round(avgProf),
        required_level: 5,
        current_level: Math.round(avgProf),
        children: skills.map(s => ({
          ...s,
          children: null,
        })),
      };
    });

    return {
      skill: careerName,
      name: careerName,
      category: 'Career Goal',
      proficiency: Math.round(categoryNodes.reduce((s, c) => s + c.proficiency, 0) / Math.max(categoryNodes.length, 1)),
      required_level: 5,
      current_level: Math.round(categoryNodes.reduce((s, c) => s + c.current_level, 0) / Math.max(categoryNodes.length, 1)),
      children: categoryNodes,
    };
  }, [gapData, userSkills, roadmap, user]);

  const careerName = roadmap?.career || user?.targetGoal || "Career Goal";
  const skillTree = !loading && (gapData || userSkills.length > 0) ? buildSkillTree() : null;

  // Stats
  const allSkills = gapData?.skills || [];
  const readyCount = allSkills.filter(s => s.status === 'ready' || (s.current_level >= s.required_level)).length;
  const learningCount = allSkills.filter(s => s.current_level > 0 && s.current_level < s.required_level).length;
  const gapCount = allSkills.filter(s => s.current_level === 0 || !s.current_level).length;

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-5xl mx-auto pb-12">
      <div className="space-y-1">
        <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">SKILL INTELLIGENCE</span>
        <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">Interactive Skill Tree</h1>
        <p className="text-sm text-[#45515E]">
          Target: <strong className="text-[#0A0A0A]">{careerName}</strong> — Skills auto-update from lessons, quizzes, and projects.
        </p>
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: 'Total Skills', value: allSkills.length, icon: Target, color: '#0A0A0A' },
          { label: 'Completed', value: readyCount, icon: Award, color: '#059669' },
          { label: 'Learning', value: learningCount, icon: TrendingUp, color: '#2563EB' },
          { label: 'To Start', value: gapCount, icon: BookOpen, color: '#D97706' },
        ].map(stat => (
          <Card key={stat.label} radius="16" className="p-4 flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ backgroundColor: stat.color + '10' }}>
              <stat.icon className="w-4 h-4" style={{ color: stat.color }} />
            </div>
            <div>
              <span className="text-xl font-bold text-[#0A0A0A] block">{stat.value}</span>
              <span className="text-[10px] font-semibold text-[#8E8E93] uppercase">{stat.label}</span>
            </div>
          </Card>
        ))}
      </div>

      {loading ? (
        <LoadingState message="Analyzing skill intelligence..." />
      ) : skillTree ? (
        <Card radius="24" className="p-6 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-[#E5E7EB]">
            <Target className="w-4 h-4 text-[#0A0A0A]" />
            <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">Skill Tree — Click to expand/collapse branches</span>
          </div>
          <div className="space-y-3">
            <SkillNode skill={skillTree} depth={0} />
          </div>
        </Card>
      ) : (
        <Card radius="20" className="p-8 text-center space-y-4">
          <Target className="w-12 h-12 text-[#8E8E93] mx-auto" />
          <h3 className="text-lg font-bold text-[#0A0A0A]">Complete your profile to see your Skill Tree</h3>
          <p className="text-sm text-[#45515E]">
            Start learning lessons, take quizzes, and complete projects to see your skill visualization update.
          </p>
        </Card>
      )}

      {/* Legend */}
      <Card radius="16" className="p-4">
        <div className="flex flex-wrap items-center gap-4 text-xs font-semibold">
          <span className="text-[#8E8E93] uppercase tracking-wider">Legend:</span>
          {Object.entries(PROFICIENCY_LABELS).map(([level, info]) => (
            <span
              key={level}
              className="px-2 py-0.5 rounded-full border"
              style={{ color: info.color, backgroundColor: info.bg, borderColor: info.border }}
            >
              {info.label}
            </span>
          ))}
          <span className="px-2 py-0.5 rounded-full bg-blue-50 border border-blue-200 text-blue-600">● Learning</span>
          <span className="px-2 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-600">✓ Completed</span>
        </div>
      </Card>
    </div>
  );
};
