import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import api from '../services/api';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { LoadingState } from '../components/common/LoadingState';
import { ArrowRight, CheckCircle2, Clock, Award, Sparkles, AlertCircle, RefreshCw } from 'lucide-react';

export const AssessmentsPage = () => {
  const { user } = useApp();
  const navigate = useNavigate();
  const [quizData, setQuizData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchQuizzes = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('/quizzes');
      setQuizData(res.data);
    } catch (err) {
      console.error("Failed to fetch quizzes:", err);
      setError("Failed to load quizzes. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuizzes();
  }, []);

  const quizzes = quizData?.quizzes || [];
  const courseTitle = quizData?.course_title || user?.targetGoal || "Your Course";

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-5xl mx-auto">
      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">QUIZZES</span>
          <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-[#0A0A0A] text-white flex items-center gap-1">
            <Sparkles className="w-3 h-3" /> {courseTitle}
          </span>
        </div>
        <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">Course Quizzes</h1>
        <p className="text-sm text-[#45515E]">
          {quizzes.length} quizzes personalized for your <strong>{courseTitle}</strong> track. Each quiz has 10 questions loaded from the database.
        </p>
      </div>

      {loading ? (
        <LoadingState message="Loading your course quizzes..." />
      ) : error ? (
        <Card radius="20" className="p-8 text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-red-400 mx-auto" />
          <h3 className="text-lg font-bold text-[#0A0A0A]">{error}</h3>
          <Button variant="outline" size="sm" icon={RefreshCw} onClick={fetchQuizzes}>
            Retry
          </Button>
        </Card>
      ) : quizzes.length === 0 ? (
        <Card radius="20" className="p-8 text-center space-y-4">
          <Award className="w-12 h-12 text-[#8E8E93] mx-auto" />
          <h3 className="text-lg font-bold text-[#0A0A0A]">No quizzes found for your course</h3>
          <p className="text-sm text-[#45515E]">Quizzes will appear once the database is seeded for your course.</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {quizzes.map((quiz) => {
            const isCompleted = quiz.status === 'Completed';
            const isAttempted = quiz.status === 'Attempted';

            return (
              <Card key={quiz.id} radius="20" className={`p-6 space-y-4 flex flex-col justify-between border transition-all ${
                isCompleted ? 'border-emerald-200 bg-emerald-50/30' : 'border-[#E5E7EB] hover:border-[#0A0A0A]'
              }`}>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <Badge variant={isCompleted ? 'success' : isAttempted ? 'blue' : 'dark'}>
                      Quiz {quiz.quiz_number}
                    </Badge>
                    <div className="flex items-center gap-2 text-xs text-[#8E8E93]">
                      <Clock className="w-3 h-3" />
                      <span>{quiz.timeMinutes} min</span>
                      <span className="font-mono">• {quiz.questionCount} Q</span>
                    </div>
                  </div>

                  <h3 className="text-lg font-bold text-[#0A0A0A] leading-snug">{quiz.title}</h3>
                  <p className="text-xs text-[#45515E] line-clamp-2">{quiz.description || "Course knowledge evaluation."}</p>

                  {quiz.best_score !== null && quiz.best_score !== undefined && (
                    <div className="flex items-center gap-2 pt-1">
                      <span className="text-[10px] font-semibold text-[#8E8E93] uppercase">Best Score:</span>
                      <span className={`text-sm font-bold ${quiz.passed ? 'text-emerald-600' : 'text-amber-600'}`}>
                        {quiz.best_score}%
                      </span>
                      {quiz.passed && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />}
                    </div>
                  )}
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-[#E5E7EB]">
                  <span className={`text-xs font-semibold ${
                    isCompleted ? 'text-emerald-600' : isAttempted ? 'text-blue-600' : 'text-[#8E8E93]'
                  }`}>
                    {isCompleted ? '✓ Passed' : isAttempted ? '● Attempted' : 'Available'}
                  </span>

                  <Button
                    variant={isCompleted ? 'outline' : 'primary'}
                    size="sm"
                    icon={ArrowRight}
                    iconPosition="right"
                    onClick={() => navigate(`/quizzes/${quiz.quiz_id}`)}
                  >
                    {isCompleted ? 'Retake' : isAttempted ? 'Try Again' : 'Start Quiz'}
                  </Button>
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
