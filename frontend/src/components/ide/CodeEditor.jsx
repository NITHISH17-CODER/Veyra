import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { Type, WrapText, MapPin } from 'lucide-react';

export const CodeEditor = ({
  code,
  onChange,
  language,
  monacoLanguage,
  readOnly = false
}) => {
  const [isMobile, setIsMobile] = useState(false);
  const [fontSize, setFontSize] = useState(13);
  const [wordWrap, setWordWrap] = useState('on');
  const [showMinimap, setShowMinimap] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      const userAgent = navigator.userAgent || navigator.vendor || window.opera;
      const isMobileBrowser = /android|ipad|iphone|ipod/i.test(userAgent) || window.innerWidth < 768;
      setIsMobile(isMobileBrowser);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const handleEditorChange = (value) => {
    onChange(value || '');
  };

  // Mobile Fallback Textarea Editor
  if (isMobile) {
    return (
      <div className="flex flex-col h-full bg-[#1E1E1E] rounded-xl overflow-hidden border border-white/10">
        <div className="px-3 py-1.5 bg-[#252526] text-[10px] text-white/50 flex justify-between font-mono">
          <span>Mobile Code Editor</span>
          <span>{language}</span>
        </div>
        <textarea
          value={code}
          onChange={(e) => onChange(e.target.value)}
          spellCheck={false}
          readOnly={readOnly}
          className="w-full h-full min-h-[300px] p-3 bg-[#1E1E1E] text-white/90 font-mono text-xs focus:outline-none resize-none leading-relaxed"
        />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-[#1E1E1E] rounded-xl overflow-hidden border border-white/10 shadow-lg">
      {/* Editor Controls Bar */}
      <div className="px-3 py-1.5 bg-[#252526] flex items-center justify-between border-b border-white/10 text-[11px] font-mono text-white/70">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-rose-500/80 inline-block" />
          <span className="w-2.5 h-2.5 rounded-full bg-amber-500/80 inline-block" />
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80 inline-block" />
          <span className="text-white/60 ml-2 font-semibold uppercase tracking-wider">{monacoLanguage || language || 'code'}</span>
        </div>

        <div className="flex items-center gap-3">
          {/* Font Size Selector */}
          <div className="flex items-center gap-1">
            <Type className="w-3.5 h-3.5 text-white/40" />
            <button
              onClick={() => setFontSize((s) => Math.max(11, s - 1))}
              className="px-1 py-0.5 hover:bg-white/10 rounded text-xs"
            >
              -
            </button>
            <span>{fontSize}px</span>
            <button
              onClick={() => setFontSize((s) => Math.min(20, s + 1))}
              className="px-1 py-0.5 hover:bg-white/10 rounded text-xs"
            >
              +
            </button>
          </div>

          {/* Word Wrap Toggle */}
          <button
            onClick={() => setWordWrap((w) => (w === 'on' ? 'off' : 'on'))}
            className={`px-2 py-0.5 rounded text-[10px] font-semibold flex items-center gap-1 transition-colors ${
              wordWrap === 'on' ? 'bg-blue-500/20 text-blue-300' : 'bg-white/5 text-white/40 hover:text-white'
            }`}
          >
            <WrapText className="w-3 h-3" />
            <span>Wrap</span>
          </button>

          {/* Minimap Toggle */}
          <button
            onClick={() => setShowMinimap((m) => !m)}
            className={`px-2 py-0.5 rounded text-[10px] font-semibold flex items-center gap-1 transition-colors ${
              showMinimap ? 'bg-blue-500/20 text-blue-300' : 'bg-white/5 text-white/40 hover:text-white'
            }`}
          >
            <MapPin className="w-3 h-3" />
            <span>Minimap</span>
          </button>
        </div>
      </div>

      {/* Monaco Editor Container */}
      <div className="grow min-h-[350px] relative">
        <Editor
          height="100%"
          language={monacoLanguage || language || 'javascript'}
          theme="vs-dark"
          value={code}
          onChange={handleEditorChange}
          options={{
            fontSize: fontSize,
            wordWrap: wordWrap,
            minimap: { enabled: showMinimap },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 2,
            readOnly: readOnly,
            lineNumbers: 'on',
            folding: true,
            bracketPairColorization: { enabled: true },
            suggestOnTriggerCharacters: true,
            quickSuggestions: true,
            formatOnType: true,
            fontFamily: "'Fira Code', 'Cascadia Code', Consolas, Monaco, monospace",
          }}
          loading={
            <div className="w-full h-full bg-[#1E1E1E] flex items-center justify-center text-xs text-white/50 font-mono">
              Loading Monaco Editor...
            </div>
          }
        />
      </div>
    </div>
  );
};
