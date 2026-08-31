import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { courseService } from '../services/courseService';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { ProgressBar } from '../components/common/ProgressBar';
import { LoadingState } from '../components/common/LoadingState';
import { ArrowLeft, ChevronRight } from 'lucide-react';

export const SkillDetailPage = () => {
  const { skillIdentifier } = useParams();
  const navigate = useNavigate();
  const { showToast } = useApp();

  const [skillData, setSkillData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSkill = async () => {
      setLoading(true);
      try {
        const data = await courseService.getSkillDetail(skillIdentifier);
        setSkillData(data);
      } catch (err) {
        console.error('Failed loading skill details:', err);
        showToast('Error loading skill.', 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchSkill();
  }, [skillIdentifier]);

  if (loading) return <LoadingState message="Loading skill intelligence..." />;
  if (!skillData) return (
    <Card radius="24" className="p-12 text-center space-y-4 max-w-md mx-auto my-12">
      <h2 className="text-xl font-bold text-[#0A0A0A]">Skill Not Found</h2>
      <Button variant="primary" size="md" onClick={() => navigate('/courses')}>Back to Courses</Button>
    </Card>
  );

  const userLevel = skillData.user_proficiency || 0;
  const reqLevel = skillData.required_level || 4;
  const proficiencyPct = Math.min(100, Math.round((userLevel / 5) * 100));

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-4xl mx-auto">
      <button
        onClick={() => navigate(-1)}
        className="inline-flex items-center gap-2 text-xs font-bold text-[#8E8E93] hover:text-[#0A0A0A]"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back</span>
      </button>

      {/* Skill Header */}
      <Card radius="24" className="p-8 space-y-4">
        <Badge variant="dark">{skillData.category || 'Core Skill'}</Badge>
        <h1 className="text-3xl font-bold text-[#0A0A0A]">{skillData.name}</h1>
        <p className="text-sm text-[#45515E] leading-relaxed">{skillData.description}</p>

        <div className="pt-4 border-t border-[#E5E7EB] space-y-2">
          <div className="flex justify-between text-xs font-semibold text-[#45515E]">
            <span>Proficiency: <strong className="text-[#0A0A0A]">{skillData.proficiency_label || 'Beginner'} (Level {userLevel}/5)</strong></span>
            <span className="font-mono text-[#8E8E93]">Target: Level {reqLevel}/5</span>
          </div>
          <ProgressBar value={proficiencyPct} color="dark" height="h-2.5" />
        </div>
      </Card>

      {/* Teaching Modules */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-[#0A0A0A]">Modules Teaching {skillData.name}</h2>

        {(!skillData.teaching_modules || skillData.teaching_modules.length === 0) ? (
          <Card radius="16" className="p-8 text-center text-xs text-[#8E8E93]">
            No modules currently indexed for this skill.
          </Card>
        ) : (
          <div className="space-y-3">
            {skillData.teaching_modules.map((m, idx) => (
              <Card
                key={idx}
                radius="16"
                onClick={() => navigate(`/courses/${m.course_slug}/modules/${m.module_id}`)}
                className="p-5 flex items-center justify-between gap-4 cursor-pointer hover:border-[#0A0A0A] transition-all"
              >
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-[#8E8E93] uppercase font-mono block">
                    {m.course_title} • Module {m.module_number}
                  </span>
                  <h4 className="text-sm font-bold text-[#0A0A0A]">{m.module_title}</h4>
                </div>
                <Button size="sm" variant="outline" icon={ChevronRight} iconPosition="right">
                  Open
                </Button>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
