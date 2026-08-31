import React from 'react';
import { Terminal, CheckCircle2, AlertTriangle, Clock, HardDrive } from 'lucide-react';

export const OutputPanel = ({ result, isRunning }) => {
  if (isRunning) {
    return (
      <div className="bg-[#121212] rounded-xl p-4 border border-white/10 text-xs font-mono text-white/50 flex items-center gap-2">
        <div className="w-2 h-2 rounded-full bg-blue-500 animate-ping" />
        <span>Executing program in isolated sandbox environment...</span>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="bg-[#121212] rounded-xl p-4 border border-white/10 text-xs font-mono text-white/40 italic">
        Click "Run" to execute code and view output here.
      </div>
    );
  }

  const { status, stdout, stderr, exitCode, executionTime, memoryUsed } = result;

  return (
    <div className="space-y-2 font-mono text-xs">
      <div className="flex items-center justify-between text-[11px] text-white/60 px-1">
        <div className="flex items-center gap-1.5 font-bold uppercase tracking-wider text-white/80">
          <Terminal className="w-3.5 h-3.5 text-emerald-400" />
          <span>OUTPUT</span>
        </div>
        <div className="flex items-center gap-3">
          {executionTime !== undefined && (
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3 text-blue-400" />
              <span>{executionTime}s</span>
            </span>
          )}
          {exitCode !== undefined && (
            <span className={`px-2 py-0.5 rounded font-bold ${exitCode === 0 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}`}>
              Exit Code: {exitCode}
            </span>
          )}
        </div>
      </div>

      <div className="bg-[#121212] rounded-xl p-4 border border-white/10 space-y-3 overflow-x-auto">
        {/* Stdout display */}
        {stdout && (
          <div className="space-y-1">
            <div className="text-[10px] text-emerald-400 font-semibold uppercase tracking-wider">Standard Output:</div>
            <pre className="text-white/90 leading-relaxed whitespace-pre-wrap font-mono break-all">{stdout}</pre>
          </div>
        )}

        {/* Stderr or Error display */}
        {stderr && (
          <div className="space-y-1 pt-2 border-t border-white/10">
            <div className="text-[10px] text-rose-400 font-semibold uppercase tracking-wider flex items-center gap-1">
              <AlertTriangle className="w-3 h-3" />
              <span>{status === 'timeout' ? 'Execution Timeout:' : 'Errors / Diagnostics:'}</span>
            </div>
            <pre className="text-rose-300 leading-relaxed whitespace-pre-wrap font-mono break-all">{stderr}</pre>
          </div>
        )}

        {/* Empty output case */}
        {!stdout && !stderr && (
          <div className="text-white/40 italic">
            [Program finished with no output]
          </div>
        )}
      </div>
    </div>
  );
};
