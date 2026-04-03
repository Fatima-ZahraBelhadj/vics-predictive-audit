import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="VICS // BELHADJ AUDIT",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS INJECTION
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* ── Force void-black everywhere ── */
        html, body, [data-testid="stAppViewContainer"],
        [data-testid="stApp"], section.main,
        .block-container {
            background-color: #050505 !important;
            color: #c8d6e5 !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background-color: #0a0a0a !important;
            border-right: 1px solid #00f3ff22 !important;
        }
        [data-testid="stSidebar"] * { color: #c8d6e5 !important; }

        /* ── Remove default block padding ── */
        .block-container { padding: 1.2rem 2rem 2rem 2rem !important; }

        /* ── Global font override ── */
        *, *::before, *::after {
            font-family: 'Courier New', Courier, monospace !important;
        }

        /* ── Metric cards ── */
        [data-testid="stMetric"] {
            background: #0d0d0d !important;
            border: 1px solid #00f3ff33 !important;
            border-radius: 4px !important;
            padding: 1rem 1.4rem !important;
        }
        [data-testid="stMetricLabel"] > div {
            font-size: 0.68rem !important;
            letter-spacing: 0.15em !important;
            color: #00f3ff !important;
            text-transform: uppercase !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.9rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        /* ── Tabs ── */
        [data-testid="stTabs"] button {
            background: transparent !important;
            color: #5a7a8a !important;
            border-bottom: 2px solid transparent !important;
            font-size: 0.72rem !important;
            letter-spacing: 0.18em !important;
            text-transform: uppercase !important;
            padding: 0.5rem 1.2rem !important;
        }
        [data-testid="stTabs"] button[aria-selected="true"] {
            color: #00f3ff !important;
            border-bottom: 2px solid #00f3ff !important;
            background: #00f3ff0a !important;
        }
        [data-testid="stTabs"] { border-bottom: 1px solid #00f3ff22 !important; }

        /* ── Toggle ── */
        [data-testid="stToggle"] label {
            font-size: 0.78rem !important;
            letter-spacing: 0.12em !important;
            color: #00f3ff !important;
        }

        /* ── Headers ── */
        h1, h2, h3 { color: #00f3ff !important; letter-spacing: 0.06em !important; }

        /* ── Dividers ── */
        hr { border-color: #00f3ff22 !important; }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #050505; }
        ::-webkit-scrollbar-thumb { background: #00f3ff44; border-radius: 2px; }

        /* ── System state pill ── */
        .state-catastrophic {
            display:inline-block;
            background: #ff003c18;
            border: 1px solid #ff003c;
            color: #ff003c !important;
            font-size: 1.05rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            padding: 0.45rem 1.1rem;
            border-radius: 3px;
            text-shadow: 0 0 12px #ff003ccc;
            animation: blink-red 1.2s infinite;
        }
        .state-optimized {
            display:inline-block;
            background: #00f3ff14;
            border: 1px solid #00f3ff;
            color: #00f3ff !important;
            font-size: 1.05rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            padding: 0.45rem 1.1rem;
            border-radius: 3px;
            text-shadow: 0 0 12px #00f3ffaa;
        }
        @keyframes blink-red {
            0%, 100% { opacity: 1; }
            50%       { opacity: 0.45; }
        }

        /* ── Profile card ── */
        .profile-card {
            background: #0d0d0d;
            border: 1px solid #00f3ff2a;
            border-left: 3px solid #00f3ff;
            border-radius: 4px;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
            font-size: 0.72rem;
            line-height: 1.75;
            color: #b0c4d4 !important;
        }
        .profile-card .name {
            font-size: 0.95rem;
            font-weight: 700;
            color: #00f3ff !important;
            letter-spacing: 0.08em;
            margin-bottom: 0.3rem;
        }
        .profile-card .kv {
            display: flex;
            gap: 0.5rem;
        }
        .profile-card .key {
            color: #4a6a7a !important;
            min-width: 56px;
        }
        .profile-card .val { color: #c8d6e5 !important; }

        /* ── Pitch block ── */
        .pitch-block {
            background: #05080a;
            border: 1px dashed #00f3ff44;
            border-radius: 4px;
            padding: 0.85rem 1rem;
            font-size: 0.68rem;
            line-height: 1.85;
            color: #7a9aaa !important;
            margin-top: 0.8rem;
        }

        /* ── Secure uplink header ── */
        .uplink-header {
            font-size: 0.7rem;
            letter-spacing: 0.2em;
            color: #00f3ff !important;
            text-align: center;
            padding: 0.5rem 0 1.2rem 0;
            text-shadow: 0 0 8px #00f3ff88;
        }

        /* ── Main title ── */
        .main-title {
            font-size: 1.65rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            color: #00f3ff !important;
            text-shadow: 0 0 20px #00f3ff66;
            border-bottom: 1px solid #00f3ff33;
            padding-bottom: 0.5rem;
            margin-bottom: 0.2rem;
        }
        .main-subtitle {
            font-size: 0.65rem;
            letter-spacing: 0.22em;
            color: #2a5a6a !important;
            margin-bottom: 1.4rem;
            text-transform: uppercase;
        }

        /* ── Metric label override for state col ── */
        .metric-state-label {
            font-size: 0.68rem;
            letter-spacing: 0.15em;
            color: #00f3ff !important;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }
        .metric-state-wrapper {
            background: #0d0d0d;
            border: 1px solid #00f3ff33;
            border-radius: 4px;
            padding: 1rem 1.4rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# RANDOM SEED & CONSTANTS
# ─────────────────────────────────────────────
RNG = np.random.default_rng(42)
N_POINTS = 1000
N_LAYERS = 50
N_BLOCKS  = 32

# ─────────────────────────────────────────────
# DATA GENERATORS
# ─────────────────────────────────────────────

def chaotic_spiral(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Diverging Lorenz-flavoured spiral – catastrophic drift state."""
    t = np.linspace(0, 6 * np.pi, n)
    r = np.exp(0.18 * t)                          # exponential blowup
    x = r * np.cos(t) + RNG.normal(0, 0.6, n)
    y = r * np.sin(t) + RNG.normal(0, 0.6, n)
    z = np.cumsum(RNG.normal(0, 0.35, n))         # unbounded random walk
    return x, y, z


def torus_attractor(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Tight quasi-periodic torus – optimised pipeline state."""
    R, r_minor = 3.5, 0.55
    u = RNG.uniform(0, 2 * np.pi, n)
    v = RNG.uniform(0, 2 * np.pi, n)
    noise = 0.04
    x = (R + r_minor * np.cos(v)) * np.cos(u) + RNG.normal(0, noise, n)
    y = (R + r_minor * np.cos(v)) * np.sin(u) + RNG.normal(0, noise, n)
    z = r_minor * np.sin(v)                       + RNG.normal(0, noise, n)
    return x, y, z


def memory_heatmap_data(optimised: bool) -> np.ndarray:
    """50 transformer layers × 32 memory blocks."""
    if optimised:
        base   = RNG.uniform(0.0, 0.18, (N_LAYERS, N_BLOCKS))
        spikes = np.zeros_like(base)
    else:
        base   = RNG.uniform(0.35, 0.75, (N_LAYERS, N_BLOCKS))
        spikes = RNG.choice([0, 1], size=(N_LAYERS, N_BLOCKS), p=[0.72, 0.28]) \
                 * RNG.uniform(0.6, 1.0, (N_LAYERS, N_BLOCKS))
    return np.clip(base + spikes, 0, 1)


# ─────────────────────────────────────────────
# PLOTLY CHART BUILDERS
# ─────────────────────────────────────────────
_BG = "#050505"
_TRANSPARENT = "rgba(0,0,0,0)"
_AXIS_STYLE = dict(
    showgrid=False, showline=False, zeroline=False,
    showticklabels=False, backgroundcolor=_BG,
)


def build_phase_space(optimised: bool) -> go.Figure:
    if optimised:
        x, y, z   = torus_attractor(N_POINTS)
        colors     = np.sqrt(x**2 + y**2 + z**2)
        colorscale = [
            [0.0, "#001a1f"],
            [0.3, "#005f6b"],
            [0.6, "#00c8d8"],
            [1.0, "#00f3ff"],
        ]
        marker_size = 2.2
        opacity     = 0.82
        title_txt   = "PHASE-SPACE ATTRACTOR  ·  TORUS CONVERGENCE (OPTIMISED)"
    else:
        x, y, z   = chaotic_spiral(N_POINTS)
        colors     = np.abs(z)
        colorscale = [
            [0.0, "#1a0000"],
            [0.35, "#8b0000"],
            [0.7, "#ff003c"],
            [1.0, "#ff8888"],
        ]
        marker_size = 2.5
        opacity     = 0.75
        title_txt   = "PHASE-SPACE ATTRACTOR  ·  CATASTROPHIC DIVERGENCE DETECTED"

    trace = go.Scatter3d(
        x=x, y=y, z=z,
        mode="markers",
        marker=dict(
            size=marker_size,
            color=colors,
            colorscale=colorscale,
            opacity=opacity,
            line=dict(width=0),
        ),
        hovertemplate="x:%{x:.2f}  y:%{y:.2f}  z:%{z:.2f}<extra></extra>",
    )

    fig = go.Figure(data=[trace])
    fig.update_layout(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        margin=dict(l=0, r=0, t=36, b=0),
        title=dict(
            text=title_txt,
            font=dict(family="Courier New", size=11,
                      color="#00f3ff" if optimised else "#ff003c"),
            x=0.01, y=0.98,
        ),
        scene=dict(
            bgcolor=_BG,
            xaxis=_AXIS_STYLE,
            yaxis=_AXIS_STYLE,
            zaxis=_AXIS_STYLE,
        ),
        height=540,
    )
    return fig


def build_heatmap(optimised: bool) -> go.Figure:
    data = memory_heatmap_data(optimised)

    if optimised:
        colorscale = [
            [0.0, "#050505"],
            [0.25, "#001a2a"],
            [0.6,  "#003a5a"],
            [1.0,  "#005f8a"],
        ]
        title_txt = "NVM/DRAM MEMORY MAP  ·  THERMAL PRESSURE: NOMINAL"
    else:
        colorscale = [
            [0.0, "#050505"],
            [0.15, "#1a0000"],
            [0.4,  "#8b0000"],
            [0.7,  "#cc2200"],
            [0.88, "#ff5500"],
            [1.0,  "#ff9900"],
        ]
        title_txt = "NVM/DRAM MEMORY MAP  ·  SPILLAGE HOTSPOTS ACTIVE"

    layer_labels   = [f"L{i:02d}" for i in range(N_LAYERS)]
    block_labels   = [f"B{j:02d}" for j in range(N_BLOCKS)]

    trace = go.Heatmap(
        z=data,
        x=block_labels,
        y=layer_labels,
        colorscale=colorscale,
        showscale=True,
        colorbar=dict(
            thickness=10,
            tickfont=dict(family="Courier New", size=9, color="#4a6a7a"),
            outlinecolor=_TRANSPARENT,
            bgcolor=_BG,
        ),
        hovertemplate="Layer %{y}  Block %{x}<br>Pressure: %{z:.3f}<extra></extra>",
        zmin=0, zmax=1,
    )

    fig = go.Figure(data=[trace])
    fig.update_layout(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        margin=dict(l=0, r=0, t=36, b=0),
        title=dict(
            text=title_txt,
            font=dict(family="Courier New", size=11,
                      color="#00f3ff" if optimised else "#ff003c"),
            x=0.01, y=0.98,
        ),
        xaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(family="Courier New", size=7, color="#2a4a5a"),
            tickangle=0,
        ),
        yaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(family="Courier New", size=7, color="#2a4a5a"),
            autorange="reversed",
        ),
        height=540,
    )
    return fig


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="uplink-header">[ SECURE UPLINK ESTABLISHED ]</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="profile-card">
            <div class="name">FATIMA Z. BELHADJ</div>
            <div class="kv"><span class="key">ROLE</span><span class="val">Lead Analyst · Predictive Computational Modeling</span></div>
            <div class="kv"><span class="key">DEGREE</span><span class="val">BSEMS, Summa Cum Laude</span></div>
            <div class="kv"><span class="key">RANK</span><span class="val">Cohort Rank: 1st</span></div>
            <div class="kv"><span class="key">PUB</span><span class="val">3× IEEE / Springer Published</span></div>
            <div class="kv"><span class="key">CONF</span><span class="val">Presenter — Princeton Univ. (Virtual)</span></div>
            <div class="kv"><span class="key">OPS</span><span class="val">Top 3% Global Freelance Data Analyst (Upwork)</span></div>
            <div class="kv"><span class="key">STACK</span><span class="val">Python · Predictive Modeling · Automated Pipelines</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pitch-block">
        Dr. Akram: My background is in systems engineering and predictive
        computational modeling. By integrating my experience in building
        automated data pipelines with your VICS Hybrid-NVM architecture,
        we can mathematically govern latent drift and optimize memory
        spillage. This dashboard is a live simulation of that data constraint.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="font-size:0.6rem;letter-spacing:0.18em;color:#1a3a4a;
                    text-align:center;padding-top:0.4rem;border-top:1px solid #00f3ff11;">
            SESSION · CLASSIFIED<br>
            VICS ENTROPY SIM v2.7.1<br>
            ANU CECS · RESEARCH INTERFACE
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# MAIN PANEL
# ─────────────────────────────────────────────
st.markdown(
    '<div class="main-title">VICS LAB // HYBRID-MEMORY ENTROPY SIMULATOR</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="main-subtitle">'
    'ANU · VICS RESEARCH LAB · DRAM/NVM LATENT DRIFT &amp; MEMORY SPILLAGE DIAGNOSTIC'
    '</div>',
    unsafe_allow_html=True,
)

# ── Toggle ──────────────────────────────────
optimised = st.toggle("[ INITIATE PREDICTIVE DATA CONSTRAINT ]", value=False)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP METRICS ROW
# ─────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

if optimised:
    dram_val    = f"{RNG.uniform(0.28, 0.44):.3f}"
    dram_delta  = "▼ 74.2%  constraint active"
    waste_val   = f"{RNG.uniform(1.8, 4.9):.1f}%"
    waste_delta = "▼ 91.3%  pipeline stabilised"
    state_html  = '<span class="state-optimized">PIPELINE OPTIMIZED</span>'
else:
    dram_val    = f"{RNG.uniform(3.1, 4.8):.3f}"
    dram_delta  = "▲ CRITICAL THRESHOLD EXCEEDED"
    waste_val   = f"{RNG.uniform(52.0, 78.5):.1f}%"
    waste_delta = "▲ RUNAWAY COMPUTE DETECTED"
    state_html  = '<span class="state-catastrophic">CATASTROPHIC DRIFT</span>'

with col1:
    st.metric(
        label="DRAM PRESSURE (TB/s)",
        value=dram_val,
        delta=dram_delta,
        delta_color="inverse" if optimised else "normal",
    )

with col2:
    st.metric(
        label="COMPUTE WASTE (%)",
        value=waste_val,
        delta=waste_delta,
        delta_color="inverse" if optimised else "normal",
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-state-wrapper">
            <div class="metric-state-label">SYSTEM STATE</div>
            {state_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECONDARY KPI STRIP
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5, gap="small")

kpis = (
    ("NVM WRITE AMPLIF.", f"{RNG.uniform(1.02,1.09):.4f}×" if optimised else f"{RNG.uniform(3.8,6.2):.4f}×"),
    ("LATENT DRIFT (σ)",  f"{RNG.uniform(0.001,0.004):.5f}" if optimised else f"{RNG.uniform(0.12,0.38):.5f}"),
    ("EVICTION RATE",     f"{RNG.uniform(0.3,0.9):.2f}/ms" if optimised else f"{RNG.uniform(18.4,34.2):.2f}/ms"),
    ("PIPELINE LATENCY",  f"{RNG.uniform(0.8,1.4):.2f} µs" if optimised else f"{RNG.uniform(22.1,47.8):.2f} µs"),
    ("CONSTRAINT ΔE",     f"{RNG.uniform(0.0002,0.0009):.6f}" if optimised else f"N/A"),
)

for col, (label, val) in zip([k1, k2, k3, k4, k5], kpis):
    with col:
        st.metric(label=label, value=val)

st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# VISUALISATION TABS
# ─────────────────────────────────────────────
tab1, tab2 = st.tabs(
    ["  TAB 01 // 3D LATENT PHASE-SPACE ATTRACTOR  ",
     "  TAB 02 // NVM/DRAM TRANSFORMER MEMORY HEATMAP  "]
)

with tab1:
    st.markdown(
        "<div style='font-size:0.62rem;letter-spacing:0.16em;color:#2a4a5a;"
        "margin-bottom:0.5rem;'>LATENT SPACE PHASE DIAGRAM  ·  1 000-POINT STOCHASTIC TRAJECTORY</div>",
        unsafe_allow_html=True,
    )
    fig_phase = build_phase_space(optimised)
    st.plotly_chart(fig_phase, use_container_width=True, config={"displayModeBar": False})

    # Annotation below chart
    note_col1, note_col2, note_col3 = st.columns(3)
    notes = [
        ("TRAJECTORY TYPE", "TORUS ATTRACTOR (KVLO)" if optimised else "LORENZ DIVERGENCE"),
        ("LYAPUNOV EXP.",    "λ < 0  (STABLE)"       if optimised else "λ > 0  (CHAOTIC)"),
        ("BASIN INTEGRITY",  "INTACT"                 if optimised else "FRACTURING"),
    ]
    for nc, (lbl, val) in zip([note_col1, note_col2, note_col3], notes):
        with nc:
            color = "#00f3ff" if optimised else "#ff003c"
            st.markdown(
                f"<div style='font-size:0.62rem;letter-spacing:0.12em;color:#2a4a5a;'>{lbl}</div>"
                f"<div style='font-size:0.85rem;color:{color};font-weight:700;'>{val}</div>",
                unsafe_allow_html=True,
            )

with tab2:
    st.markdown(
        "<div style='font-size:0.62rem;letter-spacing:0.16em;color:#2a4a5a;"
        "margin-bottom:0.5rem;'>50 TRANSFORMER LAYERS × 32 NVM/DRAM MEMORY BLOCKS  ·  NORMALISED THERMAL PRESSURE [0–1]</div>",
        unsafe_allow_html=True,
    )
    fig_heat = build_heatmap(optimised)
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

    # Summary stats bar
    data_np = memory_heatmap_data(optimised)
    h1, h2, h3, h4 = st.columns(4)
    heat_stats = [
        ("PEAK PRESSURE",  f"{data_np.max():.4f}"),
        ("MEAN PRESSURE",  f"{data_np.mean():.4f}"),
        ("HOTSPOT BLOCKS", f"{int((data_np > 0.70).sum()):,}"),
        ("SAFE BLOCKS",    f"{int((data_np < 0.20).sum()):,}"),
    ]
    for hc, (lbl, val) in zip([h1, h2, h3, h4], heat_stats):
        with hc:
            st.metric(label=lbl, value=val)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-size:0.58rem;letter-spacing:0.18em;color:#1a2a33;"
    "text-align:center;border-top:1px solid #00f3ff0e;padding-top:0.8rem;'>"
    "VICS ENTROPY SIMULATOR · ANU CECS · DR. SHOAIB AKRAM TARGET INTERFACE · "
    "ANALYST: F.Z. BELHADJ · SESSION CLASSIFIED · ALL VALUES STOCHASTICALLY MODELLED"
    "</div>",
    unsafe_allow_html=True,
)
