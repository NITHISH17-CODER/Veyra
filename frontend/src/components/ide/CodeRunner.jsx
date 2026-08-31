import React from 'react';
import { Play, Save, RotateCcw, Maximize2, Minimize2, Check, Loader2 } from 'lucide-react';

export const CodeRunner = ({
  onRun,
  onSave,
  onReset,
  onToggleFullscreen,
  isRunning,
  isSaving,
  isSaved,
  isFullscreen
}) => {
  return (
    <div className="flex items-center gap-2 flex-wrap">
      {/* Run Code Button */}
      <button
        onClick={onRun}
        disabled={isRunning}
        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-xs font-bold transition-colors cursor-pointer shadow-sm"
      >
        {isRunning ? (
          <>
            <Loader2 className="w-3.5 h-3.5 animate-spin" />
            <span>Running...</span>
          </>
        ) : (
          <>
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Run</span>
          </>
        )}
      </button>

      {/* Save Button */}
      <button
        onClick={onSave}
        disabled={isSaving}
        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#2D2D2D] hover:bg-[#3D3D3D] text-white/90 text-xs font-semibold border border-white/10 transition-colors cursor-pointer"
      >
        {isSaved ? (
          <>
            <Check className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-emerald-400">Saved</span>
          </>
        ) : (
          <>
            <Save className="w-3.5 h-3.5 text-blue-400" />
            <span>{isSaving ? 'Saving...' : 'Save'}</span>
          </>
        )}
      </button>

      {/* Reset Button */}
      <button
        onClick={onReset}
        title="Reset code to starter code"
        className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-[#2D2D2D] hover:bg-rose-500/20 text-white/70 hover:text-rose-300 text-xs font-medium border border-white/10 transition-colors cursor-pointer"
      >
        <RotateCcw className="w-3.5 h-3.5" />
        <span className="hidden sm:inline">Reset</span>
      </button>

      {/* Fullscreen Expand Button */}
      <button
        onClick={onToggleFullscreen}
        title={isFullscreen ? 'Exit Fullscreen' : 'Expand IDE Fullscreen'}
        className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-[#2D2D2D] hover:bg-[#3D3D3D] text-white/80 text-xs font-medium border border-white/10 transition-colors cursor-pointer"
      >
        {isFullscreen ? (
          <>
            <Minimize2 className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Exit</span>
          </>
        ) : (
          <>
            <Maximize2 className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Expand</span>
          </>
        )}
      </button>
    </div>
  );
};
