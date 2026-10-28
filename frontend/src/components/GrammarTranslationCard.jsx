import React, { useState, useEffect } from 'react';
import { Volume2, VolumeX, Copy, Check, Languages, Sparkles, BookOpen, ArrowRight } from 'lucide-react';

export default function GrammarTranslationCard({ translations, grammarAlignment, isAutoSpeak, setIsAutoSpeak }) {
  const [copiedLang, setCopiedLang] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [activeLang, setActiveLang] = useState('en');

  const enText = translations?.en || "Doctor, I am experiencing severe chest pain.";
  const hiText = translations?.hi || "डॉक्टर, मुझे सीने में बहुत तेज़ दर्द हो रहा है।";
  const taText = translations?.ta || "மருத்துவரே, எனக்கு கடுமையான மார்பு வலி உள்ளது.";

  // Text to Speech playback using Browser Web Speech API
  const speakText = (text, langCode) => {
    if (!('speechSynthesis' in window)) {
      console.warn("Web Speech API not supported in this browser.");
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    
    if (langCode === 'hi') utterance.lang = 'hi-IN';
    else if (langCode === 'ta') utterance.lang = 'ta-IN';
    else utterance.lang = 'en-IN';

    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  // Auto-speak trigger on translation change if enabled
  useEffect(() => {
    if (isAutoSpeak && enText) {
      speakText(enText, 'en');
    }
  }, [enText, isAutoSpeak]);

  const copyToClipboard = (text, lang) => {
    navigator.clipboard.writeText(text);
    setCopiedLang(lang);
    setTimeout(() => setCopiedLang(null), 2000);
  };

  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-700/60 shadow-2xl flex flex-col space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-purple-600/20 border border-purple-500/40 text-purple-400">
            <Languages className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-100 flex items-center space-x-2">
              <span>NLP Grammar Synthesis & Audio Translation</span>
              <span className="px-2 py-0.5 rounded-full text-[10px] bg-purple-950/80 border border-purple-500/40 text-purple-300 font-mono">
                Multilingual SVO/SOV
              </span>
            </h3>
            <p className="text-xs text-slate-400">Topic-Comment reordering with sub-150 ms speech output</p>
          </div>
        </div>

        {/* Auto-Speak Toggle */}
        <button
          onClick={() => setIsAutoSpeak(!isAutoSpeak)}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-xl border text-xs font-semibold transition ${
            isAutoSpeak
              ? 'bg-purple-600/30 border-purple-500 text-purple-200'
              : 'bg-slate-900 border-slate-700 text-slate-400 hover:text-slate-200'
          }`}
        >
          {isAutoSpeak ? <Volume2 className="w-3.5 h-3.5 text-purple-400 animate-pulse" /> : <VolumeX className="w-3.5 h-3.5 text-slate-500" />}
          <span>Auto-Speak</span>
        </button>
      </div>

      {/* Multilingual Translation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {/* English Card */}
        <div className="bg-slate-950/80 rounded-xl p-3.5 border border-slate-800 flex flex-col justify-between space-y-2 hover:border-slate-700 transition">
          <div className="flex items-center justify-between">
            <span className="px-2 py-0.5 rounded bg-indigo-950/80 text-indigo-300 text-[10px] font-bold uppercase tracking-wider border border-indigo-800/60">
              English (Spoken)
            </span>
            <div className="flex items-center space-x-1">
              <button
                onClick={() => copyToClipboard(enText, 'en')}
                className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition"
                title="Copy to clipboard"
              >
                {copiedLang === 'en' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
              <button
                onClick={() => speakText(enText, 'en')}
                className="p-1.5 rounded-lg bg-indigo-600/30 text-indigo-300 hover:bg-indigo-600 hover:text-white transition"
                title="Play English Speech"
              >
                <Volume2 className="w-4 h-4" />
              </button>
            </div>
          </div>
          <p className="text-sm font-semibold text-slate-100 leading-snug">
            "{enText}"
          </p>
        </div>

        {/* Hindi Card */}
        <div className="bg-slate-950/80 rounded-xl p-3.5 border border-slate-800 flex flex-col justify-between space-y-2 hover:border-slate-700 transition">
          <div className="flex items-center justify-between">
            <span className="px-2 py-0.5 rounded bg-amber-950/80 text-amber-300 text-[10px] font-bold uppercase tracking-wider border border-amber-800/60">
              Hindi (हिन्दी)
            </span>
            <div className="flex items-center space-x-1">
              <button
                onClick={() => copyToClipboard(hiText, 'hi')}
                className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition"
                title="Copy to clipboard"
              >
                {copiedLang === 'hi' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
              <button
                onClick={() => speakText(hiText, 'hi')}
                className="p-1.5 rounded-lg bg-amber-600/30 text-amber-300 hover:bg-amber-600 hover:text-white transition"
                title="Play Hindi Speech"
              >
                <Volume2 className="w-4 h-4" />
              </button>
            </div>
          </div>
          <p className="text-sm font-semibold text-slate-100 leading-snug">
            "{hiText}"
          </p>
        </div>

        {/* Tamil Card */}
        <div className="bg-slate-950/80 rounded-xl p-3.5 border border-slate-800 flex flex-col justify-between space-y-2 hover:border-slate-700 transition">
          <div className="flex items-center justify-between">
            <span className="px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-300 text-[10px] font-bold uppercase tracking-wider border border-emerald-800/60">
              Tamil (தமிழ்)
            </span>
            <div className="flex items-center space-x-1">
              <button
                onClick={() => copyToClipboard(taText, 'ta')}
                className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition"
                title="Copy to clipboard"
              >
                {copiedLang === 'ta' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
              <button
                onClick={() => speakText(taText, 'ta')}
                className="p-1.5 rounded-lg bg-emerald-600/30 text-emerald-300 hover:bg-emerald-600 hover:text-white transition"
                title="Play Tamil Speech"
              >
                <Volume2 className="w-4 h-4" />
              </button>
            </div>
          </div>
          <p className="text-sm font-semibold text-slate-100 leading-snug">
            "{taText}"
          </p>
        </div>
      </div>

      {/* Syntactic Alignment Explanation (Topic-Comment vs Natural Sentence) */}
      <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/90 space-y-2 text-xs">
        <div className="flex items-center space-x-2 text-slate-400 font-semibold uppercase tracking-wider text-[11px]">
          <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
          <span>ISL Topic-Comment Syntactic Alignment:</span>
        </div>

        <div className="flex flex-wrap items-center gap-2 pt-1">
          {grammarAlignment && grammarAlignment.length > 0 ? (
            grammarAlignment.map((item, idx) => (
              <div key={idx} className="flex items-center space-x-1.5 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800">
                <span className="font-mono text-indigo-300 font-bold">{item.isl_gloss}</span>
                <ArrowRight className="w-3 h-3 text-slate-600" />
                <span className="text-slate-300 font-medium">{item.spoken_word}</span>
                <span className="text-[9px] px-1 rounded bg-slate-800 text-slate-400 font-mono">{item.syntactic_role}</span>
              </div>
            ))
          ) : (
            <div className="flex items-center space-x-1.5 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800">
              <span className="font-mono text-indigo-300 font-bold">DOCTOR</span>
              <ArrowRight className="w-3 h-3 text-slate-600" />
              <span className="text-slate-300 font-medium">Doctor</span>
              <span className="text-[9px] px-1 rounded bg-slate-800 text-slate-400 font-mono">NOUN</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
