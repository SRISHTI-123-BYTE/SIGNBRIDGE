import React, { useRef, useEffect, useState, useCallback } from 'react';
import {
  Camera,
  Video,
  Sparkles,
  RefreshCw,
  Eye,
  EyeOff,
  Layers,
  Activity,
  Sun,
  Sliders,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  CircleDot,
  Zap,
  Check,
  RotateCcw,
  Hand
} from 'lucide-react';
import { signBridgeService } from '../services/api';

/**
 * Lifecycle State Machine for ISL Tracking, Recording & Model Inference
 */
export const RECORDING_STATES = {
  IDLE: 'IDLE',
  COUNTDOWN: 'COUNTDOWN',
  RECORDING: 'RECORDING',
  VALIDATING: 'VALIDATING',
  SAMPLE_ACCEPTED: 'SAMPLE_ACCEPTED',
  SAMPLE_REJECTED: 'SAMPLE_REJECTED',
  INFERENCE: 'INFERENCE',
  PREDICTED_ACTION: 'PREDICTED_ACTION'
};

export const TRACKING_STATES = {
  NO_SIGN: 'NO_SIGN',
  TRACKING: 'TRACKING',
  COLLECTING_SEQUENCE: 'COLLECTING_SEQUENCE',
  INFERENCE_PENDING: 'INFERENCE_PENDING',
  SIGN_CONFIRMED: 'SIGN_CONFIRMED',
  LOW_CONFIDENCE: 'LOW_CONFIDENCE',
  TRACKING_LOST: 'TRACKING_LOST'
};

// Sign guidance dictionary with descriptions, icons, and static/dynamic flag
export const SIGN_INSTRUCTIONS = {
  YES: { label: "👍 Yes", tip: "Form a fist and nod it vertically up and down twice.", isStatic: false },
  HELP: { label: "🆘 Help", tip: "Place right thumbs-up fist onto flat left palm and lift upward.", isStatic: false },
  DOCTOR: { label: "🩺 Doctor", tip: "Tap right index & middle fingers onto your left wrist pulse point.", isStatic: false },
  CHEST: { label: "💔 Chest", tip: "Press open flat palms gently against your chest.", isStatic: true },
  PAIN: { label: "⚡ Pain", tip: "Point index fingers toward each other at center torso and twist.", isStatic: false },
  HOSPITAL: { label: "🏥 Hospital", tip: "Form intersecting cross (+) with both index fingers.", isStatic: false },
  POLICE: { label: "👮 Police", tip: "Touch right hand near your right temple/badge salute.", isStatic: false },
  HELLO: { label: "👋 Hello", tip: "Wave open palm outward from temple with a friendly nod.", isStatic: false },
  WATER: { label: "💧 Water", tip: "Tap 'W' three fingers at the corner of your chin.", isStatic: false },
  NO: { label: "🙅 No", tip: "Snap index and middle fingers closed onto thumb with a head shake.", isStatic: false },
  "10": { label: "🔢 10", tip: "Hold fist with thumb straight up and shake side-to-side.", isStatic: false },
  CARD: { label: "💳 Card", tip: "Swipe right pinch hand across open left palm horizontally.", isStatic: false },
  COME: { label: "🫳 Come", tip: "Beckon inward towards chest with both open hands.", isStatic: false },
  STOP: { label: "🛑 Stop", tip: "Push right open hand forward in firm vertical halt gesture.", isStatic: false },
  LEARN: { label: "📖 Learn", tip: "Touch left open palm with right fingers, then rise to touch right temple.", isStatic: false },
  TEACHER: { label: "👨‍🏫 Teacher", tip: "Both hands near temples move forward in instructive motion.", isStatic: false },
  STUDENT: { label: "🧑‍🎓 Student", tip: "Perform learn motion followed by downward personal descent along sides.", isStatic: false },
  SCHOOL: { label: "🏫 School", tip: "Clap flat right palm horizontally atop flat left palm twice.", isStatic: false },
  FOOD: { label: "🍲 Food", tip: "Bring clustered right fingertips to mouth and lips repeatedly.", isStatic: false },
  SLEEP: { label: "😴 Sleep", tip: "Rest tilted cheek gently on right palm with soft head tilt.", isStatic: false }
};

export const ALL_51_ISL_SIGNS = [
  "DOCTOR", "CHEST", "PAIN", "SEVERE", "POLICE", "STATION", "WHERE", "HOSPITAL",
  "GO", "HOW", "SIT", "WAIT", "10", "MINUTES", "HELP", "ME", "PLEASE", "MEDICINE",
  "TIME", "WHAT", "NAME", "YOUR", "YES", "NO", "THANK_YOU", "HELLO", "WATER",
  "NEED", "EMERGENCY", "FEVER", "BREATHING", "PROBLEM", "CALL", "FAMILY", "MONEY",
  "ACCOUNT", "BANK", "DEPOSIT", "WITHDRAW", "SIGN", "LANGUAGE", "INTERPRETER",
  "CARD", "COME", "STOP", "LEARN", "TEACHER", "STUDENT", "SCHOOL", "FOOD", "SLEEP"
];

export const ALL_42_ISL_SIGNS = ALL_51_ISL_SIGNS;

/**
 * Pure helper to extract clean (25 pose, 21 LH, 21 RH, 40 face = 107 pts) skeleton
 */
function extractSkeletalLandmarks(results) {
  if (!results || !results.poseLandmarks) return null;

  // 1. Pose Landmarks: Take 25 upper body joints (0..24)
  const pose = results.poseLandmarks.slice(0, 25).map(p => ({
    x: p.x,
    y: p.y,
    z: p.z || 0,
    visibility: p.visibility !== undefined ? p.visibility : 1.0
  }));
  while (pose.length < 25) pose.push({ x: 0, y: 0, z: 0, visibility: 0 });

  const lwPose = pose[15] || { x: 0.35, y: 0.65, z: 0 };
  const rwPose = pose[16] || { x: 0.65, y: 0.65, z: 0 };

  // 2. Left Hand Landmarks: 21 joints
  let leftHand = [];
  const hasLeftHand = Boolean(results.leftHandLandmarks && results.leftHandLandmarks.length >= 21);
  if (hasLeftHand) {
    leftHand = results.leftHandLandmarks.slice(0, 21).map(h => ({ x: h.x, y: h.y, z: h.z || 0 }));
  } else {
    // Anchor to left wrist if hand ROI is missing
    for (let i = 0; i < 21; i++) {
      leftHand.push({ x: lwPose.x, y: lwPose.y, z: lwPose.z || 0 });
    }
  }

  // 3. Right Hand Landmarks: 21 joints
  let rightHand = [];
  const hasRightHand = Boolean(results.rightHandLandmarks && results.rightHandLandmarks.length >= 21);
  if (hasRightHand) {
    rightHand = results.rightHandLandmarks.slice(0, 21).map(h => ({ x: h.x, y: h.y, z: h.z || 0 }));
  } else {
    // Anchor to right wrist if hand ROI is missing
    for (let i = 0; i < 21; i++) {
      rightHand.push({ x: rwPose.x, y: rwPose.y, z: rwPose.z || 0 });
    }
  }

  // 4. Face Landmarks: 40 expressive contour joints
  let face = [];
  if (results.faceLandmarks && results.faceLandmarks.length >= 40) {
    face = results.faceLandmarks.slice(0, 40).map(f => ({ x: f.x, y: f.y, z: f.z || 0 }));
  } else {
    const nose = pose[0] || { x: 0.5, y: 0.25, z: 0 };
    for (let i = 0; i < 40; i++) {
      face.push({ x: nose.x, y: nose.y, z: nose.z || 0 });
    }
  }

  return {
    pose,
    leftHand,
    rightHand,
    face,
    hasLeftHand,
    hasRightHand,
    lhCount: hasLeftHand ? 21 : 0,
    rhCount: hasRightHand ? 21 : 0
  };
}

