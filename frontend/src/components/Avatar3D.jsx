import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import {
  Mic,
  MicOff,
  Play,
  Pause,
  RotateCcw,
  Volume2,
  Sparkles,
  Send,
  UserCheck,
  FastForward,
  Camera,
  Info,
  Layers,
  ChevronRight,
  BookOpen
} from 'lucide-react';
import { signBridgeService } from '../services/api';

// Canonical ISL dictionary definitions with linguistic annotations
const ISL_SIGN_DICTIONARY = {
  SIT: {
    category: "Action / Position",
    handshape: "Dominant 'V' (legs) on Non-Dominant 'H' (bench)",
    description: "Left hand forms horizontal flat seat with index and middle fingers; Right hand forms 'V' hooked fingers and descends to rest on them.",
    duration: 1300
  },
  WAIT: {
    category: "Action / Time",
    handshape: "Open-5 Fluttering Hands",
    description: "Both hands raised in front of chest at 45°, palms facing body, fingers fluttering sequentially in waves.",
    duration: 1300
  },
  "10": {
    category: "Number / Digit",
    handshape: "Fist with Upright Thumb (ISL 10)",
    description: "Right hand forms fist with thumb extended straight up near shoulder, oscillating side-to-side rapidly.",
    duration: 1100
  },
  MINUTES: {
    category: "Time / Unit",
    handshape: "Clock Hand Pointer on Flat Palm",
    description: "Left open palm held flat facing up; Right index finger points into palm and rotates clockwise like a minute hand.",
    duration: 1300
  },
  DOCTOR: {
    category: "Medical / Profession",
    handshape: "Double Finger Pulse Tap",
    description: "Left forearm held horizontal; Right index and middle fingers tap the pulse on inside of left wrist twice.",
    duration: 1300
  },
  CHEST: {
    category: "Anatomy",
    handshape: "Flat Open Palms",
    description: "Both flat open palms press gently against upper chest / sternum.",
    duration: 1100
  },
  PAIN: {
    category: "Medical / Sensation",
    handshape: "Dual Index Pointers Twisting",
    description: "Both index fingers point toward each other at center torso and twist/counter-rotate with urgency.",
    duration: 1200
  },
  SEVERE: {
    category: "Intensity / Modifier",
    handshape: "Forceful Downward Sweep",
    description: "Both open flat hands start high at shoulders and sweep down and forward with intense expression.",
    duration: 1100
  },
  POLICE: {
    category: "Civic / Service",
    handshape: "Temple Badge Salute",
    description: "Right hand forms 'C' / salute touching right temple/forehead (police cap/badge).",
    duration: 1200
  },
  STATION: {
    category: "Location / Building",
    handshape: "Boundary Box Corners",
    description: "Both flat hands form vertical right-angle boundary walls outlining a building space.",
    duration: 1200
  },
  WHERE: {
    category: "Interrogative / Question",
    handshape: "Open Palms Upward Shrug",
    description: "Both hands held in front with palms up, sweeping outward side-to-side with head tilt and raised eyebrows.",
    duration: 1200
  },
  HOSPITAL: {
    category: "Medical / Location",
    handshape: "Two-Handed Intersecting Cross (+)",
    description: "Left index finger held vertically (|); Right index finger held horizontally (-) intersects and taps across it at a 90° right angle to form a distinct physical Medical Cross (+) shape.",
    duration: 1300
  },
  GO: {
    category: "Direction / Action",
    handshape: "Forward Index Sweep",
    description: "Right index finger points forward and sweeps outward away from body.",
    duration: 1000
  },
  HOW: {
    category: "Interrogative / Question",
    handshape: "Curved Hands Roll Upward",
    description: "Both hands start with backs facing near chest, then roll outward and upward until palms face up.",
    duration: 1200
  },
  HELP: {
    category: "Emergency / Assistance",
    handshape: "Fist on Supporting Palm Lift",
    description: "Left palm flat facing up; Right 'A' fist with thumb up placed on left palm, both hands lifting up together.",
    duration: 1200
  },
  ME: {
    category: "Pronoun",
    handshape: "Index Point to Chest",
    description: "Right index finger points directly to center of chest.",
    duration: 1000
  },
  PLEASE: {
    category: "Social / Etiquette",
    handshape: "Circular Chest Rub",
    description: "Right open flat palm placed on center of chest and rubbed in gentle clockwise circles.",
    duration: 1200
  },
  HELLO: {
    category: "Social / Greeting",
    handshape: "Open Palm Wave / Salute",
    description: "Right open flat hand raised near right temple and waves outward gracefully.",
    duration: 1100
  },
  THANK_YOU: {
    category: "Social / Gratitude",
    handshape: "Chin Forward Arc",
    description: "Right flat fingers touch chin/lips, then move forward and down toward viewer with polite head nod.",
    duration: 1200
  },
  YES: {
    category: "Affirmation",
    handshape: "Nodding Fist",
    description: "Right fist held at shoulder height, wrist bending up and down like a nodding head.",
    duration: 1100
  },
  NO: {
    category: "Negation",
    handshape: "Two-Finger Snap",
    description: "Right index and middle fingers extended, snapping down firmly onto thumb with slight head shake.",
    duration: 1100
  },
  WATER: {
    category: "Daily Need",
    handshape: "'W' Lip Tap",
    description: "Right hand forms 'W' (index, middle, ring extended) and taps side of mouth twice.",
    duration: 1100
  },
  TIME: {
    category: "Time / Inquiry",
    handshape: "Watch Tap",
    description: "Left forearm horizontal; Right index finger taps the back of left wrist twice.",
    duration: 1100
  }
};

