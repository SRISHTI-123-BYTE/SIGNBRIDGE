import React from 'react';
import { X, Layers, Cpu, Database, Volume2, ShieldCheck, CheckCircle2, GitBranch, ArrowDown, Sparkles } from 'lucide-react';

export default function ArchitectureModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md overflow-y-auto">
      <div className="relative w-full max-w-4xl glass-panel rounded-2xl border border-slate-700/80 shadow-2xl p-6 space-y-6 max-h-[90vh] overflow-y-auto">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="border-b border-slate-800 pb-4">
          <div className="flex items-center space-x-2.5">
            <div className="p-2 rounded-xl bg-indigo-600/20 border border-indigo-500/40 text-indigo-400">
              <Layers className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-100">
                SignBridge System Architecture & Mathematical Formulation
              </h2>
              <p className="text-xs text-slate-400">
                Edge-Compute Continuous ISL Recognition, ST-GCN, CTC Sequence Alignment & Reverse 3D Avatar
              </p>
            </div>
          </div>
        </div>

        {/* 5-Stage Architecture Flow */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold text-indigo-400 uppercase tracking-wider">
            1. End-to-End Deep Learning Pipeline
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-2.5 text-xs">
            {/* Stage 1 */}
            <div className="bg-slate-950/90 rounded-xl p-3 border border-slate-800 space-y-1.5">
              <span className="text-[10px] font-mono text-emerald-400 font-bold">STAGE 01</span>
              <h4 className="font-bold text-slate-200">Vision Ingestion</h4>
              <p className="text-[11px] text-slate-400 leading-snug">
                MediaPipe Holistic extracts 107 3D landmarks (Hands 42, Pose 25, Face 40) at 30 FPS.
              </p>
            </div>

            {/* Stage 2 */}
            <div className="bg-slate-950/90 rounded-xl p-3 border border-slate-800 space-y-1.5">
              <span className="text-[10px] font-mono text-cyan-400 font-bold">STAGE 02</span>
              <h4 className="font-bold text-slate-200">Affine Normalization</h4>
              <p className="text-[11px] text-slate-400 leading-snug">
                Torso-centering & Euclidean shoulder distance scale normalization for geometric invariance.
              </p>
            </div>

            {/* Stage 3 */}
            <div className="bg-slate-950/90 rounded-xl p-3 border border-slate-800 space-y-1.5">
              <span className="text-[10px] font-mono text-indigo-400 font-bold">STAGE 03</span>
              <h4 className="font-bold text-slate-200">ST-GCN / Bi-LSTM</h4>
              <p className="text-[11px] text-slate-400 leading-snug">
                Spatial-temporal graph convolution G=(V,E) over sliding window T=30 with spatial attention.
              </p>
            </div>

            {/* Stage 4 */}
            <div className="bg-slate-950/90 rounded-xl p-3 border border-slate-800 space-y-1.5">
              <span className="text-[10px] font-mono text-amber-400 font-bold">STAGE 04</span>
              <h4 className="font-bold text-slate-200">CTC Decoding</h4>
              <p className="text-[11px] text-slate-400 leading-snug">
                Alignment-free CTC decoder collapses consecutive tokens and eliminates blank tokens.
              </p>
            </div>

            {/* Stage 5 */}
            <div className="bg-slate-950/90 rounded-xl p-3 border border-slate-800 space-y-1.5">
              <span className="text-[10px] font-mono text-purple-400 font-bold">STAGE 05</span>
              <h4 className="font-bold text-slate-200">NLP & Reverse 3D</h4>
              <p className="text-[11px] text-slate-400 leading-snug">
                Topic-Comment to English, Hindi, and Tamil + Three.js 3D WebGL Avatar for speech-to-sign.
              </p>
            </div>
          </div>
        </div>

        {/* Mathematical Formulations */}
        <div className="space-y-3 pt-2 border-t border-slate-800">
          <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
            2. Mathematical & Algorithmic Formulations
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            {/* Formula 1 */}
            <div className="bg-slate-950/90 rounded-xl p-3.5 border border-slate-800 space-y-2">
              <h4 className="font-bold text-slate-200">Geometric Coordinate Normalization</h4>
              <div className="bg-slate-900 p-2.5 rounded-lg font-mono text-[11px] text-indigo-300 space-y-1">
                <div>P_center = (P_left_shoulder + P_right_shoulder) / 2</div>
                <div>d_scale = ||P_left_shoulder - P_right_shoulder||_2</div>
                <div>P̂_i(t) = (P_i(t) - P_center(t)) / d_scale(t)</div>
              </div>
              <p className="text-[11px] text-slate-400">
                Eliminates camera distance, height differences, and lateral user positioning variations.
              </p>
            </div>

            {/* Formula 2 */}
            <div className="bg-slate-950/90 rounded-xl p-3.5 border border-slate-800 space-y-2">
              <h4 className="font-bold text-slate-200">Spatial-Temporal Graph Convolution</h4>
              <div className="bg-slate-900 p-2.5 rounded-lg font-mono text-[11px] text-cyan-300 space-y-1">
                <div>X_out = Σ_k W_k ( X_in ( D_k^(-1/2) A_k D_k^(-1/2) ) ⊙ M_k ) Θ_k</div>
              </div>
              <p className="text-[11px] text-slate-400">
                Where A_k is the skeletal adjacency matrix, M_k is learnable spatial attention, and Θ_k is the 1D temporal convolution kernel.
              </p>
            </div>
          </div>
        </div>

        {/* Dataset Benchmarks */}
        <div className="space-y-3 pt-2 border-t border-slate-800">
          <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
            3. Datasets & Benchmark Evaluation
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div className="bg-slate-950/90 p-3 rounded-xl border border-slate-800 space-y-1">
              <h4 className="font-bold text-slate-200">AI4Bharat INCLUDE</h4>
              <p className="text-[11px] text-slate-400">
                4,287 clips spanning 263 ISL signs across medical, civic, emergency, and daily domains.
              </p>
            </div>
            <div className="bg-slate-950/90 p-3 rounded-xl border border-slate-800 space-y-1">
              <h4 className="font-bold text-slate-200">ISL-CSLTR Continuous</h4>
              <p className="text-[11px] text-slate-400">
                Continuous sentence-level video sequences with paired grammatical annotations and co-articulation.
              </p>
            </div>
            <div className="bg-slate-950/90 p-3 rounded-xl border border-slate-800 space-y-1">
              <h4 className="font-bold text-slate-200">Synthetic Augmentations</h4>
              <p className="text-[11px] text-slate-400">
                Temporal Warping (±20%), 3D Gaussian Jittering (σ=0.015), and 3D Rotation matrices (±15°).
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
