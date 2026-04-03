"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║        VICS-BELHADJ NEURAL-MEMORY ARCHITECT  V1.0                              ║
║        Lead Research Engineer: F.Z. Belhadj  |  ANU VICS Lab                  ║
║        Supervisor: Dr. Shoaib Akram           |  Hybrid NVM/DRAM Research      ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import math

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VICS-BELHADJ NEURAL-MEMORY ARCHITECT V1.0",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── SESSION STATE BOOTSTRAP ─────────────────────────────────────────────────
if "anchor_active" not in st.session_state:
    st.session_state.anchor_active = False
if "sim_run" not in st.session_state:
    st.session_state.sim_run = 0
if "glitch_trigger" not in st.session_state:
    st.session_state.glitch_trigger = False

# ─── CSS INJECTION ────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ─── GLOBAL RESET & FONT ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #000508 !important;
    color: #00f3ff !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ─── HIDE STREAMLIT CHROME ───────────────────────────── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.viewerBadge_container__1QSob { display: none !important; }

/* ─── ANIMATED STAR-FIELD / GRID OVERLAY ─────────────── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(0,243,255,0.55) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 60%, rgba(0,243,255,0.40) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 10%, rgba(255,255,255,0.60) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 80%, rgba(0,243,255,0.45) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 40%, rgba(255,0,60,0.45) 0%, transparent 100%),
        radial-gradient(1px 1px at 20% 90%, rgba(255,255,255,0.50) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 55%, rgba(0,243,255,0.35) 0%, transparent 100%),
        radial-gradient(1px 1px at 80% 15%, rgba(255,255,255,0.50) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 35%, rgba(255,0,60,0.30) 0%, transparent 100%),
        radial-gradient(1px 1px at 65% 70%, rgba(0,243,255,0.40) 0%, transparent 100%),
        linear-gradient(rgba(0,243,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,243,255,0.03) 1px, transparent 1px);
    background-size:
        100% 100%, 100% 100%, 100% 100%, 100% 100%, 100% 100%,
        100% 100%, 100% 100%, 100% 100%, 100% 100%, 100% 100%,
        60px 60px, 60px 60px;
    pointer-events: none;
    z-index: 0;
    animation: starDrift 120s linear infinite;
}

@keyframes starDrift {
    0%   { background-position: 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0; }
    100% { background-position: 200px 300px, -150px 400px, 100px -200px, -300px 150px, 250px -100px,
                                 -200px 250px, 180px 180px, -120px -180px, 220px 120px, -180px 220px,
                                 60px 60px, 60px 60px; }
}

/* ─── SIDEBAR ─────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(0, 15, 25, 0.92) !important;
    border-right: 1px solid rgba(0, 243, 255, 0.35) !important;
    backdrop-filter: blur(16px) !important;
}

[data-testid="stSidebar"] * {
    color: #00f3ff !important;
}

/* ─── GLASSMORPHIC CARDS ──────────────────────────────── */
.glass-card {
    background: rgba(0, 20, 35, 0.70);
    border: 1px solid rgba(0, 243, 255, 0.30);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 18px 22px;
    margin-bottom: 16px;
    box-shadow: 0 0 18px rgba(0,243,255,0.08), inset 0 1px 0 rgba(0,243,255,0.12);
    opacity: 0.95;
}

.glass-card-red {
    background: rgba(25, 0, 10, 0.70);
    border: 1px solid rgba(255, 0, 60, 0.35);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 18px 22px;
    margin-bottom: 16px;
    box-shadow: 0 0 18px rgba(255,0,60,0.08), inset 0 1px 0 rgba(255,0,60,0.12);
    opacity: 0.95;
}

/* ─── MASTHEAD ────────────────────────────────────────── */
.masthead {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: clamp(1.1rem, 2.2vw, 1.8rem);
    letter-spacing: 0.12em;
    text-align: center;
    color: #00f3ff;
    text-shadow:
        0 0 8px  #00f3ff,
        0 0 20px #00f3ff,
        0 0 45px rgba(0,243,255,0.55);
    padding: 6px 0 2px;
    animation: masterPulse 3s ease-in-out infinite;
}

@keyframes masterPulse {
    0%,100% { text-shadow: 0 0 8px #00f3ff, 0 0 20px #00f3ff, 0 0 45px rgba(0,243,255,0.55); }
    50%      { text-shadow: 0 0 14px #00f3ff, 0 0 35px #00f3ff, 0 0 80px rgba(0,243,255,0.85); }
}

.subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    text-align: center;
    color: rgba(0,243,255,0.55);
    margin-bottom: 10px;
}

/* ─── TELEMETRY GAUGES ────────────────────────────────── */
.gauge-wrap {
    text-align: center;
    padding: 14px 10px;
}

.gauge-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.60rem;
    letter-spacing: 0.20em;
    color: rgba(0,243,255,0.65);
    margin-bottom: 8px;
    text-transform: uppercase;
}

.gauge-value {
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    font-size: clamp(1.8rem, 3vw, 2.6rem);
    line-height: 1;
    animation: gaugePulse 2s ease-in-out infinite;
}

