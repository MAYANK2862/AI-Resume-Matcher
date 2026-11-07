import React from 'react';
import { Sparkles, History, FileText, RefreshCw } from 'lucide-react';

export default function Navbar({ onOpenHistory, onReset, historyCount, onLoadSample }) {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3 cursor-pointer" onClick={onReset}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-white tracking-tight">AI Resume Matcher</span>
              <span className="px-2 py-0.5 text-xs font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/20 rounded-full">
                NLP Engine
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">Analyze • Match • Optimize for ATS</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={onLoadSample}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors"
            title="Load instant test resume & job"
          >
            <FileText className="w-3.5 h-3.5 text-sky-400" />
            <span>Load Demo Sample</span>
          </button>

          <button
            onClick={onOpenHistory}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors relative"
          >
            <History className="w-3.5 h-3.5 text-indigo-400" />
            <span>History</span>
            {historyCount > 0 && (
              <span className="ml-1 px-1.5 py-0.2 bg-indigo-500/30 text-indigo-300 rounded-full text-[10px] font-bold">
                {historyCount}
              </span>
            )}
          </button>

          <button
            onClick={onReset}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            title="Reset All"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}

