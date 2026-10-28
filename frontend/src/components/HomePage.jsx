import React, { useState } from 'react';
import {
  Hand,
  Sparkles,
  ArrowRight,
  Play,
  CheckCircle2,
  Cpu,
  Activity,
  Volume2,
  Layers,
  Zap,
  Globe,
  Eye,
  Check,
  ChevronDown,
  Camera,
  MessageSquare,
  BookOpen,
  Settings,
  ShieldCheck,
  Info
} from 'lucide-react';
import LivingLogo from './LivingLogo';

export default function HomePage({
  onNavigate,
  onStartTranslating,
  selectedLanguage,
  onSelectLanguage,
  onOpenSettings,
  onOpenA11y,
  isServerConnected
}) {
  const [isLangDropdownOpen, setIsLangDropdownOpen] = useState(false);

  const supportedLanguages = [
    { id: 'en', name: 'English', native: 'English', supported: true, flag: '🌐' },
    { id: 'hi', name: 'Hindi', native: 'हिन्दी', supported: true, flag: '🇮🇳' },
    { id: 'ta', name: 'Tamil', native: 'தமிழ்', supported: true, flag: '🇮🇳' },
    { id: 'te', name: 'Telugu', native: 'తెలుగు', supported: false, flag: '🇮🇳' },
    { id: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ', supported: false, flag: '🇮🇳' },
    { id: 'ml', name: 'Malayalam', native: 'മലയാളം', supported: false, flag: '🇮🇳' }
  ];

  const currentLangObj = supportedLanguages.find(l => l.id === selectedLanguage) || supportedLanguages[0];

  const handleLanguagePick = (lang) => {
    if (lang.supported) {
      if (onSelectLanguage) onSelectLanguage(lang.id);
      setIsLangDropdownOpen(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex flex-col justify-between p-4 sm:p-6 lg:p-8 relative overflow-hidden">
      {/* Background ambient lighting */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[450px] bg-gradient-to-r from-purple-600/15 via-blue-600/15 to-cyan-600/15 rounded-full blur-3xl pointer-events-none"></div>

      {/* TOP HEADER / NAVBAR (FULL PAGE) */}
      <header className="w-full max-w-7xl mx-auto flex items-center justify-between z-20 pb-4">
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-purple-600 via-indigo-600 to-cyan-400 p-0.5 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <div className="w-full h-full bg-[#050609] rounded-[14px] flex items-center justify-center">
              <Hand className="w-5 h-5 text-cyan-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-lg text-white tracking-tight">ISL AI</span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-950/80 border border-indigo-500/40 text-indigo-300">
                Real-Time
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">Indian Sign Language AI Translator</p>
          </div>
        </div>

        {/* Top Navigation Links */}
        <nav className="flex items-center space-x-2 sm:space-x-3">
          <button
            onClick={() => onNavigate && onNavigate('dictionary')}
            className="hidden md:flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent hover:border-slate-800 transition"
          >
            <BookOpen className="w-3.5 h-3.5 text-cyan-400" />
            <span>Dictionary</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('learn')}
            className="hidden md:flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent hover:border-slate-800 transition"
          >
            <Cpu className="w-3.5 h-3.5 text-purple-400" />
            <span>Learn ISL</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('demo')}
            className="hidden sm:flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-amber-300 hover:text-white hover:bg-amber-950/40 border border-amber-500/30 transition"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>Demo Mode</span>
          </button>

          {onOpenA11y && (
            <button
              onClick={onOpenA11y}
              className="p-2 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-300 hover:text-white text-xs transition"
              title="Accessibility Controls"
            >
              ♿
            </button>
          )}

          {onOpenSettings && (
            <button
              onClick={onOpenSettings}
              className="p-2 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-400 hover:text-white transition"
              title="Settings"
            >
              <Settings className="w-4 h-4" />
            </button>
          )}

          <button
            onClick={onStartTranslating}
            className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-purple-600/25 transition transform active:scale-95"
          >
            <Hand className="w-3.5 h-3.5" />
            <span>Open Translator</span>
          </button>
        </nav>
      </header>

      {/* HERO SECTION (MAIN CENTERSTAGE) */}
      <main className="w-full max-w-5xl mx-auto flex-1 flex flex-col justify-center items-center py-6 sm:py-10 z-10">
        <section className="relative w-full rounded-3xl overflow-hidden glass-panel border border-slate-800/80 p-6 sm:p-12 lg:p-14 shadow-2xl text-center flex flex-col items-center space-y-7">
          {/* Subtle Background Radial Glows */}
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[350px] bg-gradient-to-r from-purple-600/15 via-blue-600/15 to-cyan-600/15 rounded-full blur-3xl pointer-events-none"></div>

          {/* 1. THE LIVING LOGO ⭐ */}
          <div className="w-full flex justify-center z-10">
            <LivingLogo />
          </div>

          {/* 2. HERO HEADINGS */}
          <div className="space-y-4 max-w-4xl z-10">
            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight text-white leading-[1.08]">
              Breaking Communication<br />
              Barriers <span className="bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">with AI</span>
            </h1>

            <p className="text-base sm:text-xl font-bold bg-gradient-to-r from-indigo-300 via-cyan-300 to-emerald-300 bg-clip-text text-transparent tracking-wide">
              Real-Time Indian Sign Language to Text &amp; Speech Translation
            </p>

            <p className="text-xs sm:text-base text-slate-400 leading-relaxed max-w-2xl mx-auto font-medium">
              Translate continuous Indian Sign Language into natural language text and speech using advanced AI, Computer Vision, and NLP.
            </p>
          </div>

          {/* 3. HOMEPAGE LANGUAGE SELECTOR ⭐ */}
          <div className="relative z-30 flex flex-col items-center space-y-2">
            <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
              Select Output Language
            </label>

            <div className="relative">
              <button
                onClick={() => setIsLangDropdownOpen(!isLangDropdownOpen)}
                className="flex items-center space-x-3 px-5 py-3 rounded-2xl bg-slate-900/90 hover:bg-slate-850 border border-slate-700/80 hover:border-indigo-500/60 text-slate-100 font-semibold text-xs sm:text-sm shadow-xl transition-all duration-200"
              >
                <span className="text-base">{currentLangObj.flag}</span>
                <span className="font-bold">{currentLangObj.name} ({currentLangObj.native})</span>
                <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform duration-200 ${isLangDropdownOpen ? 'rotate-180' : ''}`} />
              </button>

              {/* Language Dropdown Menu */}
              {isLangDropdownOpen && (
                <div className="absolute top-full mt-2 w-72 bg-slate-950/95 backdrop-blur-xl border border-slate-700/80 rounded-2xl shadow-2xl p-2 z-50 divide-y divide-slate-800/60 animate-in fade-in zoom-in-95 duration-150">
                  <div className="p-2 text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                    Target Translation Dialect
                  </div>
                  <div className="py-1 space-y-1">
                    {supportedLanguages.map((lang) => {
                      const isSelected = selectedLanguage === lang.id;
                      return (
                        <button
                          key={lang.id}
                          disabled={!lang.supported}
                          onClick={() => handleLanguagePick(lang)}
                          className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition ${
                            isSelected
                              ? 'bg-indigo-600 text-white'
                              : lang.supported
                              ? 'text-slate-300 hover:text-white hover:bg-slate-800/70'
                              : 'text-slate-600 cursor-not-allowed bg-transparent'
                          }`}
                        >
                          <div className="flex items-center space-x-2.5">
                            <span>{lang.flag}</span>
                            <span>{lang.name} — <span className="font-normal opacity-80">{lang.native}</span></span>
                          </div>

                          {isSelected ? (
                            <Check className="w-3.5 h-3.5 text-white" />
                          ) : !lang.supported ? (
                            <span className="text-[9px] px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-500 font-mono">
                              Coming soon
                            </span>
                          ) : null}
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* 4. PRIMARY & SECONDARY CTA BUTTONS */}
          <div className="flex flex-wrap items-center justify-center gap-4 pt-2 z-10">
            {/* Primary CTA */}
            <button
              onClick={() => onStartTranslating ? onStartTranslating() : onNavigate('translator')}
              className="group relative inline-flex items-center space-x-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-500 hover:from-purple-500 hover:via-indigo-500 hover:to-cyan-400 text-white font-extrabold text-sm sm:text-base shadow-xl shadow-indigo-600/30 hover:shadow-indigo-600/50 hover:scale-105 active:scale-100 transition-all duration-300"
            >
              <Hand className="w-5 h-5 group-hover:rotate-12 transition-transform duration-300" />
              <span>Start Translating</span>
              <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1.5 transition-transform duration-300" />
            </button>

            {/* Secondary CTA */}
            <button
              onClick={() => onNavigate('about')}
              className="inline-flex items-center space-x-2 px-6 py-4 rounded-2xl bg-slate-900/60 hover:bg-slate-800/80 border border-slate-700/80 hover:border-slate-500 text-slate-200 hover:text-white font-bold text-sm sm:text-base transition duration-200"
            >
              <Play className="w-4 h-4 text-cyan-400 fill-cyan-400/20" />
              <span>See How It Works</span>
              <ArrowRight className="w-4 h-4 text-slate-400" />
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}
