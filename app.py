import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# --- 1. System Setup & Cybernetic CSS ---
st.set_page_config(page_title="VICS // NEURAL ARCHITECT", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Global Dark Mode & Monospace */
    html, body, [class*="css"]  {
        background-color: #050505;
        color: #00f3ff;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #00f3ff;
        box-shadow: 2px 0 15px rgba(0, 243, 255, 0.1);
    }
    
    /* Glowing Headers */
    h1, h2, h3 {
        color: #00f3ff !important;
        text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
    }
    
    /* Futuristic Button */
    .stButton>button {
        background-color: transparent;
        color: #00f3ff;
        border: 1px solid #00f3ff;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
        width: 100%;
        padding: 15px;
        font-weight: bold;
        letter-spacing: 2px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00f3ff;
        color: #050505;
        box-shadow: 0 0 25px rgba(0, 243, 255, 0.8);
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Session State Management ---
if 'optimized' not in st.session_state:
    st.session_state.optimized = False

def toggle_optimization():
    st.session_state.optimized = not st.session_state.optimized

# --- 3. The Academic Dossier (Sidebar) ---
with st.sidebar:
    st.markdown("### [ SECURE UPLINK ESTABLISHED ]")
    st.markdown("---")
    st.markdown("**OPERATOR:** Fatima Z. Belhadj")
    st.markdown("**RANK:** 1st, BSEMS (Summa Cum Laude, 2024)")
    st.markdown("**INDUSTRY:** Top-Rated Plus Data Analyst (Upwork Top 3%)")
    st.markdown("**RESEARCH:** 3x Published (IEEE/Springer) | Princeton Presenter")
    st.markdown("**AWARDS:** SSE Stonehenge | 2022 PGS Sustainability")
    st.markdown("---")
    st.markdown("> *Hypothesis: Mitigating GenAI memory spillage by governing data-ingress via predictive stochastic shaping. This terminal models the constraint.*")

# --- 4. Main Terminal UI ---
st.title("VICS HYBRID-MEMORY // KINETIC ENTROPY SIMULATOR")

# The Action Trigger
if st.button("[ INITIATE PREDICTIVE SHAPING CONSTRAINT ]", on_click=toggle_optimization):
    with st.spinner("Re-aligning Latent Vectors..."):
        time.sleep(0.6) # Simulating complex calculation

# --- 5. Mathematical Generation & State Logic ---
n_points = 1200
np.random.seed(42)

if st.session_state.optimized:
    # State: Optimized (Locked Geometric Torus)
    theta = np.random.uniform(0, 2*np.pi, n_points)
    phi = np.random.uniform(0, 2*np.pi, n_points)
    R, r = 5, 2
    x = (R + r * np.cos(theta)) * np.cos(phi)
    y = (R + r * np.cos(theta)) * np.sin(phi)
    z = r * np.sin(theta)
    
    particle_color = '#00f3ff'
    waf_metric = "1.02x"
    pressure_metric = "0.8 TB/s"
    state_text = "PIPELINE OPTIMIZED & LOCKED"
    state_color = "#00f3ff"
else:
    # State: Unconstrained Entropy (Chaotic Cloud)
    x = np.random.normal(0, 15, n_points)
    y = np.random.normal(0, 15, n_points)
    z = np.random.normal(0, 15, n_points)
    
    particle_color = '#ff003c'
    waf_metric = "5.86x"
    pressure_metric = "4.4 TB/s"
    state_text = "WARNING: CATASTROPHIC LATENT DRIFT"
    state_color = "#ff003c"

# --- 6. Live Telemetry Dashboard ---
col1, col2, col3 = st.columns(3)
col1.metric("Write Amplification (WAF)", waf_metric)
col2.metric("DRAM Pressure", pressure_metric)
col3.markdown(f"<h4 style='color:{state_color}; text-align:center; padding-top:15px; text-shadow: 0 0 8px {state_color};'>{state_text}</h4>", unsafe_allow_html=True)

st.markdown("---")

# --- 7. The 3D Render Engine ---
fig3d = go.Figure(data=[go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(
        size=3,
        color=particle_color,
        opacity=0.8,
        line=dict(width=0)
    )
)])

# Stripping away the grid to make it look like deep space
fig3d.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, b=0, t=0),
    scene=dict(
        xaxis=dict(showbackground=False, showticklabels=False, showgrid=False, zeroline=False, title=''),
        yaxis=dict(showbackground=False, showticklabels=False, showgrid=False, zeroline=False, title=''),
        zaxis=dict(showbackground=False, showticklabels=False, showgrid=False, zeroline=False, title='')
    )
)

st.plotly_chart(fig3d, use_container_width=True)
