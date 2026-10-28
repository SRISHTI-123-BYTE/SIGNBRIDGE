import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';

export default function LivingLogo() {
  const mountRef = useRef(null);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Dimensions
    const width = container.clientWidth || 700;
    const height = 180;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(-width / 2, width / 2, height / 2, -height / 2, 0.1, 1000);
    camera.position.z = 10;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Create high-res offscreen text canvas texture
    const textCanvas = document.createElement('canvas');
    textCanvas.width = 1024;
    textCanvas.height = 256;
    const ctx = textCanvas.getContext('2d');

    const drawTextTexture = () => {
      ctx.clearRect(0, 0, textCanvas.width, textCanvas.height);
      ctx.font = '900 110px "Plus Jakarta Sans", "Inter", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      // Gradient fill for text
      const grad = ctx.createLinearGradient(150, 0, 874, 0);
      grad.addColorStop(0.0, '#a78bfa'); // Purple 400
      grad.addColorStop(0.35, '#60a5fa'); // Blue 400
      grad.addColorStop(0.7, '#22d3ee'); // Cyan 400
      grad.addColorStop(1.0, '#34d399'); // Emerald 400

      ctx.fillStyle = grad;
      ctx.fillText('I S L   A I', textCanvas.width / 2, textCanvas.height / 2);
    };
    drawTextTexture();

    const texture = new THREE.CanvasTexture(textCanvas);
    texture.minFilter = THREE.LinearFilter;
    texture.magFilter = THREE.LinearFilter;

    // Custom GLSL Shader Material for Liquid / Glass Distortion
    const vertexShader = `
      uniform float uTime;
      uniform vec2 uMouse;
      uniform float uMouseRadius;
      uniform float uMouseStrength;
      
      varying vec2 vUv;
      varying vec3 vNormal;
      varying float vDistort;

      void main() {
        vUv = uv;
        vec3 pos = position;
        
        // Calculate distance from mouse in plane coordinates
        vec2 mPos = uMouse;
        float dist = distance(pos.xy, mPos);
        
        // Interactive fluid repulsion / attraction force
        float effect = smoothstep(uMouseRadius, 0.0, dist);
        
        // Wave ripple traveling outwards
        float ripple = sin(dist * 0.08 - uTime * 4.0) * effect * uMouseStrength * 12.0;
        
        // Displacement along Z and XY
        vec2 dir = normalize(pos.xy - mPos + 0.001);
        pos.xy += dir * effect * uMouseStrength * 18.0;
        pos.z += ripple + effect * uMouseStrength * 25.0;

        // Subtle ambient breathing liquid wave
        pos.z += sin(pos.x * 0.02 + uTime * 2.0) * cos(pos.y * 0.03 + uTime * 1.5) * 3.0;

        vDistort = effect * uMouseStrength;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `;

    const fragmentShader = `
      uniform sampler2D uTexture;
      uniform float uTime;
      uniform vec2 uMouse;
      uniform float uDistortStrength;
      
      varying vec2 vUv;
      varying float vDistort;

      void main() {
        // Liquid chromatic aberration / glass refraction
        vec2 uv = vUv;
        
        // Subtle ripple offset on UVs
        vec2 uvOffset = vec2(
          sin(uv.y * 20.0 + uTime * 3.0) * 0.003,
          cos(uv.x * 20.0 + uTime * 3.0) * 0.003
        ) * (1.0 + vDistort * 4.0);
        
        // Chromatic split
        float r = texture2D(uTexture, uv + uvOffset * 1.5).r;
        float g = texture2D(uTexture, uv + uvOffset * 0.5).g;
        float b = texture2D(uTexture, uv - uvOffset * 1.5).b;
        float a = texture2D(uTexture, uv).a;

        if (a < 0.05) discard;

        // Dynamic iridescent liquid shimmer
        vec3 liquidColor = vec3(r, g, b);
        float shimmer = sin(uv.x * 12.0 + uv.y * 8.0 + uTime * 2.5) * 0.15 + 0.85;
        liquidColor *= shimmer;

        // Highlight intensification on mouse interaction
        liquidColor += vec3(0.2, 0.4, 0.6) * vDistort;

        gl_FragColor = vec4(liquidColor, a * 0.95);
      }
    `;

    const uniforms = {
      uTexture: { value: texture },
      uTime: { value: 0 },
      uMouse: { value: new THREE.Vector2(-9999, -9999) },
      uMouseRadius: { value: 160.0 },
      uMouseStrength: { value: 0.0 },
      uDistortStrength: { value: 0.0 }
    };

    const planeGeometry = new THREE.PlaneGeometry(width * 0.9, (width * 0.9) * (256 / 1024), 64, 32);
    const material = new THREE.ShaderMaterial({
      vertexShader,
      fragmentShader,
      uniforms,
      transparent: true,
      depthTest: false
    });

    const mesh = new THREE.Mesh(planeGeometry, material);
    scene.add(mesh);

    // Mouse Tracking with Spring Damping
    const targetMouse = new THREE.Vector2(-9999, -9999);
    const currentMouse = new THREE.Vector2(-9999, -9999);
    let targetStrength = 0.0;
    let currentStrength = 0.0;

    const handleMouseMove = (e) => {
      const rect = container.getBoundingClientRect();
      const x = (e.clientX - rect.left) - width / 2;
      const y = -(e.clientY - rect.top) + height / 2;
      targetMouse.set(x, y);
      targetStrength = 1.0;
      setIsHovered(true);
    };

    const handleMouseLeave = () => {
      targetStrength = 0.0;
      setIsHovered(false);
    };

    container.addEventListener('mousemove', handleMouseMove);
    container.addEventListener('mouseleave', handleMouseLeave);

    // Resize Handler
    const handleResize = () => {
      if (!container) return;
      const newWidth = container.clientWidth || 700;
      renderer.setSize(newWidth, height);
      camera.left = -newWidth / 2;
      camera.right = newWidth / 2;
      camera.top = height / 2;
      camera.bottom = -height / 2;
      camera.updateProjectionMatrix();

      mesh.geometry.dispose();
      mesh.geometry = new THREE.PlaneGeometry(newWidth * 0.9, (newWidth * 0.9) * (256 / 1024), 64, 32);
    };

    window.addEventListener('resize', handleResize);

    // Animation Loop
    let animationFrameId;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Smooth mouse interpolation
      currentMouse.lerp(targetMouse, 0.12);
      currentStrength += (targetStrength - currentStrength) * 0.1;

      uniforms.uTime.value = elapsedTime;
      uniforms.uMouse.value.copy(currentMouse);
      uniforms.uMouseStrength.value = currentStrength;

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(animationFrameId);
      container.removeEventListener('mousemove', handleMouseMove);
      container.removeEventListener('mouseleave', handleMouseLeave);
      window.removeEventListener('resize', handleResize);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      planeGeometry.dispose();
      material.dispose();
      texture.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div className="relative w-full flex flex-col items-center justify-center select-none py-2">
      {/* Living Logo Three.js Canvas Container */}
      <div
        ref={mountRef}
        className="w-full max-w-2xl h-[170px] flex items-center justify-center cursor-pointer transition-transform duration-300 transform hover:scale-[1.02]"
        title="Interactive Living Logo: Move your cursor across the letters"
      />
    </div>
  );
}
