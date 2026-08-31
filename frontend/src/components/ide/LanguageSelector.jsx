import React from 'react';
import { Code2 } from 'lucide-react';

export const LanguageSelector = ({ languages, selectedLanguage, onChange }) => {
  return (
    <div className="flex items-center gap-2">
      <Code2 className="w-4 h-4 text-blue-400 shrink-0" />
      <select
        value={selectedLanguage?.key || ''}
        onChange={(e) => {
          const lang = languages.find((l) => l.key === e.target.value);
          if (lang) onChange(lang);
        }}
        className="bg-[#1E1E1E] text-xs font-semibold text-white/90 border border-white/10 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-blue-500 cursor-pointer"
      >
        {languages.map((lang) => (
          <option key={lang.key} value={lang.key}>
            {lang.language}
          </option>
        ))}
      </select>
    </div>
  );
};
