import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { projectService } from '../services/projectService';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { LoadingState } from '../components/common/LoadingState';
import { FolderGit2, ArrowRight, Award, CheckCircle2, AlertCircle } from 'lucide-react';

export const ProjectsPage = () => {
  const navigate = useNavigate();
  const { user } = useApp();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedLevel, setSelectedLevel] = useState('ALL');

  useEffect(() => {
    const fetchProjects = async () => {
      setLoading(true);
      try {
        const data = await projectService.getProjects();
        setProjects(data || []);
      } catch (err) {
        console.error("Failed loading projects catalog:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProjects();
  }, []);

  // ONLY Basic, Intermediate, Advanced (Expert strictly removed)
  const levels = ['ALL', 'BASIC', 'INTERMEDIATE', 'ADVANCED'];

  const filteredProjects = projects.filter(p => {
    const lvl = (p.difficulty || p.level || '').toUpperCase();
    if (lvl === 'EXPERT') return false; // Safety guard
    if (selectedLevel === 'ALL') return true;
    return lvl === selectedLevel;
  });

  const completedCount = projects.filter(p => p.status === 'completed' || p.verification_state === 'VERIFIED').length;
  const isCertificateEligible = completedCount >= 15 && projects.length >= 15;

  const recommendedProject = projects.find(p => (p.difficulty || p.level || '').toUpperCase() === 'ADVANCED' && p.status !== 'completed') || projects[0];

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">PROJECT CATALOG</span>
            {user?.targetGoal && (
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-[#0A0A0A] text-white">
                {user.targetGoal}
              </span>
            )}
          </div>
          <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">Build what you learn.</h1>
          <p className="text-sm text-[#45515E]">
            Apply your skills with 15 real-world coding projects (5 Basic, 5 Intermediate, 5 Advanced) verified by automated AI evaluations.
          </p>
        </div>

        {/* Certificate Badge Banner */}
        <div className="p-4 rounded-2xl bg-[#146EF5] text-white flex items-center gap-3 shrink-0 shadow-md shadow-blue-500/20">
          <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center font-bold text-white">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold block text-white">Course Certificate</span>
            <span className="text-[11px] text-blue-100 block font-mono">{completedCount} / 15 Projects Verified</span>
          </div>
        </div>
      </div>

      {/* CERTIFICATE ELIGIBILITY BANNER */}
      {isCertificateEligible && (
        <Card radius="24" className="p-6 bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Award className="w-8 h-8 text-amber-600 shrink-0" />
            <div>
              <h3 className="text-base font-bold text-amber-900">Project Completion Certificate Eligible!</h3>
              <p className="text-xs text-amber-800">
                Congratulations! You have verified all 15 projects for {user?.targetGoal || "your career path"}.
              </p>
            </div>
          </div>
          <Button
            variant="primary"
            size="md"
            onClick={() => navigate('/profile')}
            className="shrink-0"
          >
            Claim Certificate
          </Button>
        </Card>
      )}

      {/* RECOMMENDED PROJECT HIGHLIGHT CARD */}
      {recommendedProject && (
        <Card radius="32" className="p-8 bg-white border border-[#E5E7EB] space-y-6">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">RECOMMENDED PROJECT</span>
            <Badge variant="dark">{(recommendedProject.difficulty || recommendedProject.level || 'ADVANCED').toUpperCase()}</Badge>
          </div>

          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <h2 className="text-2xl font-bold text-[#0A0A0A]">{recommendedProject.title}</h2>
              <p className="text-xs text-[#45515E] max-w-2xl">{recommendedProject.description || recommendedProject.problemStatement}</p>

              {recommendedProject.skills && (
                <div className="flex flex-wrap gap-1.5 pt-2">
                  {recommendedProject.skills.map(sk => (
                    <Badge key={sk} variant="surface" size="xs">{sk}</Badge>
                  ))}
                </div>
              )}
            </div>

            <Button
              variant="primary"
              size="lg"
              icon={ArrowRight}
              iconPosition="right"
              onClick={() => navigate(`/projects/${recommendedProject.id}`)}
              className="shrink-0"
            >
              {recommendedProject.status === 'completed' ? 'Review Submission' : 'Start Project'}
            </Button>
          </div>
        </Card>
      )}

      {/* LEVEL FILTER PILLS (Only Basic, Intermediate, Advanced) */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {levels.map(lvl => (
          <button
            key={lvl}
            onClick={() => setSelectedLevel(lvl)}
            className={`btn-pill-tab ${selectedLevel === lvl ? 'bg-[#0A0A0A] text-white px-4 py-1.5 text-xs font-semibold rounded-full' : 'bg-[#F7F8FA] text-[#45515E] hover:bg-[#F2F3F5] px-4 py-1.5 text-xs font-semibold rounded-full border border-[#E5E7EB]'}`}
          >
            {lvl}
          </button>
        ))}
      </div>

      {/* PROJECT CATALOG GRID */}
      {loading ? (
        <LoadingState message="Loading database projects catalog..." />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects.map(proj => (
            <Card key={proj.id} radius="16" className="p-6 space-y-4 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="p-2 rounded-xl bg-[#F7F8FA] text-[#0A0A0A]">
                    <FolderGit2 className="w-5 h-5" />
                  </div>
                  <div className="flex items-center gap-2">
                    {proj.status === 'completed' && (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" /> Verified
                      </span>
                    )}
                    <Badge variant="surface">{(proj.difficulty || proj.level || 'BASIC').toUpperCase()}</Badge>
                  </div>
                </div>
                <h3 className="text-lg font-bold text-[#0A0A0A]">{proj.title}</h3>
                <p className="text-xs text-[#45515E] line-clamp-2">{proj.description || proj.problemStatement}</p>

                {proj.skills && (
                  <div className="flex flex-wrap gap-1 pt-2">
                    {proj.skills.slice(0, 3).map(s => (
                      <Badge key={s} variant="slate" size="xs">{s}</Badge>
                    ))}
                  </div>
                )}
              </div>

              <Button
                variant={proj.status === 'completed' ? 'outline' : 'primary'}
                size="sm"
                onClick={() => navigate(`/projects/${proj.id}`)}
                className="w-full justify-center mt-4"
              >
                {proj.status === 'completed' ? 'View Evaluation' : 'Start Project'}
              </Button>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
