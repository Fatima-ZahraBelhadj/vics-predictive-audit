import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import random
import time

st.set_page_config(
    page_title="VICS // BELHADJ AUDIT",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  GLOBAL CSS INJECTION — YEAR 2080 GLASSMORPHISM
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

/* ── PURGE DEFAULT STREAMLIT CHROME ── */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── ROOT VOID ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main {
    background: #050505 !important;
    color: #c8d6e5 !important;
    font-family: 'Rajdhani', sans-serif !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #050505; }
::-webkit-scrollbar-thumb { background: #00f3ff44; border-radius: 2px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07090f 0%, #0a0e1a 60%, #050505 100%) !important;
    border-right: 1px solid #00f3ff22 !important;
    box-shadow: 4px 0 40px #00f3ff0a !important;
}
[data-testid="stSidebar"] * { font-family: 'Share Tech Mono', monospace !important; }
[data-testid="stSidebarContent"] { padding: 1rem 1.2rem !important; }

/* ── MAIN CONTENT PADDING ── */
[data-testid="stMainBlockContainer"] { padding: 1.5rem 2.5rem !important; }

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: rgba(0, 243, 255, 0.03) !important;
    border: 1px solid #00f3ff18 !important;
    border-radius: 2px !important;
    padding: 1.2rem 1.5rem !important;
    backdrop-filter: blur(8px) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.18em !important;
    color: #00f3ff99 !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

/* ── TOGGLE ── */
[data-testid="stToggle"] label {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.12em !important;
    color: #00f3ffcc !important;
}
[data-testid="stToggle"] span[data-checked="true"] {
    background-color: #00f3ff !important;
    box-shadow: 0 0 18px #00f3ff88 !important;
}
[data-testid="stToggle"] span[data-checked="false"] {
    background-color: #ff003c !important;
    box-shadow: 0 0 18px #ff003c88 !important;
}

/* ── HORIZONTAL RULES ── */
hr { border-color: #00f3ff15 !important; margin: 0.8rem 0 !important; }

/* ── DIVIDER CLASS ── */
.vics-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #00f3ff44, transparent);
    margin: 0.6rem 0;
}

/* ── SCANLINE OVERLAY ── */
[data-testid="stApp"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,243,255,0.012) 2px,
        rgba(0,243,255,0.012) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── CORNER DECORATION ── */
[data-testid="stApp"]::after {
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 200px; height: 200px;
    background: radial-gradient(circle at top left, #00f3ff08 0%, transparent 70%);
    pointer-events: none;
    z-index: 9998;
}

/* ── COLUMNS GAP ── */
[data-testid="stHorizontalBlock"] { gap: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR — APPLICANT PROFILE
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="
        font-family:'Share Tech Mono',monospace;
        color:#00f3ff;
        font-size:0.68rem;
        letter-spacing:0.22em;
        text-align:center;
        padding:0.6rem 0.4rem;
        border:1px solid #00f3ff33;
        background:rgba(0,243,255,0.04);
        border-radius:2px;
        text-shadow:0 0 12px #00f3ffaa;
        margin-bottom:1.2rem;
    ">[ SECURE UPLINK // APPLICANT PROFILE ]</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background:rgba(0,243,255,0.03);
        border:1px solid #00f3ff1a;
        border-radius:3px;
        padding:1rem 1rem 0.8rem;
        font-family:'Share Tech Mono',monospace;
    ">
      <!-- NAME BLOCK -->
      <div style="margin-bottom:0.9rem;">
        <div style="color:#00f3ff55;font-size:0.55rem;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.25rem;">// IDENTITY NODE</div>
        <div style="color:#e8f4ff;font-size:1.05rem;font-weight:700;font-family:'Orbitron',sans-serif;letter-spacing:0.06em;text-shadow:0 0 10px #00f3ff44;">FATIMA Z. BELHADJ</div>
      </div>

      <div style="height:1px;background:linear-gradient(90deg,transparent,#00f3ff33,transparent);margin-bottom:0.9rem;"></div>

      <!-- ACADEMIC -->
      <div style="margin-bottom:0.75rem;">
        <div style="color:#00f3ff55;font-size:0.52rem;letter-spacing:0.18em;margin-bottom:0.35rem;">// ACADEMIC TELEMETRY</div>
        <div style="color:#aac8e0;font-size:0.7rem;line-height:1.8;">
          <span style="color:#00f3ffaa;">▸</span> BSEMS (2024) — <span style="color:#00f3ff;">Summa Cum Laude</span><br>
          <span style="color:#00f3ffaa;">▸</span> Cohort Rank: <span style="color:#00f3ff;">1st / Class</span><br>
          <span style="color:#00f3ffaa;">▸</span> UHP Graduate — President's &amp; Dean's Lists
        </div>
      </div>

      <div style="height:1px;background:linear-gradient(90deg,transparent,#00f3ff22,transparent);margin-bottom:0.75rem;"></div>

      <!-- GLOBAL EXP -->
      <div style="margin-bottom:0.75rem;">
        <div style="color:#00f3ff55;font-size:0.52rem;letter-spacing:0.18em;margin-bottom:0.35rem;">// GLOBAL VECTOR</div>
        <div style="color:#aac8e0;font-size:0.7rem;line-height:1.8;">
          <span style="color:#00f3ffaa;">▸</span> Bilateral Exchange Scholar<br>
          &nbsp;&nbsp;&nbsp;<span style="color:#8899bb;font-size:0.65rem;">Kansai Gaidai Univ., Japan</span>
        </div>
      </div>

      <div style="height:1px;background:linear-gradient(90deg,transparent,#00f3ff22,transparent);margin-bottom:0.75rem;"></div>

      <!-- INDUSTRY -->
      <div style="margin-bottom:0.75rem;">
        <div style="color:#00f3ff55;font-size:0.52rem;letter-spacing:0.18em;margin-bottom:0.35rem;">// INDUSTRY UPLINK</div>
        <div style="color:#aac8e0;font-size:0.7rem;line-height:1.8;">
          <span style="color:#00f3ffaa;">▸</span> Freelance Data Analyst<br>
          &nbsp;&nbsp;&nbsp;<span style="color:#00f3ff;">Upwork Top-Rated Plus</span><br>
          &nbsp;&nbsp;&nbsp;<span style="color:#8899bb;font-size:0.65rem;">Top 3% Globally</span>
        </div>
      </div>

      <div style="height:1px;background:linear-gradient(90deg,transparent,#00f3ff22,transparent);margin-bottom:0.75rem;"></div>

      <!-- RESEARCH -->
      <div style="margin-bottom:0.75rem;">
        <div style="color:#00f3ff55;font-size:0.52rem;letter-spacing:0.18em;margin-bottom:0.35rem;">// RESEARCH NODES</div>
        <div style="color:#aac8e0;font-size:0.7rem;line-height:1.8;">
          <span style="color:#00f3ffaa;">▸</span> <span style="color:#00f3ff;">3× Published</span> — IEEE / Springer<br>
          <span style="color:#00f3ffaa;">▸</span> Presenter — <span style="color:#00f3ff;">Princeton Univ.</span><br>
          &nbsp;&nbsp;&nbsp;<span style="color:#8899bb;font-size:0.65rem;">(Virtual, Invited)</span>
        </div>
      </div>

      <div style="height:1px;background:linear-gradient(90deg,transparent,#00f3ff22,transparent);margin-bottom:0.75rem;"></div>

      <!-- AWARDS -->
      <div style="margin-bottom:0.4rem;">
        <div style="color:#00f3ff55;font-size:0.52rem;letter-spacing:0.18em;margin-bottom:0.35rem;">// COMMENDATION LOG</div>
        <div style="color:#aac8e0;font-size:0.7rem;line-height:1.8;">
          <span style="color:#00f3ffaa;">▸</span> SSE Stonehenge Award<br>
          &nbsp;&nbsp;&nbsp;<span style="color:#8899bb;font-size:0.65rem;">Best Undergrad Research</span><br>
          <span style="color:#00f3ffaa;">▸</span> 2022 PGS Sustainability Award<br>
          &nbsp;&nbsp;&nbsp;<span style="color:#8899bb;font-size:0.65rem;">Africa Regional</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin:1.2rem 0 0.6rem;height:1px;background:linear-gradient(90deg,transparent,#ff003c44,transparent);'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background:rgba(255,0,60,0.05);
        border:1px solid #ff003c2a;
        border-left:2px solid #ff003c88;
        border-radius:2px;
        padding:0.85rem 0.9rem;
        font-family:'Rajdhani',sans-serif;
        font-size:0.75rem;
        color:#c8a0a8;
        line-height:1.65;
    ">
    <span style="color:#ff003ccc;font-family:'Share Tech Mono',monospace;font-size:0.6rem;letter-spacing:0.15em;display:block;margin-bottom:0.5rem;">// DIRECT TRANSMISSION → DR. AKRAM</span>
    GenAI memory bottlenecks are fundamentally <span style="color:#ff6080;">data pipeline optimization failures</span>. By applying the predictive computational modeling frameworks I use for global clients to your <span style="color:#00f3ff;">VICS Hybrid-NVM architecture</span>, we can <span style="color:#ff6080;">mathematically constrain latent drift</span>. The terminal below runs a live JavaScript physics simulation of this predictive constraint on <span style="color:#00f3ff;">DRAM state-space</span>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        margin-top:1.2rem;
        font-family:'Share Tech Mono',monospace;
        font-size:0.55rem;
        color:#00f3ff33;
        letter-spacing:0.15em;
        text-align:center;
    ">SYS.CLOCK: ANU-VICS-LAB // NODE-ACTIVE<br>ENC: AES-256 // UPLINK SECURED</div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN INTERFACE
# ─────────────────────────────────────────────

# ── GLOWING HEADER ──
st.markdown("""
<div style="text-align:center;padding:1.5rem 0 0.5rem;position:relative;">
  <div style="
      font-family:'Orbitron',sans-serif;
      font-size:1.6rem;
      font-weight:900;
      letter-spacing:0.18em;
      color:#00f3ff;
      text-shadow:
        0 0 10px #00f3ffcc,
        0 0 30px #00f3ff88,
        0 0 60px #00f3ff44,
        0 0 100px #00f3ff22;
      line-height:1.2;
  ">VICS HYBRID-MEMORY</div>
  <div style="
      font-family:'Orbitron',sans-serif;
      font-size:0.9rem;
      font-weight:600;
      letter-spacing:0.35em;
      color:#00f3ff88;
      margin-top:0.3rem;
      text-shadow:0 0 20px #00f3ff55;
  ">// KINETIC ENTROPY SIMULATOR //</div>
  <div style="
      position:absolute;top:50%;left:50%;
      transform:translate(-50%,-50%);
      width:600px;height:100px;
      background:radial-gradient(ellipse, #00f3ff08 0%, transparent 70%);
      pointer-events:none;
  "></div>
</div>
<div style="height:1px;background:linear-gradient(90deg,transparent,#00f3ff66,transparent);margin:0.5rem 0 1.2rem;"></div>
""", unsafe_allow_html=True)

# ── STATUS BAR ──
st.markdown("""
<div style="
    display:flex;justify-content:space-between;align-items:center;
    font-family:'Share Tech Mono',monospace;font-size:0.6rem;
    color:#00f3ff55;letter-spacing:0.14em;
    border:1px solid #00f3ff12;
    background:rgba(0,243,255,0.02);
    padding:0.35rem 1rem;border-radius:2px;
    margin-bottom:1.2rem;
">
  <span>SYS.CORE: ONLINE</span>
  <span>NODE: ANU-VICS-HYBRID-NVM-v4.7</span>
  <span>OPERATOR: BELHADJ.FZ</span>
  <span>STATUS: AWAITING DIRECTIVE</span>
</div>
""", unsafe_allow_html=True)

# ── TOGGLE ──
col_tog_l, col_tog_c, col_tog_r = st.columns([1, 2, 1])
with col_tog_c:
    st.markdown("""
    <div style="
        text-align:center;
        font-family:'Share Tech Mono',monospace;
        font-size:0.62rem;
        color:#00f3ff66;
        letter-spacing:0.18em;
        margin-bottom:0.4rem;
    ">▼  DIRECTIVE CONTROL  ▼</div>
    """, unsafe_allow_html=True)
    algo_active = st.toggle("[ INITIATE PREDICTIVE DATA ALGORITHM ]", value=False)

st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  JAVASCRIPT PHYSICS SIMULATION
# ─────────────────────────────────────────────
toggle_state = "true" if algo_active else "false"

SIMULATION_HTML = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    background: #050505;
    overflow: hidden;
    width: 100%;
    height: 100%;
    font-family: 'Share Tech Mono', monospace;
  }}
  canvas {{
    display: block;
    width: 100%;
    height: 100%;
  }}
  #overlay {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
  }}
  #status-tag {{
    position: absolute;
    top: 14px; left: 50%;
    transform: translateX(-50%);
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.22em;
    padding: 5px 22px;
    border-radius: 2px;
    border: 1px solid;
    transition: all 0.6s ease;
  }}
  #hud-tl {{
    position: absolute; top: 12px; left: 16px;
    font-size: 9px; letter-spacing: 0.14em;
    opacity: 0.5; line-height: 1.8;
  }}
  #hud-tr {{
    position: absolute; top: 12px; right: 16px;
    font-size: 9px; letter-spacing: 0.14em;
    opacity: 0.5; text-align: right; line-height: 1.8;
  }}
  #hud-bl {{
    position: absolute; bottom: 12px; left: 16px;
    font-size: 9px; letter-spacing: 0.14em;
    opacity: 0.5; line-height: 1.8;
  }}
  #hud-br {{
    position: absolute; bottom: 12px; right: 16px;
    font-size: 9px; letter-spacing: 0.14em;
    opacity: 0.5; text-align: right; line-height: 1.8;
  }}
  .corner-tl, .corner-tr, .corner-bl, .corner-br {{
    position: absolute;
    width: 20px; height: 20px;
    opacity: 0.4;
  }}
  .corner-tl {{ top: 6px; left: 6px;
    border-top: 1px solid #00f3ff; border-left: 1px solid #00f3ff; }}
  .corner-tr {{ top: 6px; right: 6px;
    border-top: 1px solid #00f3ff; border-right: 1px solid #00f3ff; }}
  .corner-bl {{ bottom: 6px; left: 6px;
    border-bottom: 1px solid #00f3ff; border-left: 1px solid #00f3ff; }}
  .corner-br {{ bottom: 6px; right: 6px;
    border-bottom: 1px solid #00f3ff; border-right: 1px solid #00f3ff; }}
</style>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700&display=swap" rel="stylesheet">
</head>
<body>
<canvas id="c"></canvas>
<div id="overlay">
  <div class="corner-tl"></div>
  <div class="corner-tr"></div>
  <div class="corner-bl"></div>
  <div class="corner-br"></div>
  <div id="status-tag">INITIALIZING...</div>
  <div id="hud-tl" style="color:#00f3ff;">
    PARTICLE COUNT: 500<br>
    DRAM NODES: ACTIVE<br>
    SIM ENGINE: v4.7.2
  </div>
  <div id="hud-tr" style="color:#00f3ff;">
    LAB: ANU-VICS<br>
    ARCH: HYBRID-NVM<br>
    FRAME: <span id="fps">--</span> Hz
  </div>
  <div id="hud-bl" style="color:#00f3ff;">
    OPERATOR: BELHADJ.FZ<br>
    MODE: <span id="mode-label">--</span>
  </div>
  <div id="hud-br" style="color:#00f3ff;">
    ENTROPY: <span id="entropy-val">--</span><br>
    CONSTRAINT: <span id="constraint-val">--</span>
  </div>
</div>

<script>
const ALGO_ACTIVE = {toggle_state};

const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const statusTag = document.getElementById('status-tag');
const fpsEl = document.getElementById('fps');
const modeEl = document.getElementById('mode-label');
const entEl = document.getElementById('entropy-val');
const conEl = document.getElementById('constraint-val');

function resize() {{
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}}
resize();
window.addEventListener('resize', resize);

// ── PARTICLE CONFIG ──
const N = 500;
const particles = [];
let transition = 0; // 0 = full chaos, 1 = full constrained
const TARGET_TRANSITION = ALGO_ACTIVE ? 1.0 : 0.0;
const TRANSITION_SPEED = 0.018;

// Pre-compute constrained positions on a sphere
function spherePoint(i, total) {{
  const phi = Math.acos(1 - 2 * (i + 0.5) / total);
  const theta = Math.PI * (1 + Math.sqrt(5)) * i;
  const r = 0.38;
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  // 3D sphere projected (pseudo-3D rotation)
  return {{ phi, theta, r, cx, cy }};
}}

for (let i = 0; i < N; i++) {{
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  particles.push({{
    // Chaos state
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 4.5,
    vy: (Math.random() - 0.5) * 4.5,
    ax: 0, ay: 0,
    // Constrained state (sphere)
    phi: Math.acos(1 - 2 * (i + 0.5) / N),
    theta: Math.PI * (1 + Math.sqrt(5)) * i,
    r: Math.min(canvas.width, canvas.height) * 0.3,
    size: Math.random() * 1.8 + 0.6,
    phase: Math.random() * Math.PI * 2,
    // Colour interpolation
    colorPhase: Math.random() * Math.PI * 2,
  }});
}}

let sphereAngleY = 0;
let sphereAngleX = 0;
let lastTime = performance.now();
let frameCount = 0;
let fpsTimer = 0;
let currentFps = 60;

function lerp(a, b, t) {{ return a + (b - a) * t; }}

function getConstrainedPos(p, t) {{
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const r = Math.min(canvas.width, canvas.height) * 0.28;
  // Rotate sphere
  const x0 = r * Math.sin(p.phi) * Math.cos(p.theta);
  const y0 = r * Math.cos(p.phi);
  const z0 = r * Math.sin(p.phi) * Math.sin(p.theta);
  // Y-axis rotation
  const cosY = Math.cos(sphereAngleY);
  const sinY = Math.sin(sphereAngleY);
  const x1 = x0 * cosY - z0 * sinY;
  const z1 = x0 * sinY + z0 * cosY;
  // X-axis rotation
  const cosX = Math.cos(sphereAngleX);
  const sinX = Math.sin(sphereAngleX);
  const y1 = y0 * cosX - z1 * sinX;
  const z2 = y0 * sinX + z1 * cosX;
  // Perspective
  const fov = 500;
  const scale = fov / (fov + z2);
  return {{ x: cx + x1 * scale, y: cy + y1 * scale, z: z2, scale }};
}}

function draw(timestamp) {{
  const dt = Math.min((timestamp - lastTime) / 16.67, 3);
  lastTime = timestamp;

  // FPS
  frameCount++;
  fpsTimer += dt * 16.67;
  if (fpsTimer > 500) {{
    currentFps = Math.round(frameCount / (fpsTimer / 1000));
    frameCount = 0; fpsTimer = 0;
    fpsEl.textContent = currentFps;
  }}

  // Transition
  if (transition < TARGET_TRANSITION) transition = Math.min(transition + TRANSITION_SPEED * dt, TARGET_TRANSITION);
  else if (transition > TARGET_TRANSITION) transition = Math.max(transition - TRANSITION_SPEED * dt, TARGET_TRANSITION);

  // Sphere rotation
  sphereAngleY += 0.003 * dt;
  sphereAngleX += 0.001 * dt;

  // ── CLEAR ──
  ctx.fillStyle = `rgba(5,5,5,${{lerp(0.18, 0.22, transition)}})`;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // ── BACKGROUND GLOW ──
  const bgGrad = ctx.createRadialGradient(
    canvas.width/2, canvas.height/2, 0,
    canvas.width/2, canvas.height/2, canvas.width * 0.4
  );
  if (transition > 0.01) {{
    bgGrad.addColorStop(0, `rgba(0,243,255,${{0.025 * transition}})`);
    bgGrad.addColorStop(1, 'transparent');
  }} else {{
    bgGrad.addColorStop(0, `rgba(255,30,60,${{0.02 * (1 - transition)}})`);
    bgGrad.addColorStop(1, 'transparent');
  }}
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // ── UPDATE & DRAW PARTICLES ──
  // Connection pass first (behind particles)
  for (let i = 0; i < N; i += 3) {{
    const p = particles[i];
    const cp = getConstrainedPos(p, transition);
    const px = lerp(p.x, cp.x, transition);
    const py = lerp(p.y, cp.y, transition);

    // Draw connections to nearby particles
    for (let j = i + 1; j < Math.min(i + 8, N); j++) {{
      const q = particles[j];
      const cq = getConstrainedPos(q, transition);
      const qx = lerp(q.x, cq.x, transition);
      const qy = lerp(q.y, cq.y, transition);
      const dx = px - qx, dy = py - qy;
      const dist = Math.sqrt(dx*dx + dy*dy);
      const maxDist = lerp(120, 40, transition);
      if (dist < maxDist) {{
        const alpha = (1 - dist / maxDist) * lerp(0.25, 0.15, transition);
        if (transition < 0.5) {{
          ctx.strokeStyle = `rgba(${{lerp(255,0,transition*2)}}, ${{lerp(50,100,transition)}}, ${{lerp(20,255,transition*2)}}, ${{alpha}})`;
        }} else {{
          ctx.strokeStyle = `rgba(0, ${{Math.floor(lerp(100,243,(transition-0.5)*2))}}, ${{Math.floor(lerp(100,255,(transition-0.5)*2))}}, ${{alpha}})`;
        }}
        ctx.lineWidth = lerp(0.8, 0.4, transition);
        ctx.beginPath();
        ctx.moveTo(px, py);
        ctx.lineTo(qx, qy);
        ctx.stroke();
      }}
    }}
  }}

  // Particle draw pass
  for (let i = 0; i < N; i++) {{
    const p = particles[i];
    const cp = getConstrainedPos(p, transition);

    // Chaos physics
    if (transition < 0.99) {{
      p.ax = (Math.random() - 0.5) * 0.8 * (1 - transition);
      p.ay = (Math.random() - 0.5) * 0.8 * (1 - transition);
      p.vx = (p.vx + p.ax * dt) * (1 - 0.01 * dt);
      p.vy = (p.vy + p.ay * dt) * (1 - 0.01 * dt);
      const speed = Math.sqrt(p.vx*p.vx + p.vy*p.vy);
      const maxSpeed = lerp(4.0, 0.2, transition);
      if (speed > maxSpeed) {{ p.vx *= maxSpeed/speed; p.vy *= maxSpeed/speed; }}
      p.x = (p.x + p.vx * dt + canvas.width) % canvas.width;
      p.y = (p.y + p.vy * dt + canvas.height) % canvas.height;
    }}

    const px = lerp(p.x, cp.x, transition);
    const py = lerp(p.y, cp.y, transition);
    const depth = lerp(0, cp.scale, transition);
    const baseSize = p.size * lerp(1, depth * 1.4, transition);

    // Color
    const t2 = transition;
    let r, g, b, glowR, glowG, glowB;
    if (t2 < 0.5) {{
      // Chaos: reds/oranges
      const hue = lerp(0, 30, (Math.sin(timestamp * 0.001 + p.colorPhase) + 1) / 2);
      r = 220 + Math.floor(35 * Math.random());
      g = Math.floor(50 + 80 * (1 - t2 * 2));
      b = Math.floor(10 + 20 * Math.random());
      glowR = 255; glowG = 30; glowB = 0;
    }} else {{
      // Constrained: cyan/blue
      const pulse = (Math.sin(timestamp * 0.002 + p.colorPhase) + 1) / 2;
      r = Math.floor(lerp(0, 0, (t2-0.5)*2));
      g = Math.floor(lerp(100, 200 + 43 * pulse, (t2-0.5)*2));
      b = Math.floor(lerp(200, 255, (t2-0.5)*2));
      glowR = 0; glowG = 243; glowB = 255;
    }}

    const glowAlpha = lerp(0.15, 0.35, transition) + 0.1 * Math.sin(timestamp * 0.003 + p.phase);

    // Glow halo
    const grad = ctx.createRadialGradient(px, py, 0, px, py, baseSize * 5);
    grad.addColorStop(0, `rgba(${{glowR}},${{glowG}},${{glowB}},${{glowAlpha}})`);
    grad.addColorStop(1, 'transparent');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(px, py, baseSize * 5, 0, Math.PI * 2);
    ctx.fill();

    // Core dot
    ctx.fillStyle = `rgba(${{r}},${{g}},${{b}},0.95)`;
    ctx.beginPath();
    ctx.arc(px, py, baseSize, 0, Math.PI * 2);
    ctx.fill();
  }}

  // ── HUD UPDATE ──
  const entropyVal = Math.round(lerp(94.7, 1.2, transition) + (Math.random() - 0.5) * 2);
  const constraintVal = Math.round(lerp(3.1, 98.9, transition) + (Math.random() - 0.5) * 0.5);
  entEl.textContent = entropyVal + '%';
  conEl.textContent = constraintVal + '%';
  modeEl.textContent = transition > 0.5 ? 'CONSTRAINED' : 'CHAOTIC';
  entEl.style.color = transition > 0.5 ? '#00f3ff' : '#ff003c';
  modeEl.style.color = transition > 0.5 ? '#00f3ff' : '#ff004c';

  // ── STATUS TAG ──
  if (transition > 0.92) {{
    statusTag.textContent = '◈  BELHADJ CONSTRAINT ACTIVE — PIPELINE LOCKED  ◈';
    statusTag.style.color = '#00f3ff';
    statusTag.style.borderColor = '#00f3ff44';
    statusTag.style.background = 'rgba(0,243,255,0.06)';
    statusTag.style.textShadow = '0 0 12px #00f3ffaa';
  }} else if (transition > 0.1) {{
    statusTag.textContent = '⚡  TRANSITIONING STATE-SPACE...  ⚡';
    statusTag.style.color = '#ffaa00';
    statusTag.style.borderColor = '#ffaa0044';
    statusTag.style.background = 'rgba(255,170,0,0.04)';
    statusTag.style.textShadow = '0 0 10px #ffaa0088';
  }} else {{
    statusTag.textContent = '⚠  ENTROPY LEAK DETECTED — MEMORY SPILLAGE CRITICAL  ⚠';
    statusTag.style.color = '#ff003c';
    statusTag.style.borderColor = '#ff003c44';
    statusTag.style.background = 'rgba(255,0,60,0.06)';
    statusTag.style.textShadow = '0 0 12px #ff003caa';
  }}

  requestAnimationFrame(draw);
}}

requestAnimationFrame(draw);
</script>
</body>
</html>
"""

# ── RENDER SIMULATION ──
st.markdown("""
<div style="
    border:1px solid #00f3ff22;
    border-radius:3px;
    overflow:hidden;
    box-shadow:
        0 0 40px #00f3ff0a,
        inset 0 0 80px #050505;
    position:relative;
">
""", unsafe_allow_html=True)

components.html(SIMULATION_HTML, height=580, scrolling=False)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  BOTTOM METRICS
# ─────────────────────────────────────────────
st.markdown("""
<div style="
    font-family:'Share Tech Mono',monospace;
    font-size:0.6rem;
    color:#00f3ff55;
    letter-spacing:0.2em;
    text-align:center;
    margin-bottom:0.8rem;
">▼  LIVE TELEMETRY READOUT  ▼</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

if algo_active:
    dram_val = round(np.random.uniform(0.4, 0.9), 2)
    waste_val = round(np.random.uniform(1.8, 3.9), 1)
    dram_delta = "▼ -97.3%"
    waste_delta = "▼ -94.1%"
    pipeline_label = "OPTIMIZED & LOCKED"
    pipeline_color = "#00f3ff"
    pipeline_glow = "#00f3ff88"
    dram_color = "#00f3ff"
    waste_color = "#00f3ff"
else:
    dram_val = round(np.random.uniform(14.8, 18.4), 2)
    waste_val = round(np.random.uniform(62.0, 78.5), 1)
    dram_delta = "▲ CRITICAL"
    waste_delta = "▲ SEVERE"
    pipeline_label = "UNCONSTRAINED"
    pipeline_color = "#ff003c"
    pipeline_glow = "#ff003c88"
    dram_color = "#ff4466"
    waste_color = "#ff3355"

with col1:
    st.metric(
        label="DRAM PRESSURE (TB/s)",
        value=f"{dram_val}",
        delta=dram_delta,
        delta_color="normal" if algo_active else "inverse"
    )
    st.markdown(f"""
    <style>
    [data-testid="stColumns"] > div:nth-child(1) [data-testid="stMetricValue"] {{
        color: {dram_color} !important;
        text-shadow: 0 0 20px {dram_color}88;
    }}
    </style>
    """, unsafe_allow_html=True)

with col2:
    st.metric(
        label="COMPUTE WASTE (%)",
        value=f"{waste_val}%",
        delta=waste_delta,
        delta_color="normal" if algo_active else "inverse"
    )

with col3:
    st.markdown(f"""
    <div style="
        background: rgba(0,0,0,0.3);
        border: 1px solid {pipeline_color}33;
        border-radius: 2px;
        padding: 1.2rem 1.5rem;
        text-align: left;
        backdrop-filter: blur(8px);
        height: 100%;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
      <div style="
          font-family:'Share Tech Mono',monospace;
          font-size:0.62rem;
          letter-spacing:0.18em;
          color:{pipeline_color}99;
          text-transform:uppercase;
          margin-bottom:0.5rem;
      ">PIPELINE STATE</div>
      <div style="
          font-family:'Orbitron',sans-serif;
          font-size:1.25rem;
          font-weight:700;
          color:{pipeline_color};
          text-shadow: 0 0 16px {pipeline_glow}, 0 0 32px {pipeline_color}44;
          letter-spacing:0.06em;
          animation: pulseglow 1.4s ease-in-out infinite alternate;
      ">{pipeline_label}</div>
      <style>
        @keyframes pulseglow {{
          from {{ text-shadow: 0 0 8px {pipeline_glow}; }}
          to   {{ text-shadow: 0 0 28px {pipeline_glow}, 0 0 50px {pipeline_color}44; }}
        }}
      </style>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ──
st.markdown(f"""
<div style="
    margin-top:2rem;
    height:1px;
    background:linear-gradient(90deg,transparent,#00f3ff33,transparent);
"></div>
<div style="
    display:flex;justify-content:space-between;
    font-family:'Share Tech Mono',monospace;
    font-size:0.55rem;
    color:#00f3ff28;
    letter-spacing:0.14em;
    padding:0.6rem 0 0.3rem;
">
  <span>VICS-BELHADJ-AUDIT // TERMINAL BUILD 2080.04.03</span>
  <span>ALGO: {'ACTIVE — CONSTRAINT ENGAGED' if algo_active else 'STANDBY — ENTROPY MODE'}</span>
  <span>ANU-CECS // DR. AKRAM RESEARCH NODE</span>
</div>
""", unsafe_allow_html=True)
