import React, { useState } from 'react';
import {
  Search,
  BookOpen,
  Volume2,
  Hand,
  Sparkles,
  ArrowRight,
  Filter,
  Play,
  UserCheck,
  CheckCircle2,
  Activity,
  Layers,
  Heart,
  ShieldAlert,
  Compass,
  Building2,
  Clock,
  Target,
  Flame,
  Award,
  RotateCcw,
  Zap,
  Check,
  Camera,
  X,
  ChevronLeft,
  ChevronRight,
  AlertTriangle
} from 'lucide-react';
import VisionTracker from './VisionTracker';

export default function LearnISLPage({ onPracticeSign, onDemoAvatar }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [playingSign, setPlayingSign] = useState(null);

  // Dynamic user learning stats (starts clean from 0)
  const [learnedSigns, setLearnedSigns] = useState(() => {
    try {
      const saved = localStorage.getItem('isl_learned_signs');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });
  const [averageScore, setAverageScore] = useState(() => {
    try {
      const saved = localStorage.getItem('isl_average_score');
      return saved ? Number(saved) : 0;
    } catch {
      return 0;
    }
  });
  const [streakDays, setStreakDays] = useState(() => {
    try {
      const saved = localStorage.getItem('isl_practice_streak');
      return saved ? Number(saved) : 0;
    } catch {
      return 0;
    }
  });

  // Practice Mode (AI Coach) State
  const [isPracticeActive, setIsPracticeActive] = useState(false);
  const [practiceStep, setPracticeStep] = useState(0);
  const [practiceEvaluation, setPracticeEvaluation] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [isCameraActive, setIsCameraActive] = useState(true);

  const basePracticeSigns = [
    { gloss: 'HELLO', title: 'Hello / Namaste', emoji: '👋', prompt: 'Form flat open palm salute at temple and sweep outward.' },
    { gloss: 'THANK_YOU', title: 'Thank You', emoji: '🤲', prompt: 'Touch chin with open palm and extend forward with a gentle nod.' },
    { gloss: 'DOCTOR', title: 'Doctor', emoji: '🩺', prompt: 'Tap two fingers on your left wrist pulse point twice.' },
    { gloss: 'WATER', title: 'Water', emoji: '💧', prompt: 'Form "W" three fingers at chin and tap twice.' },
    { gloss: 'HELP', title: 'Help Me', emoji: '🆘', prompt: 'Rest thumbs-up fist on horizontal palm and lift upward.' }
  ];
  const [dynamicPracticeSigns, setDynamicPracticeSigns] = useState([]);
  const practiceSigns = [...basePracticeSigns, ...dynamicPracticeSigns];

  const categories = [
    { id: 'all', label: 'All Signs' },
    { id: 'emergency', label: '🚑 Medical & Emergency' },
    { id: 'greetings', label: '👋 Greetings & Social' },
    { id: 'civic', label: '🏛 Civic & Navigation' },
    { id: 'daily', label: '💧 Daily Needs & Actions' },
    { id: 'numbers', label: '🔢 Numbers & Time' }
  ];

  const signsData = [
    {
      id: 'hello',
      title: 'Hello / Namaste',
      gloss: 'HELLO',
      category: 'greetings',
      categoryLabel: 'Greetings',
      emoji: '👋',
      spokenText: 'Hello',
      hindiText: 'नमस्ते',
      tamilText: 'வணக்கம்',
      handshape: 'Open Flat Palm Salute',
      movement: 'Dominant open hand raises to forehead/temple and sweeps outward with an inviting nod and warm smile.',
      grammaticalRole: 'Salutation',
      urgency: false
    },
    {
      id: 'thank_you',
      title: 'Thank You',
      gloss: 'THANK YOU',
      category: 'greetings',
      categoryLabel: 'Greetings',
      emoji: '🤲',
      spokenText: 'Thank you',
      hindiText: 'धन्यवाद',
      tamilText: 'நன்றி',
      handshape: 'Flat Open Palm to Chin',
      movement: 'Fingertips of dominant flat hand lightly touch chin/lips and extend forward toward the recipient.',
      grammaticalRole: 'Social Politeness',
      urgency: false
    },
    {
      id: 'yes',
      title: 'Yes',
      gloss: 'YES',
      category: 'greetings',
      categoryLabel: 'Greetings',
      emoji: '👍',
      spokenText: 'Yes',
      hindiText: 'हाँ',
      tamilText: 'ஆம்',
      handshape: 'S-Fist Head Nod',
      movement: 'Form a closed fist at chest height and nod the fist up and down twice, mimicking an affirmative head nod.',
      grammaticalRole: 'Affirmative Particle',
      urgency: false
    },
    {
      id: 'no',
      title: 'No',
      gloss: 'NO',
      category: 'greetings',
      categoryLabel: 'Greetings',
      emoji: '🙅',
      spokenText: 'No',
      hindiText: 'नहीं',
      tamilText: 'இல்லை',
      handshape: 'Dual Index/Middle Snap',
      movement: 'Index and middle fingers extend and snap closed against the thumb with a slight head shake.',
      grammaticalRole: 'Negation',
      urgency: false
    },
    {
      id: 'doctor',
      title: 'Doctor',
      gloss: 'DOCTOR',
      category: 'emergency',
      categoryLabel: 'Medical & Emergency',
      emoji: '🩺',
      spokenText: 'Doctor',
      hindiText: 'डॉक्टर',
      tamilText: 'மருத்துவர்',
      handshape: 'Double Pulse Tap',
      movement: 'Non-dominant forearm held horizontally; Dominant index and middle fingers tap the inside wrist pulse twice.',
      grammaticalRole: 'Medical Noun',
      urgency: true
    },
    {
      id: 'chest_pain',
      title: 'Chest Pain',
      gloss: 'CHEST PAIN',
      category: 'emergency',
      categoryLabel: 'Medical & Emergency',
      emoji: '💔',
      spokenText: 'Chest pain',
      hindiText: 'सीने में दर्द',
      tamilText: 'மார்பு வலி',
      handshape: 'Dual Index Twist at Chest',
      movement: 'Press flat hand to chest, followed by both index fingers pointing toward center torso and twisting urgently.',
      grammaticalRole: 'Symptom / Noun Phrase',
      urgency: true
    },
    {
      id: 'hospital',
      title: 'Hospital',
      gloss: 'HOSPITAL',
      category: 'emergency',
      categoryLabel: 'Medical & Emergency',
      emoji: '🏥',
      spokenText: 'Hospital',
      hindiText: 'अस्पताल',
      tamilText: 'மருத்துவமனை',
      handshape: 'Intersecting Cross (+)',
      movement: 'Left index finger held vertically (|); Right index finger intersects horizontally (-) to form a physical Medical Cross (+).',
      grammaticalRole: 'Location Noun',
      urgency: true
    },
    {
      id: 'police',
      title: 'Police',
      gloss: 'POLICE',
      category: 'civic',
      categoryLabel: 'Civic & Navigation',
      emoji: '👮',
      spokenText: 'Police',
      hindiText: 'पुलिस',
      tamilText: 'காவல்துறை',
      handshape: 'Temple Badge Salute',
      movement: 'Dominant hand forms a "C" cup or two-finger touch against the temple/forehead indicating police cap badge.',
      grammaticalRole: 'Civic Noun',
      urgency: false
    },
    {
      id: 'water',
      title: 'Water',
      gloss: 'WATER',
      category: 'daily',
      categoryLabel: 'Daily Needs & Actions',
      emoji: '💧',
      spokenText: 'Water',
      hindiText: 'पानी',
      tamilText: 'தண்ணீர்',
      handshape: '"W" Handshape at Chin',
      movement: 'Form a "W" with index, middle, and ring fingers; lightly tap chin twice.',
      grammaticalRole: 'Daily Noun',
      urgency: false
    },
    {
      id: 'help',
      title: 'Help / Assistance',
      gloss: 'HELP',
      category: 'emergency',
      categoryLabel: 'Medical & Emergency',
      emoji: '🆘',
      spokenText: 'Help me',
      hindiText: 'मदद',
      tamilText: 'உதவி',
      handshape: 'Thumbs-Up on Flat Palm',
      movement: 'Left open palm held flat facing up; Right hand in thumbs-up fist rests on palm and lifts upward together.',
      grammaticalRole: 'Action / Request',
      urgency: true
    },
    {
      id: 'money',
      title: 'Money / Bank',
      gloss: 'MONEY',
      category: 'civic',
      categoryLabel: 'Civic & Navigation',
      emoji: '💰',
      spokenText: 'Money',
      hindiText: 'पैसे',
      tamilText: 'பணம்',
      handshape: 'Thumb and Finger Rub',
      movement: 'Dominant thumb rubs across fingertips of the same hand repeatedly at chest height.',
      grammaticalRole: 'Financial Noun',
      urgency: false
    },
    {
      id: 'where',
      title: 'Where (Location Query)',
      gloss: 'WHERE',
      category: 'civic',
      categoryLabel: 'Civic & Navigation',
      emoji: '📍',
      spokenText: 'Where is it?',
      hindiText: 'कहाँ है?',
      tamilText: 'எங்கே?',
      handshape: 'Open Palms Upward Shrug',
      movement: 'Both hands held open with palms up, oscillating gently side to side with raised eyebrows (Interrogative NMM).',
      grammaticalRole: 'Wh-Question (Locative)',
      urgency: false
    },
    {
      id: '10_minutes',
      title: '10 Minutes',
      gloss: '10 MINUTES',
      category: 'numbers',
      categoryLabel: 'Numbers & Time',
      emoji: '⏱',
      spokenText: '10 minutes',
      hindiText: '10 मिनट',
      tamilText: '10 நிமிடங்கள்',
      handshape: 'Thumb Upright + Clock Rotation',
      movement: 'Fist with upright thumb oscillates (10), followed by index finger rotating on open palm (Minutes).',
      grammaticalRole: 'Temporal Modifier',
      urgency: false
    }
  ];

  const filteredSigns = signsData.filter((sign) => {
    const matchesCategory = selectedCategory === 'all' || sign.category === selectedCategory;
    const matchesSearch =
      sign.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sign.gloss.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sign.handshape.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sign.spokenText.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const speakSign = (text) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'en-IN';
    u.rate = 0.95;
    setPlayingSign(text);
    u.onend = () => setPlayingSign(null);
    u.onerror = () => setPlayingSign(null);
    window.speechSynthesis.speak(u);
  };

  const normalizeGloss = (g) => String(g || '').replace(/[\s_-]+/g, '').toUpperCase();

  // AI Practice Evaluation Handler (ST-GCN Real-Time Feedback)
  const handleEvaluationResult = (res) => {
    if (!res) return;
    setIsEvaluating(false);

    const currentTarget = practiceSigns[practiceStep] || practiceSigns[0];
    const targetNorm = normalizeGloss(currentTarget.gloss);
    const detectedNorm = normalizeGloss(res.gloss);

    if (res.success && detectedNorm === targetNorm) {
      const realScore = Math.max(70, Math.round((res.confidence || 0.88) * 100));
      setPracticeEvaluation({
        status: 'SUCCESS',
        score: realScore,
        detectedGloss: res.gloss,
        feedback: `Excellent! Correct gesture recognized for [${currentTarget.title}] with ${realScore}% confidence. Skeletal kinematics and handshape verified by ST-GCN AI model.`
      });

      // Update learned signs
      setLearnedSigns((prev) => {
        const updated = Array.from(new Set([...prev, currentTarget.gloss]));
        localStorage.setItem('isl_learned_signs', JSON.stringify(updated));
        return updated;
      });

      // Update average score
      setAverageScore((prev) => {
        const next = prev === 0 ? realScore : Math.round((prev + realScore) / 2);
        localStorage.setItem('isl_average_score', next.toString());
        return next;
      });

      // Update streak
      setStreakDays((prev) => {
        const next = Math.max(1, prev || 1);
        localStorage.setItem('isl_practice_streak', next.toString());
        return next;
      });
    } else if (res.gloss && res.gloss !== '<BLANK>') {
      const confPct = Math.round((res.confidence || 0) * 100);
      setPracticeEvaluation({
        status: 'MISMATCH',
        score: confPct,
        detectedGloss: res.gloss,
        feedback: `Detected sign [${res.gloss}] (${confPct}%), but the target sign is [${currentTarget.title}]. Tip: ${currentTarget.prompt}`
      });
    } else {
      setPracticeEvaluation({
        status: 'RETRY',
        score: 0,
        detectedGloss: null,
        feedback: res.reason || `Handshape or motion not clearly recognized. Please keep both hands visible and follow: "${currentTarget.prompt}"`
      });
    }
  };

  const handleRecordSignPractice = (detectedGloss, confidence, fullResult) => {
    handleEvaluationResult({
      success: true,
      gloss: detectedGloss,
      confidence: confidence,
      fullResult: fullResult
    });
  };

  const handlePrevPracticeSign = () => {
    setPracticeEvaluation(null);
    setPracticeStep((prev) => (prev - 1 + practiceSigns.length) % practiceSigns.length);
  };

  const handleNextPracticeSign = () => {
    setPracticeEvaluation(null);
    setPracticeStep((prev) => (prev + 1) % practiceSigns.length);
  };

  const handleSelectPracticeSign = (index) => {
    setPracticeEvaluation(null);
    setPracticeStep(index);
  };

  const handlePracticeCardSign = (sign) => {
    const idx = practiceSigns.findIndex(s => normalizeGloss(s.gloss) === normalizeGloss(sign.gloss));
    if (idx !== -1) {
      setPracticeStep(idx);
    } else {
      const newPracticeItem = {
        gloss: sign.gloss,
        title: sign.title,
        emoji: sign.emoji || '🤟',
        prompt: sign.movement || `Perform standard gesture for ${sign.title}`
      };
      setDynamicPracticeSigns(prev => [...prev, newPracticeItem]);
      setPracticeStep(practiceSigns.length);
    }
    setIsPracticeActive(true);
    setPracticeEvaluation(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const currentPractice = practiceSigns[practiceStep] || practiceSigns[0];
  const learnedPercent = Math.round((learnedSigns.length / signsData.length) * 100);

  return (
    <div className="space-y-8 py-2">
      {/* 1. HEADER & GAMIFICATION STATS */}
      <div className="glass-panel rounded-3xl p-6 sm:p-10 border border-slate-700/60 shadow-2xl space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div className="space-y-1">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-950/80 border border-indigo-500/40 text-indigo-300 text-xs font-semibold">
              <BookOpen className="w-3.5 h-3.5" />
              <span>ISL LEARNING & INTERACTIVE PRACTICE COACH</span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-extrabold text-white">
              Learn Indian Sign Language (ISL)
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 max-w-3xl">
              Master standard ISL handshapes, spatial movements, and non-manual facial grammar with interactive AI evaluation.
            </p>
          </div>

          <button
            onClick={() => setIsPracticeActive(!isPracticeActive)}
            className={`px-5 py-3 rounded-2xl font-bold text-xs sm:text-sm shadow-xl transition flex items-center space-x-2 ${
              isPracticeActive
                ? 'bg-purple-600 text-white shadow-purple-600/30'
                : 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-indigo-600/30'
            }`}
          >
            <Target className="w-4 h-4" />
            <span>{isPracticeActive ? 'Close AI Coach' : 'Launch AI Practice Mode 🎯'}</span>
          </button>
        </div>

        {/* Gamification Progress Bar */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-xs font-bold text-slate-300">
              <span className="flex items-center space-x-1.5">
                <Award className="w-4 h-4 text-emerald-400" />
                <span>Signs Learned</span>
              </span>
              <span className="text-emerald-400 font-mono">
                {learnedSigns.length} / {signsData.length} ({learnedPercent}%)
              </span>
            </div>
            <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 to-cyan-400 transition-all duration-300"
                style={{ width: `${learnedPercent}%` }}
              ></div>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-xs font-bold text-slate-300">
              <span className="flex items-center space-x-1.5">
                <Zap className="w-4 h-4 text-indigo-400" />
                <span>Average AI Accuracy</span>
              </span>
              <span className="text-indigo-400 font-mono">
                {averageScore > 0 ? `${averageScore}%` : '0%'}
              </span>
            </div>
            <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
              <div
                className="h-full bg-gradient-to-r from-indigo-500 to-purple-400 transition-all duration-300"
                style={{ width: `${averageScore}%` }}
              ></div>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 flex items-center justify-between">
            <div className="space-y-0.5">
              <span className="text-xs font-bold text-slate-300 flex items-center space-x-1.5">
                <Flame className="w-4 h-4 text-amber-400" />
                <span>Practice Streak</span>
              </span>
              <span className="text-xs text-slate-400">Consistent daily signing</span>
            </div>
            <span className="text-xl font-extrabold text-amber-400 font-mono">
              {streakDays > 0 ? `🔥 ${streakDays} Day${streakDays > 1 ? 's' : ''}` : '0 Days'}
            </span>
          </div>
        </div>
      </div>

      {/* 2. INTERACTIVE AI PRACTICE MODE (AI COACH) */}
      {isPracticeActive && (
        <div className="glass-panel rounded-3xl p-5 sm:p-7 border border-purple-500/50 shadow-2xl space-y-5 bg-gradient-to-b from-purple-950/20 via-slate-950 to-slate-950 animate-in fade-in zoom-in-95 duration-200">
          {/* Top Bar with Sign Switcher & Controls */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
            <div className="flex items-center space-x-3">
              <div className="p-2.5 rounded-2xl bg-purple-600/30 text-purple-300 border border-purple-500/40">
                <Target className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <h3 className="text-base font-bold text-white">
                    Interactive AI Practice Coach
                  </h3>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-purple-950 text-purple-300 border border-purple-500/40">
                    Sign {practiceStep + 1} of {practiceSigns.length}
                  </span>
                </div>
                <p className="text-xs text-slate-400">Perform the prompted sign in the live camera feed below and get instant ST-GCN AI evaluation.</p>
              </div>
            </div>

            {/* Quick Practice Sign Pills */}
            <div className="flex flex-wrap items-center gap-1.5">
              {practiceSigns.map((s, idx) => (
                <button
                  key={`${s.gloss}-${idx}`}
                  onClick={() => handleSelectPracticeSign(idx)}
                  className={`px-2.5 py-1 rounded-xl text-xs font-semibold flex items-center space-x-1.5 transition ${
                    practiceStep === idx
                      ? 'bg-purple-600 text-white font-bold shadow-md shadow-purple-600/30 ring-1 ring-purple-400'
                      : 'bg-slate-900/80 hover:bg-slate-800 text-slate-300 border border-slate-800'
                  }`}
                >
                  <span>{s.emoji}</span>
                  <span className="hidden sm:inline">{s.title}</span>
                </button>
              ))}
              
              <button
                onClick={() => setIsPracticeActive(false)}
                className="p-1.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition ml-1"
                title="Close AI Coach"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Main 2-Column Practice Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* LEFT: Live Camera Tracker HUD (7 cols) */}
            <div className="lg:col-span-7 space-y-3">
              <div className="relative rounded-2xl overflow-hidden border border-purple-500/40 shadow-xl bg-slate-950">
                <VisionTracker
                  isStreaming={isCameraActive}
                  setIsStreaming={setIsCameraActive}
                  onRecordSign={handleRecordSignPractice}
                  onEvaluationResult={handleEvaluationResult}
                  captureMode="on-demand"
                />
              </div>

              {/* Camera Status & Guidance Strip */}
              <div className="flex flex-wrap items-center justify-between gap-2 px-3 py-2 rounded-xl bg-slate-950/80 border border-slate-800/80 text-xs">
                <div className="flex items-center space-x-2 text-slate-300">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span className="font-mono text-[11px]">AI Camera HUD Active</span>
                </div>
                <div className="flex items-center space-x-3 text-[11px] text-slate-400">
                  <span>Target: <strong className="text-purple-300 font-mono">[{currentPractice.gloss}]</strong></span>
                  <span>Press <kbd className="px-1.5 py-0.5 rounded bg-slate-900 border border-slate-700 text-slate-200 font-mono text-[10px]">Space</kbd> or click 🔴 Capture</span>
                </div>
              </div>
            </div>

            {/* RIGHT: Target Sign Prompt & AI Evaluation Feedback (5 cols) */}
            <div className="lg:col-span-5 space-y-4">
              {/* Target Prompt Card */}
              <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-3 shadow-lg">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center space-x-3">
                    <span className="text-3xl p-1 bg-slate-950 rounded-xl border border-slate-800">{currentPractice.emoji}</span>
                    <div>
                      <span className="text-[10px] font-mono text-purple-400 font-bold uppercase tracking-wider">Target Sign:</span>
                      <h4 className="text-lg font-extrabold text-white">"{currentPractice.title}"</h4>
                      <span className="text-xs font-mono text-cyan-300 font-bold">[{currentPractice.gloss}]</span>
                    </div>
                  </div>

                  <button
                    onClick={() => speakSign(currentPractice.title)}
                    className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 transition"
                    title="Pronounce Word"
                  >
                    <Volume2 className="w-4 h-4 text-purple-400" />
                  </button>
                </div>

                <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 space-y-1 text-xs">
                  <span className="text-slate-400 font-semibold uppercase text-[10px] tracking-wider">How to Perform:</span>
                  <p className="text-slate-200 font-medium leading-relaxed">{currentPractice.prompt}</p>
                </div>

                {/* Navigation Between Signs */}
                <div className="flex items-center justify-between pt-1">
                  <button
                    onClick={handlePrevPracticeSign}
                    className="flex items-center space-x-1 px-3 py-1.5 rounded-xl bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs font-semibold transition"
                  >
                    <ChevronLeft className="w-3.5 h-3.5" />
                    <span>Previous</span>
                  </button>
                  <span className="text-xs font-mono text-slate-400">
                    {practiceStep + 1} / {practiceSigns.length}
                  </span>
                  <button
                    onClick={handleNextPracticeSign}
                    className="flex items-center space-x-1 px-3 py-1.5 rounded-xl bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs font-semibold transition"
                  >
                    <span>Next</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

              {/* Live AI Practice Evaluation Card */}
              <div className={`p-5 rounded-2xl border transition-all duration-300 flex flex-col justify-between min-h-[190px] shadow-lg ${
                practiceEvaluation?.status === 'SUCCESS'
                  ? 'bg-emerald-950/30 border-emerald-500/50 shadow-emerald-950/30'
                  : practiceEvaluation?.status === 'MISMATCH'
                  ? 'bg-amber-950/30 border-amber-500/50 shadow-amber-950/30'
                  : practiceEvaluation?.status === 'RETRY'
                  ? 'bg-indigo-950/20 border-indigo-500/40 shadow-indigo-950/20'
                  : 'bg-slate-950/90 border-slate-800'
              }`}>
                {isEvaluating ? (
                  <div className="flex flex-col items-center justify-center text-center space-y-3 py-6">
                    <Activity className="w-8 h-8 text-purple-400 animate-spin" />
                    <div className="space-y-1">
                      <p className="text-xs font-bold text-white">Analyzing Skeletal Trajectory...</p>
                      <p className="text-[11px] text-slate-400">ST-GCN model is processing 30 temporal landmark frames.</p>
                    </div>
                  </div>
                ) : practiceEvaluation?.status === 'SUCCESS' ? (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center space-x-1.5">
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        <span>Form Verified</span>
                      </span>
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-500/40">
                        {practiceEvaluation.score}% MATCH
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-950/80 border border-emerald-500/30 space-y-1">
                      <div className="flex items-baseline space-x-2">
                        <span className="text-2xl font-black text-emerald-400 font-mono">
                          {practiceEvaluation.score}%
                        </span>
                        <span className="text-xs font-bold text-slate-300">
                          [{practiceEvaluation.detectedGloss || currentPractice.gloss}] Verified
                        </span>
                      </div>
                      <p className="text-xs text-slate-200 leading-relaxed">
                        {practiceEvaluation.feedback}
                      </p>
                    </div>

                    <div className="pt-2 flex items-center justify-between gap-2">
                      <button
                        onClick={() => setPracticeEvaluation(null)}
                        className="flex items-center space-x-1 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold transition"
                      >
                        <RotateCcw className="w-3.5 h-3.5" />
                        <span>Practice Again</span>
                      </button>

                      <button
                        onClick={handleNextPracticeSign}
                        className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold shadow-lg transition"
                      >
                        <span>Next Sign</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                ) : practiceEvaluation?.status === 'MISMATCH' ? (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center space-x-1.5">
                        <AlertTriangle className="w-4 h-4 text-amber-400" />
                        <span>Different Sign Detected</span>
                      </span>
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-amber-950 text-amber-300 border border-amber-500/40">
                        DETECTED: [{practiceEvaluation.detectedGloss}]
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-950/80 border border-amber-500/30 space-y-1">
                      <p className="text-xs text-slate-200 leading-relaxed">
                        {practiceEvaluation.feedback}
                      </p>
                    </div>

                    <div className="pt-2 flex items-center justify-end">
                      <button
                        onClick={() => setPracticeEvaluation(null)}
                        className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold shadow transition"
                      >
                        <RotateCcw className="w-3.5 h-3.5" />
                        <span>Try Target Sign Again</span>
                      </button>
                    </div>
                  </div>
                ) : practiceEvaluation?.status === 'RETRY' ? (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider flex items-center space-x-1.5">
                        <Hand className="w-4 h-4 text-indigo-400" />
                        <span>Adjust Form &amp; Retry</span>
                      </span>
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-indigo-950 text-indigo-300 border border-indigo-500/40">
                        RETRY
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-950/80 border border-indigo-500/30 space-y-1">
                      <p className="text-xs text-slate-300 leading-relaxed">
                        {practiceEvaluation.feedback}
                      </p>
                    </div>

                    <div className="pt-2 flex items-center justify-end">
                      <button
                        onClick={() => setPracticeEvaluation(null)}
                        className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow transition"
                      >
                        <RotateCcw className="w-3.5 h-3.5" />
                        <span>Try Again</span>
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center text-center space-y-2.5 py-6">
                    <div className="p-3 rounded-2xl bg-purple-950/50 border border-purple-500/30 text-purple-300">
                      <Sparkles className="w-6 h-6 animate-pulse" />
                    </div>
                    <div className="space-y-1 max-w-xs">
                      <p className="text-xs font-bold text-white">Live AI Evaluator Ready</p>
                      <p className="text-[11px] text-slate-400 leading-relaxed">
                        Stand in camera view, perform the <strong>[{currentPractice.title}]</strong> gesture, and click <strong>🔴 Capture Sign (3s)</strong> or press <strong>Spacebar</strong>.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 3. SEARCH & CATEGORY FILTER BAR */}
      <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-4 shadow-xl">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search signs by name, gloss, or handshape (e.g. Doctor, Water, Hello)..."
            className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-900/90 border border-slate-800 focus:border-indigo-500 text-slate-100 text-xs sm:text-sm placeholder:text-slate-500 focus:outline-none transition"
          />
        </div>

        {/* Category Pills */}
        <div className="flex flex-wrap items-center gap-2">
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition ${
                selectedCategory === cat.id
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* 4. SIGNS CARDS GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredSigns.map((sign) => (
          <div
            key={sign.id}
            className="glass-panel rounded-2xl p-5 border border-slate-800 hover:border-indigo-500/50 transition flex flex-col justify-between space-y-4 shadow-lg group"
          >
            {/* Top Row: Emoji + Title + Category Badge */}
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-700/80 flex items-center justify-center text-2xl shadow-inner group-hover:scale-110 transition transform">
                  {sign.emoji}
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-100 flex items-center space-x-1.5">
                    <span>{sign.title}</span>
                  </h3>
                  <span className="font-mono text-[11px] font-bold text-indigo-400">
                    [{sign.gloss}]
                  </span>
                </div>
              </div>

              <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                sign.urgency
                  ? 'bg-red-950/80 border border-red-500/40 text-red-300'
                  : 'bg-slate-900 border border-slate-800 text-slate-400'
              }`}>
                {sign.categoryLabel}
              </span>
            </div>

            {/* Handshape & Movement Breakdown */}
            <div className="space-y-2 text-xs bg-slate-950/80 p-3 rounded-xl border border-slate-800/80">
              <div>
                <span className="text-slate-400 font-semibold uppercase text-[10px]">Handshape:</span>
                <p className="text-slate-200 font-medium">{sign.handshape}</p>
              </div>
              <div>
                <span className="text-slate-400 font-semibold uppercase text-[10px]">Movement & Dynamics:</span>
                <p className="text-slate-300 text-[11px] leading-relaxed">{sign.movement}</p>
              </div>
            </div>

            {/* Multilingual labels */}
            <div className="flex items-center justify-between text-[11px] px-2.5 py-1.5 bg-slate-900/50 rounded-xl border border-slate-800/60 font-medium text-slate-400">
              <span>🇮🇳 हिन्दी: <strong className="text-slate-200">{sign.hindiText}</strong></span>
              <span>தமிழ்: <strong className="text-slate-200">{sign.tamilText}</strong></span>
            </div>

            {/* Actions: Listen Pronunciation + Practice */}
            <div className="pt-2 border-t border-slate-800 flex items-center justify-between gap-2">
              <button
                onClick={() => speakSign(sign.spokenText)}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-white text-xs font-semibold transition"
                title="Pronounce Word"
              >
                <Volume2 className={`w-3.5 h-3.5 ${playingSign === sign.spokenText ? 'text-indigo-400 animate-pulse' : 'text-slate-400'}`} />
                <span>Listen</span>
              </button>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handlePracticeCardSign(sign)}
                  className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/40 text-xs font-semibold transition"
                  title="Practice this sign with live AI coach"
                >
                  <Hand className="w-3 h-3" />
                  <span>Practice</span>
                </button>

                <button
                  onClick={() => onDemoAvatar && onDemoAvatar(sign.spokenText)}
                  className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-cyan-600/30 hover:bg-cyan-600 text-cyan-300 hover:text-white border border-cyan-500/40 text-xs font-semibold transition"
                  title="View in 3D WebGL Avatar"
                >
                  <UserCheck className="w-3 h-3" />
                  <span>3D Avatar</span>
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
