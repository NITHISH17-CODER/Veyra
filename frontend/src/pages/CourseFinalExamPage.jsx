import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { courseService } from '../services/courseService';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { ProgressBar } from '../components/common/ProgressBar';
import { LoadingState } from '../components/common/LoadingState';
import { QuestionReviewCard } from '../components/common/QuestionReviewCard';
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  XCircle,
  Clock,
  Award,
  Sparkles,
  RotateCcw,
  BookOpen,
  TrendingUp,
  FileCheck,
} from 'lucide-react';

export const CourseFinalExamPage = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const { showToast } = useApp();

  const [exam, setExam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [timeLeft, setTimeLeft] = useState(2700); // 45 minutes default

  useEffect(() => {
    const fetchExam = async () => {
      setLoading(true);
      try {
        const data = await courseService.getFinalAssessment(slug);
        setExam(data);
        if (data.time_minutes) {
          setTimeLeft(data.time_minutes * 60);
        }
      } catch (err) {
        console.error('Failed loading final exam:', err);
        showToast('Error loading comprehensive final exam.', 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchExam();
  }, [slug]);

  // Timer countdown
  useEffect(() => {
    if (!result && timeLeft > 0) {
      const timer = setInterval(() => setTimeLeft((t) => t - 1), 1000);
      return () => clearInterval(timer);
    }
  }, [result, timeLeft]);

  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  const handleSelectOption = (questionId, optionIndex) => {
    setAnswers({
      ...answers,
      [String(questionId)]: optionIndex,
    });
  };

  const handleSubmitFinalExam = async () => {
    if (!exam) return;
    const questions = exam.questions || [];
    const answeredCount = Object.keys(answers).length;

    if (answeredCount < questions.length) {
      const confirm = window.confirm(`You answered ${answeredCount} of ${questions.length} questions. Do you want to submit your final exam?`);
      if (!confirm) return;
    }

    setSubmitting(true);
    try {
      const res = await courseService.submitFinalAssessment(slug, answers);
      setResult(res);
      if (res.passed) {
        showToast(`🎉 Outstanding! You achieved Grade ${res.grade} with ${res.score}%! Course Completed!`, 'success');
      } else {
        showToast(`You scored ${res.score}%. The passing threshold is 70%. Review curriculum and retry.`, 'warning');
      }
    } catch (err) {
      console.error('Failed submitting final exam:', err);
      showToast('Error submitting exam to backend.', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <LoadingState message="Loading comprehensive course exam..." />;
  if (!exam || !exam.questions || exam.questions.length === 0) {
    return (
      <div className="p-12 text-center bg-white rounded-3xl border border-[#E5E7EB] space-y-4">
        <h2 className="text-xl font-bold text-[#0A0A0A]">Final Exam Not Found</h2>
        <Button variant="primary" size="md" onClick={() => navigate(`/courses/${slug}`)}>
          Back to Course Overview
        </Button>
      </div>
    );
  }

  const questions = exam.questions;
  const currentQ = questions[currentQIndex];

  return (
    <div className="space-y-8 animate-fadeIn max-w-4xl mx-auto pb-16">
      {/* Back button */}
      <button
        onClick={() => navigate(`/courses/${slug}`)}
        className="inline-flex items-center gap-2 text-xs font-bold text-[#8E8E93] hover:text-[#0A0A0A] transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Course Syllabus</span>
      </button>

      {/* Header Banner */}
      <div className="p-8 rounded-3xl bg-gradient-to-br from-[#0A0A0A] to-[#111111] text-white shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 border-2 border-[#FFFFFF]">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-[#FFFFFF]" />
            <span className="text-xs font-extrabold text-[#FFFFFF] uppercase tracking-wider">
              {exam.course_title} • Capstone Certification
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
            {exam.exam_title || 'Comprehensive Course Final Exam'}
          </h1>
          <p className="text-xs text-slate-300 max-w-lg leading-relaxed">
            {exam.description || '10-question rigorous examination covering all 12 modules. Score ≥70% to graduate.'}
          </p>
        </div>

        {!result && (
          <div className="flex items-center gap-3 bg-white/10 px-5 py-3 rounded-2xl border border-white/20">
            <Clock className="w-5 h-5 text-[#FFFFFF]" />
            <div className="text-right">
              <span className="text-[10px] text-slate-300 uppercase font-bold block">Time Left</span>
              <span className="font-mono text-base font-extrabold text-[#FFFFFF]">
                {formatTime(timeLeft)}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* =========================================================================
          EXAM QUESTIONS INTERFACE
         ========================================================================= */}
      {!result ? (
        <div className="space-y-6">
          {/* Question Grid Stepper */}
          <div className="flex items-center gap-2 overflow-x-auto pb-2">
            {questions.map((q, idx) => {
              const isAnswered = answers[String(q.id)] !== undefined;
              const isCurrent = idx === currentQIndex;
              return (
                <button
                  key={q.id}
                  onClick={() => setCurrentQIndex(idx)}
                  className={`w-9 h-9 rounded-xl text-xs font-bold font-mono transition-all flex items-center justify-center shrink-0 ${
                    isCurrent
                      ? 'bg-[#0A0A0A] text-[#FFFFFF] ring-2 ring-[#0A0A0A] shadow-md'
                      : isAnswered
                      ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                      : 'bg-white text-slate-600 border border-[#E5E7EB] hover:border-[#0A0A0A]'
                  }`}
                >
                  {idx + 1}
                </button>
              );
            })}
          </div>

          {/* Active Question Card */}
          <Card className="p-8 space-y-6 bg-white border border-[#E5E7EB] rounded-3xl shadow-sm">
            <div className="flex justify-between items-center border-b border-[#E5E7EB] pb-3">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-bold text-[#0A0A0A] uppercase">
                  Question {currentQIndex + 1} of {questions.length}
                </span>
                {currentQ.topic && (
                  <Badge variant="indigo" size="xs">{currentQ.topic}</Badge>
                )}
              </div>
              <span className="text-[11px] font-semibold text-slate-400">
                Single Choice
              </span>
            </div>

            <h3 className="text-base sm:text-lg font-extrabold text-[#0A0A0A] leading-relaxed">
              {currentQ.question_text}
            </h3>

            {/* Options */}
            <div className="space-y-3">
              {(currentQ.options || []).map((opt, optIdx) => {
                const isSelected = answers[String(currentQ.id)] === optIdx;
                return (
                  <div
                    key={optIdx}
                    onClick={() => handleSelectOption(currentQ.id, optIdx)}
                    className={`p-4 rounded-2xl border transition-all cursor-pointer flex items-center gap-3.5 ${
                      isSelected
                        ? 'bg-[#F7F8FA] border-2 border-[#0A0A0A] shadow-sm text-[#0A0A0A]'
                        : 'bg-white border-[#E5E7EB] hover:border-slate-300 text-slate-700'
                    }`}
                  >
                    <div
                      className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${
                        isSelected
                          ? 'bg-[#0A0A0A] text-white'
                          : 'border border-slate-300 text-slate-400'
                      }`}
                    >
                      {String.fromCharCode(65 + optIdx)}
                    </div>
                    <span className="text-xs sm:text-sm font-semibold leading-normal">
                      {opt}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Nav & Submit */}
            <div className="flex items-center justify-between pt-6 border-t border-[#E5E7EB]">
              <Button
                variant="outline"
                size="md"
                onClick={() => setCurrentQIndex((i) => Math.max(0, i - 1))}
                disabled={currentQIndex === 0}
                className="text-xs font-bold"
              >
                Previous
              </Button>

              {currentQIndex < questions.length - 1 ? (
                <Button
                  variant="primary"
                  size="md"
                  onClick={() => setCurrentQIndex((i) => Math.min(questions.length - 1, i + 1))}
                  className="bg-[#0A0A0A] hover:bg-[#3882e0] font-bold text-xs"
                >
                  Next Question
                </Button>
              ) : (
                <Button
                  variant="yellow"
                  size="lg"
                  icon={CheckCircle2}
                  onClick={handleSubmitFinalExam}
                  disabled={submitting}
                  className="font-extrabold text-xs px-8 py-3.5 shadow-xl"
                >
                  {submitting ? 'Evaluating Final Exam...' : 'Submit Final Exam'}
                </Button>
              )}
            </div>
          </Card>
        </div>
      ) : (
        /* =========================================================================
            RESULTS VIEW (AFTER SUBMISSION)
           ========================================================================= */
        <div className="space-y-6 animate-fadeIn">
          <Card
            className={`p-8 space-y-6 text-center border-2 rounded-3xl ${
              result.passed
                ? 'bg-emerald-50/80 border-emerald-300'
                : 'bg-rose-50/80 border-rose-300'
            }`}
          >
            <div
              className={`w-20 h-20 rounded-full mx-auto flex items-center justify-center shadow-xl ${
                result.passed
                  ? 'bg-emerald-600 text-white'
                  : 'bg-rose-600 text-white'
              }`}
            >
              {result.passed ? <Award className="w-10 h-10 text-[#FFFFFF]" /> : <XCircle className="w-10 h-10" />}
            </div>

            <div className="space-y-1">
              <span className="text-xs font-mono font-extrabold uppercase tracking-widest text-[#8E8E93]">
                Official Certification Result
              </span>
              <h2 className="text-3xl font-extrabold text-[#0A0A0A]">
                {result.passed ? 'Course Completed with Honors! 🎓' : 'Final Exam Not Passed'}
              </h2>
              <p className="text-xs sm:text-sm text-slate-600 max-w-lg mx-auto">
                {result.passed
                  ? `Congratulations! You scored ${result.score}% (Grade: ${result.grade}) on the comprehensive exam and have successfully graduated from this career program.`
                  : 'You achieved below 70%. Review the topic diagnostics below to prepare for your retake.'}
              </p>
            </div>

            {/* Score & Grade Cards */}
            <div className="flex justify-center items-center gap-4 sm:gap-6 py-2 flex-wrap">
              <div className="p-4 rounded-2xl bg-white border border-[#E5E7EB] shadow-sm min-w-28 text-center">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Grade</span>
                <span className="text-3xl font-extrabold font-mono text-[#0A0A0A]">
                  {result.grade}
                </span>
              </div>
              <div className="p-4 rounded-2xl bg-white border border-[#E5E7EB] shadow-sm min-w-28 text-center">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Score</span>
                <span className={`text-3xl font-extrabold font-mono ${result.passed ? 'text-emerald-600' : 'text-rose-600'}`}>
                  {result.score}%
                </span>
              </div>
              <div className="p-4 rounded-2xl bg-white border border-[#E5E7EB] shadow-sm min-w-28 text-center">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Correct</span>
                <span className="text-3xl font-extrabold font-mono text-[#0A0A0A]">
                  {result.correct_answers}/{result.total_questions}
                </span>
              </div>
            </div>

            {/* Topic Diagnostics: Strong vs Weak */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-left max-w-2xl mx-auto pt-2">
              <div className="p-4 rounded-2xl bg-white border border-emerald-200 space-y-2">
                <span className="text-xs font-bold text-emerald-800 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Strong Topic Mastery:
                </span>
                <div className="flex flex-wrap gap-1">
                  {(result.strong_topics || []).map((t) => (
                    <span key={t} className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 text-[10px] font-bold border border-emerald-200">
                      {t}
                    </span>
                  ))}
                  {(result.strong_topics || []).length === 0 && (
                    <span className="text-[11px] text-slate-400 italic">None identified</span>
                  )}
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-white border border-amber-200 space-y-2">
                <span className="text-xs font-bold text-amber-800 flex items-center gap-1.5">
                  <TrendingUp className="w-4 h-4 text-amber-600" /> Recommended Review Areas:
                </span>
                <div className="flex flex-wrap gap-1">
                  {(result.weak_topics || []).map((t) => (
                    <span key={t} className="px-2 py-0.5 rounded bg-amber-50 text-amber-800 text-[10px] font-bold border border-amber-200">
                      {t}
                    </span>
                  ))}
                  {(result.weak_topics || []).length === 0 && (
                    <span className="text-[11px] text-emerald-600 font-bold">100% Mastery across all topics!</span>
                  )}
                </div>
              </div>
            </div>

            {/* Action buttons */}
            <div className="flex flex-wrap justify-center gap-4 pt-6 border-t border-[#E5E7EB]/60">
              {result.passed ? (
                <>
                  <Button
                    variant="yellow"
                    size="xl"
                    icon={Award}
                    onClick={() => navigate(`/courses/${slug}/completion`)}
                    className="font-extrabold text-xs px-8 py-3.5 shadow-xl"
                  >
                    View Certificate & Summary
                  </Button>

                  <Button
                    variant="outline"
                    size="lg"
                    onClick={() => navigate(`/courses/${slug}`)}
                    className="font-bold text-xs"
                  >
                    Back to Course Syllabus
                  </Button>
                </>
              ) : (
                <>
                  <Button
                    variant="yellow"
                    size="lg"
                    icon={RotateCcw}
                    onClick={() => {
                      setResult(null);
                      setAnswers({});
                      setCurrentQIndex(0);
                    }}
                    className="font-extrabold text-xs px-8 py-3 shadow-lg"
                  >
                    Retake Final Exam
                  </Button>

                  <Button
                    variant="outline"
                    size="lg"
                    onClick={() => navigate(`/courses/${slug}`)}
                    className="font-bold text-xs"
                  >
                    Review Curriculum Modules
                  </Button>
                </>
              )}
            </div>
          </Card>

          {/* Detailed Question Review */}
          <div className="space-y-4">
            <h3 className="text-base font-extrabold text-[#0A0A0A]">
              Question Review & Deep Explanations
            </h3>

            {(result.questions_review || result.detailed_results || questions).map((q, idx) => (
              <QuestionReviewCard
                key={q.id || idx}
                question={q}
                index={idx}
                userSelection={answers[String(q.id || q.question_id)]}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
