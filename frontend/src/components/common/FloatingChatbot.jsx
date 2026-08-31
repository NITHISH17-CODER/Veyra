import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useApp } from '../../context/AppContext';
import { chatService } from '../../services/chatService';
import {
  Bot,
  Send,
  X,
  ChevronDown,
  Minimize2,
  Maximize2,
  RotateCcw,
  Copy,
  Check,
  ArrowRight,
  MessageSquare,
  Sparkles,
  Loader2,
  GripVertical,
} from 'lucide-react';

// ── Quick action prompts shown in the widget ───────────────────────────────
const QUICK_PROMPTS = [
  "What should I learn next?",
  "Show my progress",
  "Career advice",
  "Help me navigate",
];

// ── Markdown-like text renderer (bold, bullets) ────────────────────────────
const RichText = ({ text }) => {
  if (!text) return null;
  const lines = text.split('\n');
  return (
    <div className="space-y-1">
      {lines.map((line, i) => {
        // Bold via **text**
        const parts = line.split(/(\*\*[^*]+\*\*)/g);
        const rendered = parts.map((p, j) =>
          p.startsWith('**') && p.endsWith('**')
            ? <strong key={j} className="font-bold text-[#0A0A0A]">{p.slice(2, -2)}</strong>
            : <span key={j}>{p}</span>
        );
        // Bullet line
        if (line.startsWith('•') || line.startsWith('-') || line.startsWith('   •')) {
          return (
            <div key={i} className="flex gap-1.5 items-start">
              <span className="mt-0.5 shrink-0 text-[#1D70EF] font-bold">•</span>
              <p className="leading-relaxed">{rendered}</p>
            </div>
          );
        }
        // Emoji lines (tips, etc.)
        if (/^[🚀⚡🏁📌🎯💡🧠🎉👍💪🌱✅📚🔥🎓💼🏆📝📖📊⭐]/.test(line)) {
          return <p key={i} className="leading-relaxed">{rendered}</p>;
        }
        if (line === '') return <div key={i} className="h-1" />;
        return <p key={i} className="leading-relaxed">{rendered}</p>;
      })}
    </div>
  );
};

