import React, { useState } from 'react';
import { Play, Sparkles, Activity, ShieldAlert, Compass, Building2, UserCheck, CheckCircle2, ChevronRight, Volume2 } from 'lucide-react';
import { signBridgeService } from '../services/api';

export default function ScenarioDemos({ onApplyScenario, setActiveTab }) {
  const [activeScenarioId, setActiveScenarioId] = useState('emergency');
  const [isLoading, setIsLoading] = useState(false);

  const scenarios = [
    {
      id: 'emergency',
      title: 'Scenario 1: Healthcare Emergency',
      category: 'Triage / Hospital Care',
      icon: ShieldAlert,
      iconColor: 'text-red-400 bg-red-950/60 border-red-500/30',
      badge: 'Critical Care',
      signerActions: ['DOCTOR', 'CHEST', 'PAIN', 'SEVERE'],
      englishText: 'Doctor, I am experiencing severe chest pain.',
      hindiText: 'डॉक्टर, मुझे सीने में बहुत तेज़ दर्द हो रहा है।',
      tamilText: 'மருத்துவரே, எனக்கு கடுமையான மார்பு வலி உள்ளது.',
      targetLatency: '88 ms'
    },
    {
      id: 'police',
      title: 'Scenario 2: Public Navigation & Police',
      category: 'Civic Infrastructure',
      icon: Compass,
      iconColor: 'text-cyan-400 bg-cyan-950/60 border-cyan-500/30',
      badge: 'Public Safety',
      signerActions: ['POLICE', 'STATION', 'WHERE'],
      englishText: 'Where is the nearest police station?',
      hindiText: 'निकटतम पुलिस स्टेशन कहाँ है?',
      tamilText: 'அருகிலுள்ள காவல் நிலையம் எங்கே இருக்கிறது?',
      targetLatency: '84 ms'
    },
    {
      id: 'hospital',
      title: 'Scenario 3: Hospital Direction Guidance',
      category: 'Healthcare Access',
      icon: Activity,
      iconColor: 'text-emerald-400 bg-emerald-950/60 border-emerald-500/30',
      badge: 'Emergency Navigation',
      signerActions: ['HOSPITAL', 'GO', 'HOW'],
      englishText: 'How do I go to the hospital?',
      hindiText: 'अस्पताल कैसे जाना है?',
      tamilText: 'மருத்துவமனைக்கு எப்படி செல்வது?',
      targetLatency: '86 ms'
    },
    {
      id: 'banking',
      title: 'Scenario 4: Banking & Financial Transactions',
      category: 'Financial Inclusion',
      icon: Building2,
      iconColor: 'text-amber-400 bg-amber-950/60 border-amber-500/30',
      badge: 'Civic Banking',
      signerActions: ['MONEY', 'ACCOUNT', 'BANK', 'DEPOSIT'],
      englishText: 'I want to deposit money into my bank account.',
      hindiText: 'मैं अपने बैंक खाते में पैसे जमा करना चाहता हूँ।',
      tamilText: 'நான் எனது வங்கிக் கணக்கில் பணம் டெபாசிட் செய்ய விரும்புகிறேன்.',
      targetLatency: '91 ms'
    },
    {
      id: 'reverse_demo',
      title: 'Scenario 5: Reverse Flow (Hearing to Deaf)',
      category: 'Bi-Directional Speech-to-Sign',
      icon: UserCheck,
      iconColor: 'text-indigo-400 bg-indigo-950/60 border-indigo-500/30',
      badge: '3D WebGL Avatar',
      spokenInput: 'Please sit down and wait for 10 minutes.',
      signerActions: ['SIT', 'WAIT', '10', 'MINUTES'],
      englishText: 'Avatar renders procedural ISL signs [SIT] [WAIT] [10] [MINUTES].',
      hindiText: '3D अवतार सांकेतिक भाषा प्रस्तुत करता है।',
      tamilText: '3D அவதார் சைகை மொழியை செய்கிறது.',
      targetLatency: '24 ms',
      isReverse: true
    }
  ];

  const handleRunScenario = async (sc) => {
    setIsLoading(true);
    setActiveScenarioId(sc.id);

    if (sc.isReverse) {
      if (setActiveTab) setActiveTab('avatar');
      setIsLoading(false);
      return;
    }

    const result = await signBridgeService.simulateScenario(sc.id);
    if (onApplyScenario) {
      onApplyScenario(result);
    }
    if (setActiveTab) {
      setActiveTab('recognition');
    }
    setIsLoading(false);
  };

  const speakPreview = (text, lang) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    if (lang === 'hi') u.lang = 'hi-IN';
    else if (lang === 'ta') u.lang = 'ta-IN';
    else u.lang = 'en-IN';
    window.speechSynthesis.speak(u);
  };

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-700/60 shadow-2xl flex flex-col space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-lg font-bold text-slate-100 flex items-center space-x-2">
            <span>Live Demonstration & Evaluation Protocol</span>
            <span className="px-2.5 py-0.5 rounded-full text-xs bg-indigo-950/80 border border-indigo-500/40 text-indigo-300 font-mono">
              5 Canonical Scenarios
            </span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Pre-configured validation suite matching presentation protocol for jury demonstrations.
          </p>
        </div>
      </div>

      {/* Scenario Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {scenarios.map((sc) => {
          const IconComp = sc.icon;
          const isSelected = activeScenarioId === sc.id;

          return (
            <div
              key={sc.id}
              className={`rounded-xl p-4 border flex flex-col justify-between space-y-3 transition-all ${
                isSelected
                  ? 'bg-slate-900/90 border-indigo-500/70 shadow-lg ring-1 ring-indigo-500/40'
                  : 'bg-slate-950/70 border-slate-800 hover:border-slate-700'
              }`}
            >
              {/* Header */}
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2.5">
                  <div className={`p-2 rounded-lg border ${sc.iconColor}`}>
                    <IconComp className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-slate-100">{sc.title}</h3>
                    <span className="text-[10px] text-slate-400">{sc.category}</span>
                  </div>
                </div>
                <span className="px-2 py-0.5 rounded text-[9px] font-mono bg-slate-900 border border-slate-800 text-slate-400">
                  {sc.badge}
                </span>
              </div>

              {/* ISL Gestures Flow */}
              <div className="space-y-1 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
                <div className="text-[10px] text-slate-400 uppercase font-semibold">
                  {sc.isReverse ? 'Spoken Input ➔ ISL Output:' : 'ISL Signer Actions (Gestures):'}
                </div>
                <div className="flex flex-wrap items-center gap-1.5 pt-1">
                  {sc.signerActions.map((g, idx) => (
                    <React.Fragment key={idx}>
                      <span className="px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 font-mono text-[11px] font-bold border border-indigo-800/50">
                        {g}
                      </span>
                      {idx < sc.signerActions.length - 1 && (
                        <ChevronRight className="w-3 h-3 text-slate-600" />
                      )}
                    </React.Fragment>
                  ))}
                </div>
              </div>

              {/* Translation Previews */}
              <div className="space-y-1.5 text-xs">
                <div className="p-2 rounded bg-slate-950/80 border border-slate-800/80 text-slate-200 font-medium flex items-center justify-between">
                  <span className="text-[11px] italic">"{sc.englishText}"</span>
                  <button
                    onClick={() => speakPreview(sc.englishText, 'en')}
                    className="p-1 rounded text-slate-400 hover:text-indigo-300 transition"
                    title="Speak Preview"
                  >
                    <Volume2 className="w-3.5 h-3.5" />
                  </button>
                </div>
                <div className="px-2 py-1 text-[11px] text-amber-300/90 font-medium truncate">
                  {sc.hindiText}
                </div>
              </div>

              {/* Action Button */}
              <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
                <span className="text-[10px] text-emerald-400 font-mono">
                  Latency: ~{sc.targetLatency}
                </span>
                <button
                  onClick={() => handleRunScenario(sc)}
                  disabled={isLoading}
                  className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 text-white text-xs font-semibold hover:bg-indigo-500 transition shadow"
                >
                  <Play className="w-3 h-3 fill-current" />
                  <span>{sc.isReverse ? 'Open 3D Avatar' : 'Run Live Demo'}</span>
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
