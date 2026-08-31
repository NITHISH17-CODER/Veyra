import React, { useState, useEffect, useRef } from 'react';
import { codeExecutionService } from '../../services/codeExecutionService';
import { LanguageSelector } from './LanguageSelector';
import { VersionSelector } from './VersionSelector';
import { ExecutionStatus } from './ExecutionStatus';
import { CodeRunner } from './CodeRunner';
import { CodeEditor } from './CodeEditor';
import { InputPanel } from './InputPanel';
import { OutputPanel } from './OutputPanel';
import { LivePreview } from './LivePreview';
import { Sparkles, Terminal, Eye, AlertCircle } from 'lucide-react';

export const CodeIDE = ({
  lessonId,
  starterCode,
  defaultLanguage,
  defaultVersion,
  codingInstructions
}) => {
  const [languages, setLanguages] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState(null);
  const [selectedVersion, setSelectedVersion] = useState('');
  const [code, setCode] = useState(starterCode || '');
  const [stdin, setStdin] = useState('');
  const [executionResult, setExecutionResult] = useState(null);
  const [status, setStatus] = useState('ready'); // ready, running, completed, error, timeout
  const [isSaving, setIsSaving] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showResetModal, setShowResetModal] = useState(false);
  const [activeTab, setActiveTab] = useState('editor'); // 'editor', 'stdin', 'output', 'preview'

  const autosaveTimerRef = useRef(null);
  const initialCodeRef = useRef(starterCode || '');

  // 1. Fetch available languages from backend
  useEffect(() => {
    const fetchLangs = async () => {
      try {
        const list = await codeExecutionService.getLanguages();
        setLanguages(list);

        // Match default language
        const match = list.find(
          (l) => l.key === (defaultLanguage || 'python').toLowerCase() || l.language.toLowerCase() === (defaultLanguage || 'python').toLowerCase()
        ) || list[0];

        setSelectedLanguage(match);
        if (match) {
          setSelectedVersion(defaultVersion || match.defaultVersion);
        }
      } catch (err) {
        console.error('Failed to load compiler languages:', err);
      }
    };
    fetchLangs();
  }, [defaultLanguage, defaultVersion]);

  // 2. Fetch user's saved code for this lesson if available
  useEffect(() => {
    if (!lessonId) return;
    const fetchSaved = async () => {
      try {
        const res = await codeExecutionService.getSavedCode(lessonId);
        if (res.has_saved_code && res.code) {
          setCode(res.code);
          if (res.stdin) setStdin(res.stdin);
          if (res.language && languages.length > 0) {
            const langObj = languages.find((l) => l.key === res.language);
            if (langObj) {
              setSelectedLanguage(langObj);
              if (res.version) setSelectedVersion(res.version);
            }
          }
        }
      } catch (err) {
        console.error('Failed to fetch saved code:', err);
      }
    };
    fetchSaved();
  }, [lessonId, languages]);

  // 3. Debounced Autosave (1.5s inactivity)
  useEffect(() => {
    if (!lessonId || !selectedLanguage) return;
    if (autosaveTimerRef.current) clearTimeout(autosaveTimerRef.current);

    autosaveTimerRef.current = setTimeout(async () => {
      try {
        await codeExecutionService.saveCode(lessonId, {
          language: selectedLanguage.key,
          version: selectedVersion,
          code,
          stdin
        });
        setIsSaved(true);
        setTimeout(() => setIsSaved(false), 2000);
      } catch (e) {
        // Silent background save
      }
    }, 1500);

    return () => {
      if (autosaveTimerRef.current) clearTimeout(autosaveTimerRef.current);
    };
  }, [code, stdin, selectedLanguage, selectedVersion, lessonId]);

  // 4. Run Code handler
  const handleRun = async () => {
    if (!selectedLanguage) return;
    setStatus('running');
    setExecutionResult(null);

    if (selectedLanguage.isLivePreview) {
      setStatus('completed');
      setActiveTab('preview');
      return;
    }

    try {
      const res = await codeExecutionService.executeCode({
        lessonId,
        language: selectedLanguage.key,
        version: selectedVersion,
        sourceCode: code,
        stdin
      });

      setExecutionResult(res);
      setStatus(res.status || 'completed');
      setActiveTab('output');
    } catch (err) {
      console.error('Code execution failed:', err);
      const errMsg = err.response?.data?.detail || 'Execution error occurred.';
      setExecutionResult({
        status: 'error',
        stdout: '',
        stderr: errMsg,
        exitCode: 1,
        executionTime: 0.0
      });
      setStatus('error');
      setActiveTab('output');
    }
  };

  // 5. Manual Save handler
  const handleManualSave = async () => {
    if (!lessonId || !selectedLanguage) return;
    setIsSaving(true);
    try {
      await codeExecutionService.saveCode(lessonId, {
        language: selectedLanguage.key,
        version: selectedVersion,
        code,
        stdin
      });
      setIsSaved(true);
      setTimeout(() => setIsSaved(false), 2500);
    } catch (err) {
      console.error('Save failed:', err);
    } finally {
      setIsSaving(false);
    }
  };

  // 6. Reset handler
  const handleConfirmReset = () => {
    setCode(initialCodeRef.current);
    setExecutionResult(null);
    setStatus('ready');
    setShowResetModal(false);
  };

  return (
    <div
      className={`bg-[#141414] text-white rounded-2xl border border-white/10 overflow-hidden flex flex-col font-sans shadow-2xl transition-all ${
        isFullscreen ? 'fixed inset-4 z-50 rounded-2xl' : 'w-full h-full min-h-[550px]'
      }`}
    >
      {/* IDE HEADER */}
      <div className="bg-[#1C1C1E] px-4 py-3 border-b border-white/10 flex flex-wrap items-center justify-between gap-3 shrink-0">
        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-2">
            <img src="/veyra-logo.png" alt="Veyra" className="w-4 h-4 rounded object-contain shrink-0" />
            <span className="text-xs font-bold text-white tracking-wide">Veyra IDE</span>
          </div>

          <div className="h-4 w-px bg-white/10 hidden sm:block" />

          {/* Language Selector */}
          <LanguageSelector
            languages={languages}
            selectedLanguage={selectedLanguage}
            onChange={(lang) => {
              setSelectedLanguage(lang);
              setSelectedVersion(lang.defaultVersion);
            }}
          />

          {/* Version Selector */}
          {selectedLanguage && (
            <VersionSelector
              versions={selectedLanguage.versions}
              selectedVersion={selectedVersion}
              onChange={setSelectedVersion}
            />
          )}

          {/* Execution Status Badge */}
          <ExecutionStatus status={status} />
        </div>

        {/* IDE Control Bar */}
        <CodeRunner
          onRun={handleRun}
          onSave={handleManualSave}
          onReset={() => setShowResetModal(true)}
          onToggleFullscreen={() => setIsFullscreen(!isFullscreen)}
          isRunning={status === 'running'}
          isSaving={isSaving}
          isSaved={isSaved}
          isFullscreen={isFullscreen}
        />
      </div>

      {/* CODING INSTRUCTIONS (If present) */}
      {codingInstructions && (
        <div className="bg-[#19191C] px-4 py-2 border-b border-white/10 text-xs text-white/80 flex items-center gap-2">
          <span className="font-semibold text-blue-400 shrink-0">Task:</span>
          <span className="truncate">{codingInstructions}</span>
        </div>
      )}

      {/* IDE NAVIGATION TABS (Editor, STDIN, Output, Live Preview) */}
      <div className="bg-[#18181A] px-4 py-1 border-b border-white/10 flex items-center justify-between text-xs text-white/60">
        <div className="flex items-center gap-1">
          <button
            onClick={() => setActiveTab('editor')}
            className={`px-3 py-1 rounded-md text-xs font-semibold cursor-pointer transition-colors ${
              activeTab === 'editor' ? 'bg-[#2C2C2E] text-white' : 'hover:text-white'
            }`}
          >
            Code Editor
          </button>
          <button
            onClick={() => setActiveTab('stdin')}
            className={`px-3 py-1 rounded-md text-xs font-semibold cursor-pointer transition-colors ${
              activeTab === 'stdin' ? 'bg-[#2C2C2E] text-white' : 'hover:text-white'
            }`}
          >
            Input (STDIN)
          </button>
          {selectedLanguage?.isLivePreview ? (
            <button
              onClick={() => setActiveTab('preview')}
              className={`px-3 py-1 rounded-md text-xs font-semibold cursor-pointer flex items-center gap-1 transition-colors ${
                activeTab === 'preview' ? 'bg-[#2C2C2E] text-blue-300' : 'hover:text-white'
              }`}
            >
              <Eye className="w-3 h-3 text-blue-400" />
              <span>Live Preview</span>
            </button>
          ) : (
            <button
              onClick={() => setActiveTab('output')}
              className={`px-3 py-1 rounded-md text-xs font-semibold cursor-pointer flex items-center gap-1 transition-colors ${
                activeTab === 'output' ? 'bg-[#2C2C2E] text-emerald-300' : 'hover:text-white'
              }`}
            >
              <Terminal className="w-3 h-3 text-emerald-400" />
              <span>Output</span>
            </button>
          )}
        </div>
      </div>

      {/* MAIN BODY AREA */}
      <div className="grow p-3 flex flex-col gap-3 overflow-hidden min-h-[350px]">
        {activeTab === 'editor' && (
          <div className="grow flex flex-col h-full min-h-[320px]">
            <CodeEditor
              code={code}
              onChange={setCode}
              language={selectedLanguage?.key}
              monacoLanguage={selectedLanguage?.monacoLanguage}
            />
          </div>
        )}

        {activeTab === 'stdin' && (
          <div className="p-2">
            <InputPanel stdin={stdin} onChange={setStdin} />
          </div>
        )}

        {activeTab === 'output' && (
          <div className="p-2 grow overflow-y-auto">
            <OutputPanel result={executionResult} isRunning={status === 'running'} />
          </div>
        )}

        {activeTab === 'preview' && selectedLanguage?.isLivePreview && (
          <div className="p-2 grow">
            <LivePreview htmlCode={code} cssCode="" />
          </div>
        )}
      </div>

      {/* RESET CONFIRMATION MODAL */}
      {showResetModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#1C1C1E] border border-white/10 rounded-2xl p-6 max-w-sm w-full space-y-4 shadow-2xl animate-scaleIn">
            <div className="flex items-center gap-2 text-rose-400">
              <AlertCircle className="w-5 h-5" />
              <h3 className="text-base font-bold text-white">Reset Code to Starter?</h3>
            </div>
            <p className="text-xs text-white/70 leading-relaxed">
              Are you sure you want to reset your code? Any unsaved changes for this lesson will be discarded and restored to the original starter code.
            </p>
            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                onClick={() => setShowResetModal(false)}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold text-white/70 hover:bg-white/10 cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmReset}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-rose-600 hover:bg-rose-500 text-white cursor-pointer"
              >
                Reset Code
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
