import React, { useEffect, useState } from 'react';
import { Eye, ShieldCheck } from 'lucide-react';

export const LivePreview = ({ htmlCode, cssCode }) => {
  const [srcDoc, setSrcDoc] = useState('');

  useEffect(() => {
    const combined = `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding: 1.5rem;
            margin: 0;
            background-color: #ffffff;
            color: #111827;
          }
          ${cssCode || ''}
        </style>
      </head>
      <body>
        ${htmlCode || ''}
      </body>
      </html>
    `;
    setSrcDoc(combined);
  }, [htmlCode, cssCode]);

  return (
    <div className="space-y-2 h-full flex flex-col">
      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-1.5 text-xs font-bold text-white/80 uppercase tracking-wider">
          <Eye className="w-3.5 h-3.5 text-blue-400" />
          <span>HTML/CSS Live Preview</span>
        </div>
        <div className="flex items-center gap-1 text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full">
          <ShieldCheck className="w-3 h-3" />
          <span>Sandboxed Isolated Environment</span>
        </div>
      </div>
      <div className="grow bg-white rounded-xl overflow-hidden border border-white/10 shadow-inner min-h-[300px] relative">
        <iframe
          srcDoc={srcDoc}
          title="HTML Live Sandbox Preview"
          sandbox="allow-scripts"
          className="w-full h-full border-0 min-h-[300px]"
        />
      </div>
    </div>
  );
};
