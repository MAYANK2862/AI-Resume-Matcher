import React, { useState } from 'react';
import { CheckCircle2, XCircle, PlusCircle, Search, Copy, Check } from 'lucide-react';

export default function SkillsComparison({ analysis }) {
  const [filter, setFilter] = useState('missing'); // 'all', 'matched', 'missing', 'extra'
  const [searchQuery, setSearchQuery] = useState('');
  const [copied, setCopied] = useState(false);

  if (!analysis) return null;

  const {
    matched_skills = [],
    missing_skills = [],
    candidate_skills = [],
    job_skills = []
  } = analysis;

  // Extra candidate skills: skills candidate has that weren't strictly requested in JD
  const matchedSet = new Set(matched_skills.map((s) => s.toLowerCase()));
  const extraSkills = candidate_skills.filter((s) => !matchedSet.has(s.toLowerCase()));

  const handleCopyMissing = () => {
    if (missing_skills.length === 0) return;
    navigator.clipboard.writeText(missing_skills.join(', '));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getFilteredSkills = () => {
    let list = [];
    if (filter === 'all') {
      list = [
        ...matched_skills.map((name) => ({ name, type: 'matched' })),
        ...missing_skills.map((name) => ({ name, type: 'missing' })),
      ];
    } else if (filter === 'matched') {
      list = matched_skills.map((name) => ({ name, type: 'matched' }));
    } else if (filter === 'missing') {
      list = missing_skills.map((name) => ({ name, type: 'missing' }));
    } else if (filter === 'extra') {
      list = extraSkills.map((name) => ({ name, type: 'extra' }));
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      list = list.filter((s) => s.name.toLowerCase().includes(q));
    }
    return list;
  };

  const currentList = getFilteredSkills();

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h3 className="text-base font-bold text-white tracking-tight">Skills Breakdown & Gap Analysis</h3>
          <p className="text-xs text-slate-400">
            Compare skills requested by employer vs. detected on candidate resume
          </p>
        </div>

        {missing_skills.length > 0 && (
          <button
            onClick={handleCopyMissing}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors self-start sm:self-auto"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied Missing Skills!' : 'Copy Missing Skills'}</span>
          </button>
        )}
      </div>

      {/* Filter Tabs & Search Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 my-4">
        <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs overflow-x-auto">
          <button
            onClick={() => setFilter('missing')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center space-x-1.5 whitespace-nowrap ${
              filter === 'missing'
                ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <XCircle className="w-3.5 h-3.5 text-rose-400" />
            <span>Missing Skills ({missing_skills.length})</span>
          </button>

          <button
            onClick={() => setFilter('matched')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center space-x-1.5 whitespace-nowrap ${
              filter === 'matched'
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>Matched ({matched_skills.length})</span>
          </button>

          <button
            onClick={() => setFilter('extra')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center space-x-1.5 whitespace-nowrap ${
              filter === 'extra'
                ? 'bg-sky-500/20 text-sky-300 border border-sky-500/30'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <PlusCircle className="w-3.5 h-3.5 text-sky-400" />
            <span>Bonus Skills ({extraSkills.length})</span>
          </button>

          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition-all whitespace-nowrap ${
              filter === 'all'
                ? 'bg-slate-800 text-white border border-slate-700'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <span>All Target ({job_skills.length})</span>
          </button>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Filter skills..."
            className="pl-8 pr-3 py-1.5 bg-slate-950 rounded-xl border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500 w-full sm:w-44"
          />
        </div>
      </div>

      {/* Skills Pill Grid */}
      <div className="min-h-[140px] p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
        {currentList.length === 0 ? (
          <div className="h-28 flex flex-col items-center justify-center text-slate-500 text-xs">
            <p>No skills found matching this view.</p>
          </div>
        ) : (
          <div className="flex flex-wrap gap-2">
            {currentList.map((item, idx) => {
              let badgeStyle = '';
              let icon = null;

              if (item.type === 'matched') {
                badgeStyle = 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30 hover:bg-emerald-500/20';
                icon = <CheckCircle2 className="w-3 h-3 text-emerald-400" />;
              } else if (item.type === 'missing') {
                badgeStyle = 'bg-rose-500/10 text-rose-300 border-rose-500/30 hover:bg-rose-500/20';
                icon = <XCircle className="w-3 h-3 text-rose-400" />;
              } else {
                badgeStyle = 'bg-sky-500/10 text-sky-300 border-sky-500/30 hover:bg-sky-500/20';
                icon = <PlusCircle className="w-3 h-3 text-sky-400" />;
              }

              return (
                <div
                  key={idx}
                  className={`flex items-center space-x-1.5 px-3 py-1 rounded-lg border text-xs font-medium transition-colors ${badgeStyle}`}
                >
                  {icon}
                  <span>{item.name}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