// ── Single Message Bubble ──────────────────────────────────────────────────
const MessageBubble = ({ msg, onSuggestionClick, onNavigate, onCopy, copiedId }) => {
  const isAi = msg.sender === 'ai';

  return (
    <div className={`flex gap-2.5 items-end ${isAi ? '' : 'flex-row-reverse'}`}>
      {/* Avatar */}
      {isAi && (
        <div className="w-7 h-7 rounded-full bg-[#1D70EF] text-white flex items-center justify-center shrink-0 mb-0.5 shadow-sm">
          <Bot className="w-4 h-4" />
        </div>
      )}

      <div className={`flex flex-col gap-1.5 max-w-[85%] ${isAi ? '' : 'items-end'}`}>
        {/* Bubble */}
        <div
          className={`px-4 py-3 rounded-2xl text-xs leading-relaxed ${
            isAi
              ? 'bg-white border border-[#DBEAFE] text-[#0A0A0A] rounded-bl-xs shadow-sm'
              : 'bg-[#1D70EF] text-white font-medium rounded-br-xs shadow-sm'
          }`}
        >
          {isAi ? <RichText text={msg.content} /> : <p>{msg.content}</p>}
        </div>

        {/* Timestamp + copy */}
        <div className={`flex items-center gap-2 px-1 ${isAi ? '' : 'flex-row-reverse'}`}>
          <span className="text-[10px] text-slate-400 font-medium">{msg.timestamp}</span>
          {isAi && (
            <button
              onClick={() => onCopy(msg.id, msg.content)}
              className="text-slate-400 hover:text-slate-600 transition-colors p-0.5 rounded"
              title="Copy response"
            >
              {copiedId === msg.id
                ? <Check className="w-3 h-3 text-emerald-600" />
                : <Copy className="w-3 h-3" />}
            </button>
          )}
        </div>

        {/* Navigate button */}
        {isAi && msg.navigateTo && (
          <button
            onClick={() => onNavigate(msg.navigateTo)}
            className="self-start flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#1D70EF] hover:bg-[#1456F0] text-white text-xs font-bold transition-all shadow-sm active:scale-95"
          >
            <ArrowRight className="w-3.5 h-3.5" />
            Go to page
          </button>
        )}

        {/* Suggestion chips */}
        {isAi && msg.suggestions && msg.suggestions.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-1">
            {msg.suggestions.map((s) => (
              <button
                key={s}
                onClick={() => onSuggestionClick(s)}
                className="px-3 py-1 rounded-full bg-[#EFF6FF] hover:bg-[#DBEAFE] border border-[#BFDBFE] text-[#1D70EF] text-xs font-semibold transition-colors text-left"
              >
                {s}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// ── Typing Indicator ───────────────────────────────────────────────────────
const TypingIndicator = () => (
  <div className="flex gap-2.5 items-end">
    <div className="w-7 h-7 rounded-full bg-[#1D70EF] text-white flex items-center justify-center shrink-0 mb-0.5 shadow-sm">
      <Bot className="w-4 h-4" />
    </div>
    <div className="px-4 py-3 rounded-2xl rounded-bl-xs bg-white border border-[#DBEAFE] shadow-sm flex items-center gap-1.5">
      <span className="w-1.5 h-1.5 rounded-full bg-[#1D70EF] animate-bounce" style={{ animationDelay: '0ms' }} />
      <span className="w-1.5 h-1.5 rounded-full bg-[#1D70EF] animate-bounce" style={{ animationDelay: '150ms' }} />
      <span className="w-1.5 h-1.5 rounded-full bg-[#1D70EF] animate-bounce" style={{ animationDelay: '300ms' }} />
      <span className="text-[11px] font-medium text-slate-500 ml-1">Veyra AI is thinking...</span>
    </div>
  </div>
);

// ── Main FloatingChatbot Component ─────────────────────────────────────────
export const FloatingChatbot = () => {
  const { user, roadmap } = useApp();
  const navigate = useNavigate();
  const location = useLocation();

  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const [unreadCount, setUnreadCount] = useState(0);
  const [hasInitialized, setHasInitialized] = useState(false);

  // Draggable Floating Action Button Position State
  const [dragPos, setDragPos] = useState({ x: 0, y: 0 });
  const isDraggingRef = useRef(false);
  const dragStartRef = useRef({ mouseX: 0, mouseY: 0, startX: 0, startY: 0 });
  const hasMovedRef = useRef(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Scroll to bottom on new messages
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
      setUnreadCount(0);
    }
  }, [messages, isTyping, isOpen, scrollToBottom]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen && !isMinimized) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen, isMinimized]);

  // Initialize welcome message with Veyra AI branding
  useEffect(() => {
    if (user && !hasInitialized) {
      const goal = user.targetGoal || roadmap?.career || 'your career goal';
      const course = roadmap?.courses?.[0]?.name || null;
      setMessages([
        {
          id: 'welcome',
          sender: 'ai',
          timestamp: 'Just now',
          content: `Hi ${user.name || 'there'}! 👋 I am your **Veyra AI Assistant**.\n\nI know your learning journey toward **${goal}**${course ? ` and your active course **${course}**` : ''}. Ask me anything about your progress, courses, skills, quizzes, or what to learn next!`,
          suggestions: ['What should I learn next?', 'Show my progress', 'Career advice'],
          navigateTo: null,
        },
      ]);
      setHasInitialized(true);
    }
  }, [user, roadmap, hasInitialized]);

  // Get current page context to send to backend
  const getPageContext = useCallback(() => {
    const pageName = location.pathname.split('/')[1] || 'dashboard';
    return {
      page: pageName,
      url: location.pathname,
      params: Object.fromEntries(new URLSearchParams(location.search)),
    };
  }, [location]);

  // Send a message
  const handleSend = async (text) => {
    const msgText = (text || inputValue).trim();
    if (!msgText || isTyping) return;

    const userMsg = {
      id: `u-${Date.now()}`,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      content: msgText,
    };

    setMessages(prev => [...prev, userMsg]);
    setInputValue('');
    setIsTyping(true);

    try {
      const history = messages.slice(-8).map(m => ({ role: m.sender === 'ai' ? 'assistant' : 'user', content: m.content }));
      const response = await chatService.sendMessage(msgText, history, getPageContext());
      setIsTyping(false);
      setMessages(prev => [...prev, {
        ...response,
        id: response.id || `ai-${Date.now()}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }]);
      if (!isOpen) setUnreadCount(prev => prev + 1);
    } catch {
      setIsTyping(false);
      setMessages(prev => [...prev, {
        id: `err-${Date.now()}`,
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        content: "I'm having trouble connecting right now. Please try again in a moment! 🔄",
        suggestions: [],
        navigateTo: null,
      }]);
    }
  };

  // Navigate and close chat
  const handleNavigate = (route) => {
    navigate(route);
    setIsOpen(false);
  };

  // Copy message
  const handleCopy = (id, content) => {
    navigator.clipboard.writeText(content);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Reset conversation
  const handleReset = () => {
    const goal = user?.targetGoal || roadmap?.career || 'your career goal';
    setMessages([
      {
        id: `reset-${Date.now()}`,
        sender: 'ai',
        timestamp: 'Just now',
        content: `Hi again, **${user?.name || 'there'}**! 👋 Fresh start — how can Veyra AI assist your learning path today?\n\nTarget Goal: **${goal}**`,
        suggestions: ['What should I learn next?', 'Show my progress', 'Career advice'],
        navigateTo: null,
      },
    ]);
  };

  // Handle enter key in input
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // ── Drag Logic for Floating Button ─────────────────────────────────────────
  const handleMouseDown = (e) => {
    if (e.button !== 0) return; // Only left click
    isDraggingRef.current = true;
    hasMovedRef.current = false;
    dragStartRef.current = {
      mouseX: e.clientX,
      mouseY: e.clientY,
      startX: dragPos.x,
      startY: dragPos.y,
    };
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  };

  const handleMouseMove = (e) => {
    if (!isDraggingRef.current) return;
    const dx = e.clientX - dragStartRef.current.mouseX;
    const dy = e.clientY - dragStartRef.current.mouseY;
    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
      hasMovedRef.current = true;
    }
    setDragPos({
      x: dragStartRef.current.startX + dx,
      y: dragStartRef.current.startY + dy,
    });
  };

  const handleMouseUp = () => {
    isDraggingRef.current = false;
    window.removeEventListener('mousemove', handleMouseMove);
    window.removeEventListener('mouseup', handleMouseUp);
  };

  const handleFabClick = (e) => {
    if (hasMovedRef.current) {
      e.preventDefault();
      e.stopPropagation();
      return;
    }
    setIsOpen(true);
    setIsMinimized(false);
  };

  // Touch drag support
  const handleTouchStart = (e) => {
    const touch = e.touches[0];
    isDraggingRef.current = true;
    hasMovedRef.current = false;
    dragStartRef.current = {
      mouseX: touch.clientX,
      mouseY: touch.clientY,
      startX: dragPos.x,
      startY: dragPos.y,
    };
    window.addEventListener('touchmove', handleTouchMove);
    window.addEventListener('touchend', handleTouchEnd);
  };

  const handleTouchMove = (e) => {
    if (!isDraggingRef.current) return;
    const touch = e.touches[0];
    const dx = touch.clientX - dragStartRef.current.mouseX;
    const dy = touch.clientY - dragStartRef.current.mouseY;
    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
      hasMovedRef.current = true;
    }
    setDragPos({
      x: dragStartRef.current.startX + dx,
      y: dragStartRef.current.startY + dy,
    });
  };

  const handleTouchEnd = () => {
    isDraggingRef.current = false;
    window.removeEventListener('touchmove', handleTouchMove);
    window.removeEventListener('touchend', handleTouchEnd);
  };

  // Don't render on unauthenticated pages
  if (!user) return null;

  // ── Widget Responsive Dimensions ──────────────────────────────────────────
  const widgetWidth = isExpanded ? 'w-full sm:w-[440px]' : 'w-full sm:w-[360px]';
  const widgetHeight = isExpanded ? 'h-[85vh] sm:h-[580px]' : 'h-[80vh] sm:h-[490px]';

  return (
    <>
      {/* ── Floating Action Button (Veyra Primary Blue & Draggable) ───────────── */}
      {!isOpen && (
        <div
          id="chatbot-fab-container"
          className="fixed bottom-6 right-6 z-50 touch-none"
          style={{
            transform: `translate(${dragPos.x}px, ${dragPos.y}px)`,
          }}
        >
          <button
            id="chatbot-fab"
            onMouseDown={handleMouseDown}
            onTouchStart={handleTouchStart}
            onClick={handleFabClick}
            className="relative w-14 h-14 rounded-full bg-[#1D70EF] hover:bg-[#1456F0] text-white shadow-xl shadow-blue-500/30 hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center group cursor-grab active:cursor-grabbing"
            title="Veyra AI Assistant"
            aria-label="Open Veyra AI Assistant"
          >
            <Bot className="w-6 h-6 group-hover:scale-110 transition-transform" />

            {/* Unread badge */}
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-red-500 text-white text-[10px] font-bold flex items-center justify-center shadow-md animate-bounce">
                {unreadCount}
              </span>
            )}
            {/* Soft pulsing ring */}
            <span className="absolute inset-0 rounded-full bg-[#1D70EF] animate-ping opacity-20 pointer-events-none" />
          </button>
        </div>
      )}

      {/* ── Chat Widget Panel (Veyra Native White + Blue SaaS Identity) ──────── */}
      {isOpen && (
        <div
          id="chatbot-widget"
          className={`fixed bottom-0 right-0 sm:bottom-6 sm:right-6 z-50 ${widgetWidth} ${isMinimized ? 'h-auto' : widgetHeight} flex flex-col bg-white rounded-t-3xl sm:rounded-3xl overflow-hidden shadow-2xl border border-[#DBEAFE] transition-all duration-300 origin-bottom-right animate-scaleIn max-w-full`}
          style={{ boxShadow: '0 20px 50px rgba(29,112,239,0.18), 0 8px 24px rgba(0,0,0,0.08)' }}
        >
          {/* ── Header (Veyra Blue Gradient) ─────────────────────────────────── */}
          <div className="flex items-center justify-between px-4 py-3 bg-gradient-to-r from-[#1D70EF] via-[#1456F0] to-[#1D70EF] text-white shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-white/20 backdrop-blur-md flex items-center justify-center border border-white/20 shadow-sm shrink-0">
                <img src="/veyra-logo.png" alt="Veyra Logo" className="w-5 h-5 rounded object-contain" />
              </div>
              <div>
                <p className="text-sm font-bold leading-tight tracking-tight flex items-center gap-1.5">
                  Veyra AI
                  <span className="text-[10px] font-extrabold px-1.5 py-0.2 rounded bg-white/20 text-white">PRO</span>
                </p>
                <p className="text-[10px] text-blue-100 leading-tight flex items-center gap-1 mt-0.5">
                  {isTyping ? (
                    <span className="flex items-center gap-1 font-medium">
                      <Loader2 className="w-2.5 h-2.5 animate-spin text-white" />
                      Thinking...
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 font-medium">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
                      Online & Ready
                    </span>
                  )}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1">
              <button
                onClick={handleReset}
                className="w-7 h-7 rounded-lg hover:bg-white/20 flex items-center justify-center transition-colors text-white"
                title="Reset conversation"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setIsExpanded(v => !v)}
                className="w-7 h-7 rounded-lg hover:bg-white/20 hidden sm:flex items-center justify-center transition-colors text-white"
                title={isExpanded ? 'Shrink' : 'Expand'}
              >
                {isExpanded ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
              </button>
              <button
                onClick={() => setIsMinimized(v => !v)}
                className="w-7 h-7 rounded-lg hover:bg-white/20 flex items-center justify-center transition-colors text-white"
                title={isMinimized ? 'Expand' : 'Minimize'}
              >
                <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isMinimized ? 'rotate-180' : ''}`} />
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="w-7 h-7 rounded-lg hover:bg-white/20 flex items-center justify-center transition-colors text-white"
                title="Close"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Context Strip */}
          {!isMinimized && user?.targetGoal && (
            <div className="flex items-center gap-2 px-3.5 py-1.5 bg-[#EFF6FF] border-b border-[#DBEAFE] shrink-0">
              <Sparkles className="w-3.5 h-3.5 text-[#1D70EF] shrink-0" />
              <p className="text-[11px] text-[#1D70EF] font-medium truncate">
                Target: <strong>{user.targetGoal}</strong>
                {user.streakDays ? ` · 🔥 ${user.streakDays} day streak` : ''}
              </p>
            </div>
          )}

          {/* ── Messages Area ───────────────────────────────────────────────── */}
          {!isMinimized && (
            <>
              <div className="flex-1 overflow-y-auto px-3.5 py-4 space-y-3.5 bg-[#F8FAFC]">
                {messages.map(msg => (
                  <MessageBubble
                    key={msg.id}
                    msg={msg}
                    onSuggestionClick={(s) => handleSend(s)}
                    onNavigate={handleNavigate}
                    onCopy={handleCopy}
                    copiedId={copiedId}
                  />
                ))}
                {isTyping && <TypingIndicator />}
                <div ref={messagesEndRef} />
              </div>

              {/* ── Quick Prompts ────────────────────────────────────────────── */}
              <div className="px-3.5 py-2 bg-white border-t border-[#E2E8F0] flex items-center gap-1.5 overflow-x-auto shrink-0 scrollbar-none">
                <MessageSquare className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                {QUICK_PROMPTS.map(p => (
                  <button
                    key={p}
                    onClick={() => handleSend(p)}
                    className="shrink-0 px-2.5 py-1 rounded-full bg-[#EFF6FF] hover:bg-[#DBEAFE] border border-[#BFDBFE] text-[#1D70EF] text-[11px] font-semibold whitespace-nowrap transition-colors"
                  >
                    {p}
                  </button>
                ))}
              </div>

              {/* ── Input Bar ───────────────────────────────────────────────── */}
              <div className="px-3.5 py-2.5 bg-white border-t border-[#E2E8F0] shrink-0">
                <div className="flex items-center gap-2 bg-[#F8FAFC] rounded-2xl border border-[#DBEAFE] focus-within:border-[#1D70EF] focus-within:ring-2 focus-within:ring-[#1D70EF]/20 transition-all px-3.5 py-2">
                  <input
                    ref={inputRef}
                    type="text"
                    value={inputValue}
                    onChange={e => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask Veyra AI about your learning path..."
                    className="flex-1 bg-transparent text-xs text-[#0A0A0A] font-medium placeholder-slate-400 outline-none min-w-0"
                    disabled={isTyping}
                    id="chatbot-input"
                  />
                  <button
                    onClick={() => handleSend()}
                    disabled={!inputValue.trim() || isTyping}
                    className="w-7 h-7 rounded-xl bg-[#1D70EF] hover:bg-[#1456F0] disabled:opacity-40 disabled:cursor-not-allowed text-white flex items-center justify-center transition-all shrink-0 shadow-sm active:scale-95"
                    aria-label="Send message to Veyra AI"
                  >
                    {isTyping
                      ? <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      : <Send className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </>
  );
};

