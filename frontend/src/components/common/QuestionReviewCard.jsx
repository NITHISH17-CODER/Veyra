import React from 'react';
import { Card } from './Card';
import { CheckCircle2, XCircle, HelpCircle } from 'lucide-react';

export const QuestionReviewCard = ({ question, index, userSelection }) => {
  const options = question.options || [];
  
  // Normalize answer evaluation
  let userIdx = question.user_answer_index;
  if (userIdx === undefined && userSelection !== undefined) {
    if (typeof userSelection === 'number') userIdx = userSelection;
    else if (typeof userSelection === 'string' && !isNaN(parseInt(userSelection, 10))) {
      userIdx = parseInt(userSelection, 10);
    }
  }

  let correctIdx = question.correct_answer_index;

  const isAnswered = question.is_answered !== undefined
    ? question.is_answered
    : (userIdx !== undefined && userIdx !== null && userIdx !== '');

  const isCorrect = question.is_correct !== undefined
    ? question.is_correct
    : (isAnswered && userIdx === correctIdx);

  const status = question.status || (
    !isAnswered ? 'unanswered' : isCorrect ? 'correct' : 'incorrect'
  );

  return (
    <Card
      radius="20"
      className={`p-6 space-y-4 bg-white border transition-all ${
        status === 'correct'
          ? 'border-emerald-200 bg-emerald-50/30'
          : status === 'incorrect'
          ? 'border-rose-200 bg-rose-50/30'
          : 'border-amber-200 bg-amber-50/30'
      }`}
    >
      {/* Question Header & Status Badge */}
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-2.5">
          <span className="text-xs font-mono font-bold text-[#8E8E93] shrink-0 mt-0.5">
            Q{index !== undefined ? index + 1 : question.id}.
          </span>
          <h4 className="text-sm font-extrabold text-[#0A0A0A] leading-snug">
            {question.question_text || question.questionText || question.question}
          </h4>
        </div>

        {status === 'correct' && (
          <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-extrabold flex items-center gap-1.5 shrink-0 border border-emerald-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Correct</span>
          </span>
        )}

        {status === 'incorrect' && (
          <span className="px-3 py-1 rounded-full bg-rose-100 text-rose-800 text-xs font-extrabold flex items-center gap-1.5 shrink-0 border border-rose-300">
            <XCircle className="w-4 h-4 text-rose-600" />
            <span>Incorrect</span>
          </span>
        )}

        {status === 'unanswered' && (
          <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-extrabold flex items-center gap-1.5 shrink-0 border border-amber-300">
            <HelpCircle className="w-4 h-4 text-amber-600" />
            <span>Not Answered</span>
          </span>
        )}
      </div>

      {/* Options Breakdown */}
      <div className="space-y-2 text-xs pt-1">
        {options.map((opt, oIdx) => {
          const isUserChoice = userIdx === oIdx;
          const isCorrectChoice = correctIdx === oIdx;

          let optionStyle = "bg-[#F7F8FA] border-[#E5E7EB] text-[#8E8E93]";
          let badgeText = null;
          let badgeClass = "";

          if (status === 'correct') {
            if (isCorrectChoice) {
              optionStyle = "bg-emerald-100/80 border-emerald-400 text-emerald-950 font-bold shadow-sm ring-1 ring-emerald-400";
              badgeText = "✓ Your Answer (Correct)";
              badgeClass = "bg-emerald-700 text-white";
            }
          } else if (status === 'incorrect') {
            if (isCorrectChoice) {
              optionStyle = "bg-emerald-50 border-emerald-300 text-emerald-900 font-bold";
              badgeText = "✓ Correct Answer";
              badgeClass = "bg-emerald-600 text-white";
            } else if (isUserChoice) {
              optionStyle = "bg-rose-100/90 border-rose-400 text-rose-950 font-bold ring-1 ring-rose-400";
              badgeText = "✗ Your Answer";
              badgeClass = "bg-rose-600 text-white";
            }
          } else if (status === 'unanswered') {
            if (isCorrectChoice) {
              optionStyle = "bg-emerald-50 border-emerald-300 text-emerald-900 font-bold";
              badgeText = "✓ Correct Answer";
              badgeClass = "bg-emerald-600 text-white";
            }
          }

          return (
            <div
              key={oIdx}
              className={`p-3 rounded-xl border flex items-center justify-between transition-all ${optionStyle}`}
            >
              <div className="flex items-center gap-3">
                <span className="w-5 h-5 rounded-full flex items-center justify-center font-bold text-[10px] bg-white border shrink-0">
                  {String.fromCharCode(65 + oIdx)}
                </span>
                <span className="font-semibold text-xs leading-normal">{opt}</span>
              </div>

              {badgeText && (
                <span className={`text-[10px] uppercase font-extrabold px-2.5 py-0.5 rounded-full shrink-0 ${badgeClass}`}>
                  {badgeText}
                </span>
              )}
            </div>
          );
        })}
      </div>

      {/* Explanation Box */}
      {question.explanation && (
        <div className="p-3.5 rounded-xl bg-white/80 border border-[#E5E7EB] text-xs text-slate-700 space-y-1 mt-2">
          <strong className="text-[#0A0A0A] font-bold block flex items-center gap-1">
            <span>💡 Explanation:</span>
          </strong>
          <p className="leading-relaxed text-[#45515E]">{question.explanation}</p>
        </div>
      )}
    </Card>
  );
};
