import React, { useEffect, useState } from 'react';
import { useApp } from '../context/AppContext';
import { careerService } from '../services/careerService';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { ProgressBar } from '../components/common/ProgressBar';
import { Modal } from '../components/common/Modal';
import {
  Target,
  CheckCircle2,
  TrendingUp,
  BarChart2,
  Sparkles,
  ArrowRight,
  GitCompare
} from 'lucide-react';
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Tooltip
} from 'recharts';

export const CareerAnalysisPage = () => {
  const { user, roadmap } = useApp();
  const [careerData, setCareerData] = useState(null);
  const [selectedAlternative, setSelectedAlternative] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const goal = user?.targetGoal || roadmap?.career || '';
        const res = await careerService.getCareerAnalysis(goal);

        // Handle both mock shape { primaryTarget, alternatives } and
        // real backend shape { success, data: [ career matches ] }
        if (res?.primaryTarget) {
          // Mock data path
          setCareerData(res);
          setLoading(false);
          return;
        }

        const matches = res?.data || (Array.isArray(res) ? res : []);
        if (matches.length === 0) {
          setLoading(false);
          return;
        }

        const topMatch = matches[0];
        const careerId = topMatch.career_id || roadmap?.career_id;

        // Fetch skill gap for the top career
        let skillGapData = null;
        if (careerId) {
          try {
            const sgRes = await careerService.getSkillGap(careerId);
            skillGapData = sgRes?.data || sgRes;
          } catch (e) {
            console.warn('Skill gap fetch failed:', e);
          }
        }

        // Build skillBreakdown from skill gap (scale 1-5 levels to 0-100%)
        const skillBreakdown = (skillGapData?.skills || []).map(s => ({
          skill: s.skill,
          current: Math.round((s.current_level / 5) * 100),
          required: Math.round((s.required_level / 5) * 100),
          gap: s.gap,
          status: s.status === 'ready' ? 'Ready'
               : s.status === 'small_gap' ? 'Needs Improvement'
               : s.status === 'medium_gap' ? 'Needs Improvement'
               : 'Major Gap',
        }));

        // Ready skills become "strengths"
        const readySkills = (skillGapData?.skills || [])
          .filter(s => s.status === 'ready')
          .map(s => `Proficient in ${s.skill}`);
        const strengths = readySkills.length > 0
          ? readySkills
          : ['Relevant experience for this career', 'Strong foundational background'];

        const primaryTarget = {
          title: topMatch.career || topMatch.name || 'Target Career',
          matchPercentage: topMatch.match_score ?? topMatch.goal_relevance ?? 0,
          readinessScore: skillGapData?.readiness_score ?? topMatch.skill_match ?? 0,
          averageSalary: 'Market Rate',
          demandLevel: 'High',
          summary: topMatch.description || `Build your career as a ${topMatch.career}.`,
          strengths,
          skillBreakdown,
        };

        const alternatives = matches.slice(1).map((m, idx) => ({
          id: m.career_id ?? `alt-${idx}`,
          title: m.career || m.name,
          matchPercentage: m.match_score ?? 0,
          readinessScore: m.skill_match ?? 0,
          demandLevel: 'High',
          strengths: (m.matching_skills || []).slice(0, 4),
          mainGaps: (m.skill_gaps || []).slice(0, 3),
          description: m.description || `Alternative career path based on your skill profile.`,
        }));

        setCareerData({ primaryTarget, alternatives });
      } catch (err) {
        console.warn('Career analysis failed:', err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [user?.targetGoal, roadmap?.career_id]);

  if (loading) return (
    <div className="flex items-center justify-center min-h-64 text-[#8E8E93] text-sm">
      <span className="animate-pulse">Analyzing your career target...</span>
    </div>
  );
  if (!careerData) return (
    <div className="flex items-center justify-center min-h-64 text-[#8E8E93] text-sm">
      <span>No career data found. Complete onboarding to get your career analysis.</span>
    </div>
  );

  const { primaryTarget, alternatives } = careerData;

  const radarChartData = (primaryTarget.skillBreakdown || []).slice(0, 6).map(s => ({
    skill: s.skill,
    current: s.current,
    required: s.required
  }));

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-[#E5E7EB] pb-6">
        <Badge variant="indigo" size="sm" className="mb-2">AI Career Diagnostics</Badge>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-[#0A0A0A]">
          Career Goal Analysis: <span className="text-[#0A0A0A]">{primaryTarget.title}</span>
        </h1>
        <p className="text-xs sm:text-sm text-[#8E8E93] mt-1">
          Detailed match calculation comparing your current skill vector against industry role requirements.
        </p>
      </div>

      {/* Target Goal Summary Banner */}
      <div className="bg-[#0A0A0A] text-white rounded-3xl p-8 space-y-6 shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-[#0A0A0A]/15 rounded-full blur-3xl pointer-events-none" />
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center relative z-10">
          <div className="md:col-span-8 space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-2xl bg-white/10 text-[#FFFFFF]">
                <Target className="w-7 h-7" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">{primaryTarget.title}</h2>
                <p className="text-xs text-slate-200 mt-0.5">{primaryTarget.summary}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2">
              <div className="p-3 rounded-xl bg-white/10 border border-white/10 text-xs">
                <span className="text-slate-300 text-[10px] block">Average Salary</span>
                <span className="font-bold text-[#FFFFFF]">{primaryTarget.averageSalary}</span>
              </div>
              <div className="p-3 rounded-xl bg-white/10 border border-white/10 text-xs">
                <span className="text-slate-300 text-[10px] block">Market Demand</span>
                <span className="font-bold text-emerald-300">{primaryTarget.demandLevel}</span>
              </div>
              <div className="p-3 rounded-xl bg-white/10 border border-white/10 text-xs">
                <span className="text-slate-300 text-[10px] block">Overall Readiness</span>
                <span className="font-bold text-[#0A0A0A]">{primaryTarget.readinessScore}%</span>
              </div>
            </div>
          </div>

          <div className="md:col-span-4 text-center p-6 rounded-2xl bg-white/10 border border-white/20 space-y-2 backdrop-blur-sm">
            <span className="text-xs text-slate-200 font-medium block">Goal Match Accuracy</span>
            <div className="text-4xl font-extrabold text-[#FFFFFF] font-mono">
              {primaryTarget.matchPercentage}%
            </div>
            <span className="px-3 py-1 rounded-full bg-emerald-400/20 text-emerald-300 text-xs font-semibold inline-block">
              High Potential Fit
            </span>
          </div>
        </div>
      </div>

      {/* WHY THIS GOAL FITS YOU */}
      <Card className="space-y-4">
        <h3 className="text-base font-bold text-[#0A0A0A] flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-[#0A0A0A]" />
          <span>Why This Goal Fits You</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {primaryTarget.strengths.map((str, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-[#F7F8FA] border border-[#E5E7EB] flex items-start gap-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
              <span className="text-xs font-semibold text-[#0A0A0A]">{str}</span>
            </div>
          ))}
        </div>
      </Card>

      {/* SKILL READINESS CHARTS */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Radar Chart */}
        <Card className="lg:col-span-6 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-[#0A0A0A] flex items-center gap-2">
              <BarChart2 className="w-5 h-5 text-[#0A0A0A]" />
              <span>Skill Vector Radar Analysis</span>
            </h3>
            <span className="text-[10px] text-[#8E8E93] font-medium">Current vs Target Baseline</span>
          </div>

          <div className="h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarChartData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="skill" stroke="#475569" tick={{ fontSize: 11, fill: '#0A0A0A', fontWeight: 600 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#cbd5e1" />
                <Radar name="Current Level" dataKey="current" stroke="#0A0A0A" fill="#0A0A0A" fillOpacity={0.4} />
                <Radar name="Required Level" dataKey="required" stroke="#0A0A0A" fill="#0A0A0A" fillOpacity={0.15} />
                <Tooltip contentStyle={{ backgroundColor: '#0A0A0A', color: '#fff', borderColor: '#0A0A0A', borderRadius: '12px', fontSize: '12px' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Skill Progress Bar Breakdown */}
        <Card className="lg:col-span-6 space-y-4">
          <h3 className="text-base font-bold text-[#0A0A0A] flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-[#0A0A0A]" />
            <span>Detailed Skill Readiness Matrix</span>
          </h3>

          <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
            {primaryTarget.skillBreakdown.map((item) => (
              <div key={item.skill} className="p-3 rounded-xl bg-[#F7F8FA] border border-[#E5E7EB] space-y-1.5">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-bold text-[#0A0A0A]">{item.skill}</span>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-[#8E8E93] font-semibold">{item.current}% / {item.required}%</span>
                    <Badge variant={item.status === 'Ready' ? 'emerald' : item.status === 'Needs Improvement' ? 'amber' : 'rose'} size="xs">
                      {item.status}
                    </Badge>
                  </div>
                </div>
                <ProgressBar value={item.current} max={item.required} color={item.current >= item.required ? 'emerald' : item.current >= 40 ? 'indigo' : 'rose'} />
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* CAREER ALTERNATIVES */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-[#0A0A0A]">Alternative Career Matches</h3>
            <p className="text-xs text-[#8E8E93]">Other roles matching your existing Python & SQL skill profile</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {alternatives.map((alt) => (
            <Card key={alt.id} hover className="flex flex-col justify-between space-y-4 bg-white">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-[#0A0A0A] font-bold">{alt.demandLevel} Demand</span>
                  <span className="px-2.5 py-0.5 rounded-full bg-[#F2F3F5] text-[#0A0A0A] text-xs font-bold border border-[#E5E7EB]">
                    {alt.matchPercentage}% Match
                  </span>
                </div>

                <h4 className="text-base font-bold text-[#0A0A0A]">{alt.title}</h4>
                <p className="text-xs text-slate-600 leading-relaxed">{alt.description}</p>

                <div className="space-y-1.5 text-xs pt-2 border-t border-[#E5E7EB]">
                  <span className="text-[10px] text-emerald-700 font-bold uppercase block">Top Strengths</span>
                  <div className="flex flex-wrap gap-1">
                    {alt.strengths.map(s => <span key={s} className="px-2 py-0.5 bg-[#F7F8FA] text-[#0A0A0A] border border-[#E5E7EB] rounded text-[10px] font-medium">{s}</span>)}
                  </div>
                </div>
              </div>

              <Button
                variant="outline"
                size="sm"
                icon={GitCompare}
                onClick={() => setSelectedAlternative(alt)}
                className="w-full text-[#0A0A0A] border-[#E5E7EB] hover:bg-[#F7F8FA]"
              >
                Compare Goal
              </Button>
            </Card>
          ))}
        </div>
      </div>

      {/* Comparison Modal */}
      {selectedAlternative && (
        <Modal isOpen={!!selectedAlternative} onClose={() => setSelectedAlternative(null)} title={`Compare: ${primaryTarget.title} vs ${selectedAlternative.title}`}>
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4 p-4 rounded-xl bg-[#F7F8FA] border border-[#E5E7EB] text-center">
              <div>
                <span className="text-[10px] text-[#8E8E93] block uppercase font-bold">Current Choice</span>
                <h4 className="text-sm font-bold text-[#0A0A0A] mt-1">{primaryTarget.title}</h4>
                <span className="text-lg font-bold text-[#0A0A0A] mt-1 block">{primaryTarget.readinessScore}% Readiness</span>
              </div>
              <div>
                <span className="text-[10px] text-[#8E8E93] block uppercase font-bold">Alternative Option</span>
                <h4 className="text-sm font-bold text-[#0A0A0A] mt-1">{selectedAlternative.title}</h4>
                <span className="text-lg font-bold text-[#0A0A0A] mt-1 block">{selectedAlternative.readinessScore}% Readiness</span>
              </div>
            </div>

            <div className="space-y-3">
              <h5 className="text-xs font-bold text-[#0A0A0A] uppercase tracking-wider">Main Skill Gaps to Bridge</h5>
              <div className="space-y-2 text-xs">
                {selectedAlternative.mainGaps.map(gap => (
                  <div key={gap} className="p-2.5 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 font-medium">
                    • {gap}
                  </div>
                ))}
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-2 border-t border-[#E5E7EB]">
              <Button variant="ghost" size="sm" onClick={() => setSelectedAlternative(null)}>Close</Button>
              <Button variant="primary" size="sm" onClick={() => setSelectedAlternative(null)}>Switch Primary Target</Button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};
