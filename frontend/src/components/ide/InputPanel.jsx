import React from 'react';
import { Terminal } from 'lucide-react';

export const InputPanel = ({ stdin, onChange }) => {
  return (
    <div className="space-y-1.5 font-sans">
      <div className="flex items-center gap-1.5 text-xs font-semibold text-white/70">
        <Terminal className="w-3.5 h-3.5 text-blue-400" />
        <span>INPUT (STDIN)</span>
      </div>
      <textarea
        value={stdin}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Provide input for your program here (e.g. 5\n10)..."
        rows={3}
        className="w-full bg-[#121212] text-xs font-mono text-white/90 p-3 rounded-xl border border-white/10 focus:outline-none focus:border-blue-500/50 resize-y"
      />
    </div>
  );
};
