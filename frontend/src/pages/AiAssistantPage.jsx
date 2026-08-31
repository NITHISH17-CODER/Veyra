import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { chatService } from '../services/chatService';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import {
  Bot,
  Send,
  Sparkles,
  User,
  Copy,
  RotateCcw,
  Check,
  MessageSquare,
  Plus,
  PlayCircle,
  Target
} from 'lucide-react';

export const AiAssistantPage = () => {
  const { user, roadmap, showToast } = useApp();
  const navigate = useNavigate();
  const [messages, setMessages] = useState(() => [
    {
      id: 'welcome-1',
      sender: 'ai',
      timestamp: 'Just now',
      content: `Hello ${user?.name || 'there'}! I am your **Veyra AI Assistant**.\n\nI can help you explore learning topics, clarify course concepts, prepare for quizzes, or adjust your career roadmap. What would you like to work on today?`
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);

  const messagesEndRef = useRef(null);

  const suggestedActionPrompts = [
    "What should I learn today?",
    "Why am I learning Statistics?",
    "Can I skip this topic?",
    "What project should I build next?",
    "How close am I to my goal?"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userText = inputMessage;
    const userMsg = { id: Date.now(), role: 'user', content: userText };
    setMessages(prev => [...prev, userMsg]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const res = await chatService.sendMessage(userText);
      const aiMsg = { id: Date.now() + 1, role: 'ai', content: res.reply || res.response || "I am here to help you on Veyra." };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { id: Date.now() + 1, role: 'ai', content: "I'm having trouble connecting to Veyra services right now. Please try again." }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = (id, content) => {
    navigator.clipboard.writeText(content);
    setCopiedId(id);
    showToast("Response copied to clipboard", "info");
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="h-[calc(100vh-7rem)] flex flex-col gap-4 animate-fadeIn font-sans">
      {/* 1. GREETING & CONTEXT BANNER */}
      <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-r from-[#1D70EF] via-[#1456F0] to-[#1D70EF] border border-[#1D70EF] text-white flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shrink-0 shadow-md">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-md text-white flex items-center justify-center shrink-0 border border-white/20">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
              Hi {user?.name || "Learner"} 👋
              <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-white/20 text-white">VEYRA AI</span>
            </h1>
            <p className="text-xs text-blue-100 mt-0.5">
              Goal: <strong className="text-white">{user?.targetGoal || roadmap?.career || "Complete onboarding to set your goal"}</strong>
            </p>
          </div>
        </div>

        {/* QUICK SUGGESTED ACTION PILLS */}
        <div className="flex flex-wrap items-center gap-1.5 w-full sm:w-auto">
          {suggestedActionPrompts.slice(0, 3).map((prompt) => (
            <button
              key={prompt}
              onClick={() => handleSend(prompt)}
              className="px-3 py-1 rounded-full bg-white/20 hover:bg-white/30 border border-white/30 text-xs text-white font-semibold transition-all"
            >
              {prompt}
            </button>
          ))}
        </div>
      </div>

      {/* 2. CHAT STREAM CONTAINER */}
      <Card className="flex-1 flex flex-col p-0 overflow-hidden border-[#DBEAFE] bg-white">
        {/* Scrollable Message List */}
        <div className="flex-1 p-4 sm:p-6 overflow-y-auto space-y-6 bg-[#F8FAFC]">
          {messages.map((msg) => {
            const isAi = msg.sender === 'ai' || msg.role === 'ai';
            return (
              <div
                key={msg.id}
                className={`flex items-start gap-3 ${isAi ? '' : 'flex-row-reverse'}`}
              >
                <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 ${
                  isAi ? 'bg-[#1D70EF] text-white shadow-sm' : 'bg-[#0A0A0A] text-white shadow-sm'
                }`}>
                  {isAi ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
                </div>

                <div className={`max-w-2xl space-y-2 ${isAi ? '' : 'text-right'}`}>
                  <div className="flex items-center gap-2 text-[10px] text-slate-500 font-medium">
                    <span className="font-bold text-[#0A0A0A]">{isAi ? 'Veyra AI Assistant' : user?.name}</span>
                    <span>• {msg.timestamp || 'Just now'}</span>
                  </div>

                  <div className={`p-4 rounded-2xl text-xs leading-relaxed text-left space-y-3 whitespace-pre-line ${
                    isAi
                      ? 'bg-white border border-[#DBEAFE] text-[#0A0A0A] shadow-sm'
                      : 'bg-[#1D70EF] text-white font-medium shadow-sm'
                  }`}>
                    {msg.content}
                  </div>

                  {/* AI Response Tools & Action Buttons */}
                  {isAi && (
                    <div className="space-y-3 pt-1">
                      <div className="flex items-center justify-between">
                        <button
                          onClick={() => handleCopy(msg.id, msg.content)}
                          className="text-[10px] text-slate-500 hover:text-[#1D70EF] flex items-center gap-1 px-2.5 py-1 rounded-lg bg-[#EFF6FF] border border-[#BFDBFE] font-semibold transition-colors"
                        >
                          {copiedId === msg.id ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
                          <span>{copiedId === msg.id ? 'Copied' : 'Copy Response'}</span>
                        </button>
                      </div>

                      {/* Suggested Prompts */}
                      {msg.suggestions?.length > 0 && (
                        <div className="space-y-1.5 pt-1">
                          <span className="text-[10px] text-slate-500 uppercase tracking-wider font-extrabold block">Follow-ups:</span>
                          <div className="flex flex-wrap gap-1.5">
                            {msg.suggestions.map((sugg) => (
                              <button
                                key={sugg}
                                onClick={() => handleSend(sugg)}
                                className="px-3 py-1.5 rounded-full bg-[#EFF6FF] hover:bg-[#DBEAFE] border border-[#BFDBFE] text-xs text-[#1D70EF] font-semibold transition-all text-left"
                              >
                                {sugg}
                              </button>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            );
          })}

          {/* Typing Indicator */}
          {isLoading && (
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-xl bg-[#1D70EF] flex items-center justify-center text-white shadow-sm">
                <Bot className="w-4 h-4" />
              </div>
              <div className="p-3.5 rounded-2xl bg-white border border-[#DBEAFE] flex items-center gap-2 shadow-sm">
                <span className="w-2 h-2 rounded-full bg-[#1D70EF] animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 rounded-full bg-[#1D70EF] animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 rounded-full bg-[#1D70EF] animate-bounce" style={{ animationDelay: '300ms' }} />
                <span className="text-xs text-slate-500 font-medium ml-1">Veyra AI is analyzing...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Action Pills Row above input */}
        <div className="px-4 py-2 bg-[#F8FAFC] border-t border-[#DBEAFE] flex items-center gap-2 overflow-x-auto">
          <span className="text-[10px] font-bold text-slate-500 uppercase shrink-0">Ask Veyra AI:</span>
          {suggestedActionPrompts.map((prompt) => (
            <button
              key={prompt}
              onClick={() => handleSend(prompt)}
              className="px-3 py-1 rounded-full bg-white hover:bg-[#EFF6FF] border border-[#BFDBFE] text-[11px] text-[#1D70EF] font-semibold whitespace-nowrap transition-colors"
            >
              {prompt}
            </button>
          ))}
        </div>

        {/* Chat Input Bar */}
        <div className="p-3 border-t border-[#DBEAFE] bg-white">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-3"
          >
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask anything about your path, skills, or career goals..."
              className="flex-1 bg-[#F8FAFC] border border-[#DBEAFE] rounded-xl px-4 py-2.5 text-xs text-[#0A0A0A] placeholder-slate-400 focus:outline-none focus:border-[#1D70EF] focus:ring-2 focus:ring-[#1D70EF]/20"
            />
            <Button
              type="submit"
              variant="primary"
              size="sm"
              disabled={!inputMessage.trim() || isLoading}
              icon={Send}
              className="bg-[#1D70EF] hover:bg-[#1456F0] font-bold text-white shadow-sm"
            >
              Send
            </Button>
          </form>
        </div>
      </Card>
    </div>
  );
};