export default function Avatar3D() {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const avatarRigRef = useRef(null);
  const animationFrameRef = useRef(null);

  const [spokenInput, setSpokenInput] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isPlaying, setIsPlaying] = useState(true);
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
  const [cameraView, setCameraView] = useState('front'); // 'front' | 'perspective' | 'closeup'
  const [activeSignIndex, setActiveSignIndex] = useState(0);
  const [glossSequence, setGlossSequence] = useState([
    { gloss: "HELLO", duration_ms: 1100 }
  ]);

  const activeSignKey = glossSequence[activeSignIndex]?.gloss || "HELLO";
  const activeSignMeta = ISL_SIGN_DICTIONARY[activeSignKey] || {
    category: "ISL Sign",
    handshape: "Standard Sign Pose",
    description: "Signing " + activeSignKey,
    duration: 1200
  };

  // Speech Recognition (Web Speech API)
  const toggleSpeechRecognition = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert("Speech recognition is not supported in this browser. You can type in the box directly.");
      return;
    }

    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRec();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    if (!isListening) {
      recognition.start();
      setIsListening(true);
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setSpokenInput(transcript);
        handleTranslateAndSign(transcript);
        setIsListening(false);
      };
      recognition.onerror = () => setIsListening(false);
      recognition.onend = () => setIsListening(false);
    } else {
      recognition.stop();
      setIsListening(false);
    }
  };

  const handleTranslateAndSign = async (text) => {
    if (!text.trim()) return;
    const res = await signBridgeService.speechToSign(text);
    if (res.isl_gloss_sequence && res.isl_gloss_sequence.length > 0) {
      setGlossSequence(res.isl_gloss_sequence);
      setActiveSignIndex(0);
      setIsPlaying(true);
    }
  };

  const handleSingleSignSelect = (signKey) => {
    setGlossSequence([{ gloss: signKey, duration_ms: ISL_SIGN_DICTIONARY[signKey]?.duration || 1200 }]);
    setActiveSignIndex(0);
    setIsPlaying(true);
  };

  // Camera preset switcher
  useEffect(() => {
    if (!cameraRef.current) return;
    const camera = cameraRef.current;
    if (cameraView === 'front') {
      camera.position.set(0, 1.35, 2.5);
      camera.lookAt(0, 1.2, 0);
    } else if (cameraView === 'perspective') {
      camera.position.set(1.4, 1.45, 2.3);
      camera.lookAt(0, 1.2, 0);
    } else if (cameraView === 'closeup') {
      camera.position.set(0, 1.15, 1.6);
      camera.lookAt(0, 1.1, 0);
    }
  }, [cameraView]);

  // --- Three.js 3D WebGL Avatar Setup ---
  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 450;

    // Scene & Camera
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 1000);
    camera.position.set(0, 1.35, 2.5);
    camera.lookAt(0, 1.2, 0);
    cameraRef.current = camera;

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    rendererRef.current = renderer;
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // Studio Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const mainKeyLight = new THREE.DirectionalLight(0xffffff, 1.1);
    mainKeyLight.position.set(2, 3.5, 3);
    mainKeyLight.castShadow = true;
    scene.add(mainKeyLight);

    const cyanRimLight = new THREE.DirectionalLight(0x06b6d4, 0.9);
    cyanRimLight.position.set(-3, 2, -2);
    scene.add(cyanRimLight);

    const purpleFillLight = new THREE.DirectionalLight(0x818cf8, 0.5);
    purpleFillLight.position.set(2.5, -1, -2);
    scene.add(purpleFillLight);

    // Modern Pedestal / Stage
    const pedestalGeo = new THREE.CylinderGeometry(1.1, 1.2, 0.08, 32);
    const pedestalMat = new THREE.MeshStandardMaterial({
      color: 0x090d16,
      roughness: 0.3,
      metalness: 0.8
    });
    const pedestal = new THREE.Mesh(pedestalGeo, pedestalMat);
    pedestal.position.y = 0;
    pedestal.receiveShadow = true;
    scene.add(pedestal);

    // Glowing stage ring
    const ringGeo = new THREE.RingGeometry(0.95, 1.05, 32);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0x6366f1, side: THREE.DoubleSide });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = 0.045;
    scene.add(ring);

    // --- Build Full-Articulated Humanoid Avatar Rig ---
    const avatarGroup = new THREE.Group();
    avatarRigRef.current = buildFullArticulatedAvatar(avatarGroup);
    scene.add(avatarGroup);

    // Handle Window Resize
    const handleResize = () => {
      if (!container || !rendererRef.current) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      rendererRef.current.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    // Animation Clock & Loop
    let clock = new THREE.Clock();
    let currentSignTime = 0;

    const animate = () => {
      const delta = clock.getDelta();
      const elapsedTime = clock.getElapsedTime();

      if (avatarRigRef.current) {
        const rig = avatarRigRef.current;

        // Subtle realistic idle breathing motion
        rig.chest.position.y = 1.15 + Math.sin(elapsedTime * 1.6) * 0.004;
        rig.head.rotation.y = Math.sin(elapsedTime * 0.6) * 0.03;

        // Animate Current ISL Sign
        if (glossSequence.length > 0) {
          const currentGlossObj = glossSequence[activeSignIndex] || glossSequence[0];
          const duration = (currentGlossObj.duration_ms || 1200) / 1000 / playbackSpeed;

          if (isPlaying) {
            currentSignTime += delta;
            if (currentSignTime >= duration) {
              currentSignTime = 0;
              setActiveSignIndex((prev) => (prev + 1) % glossSequence.length);
            }
          }

          const progress = Math.min(currentSignTime / duration, 1.0);
          applyAccurateISLSign(rig, currentGlossObj.gloss, progress, elapsedTime);
        }
      }

      renderer.render(scene, camera);
      animationFrameRef.current = requestAnimationFrame(animate);
    };

    animationFrameRef.current = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
      if (rendererRef.current && container) {
        container.innerHTML = '';
      }
    };
  }, [glossSequence, isPlaying, playbackSpeed, activeSignIndex]);

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-700/60 shadow-2xl flex flex-col space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-cyan-600/20 border border-cyan-500/40 text-cyan-400">
            <UserCheck className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-100 flex items-center space-x-2">
              <span>Speech-to-Sign 3D WebGL Avatar</span>
              <span className="px-2 py-0.5 rounded-full text-[10px] bg-cyan-950/80 border border-cyan-500/40 text-cyan-300 font-mono">
                5-Finger Articulated ISL Rig
              </span>
            </h3>
            <p className="text-xs text-slate-400">Accurate Indian Sign Language postures, non-manual markers & finger kinematics</p>
          </div>
        </div>

        {/* View & Speed Toolbar */}
        <div className="flex items-center space-x-2">
          {/* Camera View Selector */}
          <div className="flex items-center space-x-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
            <span className="text-slate-400 px-1 text-[11px]">View:</span>
            {[
              { id: 'front', label: 'Front' },
              { id: 'perspective', label: '3/4 Angle' },
              { id: 'closeup', label: 'Hands Close' }
            ].map((v) => (
              <button
                key={v.id}
                onClick={() => setCameraView(v.id)}
                className={`px-2 py-1 rounded text-[11px] font-medium transition ${
                  cameraView === v.id ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {v.label}
              </button>
            ))}
          </div>

          {/* Speed Selector */}
          <div className="flex items-center space-x-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
            <span className="text-slate-400 px-1 text-[11px]">Speed:</span>
            {[0.5, 1.0, 1.5, 2.0].map((s) => (
              <button
                key={s}
                onClick={() => setPlaybackSpeed(s)}
                className={`px-2 py-1 rounded font-mono font-semibold text-[11px] transition ${
                  playbackSpeed === s
                    ? 'bg-cyan-600 text-white shadow'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {s}x
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Avatar 3D Viewport & Sign Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* 3D WebGL Viewport + Down-of-Avatar Status Card */}
        <div className="lg:col-span-8 flex flex-col space-y-3.5">
          <div className="relative aspect-[16/10] bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden flex items-center justify-center shadow-2xl">
            <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

            {/* Playback Controls Overlay (Bottom Right) */}
            <div className="absolute bottom-3 right-3 flex items-center space-x-2 bg-slate-900/90 backdrop-blur-md p-1.5 rounded-xl border border-slate-800 shadow-lg z-10">
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="p-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-500 transition shadow"
                title={isPlaying ? "Pause" : "Play"}
              >
                {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              </button>
              <button
                onClick={() => {
                  setActiveSignIndex(0);
                  setIsPlaying(true);
                }}
                className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition"
                title="Repeat Sequence"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* EXACT CARD DISPLAYED AT DOWN OF AVATAR */}
          <div className="bg-[#070c18] border-[1.5px] border-[#06b6d4]/70 p-4 sm:p-5 rounded-2xl shadow-[0_0_20px_rgba(6,182,212,0.18)] space-y-2">
            <div className="flex items-center space-x-2.5">
              <span className="w-3.5 h-3.5 rounded-full bg-[#14b8a6] flex-shrink-0 shadow-[0_0_8px_#14b8a6]"></span>
              <span className="text-xs sm:text-sm font-bold text-slate-300 uppercase tracking-wider font-mono">
                CURRENT ISL SIGN:
              </span>
              <span className="text-sm sm:text-base font-black text-cyan-300 font-mono tracking-wide">
                {activeSignKey}
              </span>
            </div>
            <div className="text-xs sm:text-sm font-mono flex items-center space-x-2 flex-wrap">
              <span className="text-indigo-400 font-bold">Handshape:</span>
              <span className="text-slate-100">{activeSignMeta.handshape}</span>
            </div>
          </div>
        </div>

        {/* Side Timeline & Sign Queue */}
        <div className="lg:col-span-4 flex flex-col justify-between space-y-4">
          {/* Active ISL Gloss Sequence Queue */}
          <div className="bg-slate-950/80 rounded-xl p-3.5 border border-slate-800 space-y-2.5 flex-1">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Avatar Sign Queue:
              </span>
              <span className="text-[11px] font-mono text-cyan-400">
                {activeSignIndex + 1} / {glossSequence.length}
              </span>
            </div>

            <div className="space-y-1.5 max-h-[160px] overflow-y-auto pr-1">
              {glossSequence.map((item, idx) => {
                const isActive = idx === activeSignIndex;
                return (
                  <div
                    key={idx}
                    onClick={() => {
                      setActiveSignIndex(idx);
                      setIsPlaying(true);
                    }}
                    className={`flex items-center justify-between p-2 rounded-lg border text-xs font-mono cursor-pointer transition ${
                      isActive
                        ? 'bg-cyan-950/70 border-cyan-500/60 text-cyan-200 shadow-md font-bold'
                        : 'bg-slate-900/60 border-slate-800/80 text-slate-400 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center space-x-2">
                      <span className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px] ${
                        isActive ? 'bg-cyan-500 text-slate-950 font-bold' : 'bg-slate-800 text-slate-400'
                      }`}>
                        {idx + 1}
                      </span>
                      <span>{item.gloss}</span>
                    </div>
                    <span className="text-[10px] text-slate-500">{(item.duration_ms / 1000).toFixed(1)}s</span>
                  </div>
                );
              })}
            </div>

            {/* Linguistic Details Box */}
            <div className="bg-slate-900/70 p-2.5 rounded-lg border border-slate-800/80 text-[11px] space-y-1 text-slate-300">
              <div className="font-semibold text-indigo-300 flex items-center space-x-1.5">
                <BookOpen className="w-3.5 h-3.5" />
                <span>ISL Motion Description:</span>
              </div>
              <p className="text-[11px] text-slate-400 leading-snug">
                {activeSignMeta.description}
              </p>
            </div>
          </div>

          {/* Quick Individual Sign Dictionary Tester */}
          <div className="space-y-1.5">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              Test Individual ISL Signs:
            </span>
            <div className="flex flex-wrap gap-1.5">
              {['SIT', 'WAIT', '10', 'MINUTES', 'DOCTOR', 'CHEST', 'PAIN', 'POLICE', 'HOSPITAL', 'WHERE', 'HELP', 'THANK_YOU', 'HELLO', 'YES', 'NO', 'TIME'].map((s) => (
                <button
                  key={s}
                  onClick={() => handleSingleSignSelect(s)}
                  className={`px-2 py-1 rounded text-[10px] font-mono font-semibold transition ${
                    activeSignKey === s
                      ? 'bg-cyan-600 text-white shadow'
                      : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-cyan-300 hover:border-cyan-500/40'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Hearing User Voice & Text Input Toolbar */}
      <div className="bg-slate-950/90 p-3 rounded-xl border border-slate-800 flex items-center space-x-2">
        <button
          onClick={toggleSpeechRecognition}
          className={`p-3 rounded-xl transition flex items-center justify-center ${
            isListening
              ? 'bg-red-600 text-white animate-pulse shadow-lg'
              : 'bg-indigo-600/30 border border-indigo-500/50 text-indigo-300 hover:bg-indigo-600 hover:text-white'
          }`}
          title={isListening ? "Listening... Click to Stop" : "Click to Speak via Microphone"}
        >
          {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
        </button>

        <input
          type="text"
          value={spokenInput}
          onChange={(e) => setSpokenInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleTranslateAndSign(spokenInput)}
          placeholder="Speak or type hearing sentences in English / Hindi / Tamil..."
          className="flex-1 bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition font-medium"
        />

        <button
          onClick={() => handleTranslateAndSign(spokenInput)}
          className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 to-indigo-600 text-white text-sm font-semibold hover:from-cyan-500 hover:to-indigo-500 transition shadow-lg"
        >
          <span>Sign ISL</span>
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

// --- Procedural 3D Articulated Humanoid Avatar Constructor ---

function buildFullArticulatedAvatar(group) {
  const skinMat = new THREE.MeshStandardMaterial({
    color: 0xf5caa6,
    roughness: 0.5,
    metalness: 0.05
  });

  const clothesMat = new THREE.MeshStandardMaterial({
    color: 0x1e1b4b, // Indigo Dark Blue Shirt
    roughness: 0.65,
    metalness: 0.15
  });

  const hairMat = new THREE.MeshStandardMaterial({
    color: 0x0f172a,
    roughness: 0.9
  });

  const eyeMat = new THREE.MeshBasicMaterial({ color: 0x090d16 });
  const browMat = new THREE.MeshBasicMaterial({ color: 0x1e293b });

  // Torso / Chest
  const chestGeo = new THREE.CylinderGeometry(0.24, 0.19, 0.46, 16);
  const chest = new THREE.Mesh(chestGeo, clothesMat);
  chest.position.y = 1.15;
  chest.castShadow = true;
  chest.receiveShadow = true;
  group.add(chest);

  // Neck
  const neckGeo = new THREE.CylinderGeometry(0.065, 0.075, 0.12, 16);
  const neck = new THREE.Mesh(neckGeo, skinMat);
  neck.position.y = 0.28;
  chest.add(neck);

  // Head
  const headGeo = new THREE.SphereGeometry(0.14, 24, 24);
  const head = new THREE.Mesh(headGeo, skinMat);
  head.position.y = 0.14;
  neck.add(head);

  // Hair
  const hairGeo = new THREE.SphereGeometry(0.146, 16, 16, 0, Math.PI * 2, 0, Math.PI * 0.52);
  const hair = new THREE.Mesh(hairGeo, hairMat);
  hair.position.y = 0.02;
  head.add(hair);

  // Eyebrows (Articulated for Non-Manual Markers)
  const leftEyebrow = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.01, 0.015), browMat);
  leftEyebrow.position.set(-0.045, 0.06, 0.135);
  head.add(leftEyebrow);

  const rightEyebrow = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.01, 0.015), browMat);
  rightEyebrow.position.set(0.045, 0.06, 0.135);
  head.add(rightEyebrow);

  // Eyes
  const leftEye = new THREE.Mesh(new THREE.SphereGeometry(0.018, 12, 12), eyeMat);
  leftEye.position.set(-0.045, 0.02, 0.13);
  head.add(leftEye);

  const rightEye = new THREE.Mesh(new THREE.SphereGeometry(0.018, 12, 12), eyeMat);
  rightEye.position.set(0.045, 0.02, 0.13);
  head.add(rightEye);

  // --- Left Arm & 5 Articulated Fingers ---
  const leftShoulder = new THREE.Group();
  leftShoulder.position.set(-0.28, 0.16, 0);
  chest.add(leftShoulder);

  const leftUpperArm = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.045, 0.28, 16), clothesMat);
  leftUpperArm.position.y = -0.14;
  leftShoulder.add(leftUpperArm);

  const leftElbow = new THREE.Group();
  leftElbow.position.y = -0.15;
  leftUpperArm.add(leftElbow);

  const leftForearm = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.038, 0.26, 16), skinMat);
  leftForearm.position.y = -0.13;
  leftElbow.add(leftForearm);

  const leftWrist = new THREE.Group();
  leftWrist.position.y = -0.14;
  leftForearm.add(leftWrist);

  const leftPalm = new THREE.Mesh(new THREE.BoxGeometry(0.065, 0.07, 0.022), skinMat);
  leftPalm.position.y = -0.035;
  leftWrist.add(leftPalm);

  // Build Left Hand 5 Fingers
  const leftFingers = buildArticulatedFingers(leftWrist, skinMat, false);

  // --- Right Arm & 5 Articulated Fingers ---
  const rightShoulder = new THREE.Group();
  rightShoulder.position.set(0.28, 0.16, 0);
  chest.add(rightShoulder);

  const rightUpperArm = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.045, 0.28, 16), clothesMat);
  rightUpperArm.position.y = -0.14;
  rightShoulder.add(rightUpperArm);

  const rightElbow = new THREE.Group();
  rightElbow.position.y = -0.15;
  rightUpperArm.add(rightElbow);

  const rightForearm = new THREE.Mesh(new THREE.CylinderGeometry(0.042, 0.038, 0.26, 16), skinMat);
  rightForearm.position.y = -0.13;
  rightElbow.add(rightForearm);

  const rightWrist = new THREE.Group();
  rightWrist.position.y = -0.14;
  rightForearm.add(rightWrist);

  const rightPalm = new THREE.Mesh(new THREE.BoxGeometry(0.065, 0.07, 0.022), skinMat);
  rightPalm.position.y = -0.035;
  rightWrist.add(rightPalm);

  // Build Right Hand 5 Fingers
  const rightFingers = buildArticulatedFingers(rightWrist, skinMat, true);

  return {
    chest,
    neck,
    head,
    leftEyebrow,
    rightEyebrow,
    leftShoulder,
    leftElbow,
    leftWrist,
    leftFingers,
    rightShoulder,
    rightElbow,
    rightWrist,
    rightFingers
  };
}

// Builds individual articulated joints for Thumb, Index, Middle, Ring, Pinky
function buildArticulatedFingers(wristGroup, skinMat, isRight) {
  const fingers = {};
  const fingerNames = ['thumb', 'index', 'middle', 'ring', 'pinky'];
  const xOffsets = isRight
    ? [-0.035, -0.02, -0.005, 0.012, 0.028]
    : [0.035, 0.02, 0.005, -0.012, -0.028];

  fingerNames.forEach((name, i) => {
    const fingerRoot = new THREE.Group();
    const isThumb = name === 'thumb';
    const rootY = isThumb ? -0.03 : -0.07;
    fingerRoot.position.set(xOffsets[i], rootY, isThumb ? 0.01 : 0);
    wristGroup.add(fingerRoot);

    // Phalanx 1
    const p1Len = isThumb ? 0.035 : (name === 'middle' ? 0.045 : (name === 'pinky' ? 0.032 : 0.04));
    const p1 = new THREE.Mesh(new THREE.BoxGeometry(0.012, p1Len, 0.012), skinMat);
    p1.position.y = -p1Len / 2;
    fingerRoot.add(p1);

    // Phalanx 2 (Joint tip)
    const p2Root = new THREE.Group();
    p2Root.position.y = -p1Len;
    fingerRoot.add(p2Root);

    const p2Len = p1Len * 0.8;
    const p2 = new THREE.Mesh(new THREE.BoxGeometry(0.011, p2Len, 0.011), skinMat);
    p2.position.y = -p2Len / 2;
    p2Root.add(p2);

    fingers[name] = {
      root: fingerRoot,
      tipJoint: p2Root
    };
  });

  return fingers;
}

// Helper to set individual finger curl (0 = straight open, 1.5 = fully curled fist)
function setFingerCurl(finger, curlAmount, splayAngle = 0) {
  if (!finger) return;
  finger.root.rotation.x = curlAmount;
  finger.root.rotation.z = splayAngle;
  finger.tipJoint.rotation.x = curlAmount * 0.8;
}

function setHandHandshape(fingers, shape) {
  if (!fingers) return;

  if (shape === 'OPEN_FLAT') {
    // All 5 fingers extended flat
    setFingerCurl(fingers.thumb, 0.1, -0.2);
    setFingerCurl(fingers.index, 0.05, -0.05);
    setFingerCurl(fingers.middle, 0.05, 0);
    setFingerCurl(fingers.ring, 0.05, 0.05);
    setFingerCurl(fingers.pinky, 0.05, 0.1);
  } else if (shape === 'FIST') {
    // Tight closed fist
    setFingerCurl(fingers.thumb, 1.2, 0.3);
    setFingerCurl(fingers.index, 1.6, 0);
    setFingerCurl(fingers.middle, 1.6, 0);
    setFingerCurl(fingers.ring, 1.6, 0);
    setFingerCurl(fingers.pinky, 1.6, 0);
  } else if (shape === 'THUMB_UP_10') {
    // Thumb extended straight up, rest in tight fist
    setFingerCurl(fingers.thumb, -0.3, -0.4);
    setFingerCurl(fingers.index, 1.6, 0);
    setFingerCurl(fingers.middle, 1.6, 0);
    setFingerCurl(fingers.ring, 1.6, 0);
    setFingerCurl(fingers.pinky, 1.6, 0);
  } else if (shape === 'INDEX_POINT') {
    // Index extended, others closed in fist
    setFingerCurl(fingers.thumb, 1.2, 0.2);
    setFingerCurl(fingers.index, 0.0, 0);
    setFingerCurl(fingers.middle, 1.6, 0);
    setFingerCurl(fingers.ring, 1.6, 0);
    setFingerCurl(fingers.pinky, 1.6, 0);
  } else if (shape === 'V_HOOK') {
    // Index & Middle extended & hooked (SIT sign)
    setFingerCurl(fingers.thumb, 1.2, 0.2);
    setFingerCurl(fingers.index, 0.8, -0.15);
    setFingerCurl(fingers.middle, 0.8, 0.15);
    setFingerCurl(fingers.ring, 1.6, 0);
    setFingerCurl(fingers.pinky, 1.6, 0);
  } else if (shape === 'H_FLAT') {
    // Index & Middle straight horizontal
    setFingerCurl(fingers.thumb, 1.2, 0.2);
    setFingerCurl(fingers.index, 0.05, -0.05);
    setFingerCurl(fingers.middle, 0.05, 0.05);
    setFingerCurl(fingers.ring, 1.6, 0);
    setFingerCurl(fingers.pinky, 1.6, 0);
  } else if (shape === 'W_SHAPE') {
    // Index, Middle, Ring extended, Thumb holds Pinky
    setFingerCurl(fingers.thumb, 1.2, 0.3);
    setFingerCurl(fingers.index, 0.05, -0.1);
    setFingerCurl(fingers.middle, 0.05, 0);
    setFingerCurl(fingers.ring, 0.05, 0.1);
    setFingerCurl(fingers.pinky, 1.6, 0);
  } else if (shape === 'FLUTTER') {
    // Open hand with fluttering fingers
    setFingerCurl(fingers.thumb, 0.1, -0.2);
    setFingerCurl(fingers.index, 0.2, 0);
    setFingerCurl(fingers.middle, 0.3, 0);
    setFingerCurl(fingers.ring, 0.2, 0);
    setFingerCurl(fingers.pinky, 0.1, 0);
  }
}

// --- Precise Indian Sign Language (ISL) Kinematic Controller ---

function applyAccurateISLSign(rig, signName, progress, time) {
  const ease = Math.sin(progress * Math.PI); // Smooth Bell Curve 0 -> 1 -> 0

  // 1. Reset / Neutral Baseline
  rig.head.rotation.set(0, 0, 0);
  rig.leftEyebrow.position.y = 0.06;
  rig.rightEyebrow.position.y = 0.06;

  rig.leftShoulder.rotation.set(0.1, 0, -0.2);
  rig.leftElbow.rotation.set(-0.2, 0, 0);
  rig.leftWrist.rotation.set(0, 0, 0);
  setHandHandshape(rig.leftFingers, 'OPEN_FLAT');

  rig.rightShoulder.rotation.set(0.1, 0, 0.2);
  rig.rightElbow.rotation.set(-0.2, 0, 0);
  rig.rightWrist.rotation.set(0, 0, 0);
  setHandHandshape(rig.rightFingers, 'OPEN_FLAT');

  // 2. Canonical Sign Postures & Trajectories
  if (signName === "SIT") {
    // Left hand creates flat seat: forearm raised in front, wrist rotated so fingers point right/forward
    rig.leftShoulder.rotation.set(-0.6 * ease, 0.2 * ease, -0.3 * ease);
    rig.leftElbow.rotation.set(-1.4 * ease, 0, 0);
    rig.leftWrist.rotation.set(0, 0.5 * ease, 1.2 * ease);
    setHandHandshape(rig.leftFingers, 'H_FLAT');

    // Right hand forms 'V' hooked legs and descends onto left fingers
    const sitDescend = -0.5 * ease - progress * 0.3 * ease;
    rig.rightShoulder.rotation.set(sitDescend, -0.2 * ease, 0.2 * ease);
    rig.rightElbow.rotation.set(-1.6 * ease, 0, 0);
    rig.rightWrist.rotation.set(0.2 * ease, -0.4 * ease, -0.8 * ease);
    setHandHandshape(rig.rightFingers, 'V_HOOK');
  } else if (signName === "WAIT") {
    // Both hands raised in front of chest at 45°, palms facing body, all fingers fluttering
    const wave1 = Math.sin(time * 14) * 0.25 * ease;
    const wave2 = Math.cos(time * 14) * 0.25 * ease;

    rig.leftShoulder.rotation.set(-0.65 * ease, 0.15 * ease, -0.3 * ease);
    rig.leftElbow.rotation.set(-1.3 * ease + wave1 * 0.2, 0, 0);
    rig.leftWrist.rotation.set(0.6 * ease + wave1, 0.4 * ease, 0);
    setFingerCurl(rig.leftFingers.thumb, 0.1 + wave1 * 0.3);
    setFingerCurl(rig.leftFingers.index, 0.2 + wave2 * 0.4);
    setFingerCurl(rig.leftFingers.middle, 0.3 + wave1 * 0.4);
    setFingerCurl(rig.leftFingers.ring, 0.2 + wave2 * 0.4);
    setFingerCurl(rig.leftFingers.pinky, 0.1 + wave1 * 0.3);

    rig.rightShoulder.rotation.set(-0.65 * ease, -0.15 * ease, 0.3 * ease);
    rig.rightElbow.rotation.set(-1.3 * ease + wave2 * 0.2, 0, 0);
    rig.rightWrist.rotation.set(0.6 * ease + wave2, -0.4 * ease, 0);
    setFingerCurl(rig.rightFingers.thumb, 0.1 + wave2 * 0.3);
    setFingerCurl(rig.rightFingers.index, 0.2 + wave1 * 0.4);
    setFingerCurl(rig.rightFingers.middle, 0.3 + wave2 * 0.4);
    setFingerCurl(rig.rightFingers.ring, 0.2 + wave1 * 0.4);
    setFingerCurl(rig.rightFingers.pinky, 0.1 + wave2 * 0.3);
  } else if (signName === "10") {
    // Dominant right fist with thumb straight up shaking side-to-side (ISL 10)
    const shake10 = Math.sin(time * 16) * 0.25 * ease;
    rig.rightShoulder.rotation.set(-0.85 * ease, -0.2 * ease, 0.45 * ease);
    rig.rightElbow.rotation.set(-1.5 * ease, 0, 0);
    rig.rightWrist.rotation.set(0, shake10, 0.2 * ease);
    setHandHandshape(rig.rightFingers, 'THUMB_UP_10');
  } else if (signName === "MINUTES") {
    // Left palm flat facing up; Right index finger circles clockwise like a clock hand
    rig.leftShoulder.rotation.set(-0.55 * ease, 0.3 * ease, -0.4 * ease);
    rig.leftElbow.rotation.set(-1.4 * ease, 0, 0);
    rig.leftWrist.rotation.set(0, 0, 1.4 * ease); // Palm facing up
    setHandHandshape(rig.leftFingers, 'OPEN_FLAT');

    const clockAngle = time * 8;
    const circX = Math.cos(clockAngle) * 0.15 * ease;
    const circY = Math.sin(clockAngle) * 0.15 * ease;

    rig.rightShoulder.rotation.set(-0.6 * ease + circY, -0.25 * ease + circX, 0.35 * ease);
    rig.rightElbow.rotation.set(-1.5 * ease, 0, 0);
    rig.rightWrist.rotation.set(0.6 * ease, -0.3 * ease, -0.5 * ease);
    setHandHandshape(rig.rightFingers, 'INDEX_POINT');
  } else if (signName === "DOCTOR") {
    // Left forearm horizontal across chest; Right two fingers tap left wrist pulse twice
    rig.leftShoulder.rotation.set(-0.5 * ease, 0.4 * ease, -0.6 * ease);
    rig.leftElbow.rotation.set(-1.5 * ease, 0, 0);
    rig.leftWrist.rotation.set(0, 0, 1.3 * ease); // Palm facing inward/upward
    setHandHandshape(rig.leftFingers, 'OPEN_FLAT');

    const pulseTap = Math.sin(time * 10) * 0.2 * ease;
    rig.rightShoulder.rotation.set(-0.65 * ease + pulseTap * 0.3, -0.45 * ease, 0.5 * ease);
    rig.rightElbow.rotation.set(-1.55 * ease + pulseTap, 0, 0);
    rig.rightWrist.rotation.set(0.3 * ease, -0.4 * ease, -0.6 * ease);
    setHandHandshape(rig.rightFingers, 'H_FLAT');
  } else if (signName === "CHEST") {
    // Both flat hands press against upper chest
    rig.leftShoulder.rotation.set(-0.65 * ease, 0.35 * ease, -0.4 * ease);
    rig.leftElbow.rotation.set(-1.7 * ease, 0, 0);
    rig.leftWrist.rotation.set(0.4 * ease, 0.2 * ease, 0);
    setHandHandshape(rig.leftFingers, 'OPEN_FLAT');

    rig.rightShoulder.rotation.set(-0.65 * ease, -0.35 * ease, 0.4 * ease);
    rig.rightElbow.rotation.set(-1.7 * ease, 0, 0);
    rig.rightWrist.rotation.set(0.4 * ease, -0.2 * ease, 0);
    setHandHandshape(rig.rightFingers, 'OPEN_FLAT');
  } else if (signName === "PAIN") {
    // Both index pointers twist toward each other at center torso with urgency
    const twist = Math.sin(time * 14) * 0.35 * ease;
    rig.head.rotation.x = 0.1 * ease;
    rig.leftEyebrow.position.y = 0.05; // Furrowed brows
    rig.rightEyebrow.position.y = 0.05;

    rig.leftShoulder.rotation.set(-0.65 * ease, 0.25 * ease, -0.35 * ease);
    rig.leftElbow.rotation.set(-1.45 * ease + twist, 0, 0);
    rig.leftWrist.rotation.set(0.5 * ease, twist * 0.5, 0.5 * ease);
    setHandHandshape(rig.leftFingers, 'INDEX_POINT');

    rig.rightShoulder.rotation.set(-0.65 * ease, -0.25 * ease, 0.35 * ease);
    rig.rightElbow.rotation.set(-1.45 * ease - twist, 0, 0);
    rig.rightWrist.rotation.set(0.5 * ease, -twist * 0.5, -0.5 * ease);
    setHandHandshape(rig.rightFingers, 'INDEX_POINT');
  } else if (signName === "SEVERE") {
    // Both hands start high and sweep down forcefully
    const sweep = progress * 1.1;
    rig.leftShoulder.rotation.set((-0.2 - sweep * 0.6) * ease, 0.15 * ease, -0.35 * ease);
    rig.leftElbow.rotation.set(-0.8 * ease, 0, 0);
    setHandHandshape(rig.leftFingers, 'OPEN_FLAT');

    rig.rightShoulder.rotation.set((-0.2 - sweep * 0.6) * ease, -0.15 * ease, 0.35 * ease);
    rig.rightElbow.rotation.set(-0.8 * ease, 0, 0);
    setHandHandshape(rig.rightFingers, 'OPEN_FLAT');
  } else if (signName === "POLICE") {
    // Right hand touches right temple/forehead (salute/badge)
    rig.rightShoulder.rotation.set(-1.35 * ease, -0.35 * ease, 0.8 * ease);
    rig.rightElbow.rotation.set(-2.0 * ease, 0, 0);
    rig.rightWrist.rotation.set(-0.2 * ease, 0, -0.3 * ease);
    setHandHandshape(rig.rightFingers, 'OPEN_FLAT');
  } else if (signName === "STATION") {
    // Both hands form vertical right-angle boundary box
    rig.leftShoulder.rotation.set(-0.8 * ease, 0.45 * ease, -0.3 * ease);
    rig.leftElbow.rotation.set(-1.2 * ease, 0, 0);
    rig.leftWrist.rotation.set(0, 0.6 * ease, 0);
    setHandHandshape(rig.leftFingers, 'OPEN_FLAT');

    rig.rightShoulder.rotation.set(-0.8 * ease, -0.45 * ease, 0.3 * ease);
    rig.rightElbow.rotation.set(-1.2 * ease, 0, 0);
    rig.rightWrist.rotation.set(0, -0.6 * ease, 0);
    setHandHandshape(rig.rightFingers, 'OPEN_FLAT');
  } else if (signName === "WHERE") {
    // Questioning shrug: palms up sweeping outward, head tilt, raised eyebrows
    const shrug = Math.sin(time * 6) * 0.15 * ease;
    rig.head.rotation.z = 0.08 * ease; // Head tilt
    rig.leftEyebrow.position.y = 0.075 * ease + 0.06; // Raised brows (Question NMM)
    rig.rightEyebrow.position.y = 0.075 * ease + 0.06;

    rig.leftShoulder.rotation.set(-0.45 * ease, 0.55 * ease, (-0.6 - shrug) * ease);
    rig.leftElbow.rotation.set(-1.1 * ease, 0, 0);
    rig.leftWrist.rotation.set(0, 0, 1.4 * ease); // Palms face up
    setHandHandshape(rig.leftFingers, 'OPEN_FLAT');

    rig.rightShoulder.rotation.set(-0.45 * ease, -0.55 * ease, (0.6 + shrug) * ease);
    rig.rightElbow.rotation.set(-1.1 * ease, 0, 0);
    rig.rightWrist.rotation.set(0, 0, -1.4 * ease); // Palms face up
    setHandHandshape(rig.rightFingers, 'OPEN_FLAT');
  } else if (signName === "HOSPITAL") {
    // Universal ISL Medical Cross (+): 
    // Left index finger held straight VERTICAL (|) in front of center chest.
    // Right index finger held HORIZONTAL (-) intersecting at 90° across the left index finger to form a distinct '+'.
    const crossTap = Math.sin(time * 10) * 0.08 * ease;

    // Left hand: Vertical bar (|) of the Cross
    rig.leftShoulder.rotation.set(-0.6 * ease, 0.18 * ease, -0.22 * ease);
    rig.leftElbow.rotation.set(-1.5 * ease, 0, 0);
    rig.leftWrist.rotation.set(0.3 * ease, 0, 0); // Index points straight UP
    setHandHandshape(rig.leftFingers, 'INDEX_POINT');

    // Right hand: Horizontal bar (-) of the Cross crossing over Left finger
    rig.rightShoulder.rotation.set(-0.6 * ease, -0.22 * ease, 0.22 * ease);
    rig.rightElbow.rotation.set(-1.5 * ease + crossTap, 0, 0);
    rig.rightWrist.rotation.set(0, 0, -1.57 * ease); // Rotated 90° so index points HORIZONTALLY left
    setHandHandshape(rig.rightFingers, 'INDEX_POINT');
  } else if (signName === "GO") {
    // Right index points forward and sweeps outward
    const goProg = progress * 0.6;
    rig.rightShoulder.rotation.set((-0.6 - goProg) * ease, (-0.1 + goProg) * ease, 0.3 * ease);
    rig.rightElbow.rotation.set((-1.2 + goProg) * ease, 0, 0);
    setHandHandshape(rig.rightFingers, 'INDEX_POINT');
  } else if (signName === "HOW") {
    // Curved hands roll upward until palms face up
    const roll = progress * 1.5;
    rig.leftEyebrow.position.y = 0.075 * ease + 0.06;
    rig.rightEyebrow.position.y = 0.075 * ease + 0.06;

    rig.leftShoulder.rotation.set(-0.6 * ease, 0.3 * ease, -0.3 * ease);
    rig.leftElbow.rotation.set(-1.4 * ease, 0, 0);
    rig.leftWrist.rotation.set(0, roll * ease, 1.2 * ease);
    setHandHandshape(rig.leftFingers, 'OPEN_FLAT');

    rig.rightShoulder.rotation.set(-0.6 * ease, -0.3 * ease, 0.3 * ease);
    rig.rightElbow.rotation.set(-1.4 * ease, 0, 0);
    rig.rightWrist.rotation.set(0, -roll * ease, -1.2 * ease);
    setHandHandshape(rig.rightFingers, 'OPEN_FLAT');
  } else if (signName === "HELP") {
    // Left palm flat up; Right 'A' fist with thumb up lifts off left palm
    const lift = progress * 0.4;
    rig.leftShoulder.rotation.set((-0.6 - lift) * ease, 0.25 * ease, -0.3 * ease);
    rig.leftElbow.rotation.set(-1.4 * ease, 0, 0);
    rig.leftWrist.rotation.set(0, 0, 1.4 * ease);
    setHandHandshape(rig.leftFingers, 'OPEN_FLAT');

    rig.rightShoulder.rotation.set((-0.65 - lift) * ease, -0.25 * ease, 0.3 * ease);
    rig.rightElbow.rotation.set(-1.45 * ease, 0, 0);
    rig.rightWrist.rotation.set(0, 0, 0);
    setHandHandshape(rig.rightFingers, 'THUMB_UP_10');
  } else if (signName === "ME") {
    // Right index points to center of chest
    rig.rightShoulder.rotation.set(-0.65 * ease, -0.35 * ease, 0.35 * ease);
    rig.rightElbow.rotation.set(-1.65 * ease, 0, 0);
    rig.rightWrist.rotation.set(0.6 * ease, -0.2 * ease, -0.4 * ease);
    setHandHandshape(rig.rightFingers, 'INDEX_POINT');
  } else if (signName === "PLEASE") {
    // Right open flat palm rubs clockwise circle on chest
    const rubAngle = time * 7;
    const rx = Math.cos(rubAngle) * 0.1 * ease;
    const ry = Math.sin(rubAngle) * 0.1 * ease;

    rig.rightShoulder.rotation.set(-0.65 * ease + ry, -0.3 * ease + rx, 0.35 * ease);
    rig.rightElbow.rotation.set(-1.7 * ease, 0, 0);
    rig.rightWrist.rotation.set(0.5 * ease, 0, 0);
    setHandHandshape(rig.rightFingers, 'OPEN_FLAT');
  } else if (signName === "HELLO") {
    // Right open hand waves outward from right temple
    const wave = Math.sin(time * 8) * 0.25 * ease;
    rig.rightShoulder.rotation.set(-1.25 * ease, -0.3 * ease, 0.7 * ease);
    rig.rightElbow.rotation.set(-1.7 * ease, 0, 0);
    rig.rightWrist.rotation.set(0, 0, wave);
    setHandHandshape(rig.rightFingers, 'OPEN_FLAT');
  } else if (signName === "THANK_YOU") {
    // Right flat hand touches chin, then moves forward and down toward viewer with a polite head nod
    const chinToForward = progress;
    rig.head.rotation.x = 0.1 * ease; // Head nod

    rig.rightShoulder.rotation.set((-1.0 + chinToForward * 0.5) * ease, -0.15 * ease, 0.35 * ease);
    rig.rightElbow.rotation.set((-1.8 + chinToForward * 0.8) * ease, 0, 0);
    rig.rightWrist.rotation.set((-0.2 + chinToForward * 0.6) * ease, 0, 0);
    setHandHandshape(rig.rightFingers, 'OPEN_FLAT');
  } else if (signName === "YES") {
    // Right fist nods up and down at wrist
    const fistNod = Math.sin(time * 10) * 0.35 * ease;
    rig.rightShoulder.rotation.set(-0.85 * ease, -0.15 * ease, 0.4 * ease);
    rig.rightElbow.rotation.set(-1.5 * ease, 0, 0);
    rig.rightWrist.rotation.set(fistNod, 0, 0);
    setHandHandshape(rig.rightFingers, 'FIST');
  } else if (signName === "NO") {
    // Two fingers snap down onto thumb + slight head shake
    const snapProg = (time * 8) % Math.PI;
    const snapCurl = Math.sin(snapProg) > 0.5 ? 1.4 : 0.1;
    rig.head.rotation.y = Math.sin(time * 8) * 0.15 * ease; // Head shake

    rig.rightShoulder.rotation.set(-0.75 * ease, -0.2 * ease, 0.4 * ease);
    rig.rightElbow.rotation.set(-1.45 * ease, 0, 0);
    setFingerCurl(rig.rightFingers.thumb, 0.3);
    setFingerCurl(rig.rightFingers.index, snapCurl);
    setFingerCurl(rig.rightFingers.middle, snapCurl);
    setFingerCurl(rig.rightFingers.ring, 1.6);
    setFingerCurl(rig.rightFingers.pinky, 1.6);
  } else if (signName === "WATER") {
    // 'W' hand taps side of chin twice
    const wTap = Math.sin(time * 8) * 0.15 * ease;
    rig.rightShoulder.rotation.set(-1.1 * ease + wTap, -0.25 * ease, 0.45 * ease);
    rig.rightElbow.rotation.set(-1.85 * ease, 0, 0);
    setHandHandshape(rig.rightFingers, 'W_SHAPE');
  } else if (signName === "TIME") {
    // Left forearm horizontal; Right index taps left wrist watch
    rig.leftShoulder.rotation.set(-0.5 * ease, 0.35 * ease, -0.5 * ease);
    rig.leftElbow.rotation.set(-1.4 * ease, 0, 0);
    rig.leftWrist.rotation.set(0, 0, 0); // Palm down (watch face visible)
    setHandHandshape(rig.leftFingers, 'OPEN_FLAT');

    const watchTap = Math.sin(time * 10) * 0.2 * ease;
    rig.rightShoulder.rotation.set(-0.65 * ease + watchTap * 0.3, -0.35 * ease, 0.4 * ease);
    rig.rightElbow.rotation.set(-1.5 * ease + watchTap, 0, 0);
    setHandHandshape(rig.rightFingers, 'INDEX_POINT');
  } else {
    // Generic polite gesture
    rig.rightShoulder.rotation.set(-0.9 * ease, -0.2 * ease, 0.5 * ease);
    rig.rightElbow.rotation.set(-1.4 * ease, 0, 0);
    setHandHandshape(rig.rightFingers, 'OPEN_FLAT');
  }
}