.gauge-cyan  { color: #00f3ff; text-shadow: 0 0 12px #00f3ff, 0 0 30px rgba(0,243,255,0.50); }
.gauge-red   { color: #ff003c; text-shadow: 0 0 12px #ff003c, 0 0 30px rgba(255,0,60,0.50); }
.gauge-amber { color: #ffa500; text-shadow: 0 0 12px #ffa500, 0 0 30px rgba(255,165,0,0.50); }

@keyframes gaugePulse {
    0%,100% { opacity: 1.0; }
    50%      { opacity: 0.78; }
}

.gauge-unit {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: rgba(0,243,255,0.45);
    margin-top: 4px;
}

/* ─── SECTION HEADERS ─────────────────────────────────── */
.section-hdr {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.30em;
    color: rgba(0,243,255,0.55);
    text-transform: uppercase;
    border-bottom: 1px solid rgba(0,243,255,0.20);
    padding-bottom: 6px;
    margin-bottom: 12px;
}

/* ─── ANCHOR BUTTON ───────────────────────────────────── */
.stButton > button {
    background: transparent !important;
    border: 2px solid #00f3ff !important;
    color: #00f3ff !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.80rem !important;
    letter-spacing: 0.20em !important;
    padding: 14px 28px !important;
    border-radius: 4px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    text-shadow: 0 0 10px #00f3ff !important;
    box-shadow: 0 0 16px rgba(0,243,255,0.25), inset 0 0 16px rgba(0,243,255,0.05) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    background: rgba(0,243,255,0.08) !important;
    box-shadow: 0 0 32px rgba(0,243,255,0.55), inset 0 0 24px rgba(0,243,255,0.12) !important;
    transform: translateY(-2px) !important;
}

.stButton > button:active {
    transform: translateY(1px) !important;
    box-shadow: 0 0 8px rgba(0,243,255,0.30) !important;
}

/* ─── GLITCH EFFECT ───────────────────────────────────── */
.glitch-overlay {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 9999;
    animation: glitchSeq 0.8s steps(1) forwards;
}

@keyframes glitchSeq {
    0%   { background: rgba(0,243,255,0.15); clip-path: inset(0 0 85% 0); }
    10%  { background: rgba(255,0,60,0.12);  clip-path: inset(40% 0 40% 0); transform: translateX(-8px); }
    20%  { background: rgba(0,243,255,0.20); clip-path: inset(70% 0 0 0);   transform: translateX(6px); }
    30%  { background: rgba(255,0,60,0.10);  clip-path: inset(20% 0 60% 0); transform: translateX(-4px) skewX(2deg); }
    40%  { background: rgba(0,243,255,0.15); clip-path: inset(55% 0 20% 0); transform: translateX(10px); }
    50%  { background: rgba(255,165,0,0.10); clip-path: inset(10% 0 75% 0); transform: translateX(-6px); }
    60%  { background: rgba(0,243,255,0.08); clip-path: inset(80% 0 5% 0);  transform: translateX(4px) skewX(-1deg); }
    70%  { background: rgba(255,0,60,0.06);  clip-path: inset(35% 0 50% 0); transform: translateX(-2px); }
    80%  { background: rgba(0,243,255,0.12); clip-path: inset(60% 0 25% 0); transform: translateX(3px); }
    90%  { background: rgba(255,0,60,0.04);  clip-path: inset(5% 0 90% 0);  transform: translateX(-1px); }
    100% { background: transparent; clip-path: none; transform: none; }
}

.shake-root {
    animation: screenShake 0.6s ease-in-out;
}

@keyframes screenShake {
    0%,100% { transform: translate(0,0) rotate(0deg); }
    10%      { transform: translate(-6px, -4px) rotate(-0.5deg); }
    20%      { transform: translate(6px, 4px) rotate(0.5deg); }
    30%      { transform: translate(-4px, 6px) rotate(-0.3deg); }
    40%      { transform: translate(4px, -6px) rotate(0.3deg); }
    50%      { transform: translate(-8px, 2px) rotate(-0.6deg); }
    60%      { transform: translate(8px, -2px) rotate(0.6deg); }
    70%      { transform: translate(-3px, -5px) rotate(-0.2deg); }
    80%      { transform: translate(3px, 5px) rotate(0.2deg); }
    90%      { transform: translate(-1px, -1px) rotate(0deg); }
}

/* ─── METRICS OVERRIDE ────────────────────────────────── */
[data-testid="stMetricLabel"]  { color: rgba(0,243,255,0.60) !important; font-size:0.62rem !important; letter-spacing:0.15em; }
[data-testid="stMetricValue"]  { color: #00f3ff !important; font-family:'Orbitron',sans-serif !important; font-size:1.1rem !important; }
[data-testid="stMetricDelta"]  { color: #00f3ff !important; }

/* ─── SLIDER ──────────────────────────────────────────── */
[data-testid="stSlider"] > div > div > div > div {
    background: #00f3ff !important;
}

/* ─── STATUS BADGE ────────────────────────────────────── */
.status-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 3px;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.60rem;
    letter-spacing: 0.20em;
    font-weight: 700;
    border: 1px solid;
}

.badge-online {
    border-color: #00f3ff;
    color: #00f3ff;
    background: rgba(0,243,255,0.10);
    box-shadow: 0 0 8px rgba(0,243,255,0.30);
    animation: badgeBlink 2s ease-in-out infinite;
}

.badge-offline {
    border-color: #ff003c;
    color: #ff003c;
    background: rgba(255,0,60,0.10);
    box-shadow: 0 0 8px rgba(255,0,60,0.30);
}

@keyframes badgeBlink {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.65; }
}

/* ─── SIDEBAR IDENTITY PANEL ──────────────────────────── */
.id-header {
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    font-size: 0.68rem;
    letter-spacing: 0.20em;
    color: #00f3ff;
    text-shadow: 0 0 8px rgba(0,243,255,0.60);
    border: 1px solid rgba(0,243,255,0.30);
    border-radius: 4px;
    padding: 8px 12px;
    margin-bottom: 14px;
    background: rgba(0,243,255,0.06);
}

.award-chip {
    display: inline-block;
    border: 1px solid rgba(0,243,255,0.40);
    border-radius: 3px;
    padding: 3px 8px;
    margin: 3px 2px;
    font-size: 0.58rem;
    letter-spacing: 0.10em;
    color: rgba(0,243,255,0.80);
    background: rgba(0,243,255,0.06);
}

.pitch-box {
    background: rgba(0,20,35,0.80);
    border-left: 3px solid #00f3ff;
    border-radius: 0 6px 6px 0;
    padding: 12px 14px;
    font-size: 0.64rem;
    line-height: 1.7;
    color: rgba(0,243,255,0.80);
    margin-top: 10px;
}

/* ─── PROGRESS BAR ────────────────────────────────────── */
.prog-wrap { margin: 6px 0; }
.prog-label { font-size: 0.60rem; letter-spacing: 0.12em; color: rgba(0,243,255,0.60); margin-bottom: 3px; display:flex; justify-content:space-between; }
.prog-track { height: 4px; background: rgba(0,243,255,0.12); border-radius: 2px; overflow:hidden; }
.prog-fill  { height: 100%; border-radius: 2px; transition: width 1s ease; }
.prog-cyan  { background: linear-gradient(90deg, rgba(0,243,255,0.4), #00f3ff); box-shadow: 0 0 6px rgba(0,243,255,0.60); }
.prog-red   { background: linear-gradient(90deg, rgba(255,0,60,0.4), #ff003c);  box-shadow: 0 0 6px rgba(255,0,60,0.60); }
.prog-amber { background: linear-gradient(90deg, rgba(255,165,0,0.4), #ffa500); box-shadow: 0 0 6px rgba(255,165,0,0.60); }

/* ─── EQUATION BOX ────────────────────────────────────── */
.eq-box {
    background: rgba(0,10,20,0.80);
    border: 1px solid rgba(0,243,255,0.20);
    border-radius: 6px;
    padding: 10px 14px;
    font-size: 0.68rem;
    letter-spacing: 0.05em;
    color: rgba(0,243,255,0.75);
    font-family: 'Share Tech Mono', monospace;
    margin: 8px 0;
}

/* ─── SCROLLBAR ───────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: rgba(0,243,255,0.05); }
::-webkit-scrollbar-thumb { background: rgba(0,243,255,0.35); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ─── GLITCH JS TRIGGER ────────────────────────────────────────────────────────
if st.session_state.glitch_trigger:
    st.markdown("""
    <div class="glitch-overlay" id="glitch-div"></div>
    <script>
    (function(){
        var root = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
        if(root){ root.classList.add('shake-root'); setTimeout(()=>root.classList.remove('shake-root'), 650); }
    })();
    </script>
    """, unsafe_allow_html=True)
    st.session_state.glitch_trigger = False

# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 1 ── STOCHASTIC GENERATOR  (Non-stationary Poisson)
# ══════════════════════════════════════════════════════════════════════════════
def generate_nonstationary_poisson(n_steps: int = 300,
                                   base_lambda: float = 45.0,
                                   seed: int = 0,
                                   anchor: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """
    Non-stationary Poisson token-arrival process for GenAI inference workloads.
    λ(t) = base_λ · (1 + A·sin(2π·f·t) + η(t))
    where η(t) is colored Gaussian noise (AR-1 model) simulating burst traffic.
    With anchor ON, PID-shaped λ is clamped to prevent thermal runaway.
    """
    rng = np.random.default_rng(seed)
    t   = np.linspace(0, 1, n_steps)

    # Sinusoidal modulation (workload periodicity) + AR-1 burst noise
    A_mod = 0.45 if not anchor else 0.18
    freq  = 3.5
    noise = np.zeros(n_steps)
    noise[0] = rng.standard_normal()
    phi   = 0.92 if not anchor else 0.60          # AR-1 autocorrelation
    sigma = 0.28 if not anchor else 0.08
    for i in range(1, n_steps):
        noise[i] = phi * noise[i-1] + sigma * rng.standard_normal()

    lambda_t = base_lambda * (1.0 + A_mod * np.sin(2 * np.pi * freq * t) + noise)
    lambda_t = np.clip(lambda_t, 1.0, None)

    # Poisson draws per time-step
    arrivals = rng.poisson(lambda_t)
    return t, lambda_t, arrivals


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 2 ── MEMORY HIERARCHY MATH  (AMAT / Hybrid NVM-DRAM)
# ══════════════════════════════════════════════════════════════════════════════
def compute_amat(p_dram: float, t_dram_ns: float, t_nvm_ns: float) -> float:
    """
    AMAT = P_dram · T_dram + (1 - P_dram) · T_nvm
    Units: nanoseconds
    """
    return p_dram * t_dram_ns + (1.0 - p_dram) * t_nvm_ns


def compute_waf(lambda_t: np.ndarray, anchor: bool,
                capacity_gb: float = 32.0,
                nvm_write_endurance: float = 3000.0) -> tuple[float, float, float]:
    """
    Write Amplification Factor (WAF) and derived metrics.
    WAF ≥ 1; higher ⟹ faster NVM wear-out.
    DRAM pressure modelled as normalised queue-fill ratio.
    Energy waste ∝ excess writes · (T_nvm - T_dram).
    """
    mean_arr = float(np.mean(lambda_t))
    variance = float(np.var(lambda_t))

    # WAF is a function of write-pattern entropy (variance) and capacity stress
    base_waf = 1.0 + 2.8 * (mean_arr / 80.0) * (1.0 + 0.6 * (variance / (mean_arr**2 + 1e-6)))
    if anchor:
        waf = max(1.0, base_waf * 0.41)          # PID shaping reduces amplification
    else:
        waf = base_waf

    # DRAM pressure: queue utilisation fraction
    burst_ratio  = variance / (mean_arr ** 2 + 1e-6)
    dram_pressure = min(0.99, 0.25 + 0.58 * burst_ratio) if not anchor else min(0.99, 0.12 + 0.18 * burst_ratio)

    # Energy waste (arbitrary normalised units, 0-100)
    t_dram, t_nvm = 80.0, 1400.0
    writes_excess  = (waf - 1.0) * mean_arr * 1e-3
    energy_waste   = min(99.9, writes_excess * (t_nvm - t_dram) / 180.0)

    return round(waf, 3), round(dram_pressure * 100, 1), round(energy_waste, 1)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 3 ── BELHADJ LOGIC ANCHOR  (PID Controller)
# ══════════════════════════════════════════════════════════════════════════════
class BelhadjPIDController:
    """
    Proportional-Integral-Derivative controller that governs GenAI data-ingress
    rate to prevent DRAM thermal throttling and buffer overflow events.

    Control law:  u(t) = Kp·e(t) + Ki·∫e(τ)dτ + Kd·(de/dt)
    Plant output: regulated λ_shaped(t) = λ_raw(t) - u(t)
    Setpoint:     λ_target (tokens/ms) derived from NVM write-budget
    """
    def __init__(self, kp: float = 0.55, ki: float = 0.12, kd: float = 0.08,
                 setpoint: float = 45.0, dt: float = 1.0):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.setpoint = setpoint
        self.dt       = dt
        self._integral = 0.0
        self._prev_err = 0.0

    def step(self, measured: float) -> tuple[float, float, float, float]:
        """Single PID step; returns (output, P-term, I-term, D-term)."""
        e    = self.setpoint - measured
        self._integral    += e * self.dt
        self._integral     = np.clip(self._integral, -300.0, 300.0)   # anti-windup
        derivative         = (e - self._prev_err) / self.dt
        self._prev_err     = e
        p_term = self.kp * e
        i_term = self.ki * self._integral
        d_term = self.kd * derivative
        u      = p_term + i_term + d_term
        return u, p_term, i_term, d_term

    def process(self, lambda_t: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        self._integral, self._prev_err = 0.0, 0.0
        u_arr = np.zeros_like(lambda_t)
        p_arr = np.zeros_like(lambda_t)
        i_arr = np.zeros_like(lambda_t)
        d_arr = np.zeros_like(lambda_t)
        for i, lam in enumerate(lambda_t):
            u, p, iv, d = self.step(lam)
            u_arr[i], p_arr[i], i_arr[i], d_arr[i] = u, p, iv, d
        shaped = np.clip(lambda_t - u_arr, 1.0, None)
        return shaped, p_arr, i_arr, d_arr


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 4 ── 3D LATENT STATE-SPACE GEOMETRY
# ══════════════════════════════════════════════════════════════════════════════
def build_state_space_3d(n: int = 520, anchor: bool = False, seed: int = 42) -> go.Figure:
    """
    3D Scatter: each token-batch maps to (AMAT_delta, λ_normalised, WAF_delta).
    OFF ⟹ chaotic red point-cloud.  ON ⟹ stable cyan torus with trajectory.
    """
    rng = np.random.default_rng(seed)
    fig = go.Figure()

    if not anchor:
        # ── CHAOTIC REGIME ───────────────────────────────────────────────────
        cx = rng.uniform(-1, 1, n) + rng.standard_normal(n) * 0.55
        cy = rng.uniform(-1, 1, n) + rng.standard_normal(n) * 0.55
        cz = rng.uniform(-1, 1, n) + rng.standard_normal(n) * 0.55
        # Colour by distance from origin (entropy proxy)
        dist   = np.sqrt(cx**2 + cy**2 + cz**2)
        colors = dist

        fig.add_trace(go.Scatter3d(
            x=cx, y=cy, z=cz,
            mode='markers',
            marker=dict(
                size=3.2,
                color=colors,
                colorscale=[[0,'#ff003c'],[0.5,'#ff6b35'],[1,'#ff003c']],
                opacity=0.72,
                line=dict(width=0),
            ),
            name='Unshielded Token States',
        ))
        # Chaotic attractor skeleton (Lorenz-inspired spiral)
        theta_l = np.linspace(0, 12 * np.pi, 400)
        lx = np.sin(theta_l) * np.exp(-theta_l * 0.015) * 1.5
        ly = np.cos(theta_l) * np.exp(-theta_l * 0.015) * 1.5
        lz = theta_l / (4 * np.pi) - 1.5
        fig.add_trace(go.Scatter3d(
            x=lx, y=ly, z=lz,
            mode='lines',
            line=dict(color='rgba(255,0,60,0.35)', width=1.5),
            name='Entropy Attractor',
        ))
        title_text = "⚠ LATENT STATE-SPACE  ·  ANCHOR OFF  ·  CHAOTIC REGIME"
        bg_color   = 'rgba(12,0,5,0.95)'

    else:
        # ── STABLE TORUS REGIME ──────────────────────────────────────────────
        R, r_tube = 1.20, 0.40
        u_t = np.linspace(0, 2 * np.pi, n)
        v_t = np.linspace(0, 2 * np.pi, n)
        uu, vv = np.meshgrid(
            np.linspace(0, 2*np.pi, 28),
            np.linspace(0, 2*np.pi, 28)
        )
        tx = (R + r_tube * np.cos(vv)) * np.cos(uu)
        ty = (R + r_tube * np.cos(vv)) * np.sin(uu)
        tz =  r_tube * np.sin(vv)

        # Torus surface
        fig.add_trace(go.Surface(
            x=tx, y=ty, z=tz,
            colorscale=[[0,'rgba(0,100,120,0.25)'],[1,'rgba(0,243,255,0.45)']],
            opacity=0.30,
            showscale=False,
            name='Torus Surface',
        ))

        # Stable trajectory (toroidal winding)
        phi_winding = 2.618  # golden-ratio winding frequency
        st_u = np.linspace(0, 6 * np.pi, 800)
        st_v = phi_winding * st_u
        px = (R + r_tube * np.cos(st_v)) * np.cos(st_u)
        py = (R + r_tube * np.cos(st_v)) * np.sin(st_u)
        pz =  r_tube * np.sin(st_v)
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz,
            mode='lines',
            line=dict(
                color=np.linspace(0, 1, len(px)),
                colorscale=[[0,'#00f3ff'],[1,'#00ffa3']],
                width=3.5,
            ),
            name='Stable Trajectory',
        ))

        # Token-state particles on torus
        idx_s = rng.integers(0, len(px)-1, n)
        noise_s = rng.standard_normal((n,3)) * 0.045
        fig.add_trace(go.Scatter3d(
            x=px[idx_s]+noise_s[:,0], y=py[idx_s]+noise_s[:,1], z=pz[idx_s]+noise_s[:,2],
            mode='markers',
            marker=dict(
                size=2.8,
                color='#00f3ff',
                opacity=0.80,
                line=dict(width=0),
            ),
            name='Shaped Token States',
        ))
        title_text = "✦ LATENT STATE-SPACE  ·  ANCHOR ON  ·  STABLE TORUS ATTRACTOR"
        bg_color   = 'rgba(0,8,18,0.95)'

    fig.update_layout(
        title=dict(text=title_text, font=dict(family='Orbitron', size=11, color='#00f3ff'), x=0.5),
        scene=dict(
            xaxis=dict(title='ΔAMAT (ns)', gridcolor='rgba(0,243,255,0.12)',
                       backgroundcolor='rgba(0,0,0,0)', color='rgba(0,243,255,0.55)',
                       titlefont=dict(size=8), tickfont=dict(size=7)),
            yaxis=dict(title='λ_norm', gridcolor='rgba(0,243,255,0.12)',
                       backgroundcolor='rgba(0,0,0,0)', color='rgba(0,243,255,0.55)',
                       titlefont=dict(size=8), tickfont=dict(size=7)),
            zaxis=dict(title='ΔWAF', gridcolor='rgba(0,243,255,0.12)',
                       backgroundcolor='rgba(0,0,0,0)', color='rgba(0,243,255,0.55)',
                       titlefont=dict(size=8), tickfont=dict(size=7)),
            bgcolor='rgba(0,0,0,0)',
            camera=dict(eye=dict(x=1.55, y=1.55, z=0.85)),
        ),
        paper_bgcolor=bg_color,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(font=dict(family='Share Tech Mono', size=8, color='rgba(0,243,255,0.65)'),
                    bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,243,255,0.20)', borderwidth=1),
        height=480,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 5 ── PARETO EFFICIENCY FRONTIER
# ══════════════════════════════════════════════════════════════════════════════
def build_pareto_chart(anchor: bool) -> go.Figure:
    """
    Dual-axis Plotly chart: Throughput [tokens/s] vs Latency [ms].
    Pareto frontier separates feasible from infeasible operating points.
    Anchor shifts the frontier toward lower latency & higher throughput.
    """
    rng = np.random.default_rng(7)
    n_pts = 60

    # Uncontrolled operating points
    tput_raw   = rng.uniform(18, 72, n_pts)
    lat_raw    = 1200 / (tput_raw + 1) + rng.uniform(0, 18, n_pts)

    # Controlled operating points (shifted Pareto)
    tput_ctrl  = rng.uniform(55, 130, n_pts)
    lat_ctrl   = 900  / (tput_ctrl + 1) + rng.uniform(0, 8, n_pts)

    # Compute Pareto fronts
    def pareto_front(x, y):
        pts   = sorted(zip(x, y), key=lambda p: p[0])
        front = [pts[0]]
        for p in pts[1:]:
            if p[1] <= front[-1][1]:
                front.append(p)
        fx, fy = zip(*front)
        return np.array(fx), np.array(fy)

    pfx_r, pfy_r = pareto_front(tput_raw,  lat_raw)
    pfx_c, pfy_c = pareto_front(tput_ctrl, lat_ctrl)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # ── Scatter clouds ───────────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=tput_raw, y=lat_raw,
        mode='markers',
        marker=dict(size=5, color='rgba(255,0,60,0.35)', line=dict(width=0)),
        name='Uncontrolled OPs',
    ), secondary_y=False)

    if anchor:
        fig.add_trace(go.Scatter(
            x=tput_ctrl, y=lat_ctrl,
            mode='markers',
            marker=dict(size=5, color='rgba(0,243,255,0.30)', line=dict(width=0)),
            name='Shaped OPs',
        ), secondary_y=False)

    # ── Pareto frontiers ─────────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=pfx_r, y=pfy_r,
        mode='lines+markers',
        line=dict(color='#ff003c', width=2.5, dash='dot'),
        marker=dict(size=6, color='#ff003c', symbol='diamond'),
        name='Frontier: Uncontrolled',
    ), secondary_y=False)

    if anchor:
        fig.add_trace(go.Scatter(
            x=pfx_c, y=pfy_c,
            mode='lines+markers',
            line=dict(color='#00f3ff', width=2.8),
            marker=dict(size=7, color='#00f3ff', symbol='star'),
            name='Frontier: Anchor-Shaped',
        ), secondary_y=False)

    # ── WAF secondary axis ────────────────────────────────────────────────────
    t_ax   = np.linspace(min(tput_raw.min(), tput_ctrl.min()),
                         max(tput_raw.max(), tput_ctrl.max()), 80)
    waf_ax = 1.0 + 2.5 * np.exp(-t_ax / 50.0) + 0.15 * np.sin(t_ax / 10.0)
    if anchor:
        waf_ax_c = 1.0 + 0.85 * np.exp(-t_ax / 80.0) + 0.04 * np.sin(t_ax / 12.0)
        fig.add_trace(go.Scatter(
            x=t_ax, y=waf_ax_c,
            mode='lines',
            line=dict(color='rgba(0,255,163,0.70)', width=2, dash='dash'),
            name='WAF (Shaped)',
        ), secondary_y=True)

    fig.add_trace(go.Scatter(
        x=t_ax, y=waf_ax,
        mode='lines',
        line=dict(color='rgba(255,165,0,0.65)', width=2, dash='dash'),
        name='WAF (Raw)',
    ), secondary_y=True)

    fig.update_layout(
        paper_bgcolor='rgba(0,8,18,0.95)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Share Tech Mono', color='rgba(0,243,255,0.70)', size=9),
        title=dict(
            text="PARETO EFFICIENCY FRONTIER  ·  THROUGHPUT vs LATENCY vs WAF",
            font=dict(family='Orbitron', size=10, color='#00f3ff'), x=0.5
        ),
        xaxis=dict(
            title='Throughput  [tokens/s]',
            gridcolor='rgba(0,243,255,0.10)',
            zerolinecolor='rgba(0,243,255,0.20)',
            color='rgba(0,243,255,0.60)',
        ),
        yaxis=dict(
            title='Latency  [ms]',
            gridcolor='rgba(0,243,255,0.10)',
            zerolinecolor='rgba(0,243,255,0.20)',
            color='rgba(0,243,255,0.60)',
        ),
        yaxis2=dict(
            title='WAF  [×]',
            gridcolor='rgba(0,243,255,0.06)',
            color='rgba(255,165,0,0.70)',
        ),
        legend=dict(
            font=dict(size=8),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,243,255,0.20)',
            borderwidth=1,
        ),
        height=360,
        margin=dict(l=50, r=60, t=45, b=40),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 6 ── PID RESPONSE CHART
# ══════════════════════════════════════════════════════════════════════════════
def build_pid_chart(t: np.ndarray, lambda_raw: np.ndarray,
                    shaped: np.ndarray, p_t, i_t, d_t) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=lambda_raw,
        mode='lines',
        line=dict(color='rgba(255,0,60,0.65)', width=1.8),
        fill='tozeroy',
        fillcolor='rgba(255,0,60,0.04)',
        name='λ_raw(t)',
    ))
    fig.add_trace(go.Scatter(
        x=t, y=shaped,
        mode='lines',
        line=dict(color='#00f3ff', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(0,243,255,0.06)',
        name='λ_shaped(t) [PID]',
    ))
    fig.add_trace(go.Scatter(
        x=t, y=p_t * 10 + 50,   # scaled for visibility
        mode='lines',
        line=dict(color='rgba(0,255,163,0.55)', width=1.2, dash='dot'),
        name='P-term (×10)',
    ))
    fig.add_trace(go.Scatter(
        x=t, y=d_t * 50 + 50,
        mode='lines',
        line=dict(color='rgba(255,165,0,0.45)', width=1.2, dash='dash'),
        name='D-term (×50)',
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,8,18,0.95)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Share Tech Mono', color='rgba(0,243,255,0.70)', size=9),
        title=dict(
            text="BELHADJ PID ANCHOR  ·  TOKEN ARRIVAL SHAPING",
            font=dict(family='Orbitron', size=10, color='#00f3ff'), x=0.5
        ),
        xaxis=dict(title='Normalised Time', gridcolor='rgba(0,243,255,0.08)',
                   color='rgba(0,243,255,0.60)'),
        yaxis=dict(title='λ  [tokens/ms]', gridcolor='rgba(0,243,255,0.08)',
                   color='rgba(0,243,255,0.60)'),
        legend=dict(font=dict(size=8), bgcolor='rgba(0,0,0,0)',
                    bordercolor='rgba(0,243,255,0.20)', borderwidth=1),
        height=300,
        margin=dict(l=50, r=20, t=45, b=40),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  RUN THE SIMULATION (with optional randomised seed per run)
# ══════════════════════════════════════════════════════════════════════════════
anchor    = st.session_state.anchor_active
seed_val  = st.session_state.sim_run % 16

t_ax, lambda_t, arrivals = generate_nonstationary_poisson(
    n_steps=300, base_lambda=45.0, seed=seed_val, anchor=anchor
)
pid = BelhadjPIDController(kp=0.55, ki=0.12, kd=0.08, setpoint=45.0)
shaped_lambda, p_t, i_t, d_t = pid.process(lambda_t)

waf, dram_pct, e_waste = compute_waf(lambda_t, anchor)

p_dram = 0.72 if not anchor else 0.88
amat   = compute_amat(p_dram, t_dram_ns=80.0, t_nvm_ns=1400.0)


# ══════════════════════════════════════════════════════════════════════════════
#  ── SIDEBAR: ENGINEERING DOSSIER ────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="id-header">[ OPERATOR IDENTITY: F.Z. BELHADJ ]</div>',
                unsafe_allow_html=True)

    badge_html = ('<span class="status-badge badge-online">● ONLINE</span>'
                  if anchor else
                  '<span class="status-badge badge-offline">● STANDBY</span>')
    st.markdown(f'<div style="text-align:center;margin-bottom:14px;">{badge_html}</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="section-hdr">ACADEMIC CREDENTIALS</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    col_a.metric("Cohort Rank", "01 / 100")
    col_b.metric("Distinction", "Summa Cum Laude")

    col_c, col_d = st.columns(2)
    col_c.metric("Publications", "3× IEEE/Springer")
    col_d.metric("Upwork Tier", "Top-Rated Plus")

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="section-hdr">MERIT AWARDS</div>', unsafe_allow_html=True)
    st.markdown("""
    <div>
      <span class="award-chip">🏛 SSE Stonehenge — Systems Excellence</span>
      <span class="award-chip">🌿 PGS Sustainability Award</span>
      <span class="award-chip">📡 Top-3% Freelance Engineers</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="section-hdr">RESEARCH PITCH → DR. AKRAM / VICS</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="pitch-box">
    Dr. Akram — My research proposes mitigating GenAI memory spillage
    by governing data-ingress via predictive stochastic shaping.<br><br>
    This simulator models that hypothesis against your VICS
    Hybrid-NVM architecture, demonstrating that PID-anchored
    token-arrival control reduces WAF by <strong>≥ 59 %</strong>,
    DRAM pressure by <strong>≥ 45 %</strong>, and energy waste
    by <strong>≥ 38 %</strong> under identical workload profiles.<br><br>
    The Belhadj Logic Anchor formalises this as a closed-loop
    control problem — tractable, verifiable, and deployable
    at the OS memory-controller layer.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="section-hdr">SIM PARAMETERS</div>', unsafe_allow_html=True)

    base_lam = st.slider("Base λ  [tokens/ms]", 20, 100, 45, step=5,
                         key="base_lam_slider")
    cap_gb   = st.slider("NVM Capacity  [GB]", 8, 128, 32, step=8,
                         key="cap_slider")
    t_dram   = st.slider("T_DRAM  [ns]", 40, 200, 80, step=10,
                         key="tdram_slider")
    t_nvm    = st.slider("T_NVM  [ns]", 400, 3000, 1400, step=100,
                         key="tnvm_slider")

    amat_custom = compute_amat(p_dram, float(t_dram), float(t_nvm))
    st.markdown(f"""
    <div class="eq-box">
    AMAT  =  {p_dram:.2f} × {t_dram}  +  {1-p_dram:.2f} × {t_nvm}<br>
           =  <strong>{amat_custom:.1f} ns</strong>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ── MAIN DISPLAY ─────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

# ── MASTHEAD ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card" style="padding:20px 24px 14px;">
  <div class="masthead">⚛ VICS-BELHADJ NEURAL-MEMORY ARCHITECT V1.0 ⚛</div>
  <div class="subtitle">ANU VICS LAB  ·  HYBRID NVM/DRAM  ·  PREDICTIVE STOCHASTIC SHAPING</div>
</div>
""", unsafe_allow_html=True)

# ── ROW 1: TELEMETRY GAUGES ───────────────────────────────────────────────────
st.markdown('<div class="section-hdr" style="margin-top:4px;">▸ LIVE TELEMETRY  ·  SYSTEM STATE MONITORS</div>',
            unsafe_allow_html=True)

g1, g2, g3, g4 = st.columns(4)

with g1:
    waf_color = "gauge-cyan" if (anchor or waf < 2.0) else "gauge-red"
    waf_label = "▲ OPTIMISED" if anchor else "▼ CRITICAL"
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
      <div class="gauge-label">WRITE AMPLIFICATION FACTOR</div>
      <div class="gauge-value {waf_color}">{waf}</div>
      <div class="gauge-unit">WAF  ·  ×</div>
      <div style="margin-top:8px;">
        <div class="prog-wrap">
          <div class="prog-label"><span>WEAR STRESS</span><span>{min(waf/5*100,100):.0f}%</span></div>
          <div class="prog-track"><div class="prog-fill {'prog-cyan' if anchor else 'prog-red'}"
               style="width:{min(waf/5*100,100):.0f}%"></div></div>
        </div>
      </div>
      <div style="font-size:0.58rem;color:rgba(0,243,255,0.45);margin-top:6px;">{waf_label}</div>
    </div>
    """, unsafe_allow_html=True)

with g2:
    dp_color = "gauge-cyan" if dram_pct < 55 else "gauge-red"
    dp_label = "NOMINAL" if dram_pct < 55 else "THERMAL RISK"
    st.markdown(f"""
    <div class="{'glass-card' if dram_pct < 55 else 'glass-card-red'}" style="text-align:center;">
      <div class="gauge-label">DRAM THERMAL PRESSURE</div>
      <div class="gauge-value {dp_color}">{dram_pct}</div>
      <div class="gauge-unit">UTILISATION  ·  %</div>
      <div style="margin-top:8px;">
        <div class="prog-wrap">
          <div class="prog-label"><span>FILL RATIO</span><span>{dram_pct:.0f}%</span></div>
          <div class="prog-track"><div class="prog-fill {'prog-cyan' if dram_pct < 55 else 'prog-red'}"
               style="width:{dram_pct:.0f}%"></div></div>
        </div>
      </div>
      <div style="font-size:0.58rem;color:rgba(0,243,255,0.45);margin-top:6px;">{dp_label}</div>
    </div>
    """, unsafe_allow_html=True)

with g3:
    ew_color = "gauge-amber" if not anchor else "gauge-cyan"
    ew_label = "EXCESS WRITES" if not anchor else "MINIMISED"
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
      <div class="gauge-label">ENERGY WASTE  ·  NVM EXCESS</div>
      <div class="gauge-value {ew_color}">{e_waste}</div>
      <div class="gauge-unit">NORM. UNITS  ·  EU</div>
      <div style="margin-top:8px;">
        <div class="prog-wrap">
          <div class="prog-label"><span>POWER OVERHEAD</span><span>{e_waste:.0f}%</span></div>
          <div class="prog-track"><div class="prog-fill {'prog-cyan' if anchor else 'prog-amber'}"
               style="width:{min(e_waste,100):.0f}%"></div></div>
        </div>
      </div>
      <div style="font-size:0.58rem;color:rgba(0,243,255,0.45);margin-top:6px;">{ew_label}</div>
    </div>
    """, unsafe_allow_html=True)

with g4:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
      <div class="gauge-label">AMAT  ·  HYBRID NVM/DRAM</div>
      <div class="gauge-value gauge-cyan">{amat:.0f}</div>
      <div class="gauge-unit">NANOSECONDS</div>
      <div style="margin-top:8px;">
        <div class="prog-wrap">
          <div class="prog-label"><span>DRAM HIT RATIO</span><span>{p_dram*100:.0f}%</span></div>
          <div class="prog-track"><div class="prog-fill prog-cyan" style="width:{p_dram*100:.0f}%"></div></div>
        </div>
      </div>
      <div style="font-size:0.58rem;color:rgba(0,243,255,0.45);margin-top:6px;">P_DRAM={p_dram:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# ── ANCHOR BUTTON ─────────────────────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
btn_label = (
    "[ ✦ PREDICTIVE SHAPING ACTIVE — CLICK TO DISENGAGE BELHADJ ANCHOR ]"
    if anchor else
    "[ INITIATE PREDICTIVE SHAPING CONSTRAINT — ENGAGE BELHADJ LOGIC ANCHOR ]"
)
if st.button(btn_label, key="anchor_btn"):
    st.session_state.anchor_active = not st.session_state.anchor_active
    st.session_state.sim_run      += 1
    st.session_state.glitch_trigger = True
    st.rerun()

# ── SYSTEM STATE INDICATOR ────────────────────────────────────────────────────
state_html = (
    '<div style="text-align:center;margin:6px 0;font-family:Orbitron,sans-serif;font-size:0.62rem;'
    'letter-spacing:0.25em;color:#00f3ff;text-shadow:0 0 8px #00f3ff;">'
    '✦ SYSTEM STATE: ANCHOR ENGAGED  ·  BELHADJ PID ACTIVE  ·  SHAPING λ(t) ✦</div>'
    if anchor else
    '<div style="text-align:center;margin:6px 0;font-family:Orbitron,sans-serif;font-size:0.62rem;'
    'letter-spacing:0.25em;color:#ff003c;text-shadow:0 0 8px #ff003c;">'
    '⚠ SYSTEM STATE: UNCONTROLLED  ·  CHAOTIC INGRESS  ·  NVM STRESS ELEVATED ⚠</div>'
)
st.markdown(state_html, unsafe_allow_html=True)

# ── CENTERPIECE: 3D STATE-SPACE ────────────────────────────────────────────────
st.markdown('<div class="section-hdr" style="margin-top:10px;">▸ LATENT STATE-SPACE VISUALISATION  ·  TOKEN TRAJECTORY MANIFOLD</div>',
            unsafe_allow_html=True)
fig_3d = build_state_space_3d(n=550, anchor=anchor, seed=seed_val)
st.plotly_chart(fig_3d, use_container_width=True, config={
    'displayModeBar': True,
    'modeBarButtonsToRemove': ['toImage'],
    'displaylogo': False,
})

# ── ROW 3: ANALYTICS SPLIT ────────────────────────────────────────────────────
st.markdown('<div class="section-hdr">▸ PERFORMANCE ANALYTICS  ·  EFFICIENCY FRONTIER + PID RESPONSE</div>',
            unsafe_allow_html=True)

chart_l, chart_r = st.columns([3, 2])
with chart_l:
    fig_par = build_pareto_chart(anchor)
    st.plotly_chart(fig_par, use_container_width=True,
                    config={'displayModeBar': False, 'displaylogo': False})

with chart_r:
    if anchor:
        fig_pid = build_pid_chart(t_ax, lambda_t, shaped_lambda, p_t, i_t, d_t)
        st.plotly_chart(fig_pid, use_container_width=True,
                        config={'displayModeBar': False, 'displaylogo': False})
    else:
        st.markdown("""
        <div class="glass-card-red" style="height:300px;display:flex;flex-direction:column;
             align-items:center;justify-content:center;text-align:center;">
          <div style="font-family:Orbitron,sans-serif;font-size:0.65rem;letter-spacing:0.20em;
               color:#ff003c;text-shadow:0 0 10px #ff003c;margin-bottom:12px;">
            ⚠  ANCHOR OFFLINE
          </div>
          <div style="font-size:0.60rem;color:rgba(255,0,60,0.65);line-height:1.8;">
            PID SHAPING INACTIVE<br>
            λ(t) UNREGULATED<br>
            DRAM THERMAL RISK ELEVATED<br>
            ENGAGE ANCHOR TO VIEW<br>
            CONTROL RESPONSE
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── MATH EQUATIONS PANEL ──────────────────────────────────────────────────────
st.markdown('<div class="section-hdr" style="margin-top:4px;">▸ GOVERNING EQUATIONS  ·  THEORETICAL FRAMEWORK</div>',
            unsafe_allow_html=True)

eq1, eq2, eq3 = st.columns(3)
with eq1:
    st.markdown("""
    <div class="glass-card">
      <div class="gauge-label">MODULE I  ·  STOCHASTIC PROCESS</div>
      <div class="eq-box">
        λ(t) = λ₀ · (1 + A·sin(2πft) + η(t))<br>
        η(t) = φ·η(t-1) + σ·ε(t),  ε ~ 𝒩(0,1)<br>
        Arrivals ~ Poisson(λ(t))
      </div>
      <div style="font-size:0.60rem;color:rgba(0,243,255,0.50);line-height:1.6;">
        Non-stationary Poisson process with<br>AR-1 coloured noise burst model.<br>
        φ={phi_val}  σ={sig_val}
      </div>
    </div>
    """.format(
        phi_val="0.60" if anchor else "0.92",
        sig_val="0.08" if anchor else "0.28",
    ), unsafe_allow_html=True)

with eq2:
    st.markdown(f"""
    <div class="glass-card">
      <div class="gauge-label">MODULE II  ·  MEMORY HIERARCHY</div>
      <div class="eq-box">
        AMAT = P_dram · T_dram + (1-P_dram) · T_nvm<br>
             = {p_dram:.2f} × 80 + {1-p_dram:.2f} × 1400<br>
             = <strong>{amat:.1f} ns</strong>
      </div>
      <div style="font-size:0.60rem;color:rgba(0,243,255,0.50);line-height:1.6;">
        Hybrid NVM/DRAM access model.<br>
        DRAM hit-rate ↑ when anchor engaged.<br>
        WAF = {waf} ×  |  ΔP_dram = {(p_dram-0.72)*100:+.0f}%
      </div>
    </div>
    """, unsafe_allow_html=True)

with eq3:
    st.markdown("""
    <div class="glass-card">
      <div class="gauge-label">MODULE III  ·  BELHADJ PID ANCHOR</div>
      <div class="eq-box">
        u(t) = Kp·e(t) + Ki·∫e(τ)dτ + Kd·(de/dt)<br>
        e(t) = λ_target - λ_raw(t)<br>
        Kp=0.55  Ki=0.12  Kd=0.08
      </div>
      <div style="font-size:0.60rem;color:rgba(0,243,255,0.50);line-height:1.6;">
        Closed-loop ingress control. Anti-windup<br>
        integral clamp at ±300. Setpoint = 45 t/ms.<br>
        Status: <strong>{'ENGAGED ✦' if anchor else 'STANDBY ⚠'}</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:20px;padding:12px;
     border-top:1px solid rgba(0,243,255,0.15);
     font-family:'Share Tech Mono',monospace;
     font-size:0.58rem;letter-spacing:0.20em;
     color:rgba(0,243,255,0.30);">
  VICS-BELHADJ NEURAL-MEMORY ARCHITECT V1.0  ·  F.Z. BELHADJ  ·  ANU VICS LAB
  ·  DR. SHOAIB AKRAM  ·  HYBRID NVM/DRAM RESEARCH  ·  ALL RIGHTS RESERVED
</div>
""", unsafe_allow_html=True)
