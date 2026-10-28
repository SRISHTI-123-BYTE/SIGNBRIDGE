import React from 'react';
import {
  X,
  Settings,
  Camera,
  Volume2,
  Globe,
  Sliders,
  Eye,
  Type,
  Layers,
  Sparkles,
  CheckCircle2,
  Radio,
  Keyboard
} from 'lucide-react';

export default function SettingsModal({
  isOpen,
  onClose,
  settings,
  onUpdateSettings
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md overflow-y-auto">
      <div className="relative w-full max-w-2xl glass-panel rounded-3xl border border-slate-700/80 shadow-2xl p-6 sm:p-8 space-y-6 max-h-[90vh] overflow-y-auto">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center space-x-3 border-b border-slate-800 pb-4">
          <div className="p-2.5 rounded-2xl bg-indigo-600/20 border border-indigo-500/40 text-indigo-400">
            <Settings className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-slate-100">
              System & Accessibility Settings
            </h2>
            <p className="text-xs text-slate-400">
              Configure camera feeds, TTS speech rates, language defaults, and visual accessibility.
            </p>
          </div>
        </div>

        {/* Settings Sections */}
        <div className="space-y-5 text-xs sm:text-sm">
          {/* 1. Camera & Video Input */}
          <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-3">
            <div className="flex items-center space-x-2 text-indigo-400 font-bold text-xs uppercase tracking-wider">
              <Camera className="w-4 h-4" />
              <span>Camera Input Device</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                onClick={() => onUpdateSettings({ cameraSource: 'webcam' })}
                className={`p-3 rounded-xl border flex items-center justify-between text-xs font-semibold transition ${
                  settings.cameraSource === 'webcam'
                    ? 'bg-indigo-600/30 border-indigo-500 text-indigo-200 shadow'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                <span>Default Laptop Webcam</span>
                {settings.cameraSource === 'webcam' && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
              </button>

              <button
                onClick={() => onUpdateSettings({ cameraSource: 'simulator' })}
                className={`p-3 rounded-xl border flex items-center justify-between text-xs font-semibold transition ${
                  settings.cameraSource === 'simulator'
                    ? 'bg-indigo-600/30 border-indigo-500 text-indigo-200 shadow'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                <span>Synthetic Skeletal Simulator</span>
                {settings.cameraSource === 'simulator' && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
              </button>
            </div>
          </div>

          {/* 2. Translation & Language */}
          <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-3">
            <div className="flex items-center space-x-2 text-cyan-400 font-bold text-xs uppercase tracking-wider">
              <Globe className="w-4 h-4" />
              <span>Default Translation Language</span>
            </div>

            <div className="grid grid-cols-3 gap-2">
              {[
                { id: 'en', label: 'English' },
                { id: 'hi', label: 'Hindi (हिन्दी)' },
                { id: 'ta', label: 'Tamil (தமிழ்)' }
              ].map((lang) => (
                <button
                  key={lang.id}
                  onClick={() => onUpdateSettings({ defaultLang: lang.id })}
                  className={`p-2.5 rounded-xl border text-center text-xs font-bold transition ${
                    settings.defaultLang === lang.id
                      ? 'bg-cyan-600/30 border-cyan-500 text-cyan-200 shadow'
                      : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {lang.label}
                </button>
              ))}
            </div>
          </div>

          {/* 3. Audio & Speech Synthesis */}
          <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-3">
            <div className="flex items-center space-x-2 text-purple-400 font-bold text-xs uppercase tracking-wider">
              <Volume2 className="w-4 h-4" />
              <span>Speech & Audio Output</span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-300">Auto-Speak Spoken Sentence:</span>
              <button
                onClick={() => onUpdateSettings({ autoSpeak: !settings.autoSpeak })}
                className={`px-3 py-1 rounded-full text-xs font-bold border transition ${
                  settings.autoSpeak
                    ? 'bg-purple-600 text-white border-purple-500'
                    : 'bg-slate-900 text-slate-500 border-slate-800'
                }`}
              >
                {settings.autoSpeak ? 'ON' : 'OFF'}
              </button>
            </div>

            {/* Speech Speed Slider */}
            <div className="space-y-1 pt-1">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span>Speech Speed Rate:</span>
                <span className="font-mono text-purple-300 font-bold">{settings.speechRate || 1.0}x</span>
              </div>
              <input
                type="range"
                min="0.75"
                max="1.5"
                step="0.05"
                value={settings.speechRate || 1.0}
                onChange={(e) => onUpdateSettings({ speechRate: parseFloat(e.target.value) })}
                className="w-full h-1.5 bg-slate-900 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
            </div>
          </div>

          {/* 4. Accessibility Options (High Contrast & Font Size) */}
          <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-3">
            <div className="flex items-center space-x-2 text-emerald-400 font-bold text-xs uppercase tracking-wider">
              <Eye className="w-4 h-4" />
              <span>Accessibility Preferences</span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-300">High-Contrast Mode:</span>
              <button
                onClick={() => onUpdateSettings({ highContrast: !settings.highContrast })}
                className={`px-3 py-1 rounded-full text-xs font-bold border transition ${
                  settings.highContrast
                    ? 'bg-emerald-600 text-white border-emerald-500'
                    : 'bg-slate-900 text-slate-500 border-slate-800'
                }`}
              >
                {settings.highContrast ? 'ON' : 'OFF'}
              </button>
            </div>

            <div className="flex items-center justify-between pt-1">
              <span className="text-xs text-slate-300">Interface Font Scaling:</span>
              <div className="flex items-center space-x-1.5 bg-slate-900 p-1 rounded-xl border border-slate-800">
                {['normal', 'medium', 'large'].map((size) => (
                  <button
                    key={size}
                    onClick={() => onUpdateSettings({ fontSize: size })}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition ${
                      settings.fontSize === size
                        ? 'bg-emerald-600 text-white shadow'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {size === 'normal' ? 'A' : size === 'medium' ? 'A+' : 'A++'}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-2 border-t border-slate-800 flex items-center justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow transition"
          >
            Save & Close
          </button>
        </div>
      </div>
    </div>
  );
}

