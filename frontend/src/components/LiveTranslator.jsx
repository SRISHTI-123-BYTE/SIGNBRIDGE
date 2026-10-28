import React, { useState } from 'react';
import {
  Hand,
  Volume2,
  VolumeX,
  Play,
  Pause,
  RotateCcw,
  Sparkles,
  CheckCircle2,
  Cpu,
  Activity,
  Layers,
  ChevronRight,
  ChevronDown,
  ChevronUp,
  Clock,
  Zap,
  Globe,
  Copy,
  Check,
  BookOpen,
  ArrowRight,
  ShieldAlert,
  Compass,
  Building2,
  UserCheck,
  MessageSquare,
  Mic,
  Sliders,
  Radio,
  Eye,
  Camera,
  AlertTriangle,
  Lock,
  Send,
  Target
} from 'lucide-react';

import VisionTracker from './VisionTracker';
import Avatar3D from './Avatar3D';
import DemoMode from './DemoMode';
import SystemPipelineSection from './SystemPipelineSection';
import { signBridgeService } from '../services/api';
import { INDIAN_SIGN_LANGUAGES } from '../data/indianSignLanguages';

export default function LiveTranslator({
  activeGlosses,
  recognizedTokens,
  translations,
  grammarAlignment,
  nmmState,
  latencyMetrics,
  isStreaming,
  setIsStreaming,
  isAutoSpeak,
  setIsAutoSpeak,
  isServerConnected,
  recentHistory,
  onApplyScenario,
  onClearSession,
  onRecordSign,
  onNavigateToHistory,
  onNavigateToDemo,
  onNavigateToDictionary,
  selectedLanguage = 'en',
  onSelectLanguage,
  selectedDialect = 'isl-standard',
  onSelectDialect
}) {
  const [translatorMode, setTranslatorMode] = useState('sign-to-speech'); // 'sign-to-speech' | 'two-way' | 'demo'
  const [captureMode, setCaptureMode] = useState('on-demand'); // 'on-demand' (Default: Capture on Click) | 'continuous'
  const [isRecognitionPaused, setIsRecognitionPaused] = useState(false);
  const [activeLang, setActiveLang] = useState(selectedLanguage);
  const [copiedLang, setCopiedLang] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isDetailsExpanded, setIsDetailsExpanded] = useState(true);
  const [speechSpeed, setSpeechSpeed] = useState(1.0);
  const [volume, setVolume] = useState(1.0);

  // Two-Way Conversation Dialogue State (starts empty)
  const [conversationList, setConversationList] = useState([]);
  const [hearingInputText, setHearingInputText] = useState('');

  // Fallback / Defaults (starts clean and empty)
  const displayGlosses = activeGlosses && activeGlosses.length > 0
    ? activeGlosses
    : [];

  const topConfidence = recognizedTokens && recognizedTokens.length > 0
    ? Math.round(recognizedTokens[recognizedTokens.length - 1].confidence * 100)
    : 0;

  const totalLatency = latencyMetrics?.total_end_to_end_ms || 0;
  const enText = translations?.en || "";
  const hiText = translations?.hi || "";
  const taText = translations?.ta || "";

  const currentDialectObj = INDIAN_SIGN_LANGUAGES.find(d => d.id === selectedDialect) || INDIAN_SIGN_LANGUAGES[0];

  const effectiveLang = activeLang || selectedLanguage || 'en';
  const handleLangChange = (lang) => {
    setActiveLang(lang);
    if (onSelectLanguage) onSelectLanguage(lang);
  };

  const primaryText = effectiveLang === 'hi' ? hiText : effectiveLang === 'ta' ? taText : enText;
  const primaryLangLabel = effectiveLang === 'hi' ? 'Hindi (हिन्दी)' : effectiveLang === 'ta' ? 'Tamil (தமிழ்)' : 'English (Spoken)';

  // Emergency Mode Detection
  const isEmergencyActive =
    nmmState?.is_urgent ||
    (displayGlosses.length > 0 && displayGlosses.some(g => ['DOCTOR', 'PAIN', 'CHEST', 'SEVERE', 'HELP', 'HOSPITAL', 'POLICE'].includes(g)));

  // Quick canonical scenarios
  const quickScenarios = [
    { id: 'emergency', label: '🚑 Medical Emergency', glosses: ['DOCTOR', 'CHEST', 'PAIN', 'SEVERE'] },
    { id: 'police', label: '👮 Police Station', glosses: ['POLICE', 'STATION', 'WHERE'] },
    { id: 'hospital', label: '🏥 Hospital Route', glosses: ['HOSPITAL', 'GO', 'HOW'] },
    { id: 'banking', label: '🏦 Bank Deposit', glosses: ['MONEY', 'ACCOUNT', 'BANK', 'DEPOSIT'] },
    { id: 'assistance', label: '🤝 Need Help', glosses: ['HELP', 'ME', 'PLEASE'] }
  ];

  // Text-To-Speech Playback
  const speakText = (text, langCode = selectedLanguage) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    if (langCode === 'hi') utterance.lang = 'hi-IN';
    else if (langCode === 'ta') utterance.lang = 'ta-IN';
    else utterance.lang = 'en-IN';

    utterance.rate = speechSpeed;
    utterance.volume = volume;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  const stopSpeech = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  const copyToClipboard = (text, lang) => {
    navigator.clipboard.writeText(text);
    setCopiedLang(lang);
    setTimeout(() => setCopiedLang(null), 2000);
  };

  const handleSendHearingResponse = (e) => {
    e.preventDefault();
    if (!hearingInputText.trim()) return;

    const newMsg = {
      sender: 'hearing',
      label: 'Hearing Responder (Text/Voice)',
      text: hearingInputText,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setConversationList(prev => [...prev, newMsg]);
    setHearingInputText('');
  };

  // Auto-speak synthesized translation if enabled
  React.useEffect(() => {
    if (isAutoSpeak && primaryText && primaryText.trim().length > 0) {
      speakText(primaryText, selectedLanguage);
    }
  }, [primaryText, isAutoSpeak, selectedLanguage]);

  return (
    <div className="space-y-6">
      {/* 1. TOP HEADER & MODE SWITCHER */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-800/80 shadow-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-3">
            <h1 className="text-xl sm:text-2xl font-black tracking-tight text-white flex items-center space-x-2">
              <span>REAL-TIME CONTINUOUS ISL TRANSLATOR</span>
            </h1>
            <span className="flex items-center space-x-1.5 px-3 py-0.5 rounded-full text-[11px] font-mono font-bold bg-emerald-950/80 border border-emerald-500/40 text-emerald-300">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>AI ONLINE</span>
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-400 font-medium">
            Continuous MediaPipe 3D tracking, Temporal Transformer/ST-GCN sequence recognition, and Multilingual NLP synthesis.
          </p>
        </div>

        {/* Mode Selector Tabs */}
        <div className="flex items-center space-x-1.5 bg-slate-900/90 p-1.5 rounded-2xl border border-slate-800 text-xs font-semibold">
          <button
            onClick={() => setTranslatorMode('sign-to-speech')}
            className={`flex items-center space-x-1.5 px-4 py-2 rounded-xl transition ${
              translatorMode === 'sign-to-speech'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md font-bold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Hand className="w-4 h-4" />
            <span>Live Translator</span>
          </button>

          <button
            onClick={() => setTranslatorMode('demo')}
            className={`flex items-center space-x-1.5 px-4 py-2 rounded-xl transition ${
              translatorMode === 'demo'
                ? 'bg-gradient-to-r from-amber-600 to-indigo-600 text-white shadow-md font-bold'
                : 'text-amber-300 hover:text-white hover:bg-amber-950/40 border border-amber-500/40'
            }`}
          >
            <Sparkles className="w-4 h-4 text-amber-400" />
            <span>Demo Mode 🎬</span>
          </button>

          <button
            onClick={() => setTranslatorMode('two-way')}
            className={`flex items-center space-x-1.5 px-4 py-2 rounded-xl transition ${
              translatorMode === 'two-way'
                ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md font-bold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <MessageSquare className="w-4 h-4" />
            <span>Two-Way (3D)</span>
          </button>

          <button
            onClick={() => setTranslatorMode('pipeline')}
            className={`flex items-center space-x-1.5 px-4 py-2 rounded-xl transition ${
              translatorMode === 'pipeline'
                ? 'bg-gradient-to-r from-cyan-600 to-indigo-600 text-white shadow-md font-bold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>AI Pipeline &amp; Status</span>
          </button>
        </div>
      </div>

      {/* 2. MAIN VIEW BASED ON ACTIVE MODE */}
      {translatorMode === 'demo' ? (
        <DemoMode onReturnToLive={() => setTranslatorMode('sign-to-speech')} />
      ) : translatorMode === 'pipeline' ? (
        <SystemPipelineSection
          isStreaming={isStreaming}
          totalLatency={totalLatency}
          isServerConnected={isServerConnected}
          onReturnToLive={() => setTranslatorMode('sign-to-speech')}
        />
      ) : translatorMode === 'sign-to-speech' ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* LEFT SIDE: CAMERA, STATUS, AI PIPELINE & PRIVACY (6 COLS) */}
          <div className="lg:col-span-6 space-y-4">
            {/* Webcam / Simulator HUD */}
            <VisionTracker
              isStreaming={isStreaming}
              setIsStreaming={setIsStreaming}
              onRecordSign={onRecordSign}
              captureMode={captureMode}
              onLandmarksUpdate={(landmarks, meta) => {
                // In continuous mode, auto-stream to WebSocket.
                // In on-demand mode, do NOT stream while idle (signs are only captured when user clicks 'Capture Sign').
                if (captureMode === 'continuous' && !isRecognitionPaused) {
                  signBridgeService.sendLandmarks(landmarks, meta);
                }
              }}
            />

            {/* Live Translation Control Action Bar */}
            <div className="p-4 bg-slate-950/90 rounded-2xl border border-slate-800 space-y-3">
              {/* Indian Sign Language & Regional Dialect Selector */}
              <div className="flex flex-wrap items-center justify-between gap-2.5 p-2.5 rounded-xl bg-slate-900/90 border border-slate-800/80">
                <div className="flex items-center space-x-2.5 min-w-0">
                  <span className="text-xl p-1 bg-slate-950 rounded-lg border border-slate-800 flex-shrink-0">
                    {currentDialectObj.icon}
                  </span>
                  <div className="min-w-0">
                    <div className="flex items-center space-x-1.5">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                        Official Standard ISL:
                      </span>
                      <span className="px-1.5 py-0.2 rounded-full text-[9px] font-bold border bg-emerald-950/80 border-emerald-500/40 text-emerald-300">
                        ISLRTC Certified
                      </span>
                    </div>
                    <div className="text-xs font-bold text-white truncate">
                      {currentDialectObj.name}
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <select
                    value={selectedDialect}
                    onChange={(e) => onSelectDialect && onSelectDialect(e.target.value)}
                    className="bg-slate-950 border border-slate-700/80 rounded-xl px-2.5 py-1 text-xs font-semibold text-slate-200 focus:outline-none focus:border-indigo-500 transition shadow-inner cursor-pointer"
                    title="Select Indian Sign Language or Regional Dialect"
                  >
                    {INDIAN_SIGN_LANGUAGES.map(d => (
                      <option key={d.id} value={d.id}>
                        {d.icon} {d.shortName}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-2">
                {/* Start / Stop Live Translation & Capture Mode Controls */}
                <div className="flex flex-wrap items-center gap-2">
                  <button
                    onClick={() => setIsStreaming(!isStreaming)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-extrabold transition shadow-lg ${
                      isStreaming
                        ? 'bg-emerald-600 text-white shadow-emerald-600/30'
                        : 'bg-red-600 text-white shadow-red-600/30'
                    }`}
                  >
                    {isStreaming ? <Play className="w-3.5 h-3.5 fill-current" /> : <Pause className="w-3.5 h-3.5" />}
                    <span>{isStreaming ? 'CAMERA LIVE' : 'START CAMERA'}</span>
                  </button>

                  {/* Mode Toggle: Capture on Click (Default) vs Continuous Stream */}
                  <div className="flex items-center space-x-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800 text-xs">
                    <button
                      onClick={() => setCaptureMode('on-demand')}
                      className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                        captureMode === 'on-demand'
                          ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow'
                          : 'text-slate-400 hover:text-slate-200'
                      }`}
                      title="Only capture signs when you click 'Capture Sign' button (Default & Recommended)"
                    >
                      <Target className="w-3.5 h-3.5" />
                      <span>Capture on Click</span>
                    </button>
                    <button
                      onClick={() => setCaptureMode('continuous')}
                      className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                        captureMode === 'continuous'
                          ? 'bg-emerald-600 text-white shadow'
                          : 'text-slate-400 hover:text-slate-200'
                      }`}
                      title="Continuously auto-detect signs from live stream"
                    >
                      <Radio className="w-3.5 h-3.5" />
                      <span>Continuous Stream</span>
                    </button>
                  </div>

                  {captureMode === 'continuous' && (
                    <button
                      onClick={() => setIsRecognitionPaused(!isRecognitionPaused)}
                      className={`flex items-center space-x-1.5 px-3 py-2 rounded-xl text-xs font-bold transition border ${
                        isRecognitionPaused
                          ? 'bg-amber-950/80 border-amber-500/50 text-amber-300'
                          : 'bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800'
                      }`}
                    >
                      <Pause className="w-3 h-3" />
                      <span>{isRecognitionPaused ? 'RESUME REC' : 'PAUSE REC'}</span>
                    </button>
                  )}

                  <button
                    onClick={onClearSession}
                    className="flex items-center space-x-1.5 px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-850 border border-slate-700 text-slate-400 hover:text-slate-200 text-xs font-semibold transition"
                    title="Clear output session"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>CLEAR</span>
                  </button>
                </div>

                {/* Configurable Translation Language Selector */}
                <div className="flex items-center space-x-1 bg-slate-900 p-1 rounded-xl border border-slate-800 text-xs">
                  <span className="text-[11px] text-slate-500 font-semibold px-1.5">Output:</span>
                  {[
                    { code: 'en', label: 'English' },
                    { code: 'hi', label: 'हिन्दी' },
                    { code: 'ta', label: 'தமிழ்' }
                  ].map(lang => (
                    <button
                      key={lang.code}
                      onClick={() => handleLangChange(lang.code)}
                      className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition ${
                        effectiveLang === lang.code
                          ? 'bg-indigo-600 text-white shadow-sm'
                          : 'text-slate-400 hover:text-slate-200'
                      }`}
                    >
                      {lang.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Status and Recognition Metrics Row */}
              <div className="grid grid-cols-3 gap-2 text-[11px] font-mono border-t border-slate-800/80 pt-2.5">
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/80 flex items-center justify-between">
                  <span className="text-slate-500">Pipeline:</span>
                  <span className={isStreaming && !isRecognitionPaused ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'}>
                    {!isStreaming ? 'OFFLINE' : isRecognitionPaused ? 'PAUSED' : captureMode === 'on-demand' ? 'CAPTURE ON CLICK' : 'CONTINUOUS'}
                  </span>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/80 flex items-center justify-between">
                  <span className="text-slate-500">Confidence:</span>
                  <span className={topConfidence >= 70 ? 'text-emerald-400 font-bold' : topConfidence > 0 ? 'text-amber-400 font-bold' : 'text-slate-400'}>
                    {topConfidence > 0 ? `${topConfidence}%` : '0%'}
                  </span>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/80 flex items-center justify-between">
                  <span className="text-slate-500">Vocabulary:</span>
                  <span className="text-cyan-400 font-bold">43 Classes</span>
                </div>
              </div>
            </div>

            {/* Live Pipeline Telemetry Summary Strip with quick link to dedicated section */}
            <div className="flex items-center justify-between p-3 rounded-2xl bg-slate-950/80 border border-slate-800 text-xs">
              <div className="flex items-center space-x-2 text-slate-300">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span className="font-mono text-[11px]">AI System Online • MediaPipe 3D • ST-GCN</span>
              </div>
              <button
                onClick={() => setTranslatorMode('pipeline')}
                className="px-2.5 py-1 rounded-xl bg-indigo-950/70 hover:bg-indigo-900/80 text-cyan-300 hover:text-white border border-indigo-500/40 text-[11px] font-bold flex items-center space-x-1 transition shadow"
              >
                <span>View Full Pipeline</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>

            {/* PRIVACY GUARANTEE BADGE */}
            <div className="p-3 bg-slate-950/80 border border-slate-800/80 rounded-2xl flex items-center space-x-2.5 text-xs text-slate-400">
              <Lock className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              <span>
                <strong>Privacy Guaranteed:</strong> Camera skeletal landmarks are computed locally on your edge device; video frames are never stored or transmitted to external clouds.
              </span>
            </div>
          </div>

          {/* RIGHT SIDE: LIVE TRANSLATION & NLP SENTENCE CORRECTION (6 COLS) */}
          <div className="lg:col-span-6 space-y-5">
            {/* MAIN LIVE TRANSLATION CARD */}
            <div className="glass-panel rounded-3xl p-6 border border-slate-800/80 shadow-2xl space-y-5">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <div className="flex items-center space-x-3">
                  <div className="p-2.5 rounded-2xl bg-indigo-600/20 border border-indigo-500/40 text-indigo-400">
                    <Hand className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-sm font-black text-slate-100 uppercase tracking-wider">
                      TRANSLATED OUTPUT
                    </h2>
                    <p className="text-xs text-slate-400">Real-time continuous gesture stream to natural speech</p>
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

              {/* 1. Detected Signs Stream */}
              <div className="space-y-1.5">
                <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                  <span>Detected Sign Sequence (Raw ISL Tokens)</span>
                  <span className="text-[10px] text-indigo-400 font-mono">CTC Decoded</span>
                </div>

                <div className="flex flex-wrap items-center gap-2 p-3.5 bg-slate-950/90 rounded-2xl border border-slate-800 min-h-[58px]">
                  {displayGlosses.length > 0 ? (
                    displayGlosses.map((gloss, idx) => {
                      const isLatest = idx === displayGlosses.length - 1;
                      return (
                        <React.Fragment key={`${gloss}-${idx}`}>
                          <div
                            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-xl border font-mono text-xs font-bold transition-all transform ${
                              isLatest
                                ? 'bg-indigo-600/30 border-indigo-500 text-indigo-200 shadow-lg scale-105'
                                : 'bg-slate-900 border-slate-700 text-slate-300'
                            }`}
                          >
                            <Sparkles className={`w-3 h-3 ${isLatest ? 'text-indigo-400' : 'text-slate-500'}`} />
                            <span>{gloss}</span>
                          </div>
                          {idx < displayGlosses.length - 1 && (
                            <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
                          )}
                        </React.Fragment>
                      );
                    })
                  ) : (
                    <div className="flex items-center space-x-2 text-slate-400 text-xs font-mono py-1">
                      <Target className="w-3.5 h-3.5 text-indigo-400 animate-pulse" />
                      <span>
                        {captureMode === 'on-demand'
                          ? "Ready to capture. Click '🔴 Capture Sign (3s)' below camera to perform a sign."
                          : "Waiting for a valid ISL sign in camera view..."}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              {/* 2. Generated Sentence (Primary Display with NLP Normalization) */}
              <div className="space-y-1.5">
                <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                  <span>Synthesized Sentence ({primaryLangLabel})</span>
                  <span className={`text-[10px] font-mono ${primaryText ? 'text-emerald-400' : 'text-slate-500'}`}>
                    {primaryText ? 'NLP Corrected ✓' : 'NLP Ready'}
                  </span>
                </div>

                <div className="p-5 rounded-2xl bg-gradient-to-br from-slate-950 via-indigo-950/20 to-slate-950 border border-indigo-500/40 space-y-3">
                  <p className="text-lg sm:text-xl font-bold text-white leading-snug">
                    {primaryText ? (
                      `"${primaryText}"`
                    ) : (
                      <span className="text-slate-500 italic font-normal text-base">
                        {captureMode === 'on-demand'
                          ? "Click 'Capture Sign (3s)' below camera to begin signing."
                          : "Waiting for a valid ISL sign..."}
                      </span>
                    )}
                  </p>

                  {/* Smart Sentence Correction Demonstration */}
                  <div className="pt-2 border-t border-slate-800/80 text-xs flex flex-wrap items-center justify-between gap-2">
                    <span className="text-slate-400 font-mono text-[11px]">
                      {displayGlosses.length > 0 ? (
                        <>Raw ISL: <strong className="text-indigo-300">{displayGlosses.join(' ')}</strong> ➔ Natural: <strong className="text-slate-200">SVO Syntax</strong></>
                      ) : (
                        <span>Waiting for a valid ISL sign</span>
                      )}
                    </span>
                    {primaryText && (
                      <button
                        onClick={() => copyToClipboard(primaryText, selectedLanguage)}
                        className="text-slate-400 hover:text-indigo-300 flex items-center space-x-1 text-[11px]"
                      >
                        {copiedLang === selectedLanguage ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                        <span>{copiedLang === selectedLanguage ? 'Copied' : 'Copy'}</span>
                      </button>
                    )}
                  </div>
                </div>
              </div>

              {/* 3. AI Confidence Meter + Low Confidence Warning */}
              <div className="space-y-2 bg-slate-950/70 p-4 rounded-2xl border border-slate-800">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-slate-300 flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>AI Confidence</span>
                  </span>
                  <span className={`font-mono font-bold text-sm ${topConfidence >= 80 ? 'text-emerald-400' : topConfidence > 0 ? 'text-amber-400' : 'text-slate-400'}`}>
                    {topConfidence > 0 ? `${topConfidence}%` : '0% (Ready)'}
                  </span>
                </div>
                {/* Progress bar */}
                <div className="w-full h-2.5 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                  <div
                    className="h-full bg-gradient-to-r from-purple-500 via-blue-400 to-emerald-400 transition-all duration-300"
                    style={{ width: `${topConfidence}%` }}
                  ></div>
                </div>

                {topConfidence > 0 && topConfidence < 80 && (
                  <div className="pt-1 text-[11px] text-amber-300 flex items-center space-x-1.5 font-medium">
                    <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                    <span>Low confidence detected. Please sign with clear lighting within camera bounds.</span>
                  </div>
                )}
              </div>

              {/* 4. Multilingual Translation Outputs */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {/* English Output */}
                {selectedLanguage !== 'en' && (
                  <div className="p-3.5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800/60 uppercase">
                        English
                      </span>
                      <button
                        onClick={() => speakText(enText, 'en')}
                        className="p-1 text-indigo-400 hover:text-indigo-300"
                        title="Replay English Speech"
                      >
                        <Volume2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                    <p className="text-xs font-semibold text-slate-200">"{enText}"</p>
                  </div>
                )}

                {/* Hindi Output */}
                {selectedLanguage !== 'hi' && (
                  <div className="p-3.5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800/60 uppercase">
                        Hindi (हिन्दी)
                      </span>
                      <button
                        onClick={() => speakText(hiText, 'hi')}
                        className="p-1 text-amber-400 hover:text-amber-300"
                        title="Replay Hindi Speech"
                      >
                        <Volume2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                    <p className="text-xs font-semibold text-slate-200">"{hiText}"</p>
                  </div>
                )}

                {/* Tamil Output */}
                {selectedLanguage !== 'ta' && (
                  <div className="p-3.5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/60 uppercase">
                        Tamil (தமிழ்)
                      </span>
                      <button
                        onClick={() => speakText(taText, 'ta')}
                        className="p-1 text-emerald-400 hover:text-emerald-300"
                        title="Replay Tamil Speech"
                      >
                        <Volume2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                    <p className="text-xs font-semibold text-slate-200">"{taText}"</p>
                  </div>
                )}
              </div>

              {/* 5. SPEECH AUDIO CONTROLS & SPEED */}
              <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 text-xs font-bold text-slate-200">
                    <Volume2 className="w-4 h-4 text-cyan-400" />
                    <span>SPEECH SYNTHESIS CONTROLS</span>
                  </div>
                  <span className={`text-[10px] font-mono font-bold ${isSpeaking ? 'text-emerald-400 animate-pulse' : 'text-slate-500'}`}>
                    {isSpeaking ? '● PLAYING AUDIO...' : 'IDLE'}
                  </span>
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => speakText(primaryText, selectedLanguage)}
                    className="flex-1 flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white font-bold text-xs shadow-lg transition"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" />
                    <span>Play {primaryLangLabel}</span>
                  </button>

                  <button
                    onClick={stopSpeech}
                    className="p-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-400 hover:text-white transition"
                    title="Stop Speech"
                  >
                    <Pause className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* 6. Syntactic Grammar Alignment Preview */}
              <div className="bg-slate-950/60 p-3.5 rounded-2xl border border-slate-800 space-y-2 text-xs">
                <div className="flex items-center space-x-2 text-slate-400 font-semibold text-[11px] uppercase">
                  <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Topic-Comment Syntactic Alignment:</span>
                </div>
                <div className="flex flex-wrap items-center gap-1.5">
                  {grammarAlignment && grammarAlignment.length > 0 ? (
                    grammarAlignment.map((item, idx) => (
                      <div key={idx} className="flex items-center space-x-1.5 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800 text-[11px]">
                        <span className="font-mono text-indigo-300 font-bold">{item.isl_gloss}</span>
                        <ArrowRight className="w-2.5 h-2.5 text-slate-600" />
                        <span className="text-slate-300 font-medium">{item.spoken_word}</span>
                        <span className="text-[9px] px-1 rounded bg-slate-800 text-slate-400 font-mono">{item.syntactic_role}</span>
                      </div>
                    ))
                  ) : (
                    <div className="text-slate-500 font-mono text-[11px]">ISL Topic-Comment to SVO reordered</div>
                  )}
                </div>
              </div>
            </div>

            {/* QUICK BENCHMARK SCENARIO SELECTOR */}
            <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-2.5">
              <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                <span>Canonical Benchmark Scenarios</span>
                <span className="text-[10px] text-slate-500">Instant Load</span>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                {quickScenarios.map((sc) => (
                  <button
                    key={sc.id}
                    onClick={() => onApplyScenario && onApplyScenario(sc.id)}
                    className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-white text-xs font-semibold transition"
                  >
                    {sc.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* TWO-WAY CONVERSATION DIALOGUE MODE */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* 3D WebGL Avatar Display (6 cols) */}
          <div className="lg:col-span-6 space-y-4">
            <Avatar3D />
          </div>

          {/* Conversation Dialogue History & Hearing Responder Input (6 cols) */}
          <div className="lg:col-span-6 glass-panel rounded-3xl p-6 border border-slate-800 shadow-2xl space-y-4 flex flex-col justify-between min-h-[500px]">
            <div>
              <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                <div className="flex items-center space-x-2.5">
                  <MessageSquare className="w-5 h-5 text-purple-400" />
                  <h3 className="text-sm font-black text-white uppercase tracking-wider">
                    Two-Way Dialogue Stream
                  </h3>
                </div>
                <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/80 px-2.5 py-0.5 rounded-full border border-cyan-500/30">
                  DEAF ↔ HEARING BRIDGE
                </span>
              </div>

              {/* Messages Stream */}
              <div className="space-y-3 max-h-[380px] overflow-y-auto pr-1">
                {conversationList.length > 0 ? (
                  conversationList.map((msg, idx) => (
                    <div
                      key={idx}
                      className={`p-3.5 rounded-2xl border text-xs space-y-1.5 ${
                        msg.sender === 'signer'
                          ? 'bg-indigo-950/60 border-indigo-800/60 text-indigo-100 ml-0 mr-6'
                          : 'bg-cyan-950/60 border-cyan-800/60 text-cyan-100 ml-6 mr-0'
                      }`}
                    >
                      <div className="flex items-center justify-between text-[10px] font-bold">
                        <span className={msg.sender === 'signer' ? 'text-indigo-300' : 'text-cyan-300'}>
                          {msg.sender === 'signer' ? '🤟 ' : '🗣️ '} {msg.label}
                        </span>
                        <span className="text-slate-500 font-mono">{msg.time}</span>
                      </div>
                      <p className="font-semibold text-sm text-white">"{msg.text}"</p>
                      {msg.glosses && (
                        <div className="text-[10px] font-mono text-slate-400">
                          ISL Sequence: [{msg.glosses.join('] [')}]
                        </div>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="text-center text-slate-500 text-xs py-16 space-y-2">
                    <MessageSquare className="w-8 h-8 text-slate-700 mx-auto" />
                    <p className="font-semibold text-slate-400">No conversation yet.</p>
                    <p className="text-[11px] text-slate-600">Sign in camera or type a hearing response below to begin two-way dialogue.</p>
                  </div>
                )}
              </div>
            </div>

            {/* Hearing Responder Input Form */}
            <form onSubmit={handleSendHearingResponse} className="pt-3 border-t border-slate-800 space-y-2">
              <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                Hearing User: Type or Speak Response (Triggers 3D ISL Avatar)
              </label>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={hearingInputText}
                  onChange={(e) => setHearingInputText(e.target.value)}
                  placeholder="Type response (e.g. 'Please wait 10 minutes')..."
                  className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-cyan-500 transition"
                />
                <button
                  type="submit"
                  className="px-4 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs shadow transition flex items-center space-x-1.5"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>Send</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
