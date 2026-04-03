import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Neural Command Interface // BELHADJ", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #000008 !important;
    overflow: hidden !important;
    height: 100vh !important;
    width: 100vw !important;
}

#MainMenu, header[data-testid="stHeader"], footer,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], .stDeployButton,
[data-testid="collapsedControl"] { display: none !important; visibility: hidden !important; }

[data-testid="stAppViewContainer"] > div:first-child { padding: 0 !important; }
[data-testid="block-container"] { padding: 0 !important; max-width: 100vw !important; }
section[data-testid="stSidebar"] { display: none !important; }

.element-container, .stMarkdown { margin: 0 !important; padding: 0 !important; }
iframe { display: block; border: none; }
</style>
""", unsafe_allow_html=True)

components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: #000008;
    overflow: hidden;
    font-family: 'Share Tech Mono', monospace;
    width: 100vw; height: 100vh;
  }
  canvas#bg { position:fixed; top:0; left:0; z-index:0; }

  /* ── SCANLINE OVERLAY ── */
  .scanlines {
    position: fixed; top:0; left:0; width:100%; height:100%;
    background: repeating-linear-gradient(
      to bottom,
      transparent 0px, transparent 3px,
      rgba(0,243,255,0.018) 3px, rgba(0,243,255,0.018) 4px
    );
    pointer-events: none; z-index: 1;
    animation: scanmove 8s linear infinite;
  }
  @keyframes scanmove {
    0%   { background-position: 0 0; }
    100% { background-position: 0 100vh; }
  }

  /* ── VIGNETTE ── */
  .vignette {
    position: fixed; top:0; left:0; width:100%; height:100%;
    background: radial-gradient(ellipse at center, transparent 45%, rgba(0,0,8,0.82) 100%);
    pointer-events: none; z-index: 2;
  }

  /* ── DOSSIER PANEL ── */
  .dossier {
    position: fixed; left: 24px; top: 50%; transform: translateY(-50%);
    width: 270px; z-index: 20;
    background: rgba(0,10,30,0.62);
    border: 1px solid rgba(0,243,255,0.28);
    border-radius: 16px;
    backdrop-filter: blur(18px) saturate(180%);
    -webkit-backdrop-filter: blur(18px) saturate(180%);
    box-shadow: 0 0 40px rgba(0,243,255,0.12), inset 0 0 30px rgba(0,243,255,0.04);
    padding: 22px 18px 18px;
    overflow: hidden;
  }
  .dossier::before {
    content:'';
    position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, #00f3ff, #7000ff, transparent);
    animation: borderflow 3s linear infinite;
  }
  @keyframes borderflow {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
  }
  .dossier-tag {
    font-family: 'Orbitron', sans-serif;
    font-size: 9px; letter-spacing: 3px; color: #7000ff;
    text-transform: uppercase; margin-bottom: 14px;
  }
  .dossier-name {
    font-family: 'Orbitron', sans-serif;
    font-size: 15px; font-weight: 900;
    color: #00f3ff;
    text-shadow: 0 0 12px rgba(0,243,255,0.8);
    letter-spacing: 1px; margin-bottom: 5px;
  }
  .dossier-sub {
    font-size: 10px; color: rgba(0,243,255,0.5);
    letter-spacing: 2px; margin-bottom: 16px;
  }
  .dossier-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,243,255,0.3), transparent);
    margin: 12px 0;
  }
  .dossier-row {
    display: flex; align-items: flex-start; gap: 8px; margin-bottom: 9px;
  }
  .dossier-icon {
    font-size: 11px; color: #7000ff; margin-top: 1px; flex-shrink: 0; width: 14px;
  }
  .dossier-label {
    font-size: 9px; color: rgba(0,243,255,0.45); letter-spacing: 1.5px;
    text-transform: uppercase; margin-bottom: 2px;
  }
  .dossier-value {
    font-size: 10.5px; color: rgba(220,240,255,0.88); line-height: 1.4;
  }
  .badge {
    display: inline-block; font-size: 8px;
    padding: 2px 7px; border-radius: 3px; margin: 2px 2px 0 0;
    letter-spacing: 1px; text-transform: uppercase;
  }
  .badge-cyan  { background: rgba(0,243,255,0.12); border:1px solid rgba(0,243,255,0.35); color:#00f3ff; }
  .badge-violet{ background: rgba(112,0,255,0.12); border:1px solid rgba(112,0,255,0.4);  color:#b580ff; }
  .badge-red   { background: rgba(255,0,85,0.12);  border:1px solid rgba(255,0,85,0.35);  color:#ff6699; }

  /* ── MAIN CANVAS WRAPPER ── */
  .command-canvas {
    position: fixed; top:0; left:0; width:100%; height:100%;
    z-index: 5; pointer-events: none;
  }
  #threeCanvas {
    position: fixed; top:0; left:0;
    width:100vw; height:100vh; z-index: 3;
  }

  /* ── TOP HEADER BAR ── */
  .top-bar {
    position: fixed; top:0; left:0; right:0; height:52px;
    background: rgba(0,5,18,0.75);
    border-bottom: 1px solid rgba(0,243,255,0.15);
    backdrop-filter: blur(12px);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 28px; z-index: 25;
  }
  .top-bar-left {
    font-family: 'Orbitron', sans-serif;
    font-size: 12px; font-weight: 700; letter-spacing: 4px;
    color: #00f3ff; text-shadow: 0 0 12px rgba(0,243,255,0.7);
  }
  .top-bar-center {
    font-size: 10px; letter-spacing: 3px; color: rgba(0,243,255,0.4);
    text-transform: uppercase;
  }
  .top-bar-right {
    display: flex; align-items: center; gap: 18px;
  }
  .status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #ff0055; box-shadow: 0 0 8px #ff0055;
    animation: pulse-dot 1.2s ease-in-out infinite;
  }
  .status-dot.stable { background: #00f3ff; box-shadow: 0 0 8px #00f3ff; animation: none; }
  @keyframes pulse-dot {
    0%,100%{ opacity:1; } 50%{ opacity:0.2; }
  }
  .status-text { font-size: 9px; letter-spacing: 2px; color: #ff0055; }
  .status-text.stable { color: #00f3ff; }
  .clock { font-size: 10px; letter-spacing: 2px; color: rgba(0,243,255,0.5); }

  /* ── STAT OVERLAYS ── */
  .stats-right {
    position: fixed; right: 24px; top: 50%; transform: translateY(-50%);
    width: 210px; z-index: 20;
    display: flex; flex-direction: column; gap: 12px;
  }
  .stat-card {
    background: rgba(0,10,30,0.55);
    border: 1px solid rgba(0,243,255,0.18);
    border-radius: 10px;
    backdrop-filter: blur(14px);
    padding: 12px 15px;
    position: relative; overflow: hidden;
  }
  .stat-card::after {
    content:''; position:absolute; bottom:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent, var(--accent,#00f3ff), transparent);
  }
  .stat-title {
    font-size: 8px; letter-spacing: 2.5px; color: rgba(0,243,255,0.45);
    text-transform: uppercase; margin-bottom: 6px;
  }
  .stat-val {
    font-family: 'Orbitron', sans-serif;
    font-size: 22px; font-weight: 700;
    color: var(--accent, #00f3ff);
    text-shadow: 0 0 14px var(--accent,#00f3ff);
  }
  .stat-unit { font-size: 10px; color: rgba(0,243,255,0.4); margin-left: 4px; }
  .stat-bar-bg {
    margin-top: 6px; height: 3px; background: rgba(0,243,255,0.1); border-radius: 2px;
  }
  .stat-bar-fill {
    height: 100%; border-radius: 2px;
    background: linear-gradient(90deg, var(--accent,#00f3ff), rgba(0,243,255,0.3));
    transition: width 1.5s ease;
  }
  .stat-flicker { animation: flicker 2.3s infinite; }
  @keyframes flicker {
    0%,100%{opacity:1;} 92%{opacity:1;} 93%{opacity:0.4;} 94%{opacity:1;} 97%{opacity:0.7;} 98%{opacity:1;}
  }

  /* ── NEURAL ANCHOR BUTTON ── */
  .anchor-wrap {
    position: fixed; bottom: 90px; left: 50%; transform: translateX(-50%);
    z-index: 25; text-align: center;
  }
  #anchorBtn {
    font-family: 'Orbitron', sans-serif;
    font-size: 11px; font-weight: 700; letter-spacing: 4px;
    text-transform: uppercase;
    padding: 16px 44px;
    background: rgba(0,5,18,0.7);
    border: 1.5px solid #ff0055;
    border-radius: 4px; color: #ff0055;
    cursor: pointer; position: relative; overflow: hidden;
    text-shadow: 0 0 10px #ff0055;
    box-shadow: 0 0 24px rgba(255,0,85,0.25), inset 0 0 16px rgba(255,0,85,0.06);
    transition: all 0.4s ease;
    backdrop-filter: blur(10px);
  }
  #anchorBtn::before {
    content:''; position:absolute; top:-50%; left:-60%;
    width: 40%; height: 200%; background: rgba(255,0,85,0.08);
    transform: skewX(-20deg);
    animation: btn-sweep 3s linear infinite;
  }
  @keyframes btn-sweep {
    0%  { left:-60%; }
    100%{ left:160%; }
  }
  #anchorBtn.stable {
    border-color: #00f3ff; color: #00f3ff;
    text-shadow: 0 0 10px #00f3ff;
    box-shadow: 0 0 30px rgba(0,243,255,0.3), inset 0 0 20px rgba(0,243,255,0.06);
  }
  #anchorBtn.stable::before { background: rgba(0,243,255,0.08); }
  .anchor-label {
    font-size: 9px; letter-spacing: 3px; color: rgba(255,0,85,0.5);
    margin-top: 8px; text-transform: uppercase;
    transition: color 0.4s;
  }
  .anchor-label.stable { color: rgba(0,243,255,0.5); }

  /* ── SHOCKWAVE ── */
  .shockwave {
    position: fixed; top:50%; left:50%;
    transform: translate(-50%,-50%) scale(0);
    width: 10px; height: 10px; border-radius: 50%;
    border: 2px solid #00f3ff;
    pointer-events: none; z-index: 30;
    opacity: 0;
  }
  .shockwave.fire {
    animation: shockboom 1.2s ease-out forwards;
  }
  @keyframes shockboom {
    0%   { transform: translate(-50%,-50%) scale(0); opacity: 0.9; border-color:#ff0055; }
    40%  { border-color: #7000ff; }
    100% { transform: translate(-50%,-50%) scale(220); opacity: 0; border-color:#00f3ff; }
  }

  /* ── MAIN STATUS TEXT ── */
  .status-overlay {
    position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
    text-align: center; pointer-events: none; z-index: 10;
    margin-top: -120px;
  }
  .status-headline {
    font-family: 'Orbitron', sans-serif;
    font-size: 13px; font-weight: 900; letter-spacing: 6px;
    color: #ff0055; text-shadow: 0 0 20px #ff0055;
    text-transform: uppercase;
    animation: headline-flash 1.8s ease-in-out infinite;
    transition: all 0.6s ease;
  }
  .status-headline.stable {
    color: #00f3ff; text-shadow: 0 0 24px #00f3ff;
    animation: none;
  }
  @keyframes headline-flash {
    0%,100%{opacity:1;} 50%{opacity:0.3;}
  }
  .status-sub {
    font-size: 9px; letter-spacing: 4px; color: rgba(0,243,255,0.35);
    margin-top: 8px; text-transform: uppercase; transition: all 0.6s;
  }
  .status-sub.stable { color: rgba(0,243,255,0.6); }

  /* ── FOOTER ── */
  .cmd-footer {
    position: fixed; bottom: 0; left: 0; right: 0; height: 44px;
    background: rgba(0,5,18,0.75);
    border-top: 1px solid rgba(0,243,255,0.1);
    backdrop-filter: blur(12px);
    display: flex; align-items: center; justify-content: center;
    z-index: 25;
    font-size: 9px; letter-spacing: 2.5px; color: rgba(0,243,255,0.35);
    text-transform: uppercase;
  }
  .cmd-footer span { color: rgba(0,243,255,0.6); }

  /* ── CORNER DECORATORS ── */
  .corner {
    position: fixed; width: 30px; height: 30px; z-index: 22;
    opacity: 0.5;
  }
  .corner.tl { top:60px; left:10px; border-top:1.5px solid #00f3ff; border-left:1.5px solid #00f3ff; }
  .corner.tr { top:60px; right:10px; border-top:1.5px solid #00f3ff; border-right:1.5px solid #00f3ff; }
  .corner.bl { bottom:52px; left:10px; border-bottom:1.5px solid #00f3ff; border-left:1.5px solid #00f3ff; }
  .corner.br { bottom:52px; right:10px; border-bottom:1.5px solid #00f3ff; border-right:1.5px solid #00f3ff; }
</style>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap" rel="stylesheet"/>
</head>
<body>

<!-- BG Three.js Canvas -->
<canvas id="threeCanvas"></canvas>

<!-- Scanlines + Vignette -->
<div class="scanlines"></div>
<div class="vignette"></div>

<!-- Corners -->
<div class="corner tl"></div>
<div class="corner tr"></div>
<div class="corner bl"></div>
<div class="corner br"></div>

<!-- Top Bar -->
<div class="top-bar">
  <div class="top-bar-left">◈ NCI // VICS-LAB</div>
  <div class="top-bar-center">DRAM PRESSURE MANAGEMENT SYSTEM // ANU R&D NODE 7</div>
  <div class="top-bar-right">
    <div id="statusDot" class="status-dot"></div>
    <div id="statusText" class="status-text">ENTROPY CRITICAL</div>
    <div class="clock" id="clockEl">00:00:00</div>
  </div>
</div>

<!-- Dossier -->
<div class="dossier">
  <div class="dossier-tag">◈ Operator Dossier // Classified</div>
  <div class="dossier-name">Fatima Z. Belhadj</div>
  <div class="dossier-sub">ANU · MPhil Candidate · Systems Engineering</div>
  <div class="dossier-divider"></div>
  <div class="dossier-row">
    <div class="dossier-icon">▸</div>
    <div>
      <div class="dossier-label">Academic Standing</div>
      <div class="dossier-value">Ranked 1st · BSEMS Cohort 2024</div>
      <div style="margin-top:4px">
        <span class="badge badge-cyan">Summa Cum Laude</span>
        <span class="badge badge-violet">Honors Program</span>
      </div>
    </div>
  </div>
  <div class="dossier-row">
    <div class="dossier-icon">▸</div>
    <div>
      <div class="dossier-label">Academic Distinctions</div>
      <div class="dossier-value">President's List · Dean's List</div>
      <div style="margin-top:4px">
        <span class="badge badge-violet">Bilateral Exchange · Japan</span>
      </div>
    </div>
  </div>
  <div class="dossier-row">
    <div class="dossier-icon">▸</div>
    <div>
      <div class="dossier-label">Professional Grade</div>
      <div class="dossier-value">Top-Rated Plus Data Analyst</div>
      <div style="margin-top:4px">
        <span class="badge badge-cyan">Upwork Top 3%</span>
      </div>
    </div>
  </div>
  <div class="dossier-row">
    <div class="dossier-icon">▸</div>
    <div>
      <div class="dossier-label">Research Publications</div>
      <div class="dossier-value">3× Published · IEEE / Springer</div>
      <div style="margin-top:4px">
        <span class="badge badge-violet">Princeton Presenter</span>
      </div>
    </div>
  </div>
  <div class="dossier-row">
    <div class="dossier-icon">▸</div>
    <div>
      <div class="dossier-label">Awards</div>
      <div style="margin-top:4px">
        <span class="badge badge-red">SSE Stonehenge Award</span>
        <span class="badge badge-cyan">PGS Sustainability Africa</span>
      </div>
    </div>
  </div>
</div>

<!-- Center Status Text -->
<div class="status-overlay">
  <div class="status-headline" id="statusHeadline">⚠ CRITICAL ENTROPY LEAK</div>
  <div class="status-sub" id="statusSub">DRAM CUBE DESTABILIZED // AWAITING NEURAL ANCHOR</div>
</div>

<!-- Shockwave -->
<div class="shockwave" id="shockwave"></div>

<!-- Neural Anchor Button -->
<div class="anchor-wrap">
  <button id="anchorBtn" onclick="engageAnchor()">⬡ ENGAGE NEURAL ANCHOR</button>
  <div class="anchor-label" id="anchorLabel">BELHADJ CONSTRAINT :: DISENGAGED</div>
</div>

<!-- Stats Right -->
<div class="stats-right">
  <div class="stat-card stat-flicker" style="--accent:#ff0055">
    <div class="stat-title">DRAM Spillage Index</div>
    <div><span class="stat-val" id="stat1">87.4</span><span class="stat-unit">%</span></div>
    <div class="stat-bar-bg"><div class="stat-bar-fill" id="bar1" style="width:87.4%; background:linear-gradient(90deg,#ff0055,rgba(255,0,85,0.3))"></div></div>
  </div>
  <div class="stat-card" style="--accent:#7000ff">
    <div class="stat-title">Write-Rationing Efficiency</div>
    <div><span class="stat-val" id="stat2">12.1</span><span class="stat-unit">%</span></div>
    <div class="stat-bar-bg"><div class="stat-bar-fill" id="bar2" style="width:12.1%; background:linear-gradient(90deg,#7000ff,rgba(112,0,255,0.3))"></div></div>
  </div>
  <div class="stat-card stat-flicker" style="--accent:#ff0055">
    <div class="stat-title">Latent Trajectory Variance</div>
    <div><span class="stat-val" id="stat3">±3.82</span><span class="stat-unit">σ</span></div>
    <div class="stat-bar-bg"><div class="stat-bar-fill" id="bar3" style="width:76%; background:linear-gradient(90deg,#ff0055,rgba(255,0,85,0.3))"></div></div>
  </div>
  <div class="stat-card" style="--accent:#00f3ff">
    <div class="stat-title">Neural Coherence</div>
    <div><span class="stat-val" id="stat4">4.3</span><span class="stat-unit">%</span></div>
    <div class="stat-bar-bg"><div class="stat-bar-fill" id="bar4" style="width:4.3%; background:linear-gradient(90deg,#00f3ff,rgba(0,243,255,0.3))"></div></div>
  </div>
</div>

<!-- Footer -->
<div class="cmd-footer">
  Architecture proposed by <span>&nbsp;F.Z. Belhadj&nbsp;</span> | ANU MPhil Candidate | <span>&nbsp;Systems Engineering Apex&nbsp;</span> | VICS Lab · Shoaib Akram
</div>

<!-- Three.js CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
// ── STATE ──
let isStable = false;
let mouseX = 0, mouseY = 0;
let targetRotX = 0, targetRotY = 0;
const W = window.innerWidth, H = window.innerHeight;

// ── THREE.JS SETUP ──
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('threeCanvas'), antialias: true, alpha: true });
renderer.setSize(W, H);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0x000008, 1);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, W/H, 0.1, 2000);
camera.position.set(0, 0, 280);

// ── NEBULA BACKGROUND ──
const bgGeo = new THREE.PlaneGeometry(2000, 2000);
const bgMat = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 },
    uPressure: { value: 1.0 }
  },
  vertexShader: `
    varying vec2 vUv;
    void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }
  `,
  fragmentShader: `
    uniform float uTime;
    uniform float uPressure;
    varying vec2 vUv;
    float rand(vec2 c){ return fract(sin(dot(c.xy, vec2(12.9898,78.233))) * 43758.5453); }
    float noise(vec2 p){
      vec2 i=floor(p), f=fract(p);
      float a=rand(i), b=rand(i+vec2(1,0)), c2=rand(i+vec2(0,1)), d=rand(i+vec2(1,1));
      vec2 u=f*f*(3.0-2.0*f);
      return mix(mix(a,b,u.x),mix(c2,d,u.x),u.y);
    }
    void main(){
      vec2 uv = vUv - 0.5;
      float dist = length(uv);
      float n1 = noise(uv * 3.0 + uTime * 0.06);
      float n2 = noise(uv * 6.0 - uTime * 0.04);
      float nebula = n1 * 0.6 + n2 * 0.4;
      vec3 col1 = mix(vec3(0.0,0.0,0.03), vec3(0.28,0.0,1.0)*0.18, nebula);
      vec3 coldark = mix(col1, vec3(1.0,0.0,0.33)*0.12 * uPressure, n2 * 0.5);
      float stars = step(0.985, rand(vUv * 800.0 + floor(uTime*0.1)));
      vec3 final = coldark + vec3(stars) * 0.6;
      gl_FragColor = vec4(final, 1.0);
    }
  `,
  side: THREE.FrontSide,
  depthWrite: false
});
const bgMesh = new THREE.Mesh(bgGeo, bgMat);
bgMesh.position.z = -500;
scene.add(bgMesh);

// ── PARTICLE CUBE ──
const N = 2000;
const geo = new THREE.BufferGeometry();
const positions = new Float32Array(N * 3);
const colors    = new Float32Array(N * 3);
const sizes     = new Float32Array(N);
const basePos   = new Float32Array(N * 3); // crystal target
const randomPos = new Float32Array(N * 3); // chaos positions
const velocities= new Float32Array(N * 3);

// Build crystal cube lattice (±80 box)
const side = Math.cbrt(N) | 0; // ~12
let idx = 0;
for(let x=0; x<side && idx<N; x++)
  for(let y=0; y<side && idx<N; y++)
    for(let z=0; z<side && idx<N; z++){
      const px = (x/(side-1)-0.5)*160;
      const py = (y/(side-1)-0.5)*160;
      const pz = (z/(side-1)-0.5)*160;
      basePos[idx*3]   = px;
      basePos[idx*3+1] = py;
      basePos[idx*3+2] = pz;
      idx++;
    }
// Fill leftover randomly on cube surface
for(let i=idx; i<N; i++){
  const face = Math.floor(Math.random()*6);
  let px,py,pz;
  const r=()=>(Math.random()-0.5)*160;
  if(face===0){px=80;py=r();pz=r();}
  else if(face===1){px=-80;py=r();pz=r();}
  else if(face===2){py=80;px=r();pz=r();}
  else if(face===3){py=-80;px=r();pz=r();}
  else if(face===4){pz=80;px=r();py=r();}
  else{pz=-80;px=r();py=r();}
  basePos[i*3]=px; basePos[i*3+1]=py; basePos[i*3+2]=pz;
}

// Random explosive positions
for(let i=0; i<N; i++){
  const theta = Math.random()*Math.PI*2;
  const phi   = Math.random()*Math.PI;
  const r2    = 80 + Math.random()*220;
  randomPos[i*3]   = r2*Math.sin(phi)*Math.cos(theta);
  randomPos[i*3+1] = r2*Math.sin(phi)*Math.sin(theta);
  randomPos[i*3+2] = r2*Math.cos(phi);
  velocities[i*3]   = (Math.random()-0.5)*0.4;
  velocities[i*3+1] = (Math.random()-0.5)*0.4;
  velocities[i*3+2] = (Math.random()-0.5)*0.4;
}

// Init at random
for(let i=0;i<N*3;i++) positions[i] = randomPos[i];

// Colors: red for chaos, cyan for stable
for(let i=0;i<N;i++){
  colors[i*3]   = 1.0;
  colors[i*3+1] = 0.0;
  colors[i*3+2] = 0.2;
  sizes[i] = 1.5 + Math.random()*2.0;
}

geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geo.setAttribute('color',    new THREE.BufferAttribute(colors,    3));
geo.setAttribute('size',     new THREE.BufferAttribute(sizes,     1));

const particleMat = new THREE.ShaderMaterial({
  uniforms: {
    uTime:    { value: 0 },
    uStable:  { value: 0.0 }
  },
  vertexShader: `
    attribute float size;
    attribute vec3 color;
    varying vec3 vColor;
    uniform float uTime;
    uniform float uStable;
    void main(){
      vColor = color;
      vec4 mv = modelViewMatrix * vec4(position, 1.0);
      float s = size * (1.0 + 0.3*sin(uTime*4.0 + position.x));
      gl_PointSize = s * (300.0 / -mv.z);
      gl_Position = projectionMatrix * mv;
    }
  `,
  fragmentShader: `
    varying vec3 vColor;
    void main(){
      float d = length(gl_PointCoord - vec2(0.5));
      if(d > 0.5) discard;
      float glow = 1.0 - d*2.0;
      glow = pow(glow, 1.8);
      gl_FragColor = vec4(vColor * glow, glow * 0.95);
    }
  `,
  vertexColors: true,
  transparent: true,
  depthWrite: false,
  blending: THREE.AdditiveBlending
});

const particles = new THREE.Points(geo, particleMat);
scene.add(particles);

// ── CORE GLOW SPHERE ──
const coreGeo = new THREE.SphereGeometry(14, 32, 32);
const coreMat = new THREE.MeshBasicMaterial({ color: 0xff0055, transparent: true, opacity: 0.85 });
const core = new THREE.Mesh(coreGeo, coreMat);
scene.add(core);

const coreGlowGeo = new THREE.SphereGeometry(22, 32, 32);
const coreGlowMat = new THREE.MeshBasicMaterial({ color: 0xff0033, transparent: true, opacity: 0.2, side: THREE.BackSide });
const coreGlow = new THREE.Mesh(coreGlowGeo, coreGlowMat);
scene.add(coreGlow);

// ── CUBE WIREFRAME (stable) ──
const wireGeo = new THREE.BoxGeometry(162, 162, 162);
const wireMat = new THREE.MeshBasicMaterial({ color: 0x00f3ff, wireframe: true, transparent: true, opacity: 0 });
const wireBox = new THREE.Mesh(wireGeo, wireMat);
scene.add(wireBox);

// ── RING DECORATORS ──
function makeRing(r, axis){
  const rGeo = new THREE.TorusGeometry(r, 0.6, 8, 80);
  const rMat = new THREE.MeshBasicMaterial({ color: 0x7000ff, transparent: true, opacity: 0.35 });
  const ring = new THREE.Mesh(rGeo, rMat);
  if(axis==='x') ring.rotation.x = Math.PI/2;
  if(axis==='z') ring.rotation.z = Math.PI/3;
  scene.add(ring); return ring;
}
const ring1 = makeRing(100,'y');
const ring2 = makeRing(120,'x');
const ring3 = makeRing(90, 'z');

// ── CLOCK ──
function updateClock(){
  const d=new Date();
  document.getElementById('clockEl').textContent =
    String(d.getHours()).padStart(2,'0')+':'+
    String(d.getMinutes()).padStart(2,'0')+':'+
    String(d.getSeconds()).padStart(2,'0');
}
setInterval(updateClock, 1000);

// ── MOUSE ──
document.addEventListener('mousemove', e=>{
  mouseX = (e.clientX/W - 0.5)*2;
  mouseY = (e.clientY/H - 0.5)*2;
});

// ── ENGAGE ANCHOR ──
let transitionProgress = 0;
let transitionActive   = false;

function engageAnchor(){
  if(transitionActive) return;
  isStable = !isStable;
  transitionActive = true; transitionProgress = 0;

  // Shockwave
  const sw = document.getElementById('shockwave');
  sw.classList.remove('fire');
  void sw.offsetWidth;
  sw.classList.add('fire');

  const btn    = document.getElementById('anchorBtn');
  const label  = document.getElementById('anchorLabel');
  const dot    = document.getElementById('statusDot');
  const stText = document.getElementById('statusText');
  const hl     = document.getElementById('statusHeadline');
  const sub    = document.getElementById('statusSub');

  if(isStable){
    btn.textContent    = '⬡ DISENGAGE NEURAL ANCHOR';
    btn.classList.add('stable');
    label.textContent  = 'BELHADJ CONSTRAINT :: ENGAGED';
    label.classList.add('stable');
    dot.classList.add('stable');
    stText.textContent = 'DRAM PRESSURE NOMINAL';
    stText.classList.add('stable');
    hl.textContent     = '✦ DRAM PRESSURE STABILIZED';
    hl.classList.add('stable');
    sub.textContent    = 'BELHADJ CONSTRAINT ACTIVE // CRYSTALLINE COHERENCE ACHIEVED';
    sub.classList.add('stable');
    stabilizeStats();
  } else {
    btn.textContent    = '⬡ ENGAGE NEURAL ANCHOR';
    btn.classList.remove('stable');
    label.textContent  = 'BELHADJ CONSTRAINT :: DISENGAGED';
    label.classList.remove('stable');
    dot.classList.remove('stable');
    stText.textContent = 'ENTROPY CRITICAL';
    stText.classList.remove('stable');
    hl.textContent     = '⚠ CRITICAL ENTROPY LEAK';
    hl.classList.remove('stable');
    sub.textContent    = 'DRAM CUBE DESTABILIZED // AWAITING NEURAL ANCHOR';
    sub.classList.remove('stable');
    destabilizeStats();
  }
}

// ── STAT ANIMATIONS ──
function animateStat(id, target, suffix, barId, barPct){
  const el  = document.getElementById(id);
  const bar = document.getElementById(barId);
  const start = parseFloat(el.textContent);
  const dur = 2000; const t0 = Date.now();
  function step(){
    const prog = Math.min((Date.now()-t0)/dur, 1);
    const ease = 1-Math.pow(1-prog,3);
    const cur  = start + (target-start)*ease;
    el.textContent = (typeof target==='number'? cur.toFixed(typeof suffix==='string'&&suffix.includes('σ')?2:1) : target)+suffix;
    if(bar) bar.style.width = (barPct * ease + (parseFloat(bar.style.width)||0)*(1-ease)).toFixed(1)+'%';
    if(prog<1) requestAnimationFrame(step);
  }
  step();
}
function stabilizeStats(){
  document.getElementById('stat3').textContent='±3.82';
  animateStat('stat1', 3.2, '',  'bar1', 3.2);
  animateStat('stat2', 98.7,'',  'bar2', 98.7);
  animateStat('stat4', 99.1,'',  'bar4', 99.1);
  setTimeout(()=>{ document.getElementById('stat3').textContent='±0.02'; document.getElementById('bar3').style.width='2%'; },1200);
  document.getElementById('bar1').style.background='linear-gradient(90deg,#00f3ff,rgba(0,243,255,0.3))';
  document.getElementById('bar3').style.background='linear-gradient(90deg,#00f3ff,rgba(0,243,255,0.3))';
}
function destabilizeStats(){
  animateStat('stat1',87.4,'', 'bar1',87.4);
  animateStat('stat2',12.1,'', 'bar2',12.1);
  animateStat('stat4', 4.3,'', 'bar4', 4.3);
  setTimeout(()=>{ document.getElementById('stat3').textContent='±3.82'; document.getElementById('bar3').style.width='76%'; },600);
  document.getElementById('bar1').style.background='linear-gradient(90deg,#ff0055,rgba(255,0,85,0.3))';
  document.getElementById('bar3').style.background='linear-gradient(90deg,#ff0055,rgba(255,0,85,0.3))';
}

// ── ANIMATION LOOP ──
let clock = 0;
function animate(){
  requestAnimationFrame(animate);
  clock += 0.016;
  bgMat.uniforms.uTime.value = clock;
  particleMat.uniforms.uTime.value = clock;

  // Smooth camera tilt from mouse
  targetRotY += (mouseX * 0.3 - targetRotY) * 0.04;
  targetRotX += (mouseY * 0.2 - targetRotX) * 0.04;
  particles.rotation.y += 0.003 + targetRotY * 0.005;
  particles.rotation.x += 0.001 + targetRotX * 0.005;
  wireBox.rotation.y = particles.rotation.y;
  wireBox.rotation.x = particles.rotation.x;
  ring1.rotation.y   = clock * 0.4;
  ring2.rotation.z   = clock * 0.3;
  ring3.rotation.x   = clock * 0.25;

  // Transition
  if(transitionActive){
    transitionProgress = Math.min(transitionProgress + 0.018, 1);
    if(transitionProgress >= 1) transitionActive = false;
  }
  const t = isStable ? transitionProgress : 1-transitionProgress;
  const ease = t<0.5 ? 4*t*t*t : 1-Math.pow(-2*t+2,3)/2;

  for(let i=0;i<N;i++){
    const tx = basePos[i*3],   ty = basePos[i*3+1],   tz = basePos[i*3+2];
    const cx = randomPos[i*3], cy = randomPos[i*3+1], cz = randomPos[i*3+2];

    // Chaos drift
    if(!isStable || transitionActive){
      randomPos[i*3]   += velocities[i*3]   * (1-ease);
      randomPos[i*3+1] += velocities[i*3+1] * (1-ease);
      randomPos[i*3+2] += velocities[i*3+2] * (1-ease);
      // Bounce
      for(let ax=0;ax<3;ax++){
        if(Math.abs(randomPos[i*3+ax])>320){ velocities[i*3+ax]*=-1; }
      }
      // Shiver
      const shiver = (1-ease)*2.0;
      positions[i*3]   = tx*(ease) + (randomPos[i*3]  +  (Math.random()-0.5)*shiver)*(1-ease);
      positions[i*3+1] = ty*(ease) + (randomPos[i*3+1]+ (Math.random()-0.5)*shiver)*(1-ease);
      positions[i*3+2] = tz*(ease) + (randomPos[i*3+2]+ (Math.random()-0.5)*shiver)*(1-ease);
    } else {
      // Stable: slight breathe
      const breathe = Math.sin(clock*1.5 + i*0.1)*0.4;
      positions[i*3]   = tx + breathe*(tx/160);
      positions[i*3+1] = ty + breathe*(ty/160);
      positions[i*3+2] = tz + breathe*(tz/160);
    }

    // Color: red→cyan
    const rt = Math.min(ease + (Math.random()-0.5)*0.1, 1);
    colors[i*3]   = 1.0 - rt;           // R
    colors[i*3+1] = rt * 0.95;          // G
    colors[i*3+2] = 0.2 + rt * 0.8;    // B
    sizes[i]      = (1.5 + Math.random()*2.0) * (isStable ? 1.0 : 1.0+Math.random()*0.5);
  }

  geo.attributes.position.needsUpdate = true;
  geo.attributes.color.needsUpdate    = true;
  geo.attributes.size.needsUpdate     = true;

  // Core sphere color
  coreMat.color.setRGB(1-ease, ease*0.95, 0.2+ease*0.8);
  coreGlowMat.color.setRGB(1-ease, ease*0.95, 0.2+ease*0.8);
  coreGlow.scale.setScalar(1 + 0.15*Math.sin(clock*3));
  core.scale.setScalar(1 + 0.08*Math.sin(clock*5));

  // Wire box
  wireMat.opacity = ease * 0.45;
  bgMat.uniforms.uPressure.value = 1-ease;

  renderer.render(scene, camera);
}

window.addEventListener('resize', ()=>{
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
});

animate();
</script>
</body>
</html>
""", height=1080, scrolling=False)
