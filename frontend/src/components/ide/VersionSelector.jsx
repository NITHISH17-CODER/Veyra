import React from 'react';

export const VersionSelector = ({ versions, selectedVersion, onChange }) => {
  if (!versions || versions.length === 0) return null;

  return (
    <select
      value={selectedVersion || versions[0]}
      onChange={(e) => onChange(e.target.value)}
      className="bg-[#1E1E1E] text-[11px] font-mono text-white/70 border border-white/10 rounded-lg px-2 py-1.5 focus:outline-none focus:border-blue-500 cursor-pointer"
    >
      {versions.map((ver) => (
        <option key={ver} value={ver}>
          {ver}
        </option>
      ))}
    </select>
  );
};
