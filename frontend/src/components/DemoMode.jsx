/**
 * DemoMode.jsx — Dedicated curated demonstration viewer.
 *
 * Strict design rules enforced here:
 * 1. NEVER sends any data to the live recognition model.
 * 2. ALL outputs come from pre-defined static example data.
 * 3. Every output carries a persistent "DEMO MODE — PREDEFINED EXAMPLE" banner.
 * 4. Reported confidence/FPS/accuracy metrics are NOT shown (they would be fabricated).
 * 5. A button to return to Live Translator is always visible.
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  RotateCcw,
  Volume2,
  VolumeX,
  ChevronRight,
  AlertTriangle,
  Hand,
  ArrowLeft,
  BookOpen,
  Sparkles,
  Globe,
  CheckCircle2,
  Copy,
  Check,
  Video,
  Info,
} from 'lucide-react';

// ─────────────────────────────────────────────────────────────────────────────
// DEMO DATA — All outputs are statically authored, never model-generated.
// Each scenario has:
//   - title, icon, category
//   - isl_tokens: ordered gloss sequence
//   - translations: English, Hindi, Tamil (authored, not AI-translated)
//   - signing_description: prose description of what the signer does
//   - context: when / where this scenario applies
//   - video: null (no licensed video available)
// ─────────────────────────────────────────────────────────────────────────────
const DEMO_SCENARIOS = [
  {
    id: 'greeting',
    index: 0,
    category: 'Greetings & Social',
    icon: '👋',
    title: 'Basic Greeting and Introduction',
    subtitle: 'Scenario 1 of 6',
    context: 'Used when meeting someone new — at a clinic reception, police station, or public office.',
    isl_tokens: ['HELLO', 'ME', 'PLEASE', 'HELP'],
    signing_description:
      'The signer waves an open palm from the temple (HELLO), points to self (ME), rubs flat palm on chest (PLEASE), then lifts a fist on open palm (HELP).',
    translations: {
      en: 'Hello! Please help me.',
      hi: 'नमस्ते! कृपया मेरी मदद करें।',
      ta: 'வணக்கம்! தயவுசெய்து எனக்கு உதவுங்கள்.',
    },
    video: null,
    note: 'These glosses are drawn from the SignBridge model vocabulary. No signing video is available — consult a certified ISL interpreter for authentic demonstration.',
  },
  {
    id: 'water',
    index: 1,
    category: 'Daily Needs',
    icon: '💧',
    title: 'Asking for Water',
    subtitle: 'Scenario 2 of 6',
    context: 'Used when the signer is thirsty and needs drinking water at a hospital, waiting area, or public space.',
    isl_tokens: ['WATER', 'NEED', 'PLEASE'],
    signing_description:
      'The signer taps three fingers at the chin corner (WATER), makes a bent X hand move downward (NEED), then rubs palm on chest (PLEASE).',
    translations: {
      en: 'I need drinking water, please.',
      hi: 'मुझे पीने का पानी चाहिए, कृपया।',
      ta: 'எனக்கு குடிநீர் வேண்டும், தயவுசெய்து.',
    },
    video: null,
    note: 'NEED is not yet in the recognition model vocabulary. In live mode, only WATER and PLEASE are detected.',
  },
  {
    id: 'emergency',
    index: 2,
    category: 'Emergency & Health',
    icon: '🚑',
    title: 'Requesting Help in an Emergency',
    subtitle: 'Scenario 3 of 6',
    context: 'Used in a medical emergency — hospital triage, ambulance, or doctor\'s reception.',
    isl_tokens: ['DOCTOR', 'CHEST', 'PAIN', 'SEVERE'],
    signing_description:
      'The signer taps right fingers on left wrist (DOCTOR), presses palms to chest (CHEST), twists index fingers at torso (PAIN), then brings both hands sharply down (SEVERE).',
    translations: {
      en: 'Doctor, I am experiencing severe chest pain.',
      hi: 'डॉक्टर, मुझे सीने में बहुत तेज़ दर्द हो रहा है।',
      ta: 'மருத்துவரே, எனக்கு கடுமையான மார்பு வலி உள்ளது.',
    },
    video: null,
    note: 'All four glosses are in the recognition model vocabulary. This is the highest-confidence scenario in the current model.',
  },
  {
    id: 'directions',
    index: 3,
    category: 'Navigation & Places',
    icon: '🧭',
    title: 'Asking for Directions',
    subtitle: 'Scenario 4 of 6',
    context: 'Used when the signer needs to find the nearest police station or public service.',
    isl_tokens: ['POLICE', 'STATION', 'WHERE'],
    signing_description:
      'The signer salutes near the right temple (POLICE), outlines a box shape at chest (STATION), then shrugs both open palms outward (WHERE).',
    translations: {
      en: 'Where is the nearest police station?',
      hi: 'निकटतम पुलिस स्टेशन कहाँ है?',
      ta: 'அருகிலுள்ள காவல் நிலையம் எங்கே இருக்கிறது?',
    },
    video: null,
    note: 'All three glosses are in the recognition model vocabulary.',
  },
  {
    id: 'hospital',
    index: 4,
    category: 'Emergency & Health',
    icon: '🏥',
    title: 'Visiting a Hospital',
    subtitle: 'Scenario 5 of 6',
    context: 'Used when the signer needs to ask how to reach the hospital.',
    isl_tokens: ['HOSPITAL', 'GO', 'HOW'],
    signing_description:
      'The signer forms a cross with index fingers (HOSPITAL), points forward (GO), then rolls both palms upward in a questioning gesture (HOW).',
    translations: {
      en: 'How do I go to the hospital?',
      hi: 'अस्पताल कैसे जाना है?',
      ta: 'மருத்துவமனைக்கு எப்படி செல்வது?',
    },
    video: null,
    note: 'All three glosses are in the recognition model vocabulary.',
  },
  {
    id: 'conversation',
    index: 5,
    category: 'Everyday Conversation',
    icon: '💬',
    title: 'Everyday Conversation',
    subtitle: 'Scenario 6 of 6',
    context: 'A general polite request — asking someone to wait for ten minutes.',
    isl_tokens: ['SIT', 'WAIT', '10', 'MINUTES'],
    signing_description:
      'The signer taps two fingers on horizontal fingers (SIT), raises both palms in a stop gesture (WAIT), shakes thumb-up fist (10), and rotates index finger on upright left palm (MINUTES).',
    translations: {
      en: 'Please sit down and wait for 10 minutes.',
      hi: 'कृपया बैठिए और 10 मिनट प्रतीक्षा करें।',
      ta: 'தயவுசெய்து உட்கார்ந்து 10 நிமிடங்கள் காத்திருங்கள்.',
    },
    video: null,
    note: 'All four glosses are in the recognition model vocabulary.',
  },
];

// ─────────────────────────────────────────────────────────────────────────────
// Component
// ─────────────────────────────────────────────────────────────────────────────

export default function DemoMode({ onReturnToLive }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [tokenIndex, setTokenIndex] = useState(-1);   // -1 = all shown; 0..n = animated
  const [isAutoSpeak, setIsAutoSpeak] = useState(false);
  const [selectedLang, setSelectedLang] = useState('en');
  const [copiedLang, setCopiedLang] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const playIntervalRef = useRef(null);

  const scenario = DEMO_SCENARIOS[currentIndex];

  // Clear interval on scenario change
  useEffect(() => {
    stopAnimation();
    setTokenIndex(-1);
  }, [currentIndex]);

  // Auto-speak when animation completes
  useEffect(() => {
    if (tokenIndex === scenario.isl_tokens.length - 1) {
      stopAnimation();
      setIsPlaying(false);
      if (isAutoSpeak) {
        speakText(scenario.translations[selectedLang], selectedLang);
      }
    }
  }, [tokenIndex]);

  const startAnimation = () => {
    stopAnimation();
    setTokenIndex(0);
    setIsPlaying(true);

    let idx = 0;
    playIntervalRef.current = setInterval(() => {
      idx += 1;
      setTokenIndex(idx);
      if (idx >= scenario.isl_tokens.length - 1) {
        clearInterval(playIntervalRef.current);
        playIntervalRef.current = null;
        setIsPlaying(false);
      }
    }, 900);
  };

  const stopAnimation = () => {
    if (playIntervalRef.current) {
      clearInterval(playIntervalRef.current);
      playIntervalRef.current = null;
    }
    setIsPlaying(false);
  };

  const restartDemo = () => {
    stopAnimation();
    setTokenIndex(-1);
    setTimeout(startAnimation, 50);
  };

  const goNext = () => {
    stopAnimation();
    setCurrentIndex(prev => Math.min(prev + 1, DEMO_SCENARIOS.length - 1));
  };

  const goPrev = () => {
    stopAnimation();
    setCurrentIndex(prev => Math.max(prev - 1, 0));
  };

  const speakText = (text, lang) => {
    if (!('speechSynthesis' in window) || !text) return;
    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(text);
    utt.lang = lang === 'hi' ? 'hi-IN' : lang === 'ta' ? 'ta-IN' : 'en-IN';
    utt.rate = 0.9;
    utt.onstart = () => setIsSpeaking(true);
    utt.onend = () => setIsSpeaking(false);
    utt.onerror = () => setIsSpeaking(false);
    window.speechSynthesis.speak(utt);
  };

  const copyText = (text, lang) => {
    navigator.clipboard.writeText(text).catch(() => {});
    setCopiedLang(lang);
    setTimeout(() => setCopiedLang(null), 2000);
  };

  const LANG_LABELS = { en: 'English', hi: 'हिन्दी', ta: 'தமிழ்' };

  const visibleTokens = tokenIndex === -1
    ? scenario.isl_tokens
    : scenario.isl_tokens.slice(0, tokenIndex + 1);

  return (
    <div className="w-full space-y-5 max-w-5xl mx-auto">

      {/* ── PERSISTENT DEMO MODE BANNER ────────────────────────────────── */}
      <div className="flex items-center justify-between gap-3 p-3 rounded-2xl bg-amber-950/80 border border-amber-500/60 shadow-lg">
        <div className="flex items-center space-x-2.5">
          <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0 animate-pulse" />
          <div>
            <span className="text-xs font-extrabold text-amber-200 uppercase tracking-widest">
              DEMO MODE — PREDEFINED EXAMPLE
            </span>
            <p className="text-[11px] text-amber-400 mt-0.5">
              Outputs are statically authored examples, NOT live AI recognition results.
              No webcam data is used. No model inference is running.
            </p>
          </div>
        </div>
        <button
          onClick={onReturnToLive}
          className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow transition flex-shrink-0"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Live Translator</span>
        </button>
      </div>

      {/* ── SCENARIO LIST + VIEWER ─────────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">

        {/* Left: Scenario List */}
        <div className="lg:col-span-4 space-y-2">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-1 pb-1 border-b border-slate-800">
            Curated Scenarios
          </div>
          {DEMO_SCENARIOS.map((sc, idx) => (
            <button
              key={sc.id}
              onClick={() => setCurrentIndex(idx)}
              className={`w-full text-left p-3 rounded-2xl border transition text-xs font-semibold ${
                idx === currentIndex
                  ? 'bg-indigo-600/20 border-indigo-500/60 text-white'
                  : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
              }`}
            >
              <div className="flex items-center space-x-2.5">
                <span className="text-lg">{sc.icon}</span>
                <div>
                  <div className="font-bold">{sc.title}</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">{sc.category}</div>
                </div>
              </div>
            </button>
          ))}
        </div>

        {/* Right: Scenario Viewer */}
        <div className="lg:col-span-8 space-y-4">

          {/* Header */}
          <div className="glass-panel rounded-2xl p-5 border border-slate-800/80 space-y-1">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2.5">
                <span className="text-2xl">{scenario.icon}</span>
                <div>
                  <h2 className="text-base font-black text-white">{scenario.title}</h2>
                  <p className="text-[11px] text-slate-400">{scenario.subtitle} · {scenario.category}</p>
                </div>
              </div>
              {/* Progress dots */}
              <div className="flex items-center space-x-1.5">
                {DEMO_SCENARIOS.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setCurrentIndex(i)}
                    className={`w-2.5 h-2.5 rounded-full transition ${
                      i === currentIndex ? 'bg-indigo-400' : 'bg-slate-700 hover:bg-slate-600'
                    }`}
                    aria-label={`Go to scenario ${i + 1}`}
                  />
                ))}
              </div>
            </div>
            <p className="text-xs text-slate-400 pt-1 border-t border-slate-800/60 mt-2">
              <span className="text-slate-500 font-semibold">Context: </span>{scenario.context}
            </p>
          </div>

          {/* Video Placeholder */}
          <div className="rounded-2xl border border-slate-800/80 bg-slate-950/80 overflow-hidden">
            <div className="aspect-[16/7] flex flex-col items-center justify-center space-y-3 p-6">
              <Video className="w-10 h-10 text-slate-700" />
              <div className="text-center space-y-1">
                <p className="text-sm font-semibold text-slate-500">No signing video available</p>
                <p className="text-xs text-slate-600 max-w-md">
                  No licensed ISL demonstration video exists for this scenario.
                  The animated token sequence below is an illustrative placeholder only.
                  For authentic ISL, please consult a certified interpreter.
                </p>
              </div>
            </div>

            {/* Token Animation */}
            <div className="p-4 border-t border-slate-800/60 space-y-3">
              <div className="flex items-center justify-between text-[11px] font-bold text-slate-400 uppercase">
                <span>ISL Token Sequence</span>
                <span className="font-mono text-indigo-400">Illustrative — not live AI</span>
              </div>

              <div className="flex flex-wrap items-center gap-2 min-h-[48px]">
                {scenario.isl_tokens.map((token, i) => {
                  const isActive = tokenIndex === -1 || i <= tokenIndex;
                  const isCurrent = i === tokenIndex;
                  return (
                    <React.Fragment key={`${token}-${i}`}>
                      <div className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold font-mono transition-all duration-300 ${
                        isCurrent
                          ? 'bg-indigo-600/40 border-indigo-400 text-white scale-110 shadow-lg shadow-indigo-500/20'
                          : isActive
                          ? 'bg-slate-800 border-slate-700 text-slate-200'
                          : 'bg-slate-950 border-slate-900 text-slate-600'
                      }`}>
                        <Sparkles className={`w-3 h-3 ${isCurrent ? 'text-indigo-300 animate-spin' : isActive ? 'text-slate-500' : 'text-slate-700'}`} />
                        <span>{token}</span>
                      </div>
                      {i < scenario.isl_tokens.length - 1 && (
                        <ChevronRight className={`w-3.5 h-3.5 ${isActive ? 'text-slate-500' : 'text-slate-800'}`} />
                      )}
                    </React.Fragment>
                  );
                })}
              </div>

              {/* Signing Description */}
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-[11px] text-slate-400">
                <span className="text-slate-500 font-semibold">Signing: </span>
                {scenario.signing_description}
              </div>
            </div>
          </div>

          {/* Playback Controls */}
          <div className="flex items-center justify-between gap-3 p-3 bg-slate-950/80 rounded-2xl border border-slate-800">
            <div className="flex items-center space-x-2">
              <button
                onClick={goPrev}
                disabled={currentIndex === 0}
                className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white disabled:opacity-30 transition"
              >
                <SkipBack className="w-4 h-4" />
              </button>

              <button
                onClick={isPlaying ? stopAnimation : startAnimation}
                className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold shadow transition ${
                  isPlaying
                    ? 'bg-red-600 hover:bg-red-500 text-white'
                    : 'bg-indigo-600 hover:bg-indigo-500 text-white'
                }`}
              >
                {isPlaying
                  ? <><Pause className="w-3.5 h-3.5" /><span>Pause</span></>
                  : <><Play className="w-3.5 h-3.5 fill-current" /><span>Play Sequence</span></>
                }
              </button>

              <button
                onClick={restartDemo}
                className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition"
                title="Restart demonstration"
              >
                <RotateCcw className="w-4 h-4" />
              </button>

              <button
                onClick={goNext}
                disabled={currentIndex === DEMO_SCENARIOS.length - 1}
                className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white disabled:opacity-30 transition"
              >
                <SkipForward className="w-4 h-4" />
              </button>
            </div>

            <div className="flex items-center space-x-2">
              {/* Auto-speak toggle */}
              <button
                onClick={() => setIsAutoSpeak(!isAutoSpeak)}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-xl border text-xs font-semibold transition ${
                  isAutoSpeak
                    ? 'bg-purple-600/20 border-purple-500/50 text-purple-300'
                    : 'bg-slate-900 border-slate-700 text-slate-400 hover:text-slate-200'
                }`}
              >
                {isAutoSpeak ? <Volume2 className="w-3.5 h-3.5 animate-pulse" /> : <VolumeX className="w-3.5 h-3.5" />}
                <span>Auto-speak</span>
              </button>

              {/* Language selector */}
              <div className="flex items-center space-x-1 bg-slate-900 p-1 rounded-xl border border-slate-800">
                {['en', 'hi', 'ta'].map(lang => (
                  <button
                    key={lang}
                    onClick={() => setSelectedLang(lang)}
                    className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition ${
                      selectedLang === lang
                        ? 'bg-indigo-600 text-white'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {LANG_LABELS[lang]}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Translation Output */}
          <div className="glass-panel rounded-2xl p-5 border border-slate-800/80 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-xs font-bold text-slate-300 uppercase tracking-wider">
                <Globe className="w-4 h-4 text-indigo-400" />
                <span>Translation Output</span>
              </div>
              <span className="text-[10px] font-bold text-amber-300 bg-amber-950/80 border border-amber-500/40 px-2 py-0.5 rounded-full">
                DEMO EXAMPLE — NOT AI GENERATED
              </span>
            </div>

            {/* Primary output */}
            <div className="p-4 rounded-2xl bg-gradient-to-br from-slate-950 via-indigo-950/20 to-slate-950 border border-indigo-500/30 space-y-3">
              <p className="text-xl font-bold text-white">
                "{scenario.translations[selectedLang]}"
              </p>
              <div className="flex items-center justify-between border-t border-slate-800/80 pt-2">
                <span className="text-[11px] text-slate-500 font-mono">
                  {LANG_LABELS[selectedLang]} · Authored translation
                </span>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => copyText(scenario.translations[selectedLang], selectedLang)}
                    className="flex items-center space-x-1 text-slate-400 hover:text-indigo-300 text-[11px] transition"
                  >
                    {copiedLang === selectedLang ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                    <span>{copiedLang === selectedLang ? 'Copied' : 'Copy'}</span>
                  </button>
                  <button
                    onClick={() => speakText(scenario.translations[selectedLang], selectedLang)}
                    disabled={isSpeaking}
                    className="flex items-center space-x-1 text-slate-400 hover:text-indigo-300 text-[11px] transition"
                  >
                    <Volume2 className={`w-3.5 h-3.5 ${isSpeaking ? 'text-purple-400 animate-pulse' : ''}`} />
                    <span>{isSpeaking ? 'Playing...' : 'Speak'}</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Secondary outputs (other languages) */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {['en', 'hi', 'ta'].map(lang => {
                const colors = {
                  en: 'border-indigo-800/50 bg-indigo-950/20',
                  hi: 'border-amber-800/50 bg-amber-950/20',
                  ta: 'border-emerald-800/50 bg-emerald-950/20',
                };
                const badges = {
                  en: 'text-indigo-300 bg-indigo-950 border-indigo-800/60',
                  hi: 'text-amber-300 bg-amber-950 border-amber-800/60',
                  ta: 'text-emerald-300 bg-emerald-950 border-emerald-800/60',
                };
                return (
                  <div key={lang} className={`p-3 rounded-xl border ${colors[lang]} space-y-1.5`}>
                    <div className="flex items-center justify-between">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase ${badges[lang]}`}>
                        {LANG_LABELS[lang]}
                      </span>
                      <button
                        onClick={() => speakText(scenario.translations[lang], lang)}
                        className="text-slate-500 hover:text-slate-300 transition"
                        title={`Speak in ${LANG_LABELS[lang]}`}
                      >
                        <Volume2 className="w-3 h-3" />
                      </button>
                    </div>
                    <p className="text-xs font-semibold text-slate-200 leading-relaxed">
                      "{scenario.translations[lang]}"
                    </p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Notes / Attribution */}
          <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 flex items-start space-x-2.5 text-xs text-slate-400">
            <Info className="w-4 h-4 text-indigo-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-slate-300">Note: </span>
              {scenario.note}
            </div>
          </div>

          {/* Navigation arrows (bottom) */}
          <div className="flex items-center justify-between text-xs font-semibold">
            <button
              onClick={goPrev}
              disabled={currentIndex === 0}
              className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white disabled:opacity-30 transition"
            >
              <SkipBack className="w-3.5 h-3.5" />
              <span>Previous</span>
            </button>

            <span className="text-slate-600">
              {currentIndex + 1} / {DEMO_SCENARIOS.length}
            </span>

            <button
              onClick={goNext}
              disabled={currentIndex === DEMO_SCENARIOS.length - 1}
              className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white disabled:opacity-30 transition"
            >
              <span>Next</span>
              <SkipForward className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
