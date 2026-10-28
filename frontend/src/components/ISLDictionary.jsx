/**
 * ISLDictionary.jsx — Official Standard Indian Sign Language (ISLRTC) Portal.
 *
 * Exclusively implements the official national standards codified by the
 * Indian Sign Language Research and Training Centre (ISLRTC), Ministry of
 * Social Justice and Empowerment, Government of India.
 */

import React, { useState, useMemo } from 'react';
import {
  Search,
  CheckCircle2,
  AlertCircle,
  BookOpen,
  ChevronLeft,
  ChevronRight,
  X,
  Info,
  Cpu,
  Globe,
  Tag,
  MapPin,
  Users,
  Compass,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Check,
  Award,
  Layers,
  GraduationCap
} from 'lucide-react';
import {
  ISL_DICTIONARY,
  ISL_CATEGORIES,
  searchDictionary,
  MODEL_SUPPORTED_GLOSSES,
} from '../data/islDictionary';
import {
  INDIAN_SIGN_LANGUAGES,
  ISLRTC_OFFICIAL_VOLUMES,
  getIndianSignLanguages
} from '../data/indianSignLanguages';

const PAGE_SIZE = 12;

export default function ISLDictionary({
  selectedDialect = 'isl-standard',
  onSelectDialect,
  onNavigateToTranslator
}) {
  // Main View Toggle: 'standards' | 'vocabulary'
  const [viewMode, setViewMode] = useState('standards');

  // Sign Vocabulary View State
  const [vocabQuery, setVocabQuery] = useState('');
  const [categoryId, setCategoryId] = useState('all');
  const [modelFilter, setModelFilter] = useState(null); // null | true | false
  const [page, setPage] = useState(1);
  const [expandedSignId, setExpandedSignId] = useState(null);

  // Standards Explorer Search State
  const [standardQuery, setStandardQuery] = useState('');

  // Vocabulary Results
  const vocabResults = useMemo(
    () => searchDictionary(vocabQuery, categoryId, modelFilter),
    [vocabQuery, categoryId, modelFilter]
  );
  const totalPages = Math.max(1, Math.ceil(vocabResults.length / PAGE_SIZE));
  const safePage = Math.min(page, totalPages);
  const pageResults = vocabResults.slice((safePage - 1) * PAGE_SIZE, safePage * PAGE_SIZE);

  // Standard Zonal Chapters Results
  const standardZonalResults = useMemo(
    () => getIndianSignLanguages(standardQuery),
    [standardQuery]
  );

  // Filtered Volumes
  const filteredVolumes = useMemo(() => {
    if (!standardQuery.trim()) return ISLRTC_OFFICIAL_VOLUMES;
    const q = standardQuery.toLowerCase();
    return ISLRTC_OFFICIAL_VOLUMES.filter(v =>
      v.name.toLowerCase().includes(q) ||
      v.hindiName.toLowerCase().includes(q) ||
      v.description.toLowerCase().includes(q) ||
      v.signs.some(s => s.toLowerCase().includes(q))
    );
  }, [standardQuery]);

  const resetPage = () => setPage(1);

  const totalSupported = MODEL_SUPPORTED_GLOSSES.length;
  const totalDict = ISL_DICTIONARY.length;

  return (
    <div className="w-full space-y-6 max-w-6xl mx-auto">

      {/* ── Official ISLRTC Header ────────────────────────────────────────── */}
      <div className="glass-panel rounded-3xl p-5 border border-slate-800/80 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center space-x-3.5">
            <div className="p-3 rounded-2xl bg-gradient-to-tr from-purple-600 via-indigo-600 to-cyan-400 p-0.5 shadow-lg shadow-indigo-500/20">
              <div className="w-full h-full bg-[#050609] p-2 rounded-[14px]">
                <Award className="w-5 h-5 text-cyan-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h2 className="text-lg font-black text-white tracking-wide">
                  Standard Indian Sign Language (ISLRTC)
                </h2>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-950/80 border border-emerald-500/40 text-emerald-300">
                  National Standard Certified
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Official National Standards codified by ISLRTC, Ministry of Social Justice & Empowerment, Govt. of India.
              </p>
            </div>
          </div>

          {/* Primary View Toggle Tabs & Open in Live Translator Action */}
          <div className="flex flex-wrap items-center gap-2.5">
            <div className="flex items-center bg-slate-900/90 p-1 rounded-2xl border border-slate-800 text-xs font-semibold">
              <button
                onClick={() => setViewMode('standards')}
                className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl transition ${
                  viewMode === 'standards'
                    ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold shadow-md'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <GraduationCap className="w-4 h-4 text-cyan-300" />
                <span>ISLRTC Standard Curricula (9 Volumes)</span>
              </button>

              <button
                onClick={() => setViewMode('vocabulary')}
                className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl transition ${
                  viewMode === 'vocabulary'
                    ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white font-bold shadow-md'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Tag className="w-4 h-4 text-indigo-300" />
                <span>Standard Sign Vocabulary ({totalDict})</span>
              </button>
            </div>

            {onNavigateToTranslator && (
              <button
                onClick={onNavigateToTranslator}
                className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-md shadow-indigo-600/20 transition transform hover:scale-[1.02] active:scale-[0.98]"
                title="Launch Live Sign Language Translator"
              >
                <span>Open in Live Translator</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* ══════════════════════════════════════════════════════════════════════════
          VIEW 1: ISLRTC OFFICIAL STANDARDS (9 THEMATIC VOLUMES & ZONAL CHAPTERS)
         ══════════════════════════════════════════════════════════════════════════ */}
      {viewMode === 'standards' && (
        <div className="space-y-6 animate-in fade-in duration-200">
          {/* Search bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
            <input
              type="text"
              value={standardQuery}
              onChange={e => setStandardQuery(e.target.value)}
              placeholder="Search official ISLRTC standards, healthcare, legal, banking, academic volumes…"
              className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-9 py-2.5 text-sm text-slate-100 placeholder-slate-600 focus:outline-none focus:border-indigo-500 transition"
            />
            {standardQuery && (
              <button
                onClick={() => setStandardQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Section A: The 9 Official ISLRTC Standard Thematic Volumes */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
                <Layers className="w-4 h-4 text-cyan-400" />
                <span>The 9 Official ISLRTC Standard Thematic Volumes (10,000+ Signs)</span>
              </h3>
              <span className="text-[11px] text-slate-500 font-mono">Certified National Corpus</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3.5">
              {filteredVolumes.map(vol => (
                <div
                  key={vol.id}
                  className="glass-panel rounded-2xl border border-slate-800/80 p-4 hover:border-slate-700 transition flex flex-col justify-between space-y-3"
                >
                  <div className="flex items-start justify-between">
                    <span className="text-2xl p-2 bg-slate-900 rounded-xl border border-slate-800">
                      {vol.icon}
                    </span>
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-950/80 border border-indigo-500/40 text-indigo-300">
                      {vol.volume}
                    </span>
                  </div>

                  <div className="space-y-2">
                    <div>
                      <h4 className="text-sm font-bold text-white leading-snug">
                        {vol.name}
                      </h4>
                      <div className="text-[11px] text-slate-400 mt-0.5">{vol.hindiName}</div>
                      <span className="text-xs text-emerald-400 font-mono font-bold mt-1 block">
                        {vol.signCount}
                      </span>
                    </div>

                    {vol.signs && vol.signs.length > 0 && (
                      <div className="pt-2 border-t border-slate-800/60">
                        <div className="text-[10px] uppercase font-bold text-slate-400 mb-1.5 flex items-center justify-between">
                          <span>Standard Signs</span>
                          <span className="text-indigo-400 font-mono">{vol.signs.length} signs</span>
                        </div>
                        <div className="flex flex-wrap gap-1 max-h-24 overflow-y-auto pr-1">
                          {vol.signs.map(sign => (
                            <span
                              key={sign}
                              onClick={(e) => {
                                e.stopPropagation();
                                setViewMode('vocabulary');
                                setVocabQuery(sign);
                              }}
                              className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-900/90 text-indigo-300 border border-slate-800 hover:border-indigo-500/60 hover:text-white cursor-pointer transition"
                              title={`View "${sign}" in vocabulary`}
                            >
                              {sign}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Section B: Official ISLRTC Zonal Consultative Chapters */}
          <div className="space-y-3 pt-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
                <Compass className="w-4 h-4 text-purple-400" />
                <span>Official ISLRTC Zonal Standard Chapters</span>
              </h3>
              <span className="text-[11px] text-slate-500 font-mono">Harmonized Regional Implementation</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {standardZonalResults.map(standard => {
                const isSelected = selectedDialect === standard.id;
                return (
                  <div
                    key={standard.id}
                    className={`glass-panel rounded-2xl border p-4 space-y-3 transition ${
                      isSelected
                        ? 'border-indigo-500/80 shadow-lg shadow-indigo-500/10 bg-indigo-950/20'
                        : 'border-slate-800/80 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-start space-x-3">
                        <span className="text-2xl p-2 bg-slate-900 rounded-2xl border border-slate-800 flex-shrink-0">
                          {standard.icon}
                        </span>
                        <div>
                          <h4 className="text-sm font-black text-white">{standard.name}</h4>
                        </div>
                      </div>

                      <div className="flex flex-col items-end space-y-1 flex-shrink-0">
                        <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold border bg-emerald-950/80 border-emerald-500/40 text-emerald-300">
                          {standard.badge}
                        </span>
                        {isSelected && (
                          <span className="flex items-center space-x-1 px-2 py-0.5 rounded-full text-[9px] font-bold bg-indigo-600 text-white">
                            <Check className="w-3 h-3" />
                            <span>Active Input</span>
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Sample Zonal Signs */}
                    {standard.sampleSigns && standard.sampleSigns.length > 0 && (
                      <div className="pt-2 border-t border-slate-800/60">
                        <div className="text-[10px] uppercase font-bold text-slate-400 mb-1.5 flex items-center justify-between">
                          <span>Standard Lexicon</span>
                          <span className="text-purple-400 font-mono">{standard.sampleSigns.length} signs</span>
                        </div>
                        <div className="flex flex-wrap gap-1 max-h-20 overflow-y-auto pr-1">
                          {standard.sampleSigns.map(sign => (
                            <span
                              key={sign}
                              onClick={(e) => {
                                e.stopPropagation();
                                setViewMode('vocabulary');
                                setVocabQuery(sign);
                              }}
                              className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-900/90 text-purple-300 border border-slate-800 hover:border-purple-500/60 hover:text-white cursor-pointer transition"
                              title={`View "${sign}" in vocabulary`}
                            >
                              {sign}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-xs">
                      <span className="text-[10px] text-slate-500">
                        Authority: <span className="text-slate-400">{standard.standardizingBody}</span>
                      </span>

                      {onSelectDialect && (
                        <button
                          onClick={() => onSelectDialect(standard.id)}
                          className={`px-3 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
                            isSelected
                              ? 'bg-emerald-600 text-white shadow'
                              : 'bg-slate-900 hover:bg-slate-850 text-slate-200 border border-slate-700/80 hover:border-indigo-500'
                          }`}
                        >
                          {isSelected ? (
                            <>
                              <Check className="w-3.5 h-3.5" />
                              <span>Selected</span>
                            </>
                          ) : (
                            <span>Set as Active Standard</span>
                          )}
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* ══════════════════════════════════════════════════════════════════════════
          VIEW 2: STANDARD ISL SIGN VOCABULARY (42 STANDARDIZED SIGNS)
         ══════════════════════════════════════════════════════════════════════════ */}
      {viewMode === 'vocabulary' && (
        <div className="space-y-5 animate-in fade-in duration-200">
          {/* Category Filter Pills & Search */}
          <div className="space-y-3">
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
                <input
                  type="text"
                  value={vocabQuery}
                  onChange={e => { setVocabQuery(e.target.value); resetPage(); }}
                  placeholder="Search standard ISL signs, Hindi, Tamil…"
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-9 py-2.5 text-sm text-slate-100 placeholder-slate-600 focus:outline-none focus:border-indigo-500 transition"
                />
                {vocabQuery && (
                  <button
                    onClick={() => { setVocabQuery(''); resetPage(); }}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              {/* Model coverage filter */}
              <div className="flex items-center space-x-1.5 text-xs font-semibold">
                <button
                  onClick={() => { setModelFilter(null); resetPage(); }}
                  className={`px-3 py-1.5 rounded-xl border transition ${
                    modelFilter === null
                      ? 'bg-indigo-600 text-white border-indigo-500 shadow'
                      : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-slate-200'
                  }`}
                >
                  All Standard ({totalDict})
                </button>
                <button
                  onClick={() => { setModelFilter(true); resetPage(); }}
                  className={`flex items-center space-x-1 px-3 py-1.5 rounded-xl border transition ${
                    modelFilter === true
                      ? 'bg-emerald-700 text-white border-emerald-500 shadow'
                      : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-slate-200'
                  }`}
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>AI Recognizes ({totalSupported})</span>
                </button>
              </div>
            </div>

            {/* Category pills */}
            <div className="flex flex-wrap gap-1.5">
              {ISL_CATEGORIES.map(cat => (
                <button
                  key={cat.id}
                  onClick={() => { setCategoryId(cat.id); resetPage(); }}
                  className={`px-3 py-1.5 rounded-xl border text-xs font-semibold transition ${
                    categoryId === cat.id
                      ? 'bg-indigo-600 text-white border-indigo-500 shadow'
                      : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-slate-200'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>
          </div>

          {/* Results Count */}
          <div className="text-xs text-slate-500 font-mono">
            {vocabResults.length} standard sign{vocabResults.length !== 1 ? 's' : ''} found
            {vocabQuery && <> for "<span className="text-indigo-300">{vocabQuery}</span>"</>}
            {categoryId !== 'all' && <> in <span className="text-indigo-300">{ISL_CATEGORIES.find(c => c.id === categoryId)?.label}</span></>}
          </div>

          {/* Card Grid */}
          {pageResults.length === 0 ? (
            <div className="text-center py-16 text-slate-500 space-y-2">
              <BookOpen className="w-10 h-10 text-slate-700 mx-auto" />
              <p className="font-semibold">No standard signs found.</p>
              <p className="text-xs">Try a different search term or category.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {pageResults.map(entry => {
                const isExpanded = expandedSignId === entry.id;
                return (
                  <div
                    key={entry.id}
                    className={`glass-panel rounded-2xl border transition-all duration-200 ${
                      entry.modelSupported
                        ? 'border-slate-800/80 hover:border-emerald-500/30'
                        : 'border-slate-800/60 hover:border-amber-500/20'
                    }`}
                  >
                    <div className="p-4 space-y-3">
                      {/* Top row: gloss + model badge */}
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <div className="font-black text-lg text-white font-mono tracking-tight">
                            {entry.gloss}
                          </div>
                          <div className="text-[10px] text-slate-500 mt-0.5">{entry.en}</div>
                        </div>
                        <div className={`flex items-center space-x-1 px-2 py-0.5 rounded-full text-[10px] font-bold border flex-shrink-0 ${
                          entry.modelSupported
                            ? 'bg-emerald-950/80 border-emerald-500/40 text-emerald-300'
                            : 'bg-amber-950/80 border-amber-500/40 text-amber-300'
                        }`}>
                          {entry.modelSupported
                            ? <><CheckCircle2 className="w-3 h-3" /><span>AI READY</span></>
                            : <><AlertCircle className="w-3 h-3" /><span>PENDING DATA</span></>
                          }
                        </div>
                      </div>

                      {/* Spoken Translations */}
                      <div className="space-y-1 text-xs">
                        <div className="flex items-center space-x-2">
                          <span className="text-slate-600 w-12 text-right text-[10px]">Hindi</span>
                          <span className="text-slate-300 font-medium">{entry.hi}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="text-slate-600 w-12 text-right text-[10px]">Tamil</span>
                          <span className="text-slate-300 font-medium">{entry.ta}</span>
                        </div>
                      </div>

                      {/* Category + ISLRTC Source */}
                      <div className="flex flex-wrap gap-1.5">
                        <span className="flex items-center space-x-1 px-2 py-0.5 rounded-full bg-slate-900 border border-slate-800 text-[10px] text-slate-400">
                          <Tag className="w-2.5 h-2.5" />
                          <span>{ISL_CATEGORIES.find(c => c.id === entry.category)?.label || entry.category}</span>
                        </span>
                        <span className="px-2 py-0.5 rounded-full bg-indigo-950/50 border border-indigo-500/30 text-[10px] text-indigo-300 font-mono">
                          ISLRTC Standard
                        </span>
                      </div>

                      {/* Expand button */}
                      <button
                        onClick={() => setExpandedSignId(isExpanded ? null : entry.id)}
                        className="text-[11px] text-indigo-400 hover:text-indigo-300 font-semibold transition"
                      >
                        {isExpanded ? 'Show less ▲' : 'Show details ▼'}
                      </button>

                      {/* Expanded details */}
                      {isExpanded && (
                        <div className="space-y-2 pt-2 border-t border-slate-800/60 text-xs">
                          <div>
                            <span className="text-slate-500 font-semibold text-[10px] uppercase">Official Gesture Execution:</span>
                            <p className="text-slate-300 mt-0.5">{entry.description}</p>
                          </div>
                          <div>
                            <span className="text-slate-500 font-semibold text-[10px] uppercase">Standard Authority:</span>
                            <p className="text-slate-400 mt-0.5 text-[10px]">{entry.source}</p>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center space-x-3 pt-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={safePage === 1}
                className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white disabled:opacity-30 transition"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>

              <span className="text-xs text-slate-400 font-mono">
                Page {safePage} of {totalPages}
              </span>

              <button
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={safePage === totalPages}
                className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white disabled:opacity-30 transition"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      )}

    </div>
  );
}
