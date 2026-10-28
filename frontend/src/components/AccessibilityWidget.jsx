import React, { useState } from 'react';
import {
  Eye,
  Type,
  Volume2,
  VolumeX,
  Keyboard,
  Sparkles,
  CheckCircle2,
  X,
  Sliders,
  Sun,
  ShieldCheck
} from 'lucide-react';

export default function AccessibilityWidget({
  isOpen,
  onClose,
  settings,
  onUpdateSettings
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="relative w-full max-w-lg glass-panel rounded-3xl border border-slate-700/80 shadow-2xl p-6 sm:p-8 space-y-6 animate-in fade-in zoom-in-95 duration-200">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center space-x-3 border-b border-slate-800 pb-4">
          <div className="p-2.5 rounded-2xl bg-indigo-600/20 border border-indigo-500/40 text-indigo-400">
            <Eye className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-slate-100 uppercase tracking-tight">
              Accessibility Controls
            </h2>
            <p className="text-xs text-slate-400">
              Customize contrast, typography scaling, speech feedback, and motion.
            </p>
          </div>
        </div>

        {/* Accessibility Features */}
        <div className="space-y-4 text-xs sm:text-sm">
          {/* 1. Text Size Scaling */}
          <div className="bg-slate-950/90 p-4 rounded-2xl border border-slate-800 flex items-center justify-between">
            <div className="space-y-0.5">
              <span className="font-bold text-slate-200 block">Text Size Scaling</span>
              <span className="text-[11px] text-slate-400">Adjust layout readability</span>
            </div>

            <div className="flex items-center space-x-1.5 bg-slate-900 p-1 rounded-xl border border-slate-800">
              {[
                { id: 'normal', label: 'A−' },
                { id: 'medium', label: 'A' },
                { id: 'large', label: 'A+' }
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => onUpdateSettings({ fontSize: item.id })}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                    settings.fontSize === item.id
                      ? 'bg-indigo-600 text-white shadow-md'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          {/* 2. High Contrast */}
          <div className="bg-slate-950/90 p-4 rounded-2xl border border-slate-800 flex items-center justify-between">
            <div className="space-y-0.5">
              <span className="font-bold text-slate-200 block">High Contrast Mode</span>
              <span className="text-[11px] text-slate-400">Enhance edge contrast and text sharpness</span>
            </div>

            <button
              onClick={() => onUpdateSettings({ highContrast: !settings.highContrast })}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                settings.highContrast ? 'bg-emerald-500' : 'bg-slate-800'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  settings.highContrast ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          {/* 3. Reduced Motion */}
          <div className="bg-slate-950/90 p-4 rounded-2xl border border-slate-800 flex items-center justify-between">
            <div className="space-y-0.5">
              <span className="font-bold text-slate-200 block">Reduced Motion</span>
              <span className="text-[11px] text-slate-400">Minimize animations and transition effects</span>
            </div>

            <button
              onClick={() => onUpdateSettings({ reducedMotion: !settings.reducedMotion })}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                settings.reducedMotion ? 'bg-indigo-500' : 'bg-slate-800'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  settings.reducedMotion ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          {/* 4. Text-to-Speech Output */}
          <div className="bg-slate-950/90 p-4 rounded-2xl border border-slate-800 flex items-center justify-between">
            <div className="space-y-0.5">
              <span className="font-bold text-slate-200 block">Spoken Audio Output</span>
              <span className="text-[11px] text-slate-400">Automatically speak translated sentences</span>
            </div>

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

          {/* 5. Keyboard Navigation Status */}
          <div className="bg-slate-950/90 p-4 rounded-2xl border border-slate-800 flex items-center justify-between">
            <div className="flex items-center space-x-2.5">
              <Keyboard className="w-4 h-4 text-cyan-400" />
              <div>
                <span className="font-bold text-slate-200 block">Keyboard Operability</span>
                <span className="text-[11px] text-slate-400">Full Tab / Enter / Space shortcut support</span>
              </div>
            </div>
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-950/80 border border-emerald-500/40 text-emerald-300">
              ACTIVE (ON)
            </span>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-2 border-t border-slate-800 flex items-center justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white font-bold text-xs shadow-lg transition"
          >
            Apply & Close
          </button>
        </div>
      </div>
    </div>
  );
}
