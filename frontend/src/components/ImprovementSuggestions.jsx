import React from 'react';
import { Lightbulb, AlertTriangle, ArrowRight, CheckCircle, Zap } from 'lucide-react';

export default function ImprovementSuggestions({ suggestions }) {
  if (!suggestions || suggestions.length === 0) {
    return (
      <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl text-center">
        <CheckCircle className="w-10 h-10 text-emerald-400 mx-auto mb-2" />
        <h3 className="font-semibold text-slate-200">Outstanding Alignment!</h3>
        <p className="text-xs text-slate-400">No major critical gaps detected between resume and target role.</p>
      </div>
    );
  }

  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
      case 'medium':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
      default:
        return 'bg-sky-500/10 text-sky-400 border-sky-500/20';
    }
  };

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl space-y-4">
      <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
        <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
          <Lightbulb className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-base font-bold text-white tracking-tight">AI Improvement Recommendations</h3>
          <p className="text-xs text-slate-400">Prioritized guidance to boost ATS score and interview callbacks</p>
        </div>
      </div>

      <div className="space-y-3">
        {suggestions.map((item, idx) => (
          <div
            key={idx}
            className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 hover:border-slate-700 transition-all flex flex-col space-y-2.5"
          >
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-center space-x-2">
                <span className="text-sm font-semibold text-slate-100">{item.title}</span>
              </div>
              <div className="flex items-center space-x-1.5 flex-shrink-0">
                <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border bg-slate-900 text-slate-400 border-slate-700">
                  {item.category}
                </span>
                <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${getPriorityBadge(item.priority)}`}>
                  {item.priority}
                </span>
              </div>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">{item.description}</p>

            <div className="mt-1 p-3 rounded-lg bg-sky-950/30 border border-sky-500/20 flex items-start space-x-2 text-xs text-sky-200">
              <Zap className="w-4 h-4 text-sky-400 flex-shrink-0 mt-0.5" />
              <div>
                <strong className="font-semibold text-sky-300">Actionable Fix: </strong>
                <span>{item.actionable_tip}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