export default function VisionTracker({
  onLandmarksUpdate,
  isStreaming = true,
  setIsStreaming,
  onRecordSign,
  onEvaluationResult,
  captureMode = 'on-demand'
}) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const mediaStreamRef = useRef(null);
  const animationFrameRef = useRef(null);
  const videoFrameCallbackHandleRef = useRef(null);

  // Persistent Timing, Recording, and Tracking References
  const cameraFrameCounterRef = useRef(0);
  const renderFrameCounterRef = useRef(0);
  const prevFrameTimestampRef = useRef(performance.now());
  const lastVideoCurrentTimeRef = useRef(-1);
  const lastVideoFrameTimeRef = useRef(performance.now());
  const lastDiagnosticLogTimeRef = useRef(0);
  
  // FPS calculation references
  const lastRenderFpsUpdateTimeRef = useRef(performance.now());
  const renderFramesSinceUpdateRef = useRef(0);
  const lastInferenceFpsUpdateTimeRef = useRef(performance.now());
  const inferenceResultsSinceUpdateRef = useRef(0);
  const lastCameraFpsUpdateTimeRef = useRef(performance.now());
  const cameraFramesSinceUpdateRef = useRef(0);

  // MediaPipe Inference & Diagnostics References
  const mediaPipeResultIdRef = useRef(0);
  const mediaPipeProcessingDurationRef = useRef(0);
  const backendInferenceDurationRef = useRef(0);
  const holisticInstanceRef = useRef(null);
  const isHolisticProcessingRef = useRef(false);
  const holisticProcessingStartTimeRef = useRef(0);
  const liveResultsRef = useRef(null);
  const offscreenCanvasRef = useRef(null);
  const lastMediaPipeResultTimeRef = useRef(performance.now());

  // Motion, Landmarks, and Recording Buffer
  const prevMediaPipeLandmarksRef = useRef(null);
  const recordedSamplesRef = useRef([]);
  const isActivelyRecordingRef = useRef(false);
  const recordingStartTimeRef = useRef(0);
  const smoothedVelocityRef = useRef(0.0);
  const smoothedDisplacementRef = useRef(0.0);

  // Telemetry ref (avoids re-rendering React on every 16ms animation frame)
  const latestTelemetryRef = useRef({
    torsoCenter: { x: 0.5, y: 0.42, z: 0.0 },
    shoulderScale: 0.4,
    jointVelocityNorm: 0.0,
    jointVelocityMs: 0.0,
    handDisplacement: 0.0,
    leftHandVisible: false,
    rightHandVisible: false,
    poseVisible: true,
    motionLevel: 'IDLE'
  });

  // Component States (Throttled updates to prevent main-thread lag)
  const [inputSource, setInputSource] = useState('webcam'); // 'webcam' | 'simulator'
  const [recordingState, setRecordingState] = useState(RECORDING_STATES.IDLE);
  const [trackingState, setTrackingState] = useState(TRACKING_STATES.NO_SIGN);
  const [renderFps, setRenderFps] = useState(60);
  const [inferenceFps, setInferenceFps] = useState(0);
  const [cameraFps, setCameraFps] = useState(30);
  const [mediaPipeLatencyMs, setMediaPipeLatencyMs] = useState(0);

  // Dataset Recording Mode State
  const [recordMode, setRecordMode] = useState('RECOGNIZE'); // 'RECOGNIZE' | 'DATASET'
  const [datasetSign, setDatasetSign] = useState('DOCTOR');
  const [datasetUserId, setDatasetUserId] = useState('user_01');
  const [datasetSavedCount, setDatasetSavedCount] = useState(0);

  // HUD System Diagnostics State (8 Requested Real-time Fields)
  const [hudDiagnostics, setHudDiagnostics] = useState({
    frameId: 0,
    timestamp: '0.00s',
    lhCount: '0 (Anchored)',
    rhCount: '0 (Anchored)',
    trackingStatus: TRACKING_STATES.NO_SIGN,
    motionScore: 0.0,
    validSeqLength: 0,
    modelPrediction: 'None (0%)',
    decisionReason: 'Waiting for a valid ISL sign'
  });

  const [showPose, setShowPose] = useState(true);
  const [showHands, setShowHands] = useState(true);
  const [showFace, setShowFace] = useState(true);
  const [showMetrics, setShowMetrics] = useState(true);
  const [showHudDebug, setShowHudDebug] = useState(true);
  const [cameraError, setCameraError] = useState(null);

  // Simulator default sign for visual preview
  const simulatorSign = 'YES';

  // Active UI Recording Timers & Feedback
  const [recordingPhase, setRecordingPhase] = useState('idle'); // 'idle' | 'countdown' | 'recording'
  const [displayCountdown, setDisplayCountdown] = useState(3);
  const [actionFeedback, setActionFeedback] = useState(null); // { type: 'success' | 'warning', text: string }

  // Telemetry UI state (throttled to 2-3 updates/sec)
  const [telemetry, setTelemetry] = useState(latestTelemetryRef.current);

  // Observation sequence tracking refs
  const lastRecordedTimestampRef = useRef(0);
  const lastRecordedObsIdRef = useRef(0);

  // Helper to record a fresh MediaPipe observation into persistent buffer with temporal validation
  const recordObservationSample = useCallback((obsId, timestamp, skeleton, motionMetrics) => {
    if (!isActivelyRecordingRef.current || !skeleton) return;

    // Temporal validation: ensure strictly increasing timestamp
    if (timestamp <= lastRecordedTimestampRef.current) {
      return;
    }
    lastRecordedTimestampRef.current = timestamp;
    lastRecordedObsIdRef.current += 1;

    const curLeftWrist = skeleton.pose[15] || skeleton.leftHand[0] || { x: 0.35, y: 0.65, z: 0 };
    const curRightWrist = skeleton.pose[16] || skeleton.rightHand[0] || { x: 0.65, y: 0.65, z: 0 };
    const curLeftThumb = skeleton.leftHand[4] || { x: curLeftWrist.x - 0.02, y: curLeftWrist.y - 0.04, z: 0 };
    const curRightThumb = skeleton.rightHand[4] || { x: curRightWrist.x + 0.02, y: curRightWrist.y - 0.04, z: 0 };

    recordedSamplesRef.current.push({
      observationId: lastRecordedObsIdRef.current,
      timestamp: timestamp,
      landmarks: skeleton,
      leftWrist: { ...curLeftWrist },
      rightWrist: { ...curRightWrist },
      leftThumb: { ...curLeftThumb },
      rightThumb: { ...curRightThumb },
      handDisplacement: motionMetrics.displacement,
      handVelocity: motionMetrics.velocity,
      isHandMoving: motionMetrics.isMoving,
      leftHandVisible: skeleton.hasLeftHand,
      rightHandVisible: skeleton.hasRightHand,
      poseVisible: Boolean(skeleton.pose && skeleton.pose.length >= 17)
    });
  }, []);

  // Spacebar keyboard shortcut to trigger sign capture
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === 'Space' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {
        e.preventDefault();
        if (recordingPhase === 'idle') {
          handleStartRecordingAction();
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [recordingPhase]);

  // Start 2-Phase Recording Workflow: Countdown (3s) -> Active Capture (3s) -> Evaluation
  const handleStartRecordingAction = () => {
    if (recordingPhase !== 'idle') return;

    if (cameraError) {
      setRecordingState(RECORDING_STATES.SAMPLE_REJECTED);
      setActionFeedback({
        type: 'warning',
        text: '⚠️ Camera tracking error. Please ensure camera access is granted.'
      });
      return;
    }

    // Phase 1: Countdown (3... 2... 1...)
    setRecordingPhase('countdown');
    setRecordingState(RECORDING_STATES.COUNTDOWN);
    setDisplayCountdown(3);
    setActionFeedback(null);
    recordedSamplesRef.current = [];
    lastRecordedTimestampRef.current = 0;
    lastRecordedObsIdRef.current = 0;
    isActivelyRecordingRef.current = false;

    let count = 3;
    const countdownInterval = setInterval(() => {
      count -= 1;
      setDisplayCountdown(count);

      if (count <= 0) {
        clearInterval(countdownInterval);
        // Phase 2: Switch to Active Frame Recording (Full 3.0 Seconds Capture Window)
        startActiveFrameCapture();
      }
    }, 1000);
  };

  // Starts active frame collection into the persistent ref buffer
  const startActiveFrameCapture = () => {
    setRecordingPhase('recording');
    setRecordingState(RECORDING_STATES.RECORDING);
    setDisplayCountdown(3);
    recordedSamplesRef.current = [];
    isActivelyRecordingRef.current = true;
    recordingStartTimeRef.current = performance.now();
    lastRecordedTimestampRef.current = 0;
    lastRecordedObsIdRef.current = 0;

    let recordSeconds = 3;
    const captureInterval = setInterval(() => {
      recordSeconds -= 1;
      setDisplayCountdown(recordSeconds);

      if (recordSeconds <= 0) {
        clearInterval(captureInterval);
        isActivelyRecordingRef.current = false;
        setRecordingPhase('idle');
        evaluateRecordedSequence();
      }
    }, 1000);
  };

  // Evaluates the collected sequence across Data Quality, Hand Visibility, Movement & ST-GCN Model
  const evaluateRecordedSequence = async () => {
    setRecordingState(RECORDING_STATES.VALIDATING);
    setTrackingState(TRACKING_STATES.INFERENCE_PENDING);
    const recordingEndTime = performance.now();
    const actualDurationMs = recordingEndTime - recordingStartTimeRef.current;

    const samples = recordedSamplesRef.current || [];
    const uniqueObservationsCount = samples.length;
    const validPoseFrames = samples.filter(s => s.poseVisible).length;
    const validLeftHandFrames = samples.filter(s => s.leftHandVisible).length;
    const validRightHandFrames = samples.filter(s => s.rightHandVisible).length;

    // Detailed Diagnostics Logging
    console.log(`[SignBridge Recording Diagnostics] Capture Completed:`, {
      recordingStartTimeMs: Number(recordingStartTimeRef.current.toFixed(2)),
      recordingEndTimeMs: Number(recordingEndTime.toFixed(2)),
      actualDurationMs: Number(actualDurationMs.toFixed(2)),
      totalCameraFramesProcessed: cameraFrameCounterRef.current,
      totalMediaPipeResultsReceived: mediaPipeResultIdRef.current,
      uniqueObservationsRecorded: uniqueObservationsCount,
      validPoseFrames,
      validLeftHandFrames,
      validRightHandFrames,
      renderFPS: renderFps,
      inferenceFPS: inferenceFps,
      cameraFPS: cameraFps,
      mediaPipeLatencyMs: mediaPipeLatencyMs,
      targetSign: 'CONTINUOUS'
    });

    // Check 1: Minimum Valid Observation Count (At least 6 valid frames required for sequence recognition, resampled to 30)
    if (uniqueObservationsCount < 6 && inputSource === 'webcam') {
      setRecordingState(RECORDING_STATES.SAMPLE_REJECTED);
      setTrackingState(TRACKING_STATES.LOW_CONFIDENCE);
      const reason = `Insufficient valid frames (${uniqueObservationsCount} collected, minimum 6 required).`;
      setHudDiagnostics(prev => ({
        ...prev,
        trackingStatus: TRACKING_STATES.LOW_CONFIDENCE,
        validSeqLength: uniqueObservationsCount,
        decisionReason: reason
      }));
      setActionFeedback({
        type: 'warning',
        text: `⚠️ ${reason} Ensure camera frame rate is stable.`
      });
      if (onEvaluationResult) {
        onEvaluationResult({
          success: false,
          status: 'RETRY',
          reason: `Insufficient valid frames (${uniqueObservationsCount} collected, minimum 6 required). Ensure camera is steady.`
        });
      }
      setTimeout(() => {
        setRecordingState(RECORDING_STATES.IDLE);
        setTrackingState(TRACKING_STATES.NO_SIGN);
      }, 4500);
      return;
    }

    // Check 2: Hand / Arm Landmark Availability Validation
    // Requires either tracked hands OR intentional wrist movement (for fist/closed-hand gestures like YES, 10, or wrist taps)
    const totalHandFrames = validLeftHandFrames + validRightHandFrames;
    const peakDisplacement = samples.length > 0 ? Math.max(...samples.map(s => s.handDisplacement || 0)) : 0;
    const hasHandTracking = totalHandFrames >= 2 || peakDisplacement >= 0.015;

    if (!hasHandTracking && inputSource === 'webcam') {
      setRecordingState(RECORDING_STATES.SAMPLE_REJECTED);
      setTrackingState(TRACKING_STATES.TRACKING_LOST);
      const reason = 'Hands / arms not detected. Please keep hands in camera view.';
      setHudDiagnostics(prev => ({
        ...prev,
        trackingStatus: TRACKING_STATES.TRACKING_LOST,
        validSeqLength: uniqueObservationsCount,
        decisionReason: reason
      }));
      setActionFeedback({
        type: 'warning',
        text: `⚠️ ${reason} Please keep hands in camera view.`
      });
      if (onEvaluationResult) {
        onEvaluationResult({
          success: false,
          status: 'RETRY',
          reason: 'Hands / arms not detected. Please keep both hands clearly in camera view.'
        });
      }
      setTimeout(() => {
        setRecordingState(RECORDING_STATES.IDLE);
        setTrackingState(TRACKING_STATES.NO_SIGN);
      }, 4500);
      return;
    }

    // Dynamic Movement Validation Path: Check intentional hand velocity and displacement
    const movingSamples = samples.filter(s => s.isHandMoving).length;
    const peakVelocity = samples.length > 0 ? Math.max(...samples.map(s => s.handVelocity || 0)) : 0;

    // Reject if user sat completely still / motionless
    if ((movingSamples < 2 || (peakVelocity < 0.05 && peakDisplacement < 0.012)) && inputSource === 'webcam') {
      setRecordingState(RECORDING_STATES.SAMPLE_REJECTED);
      setTrackingState(TRACKING_STATES.NO_SIGN);
      const reason = 'Stationary / Idle (no intentional gesture motion detected).';
      setHudDiagnostics(prev => ({
        ...prev,
        trackingStatus: TRACKING_STATES.NO_SIGN,
        validSeqLength: uniqueObservationsCount,
        modelPrediction: 'None (0%)',
        decisionReason: reason
      }));
      setActionFeedback({
        type: 'warning',
        text: `⚠️ Stationary pose detected. Insufficient intentional hand movement (${peakDisplacement.toFixed(3)} < 0.012). Please perform the sign.`
      });
      if (onEvaluationResult) {
        onEvaluationResult({
          success: false,
          status: 'RETRY',
          reason: 'Stationary pose detected. Insufficient gesture movement. Please perform the complete sign motion.'
        });
      }
      setTimeout(() => {
        setRecordingState(RECORDING_STATES.IDLE);
        setTrackingState(TRACKING_STATES.NO_SIGN);
      }, 4500);
      return;
    }

    // Step 4: Run Model Inference / Temporal Resampling
    setRecordingState(RECORDING_STATES.INFERENCE);
    setTrackingState(TRACKING_STATES.INFERENCE_PENDING);

    // Resample captured frames to model's canonical sequence length T = 30
    const resampledSequence = resampleSequence(samples, 30);

    // If in Dataset Recording Mode, persist real sequence to dataset (.npz)
    if (recordMode === 'DATASET') {
      setRecordingState(RECORDING_STATES.SAMPLE_ACCEPTED);
      setTrackingState(TRACKING_STATES.SIGN_CONFIRMED);
      try {
        const fps = cameraFps > 0 ? cameraFps : 30.0;
        await signBridgeService.recordDatasetSample(
          resampledSequence,
          datasetSign,
          datasetUserId,
          fps,
          {
            raw_frames_count: uniqueObservationsCount,
            has_left_hand: validLeftHandFrames > 0,
            has_right_hand: validRightHandFrames > 0,
            displacement: peakDisplacement,
            velocity: peakVelocity
          }
        );
        const nextCount = datasetSavedCount + 1;
        setDatasetSavedCount(nextCount);
        setActionFeedback({
          type: 'success',
          text: `💾 Saved [${datasetSign}] sample #${nextCount} for signer [${datasetUserId}] to dataset (.npz)!`
        });
        setHudDiagnostics(prev => ({
          ...prev,
          trackingStatus: TRACKING_STATES.SIGN_CONFIRMED,
          validSeqLength: uniqueObservationsCount,
          modelPrediction: `Saved: ${datasetSign}`,
          decisionReason: `Dataset recording saved to disk (.npz)`
        }));
      } catch (err) {
        setActionFeedback({
          type: 'warning',
          text: `Failed to save dataset sample: ${err.message}`
        });
      }
      setTimeout(() => {
        setRecordingState(RECORDING_STATES.IDLE);
        setTrackingState(TRACKING_STATES.NO_SIGN);
      }, 4500);
      return;
    }

    // Run backend ST-GCN inference (sole source of truth for prediction)
    let backendPrediction = null;
    let backendResult = null;
    try {
      const t0 = performance.now();
      backendResult = await signBridgeService.recognizeSequence(resampledSequence);
      backendInferenceDurationRef.current = performance.now() - t0;

      if (backendResult && backendResult.recognized_tokens && backendResult.recognized_tokens.length > 0) {
        backendPrediction = backendResult.recognized_tokens[0];
      }
    } catch (e) {
      console.warn("Backend inference error:", e);
    }

    // Step 5: Accept any valid model prediction with confidence >= 50%
    // We do NOT compare against a selectedTargetSign — the model speaks for itself.
    const backendGloss = String(backendPrediction?.gloss || '').toUpperCase();
    const backendConfidence = Number(backendPrediction?.confidence || 0);

    const hasValidPrediction = backendGloss.length > 0 && backendGloss !== '<BLANK>' && backendConfidence >= 0.50;

    if (hasValidPrediction) {
      setRecordingState(RECORDING_STATES.PREDICTED_ACTION);
      setTrackingState(TRACKING_STATES.SIGN_CONFIRMED);

      if (onRecordSign) {
        onRecordSign(backendGloss, backendConfidence, backendResult);
      }
      if (onEvaluationResult) {
        onEvaluationResult({
          success: true,
          status: 'SUCCESS',
          gloss: backendGloss,
          confidence: backendConfidence,
          fullResult: backendResult
        });
      }

      setHudDiagnostics(prev => ({
        ...prev,
        trackingStatus: TRACKING_STATES.SIGN_CONFIRMED,
        validSeqLength: uniqueObservationsCount,
        modelPrediction: `${backendGloss} (${Math.round(backendConfidence * 100)}%)`,
        decisionReason: `Confirmed: [${backendGloss}] via ST-GCN model`
      }));

      setActionFeedback({
        type: 'success',
        text: `✅ Sign recognized: [${backendGloss}] — ${Math.round(backendConfidence * 100)}% confidence, ${uniqueObservationsCount} frames`
      });
    } else {
      // Model returned blank, no prediction, or confidence too low
      setRecordingState(RECORDING_STATES.SAMPLE_REJECTED);
      setTrackingState(backendGloss ? TRACKING_STATES.LOW_CONFIDENCE : TRACKING_STATES.NO_SIGN);

      const reason = backendGloss && backendGloss !== '<BLANK>'
        ? `Model predicted [${backendGloss}] at ${Math.round(backendConfidence * 100)}% — below 50% confidence threshold.`
        : 'Model returned blank. Sign not recognized or not in vocabulary.';

      if (onEvaluationResult) {
        onEvaluationResult({
          success: false,
          status: backendGloss && backendGloss !== '<BLANK>' ? 'MISMATCH' : 'LOW_CONFIDENCE',
          gloss: backendGloss || '<BLANK>',
          confidence: backendConfidence,
          reason: reason
        });
      }

      setHudDiagnostics(prev => ({
        ...prev,
        trackingStatus: backendGloss && backendGloss !== '<BLANK>' ? TRACKING_STATES.LOW_CONFIDENCE : TRACKING_STATES.NO_SIGN,
        validSeqLength: uniqueObservationsCount,
        modelPrediction: backendGloss ? `${backendGloss} (${Math.round(backendConfidence * 100)}%)` : 'None (0%)',
        decisionReason: `Rejected: ${reason}`
      }));

      setActionFeedback({
        type: 'warning',
        text: `Sign not recognized. ${reason} Keep both hands visible and sign clearly.`
      });
    }

    setTimeout(() => {
      setRecordingState(RECORDING_STATES.IDLE);
      setTrackingState(TRACKING_STATES.NO_SIGN);
    }, 4500);
  };

  // Helper to process a new MediaPipe Holistic result and calculate precise physical kinematics
  const handleMediaPipeResults = useCallback((results) => {
    const now = performance.now();
    try {
      mediaPipeResultIdRef.current += 1;
      inferenceResultsSinceUpdateRef.current += 1;
      const procDuration = now - holisticProcessingStartTimeRef.current;
      mediaPipeProcessingDurationRef.current = procDuration;

      const formatted = extractSkeletalLandmarks(results);
      if (!formatted) return;

      liveResultsRef.current = {
        ...results,
        formattedSkeleton: formatted,
        resultId: mediaPipeResultIdRef.current,
        timestamp: now
      };

      // Extract current joints
      const curLeftWrist = formatted.pose[15] || formatted.leftHand[0] || { x: 0.35, y: 0.65, z: 0 };
      const curRightWrist = formatted.pose[16] || formatted.rightHand[0] || { x: 0.65, y: 0.65, z: 0 };
      const curLeftThumb = formatted.leftHand[4] || { x: curLeftWrist.x - 0.02, y: curLeftWrist.y - 0.04, z: 0 };
      const curRightThumb = formatted.rightHand[4] || { x: curRightWrist.x + 0.02, y: curRightWrist.y - 0.04, z: 0 };

      // Compute physical Euclidean displacement & velocity ONLY across consecutive MediaPipe inference frames
      let leftWristDisp = 0.0;
      let rightWristDisp = 0.0;
      let leftThumbDisp = 0.0;
      let rightThumbDisp = 0.0;

      const dtSec = Math.max(0.01, (now - lastMediaPipeResultTimeRef.current) / 1000.0);
      lastMediaPipeResultTimeRef.current = now;

      if (prevMediaPipeLandmarksRef.current) {
        const prev = prevMediaPipeLandmarksRef.current;

        leftWristDisp = Math.sqrt(
          Math.pow(curLeftWrist.x - prev.leftWrist.x, 2) +
          Math.pow(curLeftWrist.y - prev.leftWrist.y, 2) +
          Math.pow((curLeftWrist.z || 0) - (prev.leftWrist.z || 0), 2)
        );

        rightWristDisp = Math.sqrt(
          Math.pow(curRightWrist.x - prev.rightWrist.x, 2) +
          Math.pow(curRightWrist.y - prev.rightWrist.y, 2) +
          Math.pow((curRightWrist.z || 0) - (prev.rightWrist.z || 0), 2)
        );

        leftThumbDisp = Math.sqrt(
          Math.pow(curLeftThumb.x - prev.leftThumb.x, 2) +
          Math.pow(curLeftThumb.y - prev.leftThumb.y, 2)
        );

        rightThumbDisp = Math.sqrt(
          Math.pow(curRightThumb.x - prev.rightThumb.x, 2) +
          Math.pow(curRightThumb.y - prev.rightThumb.y, 2)
        );
      }

      prevMediaPipeLandmarksRef.current = {
        leftWrist: { ...curLeftWrist },
        rightWrist: { ...curRightWrist },
        leftThumb: { ...curLeftThumb },
        rightThumb: { ...curRightThumb },
        timestamp: now
      };

      // Apply strict deadband filter to eliminate stationary camera jitter (< 0.016 units treated as 0.0)
      const DEADBAND_THRESHOLD = 0.016;
      const applyDeadband = (d) => (d < DEADBAND_THRESHOLD ? 0.0 : d - DEADBAND_THRESHOLD);

      const filtLw = applyDeadband(leftWristDisp);
      const filtRw = applyDeadband(rightWristDisp);
      const filtLt = applyDeadband(leftThumbDisp);
      const filtRt = applyDeadband(rightThumbDisp);

      const rawDisplacement = Math.max(filtLw, filtRw, filtLt, filtRt);
      const rawVelocityNorm = rawDisplacement / dtSec;

      // Exponential Moving Average filter for clean, responsive velocity readout
      const alpha = 0.35;
      smoothedVelocityRef.current = alpha * rawVelocityNorm + (1 - alpha) * smoothedVelocityRef.current;
      smoothedDisplacementRef.current = alpha * rawDisplacement + (1 - alpha) * smoothedDisplacementRef.current;

      const activeVelocityNorm = smoothedVelocityRef.current;
      const activeVelocityMs = activeVelocityNorm * 0.42;

      // Intentional motion requires:
      // 1. Either hand genuinely tracked (not both wrist-anchored)
      // 2. Deadband displacement >= 0.018 AND velocity >= 0.10
      const hasRealHands = Boolean(formatted.hasLeftHand || formatted.hasRightHand);
      const isMoving = hasRealHands && (activeVelocityNorm >= 0.10 && smoothedDisplacementRef.current >= 0.018);

      // Update telemetry
      const p11 = formatted.pose[11] || { x: 0.3, y: 0.4, z: 0 };
      const p12 = formatted.pose[12] || { x: 0.7, y: 0.4, z: 0 };
      const center = {
        x: Number(((p11.x + p12.x) / 2).toFixed(3)),
        y: Number(((p11.y + p12.y) / 2).toFixed(3)),
        z: 0.0
      };
      const dx = p12.x - p11.x;
      const dy = p12.y - p11.y;
      const scale = Number(Math.sqrt(dx * dx + dy * dy).toFixed(3));

      latestTelemetryRef.current = {
        torsoCenter: center,
        shoulderScale: scale,
        jointVelocityNorm: Number(activeVelocityNorm.toFixed(2)),
        jointVelocityMs: Number(activeVelocityMs.toFixed(2)),
        handDisplacement: Number(smoothedDisplacementRef.current.toFixed(3)),
        leftHandVisible: Boolean(formatted.hasLeftHand),
        rightHandVisible: Boolean(formatted.hasRightHand),
        poseVisible: Boolean(formatted.pose && formatted.pose.length >= 17),
        motionLevel: isMoving ? 'ACTIVE MOTION' : 'IDLE'
      };

      // If actively recording, capture this fresh MediaPipe observation immediately
      if (isActivelyRecordingRef.current) {
        const motionMetrics = {
          velocity: activeVelocityNorm,
          displacement: smoothedDisplacementRef.current,
          isMoving: isMoving
        };
        recordObservationSample(mediaPipeResultIdRef.current, now, formatted, motionMetrics);
      }
    } catch (err) {
      console.error("[MediaPipe onResults Error]:", err);
    } finally {
      isHolisticProcessingRef.current = false;
    }
  }, [recordObservationSample]);

  // Start Webcam Stream & Initialize MediaPipe with Fast Lite Model (Model Complexity 0)
  const startWebcam = useCallback(async () => {
    try {
      setCameraError(null);
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error("Browser mediaDevices API not supported.");
      }

      // If stream is already active and tracks are running, avoid duplicate requests
      if (mediaStreamRef.current && mediaStreamRef.current.active) {
        if (videoRef.current && videoRef.current.srcObject !== mediaStreamRef.current) {
          videoRef.current.srcObject = mediaStreamRef.current;
          await videoRef.current.play().catch(() => {});
        }
        return;
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          frameRate: { ideal: 30 }
        },
        audio: false
      });

      mediaStreamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        try {
          await videoRef.current.play();
        } catch (err) {
          if (err.name !== 'AbortError') {
            console.warn("[SignBridge] Video play error:", err);
          }
        }
        if (setIsStreaming) setIsStreaming(true);
        setRecordingState(RECORDING_STATES.IDLE);

        // Hook requestVideoFrameCallback if available to register real hardware frames
        if ('requestVideoFrameCallback' in HTMLVideoElement.prototype && videoRef.current) {
          const onVideoFrameDelivered = (now, metadata) => {
            cameraFrameCounterRef.current += 1;
            cameraFramesSinceUpdateRef.current += 1;
            lastVideoFrameTimeRef.current = performance.now();
            if (videoRef.current && 'requestVideoFrameCallback' in videoRef.current) {
              videoFrameCallbackHandleRef.current = videoRef.current.requestVideoFrameCallback(onVideoFrameDelivered);
            }
          };
          videoFrameCallbackHandleRef.current = videoRef.current.requestVideoFrameCallback(onVideoFrameDelivered);
        }

        // Initialize MediaPipe Holistic once with Lite configuration for high FPS
        if (window.Holistic && !holisticInstanceRef.current) {
          try {
            const holistic = new window.Holistic({
              locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`
            });

            // Set Lite modelComplexity = 0 with optimized hand tracking confidence
            holistic.setOptions({
              modelComplexity: 0,
              smoothLandmarks: true,
              enableSegmentation: false,
              smoothSegmentation: false,
              refineFaceLandmarks: false,
              minDetectionConfidence: 0.35,
              minTrackingConfidence: 0.35
            });

            holistic.onResults((results) => {
              handleMediaPipeResults(results);
            });

            holisticInstanceRef.current = holistic;
            console.log("[SignBridge] MediaPipe Holistic (Lite 3D Mode) Initialized successfully.");
          } catch (e) {
            console.warn("[SignBridge] MediaPipe init fallback:", e);
          }
        }
      }
    } catch (err) {
      console.warn("Webcam access warning (fallback to simulator):", err);
      setCameraError("Camera unavailable or permission denied. Switched to Skeletal Simulator.");
      setInputSource('simulator');
      setRecordingState(RECORDING_STATES.IDLE);
      if (setIsStreaming) setIsStreaming(true);
    }
  }, [setIsStreaming, handleMediaPipeResults]);

  // Stop Webcam Stream
  const stopWebcam = useCallback(() => {
    if (videoFrameCallbackHandleRef.current && videoRef.current && 'cancelVideoFrameCallback' in videoRef.current) {
      try {
        videoRef.current.cancelVideoFrameCallback(videoFrameCallbackHandleRef.current);
      } catch (e) {}
      videoFrameCallbackHandleRef.current = null;
    }
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(track => track.stop());
      mediaStreamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    if (setIsStreaming) setIsStreaming(false);
  }, [setIsStreaming]);

  // Stream lifecycle effect
  useEffect(() => {
    if (inputSource === 'webcam') {
      startWebcam();
    } else {
      stopWebcam();
      setRecordingState(RECORDING_STATES.IDLE);
      if (setIsStreaming) setIsStreaming(true);
    }

    return () => {
      stopWebcam();
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (holisticInstanceRef.current) {
        try {
          holisticInstanceRef.current.close?.();
        } catch (e) {}
        holisticInstanceRef.current = null;
      }
    };
  }, [inputSource, startWebcam, stopWebcam, setIsStreaming]);

  // Main High-Performance Non-Blocking Animation & Rendering Loop (Solid 60 FPS)
  useEffect(() => {
    let animTime = 0;

    const renderLoop = (timestamp) => {
      // 1. Precise frame interval timing
      const dtSec = Math.max(0.005, (timestamp - prevFrameTimestampRef.current) / 1000.0);
      prevFrameTimestampRef.current = timestamp;
      renderFrameCounterRef.current += 1;
      renderFramesSinceUpdateRef.current += 1;
      animTime += 0.04;

      // 2. Rolling FPS Metrics updates (Every 500ms to avoid React re-render starvation)
      const elapsedRenderMs = timestamp - lastRenderFpsUpdateTimeRef.current;
      if (elapsedRenderMs >= 500) {
        const measuredRenderFps = Math.round((renderFramesSinceUpdateRef.current * 1000) / elapsedRenderMs);
        setRenderFps(measuredRenderFps);
        renderFramesSinceUpdateRef.current = 0;
        lastRenderFpsUpdateTimeRef.current = timestamp;

        // Inference FPS
        const elapsedInferenceMs = timestamp - lastInferenceFpsUpdateTimeRef.current;
        const measuredInferenceFps = Math.round((inferenceResultsSinceUpdateRef.current * 1000) / Math.max(1, elapsedInferenceMs));
        setInferenceFps(measuredInferenceFps);
        inferenceResultsSinceUpdateRef.current = 0;
        lastInferenceFpsUpdateTimeRef.current = timestamp;
        setMediaPipeLatencyMs(Math.round(mediaPipeProcessingDurationRef.current));

        // Camera FPS
        const elapsedCameraMs = timestamp - lastCameraFpsUpdateTimeRef.current;
        const measuredCameraFps = Math.round((cameraFramesSinceUpdateRef.current * 1000) / Math.max(1, elapsedCameraMs));
        setCameraFps(measuredCameraFps > 0 ? measuredCameraFps : (inputSource === 'webcam' ? 30 : measuredRenderFps));
        cameraFramesSinceUpdateRef.current = 0;
        // Sync React telemetry state
        const currentTelemetry = { ...latestTelemetryRef.current };
        setTelemetry(currentTelemetry);

        // Update HUD diagnostics
        const hasLH = currentTelemetry.leftHandVisible;
        const hasRH = currentTelemetry.rightHandVisible;
        const currentTracking = !isStreaming
          ? TRACKING_STATES.TRACKING_LOST
          : (!hasLH && !hasRH && inputSource === 'webcam')
          ? TRACKING_STATES.TRACKING_LOST
          : isActivelyRecordingRef.current
          ? TRACKING_STATES.COLLECTING_SEQUENCE
          : recordingState === RECORDING_STATES.VALIDATING || recordingState === RECORDING_STATES.INFERENCE
          ? TRACKING_STATES.INFERENCE_PENDING
          : currentTelemetry.motionLevel === 'ACTIVE MOTION'
          ? TRACKING_STATES.TRACKING
          : TRACKING_STATES.NO_SIGN;

        setHudDiagnostics(prev => ({
          ...prev,
          frameId: cameraFrameCounterRef.current || renderFrameCounterRef.current,
          timestamp: (timestamp / 1000).toFixed(2) + 's',
          lhCount: hasLH ? '21 (Tracked)' : '0 (Anchored)',
          rhCount: hasRH ? '21 (Tracked)' : '0 (Anchored)',
          trackingStatus: currentTracking,
          motionScore: currentTelemetry.jointVelocityNorm,
          validSeqLength: recordedSamplesRef.current.length,
          decisionReason: !hasLH && !hasRH && inputSource === 'webcam'
            ? 'Hands not detected. Please position hands in view.'
            : isActivelyRecordingRef.current
            ? 'Capturing temporal sequence...'
            : currentTelemetry.motionLevel === 'ACTIVE MOTION'
            ? 'Tracking active gesture movement'
            : 'Stationary / Idle (no motion)'
        }));
      }

      // Periodic Diagnostic Logging (Every 3.0s)
      if (timestamp - lastDiagnosticLogTimeRef.current >= 3000) {
        lastDiagnosticLogTimeRef.current = timestamp;
        if (inputSource === 'webcam' && videoRef.current) {
          const v = videoRef.current;
          console.log(`[SignBridge Camera Diagnostic]:`, {
            readyState: v.readyState,
            paused: v.paused,
            currentTime: Number(v.currentTime.toFixed(2)),
            videoWidth: v.videoWidth,
            videoHeight: v.videoHeight,
            cameraFps: cameraFps,
            inferenceFps: inferenceFps,
            renderFps: renderFps,
            mediaPipeLatencyMs: Math.round(mediaPipeProcessingDurationRef.current),
            motionLevel: latestTelemetryRef.current.motionLevel,
            jointVelocity: latestTelemetryRef.current.jointVelocityMs
          });
        }
      }

      const canvas = canvasRef.current;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // 3. Process Video Frame & Non-blocking MediaPipe Dispatch
        const video = videoRef.current;
        const isVideoReady = inputSource === 'webcam' && video && video.readyState >= 2 && !video.paused;

        if (isVideoReady) {
          // Track frame advancement when requestVideoFrameCallback is unsupported
          if (!('requestVideoFrameCallback' in HTMLVideoElement.prototype)) {
            if (video.currentTime !== lastVideoCurrentTimeRef.current) {
              lastVideoCurrentTimeRef.current = video.currentTime;
              cameraFrameCounterRef.current += 1;
              cameraFramesSinceUpdateRef.current += 1;
            }
          }

          // Fast GPU canvas draw (mirrored for natural user interaction)
          ctx.save();
          ctx.translate(width, 0);
          ctx.scale(-1, 1);
          ctx.drawImage(video, 0, 0, width, height);
          ctx.restore();

          // Non-blocking asynchronous MediaPipe send with 2000ms watchdog recovery
          const now = performance.now();
          if (
            isHolisticProcessingRef.current &&
            now - holisticProcessingStartTimeRef.current > 2000
          ) {
            console.warn('[SignBridge] MediaPipe inference timed out; recovering.');
            isHolisticProcessingRef.current = false;
          }

          // Ensure MediaPipe is initialized as soon as the global window.Holistic script loads
          if (!holisticInstanceRef.current && window.Holistic) {
            try {
              const holistic = new window.Holistic({
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`
              });
              holistic.setOptions({
                modelComplexity: 0,
                smoothLandmarks: true,
                enableSegmentation: false,
                smoothSegmentation: false,
                refineFaceLandmarks: false,
                minDetectionConfidence: 0.35,
                minTrackingConfidence: 0.35
              });
              holistic.onResults((results) => {
                handleMediaPipeResults(results);
              });
              holisticInstanceRef.current = holistic;
              console.log("[SignBridge] MediaPipe Holistic dynamically attached to webcam loop.");
            } catch (e) {
              console.warn("[SignBridge] Deferred MediaPipe init error:", e);
            }
          }

          if (holisticInstanceRef.current && !isHolisticProcessingRef.current) {
            isHolisticProcessingRef.current = true;
            holisticProcessingStartTimeRef.current = now;

            // Use 480x360 resolution for sharp hand palm ROI detection
            if (!offscreenCanvasRef.current) {
              const offCanvas = document.createElement('canvas');
              offCanvas.width = 480;
              offCanvas.height = 360;
              offscreenCanvasRef.current = offCanvas;
            }
            const offCtx = offscreenCanvasRef.current.getContext('2d', { willReadFrequently: false, alpha: false });
            offCtx.drawImage(video, 0, 0, 480, 360);

            holisticInstanceRef.current.send({ image: offscreenCanvasRef.current }).catch((err) => {
              isHolisticProcessingRef.current = false;
            });
          }

          // Subtle dark overlay for high contrast landmark rendering
          ctx.fillStyle = 'rgba(5, 8, 16, 0.35)';
          ctx.fillRect(0, 0, width, height);
        } else {
          // Simulator or Offline Background
          const grad = ctx.createLinearGradient(0, 0, width, height);
          grad.addColorStop(0, '#090d16');
          grad.addColorStop(1, '#0f172a');
          ctx.fillStyle = grad;
          ctx.fillRect(0, 0, width, height);

          ctx.strokeStyle = 'rgba(99, 102, 241, 0.08)';
          ctx.lineWidth = 1;
          for (let x = 0; x < width; x += 30) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
          }
          for (let y = 0; y < height; y += 30) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
          }
        }

        // 4. Extract or Synthesize 3D Landmarks
        let skeleton;
        const liveResults = liveResultsRef.current;
        if (inputSource === 'webcam' && liveResults && liveResults.formattedSkeleton) {
          skeleton = liveResults.formattedSkeleton;
        } else {
          skeleton = generateVisualLandmarks(animTime, simulatorSign, width, height);
        }

        // Simulator Recording Handler (runs per frame in simulator mode)
        if (inputSource === 'simulator') {
          const curLeftWrist = skeleton.pose[15] || skeleton.leftHand[0] || { x: 0.35, y: 0.65, z: 0 };
          const curRightWrist = skeleton.pose[16] || skeleton.rightHand[0] || { x: 0.65, y: 0.65, z: 0 };
          const curLeftThumb = skeleton.leftHand[4] || { x: curLeftWrist.x - 0.02, y: curLeftWrist.y - 0.04, z: 0 };
          const curRightThumb = skeleton.rightHand[4] || { x: curRightWrist.x + 0.02, y: curRightWrist.y - 0.04, z: 0 };

          let leftWristDisp = 0.0;
          let rightWristDisp = 0.0;

          if (prevMediaPipeLandmarksRef.current) {
            const prev = prevMediaPipeLandmarksRef.current;
            leftWristDisp = Math.sqrt(Math.pow(curLeftWrist.x - prev.leftWrist.x, 2) + Math.pow(curLeftWrist.y - prev.leftWrist.y, 2));
            rightWristDisp = Math.sqrt(Math.pow(curRightWrist.x - prev.rightWrist.x, 2) + Math.pow(curRightWrist.y - prev.rightWrist.y, 2));
          }

          prevMediaPipeLandmarksRef.current = {
            leftWrist: { ...curLeftWrist },
            rightWrist: { ...curRightWrist },
            leftThumb: { ...curLeftThumb },
            rightThumb: { ...curRightThumb },
            timestamp: timestamp
          };

          const rawDisplacement = Math.max(leftWristDisp, rightWristDisp);
          const rawVelocityNorm = rawDisplacement / dtSec;
          const alpha = 0.35;
          smoothedVelocityRef.current = alpha * rawVelocityNorm + (1 - alpha) * smoothedVelocityRef.current;
          smoothedDisplacementRef.current = alpha * rawDisplacement + (1 - alpha) * smoothedDisplacementRef.current;

          const isMoving = smoothedVelocityRef.current > 0.05 || smoothedDisplacementRef.current > 0.004;

          const p11 = skeleton.pose[11] || { x: 0.3, y: 0.4, z: 0 };
          const p12 = skeleton.pose[12] || { x: 0.7, y: 0.4, z: 0 };
          const center = {
            x: Number(((p11.x + p12.x) / 2).toFixed(3)),
            y: Number(((p11.y + p12.y) / 2).toFixed(3)),
            z: 0.0
          };
          const dx = p12.x - p11.x;
          const dy = p12.y - p11.y;
          const scale = Number(Math.sqrt(dx * dx + dy * dy).toFixed(3));

          latestTelemetryRef.current = {
            torsoCenter: center,
            shoulderScale: scale,
            jointVelocityNorm: Number(smoothedVelocityRef.current.toFixed(2)),
            jointVelocityMs: Number((smoothedVelocityRef.current * 0.42).toFixed(2)),
            handDisplacement: Number(smoothedDisplacementRef.current.toFixed(3)),
            leftHandVisible: Boolean(skeleton.hasLeftHand),
            rightHandVisible: Boolean(skeleton.hasRightHand),
            poseVisible: Boolean(skeleton.pose && skeleton.pose.length >= 17),
            motionLevel: isMoving ? 'ACTIVE MOTION' : 'IDLE'
          };
        }

        // 5. Render High-Visibility Skeletal Overlays
        if (showPose) drawPoseSkeleton(ctx, skeleton.pose, width, height);
        if (showHands) {
          // Cyan for Left Hand, Violet for Right Hand
          drawHandMesh(ctx, skeleton.leftHand, skeleton.hasLeftHand ? '#06b6d4' : 'rgba(6, 182, 212, 0.4)', width, height, skeleton.hasLeftHand);
          drawHandMesh(ctx, skeleton.rightHand, skeleton.hasRightHand ? '#a855f7' : 'rgba(168, 85, 247, 0.4)', width, height, skeleton.hasRightHand);
        }
        if (showFace) drawFaceContours(ctx, skeleton.face, width, height);

        // 6. Broadcast landmarks to parent / WebSocket with telemetry metadata if active
        if (onLandmarksUpdate) {
          const rawFlat = [];
          const allPts = [...skeleton.pose, ...skeleton.leftHand, ...skeleton.rightHand, ...skeleton.face];
          allPts.forEach(pt => rawFlat.push(pt.x, pt.y, pt.z || 0));
          const meta = {
            has_left_hand: Boolean(skeleton.hasLeftHand),
            has_right_hand: Boolean(skeleton.hasRightHand),
            is_moving: latestTelemetryRef.current.motionLevel === 'ACTIVE MOTION',
            motion_score: latestTelemetryRef.current.jointVelocityNorm,
            isActivelyRecording: isActivelyRecordingRef.current,
            recordingPhase: recordingPhase
          };
          onLandmarksUpdate(rawFlat, meta);
        }
      }

      animationFrameRef.current = requestAnimationFrame(renderLoop);
    };

    animationFrameRef.current = requestAnimationFrame(renderLoop);

    return () => {
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
    };
  }, [inputSource, showPose, showHands, showFace, onLandmarksUpdate, recordObservationSample, cameraFps, inferenceFps, renderFps]);

  return (
    <div className="relative glass-panel rounded-2xl overflow-hidden border border-slate-700/60 shadow-2xl flex flex-col">
      {/* Video & Tracking Canvas */}
      <div className="relative aspect-[4/3] w-full bg-slate-950 flex items-center justify-center overflow-hidden">
        {/* Active video element: off-screen/zero-opacity container ensures Chromium hardware decoding stays active */}
        <video
          ref={videoRef}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '1px',
            height: '1px',
            opacity: 0,
            pointerEvents: 'none',
            zIndex: -10
          }}
          playsInline
          muted
          autoPlay
        />

        {/* 2D/3D Tracking Overlay Canvas */}
        <canvas
          ref={canvasRef}
          width={640}
          height={480}
          className="w-full h-full object-cover"
        />

        {/* Top Floating HUD Badges */}
        <div className="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none">
          <div className="flex items-center space-x-2 pointer-events-auto">
            <span className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-900/90 backdrop-blur-md border border-emerald-500/30 text-emerald-400 text-xs font-semibold shadow-lg">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>CAMERA {inputSource === 'webcam' ? 'LIVE' : 'SIMULATOR'}</span>
            </span>
            <span className="px-2.5 py-1 rounded-full bg-slate-900/90 backdrop-blur-md border border-indigo-500/30 text-indigo-300 text-xs font-mono shadow-lg">
              {renderFps} FPS {inferenceFps > 0 ? `(${inferenceFps} AI FPS • ${mediaPipeLatencyMs}ms)` : ''}
            </span>
          </div>

          <div className="flex items-center space-x-2 pointer-events-auto">
            <span className={`px-2.5 py-1 rounded-full backdrop-blur-md text-xs font-mono font-bold border transition-colors shadow-lg ${
              recordingPhase === 'recording'
                ? 'bg-red-950/90 border-red-500/60 text-red-300 animate-pulse'
                : recordingPhase === 'countdown'
                ? 'bg-amber-950/90 border-amber-500/60 text-amber-300 animate-pulse'
                : telemetry.motionLevel === 'ACTIVE MOTION'
                ? 'bg-emerald-950/85 border-emerald-500/50 text-emerald-300'
                : 'bg-slate-900/85 border-slate-700/60 text-slate-400'
            }`}>
              ● {recordingPhase === 'recording'
                  ? `RECORDING (${displayCountdown}s)`
                  : recordingPhase === 'countdown'
                  ? `GET READY (${displayCountdown})`
                  : telemetry.motionLevel}
            </span>
            <span className="px-2 py-0.5 rounded-md bg-slate-900/90 border border-slate-800 text-[10px] font-mono text-cyan-300 shadow">
              STATE: {recordingState}
            </span>
          </div>
        </div>

        {/* Hand Visibility Indicators (Top Center) */}
        {inputSource === 'webcam' && (
          <div className="absolute top-12 left-3 flex items-center space-x-2 pointer-events-none">
            <span className={`px-2 py-0.5 rounded-md backdrop-blur-md text-[10px] font-mono border ${
              telemetry.leftHandVisible
                ? 'bg-cyan-950/80 border-cyan-500/40 text-cyan-300'
                : 'bg-slate-900/80 border-slate-700 text-slate-500'
            }`}>
              ✋ Left: {telemetry.leftHandVisible ? 'Tracked (21pts)' : 'Wrist-anchored'}
            </span>
            <span className={`px-2 py-0.5 rounded-md backdrop-blur-md text-[10px] font-mono border ${
              telemetry.rightHandVisible
                ? 'bg-purple-950/80 border-purple-500/40 text-purple-300'
                : 'bg-slate-900/80 border-slate-700 text-slate-500'
            }`}>
              ✋ Right: {telemetry.rightHandVisible ? 'Tracked (21pts)' : 'Wrist-anchored'}
            </span>
          </div>
        )}

        {/* Hands Missing Warning Banner */}
        {inputSource === 'webcam' && !telemetry.leftHandVisible && !telemetry.rightHandVisible && (
          <div className="absolute top-20 left-4 right-4 p-2.5 rounded-xl bg-amber-950/95 border border-amber-500/70 text-amber-200 text-xs font-bold flex items-center justify-center space-x-2 shadow-2xl backdrop-blur-md z-20 animate-in fade-in duration-200 pointer-events-none">
            <Hand className="w-4 h-4 text-amber-400 animate-pulse flex-shrink-0" />
            <span>⚠️ TRACKING WARNING: Hands not detected. Position hands in camera view.</span>
          </div>
        )}

        {/* ACTIVE COUNTDOWN / RECORDING OVERLAY */}
        {recordingPhase !== 'idle' && (
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center space-y-3 z-30 animate-in fade-in duration-150 pointer-events-none">
            <div className={`w-16 h-16 rounded-full border-2 flex items-center justify-center text-3xl font-extrabold text-white animate-pulse ${
              recordingPhase === 'countdown' ? 'bg-amber-600/40 border-amber-400' : 'bg-red-600/40 border-red-500'
            }`}>
              {displayCountdown}
            </div>
            <div className="text-center space-y-1">
              <h4 className="text-base font-extrabold text-white uppercase tracking-wider">
                {recordingPhase === 'countdown' ? '⏳ GET READY TO DEMONSTRATE SIGN' : '🔴 RECORDING NOW: PERFORM GESTURE (3s)'}
              </h4>
              <p className="text-xs text-slate-300 max-w-sm">
                Perform your ISL sign clearly and hold it within camera bounds.
              </p>
            </div>
            {/* Progress bar */}
            <div className="w-48 h-2 bg-slate-800 rounded-full overflow-hidden border border-slate-700">
              <div
                className={`h-full transition-all duration-1000 ease-linear ${
                  recordingPhase === 'countdown' ? 'bg-amber-400' : 'bg-red-500'
                }`}
                style={{ width: `${((4 - displayCountdown) / 3) * 100}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Action Feedback Banner */}
        {actionFeedback && (
          <div className={`absolute top-16 left-4 right-4 p-3 rounded-xl border shadow-2xl backdrop-blur-md flex items-center justify-between text-xs font-bold z-20 animate-in fade-in zoom-in-95 duration-200 ${
            actionFeedback.type === 'success'
              ? 'bg-emerald-950/95 border-emerald-500/60 text-emerald-200'
              : 'bg-amber-950/95 border-amber-500/60 text-amber-200'
          }`}>
            <div className="flex items-center space-x-2">
              {actionFeedback.type === 'success' ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              ) : (
                <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
              )}
              <span>{actionFeedback.text}</span>
            </div>
            <button
              onClick={() => setActionFeedback(null)}
              className="text-slate-400 hover:text-white font-bold ml-2"
            >
              ✕
            </button>
          </div>
        )}

        {/* Normalization & Telemetry Overlay (Bottom Left) */}
        {showMetrics && recordingPhase === 'idle' && (
          <div className="absolute bottom-3 left-3 bg-slate-900/90 backdrop-blur-md border border-slate-700/80 rounded-xl p-2.5 text-xs text-slate-300 font-mono space-y-1 shadow-lg pointer-events-none">
            <div className="flex items-center justify-between space-x-4">
              <span className="text-slate-400">Torso Center:</span>
              <span className="text-emerald-400">({telemetry.torsoCenter.x}, {telemetry.torsoCenter.y})</span>
            </div>
            <div className="flex items-center justify-between space-x-4">
              <span className="text-slate-400">Hand Displacement:</span>
              <span className="text-indigo-300">{telemetry.handDisplacement.toFixed(3)} norm</span>
            </div>
            <div className="flex items-center justify-between space-x-4">
              <span className="text-slate-400">Joint Velocity:</span>
              <span className="text-cyan-400 font-bold">
                {telemetry.jointVelocityNorm.toFixed(2)} norm/s (~{telemetry.jointVelocityMs.toFixed(2)} m/s)
              </span>
            </div>
          </div>
        )}

        {/* Main Action Record Trigger (Bottom Right) */}
        <div className="absolute bottom-3 right-3 flex items-center space-x-2 z-10">
          <button
            onClick={handleStartRecordingAction}
            disabled={recordingPhase !== 'idle'}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-extrabold shadow-2xl transition transform active:scale-95 ${
              recordingPhase !== 'idle'
                ? 'bg-red-600 text-white animate-pulse'
                : recordMode === 'DATASET'
                ? 'bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500 text-white shadow-lg'
                : 'bg-gradient-to-r from-red-600 via-purple-600 to-indigo-600 hover:from-red-500 hover:to-indigo-500 text-white shadow-lg'
            }`}
          >
            <CircleDot className={`w-4 h-4 text-white ${recordingPhase !== 'idle' ? 'animate-spin' : ''}`} />
            <span>
              {recordingPhase === 'countdown'
                ? `⏳ Get Ready (${displayCountdown}s)...`
                : recordingPhase === 'recording'
                ? `🔴 Recording Sign (${displayCountdown}s)...`
                : recordMode === 'DATASET'
                ? `🔴 Record [${datasetSign}] (.npz)`
                : '🔴 Capture Sign (3s)'}
            </span>
            {recordingPhase === 'idle' && (
              <span className="ml-1.5 px-1.5 py-0.5 bg-black/40 border border-white/20 rounded text-[10px] font-mono text-slate-200">
                Space
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Dataset Recording Tool Header Banner (Visible when DATASET mode selected) */}
      {recordMode === 'DATASET' && (
        <div className="p-3 bg-gradient-to-r from-emerald-950/90 via-teal-950/80 to-slate-900 border-t border-emerald-600/40 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center space-x-2">
            <span className="font-extrabold text-emerald-300 flex items-center space-x-1">
              <span>💾 Dataset Sign:</span>
            </span>
            <select
              value={datasetSign}
              onChange={(e) => setDatasetSign(e.target.value)}
              className="bg-slate-900 border border-emerald-500/50 rounded-lg px-2.5 py-1 text-xs font-bold text-white focus:outline-none focus:ring-1 focus:ring-emerald-400"
            >
              {ALL_42_ISL_SIGNS.map(sign => (
                <option key={sign} value={sign}>
                  {sign}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-slate-400 font-medium">Signer ID:</span>
            <input
              type="text"
              value={datasetUserId}
              onChange={(e) => setDatasetUserId(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1 text-xs font-mono text-cyan-300 w-24 focus:outline-none focus:border-cyan-400"
              placeholder="user_01"
            />
          </div>

          <div className="flex items-center space-x-2 text-[11px] font-mono text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded-lg border border-emerald-500/30">
            <span>Saved This Session:</span>
            <span className="font-extrabold text-white text-xs">{datasetSavedCount}</span>
          </div>
        </div>
      )}

      {/* Camera Toolbar — Source Switch, Mode Switch & Overlay Toggles */}
      <div className="p-3 bg-slate-900/90 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs">
        {/* Mode toggle: Live Recognize vs Dataset Recorder */}
        <div className="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => setRecordMode('RECOGNIZE')}
            className={`px-3 py-1 rounded-md font-semibold transition ${
              recordMode === 'RECOGNIZE' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            🎯 Live Inference
          </button>
          <button
            onClick={() => setRecordMode('DATASET')}
            className={`px-3 py-1 rounded-md font-semibold transition ${
              recordMode === 'DATASET' ? 'bg-emerald-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            💾 Dataset Recorder (42 Signs)
          </button>
        </div>

        {/* Source toggle */}
        <div className="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => setInputSource('webcam')}
            className={`px-3 py-1 rounded-md font-semibold transition ${
              inputSource === 'webcam' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Webcam
          </button>
          <button
            onClick={() => setInputSource('simulator')}
            className={`px-3 py-1 rounded-md font-semibold transition ${
              inputSource === 'simulator' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Simulator
          </button>
        </div>

        {/* Overlay toggles */}
        <div className="flex items-center space-x-1">
          <button
            onClick={() => setShowPose(!showPose)}
            className={`p-1.5 rounded-lg border text-[10px] font-bold px-2 transition ${
              showPose ? 'bg-emerald-950/60 border-emerald-500/40 text-emerald-300' : 'bg-slate-950 border-slate-800 text-slate-500'
            }`}
          >
            POSE
          </button>
          <button
            onClick={() => setShowHands(!showHands)}
            className={`p-1.5 rounded-lg border text-[10px] font-bold px-2 transition ${
              showHands ? 'bg-cyan-950/60 border-cyan-500/40 text-cyan-300' : 'bg-slate-950 border-slate-800 text-slate-500'
            }`}
          >
            HANDS
          </button>
          <button
            onClick={() => setShowFace(!showFace)}
            className={`p-1.5 rounded-lg border text-[10px] font-bold px-2 transition ${
              showFace ? 'bg-amber-950/60 border-amber-500/40 text-amber-300' : 'bg-slate-950 border-slate-800 text-slate-500'
            }`}
          >
            FACE
          </button>
          <button
            onClick={() => setShowHudDebug(!showHudDebug)}
            className={`p-1.5 rounded-lg border text-[10px] font-bold px-2 transition ${
              showHudDebug ? 'bg-indigo-950/60 border-indigo-500/40 text-indigo-300' : 'bg-slate-950 border-slate-800 text-slate-500'
            }`}
          >
            HUD DEBUG
          </button>
        </div>
      </div>

      {/* HUD SYSTEM DIAGNOSTICS PANEL (8 Requested Fields) */}
      {showHudDebug && (
        <div className="p-3.5 bg-slate-950/95 border-t border-slate-800 text-xs font-mono space-y-2.5">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
            <div className="flex items-center space-x-2 text-indigo-400 font-bold">
              <Activity className="w-3.5 h-3.5 text-cyan-400" />
              <span className="uppercase tracking-wider text-[11px]">HUD SYSTEM DIAGNOSTICS</span>
            </div>
            <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
              hudDiagnostics.trackingStatus === TRACKING_STATES.SIGN_CONFIRMED
                ? 'bg-emerald-950 text-emerald-300 border border-emerald-500/40'
                : hudDiagnostics.trackingStatus === TRACKING_STATES.TRACKING_LOST
                ? 'bg-red-950 text-red-300 border border-red-500/40'
                : hudDiagnostics.trackingStatus === TRACKING_STATES.LOW_CONFIDENCE
                ? 'bg-amber-950 text-amber-300 border border-amber-500/40'
                : 'bg-slate-900 text-slate-300 border border-slate-700'
            }`}>
              STATUS: {hudDiagnostics.trackingStatus}
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px]">
            {/* 1. Frame ID */}
            <div className="p-2 rounded-lg bg-slate-900/80 border border-slate-800/80">
              <div className="text-slate-500 text-[10px]">1. Frame ID</div>
              <div className="font-bold text-slate-200">#{hudDiagnostics.frameId}</div>
            </div>

            {/* 2. Timestamp */}
            <div className="p-2 rounded-lg bg-slate-900/80 border border-slate-800/80">
              <div className="text-slate-500 text-[10px]">2. Timestamp</div>
              <div className="font-bold text-slate-200">{hudDiagnostics.timestamp}</div>
            </div>

            {/* 3. LH/RH Counts */}
            <div className="p-2 rounded-lg bg-slate-900/80 border border-slate-800/80">
              <div className="text-slate-500 text-[10px]">3. LH / RH Counts</div>
              <div className="font-bold text-cyan-300">
                {hudDiagnostics.lhCount} | {hudDiagnostics.rhCount}
              </div>
            </div>

            {/* 4. Tracking Status */}
            <div className="p-2 rounded-lg bg-slate-900/80 border border-slate-800/80">
              <div className="text-slate-500 text-[10px]">4. Tracking Status</div>
              <div className="font-bold text-amber-300">{hudDiagnostics.trackingStatus}</div>
            </div>

            {/* 5. Motion Score */}
            <div className="p-2 rounded-lg bg-slate-900/80 border border-slate-800/80">
              <div className="text-slate-500 text-[10px]">5. Motion Score</div>
              <div className="font-bold text-emerald-400">{hudDiagnostics.motionScore.toFixed(3)}</div>
            </div>

            {/* 6. Sequence Length */}
            <div className="p-2 rounded-lg bg-slate-900/80 border border-slate-800/80">
              <div className="text-slate-500 text-[10px]">6. Valid Sequence</div>
              <div className="font-bold text-purple-300">{hudDiagnostics.validSeqLength} frames</div>
            </div>

            {/* 7. Model Prediction */}
            <div className="p-2 rounded-lg bg-slate-900/80 border border-slate-800/80">
              <div className="text-slate-500 text-[10px]">7. Model Prediction</div>
              <div className="font-bold text-indigo-300">{hudDiagnostics.modelPrediction}</div>
            </div>

            {/* 8. Decision Reason / Confirmed Token */}
            <div className="p-2 rounded-lg bg-slate-900/80 border border-slate-800/80">
              <div className="text-slate-500 text-[10px]">8. Decision Reason</div>
              <div className="font-bold text-slate-300 truncate" title={hudDiagnostics.decisionReason}>
                {hudDiagnostics.decisionReason}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// --- Temporal Coordinate Resampling Helper ---

/**
 * Resamples a variable-length recorded frame array into fixed model window T = 30 using linear interpolation.
 * Always guarantees output shape (30, 107, 3).
 */
function resampleSequence(samples, targetLength = 30) {
  if (!samples || samples.length === 0) return [];

  const extractFramePoints = (sample) => {
    const s = sample.landmarks || sample;
    const pose = (s.pose && s.pose.length >= 25) ? s.pose.slice(0, 25) : [];
    while (pose.length < 25) pose.push({ x: 0, y: 0, z: 0 });

    const lh = (s.leftHand && s.leftHand.length >= 21) ? s.leftHand.slice(0, 21) : [];
    while (lh.length < 21) lh.push({ x: pose[15]?.x || 0.35, y: pose[15]?.y || 0.65, z: 0 });

    const rh = (s.rightHand && s.rightHand.length >= 21) ? s.rightHand.slice(0, 21) : [];
    while (rh.length < 21) rh.push({ x: pose[16]?.x || 0.65, y: pose[16]?.y || 0.65, z: 0 });

    const face = (s.face && s.face.length >= 40) ? s.face.slice(0, 40) : [];
    while (face.length < 40) face.push({ x: pose[0]?.x || 0.5, y: pose[0]?.y || 0.25, z: 0 });

    const allPts = [...pose, ...lh, ...rh, ...face]; // Exactly 107 joints
    return allPts.map(pt => [pt.x, pt.y, pt.z || 0]);
  };

  if (samples.length === targetLength) {
    return samples.map(extractFramePoints);
  }

  const result = [];
  const srcLen = samples.length;

  for (let i = 0; i < targetLength; i++) {
    const srcIndexFloat = (i / (targetLength - 1)) * (srcLen - 1);
    const lowIdx = Math.floor(srcIndexFloat);
    const highIdx = Math.min(srcLen - 1, Math.ceil(srcIndexFloat));
    const fraction = srcIndexFloat - lowIdx;

    const lowPts = extractFramePoints(samples[lowIdx]);
    const highPts = extractFramePoints(samples[highIdx]);

    const framePts = [];
    for (let p = 0; p < 107; p++) {
      const pL = lowPts[p] || [0, 0, 0];
      const pH = highPts[p] || [0, 0, 0];
      framePts.push([
        pL[0] + (pH[0] - pL[0]) * fraction,
        pL[1] + (pH[1] - pL[1]) * fraction,
        pL[2] + (pH[2] - pL[2]) * fraction
      ]);
    }
    result.push(framePts);
  }

  return result;
}

// --- Kinematic Trajectory Classifier ---

/**
 * Classifies kinematic features of a recorded landmark sequence against ISL templates
 */
function classifyKinematicTrajectory(samples, targetSign) {
  if (!samples || samples.length === 0) {
    return { isMatch: false, predictedSign: 'NONE', confidence: 0.0 };
  }

  // Check genuine hand tracking: require at least 5 frames with tracked hands
  const trackedHandFrames = samples.filter(s => s.leftHandVisible || s.rightHandVisible).length;
  if (trackedHandFrames < 5 && targetSign !== 'CHEST') {
    return { isMatch: false, predictedSign: 'NO_HANDS', confidence: 0.0 };
  }

  const rwYValues = samples.map(s => s.rightWrist ? s.rightWrist.y : 0.65);
  const rwXValues = samples.map(s => s.rightWrist ? s.rightWrist.x : 0.65);

  const minY = Math.min(...rwYValues);
  const maxY = Math.max(...rwYValues);
  const deltaY = maxY - minY;

  const minX = Math.min(...rwXValues);
  const maxX = Math.max(...rwXValues);
  const deltaX = maxX - minX;

  const avgRwY = rwYValues.reduce((a, b) => a + b, 0) / rwYValues.length;
  const peakVelocity = Math.max(...samples.map(s => s.handVelocity || 0));

  // If user was essentially stationary, do not match any dynamic gesture
  if (deltaY < 0.035 && deltaX < 0.035 && peakVelocity < 0.08) {
    return { isMatch: false, predictedSign: 'IDLE', confidence: 0.0 };
  }

  // Count vertical inflection cycles with minimum displacement threshold (> 0.005 step)
  let verticalInflections = 0;
  for (let i = 2; i < rwYValues.length; i++) {
    const diff1 = rwYValues[i - 1] - rwYValues[i - 2];
    const diff2 = rwYValues[i] - rwYValues[i - 1];
    if (diff1 * diff2 < -0.0004 && Math.abs(diff1) > 0.005 && Math.abs(diff2) > 0.005) {
      verticalInflections++;
    }
  }

  // Count horizontal inflection cycles with minimum displacement threshold (> 0.005 step)
  let horizontalInflections = 0;
  for (let i = 2; i < rwXValues.length; i++) {
    const diff1 = rwXValues[i - 1] - rwXValues[i - 2];
    const diff2 = rwXValues[i] - rwXValues[i - 1];
    if (diff1 * diff2 < -0.0004 && Math.abs(diff1) > 0.005 && Math.abs(diff2) > 0.005) {
      horizontalInflections++;
    }
  }

  let isMatch = false;
  let confidence = 0.50;

  if (targetSign === 'YES') {
    // YES requires vertical nodding oscillations (deltaY >= 0.035 and vertical inflections >= 2)
    if (verticalInflections >= 2 && deltaY >= 0.035 && deltaY >= deltaX * 0.7) {
      isMatch = true;
      confidence = Math.min(0.97, 0.86 + Math.min(0.11, verticalInflections * 0.03));
    }
  } else if (targetSign === 'NO') {
    // NO requires horizontal shake oscillations (deltaX >= 0.035 and horizontal inflections >= 2)
    if (horizontalInflections >= 2 && deltaX >= 0.035 && deltaX >= deltaY * 0.7) {
      isMatch = true;
      confidence = Math.min(0.96, 0.85 + Math.min(0.11, horizontalInflections * 0.03));
    }
  } else if (targetSign === 'HELP') {
    // HELP requires right hand lifting upward
    if (minY < 0.50 && deltaY >= 0.035) {
      isMatch = true;
      confidence = Math.min(0.98, 0.88 + deltaY);
    }
  } else if (targetSign === 'HELLO') {
    // HELLO requires high hand near temple (avgY < 0.38) with lateral motion
    if (avgRwY < 0.38 && deltaX >= 0.030) {
      isMatch = true;
      confidence = Math.min(0.97, 0.86 + deltaX);
    }
  } else if (targetSign === 'WATER') {
    // WATER requires hand positioned near chin (y < 0.42)
    if (avgRwY < 0.42 && peakVelocity >= 0.06) {
      isMatch = true;
      confidence = Math.min(0.95, 0.85 + peakVelocity * 0.15);
    }
  } else if (targetSign === 'DOCTOR') {
    // DOCTOR requires right hand near left wrist
    const minDistance = Math.min(...samples.map(s => {
      const rw = s.rightWrist || { x: 0.6, y: 0.6 };
      const lw = s.leftWrist || { x: 0.4, y: 0.6 };
      return Math.sqrt(Math.pow(rw.x - lw.x, 2) + Math.pow(rw.y - lw.y, 2));
    }));
    if (minDistance < 0.28) {
      isMatch = true;
      confidence = Math.min(0.96, 0.85 + (0.28 - minDistance));
    }
  } else if (targetSign === 'HOSPITAL') {
    if (deltaY >= 0.025 && deltaX >= 0.025) {
      isMatch = true;
      confidence = 0.92;
    }
  } else if (targetSign === 'POLICE') {
    if (avgRwY < 0.36 && peakVelocity >= 0.05) {
      isMatch = true;
      confidence = 0.93;
    }
  } else if (targetSign === 'PAIN') {
    if (deltaX >= 0.025 && deltaY >= 0.025 && (horizontalInflections >= 1 || verticalInflections >= 1)) {
      isMatch = true;
      confidence = 0.91;
    }
  } else if (targetSign === '10') {
    if (avgRwY < 0.48 && deltaX >= 0.025 && horizontalInflections >= 1) {
      isMatch = true;
      confidence = 0.92;
    }
  }

  return {
    isMatch,
    predictedSign: isMatch ? targetSign : 'UNRECOGNIZED_GESTURE',
    confidence
  };
}

// --- Canvas Drawing Helpers ---

function drawPoseSkeleton(ctx, posePts, width, height) {
  if (!posePts || posePts.length < 17) return;

  const links = [
    [0, 1], [1, 2], [2, 3], [0, 4], [4, 5], [5, 6],
    [11, 12],
    [11, 13], [13, 15],
    [12, 14], [14, 16],
    [11, 23], [12, 24], [23, 24]
  ];

  ctx.lineWidth = 3;
  ctx.strokeStyle = '#10b981';
  ctx.fillStyle = '#34d399';

  for (const [u, v] of links) {
    if (posePts[u] && posePts[v]) {
      ctx.beginPath();
      ctx.moveTo(posePts[u].x * width, posePts[u].y * height);
      ctx.lineTo(posePts[v].x * width, posePts[v].y * height);
      ctx.stroke();
    }
  }

  for (let i = 0; i < posePts.length; i++) {
    if (posePts[i]) {
      const x = posePts[i].x * width;
      const y = posePts[i].y * height;
      ctx.beginPath();
      ctx.arc(x, y, i === 11 || i === 12 ? 5.5 : 3.5, 0, 2 * Math.PI);
      ctx.fill();
    }
  }
}

function drawHandMesh(ctx, handPts, color, width, height, isFullyTracked = true) {
  if (!handPts || handPts.length < 21) return;

  const fingerBones = [
    [0, 1], [1, 2], [2, 3], [3, 4],
    [0, 5], [5, 6], [6, 7], [7, 8],
    [0, 9], [9, 10], [10, 11], [11, 12],
    [0, 13], [13, 14], [14, 15], [15, 16],
    [0, 17], [17, 18], [18, 19], [19, 20],
    [5, 9], [9, 13], [13, 17]
  ];

  ctx.lineWidth = isFullyTracked ? 2.5 : 1.5;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;

  for (const [u, v] of fingerBones) {
    if (handPts[u] && handPts[v]) {
      ctx.beginPath();
      ctx.moveTo(handPts[u].x * width, handPts[u].y * height);
      ctx.lineTo(handPts[v].x * width, handPts[v].y * height);
      ctx.stroke();
    }
  }

  for (let i = 0; i < handPts.length; i++) {
    if (handPts[i]) {
      const isTip = [4, 8, 12, 16, 20].includes(i);
      ctx.beginPath();
      ctx.arc(handPts[i].x * width, handPts[i].y * height, isTip ? 4 : 2.5, 0, 2 * Math.PI);
      ctx.fill();
    }
  }
}

function drawFaceContours(ctx, facePts, width, height) {
  if (!facePts || facePts.length < 10) return;

  ctx.fillStyle = '#fbbf24';
  ctx.strokeStyle = 'rgba(251, 191, 36, 0.35)';
  ctx.lineWidth = 1;

  ctx.beginPath();
  for (let i = 0; i < facePts.length; i++) {
    const x = facePts[i].x * width;
    const y = facePts[i].y * height;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.closePath();
  ctx.stroke();

  for (let i = 0; i < facePts.length; i += 3) {
    ctx.beginPath();
    ctx.arc(facePts[i].x * width, facePts[i].y * height, 1.5, 0, 2 * Math.PI);
    ctx.fill();
  }
}

/**
 * Generates continuous skeletal trajectory with kinematic hand modulation for Simulator mode
 */
function generateVisualLandmarks(t, sign, width, height) {
  const midX = 0.5;

  const pose = [];
  for (let i = 0; i < 25; i++) pose.push({ x: 0, y: 0, z: 0 });

  pose[0] = { x: midX, y: 0.25 + Math.sin(t * 0.5) * 0.008, z: 0 };
  pose[11] = { x: midX - 0.2, y: 0.42, z: 0 };
  pose[12] = { x: midX + 0.2, y: 0.42, z: 0 };
  pose[23] = { x: midX - 0.14, y: 0.82, z: 0 };
  pose[24] = { x: midX + 0.14, y: 0.82, z: 0 };

  let lw = { x: midX - 0.15, y: 0.65, z: 0 };
  let rw = { x: midX + 0.15, y: 0.65, z: 0 };

  const amp = 1.0;

  if (sign === 'YES') {
    rw = { x: midX + 0.12, y: 0.50 + Math.sin(t * 8) * 0.045 * amp, z: 0 };
  } else if (sign === 'NO') {
    rw = { x: midX + 0.12 + Math.sin(t * 8) * 0.04 * amp, y: 0.50, z: 0 };
  } else if (sign === 'HELP') {
    lw = { x: midX - 0.04, y: 0.55 + Math.sin(t * 1.5) * 0.01 * amp, z: 0 };
    rw = { x: midX + 0.02, y: 0.52 - Math.abs(Math.sin(t * 3)) * 0.08 * amp, z: 0 };
  } else if (sign === 'DOCTOR') {
    lw = { x: midX - 0.1, y: 0.55, z: 0 };
    rw = { x: midX - 0.08 + Math.sin(t * 4) * 0.03 * amp, y: 0.54 + Math.cos(t * 4) * 0.02 * amp, z: 0 };
  } else if (sign === 'CHEST') {
    lw = { x: midX - 0.08, y: 0.48 + Math.sin(t * 2) * 0.005 * amp, z: 0 };
    rw = { x: midX + 0.08, y: 0.48 + Math.sin(t * 2) * 0.005 * amp, z: 0 };
  } else if (sign === 'PAIN') {
    lw = { x: midX - 0.12 + Math.sin(t * 6) * 0.04 * amp, y: 0.52, z: 0 };
    rw = { x: midX + 0.12 - Math.sin(t * 6) * 0.04 * amp, y: 0.52, z: 0 };
  } else if (sign === 'POLICE') {
    rw = { x: midX + 0.16, y: 0.24 + Math.sin(t * 2) * 0.02 * amp, z: 0 };
  } else if (sign === 'HOSPITAL') {
    lw = { x: midX - 0.02, y: 0.48, z: 0 };
    rw = { x: midX + 0.02 + Math.sin(t * 4) * 0.02 * amp, y: 0.48, z: 0 };
  } else if (sign === 'HELLO') {
    rw = { x: midX + 0.18 + Math.sin(t * 8) * 0.04 * amp, y: 0.22, z: 0 };
  } else if (sign === 'WATER') {
    rw = { x: midX + 0.05 + Math.sin(t * 4) * 0.02 * amp, y: 0.32, z: 0 };
  } else if (sign === '10') {
    rw = { x: midX + 0.14 + Math.sin(t * 10) * 0.03 * amp, y: 0.38, z: 0 };
  }

  pose[13] = { x: (pose[11].x + lw.x) / 2 - 0.05, y: (pose[11].y + lw.y) / 2 + 0.05, z: 0 };
  pose[14] = { x: (pose[12].x + rw.x) / 2 + 0.05, y: (pose[12].y + rw.y) / 2 + 0.05, z: 0 };
  pose[15] = lw;
  pose[16] = rw;

  const leftHand = [];
  const rightHand = [];
  for (let i = 0; i < 21; i++) {
    const fIdx = Math.floor(i / 4);
    const seg = (i % 4) + 1;
    leftHand.push({
      x: lw.x - 0.01 * fIdx,
      y: lw.y - 0.015 * seg + Math.sin(t * 3 + i) * 0.004 * amp,
      z: 0
    });
    rightHand.push({
      x: rw.x + 0.01 * fIdx,
      y: rw.y - 0.015 * seg + Math.cos(t * 3 + i) * 0.004 * amp,
      z: 0
    });
  }

  const face = [];
  for (let i = 0; i < 40; i++) {
    const angle = (i / 40) * Math.PI * 2;
    face.push({
      x: midX + 0.07 * Math.cos(angle),
      y: 0.25 + 0.09 * Math.sin(angle),
      z: 0
    });
  }

  return {
    pose,
    leftHand,
    rightHand,
    face,
    hasLeftHand: true,
    hasRightHand: true
  };
}
