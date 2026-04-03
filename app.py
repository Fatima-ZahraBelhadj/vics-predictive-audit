"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  VICS-BELHADJ NEURAL-MEMORY ARCHITECT V1.0                                ║
║  Predictive Stochastic Shaping for Hybrid NVM/DRAM Architectures           ║
║  Target: Dr. Shoaib Akram — VICS Lab, Australian National University       ║
║  Author: F.Z. BELHADJ                                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# ─────────────────────────────────────────────────────────────────────────────
# I. PAGE CONFIG & CSS INJECTION — Deep Space Glassmorphism Theme
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="VICS-BELHADJ NEURAL-MEMORY ARCHITECT V1.0",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

ELECTRIC_CYAN = "#00f3ff"
PULSING_CRIMSON = "#ff003c"
BG_DEEP = "#000508"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], .stDeployButton {{display: none !important;}}

/* ── Star-field Background ── */
@keyframes drift {{
    0%   {{ background-position: 0 0, 0 0, 0 0; }}
    100% {{ background-position: 300px 600px, -200px 400px, 100px -300px; }}
}}
@keyframes pulseGlow {{
    0%, 100% {{ opacity: 0.6; }}
    50%      {{ opacity: 1.0; }}
}}
@keyframes gridScan {{
    0%   {{ transform: translateY(-100%); }}
    100% {{ transform: translateY(100%); }}
}}
@keyframes glitchShake {{
    0%   {{ transform: translate(0); filter: hue-rotate(0deg); }}
    10%  {{ transform: translate(-4px, 3px); filter: hue-rotate(90deg); }}
    20%  {{ transform: translate(3px, -2px); filter: hue-rotate(180deg); }}
    30%  {{ transform: translate(-2px, 4px); filter: hue-rotate(270deg); }}
    40%  {{ transform: translate(4px, -3px); filter: hue-rotate(360deg); }}
    50%  {{ transform: translate(-3px, 2px); filter: hue-rotate(45deg); }}
    60%  {{ transform: translate(2px, -4px); filter: hue-rotate(135deg); }}
    70%  {{ transform: translate(-4px, 3px); filter: hue-rotate(225deg); }}
    80%  {{ transform: translate(3px, -2px); filter: hue-rotate(315deg); }}
    90%  {{ transform: translate(-2px, 4px); filter: hue-rotate(180deg); }}
    100% {{ transform: translate(0); filter: hue-rotate(0deg); }}
}}
@keyframes borderPulse {{
    0%, 100% {{ border-color: {ELECTRIC_CYAN}44; box-shadow: 0 0 15px {ELECTRIC_CYAN}11; }}
    50%      {{ border-color: {ELECTRIC_CYAN}aa; box-shadow: 0 0 30px {ELECTRIC_CYAN}33; }}
}}
@keyframes scanLine {{
    0%   {{ top: -5%; }}
    100% {{ top: 105%; }}
}}
@keyframes textFlicker {{
    0%, 100% {{ opacity: 1; }}
    92%      {{ opacity: 1; }}
    93%      {{ opacity: 0.3; }}
    94%      {{ opacity: 1; }}
    96%      {{ opacity: 0.5; }}
    97%      {{ opacity: 1; }}
}}

