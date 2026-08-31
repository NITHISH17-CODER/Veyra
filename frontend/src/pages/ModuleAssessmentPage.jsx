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
  HelpCircle,
  Sparkles,
  RotateCcw,
  BookOpen,
  ChevronRight,
} from 'lucide-react';

export const ModuleAssessmentPage = () => {
  const { slug, moduleId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useApp();

  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes default

  useEffect(() => {
    const fetchAssessment = async () => {
      setLoading(true);
      try {
        const data = await courseService.getModuleAssessment(moduleId);
        setAssessment(data);
        if (data.time_minutes) {
          setTimeLeft(data.time_minutes * 60);
        }
      } catch (err) {
        console.error('Failed loading module assessment:', err);
        showToast('Error loading assessment from database.', 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchAssessment();
  }, [moduleId]);

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

  const handleSubmitAssessment = async () => {
    if (!assessment) return;
    const questions = assessment.questions || [];
    const answeredCount = Object.keys(answers).length;

    if (answeredCount < questions.length) {
      const confirm = window.confirm(`You have answered ${answeredCount} of ${questions.length} questions. Do you want to submit now?`);
      if (!confirm) return;
    }

    setSubmitting(true);
    try {
      const res = await courseService.submitModuleAssessment(assessment.assessment_id, answers);
      setResult(res);
      if (res.passed) {
        showToast(`🎉 Congratulations! You scored ${res.score}% and passed the module assessment!`, 'success');
      } else {
        showToast(`You scored ${res.score}%. The passing threshold is 70%. Review the module and retry.`, 'warning');
      }
    } catch (err) {
      console.error('Failed submitting assessment:', err);
      showToast('Error submitting assessment to backend.', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <LoadingState message="Loading module assessment..." />;
  if (!assessment || !assessment.questions || assessment.questions.length === 0) {
    return (
      <div className="p-12 text-center bg-white rounded-3xl border border-[#E5E7EB] space-y-4">
        <h2 className="text-xl font-bold text-[#0A0A0A]">Assessment Not Found</h2>
        <Button variant="primary" size="md" onClick={() => navigate(`/courses/${slug}/modules/${moduleId}`)}>
          Back to Module
        </Button>
      </div>
    );
  }

  const questions = assessment.questions;
  const currentQ = questions[currentQIndex];

  return (
    <div className="space-y-8 animate-fadeIn max-w-4xl mx-auto pb-16">
      {/* Back button */}
      <button
        onClick={() => navigate(`/courses/${slug}/modules/${moduleId}`)}
        className="inline-flex items-center gap-2 text-xs font-bold text-[#8E8E93] hover:text-[#0A0A0A] transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Module Overview</span>
      </button>

      {/* Header Banner */}
      <div className="p-6 sm:p-8 rounded-3xl bg-[#0A0A0A] text-white shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <Badge variant="yellow" size="xs" className="mb-1">
            Module {assessment.module_number} Knowledge Check
          </Badge>
          <h1 className="text-xl sm:text-2xl font-extrabold text-white">
            {assessment.assessment_title || 'Module MCQ Assessment'}
          </h1>
          <p className="text-xs text-slate-300">
            Pass with ≥70% score to unlock subsequent modules in your learning path.
          </p>
        </div>

        {!result && (
          <div className="flex items-center gap-3 bg-white/10 px-4 py-2 rounded-2xl border border-white/20">
            <Clock className="w-4 h-4 text-[#FFFFFF]" />
            <span className="font-mono text-sm font-extrabold text-[#FFFFFF]">
              {formatTime(timeLeft)}
            </span>
          </div>
        )}
      </div>

      {/* =========================================================================
          ASSESSMENT QUESTIONS INTERFACE (BEFORE SUBMISSION)
         ========================================================================= */}
      {!result ? (
        <div className="space-y-6">
          {/* Question Stepper Indicator */}
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
              <span className="text-xs font-mono font-bold text-[#0A0A0A] uppercase">
                Question {currentQIndex + 1} of {questions.length}
              </span>
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

            {/* Nav & Submit Buttons */}
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
                  onClick={handleSubmitAssessment}
                  disabled={submitting}
                  className="font-extrabold text-xs px-8 py-3 shadow-lg"
                >
                  {submitting ? 'Submitting & Grading...' : 'Submit Assessment'}
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
          {/* Result Score Card */}
          <Card
            className={`p-8 space-y-6 text-center border-2 rounded-3xl ${
              result.passed
                ? 'bg-emerald-50/70 border-emerald-300'
                : 'bg-rose-50/70 border-rose-300'
            }`}
          >
            <div
              className={`w-16 h-16 rounded-full mx-auto flex items-center justify-center shadow-lg ${
                result.passed
                  ? 'bg-emerald-600 text-white'
                  : 'bg-rose-600 text-white'
              }`}
            >
              {result.passed ? <CheckCircle2 className="w-9 h-9" /> : <XCircle className="w-9 h-9" />}
            </div>

            <div className="space-y-1">
              <span className="text-xs font-mono font-extrabold uppercase tracking-widest text-[#8E8E93]">
                Assessment Results
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0A0A0A]">
                {result.passed ? 'Assessment Passed! 🎉' : 'Assessment Not Passed'}
              </h2>
              <p className="text-xs sm:text-sm text-slate-600 max-w-md mx-auto">
                {result.passed
                  ? 'You successfully met the passing criteria! Next module is now unlocked in your curriculum.'
                  : 'You scored below the 70% threshold. Review the questions and module lessons below to retry.'}
              </p>
            </div>

            <div className="flex justify-center items-center gap-6 py-2">
              <div className="p-4 rounded-2xl bg-white border border-[#E5E7EB] shadow-sm min-w-32">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Your Score</span>
                <span className={`text-2xl font-extrabold font-mono ${result.passed ? 'text-emerald-600' : 'text-rose-600'}`}>
                  {result.score}%
                </span>
              </div>
              <div className="p-4 rounded-2xl bg-white border border-[#E5E7EB] shadow-sm min-w-32">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Required</span>
                <span className="text-2xl font-extrabold font-mono text-[#0A0A0A]">70%</span>
              </div>
              <div className="p-4 rounded-2xl bg-white border border-[#E5E7EB] shadow-sm min-w-32">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Correct</span>
                <span className="text-2xl font-extrabold font-mono text-[#0A0A0A]">
                  {result.correct_answers} / {result.total_questions}
                </span>
              </div>
            </div>

            {/* Action buttons */}
            <div className="flex flex-wrap justify-center gap-4 pt-4 border-t border-[#E5E7EB]/60">
              {result.passed ? (
                <>
                  <Button
                    variant="primary"
                    size="lg"
                    icon={ArrowRight}
                    iconPosition="right"
                    onClick={() => {
                      if (result.next_module_id) {
                        navigate(`/courses/${slug}/modules/${result.next_module_id}`);
                      } else {
                        navigate(`/courses/${slug}`);
                      }
                    }}
                    className="bg-[#0A0A0A] hover:bg-[#3882e0] font-extrabold text-xs px-8 py-3 shadow-lg"
                  >
                    Proceed to Next Module
                  </Button>

                  <Button
                    variant="outline"
                    size="lg"
                    onClick={() => navigate(`/courses/${slug}`)}
                    className="font-bold text-xs"
                  >
                    Back to Course Roadmap
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
                    Retake Assessment
                  </Button>

                  <Button
                    variant="outline"
                    size="lg"
                    icon={BookOpen}
                    onClick={() => navigate(`/courses/${slug}/modules/${moduleId}`)}
                    className="font-bold text-xs"
                  >
                    Review Module Lessons
                  </Button>
                </>
              )}
            </div>
          </Card>

          {/* Question by Question Review */}
          <div className="space-y-4">
            <h3 className="text-base font-extrabold text-[#0A0A0A]">
              Detailed Question Review & Explanations
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
