import React from 'react';
import { Check, X, FileCheck, Layers, Award } from 'lucide-react';

export default function ResumeOverview({ analysis, resumeData }) {
  if (!analysis) return null;

  const sections = analysis.sections_detected || {};
  const sectionList = [
    { key: 'summary', label: 'Professional Summary / Objective' },
    { key: 'experience', label: 'Work Experience / History' },
    { key: 'education', label: 'Education / Academic Degrees' },
    { key: 'skills', label: 'Technical & Core Skills' },
    { key: 'projects', label: 'Key Projects & Portfolio' },
    { key: 'certifications', label: 'Certifications / Credentials' },
  ];

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl space-y-4">
      <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
        <div className="p-2 rounded-lg bg-teal-500/10 text-teal-400 border border-teal-500/20">
          <Layers className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-base font-bold text-white tracking-tight">Resume Section Audit</h3>
          <p className="text-xs text-slate-400">ATS standard section header compliance</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        {sectionList.map((sec) => {
          const isPresent = Boolean(sections[sec.key]);
          return (
            <div
              key={sec.key}
              className={`p-3 rounded-xl border flex items-center justify-between text-xs transition-all ${
                isPresent
                  ? 'bg-slate-950/60 border-slate-800 text-slate-200'
                  : 'bg-rose-500/5 border-rose-500/20 text-rose-300'
              }`}
            >
              <span className="font-medium">{sec.label}</span>
              {isPresent ? (
                <div className="flex items-center space-x-1 text-emerald-400 font-semibold text-[11px]">
                  <Check className="w-3.5 h-3.5" />
                  <span>Found</span>
                </div>
              ) : (
                <div className="flex items-center space-x-1 text-rose-400 font-semibold text-[11px]">
                  <X className="w-3.5 h-3.5" />
                  <span>Missing</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