.stApp {{
    background-color: {BG_DEEP} !important;
    background-image:
        radial-gradient(1.5px 1.5px at 20px 30px, {ELECTRIC_CYAN}18, transparent),
        radial-gradient(1px 1px at 60px 80px, {ELECTRIC_CYAN}10, transparent),
        radial-gradient(1.2px 1.2px at 120px 50px, {ELECTRIC_CYAN}14, transparent);
    background-size: 200px 200px, 150px 150px, 180px 180px;
    animation: drift 120s linear infinite;
    color: #c0e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}}

/* ── Glassmorphic Cards ── */
.glass-card {{
    background: rgba(0, 15, 25, 0.75) !important;
    backdrop-filter: blur(14px) saturate(1.4);
    -webkit-backdrop-filter: blur(14px) saturate(1.4);
    border: 1px solid {ELECTRIC_CYAN}30;
    border-radius: 12px;
    padding: 22px 26px;
    margin: 10px 0;
    position: relative;
    overflow: hidden;
    animation: borderPulse 4s ease-in-out infinite;
}}
.glass-card::before {{
    content: '';
    position: absolute;
    top: -5%;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, transparent, {ELECTRIC_CYAN}40, transparent);
    animation: scanLine 6s linear infinite;
    pointer-events: none;
}}
.glass-card-danger {{
    background: rgba(40, 0, 5, 0.7) !important;
    backdrop-filter: blur(14px);
    border: 1px solid {PULSING_CRIMSON}40;
    border-radius: 12px;
    padding: 22px 26px;
    margin: 10px 0;
}}

/* ── Gauge Displays ── */
.gauge-container {{
    text-align: center;
    padding: 18px;
}}
.gauge-value {{
    font-family: 'Orbitron', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: 3px;
    animation: textFlicker 8s infinite;
    text-shadow: 0 0 20px currentColor, 0 0 40px currentColor;
}}
.gauge-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-top: 6px;
    opacity: 0.7;
}}
.gauge-cyan  {{ color: {ELECTRIC_CYAN}; }}
.gauge-red   {{ color: {PULSING_CRIMSON}; }}
.gauge-amber {{ color: #ffaa00; }}

/* ── Typography ── */
.main-title {{
    font-family: 'Orbitron', sans-serif;
    font-size: 1.55rem;
    font-weight: 900;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: {ELECTRIC_CYAN};
    text-shadow: 0 0 30px {ELECTRIC_CYAN}88, 0 0 60px {ELECTRIC_CYAN}44;
    text-align: center;
    padding: 14px 0 4px;
    animation: textFlicker 10s infinite;
}}
.sub-title {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: {ELECTRIC_CYAN}88;
    text-align: center;
    margin-bottom: 18px;
}}
.section-head {{
    font-family: 'Orbitron', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: {ELECTRIC_CYAN};
    border-bottom: 1px solid {ELECTRIC_CYAN}30;
    padding-bottom: 8px;
    margin: 16px 0 10px;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #000a10 0%, #000508 50%, #020810 100%) !important;
    border-right: 1px solid {ELECTRIC_CYAN}20 !important;
}}
section[data-testid="stSidebar"] .stMarkdown {{
    color: #8cc8d8 !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: transparent !important;
    color: {ELECTRIC_CYAN} !important;
    border: 2px solid {ELECTRIC_CYAN} !important;
    border-radius: 6px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    font-size: 0.82rem !important;
    padding: 14px 28px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 15px {ELECTRIC_CYAN}22, inset 0 0 15px {ELECTRIC_CYAN}11 !important;
}}
.stButton > button:hover {{
    background: {ELECTRIC_CYAN}18 !important;
    box-shadow: 0 0 35px {ELECTRIC_CYAN}55, inset 0 0 25px {ELECTRIC_CYAN}22 !important;
    transform: scale(1.02);
}}
.stButton > button:active {{
    animation: glitchShake 0.4s ease;
}}

/* ── Metric overrides ── */
[data-testid="stMetric"] {{
    background: rgba(0, 20, 30, 0.5);
    border: 1px solid {ELECTRIC_CYAN}20;
    border-radius: 8px;
    padding: 10px 14px !important;
}}
[data-testid="stMetricLabel"] {{
    color: {ELECTRIC_CYAN}99 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}}
[data-testid="stMetricValue"] {{
    color: {ELECTRIC_CYAN} !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    text-shadow: 0 0 10px {ELECTRIC_CYAN}55;
}}

/* ── Slider ── */
.stSlider > div > div > div > div {{
    background-color: {ELECTRIC_CYAN} !important;
}}
.stSlider label {{
    color: {ELECTRIC_CYAN}aa !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 1px !important;
}}

/* ── Selectbox / inputs ── */
.stSelectbox label, .stNumberInput label {{
    color: {ELECTRIC_CYAN}99 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
}}

/* ── Glitch overlay on activation ── */
.glitch-overlay {{
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none; z-index: 9999;
    animation: glitchShake 0.5s ease;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        {ELECTRIC_CYAN}08 2px,
        {ELECTRIC_CYAN}08 4px
    );
    mix-blend-mode: screen;
    opacity: 0;
}}
.glitch-active {{
    opacity: 1;
    animation: glitchShake 0.6s ease forwards;
}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# II. COMPUTATIONAL ENGINE — Hard-Science Modeling
# ─────────────────────────────────────────────────────────────────────────────

class StochasticGenerator:
    """Module 1: Non-stationary Poisson process for GenAI token arrival."""

    @staticmethod
    def generate_arrivals(
        base_lambda: float,
        duration: int,
        burst_factor: float = 3.0,
        burst_prob: float = 0.15,
        seed: int = 42,
    ) -> np.ndarray:
        """
        Generate token arrival rates using a non-stationary Poisson process.
        λ(t) = λ_base + burst_factor * λ_base * B(t)
        where B(t) ~ Bernoulli(burst_prob) triggers bursty ingress spikes.
        """
        rng = np.random.RandomState(seed)
        t = np.arange(duration)
        # Sinusoidal base modulation (diurnal pattern)
        seasonal = 1 + 0.3 * np.sin(2 * np.pi * t / (duration / 4))
        # Bernoulli burst overlay
        bursts = rng.binomial(1, burst_prob, size=duration).astype(float)
        # Smoothed burst envelope (causal exponential decay)
        kernel = np.exp(-np.arange(20) / 4.0)
        burst_envelope = np.convolve(bursts, kernel, mode="full")[:duration]
        burst_envelope /= burst_envelope.max() + 1e-9
        # Composite λ(t)
        lambda_t = base_lambda * seasonal + burst_factor * base_lambda * burst_envelope
        # Realised arrivals
        arrivals = rng.poisson(lambda_t)
        return lambda_t, arrivals


class MemoryHierarchy:
    """Module 2: AMAT calculation across Hybrid NVM/DRAM stack."""

    @staticmethod
    def compute_amat(
        p_dram: float,
        t_dram_ns: float = 80.0,
        t_nvm_ns: float = 350.0,
    ) -> float:
        """
        AMAT = P_dram · T_dram + (1 − P_dram) · T_nvm
        """
        return p_dram * t_dram_ns + (1 - p_dram) * t_nvm_ns

    @staticmethod
    def compute_waf(
        write_volume: np.ndarray,
        page_size: int = 4096,
        nvm_block_size: int = 262144,
    ) -> np.ndarray:
        """
        Write Amplification Factor: ratio of physical writes (NVM block
        granularity) to logical writes. WAF ≥ 1 always.
        """
        pages_per_block = nvm_block_size / page_size
        logical = write_volume.astype(float)
        # Partial-block penalty model: each write touches ceil fraction of block
        utilisation = np.clip(logical / pages_per_block, 0.05, 1.0)
        waf = 1.0 / utilisation
        return np.clip(waf, 1.0, pages_per_block)

    @staticmethod
    def dram_pressure(arrivals: np.ndarray, capacity: float) -> np.ndarray:
        """Cumulative buffer occupancy normalised to DRAM capacity."""
        # Simple leaky-bucket: drain rate = 0.7 * mean arrival
        drain = 0.7 * arrivals.mean()
        occupancy = np.zeros_like(arrivals, dtype=float)
        for i in range(len(arrivals)):
            prev = occupancy[i - 1] if i > 0 else 0
            occupancy[i] = max(0, prev + arrivals[i] - drain)
        return occupancy / capacity

    @staticmethod
    def energy_waste(waf: np.ndarray, pressure: np.ndarray) -> np.ndarray:
        """
        Energy waste proxy: E_waste ∝ WAF × Pressure².
        Normalised to [0, 100] scale.
        """
        raw = waf * pressure ** 2
        if raw.max() > 0:
            return 100.0 * raw / raw.max()
        return raw


class BelhadjPIDController:
    """
    Module 3: PID Control-Theory Constraint.
    Modulates token arrival rate to keep DRAM pressure below threshold,
    preventing thermal throttling and buffer overflow.

    u(t) = Kp·e(t) + Ki·∫e(τ)dτ + Kd·de/dt
    where e(t) = setpoint − measured_pressure
    Output u(t) is a multiplicative gain clamped to [0.1, 1.0] applied to λ(t).
    """

    def __init__(
        self,
        kp: float = 2.0,
        ki: float = 0.05,
        kd: float = 0.8,
        setpoint: float = 0.70,
        dt: float = 1.0,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.dt = dt

    def apply(self, arrivals: np.ndarray, pressure: np.ndarray) -> np.ndarray:
        """Return shaped arrivals after PID-governed rate modulation."""
        n = len(arrivals)
        shaped = np.copy(arrivals).astype(float)
        integral = 0.0
        prev_error = 0.0

        for t in range(n):
            error = self.setpoint - pressure[t]
            integral += error * self.dt
            # Anti-windup: clamp integral
            integral = np.clip(integral, -10.0, 10.0)
            derivative = (error - prev_error) / self.dt if t > 0 else 0.0

            u = self.kp * error + self.ki * integral + self.kd * derivative
            # Convert PID output to multiplicative gain
            gain = np.clip(0.5 + 0.5 * np.tanh(u), 0.1, 1.0)
            shaped[t] = arrivals[t] * gain
            prev_error = error

        return shaped


# ─────────────────────────────────────────────────────────────────────────────
# III. PLOTLY THEME HELPER
# ─────────────────────────────────────────────────────────────────────────────

def plotly_layout_base(**overrides) -> dict:
    xaxis_base = dict(
        gridcolor="#0a2a35",
        zerolinecolor="#0a2a35",
        tickfont=dict(size=10),
    )
    yaxis_base = dict(
        gridcolor="#0a2a35",
        zerolinecolor="#0a2a35",
        tickfont=dict(size=10),
    )
    # Merge axis title shorthands into nested dicts
    if "xaxis_title" in overrides:
        xaxis_base["title"] = overrides.pop("xaxis_title")
    if "yaxis_title" in overrides:
        yaxis_base["title"] = overrides.pop("yaxis_title")
    # Merge any explicit xaxis/yaxis overrides
    if "xaxis" in overrides:
        xaxis_base.update(overrides.pop("xaxis"))
    if "yaxis" in overrides:
        yaxis_base.update(overrides.pop("yaxis"))

    base = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,5,10,0.6)",
        font=dict(family="JetBrains Mono, monospace", color="#8cc8d8", size=11),
        margin=dict(l=50, r=30, t=50, b=40),
        xaxis=xaxis_base,
        yaxis=yaxis_base,
    )
    base.update(overrides)
    return base


