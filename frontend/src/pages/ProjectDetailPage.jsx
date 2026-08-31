import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { projectService } from '../services/projectService';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { LoadingState } from '../components/common/LoadingState';
import { ArrowLeft, CheckCircle2, XCircle, AlertCircle, Send, Award, ExternalLink } from 'lucide-react';

export const ProjectDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { showToast } = useApp();
  const [project, setProject] = useState(null);
  const [submissionUrl, setSubmissionUrl] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [evaluationResult, setEvaluationResult] = useState(null);

  useEffect(() => {
    const loadProject = async () => {
      try {
        const data = await projectService.getProjectById(id);
        setProject(data);

        // Fetch existing progress
        const prog = await projectService.getProjectProgress(id);
        if (prog) {
          setEvaluationResult(prog);
          if (prog.submission_url) setSubmissionUrl(prog.submission_url);
        }
      } catch (err) {
        console.error("Failed loading project details:", err);
      }
    };
    loadProject();
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const cleanUrl = submissionUrl.trim();
    const isGithub = /^https?:\/\/(www\.)?github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+\/?.*$/i.test(cleanUrl);
    const isColab = /^https?:\/\/colab\.research\.google\.com\/.*$/i.test(cleanUrl);

    if (!isGithub && !isColab) {
      setError("Invalid submission URL. Please submit a valid GitHub repository URL or Google Colab URL.");
      return;
    }

    setSubmitting(true);
    try {
      const res = await projectService.submitProject(id, cleanUrl, "");
      if (res.success && res.data) {
        setEvaluationResult(res.data);
        const state = res.data.verification_state || (res.data.status === 'completed' ? 'VERIFIED' : 'REJECTED');
        if (state === 'VERIFIED') {
          showToast("✓ Project submission verified successfully!", "success");
        } else {
          showToast(`Submission review: ${state}`, "warning");
        }
      }
    } catch (err) {
      const msg = err.response?.data?.detail || err.response?.data?.message || err.message || "Failed evaluating project submission.";
      setError(msg);
      showToast(msg, "error");
    } finally {
      setSubmitting(false);
    }
  };

  if (!project) return <LoadingState message="Loading project details..." />;

  const verificationState = evaluationResult?.verification_state || (evaluationResult?.status === 'completed' ? 'VERIFIED' : 'NOT_SUBMITTED');

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-4xl mx-auto">
      {/* Back button */}
      <button
        onClick={() => navigate('/projects')}
        className="inline-flex items-center gap-2 text-xs font-bold text-[#8E8E93] hover:text-[#0A0A0A]"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Project Catalog</span>
      </button>

      {/* Project Header Card */}
      <Card radius="24" className="p-8 space-y-4 bg-white border border-[#E5E7EB]">
        <div className="flex items-center justify-between">
          <Badge variant="dark">{(project.difficulty || project.level || 'BASIC').toUpperCase()}</Badge>
          <span className="text-xs text-[#8E8E93] font-mono">Est: {project.estimated_hours || 15} hours</span>
        </div>

        <h1 className="text-3xl font-bold text-[#0A0A0A]">{project.title}</h1>
        <p className="text-sm text-[#45515E] leading-relaxed">{project.problemStatement || project.description}</p>

        {project.skills && (
          <div className="flex flex-wrap gap-2 pt-2 border-t border-[#E5E7EB]">
            <span className="text-xs font-semibold text-[#8E8E93]">Skills:</span>
            {project.skills.map(s => <Badge key={s} variant="surface" size="xs">{s}</Badge>)}
          </div>
        )}
      </Card>

      {/* Submission Card */}
      <Card radius="24" className="p-8 space-y-6 bg-white border border-[#E5E7EB]">
        <div className="space-y-1">
          <h2 className="text-xl font-bold text-[#0A0A0A]">Show us what you built.</h2>
          <p className="text-xs text-[#8E8E93]">Submit a public GitHub repository or Google Colab notebook URL for verification.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <div className="relative">
              <input
                type="url"
                value={submissionUrl}
                onChange={(e) => {
                  setSubmissionUrl(e.target.value);
                  if (error) setError('');
                }}
                placeholder="https://github.com/username/repository or https://colab.research.google.com/..."
                className="input-flat w-full pr-10"
              />
              {submissionUrl && (
                <a
                  href={submissionUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#8E8E93] hover:text-[#0A0A0A]"
                  title="Open URL"
                >
                  <ExternalLink className="w-4 h-4" />
                </a>
              )}
            </div>
            {error && (
              <p className="text-xs font-semibold text-rose-600 flex items-center gap-1 mt-1">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                <span>{error}</span>
              </p>
            )}
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            loading={submitting}
            disabled={!submissionUrl.trim() || submitting}
            icon={Send}
            iconPosition="right"
          >
            {submitting ? "Verifying Submission..." : "Verify & Analyze Project"}
          </Button>
        </form>
      </Card>

      {/* VERIFICATION STATE BANNER & REVIEW RESULT */}
      {evaluationResult && (
        <Card radius="24" className="p-8 space-y-6 border border-[#0A0A0A] bg-white">
          <div className="flex items-center justify-between border-b border-[#E5E7EB] pb-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">VERIFICATION STATUS</span>
                <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full flex items-center gap-1 ${
                  verificationState === 'VERIFIED'
                    ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                    : verificationState === 'ACCESS_ERROR' || verificationState === 'INVALID_URL'
                    ? 'bg-amber-100 text-amber-900 border border-amber-300'
                    : 'bg-rose-100 text-rose-800 border border-rose-300'
                }`}>
                  {verificationState === 'VERIFIED' ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                  {verificationState}
                </span>
              </div>
              <h3 className="text-xl font-bold text-[#0A0A0A]">{project.title}</h3>
            </div>
            {evaluationResult.score !== undefined && (
              <div className="text-right">
                <span className="text-3xl font-extrabold text-[#0A0A0A] font-mono">
                  {evaluationResult.score} / 100
                </span>
                <span className="text-xs text-[#8E8E93] block">Evaluation Score</span>
              </div>
            )}
          </div>

          {/* Feedback Text */}
          {evaluationResult.technical_feedback && (
            <div className="p-4 rounded-xl bg-[#F7F8FA] border border-[#E5E7EB] text-xs text-[#0A0A0A] leading-relaxed font-medium">
              {evaluationResult.technical_feedback}
            </div>
          )}

          {/* Strengths & Improvements */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-2">
            <div className="space-y-2 text-xs">
              <span className="font-bold text-[#0A0A0A] uppercase tracking-wider block">Strengths</span>
              <div className="space-y-1.5">
                {(evaluationResult.strengths || []).map((s, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-[#0A0A0A] font-medium">
                    <span className="text-[#1BA673] font-bold">✓</span>
                    <span>{s}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-2 text-xs">
              <span className="font-bold text-[#0A0A0A] uppercase tracking-wider block">Recommended Improvements</span>
              <div className="space-y-1.5">
                {(evaluationResult.recommended_improvements || evaluationResult.improvements || []).map((imp, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-[#45515E] font-medium">
                    <span className="text-[#0A0A0A] font-bold">→</span>
                    <span>{imp}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
