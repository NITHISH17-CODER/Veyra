import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { courseService } from '../services/courseService';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { LoadingState } from '../components/common/LoadingState';
import {
  ArrowLeft,
  Award,
  Download,
  CheckCircle2,
  Sparkles,
  TrendingUp,
  BookOpen,
  ArrowRight,
  ShieldCheck,
  FileText,
  Star,
} from 'lucide-react';

export const CourseCompletionPage = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const { user, showToast } = useApp();

  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    const fetchSummary = async () => {
      setLoading(true);
      try {
        const data = await courseService.getCompletionSummary(slug);
        setSummary(data);
      } catch (err) {
        console.error('Failed loading completion summary:', err);
        showToast('Error loading course completion data.', 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, [slug]);

  const handleDownloadTxt = async () => {
    setDownloading(true);
    try {
      await courseService.downloadCompletionSummary(slug);
      showToast('Downloaded course summary text file successfully!', 'success');
    } catch (err) {
      console.error('Download error:', err);
      showToast('Error downloading course summary.', 'error');
    } finally {
      setDownloading(false);
    }
  };

  if (loading) return <LoadingState message="Generating your official graduation certificate & summary..." />;
  if (!summary) return (
    <div className="p-12 text-center bg-white rounded-3xl border border-[#E5E7EB] space-y-4">
      <h2 className="text-xl font-bold text-[#0A0A0A]">Summary Not Available</h2>
      <Button variant="primary" size="md" onClick={() => navigate(`/courses/${slug}`)}>
        Back to Course
      </Button>
    </div>
  );

  return (
    <div className="space-y-8 animate-fadeIn max-w-4xl mx-auto pb-16">
      {/* Back button */}
      <button
        onClick={() => navigate(`/courses/${slug}`)}
        className="inline-flex items-center gap-2 text-xs font-bold text-[#8E8E93] hover:text-[#0A0A0A] transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Course Overview</span>
      </button>

      {/* Graduation Certificate Hero Banner */}
      <div className="p-8 sm:p-12 rounded-3xl bg-gradient-to-br from-[#146EF5] via-[#0B5ED7] to-[#146EF5] text-white shadow-2xl relative overflow-hidden space-y-6 border-4 border-white">
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl pointer-events-none" />

        <div className="text-center space-y-4 relative z-10 max-w-2xl mx-auto">
          <div className="flex items-center justify-center gap-2 mb-1">
            <img src="/veyra-logo.png" alt="Veyra Logo" className="w-10 h-10 rounded-xl object-contain shadow-md border border-white/30" />
            <span className="text-2xl font-black text-white tracking-tight font-sans">VEYRA</span>
          </div>

          <div className="w-16 h-16 rounded-2xl bg-white text-[#146EF5] mx-auto flex items-center justify-center shadow-xl shadow-blue-900/30">
            <Award className="w-10 h-10" />
          </div>

          <div className="space-y-1">
            <span className="text-xs font-mono font-extrabold uppercase tracking-widest text-blue-100">
              Official Certificate of Completion
            </span>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              {summary.course_title}
            </h1>
            <p className="text-xs sm:text-sm text-blue-100">
              Presented to <strong className="text-white font-extrabold">{summary.user_name || user?.name || 'Learner'}</strong>
            </p>
          </div>

          <div className="flex flex-wrap justify-center items-center gap-4 pt-2">
            <span className="px-4 py-1.5 rounded-full bg-white/15 border border-white/25 text-xs font-bold font-mono text-white">
              Final Grade: <strong className="text-white text-sm">{summary.final_grade || 'A+'}</strong> ({summary.final_score || 100}%)
            </span>
            <span className="px-4 py-1.5 rounded-full bg-white/15 border border-white/25 text-xs font-bold text-white">
              12 / 12 Modules Completed
            </span>
            <span className="px-4 py-1.5 rounded-full bg-white/20 border border-white/30 text-white text-xs font-bold flex items-center gap-1">
              <ShieldCheck className="w-4 h-4 text-white" /> Verified Curriculum
            </span>
          </div>
        </div>
      </div>

      {/* Skills Mastered & Verified */}
      <Card className="p-8 space-y-4 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm">
        <div className="flex items-center gap-2 border-b border-[#E5E7EB] pb-3">
          <CheckCircle2 className="w-5 h-5 text-emerald-600" />
          <h2 className="text-lg font-extrabold text-[#0A0A0A]">
            Verified Skills Mastered ({summary.skills_learned?.length || 0})
          </h2>
        </div>
        <div className="flex flex-wrap gap-2 pt-1">
          {(summary.skills_learned || []).map((sk) => (
            <span
              key={sk}
              className="px-3 py-1.5 rounded-xl bg-[#F7F8FA] text-[#0A0A0A] border border-[#E5E7EB] text-xs font-extrabold flex items-center gap-1.5 shadow-sm"
            >
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              <span>{sk}</span>
            </span>
          ))}
        </div>
      </Card>

      {/* Strengths and Highlights Diagnostics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <Card className="p-6 space-y-3 bg-white border border-[#E5E7EB] rounded-3xl">
          <div className="flex items-center gap-2 text-emerald-700 font-extrabold text-sm">
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span>Demonstrated Strengths</span>
          </div>
          <ul className="space-y-2 text-xs text-slate-700">
            {(summary.strengths || []).map((s, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-emerald-600 font-bold">•</span>
                <span>{s}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card className="p-6 space-y-3 bg-white border border-[#E5E7EB] rounded-3xl">
          <div className="flex items-center gap-2 text-[#0A0A0A] font-extrabold text-sm">
            <TrendingUp className="w-4 h-4 text-[#0A0A0A]" />
            <span>Recommended Next Steps</span>
          </div>
          <ul className="space-y-2 text-xs text-slate-700">
            {(summary.recommended_next_steps || []).map((step, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-[#0A0A0A] font-bold">→</span>
                <span>{step}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>

      {/* Action Buttons & Text File Export */}
      <div className="p-8 rounded-3xl bg-[#F7F8FA] border-2 border-[#E5E7EB] flex flex-col sm:flex-row items-center justify-between gap-6 shadow-sm">
        <div className="space-y-1 text-center sm:text-left">
          <div className="flex items-center gap-2 justify-center sm:justify-start">
            <FileText className="w-5 h-5 text-[#0A0A0A]" />
            <h3 className="text-base font-extrabold text-[#0A0A0A]">
              Download Official Course Summary (.txt)
            </h3>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed max-w-md">
            Export a full plain-text record of your curriculum, modules completed, assessment scores, and verified skills.
          </p>
        </div>

        <Button
          variant="yellow"
          size="lg"
          icon={Download}
          onClick={handleDownloadTxt}
          disabled={downloading}
          className="font-extrabold text-xs px-8 py-3.5 shadow-md shrink-0"
        >
          {downloading ? 'Downloading...' : 'Download Course Summary (.txt)'}
        </Button>
      </div>

      {/* Footer Navigation */}
      <div className="flex justify-between items-center pt-4 border-t border-[#E5E7EB]">
        <Button
          variant="ghost"
          size="md"
          icon={ArrowLeft}
          onClick={() => navigate('/courses')}
        >
          Explore All Tracks
        </Button>

        <Button
          variant="primary"
          size="md"
          icon={ArrowRight}
          iconPosition="right"
          onClick={() => navigate('/dashboard')}
          className="bg-[#0A0A0A] hover:bg-[#3882e0] font-extrabold text-xs"
        >
          Go to My Dashboard
        </Button>
      </div>
    </div>
  );
};