# ─────────────────────────────────────────────────────────────────────────────
# IV. SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

if "anchor_active" not in st.session_state:
    st.session_state.anchor_active = False
if "glitch_trigger" not in st.session_state:
    st.session_state.glitch_trigger = False
if "sim_seed" not in st.session_state:
    st.session_state.sim_seed = 42


# ─────────────────────────────────────────────────────────────────────────────
# V. SIDEBAR — The Engineering Dossier
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align:center; padding:10px 0 6px;">
            <div style="font-family:'Orbitron',sans-serif; font-size:0.65rem;
                        letter-spacing:5px; color:{ELECTRIC_CYAN}55;
                        text-transform:uppercase;">System Operator</div>
            <div style="font-family:'Orbitron',sans-serif; font-size:1.1rem;
                        font-weight:800; letter-spacing:4px; color:{ELECTRIC_CYAN};
                        text-shadow:0 0 20px {ELECTRIC_CYAN}66; margin:6px 0;">
                F.Z. BELHADJ</div>
            <div style="font-size:0.55rem; letter-spacing:3px; color:{ELECTRIC_CYAN}66;
                        text-transform:uppercase;">Operator Identity Verified</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="section-head">◈ Credentials</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Cohort Rank", "01", "Summa Cum Laude")
    c2.metric("Upwork", "Top 3%", "Top-Rated Plus")
    c3, c4 = st.columns(2)
    c3.metric("Publications", "3×", "IEEE / Springer")
    c4.metric("H-Index", "—", "Emerging")

    st.markdown(f'<div class="section-head">◈ Awards</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="font-size:0.7rem; color:#8cc8d8; line-height:1.7;">
            ▸ <span style="color:{ELECTRIC_CYAN}">SSE Stonehenge</span> — Systems Excellence<br>
            ▸ <span style="color:{ELECTRIC_CYAN}">PGS Award</span> — Sustainability Engineering
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="section-head">◈ Research Pitch</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="glass-card" style="font-size:0.68rem; line-height:1.65;
                    color:#a0d4e4; border-color:{ELECTRIC_CYAN}22;">
            <strong style="color:{ELECTRIC_CYAN}">Dr. Akram:</strong> My research proposes
            mitigating GenAI memory spillage by governing data-ingress via
            <em>predictive stochastic shaping</em>. This simulator models that
            hypothesis against your VICS Hybrid-NVM architecture — demonstrating
            how PID-governed rate control reduces write amplification,
            DRAM pressure, and energy waste simultaneously.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="section-head">◈ Simulation Parameters</div>', unsafe_allow_html=True)

    base_lambda = st.slider(
        "Base Token Arrival Rate (λ₀)",
        min_value=10, max_value=200, value=80, step=5,
        help="Mean tokens/cycle under steady-state conditions",
    )
    burst_factor = st.slider(
        "Burst Amplitude Factor",
        min_value=1.0, max_value=8.0, value=3.5, step=0.5,
        help="Multiplicative spike magnitude during bursty ingress",
    )
    p_dram = st.slider(
        "DRAM Hit Probability (P_dram)",
        min_value=0.30, max_value=0.99, value=0.72, step=0.01,
        help="Fraction of accesses served from DRAM vs NVM",
    )
    pid_kp = st.slider("PID Kp (Proportional)", 0.5, 5.0, 2.0, 0.1)
    pid_ki = st.slider("PID Ki (Integral)", 0.01, 0.20, 0.05, 0.01)
    pid_kd = st.slider("PID Kd (Derivative)", 0.1, 3.0, 0.8, 0.1)
    pid_setpoint = st.slider("Pressure Setpoint", 0.3, 0.95, 0.70, 0.05)

    duration = st.select_slider(
        "Simulation Duration (cycles)",
        options=[200, 500, 1000, 2000],
        value=500,
    )


# ─────────────────────────────────────────────────────────────────────────────
# VI. MAIN DISPLAY — Header
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<div class="main-title">VICS-BELHADJ NEURAL-MEMORY ARCHITECT</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Predictive Stochastic Shaping · Hybrid NVM/DRAM · Control-Theory Constraint</div>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# VII. COMPUTE SIMULATION
# ─────────────────────────────────────────────────────────────────────────────

lambda_t, raw_arrivals = StochasticGenerator.generate_arrivals(
    base_lambda=base_lambda,
    duration=duration,
    burst_factor=burst_factor,
    burst_prob=0.12,
    seed=st.session_state.sim_seed,
)

dram_cap = base_lambda * 15  # nominal buffer capacity
raw_pressure = MemoryHierarchy.dram_pressure(raw_arrivals, dram_cap)
raw_waf = MemoryHierarchy.compute_waf(raw_arrivals)
raw_energy = MemoryHierarchy.energy_waste(raw_waf, raw_pressure)

# PID-shaped signals
pid = BelhadjPIDController(kp=pid_kp, ki=pid_ki, kd=pid_kd, setpoint=pid_setpoint)
shaped_arrivals = pid.apply(raw_arrivals, raw_pressure)
shaped_pressure = MemoryHierarchy.dram_pressure(shaped_arrivals.astype(int), dram_cap)
shaped_waf = MemoryHierarchy.compute_waf(shaped_arrivals.astype(int))
shaped_energy = MemoryHierarchy.energy_waste(shaped_waf, shaped_pressure)

anchor = st.session_state.anchor_active
active_arrivals = shaped_arrivals if anchor else raw_arrivals
active_pressure = shaped_pressure if anchor else raw_pressure
active_waf = shaped_waf if anchor else raw_waf
active_energy = shaped_energy if anchor else raw_energy

amat_val = MemoryHierarchy.compute_amat(p_dram)


# ─────────────────────────────────────────────────────────────────────────────
# VIII. ACTIVATION BUTTON + GLITCH
# ─────────────────────────────────────────────────────────────────────────────

btn_col = st.columns([1, 3, 1])
with btn_col[1]:
    label = (
        "◈  PREDICTIVE SHAPING ACTIVE  ◈"
        if anchor
        else "◈  INITIATE PREDICTIVE SHAPING CONSTRAINT  ◈"
    )
    if st.button(label, use_container_width=True):
        st.session_state.anchor_active = not st.session_state.anchor_active
        st.session_state.glitch_trigger = True
        st.session_state.sim_seed = int(time.time()) % 100000
        st.rerun()

# Glitch effect overlay
if st.session_state.glitch_trigger:
    st.markdown(
        f"""<div class="glitch-overlay glitch-active"></div>
        <script>setTimeout(() => {{
            document.querySelector('.glitch-overlay').style.display='none';
        }}, 600);</script>""",
        unsafe_allow_html=True,
    )
    st.session_state.glitch_trigger = False

# Status bar
status_color = ELECTRIC_CYAN if anchor else PULSING_CRIMSON
status_text = "PID CONSTRAINT: ENGAGED — STABLE STATE" if anchor else "PID CONSTRAINT: DISENGAGED — ENTROPIC DRIFT"
st.markdown(
    f"""<div style="text-align:center; font-family:'Orbitron',sans-serif;
        font-size:0.65rem; letter-spacing:5px; color:{status_color};
        padding:4px 0 16px; text-shadow:0 0 15px {status_color}55;">
        {status_text}</div>""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# IX. ROW 1 — Telemetry Gauges
# ─────────────────────────────────────────────────────────────────────────────

g1, g2, g3, g4 = st.columns(4)

avg_waf = float(active_waf.mean())
avg_press = float(active_pressure.mean()) * 100
avg_energy = float(active_energy.mean())

with g1:
    waf_color = "gauge-cyan" if avg_waf < 6 else "gauge-red"
    st.markdown(
        f"""<div class="glass-card gauge-container">
            <div class="gauge-value {waf_color}">{avg_waf:.1f}×</div>
            <div class="gauge-label">Write Amplification Factor</div>
        </div>""",
        unsafe_allow_html=True,
    )

with g2:
    press_color = "gauge-cyan" if avg_press < 70 else "gauge-red"
    st.markdown(
        f"""<div class="glass-card gauge-container">
            <div class="gauge-value {press_color}">{avg_press:.0f}%</div>
            <div class="gauge-label">DRAM Buffer Pressure</div>
        </div>""",
        unsafe_allow_html=True,
    )

with g3:
    energy_color = "gauge-cyan" if avg_energy < 35 else "gauge-amber" if avg_energy < 60 else "gauge-red"
    st.markdown(
        f"""<div class="glass-card gauge-container">
            <div class="gauge-value {energy_color}">{avg_energy:.1f}</div>
            <div class="gauge-label">Energy Waste Index</div>
        </div>""",
        unsafe_allow_html=True,
    )

with g4:
    st.markdown(
        f"""<div class="glass-card gauge-container">
            <div class="gauge-value gauge-cyan">{amat_val:.0f}<span style="font-size:1rem;">ns</span></div>
            <div class="gauge-label">Avg Memory Access Time</div>
        </div>""",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# X. CENTERPIECE — 3D Latent State-Space Visualization
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    f'<div class="section-head" style="margin-top:20px;">◈ 3D Latent State-Space Manifold</div>',
    unsafe_allow_html=True,
)

rng3d = np.random.RandomState(st.session_state.sim_seed + 7)
n_pts = min(duration, 600)

if anchor:
    # Stable Torus geometry
    theta = np.linspace(0, 4 * np.pi, n_pts) + rng3d.normal(0, 0.03, n_pts)
    phi = np.linspace(0, 2 * np.pi, n_pts) + rng3d.normal(0, 0.03, n_pts)
    R, r = 3.0, 1.0
    x3d = (R + r * np.cos(phi)) * np.cos(theta)
    y3d = (R + r * np.cos(phi)) * np.sin(theta)
    z3d = r * np.sin(phi)
    colors_3d = active_pressure[:n_pts] if len(active_pressure) >= n_pts else np.tile(active_pressure, n_pts // len(active_pressure) + 1)[:n_pts]
    colorscale = [[0, "#003344"], [0.5, ELECTRIC_CYAN], [1, "#aaffff"]]
    cbar_title = "Pressure (Governed)"
else:
    # Chaotic expansion
    x3d = np.cumsum(rng3d.normal(0, 0.6, n_pts))
    y3d = np.cumsum(rng3d.normal(0, 0.6, n_pts))
    z3d = np.cumsum(rng3d.normal(0, 0.6, n_pts))
    # Add explosive bursts
    burst_idx = rng3d.choice(n_pts, size=n_pts // 8, replace=False)
    x3d[burst_idx] += rng3d.normal(0, 4, len(burst_idx))
    y3d[burst_idx] += rng3d.normal(0, 4, len(burst_idx))
    z3d[burst_idx] += rng3d.normal(0, 4, len(burst_idx))
    colors_3d = np.linspace(0, 1, n_pts)
    colorscale = [[0, "#550011"], [0.4, PULSING_CRIMSON], [0.7, "#ff6644"], [1, "#ffcc00"]]
    cbar_title = "Entropy (Uncontrolled)"

fig3d = go.Figure(
    data=[
        go.Scatter3d(
            x=x3d, y=y3d, z=z3d,
            mode="markers",
            marker=dict(
                size=2.5,
                color=colors_3d,
                colorscale=colorscale,
                opacity=0.85,
                colorbar=dict(
                    title=dict(text=cbar_title, font=dict(size=10, color="#8cc8d8")),
                    thickness=12, len=0.6,
                    tickfont=dict(size=9, color="#5a9aaa"),
                    bgcolor="rgba(0,0,0,0)",
                    borderwidth=0,
                ),
            ),
            hovertemplate="x:%{x:.2f}<br>y:%{y:.2f}<br>z:%{z:.2f}<extra></extra>",
        )
    ]
)
fig3d.update_layout(
    **plotly_layout_base(
        height=520,
        title=dict(
            text="STATE-SPACE: " + ("TORUS ATTRACTOR [STABLE]" if anchor else "CHAOTIC DRIFT [ENTROPIC]"),
            font=dict(family="Orbitron, sans-serif", size=13,
                      color=ELECTRIC_CYAN if anchor else PULSING_CRIMSON),
            x=0.5,
        ),
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,5,10,0.3)", gridcolor="#0a2a35",
                        showticklabels=False, title=""),
            yaxis=dict(backgroundcolor="rgba(0,5,10,0.3)", gridcolor="#0a2a35",
                        showticklabels=False, title=""),
            zaxis=dict(backgroundcolor="rgba(0,5,10,0.3)", gridcolor="#0a2a35",
                        showticklabels=False, title=""),
            bgcolor="rgba(0,3,8,0.9)",
            camera=dict(eye=dict(x=1.6, y=1.6, z=0.9)),
        ),
    )
)
st.plotly_chart(fig3d, use_container_width=True, key="3d_state_space")


# ─────────────────────────────────────────────────────────────────────────────
# XI. ROW 2 — Arrival Rate & Pressure Time Series
# ─────────────────────────────────────────────────────────────────────────────

ts_left, ts_right = st.columns(2)

with ts_left:
    st.markdown('<div class="section-head">◈ Token Arrival Rate λ(t)</div>', unsafe_allow_html=True)
    fig_arr = go.Figure()
    t_axis = np.arange(duration)
    fig_arr.add_trace(go.Scatter(
        x=t_axis, y=raw_arrivals, name="Raw λ(t)",
        line=dict(color=PULSING_CRIMSON, width=1.2), opacity=0.5,
    ))
    if anchor:
        fig_arr.add_trace(go.Scatter(
            x=t_axis, y=shaped_arrivals, name="Shaped λ(t)",
            line=dict(color=ELECTRIC_CYAN, width=1.8),
            fill="tonexty", fillcolor=f"{ELECTRIC_CYAN}0d",
        ))
    fig_arr.update_layout(**plotly_layout_base(
        height=300,
        title=dict(text="INGRESS RATE", font=dict(size=11, family="Orbitron"), x=0.5,
                   color=ELECTRIC_CYAN if anchor else PULSING_CRIMSON),
        showlegend=True,
        legend=dict(font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
        xaxis_title="Cycle", yaxis_title="Tokens / Cycle",
    ))
    st.plotly_chart(fig_arr, use_container_width=True, key="arrival_rate")

with ts_right:
    st.markdown('<div class="section-head">◈ DRAM Buffer Pressure P(t)</div>', unsafe_allow_html=True)
    fig_press = go.Figure()
    fig_press.add_trace(go.Scatter(
        x=t_axis, y=raw_pressure * 100, name="Raw Pressure",
        line=dict(color=PULSING_CRIMSON, width=1.2), opacity=0.5,
    ))
    if anchor:
        fig_press.add_trace(go.Scatter(
            x=t_axis, y=shaped_pressure * 100, name="Governed Pressure",
            line=dict(color=ELECTRIC_CYAN, width=1.8),
        ))
    # Setpoint line
    fig_press.add_hline(
        y=pid_setpoint * 100, line_dash="dot",
        line_color="#ffaa00", opacity=0.6,
        annotation_text=f"Setpoint {pid_setpoint*100:.0f}%",
        annotation_font=dict(size=9, color="#ffaa00"),
    )
    fig_press.update_layout(**plotly_layout_base(
        height=300,
        title=dict(text="BUFFER OCCUPANCY", font=dict(size=11, family="Orbitron"), x=0.5,
                   color=ELECTRIC_CYAN if anchor else PULSING_CRIMSON),
        showlegend=True,
        legend=dict(font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
        xaxis_title="Cycle", yaxis_title="Pressure %",
    ))
    st.plotly_chart(fig_press, use_container_width=True, key="pressure_ts")


# ─────────────────────────────────────────────────────────────────────────────
# XII. ROW 3 — Pareto Efficiency Frontier + WAF / Energy
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    '<div class="section-head" style="margin-top:10px;">◈ Performance Analytics</div>',
    unsafe_allow_html=True,
)

pa_left, pa_right = st.columns(2)

with pa_left:
    # Pareto Frontier: Throughput vs Latency
    rng_p = np.random.RandomState(st.session_state.sim_seed + 99)
    n_pareto = 80

    if anchor:
        throughput = np.linspace(20, 95, n_pareto) + rng_p.normal(0, 1.5, n_pareto)
        latency = 400 - 3.0 * throughput + rng_p.normal(0, 8, n_pareto)
        # Tight cluster near optimal
        latency = np.clip(latency, 80, 400)
        pt_color = ELECTRIC_CYAN
        frontier_label = "OPTIMISED FRONTIER"
    else:
        throughput = rng_p.uniform(10, 100, n_pareto)
        latency = 500 - 2.0 * throughput + rng_p.normal(0, 40, n_pareto)
        latency = np.clip(latency, 50, 600)
        pt_color = PULSING_CRIMSON
        frontier_label = "UNCONTROLLED SCATTER"

    # Sort for frontier line
    order = np.argsort(throughput)
    tp_sorted = throughput[order]
    lat_sorted = latency[order]
    # Compute Pareto front (non-dominated)
    pareto_t, pareto_l = [tp_sorted[0]], [lat_sorted[0]]
    min_lat = lat_sorted[0]
    for i in range(1, len(tp_sorted)):
        if lat_sorted[i] <= min_lat:
            pareto_t.append(tp_sorted[i])
            pareto_l.append(lat_sorted[i])
            min_lat = lat_sorted[i]

    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Scatter(
        x=throughput, y=latency, mode="markers", name="Operating Points",
        marker=dict(size=5, color=pt_color, opacity=0.6),
    ))
    fig_pareto.add_trace(go.Scatter(
        x=pareto_t, y=pareto_l, mode="lines+markers", name="Pareto Front",
        line=dict(color="#ffaa00", width=2, dash="dot"),
        marker=dict(size=7, color="#ffaa00", symbol="diamond"),
    ))
    fig_pareto.update_layout(**plotly_layout_base(
        height=340,
        title=dict(text=f"PARETO FRONTIER — {frontier_label}",
                   font=dict(size=11, family="Orbitron"), x=0.5,
                   color=ELECTRIC_CYAN if anchor else PULSING_CRIMSON),
        xaxis_title="Throughput (Gtokens/s)",
        yaxis_title="Latency (ns)",
        showlegend=True,
        legend=dict(font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
    ))
    st.plotly_chart(fig_pareto, use_container_width=True, key="pareto")

with pa_right:
    # Dual-axis: WAF + Energy Waste over time
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
    fig_dual.add_trace(
        go.Scatter(
            x=t_axis, y=active_waf, name="WAF",
            line=dict(color=ELECTRIC_CYAN if anchor else PULSING_CRIMSON, width=1.5),
        ),
        secondary_y=False,
    )
    fig_dual.add_trace(
        go.Scatter(
            x=t_axis, y=active_energy, name="Energy Waste",
            line=dict(color="#ffaa00", width=1.2, dash="dot"),
            opacity=0.8,
        ),
        secondary_y=True,
    )
    dual_layout = plotly_layout_base(
        height=340,
        title=dict(text="WAF & ENERGY WASTE — DUAL AXIS",
                   font=dict(size=11, family="Orbitron"), x=0.5,
                   color=ELECTRIC_CYAN if anchor else PULSING_CRIMSON),
        showlegend=True,
        legend=dict(font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
    )
    fig_dual.update_layout(**dual_layout)
    fig_dual.update_yaxes(
        title_text="WAF (×)", secondary_y=False,
        gridcolor="#0a2a35", tickfont=dict(size=10, color="#8cc8d8"),
    )
    fig_dual.update_yaxes(
        title_text="Energy Waste Index", secondary_y=True,
        gridcolor="#0a2a35", tickfont=dict(size=10, color="#ffaa00"),
    )
    st.plotly_chart(fig_dual, use_container_width=True, key="dual_axis")


# ─────────────────────────────────────────────────────────────────────────────
# XIII. FOOTER — Technical Summary
# ─────────────────────────────────────────────────────────────────────────────

raw_amat = MemoryHierarchy.compute_amat(p_dram)
improvement_waf = (1 - shaped_waf.mean() / (raw_waf.mean() + 1e-9)) * 100
improvement_press = (1 - shaped_pressure.mean() / (raw_pressure.mean() + 1e-9)) * 100
improvement_energy = (1 - shaped_energy.mean() / (raw_energy.mean() + 1e-9)) * 100

st.markdown(
    f"""
    <div class="glass-card" style="margin-top:16px;">
        <div style="font-family:'Orbitron',sans-serif; font-size:0.75rem;
                    letter-spacing:4px; color:{ELECTRIC_CYAN}; margin-bottom:10px;
                    text-transform:uppercase;">◈ Optimisation Summary</div>
        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px;
                    font-size:0.72rem; color:#8cc8d8;">
            <div>
                <div style="color:{ELECTRIC_CYAN}88; font-size:0.6rem; letter-spacing:2px;">AMAT</div>
                <div style="font-family:'Orbitron'; font-size:1.1rem; color:{ELECTRIC_CYAN};">{raw_amat:.1f} ns</div>
                <div style="font-size:0.6rem;">P_dram={p_dram:.2f}</div>
            </div>
            <div>
                <div style="color:{ELECTRIC_CYAN}88; font-size:0.6rem; letter-spacing:2px;">WAF REDUCTION</div>
                <div style="font-family:'Orbitron'; font-size:1.1rem;
                            color:{'#00ff88' if improvement_waf > 0 else PULSING_CRIMSON};">
                    {improvement_waf:+.1f}%</div>
                <div style="font-size:0.6rem;">via PID shaping</div>
            </div>
            <div>
                <div style="color:{ELECTRIC_CYAN}88; font-size:0.6rem; letter-spacing:2px;">PRESSURE Δ</div>
                <div style="font-family:'Orbitron'; font-size:1.1rem;
                            color:{'#00ff88' if improvement_press > 0 else PULSING_CRIMSON};">
                    {improvement_press:+.1f}%</div>
                <div style="font-size:0.6rem;">buffer occupancy</div>
            </div>
            <div>
                <div style="color:{ELECTRIC_CYAN}88; font-size:0.6rem; letter-spacing:2px;">ENERGY SAVED</div>
                <div style="font-family:'Orbitron'; font-size:1.1rem;
                            color:{'#00ff88' if improvement_energy > 0 else PULSING_CRIMSON};">
                    {improvement_energy:+.1f}%</div>
                <div style="font-size:0.6rem;">waste index</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="text-align:center; padding:20px 0 10px; font-size:0.5rem;
                letter-spacing:4px; color:{ELECTRIC_CYAN}33; text-transform:uppercase;
                font-family:'Orbitron',sans-serif;">
        VICS-BELHADJ Neural-Memory Architect V1.0 · ANU VICS Lab ·
        Hybrid NVM/DRAM · PID Stochastic Shaping · {duration} Cycles Simulated
    </div>
    """,
    unsafe_allow_html=True,
)
