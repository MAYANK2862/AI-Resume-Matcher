import React from 'react';
import { X, Trash2, ExternalLink, Calendar, Award, CheckCircle2 } from 'lucide-react';

export default function HistoryModal({
  isOpen,
  onClose,
  history,
  onSelectHistoryItem,
  onDeleteHistoryItem,
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <h3 className="text-lg font-bold text-white">Scan History</h3>
            <p className="text-xs text-slate-400">Previous resume matches stored in SQLite database</p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content list */}
        <div className="p-5 overflow-y-auto space-y-3 flex-1">
          {history.length === 0 ? (
            <div className="py-12 text-center text-slate-500 text-sm">
              No saved analysis history yet. Run a match scan to save records!
            </div>
          ) : (
            history.map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 hover:border-slate-700 transition-all flex items-center justify-between gap-4"
              >
                <div className="space-y-1 min-w-0">
                  <div className="flex items-center space-x-2">
                    <span className="font-semibold text-sm text-slate-200 truncate">{item.job_title}</span>
                  </div>
                  <div className="flex items-center space-x-3 text-xs text-slate-400">
                    <span>{item.candidate_name || 'Candidate'}</span>
                    <span>•</span>
                    <span className="flex items-center space-x-1">
                      <Calendar className="w-3 h-3 text-slate-500" />
                      <span>{new Date(item.created_at).toLocaleDateString()}</span>
                    </span>
                  </div>
                </div>

                <div className="flex items-center space-x-3 flex-shrink-0">
                  <div className="text-right">
                    <div className="text-sm font-bold text-sky-400">{item.match_score}% Match</div>
                    <div className="text-[10px] text-slate-500">{item.matched_count} matched • {item.missing_count} missing</div>
                  </div>

                  <button
                    onClick={() => onSelectHistoryItem(item.id)}
                    className="p-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white transition-colors"
                    title="Load Analysis"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </button>

                  <button
                    onClick={() => onDeleteHistoryItem(item.id)}
                    className="p-2 rounded-lg bg-slate-800 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition-colors"
                    title="Delete Record"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

