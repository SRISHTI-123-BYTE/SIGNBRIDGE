import React, { useState, useEffect } from 'react';
import {
  Hand,
  Volume2,
  UserCheck,
  Activity,
  Layers,
  Sparkles,
  ShieldAlert,
  Cpu,
  RefreshCw,
  Info,
  CheckCircle2,
  Settings,
  Eye,
  Type,
  BookOpen,
  History,
  Home,
  Sun,
  Moon,
  ShieldCheck,
  Menu,
  X,
  PanelLeftClose,
  PanelLeftOpen,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

import HomePage from './components/HomePage';
import LiveTranslator from './components/LiveTranslator';
import DemoMode from './components/DemoMode';
import ISLDictionary from './components/ISLDictionary';
import DatasetManager from './components/DatasetManager';
import LearnISLPage from './components/LearnISLPage';
import HistoryPage from './components/HistoryPage';
import AboutPage from './components/AboutPage';
import SettingsModal from './components/SettingsModal';
import AccessibilityWidget from './components/AccessibilityWidget';
import { signBridgeService } from './services/api';
import { INDIAN_SIGN_LANGUAGES } from './data/indianSignLanguages';

// Initial session history starts empty
const INITIAL_HISTORY = [];

export default function App() {
  const [activeTab, setActiveTab] = useState('home'); // 'home' | 'translator' | 'learn' | 'history' | 'about'
  const [isStreaming, setIsStreaming] = useState(true);
  const [isAutoSpeak, setIsAutoSpeak] = useState(true);
  const [isServerConnected, setIsServerConnected] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isA11yOpen, setIsA11yOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [selectedDialect, setSelectedDialect] = useState('isl-standard');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(() => {
    try {
      return localStorage.getItem('isl_sidebar_collapsed') === 'true';
    } catch (e) {
      return false;
    }
  });

  // Always ensure HomePage is the first page displayed on website load
  useEffect(() => {
    setActiveTab('home');
    window.scrollTo(0, 0);
  }, []);

  const toggleSidebar = () => {
    setIsSidebarCollapsed(prev => {
      const next = !prev;
      try {
        localStorage.setItem('isl_sidebar_collapsed', next.toString());
      } catch (e) {}
      return next;
    });
  };

  // Selected Language State (Shared with Homepage selector & Translator)
  const [selectedLanguage, setSelectedLanguage] = useState('en');

  // Accessibility State
  const [settings, setSettings] = useState({
    cameraSource: 'webcam',
    defaultLang: 'en',
    autoSpeak: true,
    speechRate: 1.0,
    highContrast: false,
    reducedMotion: false,
    fontSize: 'normal' // 'normal' | 'medium' | 'large'
  });

  // Live Recognition State (starts clean/empty)
  const [activeGlosses, setActiveGlosses] = useState([]);
  const [recognizedTokens, setRecognizedTokens] = useState([]);
  const [translations, setTranslations] = useState({
    en: "",
    hi: "",
    ta: ""
  });
  const [grammarAlignment, setGrammarAlignment] = useState([]);
  const [nmmState, setNmmState] = useState({ is_interrogative: false, is_urgent: false });
  const [latencyMetrics, setLatencyMetrics] = useState({ total_end_to_end_ms: 0 });

  // History State
  const [historyData, setHistoryData] = useState(() => {
    const saved = localStorage.getItem('isl_ai_history');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        return INITIAL_HISTORY;
      }
    }
    return INITIAL_HISTORY;
  });

  // Save history to localStorage
  useEffect(() => {
    localStorage.setItem('isl_ai_history', JSON.stringify(historyData));
  }, [historyData]);

  // WebSocket / Backend Health Check
  useEffect(() => {
    signBridgeService.initWebSocket(
      (data) => {
        if (data.type === 'RECOGNITION_UPDATE') {
          if (data.new_tokens && data.new_tokens.length > 0) {
            setActiveGlosses(data.active_glosses || []);
            setRecognizedTokens(data.new_tokens);
            if (data.translations && data.translations.en) {
              setTranslations(data.translations);
              // Append to history only when new tokens confirmed
              const now = new Date();
              const topTok = data.new_tokens[data.new_tokens.length - 1];
              const confPct = Math.round((topTok?.confidence || 0.94) * 100);
              const newRecord = {
                id: `hist-${Date.now()}`,
                date: 'Today',
                time: now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                glosses: data.active_glosses,
                english: data.translations.en,
                hindi: data.translations.hi,
                tamil: data.translations.ta,
                confidence: confPct
              };
              setHistoryData(prev => [newRecord, ...prev.slice(0, 30)]);
            }
          }
          if (data.grammar_alignment) {
            setGrammarAlignment(data.grammar_alignment);
          }
          if (data.nmm) {
            setNmmState(data.nmm);
          }
          if (data.frame_latency_ms) {
            setLatencyMetrics({ total_end_to_end_ms: data.frame_latency_ms });
          }
        } else if (data.type === 'NO_SIGN') {
          // Explicit NO_SIGN from backend: if history is empty, ensure clean state
          if (!data.active_glosses || data.active_glosses.length === 0) {
            setActiveGlosses([]);
            setRecognizedTokens([]);
            setTranslations({ en: "", hi: "", ta: "" });
            setGrammarAlignment([]);
          }
        } else if (data.type === 'SESSION_CLEARED') {
          setActiveGlosses([]);
          setRecognizedTokens([]);
          setTranslations({ en: "", hi: "", ta: "" });
          setGrammarAlignment([]);
        }
      },
      (status) => {
        setIsServerConnected(status);
      }
    );

    signBridgeService.checkHealth().then((res) => {
      if (res.status === 'online') setIsServerConnected(true);
    });

    return () => {
      signBridgeService.closeWebSocket();
    };
  }, []);

  const handleApplyScenario = async (scenarioId) => {
    const res = await signBridgeService.simulateScenario(scenarioId);
    if (res.ground_truth_glosses) {
      setActiveGlosses(res.ground_truth_glosses);
    }
    if (res.recognized_tokens) {
      setRecognizedTokens(res.recognized_tokens);
    }
    if (res.translations) {
      setTranslations(res.translations);
    }
    if (res.grammar_alignment) {
      setGrammarAlignment(res.grammar_alignment);
    }
    if (res.latency_ms) {
      setLatencyMetrics({ total_end_to_end_ms: res.latency_ms });
    }

    // Record in history
    const now = new Date();
    const newRecord = {
      id: `hist-${Date.now()}`,
      date: 'Today',
      time: now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      glosses: res.ground_truth_glosses,
      english: res.translations.en,
      hindi: res.translations.hi,
      tamil: res.translations.ta,
      confidence: Math.round(res.recognized_tokens[0]?.confidence * 100) || 94
    };
    setHistoryData(prev => [newRecord, ...prev.slice(0, 30)]);
  };

  const handlePracticeSign = (gloss) => {
    setActiveGlosses([gloss]);
    setActiveTab('translator');
  };

  const handleDemoAvatar = (text) => {
    setActiveTab('translator');
  };

  const handleRecordSign = async (signName, confidence = 0.94, fullResult = null) => {
    if (!signName) return;

    // Check if fullResult contains recognized tokens (single or multiple)
    const tokensToAdd = (fullResult?.recognized_tokens && fullResult.recognized_tokens.length > 0)
      ? fullResult.recognized_tokens
      : [{ gloss: signName, confidence: confidence, duration_frames: 30 }];

    const glossesToAdd = tokensToAdd.map(t => t.gloss).filter(Boolean);
    if (glossesToAdd.length === 0) return;

    const newGlosses = [...activeGlosses, ...glossesToAdd];
    setActiveGlosses(newGlosses);
    setRecognizedTokens(prev => [...prev, ...tokensToAdd]);

    // Translate full accumulated sentence
    let transResult = null;
    if (newGlosses.length === glossesToAdd.length && fullResult?.translations?.en) {
      transResult = fullResult;
    } else {
      transResult = await signBridgeService.translateGlosses(newGlosses, nmmState);
    }

    if (transResult && transResult.translations) {
      setTranslations(transResult.translations);
      if (transResult.grammar_alignment) {
        setGrammarAlignment(transResult.grammar_alignment);
      }
      // Add to session history
      const now = new Date();
      const newRecord = {
        id: `hist-${Date.now()}`,
        date: 'Today',
        time: now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        glosses: newGlosses,
        english: transResult.translations.en,
        hindi: transResult.translations.hi,
        tamil: transResult.translations.ta,
        confidence: Math.round((tokensToAdd[0]?.confidence || confidence) * 100)
      };
      setHistoryData(prev => [newRecord, ...prev.slice(0, 30)]);
    }
  };

  const handleClearSession = () => {
    setActiveGlosses([]);
    setRecognizedTokens([]);
    setTranslations({
      en: "",
      hi: "",
      ta: ""
    });
    setGrammarAlignment([]);
    signBridgeService.resetSession();
  };

  const handleDeleteHistoryItem = (id) => {
    setHistoryData(prev => prev.filter(item => item.id !== id));
  };

  const handleClearAllHistory = () => {
    setHistoryData([]);
  };

  const handleUpdateSettings = (newSettings) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
  };

  // Font scaling styles
  const getFontSizeClass = () => {
    if (settings.fontSize === 'large') return 'text-lg';
    if (settings.fontSize === 'medium') return 'text-base';
    return 'text-sm';
  };

  const navItems = [
    { id: 'home', label: 'Home', icon: Home, badge: null },
    { id: 'translator', label: 'Live Translator', icon: Hand, badge: '⭐', isStar: true },
    { id: 'demo', label: 'Demo Mode', icon: Sparkles, badge: '🎬', isAmber: true },
    { id: 'dictionary', label: 'ISL Dictionary', icon: BookOpen, badge: null },
    { id: 'dataset', label: 'Dataset & Model', icon: Layers, badge: null },
    { id: 'learn', label: 'Learn ISL', icon: Cpu, badge: null },
    { id: 'history', label: 'History', icon: History, badge: historyData.length > 0 ? historyData.length : null },
    { id: 'about', label: 'About', icon: Info, badge: null }
  ];

  // 1. FULL-PAGE HOME VIEW (Covers entire screen, no side panel)
  if (!activeTab || activeTab === 'home') {
    return (
      <div className={`min-h-screen bg-[#050609] text-slate-100 mesh-grid ${
        settings.highContrast ? 'contrast-125 brightness-110 saturate-150' : ''
      } ${settings.reducedMotion ? 'motion-reduce' : ''} ${getFontSizeClass()}`}>
        <HomePage
          onNavigate={(tab) => {
            setActiveTab(tab);
            window.scrollTo(0, 0);
          }}
          onStartTranslating={() => {
            setActiveTab('translator');
            window.scrollTo(0, 0);
          }}
          selectedLanguage={selectedLanguage}
          onSelectLanguage={setSelectedLanguage}
          onOpenSettings={() => setIsSettingsOpen(true)}
          onOpenA11y={() => setIsA11yOpen(true)}
          isServerConnected={isServerConnected}
        />

        {/* Settings Modal */}
        <SettingsModal
          isOpen={isSettingsOpen}
          onClose={() => setIsSettingsOpen(false)}
          settings={settings}
          onUpdateSettings={handleUpdateSettings}
        />

        {/* Accessibility Controls Drawer / Widget */}
        <AccessibilityWidget
          isOpen={isA11yOpen}
          onClose={() => setIsA11yOpen(false)}
          settings={settings}
          onUpdateSettings={handleUpdateSettings}
        />
      </div>
    );
  }

  // 2. MAIN APP WORKSPACE WITH SIDE PANEL (For Translator, Learn, Dictionary, Demo, Dataset, History, About)
  return (
    <div className={`min-h-screen bg-[#050609] text-slate-100 flex flex-col md:flex-row mesh-grid ${
      settings.highContrast ? 'contrast-125 brightness-110 saturate-150' : ''
    } ${settings.reducedMotion ? 'motion-reduce' : ''} ${getFontSizeClass()}`}>
      
      {/* DESKTOP SIDE PANEL (Sidebar) */}
      <aside
        className={`hidden md:flex flex-col h-screen sticky top-0 z-30 transition-all duration-300 ease-in-out border-r border-slate-800/80 bg-[#06080d]/95 backdrop-blur-2xl flex-shrink-0 ${
          isSidebarCollapsed ? 'w-20' : 'w-64 lg:w-72'
        }`}
      >
        {/* Brand Header */}
        <div className={`p-4 border-b border-slate-800/80 flex items-center ${isSidebarCollapsed ? 'justify-center flex-col space-y-2' : 'justify-between'}`}>
          <button
            onClick={() => setActiveTab('home')}
            className={`flex items-center text-left focus:outline-none group min-w-0 ${isSidebarCollapsed ? 'justify-center' : 'space-x-3'}`}
            title="ISL AI - Home"
          >
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-purple-600 via-indigo-600 to-cyan-400 p-0.5 flex-shrink-0 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition transform">
              <div className="w-full h-full bg-[#050609] rounded-[14px] flex items-center justify-center">
                <Hand className="w-5 h-5 text-cyan-400 group-hover:rotate-12 transition-transform" />
              </div>
            </div>
            {!isSidebarCollapsed && (
              <div className="min-w-0">
                <div className="flex items-center space-x-1.5">
                  <h1 className="text-base font-black tracking-tight bg-gradient-to-r from-white via-slate-100 to-indigo-300 bg-clip-text text-transparent truncate">
                    ISL AI
                  </h1>
                  <span className="px-1.5 py-0.5 rounded-full text-[9px] font-bold bg-indigo-950/80 border border-indigo-500/40 text-indigo-300 flex-shrink-0">
                    Real-Time
                  </span>
                </div>
                <p className="text-[10px] text-slate-400 truncate">
                  Sign-to-Speech Engine
                </p>
              </div>
            )}
          </button>

          <button
            onClick={toggleSidebar}
            className="p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800/60 border border-transparent hover:border-slate-700/80 transition"
            title={isSidebarCollapsed ? "Expand Side Panel" : "Collapse Side Panel"}
          >
            {isSidebarCollapsed ? <PanelLeftOpen className="w-4 h-4" /> : <PanelLeftClose className="w-4 h-4" />}
          </button>
        </div>

        {/* Navigation Items (Scrollable) */}
        <nav className="flex-1 overflow-y-auto px-2.5 py-3 space-y-1">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            const Icon = item.icon;

            if (isSidebarCollapsed) {
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center justify-center p-3 rounded-xl transition group relative ${
                    isActive
                      ? item.id === 'translator'
                        ? 'bg-gradient-to-tr from-purple-600 via-indigo-600 to-cyan-500 text-white shadow-lg shadow-indigo-500/30'
                        : item.id === 'home'
                        ? 'bg-gradient-to-tr from-purple-600 to-indigo-600 text-white shadow-md'
                        : item.id === 'demo'
                        ? 'bg-gradient-to-tr from-amber-600 to-indigo-600 text-white shadow-md'
                        : 'bg-indigo-600 text-white shadow-md'
                      : 'text-slate-400 hover:text-white hover:bg-slate-900/80'
                  }`}
                  title={`${item.label} ${item.badge ? `(${item.badge})` : ''}`}
                >
                  <Icon className="w-5 h-5 transition-transform group-hover:scale-110" />
                  {item.badge && (
                    <span className="absolute top-1.5 right-1.5 text-[9px] leading-none">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            }

            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl transition text-xs font-semibold group ${
                  isActive
                    ? item.id === 'translator'
                      ? 'bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-600 text-white font-bold shadow-lg shadow-indigo-600/25'
                      : item.id === 'home'
                      ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold shadow-md'
                      : item.id === 'demo'
                      ? 'bg-gradient-to-r from-amber-600 to-indigo-600 text-white font-bold shadow-md'
                      : 'bg-indigo-600 text-white font-bold shadow-md'
                    : item.id === 'demo'
                    ? 'text-amber-300 hover:text-white hover:bg-slate-900/80'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/80'
                }`}
              >
                <div className="flex items-center space-x-3 min-w-0">
                  <Icon
                    className={`w-4 h-4 flex-shrink-0 transition-transform group-hover:scale-110 ${
                      isActive
                        ? 'text-white'
                        : item.id === 'translator'
                        ? 'text-cyan-400'
                        : item.id === 'demo'
                        ? 'text-amber-400'
                        : item.id === 'dictionary'
                        ? 'text-indigo-400'
                        : item.id === 'dataset'
                        ? 'text-purple-400'
                        : 'text-slate-400'
                    }`}
                  />
                  <span className="truncate">{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`text-xs px-1.5 py-0.5 rounded-md font-mono ${
                    isActive ? 'bg-white/20 text-white' : 'bg-slate-800/80 text-slate-300'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Footer: AI Status & Utility Controls */}
        <div className="p-3 border-t border-slate-800/80 bg-slate-950/40 space-y-2.5">
          {/* AI System Status */}
          <div
            className={`flex items-center rounded-xl p-2 border transition ${
              isServerConnected
                ? 'bg-emerald-950/40 border-emerald-500/30 text-emerald-300'
                : 'bg-indigo-950/40 border-indigo-500/30 text-indigo-300'
            } ${isSidebarCollapsed ? 'justify-center' : 'space-x-2.5'}`}
            title={isServerConnected ? "Connected to Python Edge AI Engine (FastAPI + ST-GCN ONNX)" : "Running on In-Browser Accelerated Engine"}
          >
            <span className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${isServerConnected ? 'bg-emerald-400 animate-pulse' : 'bg-indigo-400'}`}></span>
            {!isSidebarCollapsed && (
              <div className="min-w-0 flex-1">
                <div className="text-[11px] font-mono font-bold leading-tight truncate">
                  {isServerConnected ? 'AI SYSTEM ONLINE' : 'STANDALONE ENGINE'}
                </div>
                <div className="text-[9px] text-slate-400 truncate">
                  {isServerConnected ? 'ST-GCN ONNX + Fallback' : 'In-Browser Rules'}
                </div>
              </div>
            )}
          </div>

          {/* Active Indian Sign Language Dialect Badge */}
          {!isSidebarCollapsed && (
            <div className="px-2.5 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 text-[10px] flex items-center justify-between">
              <span className="text-slate-400">Sign Lang:</span>
              <span className="font-bold text-cyan-300 truncate max-w-[130px]" title={INDIAN_SIGN_LANGUAGES.find(d => d.id === selectedDialect)?.name}>
                {INDIAN_SIGN_LANGUAGES.find(d => d.id === selectedDialect)?.shortName || 'Standard ISL'}
              </span>
            </div>
          )}

          {/* Action Buttons: Accessibility & Settings */}
          <div className={`flex items-center gap-1.5 ${isSidebarCollapsed ? 'flex-col' : ''}`}>
            <button
              onClick={() => setIsA11yOpen(true)}
              className={`flex items-center justify-center rounded-xl bg-slate-900 border border-slate-700/80 hover:border-indigo-500/60 text-slate-300 hover:text-white font-bold transition shadow-sm ${
                isSidebarCollapsed ? 'p-2 w-full' : 'flex-1 space-x-1.5 py-2 px-2 text-xs'
              }`}
              title="Accessibility Controls"
            >
              <span className="text-xs">♿</span>
              {!isSidebarCollapsed && <span>Accessibility</span>}
            </button>

            <button
              onClick={() => setIsSettingsOpen(true)}
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition flex items-center justify-center"
              title="System Settings"
            >
              <Settings className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT WORKSPACE */}
      <div className="flex-1 flex flex-col min-w-0 min-h-screen overflow-x-hidden">
        {/* MOBILE TOP HEADER BAR (Mobile / Small Screen) */}
        <div className="md:hidden sticky top-0 z-40 bg-[#050609]/95 backdrop-blur-2xl border-b border-slate-800/80 px-3.5 py-2.5 flex items-center justify-between">
          <button
            onClick={() => setIsMobileMenuOpen(true)}
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white flex items-center space-x-1.5"
            aria-label="Open Navigation Side Panel"
          >
            <Menu className="w-4 h-4" />
            <span className="text-xs font-bold">Menu</span>
          </button>

          <button
            onClick={() => setActiveTab('home')}
            className="flex items-center space-x-2 focus:outline-none"
            title="ISL AI - Home"
          >
            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-purple-600 to-cyan-400 p-0.5 flex items-center justify-center">
              <div className="w-full h-full bg-[#050609] rounded-[6px] flex items-center justify-center">
                <Hand className="w-3.5 h-3.5 text-cyan-400" />
              </div>
            </div>
            <span className="font-bold text-sm bg-gradient-to-r from-white to-indigo-300 bg-clip-text text-transparent">
              ISL AI
            </span>
            <span className="px-1.5 py-0.2 rounded-full text-[9px] font-bold bg-indigo-950/80 border border-indigo-500/40 text-indigo-300">
              Live
            </span>
          </button>

          <div className="flex items-center space-x-1.5">
            <div
              className={`w-2.5 h-2.5 rounded-full ${isServerConnected ? 'bg-emerald-400 animate-pulse' : 'bg-indigo-400'}`}
              title={isServerConnected ? "AI Online" : "Standalone"}
            />
            <button
              onClick={() => setIsA11yOpen(true)}
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white text-xs"
              title="Accessibility"
            >
              ♿
            </button>
            <button
              onClick={() => setIsSettingsOpen(true)}
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"
              title="Settings"
            >
              <Settings className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* MOBILE DRAWER (Off-canvas sidebar) */}
        {isMobileMenuOpen && (
          <div className="fixed inset-0 z-50 md:hidden flex">
            {/* Backdrop */}
            <div
              className="fixed inset-0 bg-black/75 backdrop-blur-sm transition-opacity"
              onClick={() => setIsMobileMenuOpen(false)}
            />

            {/* Drawer Content */}
            <div className="relative w-72 max-w-[85vw] bg-[#07090e] border-r border-slate-800 h-full flex flex-col z-10 shadow-2xl animate-in slide-in-from-left duration-200">
              {/* Drawer Header */}
              <div className="p-4 border-b border-slate-800 flex items-center justify-between">
                <div className="flex items-center space-x-2.5">
                  <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-purple-600 to-cyan-400 p-0.5 flex items-center justify-center">
                    <div className="w-full h-full bg-[#050609] rounded-[8px] flex items-center justify-center">
                      <Hand className="w-4 h-4 text-cyan-400" />
                    </div>
                  </div>
                  <div>
                    <h2 className="font-bold text-sm text-white">ISL AI</h2>
                    <p className="text-[10px] text-slate-400">Navigation Side Panel</p>
                  </div>
                </div>
                <button
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Mobile Nav List */}
              <div className="flex-1 overflow-y-auto p-3 space-y-1">
                {navItems.map(item => {
                  const isActive = activeTab === item.id;
                  const Icon = item.icon;
                  return (
                    <button
                      key={item.id}
                      onClick={() => { setActiveTab(item.id); setIsMobileMenuOpen(false); }}
                      className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition ${
                        isActive
                          ? item.id === 'translator'
                            ? 'bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-600 text-white font-bold shadow-lg'
                            : item.id === 'home'
                            ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold shadow-md'
                            : item.id === 'demo'
                            ? 'bg-gradient-to-r from-amber-600 to-indigo-600 text-white font-bold shadow-md'
                            : 'bg-indigo-600 text-white font-bold shadow-md'
                          : 'text-slate-300 hover:text-white hover:bg-slate-900'
                      }`}
                    >
                      <div className="flex items-center space-x-2.5">
                        <Icon className="w-4 h-4" />
                        <span>{item.label}</span>
                      </div>
                      {item.badge && <span className="text-xs font-mono">{item.badge}</span>}
                    </button>
                  );
                })}
              </div>

              {/* Mobile Drawer Footer */}
              <div className="p-3.5 border-t border-slate-800 bg-slate-950/60 space-y-2">
                <div className="flex items-center space-x-2 px-2.5 py-1.5 rounded-lg bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-[11px] font-mono">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span>{isServerConnected ? 'AI SYSTEM ONLINE' : 'STANDALONE ENGINE'}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Main Page View Router */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6 sm:py-8 flex flex-col justify-start items-center">
        {/* Page 1: Home (Default landing page when website opens) */}
        {(!activeTab || activeTab === 'home') && (
          <HomePage
            onNavigate={setActiveTab}
            onStartTranslating={() => setActiveTab('translator')}
            selectedLanguage={selectedLanguage}
            onSelectLanguage={setSelectedLanguage}
          />
        )}

        {/* Page 2: Live Translator (Centerpiece) */}
        {activeTab === 'translator' && (
          <LiveTranslator
            activeGlosses={activeGlosses}
            recognizedTokens={recognizedTokens}
            translations={translations}
            grammarAlignment={grammarAlignment}
            nmmState={nmmState}
            latencyMetrics={latencyMetrics}
            isStreaming={isStreaming}
            setIsStreaming={setIsStreaming}
            isAutoSpeak={isAutoSpeak}
            setIsAutoSpeak={setIsAutoSpeak}
            isServerConnected={isServerConnected}
            recentHistory={historyData}
            onApplyScenario={handleApplyScenario}
            onClearSession={handleClearSession}
            onRecordSign={handleRecordSign}
            onNavigateToHistory={() => setActiveTab('history')}
            onNavigateToDemo={() => setActiveTab('demo')}
            onNavigateToDictionary={() => setActiveTab('dictionary')}
            selectedLanguage={selectedLanguage}
            onSelectLanguage={setSelectedLanguage}
            selectedDialect={selectedDialect}
            onSelectDialect={setSelectedDialect}
          />
        )}

        {/* Dedicated Demo Mode (Completely separate from live recognition) */}
        {activeTab === 'demo' && (
          <DemoMode onReturnToLive={() => setActiveTab('translator')} />
        )}

        {/* Extensible ISL Sign Dictionary & All Indian Sign Languages Registry */}
        {activeTab === 'dictionary' && (
          <ISLDictionary
            selectedDialect={selectedDialect}
            onSelectDialect={setSelectedDialect}
            onNavigateToTranslator={() => setActiveTab('translator')}
          />
        )}

        {/* Ethical Dataset & Model Management */}
        {activeTab === 'dataset' && (
          <DatasetManager onClose={() => setActiveTab('translator')} />
        )}

        {/* Page 3: Learn ISL */}
        {activeTab === 'learn' && (
          <LearnISLPage
            onPracticeSign={handlePracticeSign}
            onDemoAvatar={handleDemoAvatar}
          />
        )}

        {/* Page 4: Translation History */}
        {activeTab === 'history' && (
          <HistoryPage
            historyData={historyData}
            onDeleteItem={handleDeleteHistoryItem}
            onClearAllHistory={handleClearAllHistory}
            onStartTranslating={() => setActiveTab('translator')}
          />
        )}

        {/* Page 5: About & Architecture */}
        {activeTab === 'about' && (
          <AboutPage />
        )}
      </main>
      </div>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        settings={settings}
        onUpdateSettings={handleUpdateSettings}
      />

      {/* Accessibility Controls Drawer / Widget */}
      <AccessibilityWidget
        isOpen={isA11yOpen}
        onClose={() => setIsA11yOpen(false)}
        settings={settings}
        onUpdateSettings={handleUpdateSettings}
      />
    </div>
  );
}
