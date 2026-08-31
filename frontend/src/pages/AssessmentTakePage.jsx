import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useApp } from '../context/AppContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { ProgressBar } from '../components/common/ProgressBar';
import { LoadingState } from '../components/common/LoadingState';
import { QuestionReviewCard } from '../components/common/QuestionReviewCard';
import { ArrowLeft, ArrowRight, Check, RotateCcw, Award, XCircle, CheckCircle2 } from 'lucide-react';

export const AssessmentTakePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { showToast } = useApp();

  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchQuiz = async () => {
      setLoading(true);
      try {
        const res = await api.get(`/quizzes/${id}`);
        if (res.data && res.data.questions?.length) {
          setQuiz(res.data);
        } else {
          setQuiz({ __error: true });
        }
      } catch (err) {
        console.error('Quiz fetch failed:', err);
        setQuiz({ __error: true });
      } finally {
        setLoading(false);
      }
    };
    fetchQuiz();
  }, [id]);

  if (loading) return <LoadingState message="Loading quiz questions..." />;

  if (!quiz || quiz.__error) {
    return (
      <Card radius="24" className="p-12 text-center space-y-4 max-w-md mx-auto my-12">
        <h2 className="text-xl font-bold text-[#0A0A0A]">Quiz Not Found</h2>
        <p className="text-sm text-[#45515E]">This quiz could not be loaded from the database.</p>
        <Button variant="primary" size="md" onClick={() => navigate('/quizzes')}>
          Back to Quizzes
        </Button>
      </Card>
    );
  }

  const currentQ = quiz.questions[currentQuestionIndex];
  const totalQ = quiz.questions.length;

  const handleSelectOption = (qId, optionIdx) => {
    if (submitted) return;
    setAnswers({ ...answers, [qId]: optionIdx });
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const res = await api.post(`/quizzes/${quiz.quiz_id || id}/submit`, { answers });
      const data = res.data;
      setResult({
        score: data.score,
        isPassed: data.passed,
        correctCount: data.correct_answers,
        totalQ: data.total_questions,
        incorrectCount: data.incorrect_answers,
        skillLevel: data.skill_level,
        mistakes: data.mistakes || [],
        questionsReview: data.questions_review || [],
        message: data.message,
      });
      setSubmitted(true);
      showToast?.(data.message || `Score: ${data.score}%`, data.passed ? "success" : "warning");
    } catch (err) {
      console.error('Quiz submit failed:', err);
      showToast?.("Error submitting quiz. Please try again.", "error");
    } finally {
      setSubmitting(false);
    }
  };

  const handleRetake = () => {
    setSubmitted(false);
    setResult(null);
    setAnswers({});
    setCurrentQuestionIndex(0);
  };

  return (
    <div className="space-y-8 animate-fadeIn max-w-3xl mx-auto font-sans pb-12">
      <div className="flex items-center justify-between border-b border-[#E5E7EB] pb-4">
        <button
          onClick={() => navigate('/quizzes')}
          className="inline-flex items-center gap-2 text-xs font-bold text-[#8E8E93] hover:text-[#0A0A0A]"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Exit Quiz</span>
        </button>
        <span className="text-xs font-bold text-[#0A0A0A] truncate max-w-[300px]">{quiz.title}</span>
      </div>

      {!submitted ? (
        /* Question UI */
        <Card radius="24" className="p-8 space-y-6">
          <div className="space-y-2">
            <div className="flex justify-between text-xs font-semibold text-[#8E8E93]">
              <span>Question {currentQuestionIndex + 1} / {totalQ}</span>
              <span className="font-mono">{Math.round(((currentQuestionIndex + 1) / totalQ) * 100)}%</span>
            </div>
            <ProgressBar value={currentQuestionIndex + 1} max={totalQ} color="dark" />
          </div>

          <div className="space-y-4 pt-2">
            <h2 className="text-xl font-bold text-[#0A0A0A]">
              {currentQ.questionText || currentQ.question}
            </h2>

            <div className="space-y-3 pt-2">
              {currentQ.options.map((opt, idx) => {
                const isSelected = answers[currentQ.id] === idx;
                return (
                  <div
                    key={idx}
                    onClick={() => handleSelectOption(currentQ.id, idx)}
                    className={`p-4 rounded-xl border text-sm font-semibold transition-all cursor-pointer flex items-center justify-between ${
                      isSelected
                        ? 'border-[#0A0A0A] bg-[#F7F8FA] ring-1 ring-[#0A0A0A]'
                        : 'border-[#E5E7EB] bg-white hover:border-[#0A0A0A]'
                    }`}
                  >
                    <span className="text-[#0A0A0A]">{opt}</span>
                    <div className={`w-5 h-5 rounded-full border flex items-center justify-center shrink-0 ${
                      isSelected ? 'bg-[#0A0A0A] border-[#0A0A0A] text-white' : 'border-[#E5E7EB]'
                    }`}>
                      {isSelected && <Check className="w-3 h-3 text-white" />}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="flex items-center justify-between pt-6 border-t border-[#E5E7EB]">
            <Button
              variant="ghost"
              size="sm"
              disabled={currentQuestionIndex === 0}
              onClick={() => setCurrentQuestionIndex(currentQuestionIndex - 1)}
            >
              Previous
            </Button>

            {currentQuestionIndex < totalQ - 1 ? (
              <Button
                variant="primary"
                size="md"
                onClick={() => setCurrentQuestionIndex(currentQuestionIndex + 1)}
              >
                Next
              </Button>
            ) : (
              <Button
                variant="primary"
                size="md"
                loading={submitting}
                onClick={handleSubmit}
              >
                Submit Quiz
              </Button>
            )}
          </div>
        </Card>
      ) : result ? (
        /* Result Screen with Full Review */
        <div className="space-y-6">
          {/* Score Banner */}
          <Card radius="24" className={`p-8 text-center space-y-4 ${
            result.isPassed
              ? 'bg-gradient-to-br from-emerald-50 to-white border border-emerald-200'
              : 'bg-gradient-to-br from-amber-50 to-white border border-amber-200'
          }`}>
            <div className="w-16 h-16 rounded-full mx-auto flex items-center justify-center bg-white shadow-md">
              {result.isPassed
                ? <Award className="w-8 h-8 text-emerald-500" />
                : <XCircle className="w-8 h-8 text-amber-500" />}
            </div>
            <span className="text-5xl font-extrabold text-[#0A0A0A] tracking-tight block">{result.score}%</span>
            <Badge variant={result.isPassed ? 'success' : 'coral'} size="md">
              {result.isPassed ? 'PASSED ✓' : 'NEEDS REVIEW'}
            </Badge>
            <div className="flex items-center justify-center gap-6 text-sm pt-2">
              <div className="text-center">
                <span className="text-2xl font-bold text-emerald-600">{result.correctCount}</span>
                <p className="text-[10px] text-[#8E8E93] font-semibold uppercase">Correct</p>
              </div>
              <div className="w-px h-8 bg-[#E5E7EB]" />
              <div className="text-center">
                <span className="text-2xl font-bold text-rose-500">{result.incorrectCount}</span>
                <p className="text-[10px] text-[#8E8E93] font-semibold uppercase">Incorrect</p>
              </div>
              <div className="w-px h-8 bg-[#E5E7EB]" />
              <div className="text-center">
                <span className="text-2xl font-bold text-[#0A0A0A]">{result.totalQ}</span>
                <p className="text-[10px] text-[#8E8E93] font-semibold uppercase">Total</p>
              </div>
            </div>
            {result.skillLevel && (
              <p className="text-xs text-[#45515E] pt-1">Skill Level Updated: <strong className="text-[#0A0A0A]">{result.skillLevel}</strong></p>
            )}
          </Card>

          {/* Detailed Question Review */}
          {result.questionsReview && result.questionsReview.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-sm font-bold text-[#0A0A0A] uppercase tracking-wider pl-1">Detailed Question Review</h3>
              <div className="space-y-4">
                {result.questionsReview.map((qr, idx) => (
                  <QuestionReviewCard
                    key={qr.id || idx}
                    question={qr}
                    index={idx}
                    userSelection={answers[qr.id || qr.question_id]}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-center gap-3 pt-2">
            <Button variant="secondary" size="md" icon={RotateCcw} onClick={handleRetake}>
              Retake Quiz
            </Button>
            <Button variant="primary" size="md" onClick={() => navigate('/quizzes')}>
              Back to Quizzes
            </Button>
          </div>
        </div>
      ) : null}
    </div>
  );
};
