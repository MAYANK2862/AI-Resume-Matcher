import React from 'react';
import { Briefcase, Bookmark, Sparkles } from 'lucide-react';

export default function JobDescriptionInput({
  jobTitle,
  setJobTitle,
  jobDescription,
  setJobDescription,
  sampleJobs,
  onSelectSampleJob,
  onAnalyze,
  isAnalyzing,
  canAnalyze
}) {
  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-xl flex flex-col h-full">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Briefcase className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-semibold text-slate-100 text-base">Target Job Description</h2>
            <p className="text-xs text-slate-400">Paste job requirements or pick a preset role</p>
          </div>
        </div>
      </div>

      {/* Preset Role Quick Selectors */}
      {sampleJobs && sampleJobs.length > 0 && (
        <div className="mb-3">
          <div className="flex items-center space-x-1.5 text-xs text-slate-400 mb-2">
            <Bookmark className="w-3.5 h-3.5 text-indigo-400" />
            <span>Preset Roles:</span>
          </div>
          <div className="grid grid-cols-2 gap-1.5">
            {sampleJobs.map((job) => (
              <button
                key={job.id}
                type="button"
                onClick={() => onSelectSampleJob(job)}
                className={`text-left px-2.5 py-1.5 rounded-lg border text-xs transition-all flex flex-col ${
                  jobTitle === job.title
                    ? 'bg-indigo-600/20 border-indigo-500/50 text-indigo-200'
                    : 'bg-slate-950/60 border-slate-800 text-slate-300 hover:border-slate-700 hover:bg-slate-800/50'
                }`}
              >
                <span className="font-semibold truncate">{job.title}</span>
                <span className="text-[10px] text-slate-400 truncate">{job.company}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Job Title Field */}
      <div className="space-y-3 flex-1 flex flex-col">
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Target Job Title</label>
          <input
            type="text"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            placeholder="e.g. Senior Full Stack Engineer"
            className="w-full px-3 py-2 bg-slate-950 rounded-xl border border-slate-700 text-slate-200 text-xs focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
          />
        </div>

        {/* Job Description Textarea */}
        <div className="flex-1 flex flex-col min-h-[160px]">
          <label className="block text-xs font-medium text-slate-300 mb-1">
            Job Description & Required Qualifications
          </label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste complete job description, required technical skills, responsibilities, and qualifications..."
            rows={8}
            className="w-full flex-1 p-3 bg-slate-950 rounded-xl border border-slate-700 text-slate-200 text-xs font-mono placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all resize-none"
          />
          <div className="flex justify-between items-center text-xs text-slate-400 mt-1">
            <span>{jobDescription.split(/\s+/).filter(Boolean).length} words</span>
            <span>Target specifications</span>
          </div>
        </div>

        {/* Match Action Button */}
        <button
          type="button"
          disabled={!canAnalyze || isAnalyzing}
          onClick={onAnalyze}
          className={`w-full py-3 px-4 rounded-xl font-semibold text-sm flex items-center justify-center space-x-2 transition-all shadow-lg ${
            !canAnalyze || isAnalyzing
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700/50'
              : 'bg-gradient-to-r from-sky-500 via-indigo-600 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-white shadow-indigo-500/25 active:scale-[0.99]'
          }`}
        >
          {isAnalyzing ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>Analyzing with NLP...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              <span>Run AI Match & Gap Analysis</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}

