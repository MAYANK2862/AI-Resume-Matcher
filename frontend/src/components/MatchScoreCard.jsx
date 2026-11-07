import React from 'react';
import { Target, CheckCircle2, XCircle, Award, Zap, TrendingUp, ShieldCheck } from 'lucide-react';

function CircularGauge({ score, size = 120, strokeWidth = 10, label, sublabel, colorClass }) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const clampedScore = Math.min(100, Math.max(0, score || 0));
  const offset = circumference - (clampedScore / 100) * circumference;

  let strokeColor = '#0ea5e9'; // sky
  if (clampedScore >= 75) strokeColor = '#10b981'; // emerald
  else if (clampedScore >= 50) strokeColor = '#f59e0b'; // amber
  else strokeColor = '#f43f5e'; // rose

  return (
    <div className="flex flex-col items-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg className="w-full h-full transform -rotate-90" viewBox={`0 0 ${size} ${size}`}>
          {/* Background Track */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="transparent"
            stroke="#1e293b"
            strokeWidth={strokeWidth}
          />
          {/* Progress Arc */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="transparent"
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-2xl font-extrabold text-white tracking-tight">{Math.round(clampedScore)}%</span>
          {sublabel && <span className="text-[10px] text-slate-400 font-medium">{sublabel}</span>}
        </div>
      </div>
      {label && <span className="mt-2 text-xs font-semibold text-slate-300">{label}</span>}
    </div>
  );
}

export default function MatchScoreCard({ analysis }) {
  if (!analysis) return null;

  const {
    match_score,
    skill_match_score,
    semantic_score,
    ats_score,
    matched_skills = [],
    missing_skills = [],
    metrics_detected = 0,
    action_verbs_count = 0,
    job_title,
    candidate_name
  } = analysis;

  const getMatchVerdict = (score) => {
    if (score >= 80) return { title: 'High Fit Match', badge: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20', desc: 'Candidate strongly aligns with target role qualifications and skills.' };
    if (score >= 60) return { title: 'Moderate Fit Match', badge: 'bg-amber-500/10 text-amber-400 border-amber-500/20', desc: 'Good baseline skills with a few key technical gaps to bridge.' };
    return { title: 'Low Fit / Career Pivot', badge: 'bg-rose-500/10 text-rose-400 border-rose-500/20', desc: 'Substantial skill gaps detected against the target job requirements.' };
  };

  const verdict = getMatchVerdict(match_score);

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-2xl">
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-slate-800 gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h2 className="text-xl font-bold text-white tracking-tight">Match Results Overview</h2>
            <span className={`px-2.5 py-0.5 text-xs font-semibold rounded-full border ${verdict.badge}`}>
              {verdict.title}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Analyzing <strong className="text-slate-200">{candidate_name || 'Candidate'}</strong> against{' '}
            <strong className="text-slate-200">{job_title}</strong>
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>ATS Verified NLP Score</span>
        </div>
      </div>

      {/* Main Gauges Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 py-6 border-b border-slate-800">
        <div className="flex flex-col items-center p-3 rounded-xl bg-slate-950/50 border border-slate-800/80">
          <CircularGauge
            score={match_score}
            size={110}
            strokeWidth={9}
            label="Overall Match"
            sublabel="Composite"
          />
        </div>

        <div className="flex flex-col items-center p-3 rounded-xl bg-slate-950/50 border border-slate-800/80">
          <CircularGauge
            score={skill_match_score}
            size={110}
            strokeWidth={9}
            label="Skill Match"
            sublabel="Direct Coverage"
          />
        </div>

        <div className="flex flex-col items-center p-3 rounded-xl bg-slate-950/50 border border-slate-800/80">
          <CircularGauge
            score={semantic_score}
            size={110}
            strokeWidth={9}
            label="Context Relevance"
            sublabel="TF-IDF NLP"
          />
        </div>

        <div className="flex flex-col items-center p-3 rounded-xl bg-slate-950/50 border border-slate-800/80">
          <CircularGauge
            score={ats_score}
            size={110}
            strokeWidth={9}
            label="ATS Readiness"
            sublabel="Format & Rules"
          />
        </div>
      </div>

      {/* Metric Counters Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-5">
        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800 flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
            <CheckCircle2 className="w-4 h-4" />
          </div>
          <div>
            <div className="text-base font-bold text-white">{matched_skills.length}</div>
            <div className="text-[11px] text-slate-400">Matched Skills</div>
          </div>
        </div>

        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800 flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-rose-500/10 text-rose-400">
            <XCircle className="w-4 h-4" />
          </div>
          <div>
            <div className="text-base font-bold text-white">{missing_skills.length}</div>
            <div className="text-[11px] text-slate-400">Missing Skills</div>
          </div>
        </div>

        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800 flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-sky-500/10 text-sky-400">
            <TrendingUp className="w-4 h-4" />
          </div>
          <div>
            <div className="text-base font-bold text-white">{metrics_detected}</div>
            <div className="text-[11px] text-slate-400">KPI Metrics Found</div>
          </div>
        </div>

        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800 flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400">
            <Zap className="w-4 h-4" />
          </div>
          <div>
            <div className="text-base font-bold text-white">{action_verbs_count}</div>
            <div className="text-[11px] text-slate-400">Power Action Verbs</div>
          </div>
        </div>
      </div>
    </div>
  );
}

