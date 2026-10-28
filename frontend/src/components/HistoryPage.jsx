import React, { useState } from 'react';
import {
  History,
  Search,
  Download,
  Trash2,
  Volume2,
  Copy,
  Check,
  CheckCircle2,
  Filter,
  Calendar,
  Sparkles,
  ArrowRight,
  Hand
} from 'lucide-react';

export default function HistoryPage({ historyData, onDeleteItem, onClearAllHistory, onStartTranslating }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [confidenceFilter, setConfidenceFilter] = useState('all'); // 'all' | '90' | '80'
  const [copiedId, setCopiedId] = useState(null);

  const filteredHistory = (historyData || []).filter((item) => {
    const matchesSearch =
      item.english.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (item.hindi && item.hindi.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (item.tamil && item.tamil.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (item.glosses && item.glosses.join(' ').toLowerCase().includes(searchQuery.toLowerCase()));

    const matchesConfidence =
      confidenceFilter === 'all' ||
      (confidenceFilter === '90' && item.confidence >= 90) ||
      (confidenceFilter === '80' && item.confidence >= 80);

    return matchesSearch && matchesConfidence;
  });

  const speakText = (text, lang = 'en') => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    if (lang === 'hi') u.lang = 'hi-IN';
    else if (lang === 'ta') u.lang = 'ta-IN';
    else u.lang = 'en-IN';
    window.speechSynthesis.speak(u);
  };

  const copyText = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const exportAsJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(historyData, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `isl_translation_history_${new Date().toISOString().slice(0, 10)}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  const exportAsCSV = () => {
    let csvContent = "data:text/csv;charset=utf-8,Date,Time,Glosses,English,Hindi,Tamil,Confidence\n";
    (historyData || []).forEach(row => {
      const glossStr = row.glosses ? row.glosses.join(' ') : '';
      csvContent += `"${row.date || ''}","${row.time || ''}","${glossStr}","${row.english}","${row.hindi || ''}","${row.tamil || ''}",${row.confidence}%\n`;
    });
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `isl_translation_history_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  return (
    <div className="space-y-6 py-2">
      {/* Header Panel */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-700/60 shadow-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-950/80 border border-indigo-500/40 text-indigo-300 text-xs font-semibold">
            <History className="w-3.5 h-3.5" />
            <span>SESSION & HISTORICAL ARCHIVE</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-100 mt-1">
            Translation History
          </h1>
          <p className="text-xs text-slate-400">
            Recorded continuous ISL gesture sequences, multilingual syntheses, and AI confidence telemetry.
          </p>
        </div>

        {/* Export and Clear Action buttons */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={exportAsCSV}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-white text-xs font-semibold transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export CSV</span>
          </button>

          <button
            onClick={exportAsJSON}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-white text-xs font-semibold transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export JSON</span>
          </button>

          <button
            onClick={onClearAllHistory}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-red-950/60 hover:bg-red-900/80 border border-red-500/40 text-red-300 text-xs font-semibold transition"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Delete History</span>
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="glass-panel rounded-2xl p-4 border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search translations by keyword, gloss, or sentence..."
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-900/90 border border-slate-800 focus:border-indigo-500 text-slate-100 text-xs sm:text-sm placeholder:text-slate-500 focus:outline-none transition"
          />
        </div>

        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <select
            value={confidenceFilter}
            onChange={(e) => setConfidenceFilter(e.target.value)}
            className="bg-slate-900 border border-slate-800 text-slate-300 text-xs rounded-xl px-3 py-2 focus:outline-none"
          >
            <option value="all">All Confidence Levels</option>
            <option value="90">≥ 90% Confidence</option>
            <option value="80">≥ 80% Confidence</option>
          </select>
        </div>
      </div>

      {/* History Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/90 text-slate-400 text-[11px] font-mono border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Date / Time</th>
                <th className="py-3 px-4">Detected Signs</th>
                <th className="py-3 px-4">Spoken Translation (EN / हिन्दी / தமிழ்)</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/70 font-sans">
              {filteredHistory.length > 0 ? (
                filteredHistory.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-900/40 transition">
                    {/* Timestamp */}
                    <td className="py-3 px-4 font-mono text-slate-400 whitespace-nowrap">
                      <div className="flex items-center space-x-1.5">
                        <Calendar className="w-3.5 h-3.5 text-slate-500" />
                        <span>{row.date || 'Today'}</span>
                      </div>
                      <div className="text-[10px] text-slate-500">{row.time}</div>
                    </td>

                    {/* Gloss Sequence */}
                    <td className="py-3 px-4">
                      <div className="flex flex-wrap items-center gap-1 font-mono text-[11px]">
                        {row.glosses && row.glosses.map((g, idx) => (
                          <span
                            key={idx}
                            className="px-1.5 py-0.5 rounded bg-indigo-950/80 border border-indigo-800/60 text-indigo-300 font-bold"
                          >
                            {g}
                          </span>
                        ))}
                      </div>
                    </td>

                    {/* Spoken Translation */}
                    <td className="py-3 px-4 max-w-md">
                      <div className="font-semibold text-slate-100 text-xs sm:text-sm">
                        "{row.english}"
                      </div>
                      {row.hindi && (
                        <div className="text-[11px] text-amber-300/80 mt-0.5 font-medium">
                          {row.hindi}
                        </div>
                      )}
                      {row.tamil && (
                        <div className="text-[11px] text-emerald-300/80 mt-0.5 font-medium">
                          {row.tamil}
                        </div>
                      )}
                    </td>

                    {/* Confidence */}
                    <td className="py-3 px-4 font-mono whitespace-nowrap">
                      <span className={`px-2.5 py-1 rounded-full text-[11px] font-bold border ${
                        row.confidence >= 90
                          ? 'bg-emerald-950/80 border-emerald-500/40 text-emerald-300'
                          : 'bg-amber-950/80 border-amber-500/40 text-amber-300'
                      }`}>
                        {row.confidence}%
                      </span>
                    </td>

                    {/* Action Buttons */}
                    <td className="py-3 px-4 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end space-x-1.5">
                        <button
                          onClick={() => speakText(row.english, 'en')}
                          className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-indigo-300 transition"
                          title="Play English Speech"
                        >
                          <Volume2 className="w-3.5 h-3.5" />
                        </button>

                        <button
                          onClick={() => copyText(row.english, row.id)}
                          className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition"
                          title="Copy Translation"
                        >
                          {copiedId === row.id ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                        </button>

                        <button
                          onClick={() => onDeleteItem && onDeleteItem(row.id)}
                          className="p-1.5 rounded-lg bg-slate-900 hover:bg-red-950/80 text-slate-400 hover:text-red-300 transition"
                          title="Delete Record"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="py-12 text-center text-slate-500">
                    <div className="space-y-3">
                      <p className="text-xs">No translation history found matching filters.</p>
                      <button
                        onClick={onStartTranslating}
                        className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-semibold"
                      >
                        <Hand className="w-3.5 h-3.5" />
                        <span>Start Translating in Camera</span>
                      </button>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

