"""
Home page view
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
import plotly.graph_objects as go
from models.data_loader import load_dataset, load_metrics


def _inject_styles():
    """Inject custom CSS styles"""
    st.markdown(
        """
        <style>
            .home-shell {
                max-width: 1180px;
                margin: 0 auto;
                display: flex;
                flex-direction: column;
                gap: 32px;
            }
            .section-spacing { margin: 2.25rem 0 0; }
            .hero-banner {
                position: relative;
                overflow: hidden;
                display: grid;
                grid-template-columns: 1fr;
                gap: 24px;
                padding: clamp(24px, 3vw, 36px);
                border-radius: 24px;
                background: linear-gradient(135deg, rgba(11,18,32,0.9) 0%, rgba(11,18,32,0.75) 55%, rgba(20,30,48,0.78) 100%);
                border: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: 0 30px 80px rgba(0,0,0,0.45);
                isolation: isolate;
                backdrop-filter: blur(18px) saturate(125%);
            }
            .hero-banner::before {
                content: '';
                position: absolute;
                inset: 0;
                background: radial-gradient(circle at 20% 20%, rgba(96,165,250,0.22), transparent 42%),
                            radial-gradient(circle at 80% 15%, rgba(167,139,250,0.24), transparent 40%),
                            radial-gradient(circle at 62% 75%, rgba(34,211,238,0.2), transparent 34%);
                opacity: 1;
                z-index: 0;
            }
            .hero-banner::after {
                content: '';
                position: absolute;
                inset: 0;
                background: linear-gradient(120deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 55%, rgba(255,255,255,0) 100%);
                z-index: 0;
            }
            .hero-content { position: relative; z-index: 1; }
            .hero__eyebrow {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 12px;
                border-radius: 999px;
                background: rgba(96, 165, 250, 0.14);
                color: #e0f2fe;
                font-size: 0.95rem;
                font-weight: 700;
                border: 1px solid rgba(255,255,255,0.15);
                backdrop-filter: blur(12px);
            }
            .hero__title {
                margin: 16px 0 10px;
                font-size: 3rem;
                font-weight: 800;
                letter-spacing: -0.03em;
                background: linear-gradient(135deg, #93c5fd 0%, #a78bfa 40%, #22d3ee 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .hero__subtitle {
                max-width: 820px;
                color: #dbeafe;
                font-size: 1.08rem;
                line-height: 1.7;
                margin-bottom: 18px;
            }
            .hero__actions {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-top: 12px;
                flex-wrap: wrap;
            }
            .hero-side { display: none; }
            .btn {
                padding: 12px 18px;
                border-radius: 14px;
                font-weight: 800;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                backdrop-filter: blur(14px);
                -webkit-backdrop-filter: blur(14px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                box-shadow: 0 18px 48px rgba(0, 0, 0, 0.32);
                transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease, border-color 0.2s ease;
                letter-spacing: 0.01em;
            }
            .btn-primary {
                background: linear-gradient(120deg, rgba(37, 99, 235, 0.92) 0%, rgba(124, 58, 237, 0.92) 100%);
                color: #fff;
                box-shadow: 0 22px 55px rgba(124, 58, 237, 0.35);
            }
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 26px 65px rgba(124, 58, 237, 0.42);
                border-color: rgba(255, 255, 255, 0.3);
            }
            .btn-ghost {
                background: rgba(255, 255, 255, 0.08);
                color: #e2e8f0;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .btn-ghost:hover {
                transform: translateY(-2px);
                background: rgba(255, 255, 255, 0.12);
                border-color: rgba(255, 255, 255, 0.32);
            }
            .stat-card {
                background: rgba(15,23,42,0.78);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 16px 18px;
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.32);
                backdrop-filter: blur(12px);
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 14px;
                align-items: stretch;
            }
            .stat-label { color: #9ca3af; font-size: 0.95rem; }
            .stat-value { color: #e5e7eb; font-size: 1.85rem; font-weight: 800; margin-top: 6px; }
            .stat-sub { color: #93c5fd; font-size: 0.95rem; font-weight: 700; }
            .section-card {
                background: rgba(15,23,42,0.8);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 18px;
                padding: 20px;
                box-shadow: 0 18px 48px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(12px);
            }
            .section-card h3 { color: #e5e7eb; }
            .section-card p { color: #cbd5e1; }
            .pill-rail { display: flex; gap: 10px; flex-wrap: wrap; }
            .pill {
                padding: 10px 14px;
                border-radius: 999px;
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.1);
                color: #e5e7eb;
                font-weight: 700;
                font-size: 0.95rem;
                backdrop-filter: blur(10px);
            }
            .rail {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 16px;
            }
            .rail-card {
                background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 16px;
                padding: 16px;
                color: #e5e7eb;
                box-shadow: 0 16px 44px rgba(0,0,0,0.28);
                backdrop-filter: blur(12px);
            }
            .rail-card h4 { margin: 0 0 8px; }
            .rail-card p { margin: 0; color: #cbd5e1; font-size: 0.95rem; }
            .workflow { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap: 14px; }
            .workflow-step {
                border: 1px dashed rgba(255,255,255,0.14);
                border-radius: 14px;
                padding: 14px;
                background: rgba(255,255,255,0.04);
                color: #e5e7eb;
                backdrop-filter: blur(10px);
            }
            .workflow-step strong { color: #93c5fd; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render():
    """Render home page"""
    _inject_styles()

    # Constrain layout width for better alignment
    st.markdown("<div class='home-shell'>", unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-content'>
            <div class='hero__eyebrow'>Precision Agritech Platform</div>
            <h1 class='hero__title'>Crop Yield Prediction System</h1>
            <p class='hero__subtitle'>Forecast yields, surface risks, and explain model decisions with an end-to-end ML workflow designed for agronomists.</p>
            <div class='hero__actions'>
                <a class='btn btn-primary' href='#explore-features'>🚀 Explore Features</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick actions buttons (use Streamlit buttons for navigation)
    st.markdown("<div id='quick-actions'></div>", unsafe_allow_html=True)
    cta1, cta2, cta3 = st.columns(3, gap="medium")
    with cta1:
        if st.button("🔮 Single Prediction", use_container_width=True):
            st.query_params['page'] = 'prediction'
            st.rerun()
    with cta2:
        if st.button("📈 Data Visualization", use_container_width=True):
            st.query_params['page'] = 'visualization'
            st.rerun()
    with cta3:
        if st.button("🤖 Batch Prediction", use_container_width=True):
            st.query_params['page'] = 'batch'
            st.rerun()

    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    # Stats strip
    _render_quick_stats()

    st.markdown("<div style='margin: 2.5rem 0;'></div>", unsafe_allow_html=True)

    # Feature highlights rail
    st.markdown("<div></div>", unsafe_allow_html=True)
    st.markdown("### ✨ Why This Platform")
    st.markdown("""
    <div class='rail'>
        <div class='rail-card'>
            <h4>🎯 Accurate</h4>
            <p>Advanced ensembles and tuning keep R² high across seasons.</p>
        </div>
        <div class='rail-card'>
            <h4>⚡ Fast</h4>
            <p>Optimized pipeline delivers predictions in seconds for field ops.</p>
        </div>
        <div class='rail-card'>
            <h4>🔍 Explainable</h4>
            <p>SHAP insights and correlations reveal drivers of yield.</p>
        </div>
        <div class='rail-card'>
            <h4>🛡️ Reliable</h4>
            <p>Monitored metrics with clear baselines and drift checks.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 2.5rem 0;'></div>", unsafe_allow_html=True)

    # Dataset Overview
    _render_dataset_overview()

    st.markdown("---")

    # Model Performance
    _render_model_performance()

    st.markdown("---")

    # Call to Action
    _render_call_to_action()

    # Close constrained layout
    st.markdown("</div>", unsafe_allow_html=True)


def _render_dataset_overview():
    """Render dataset overview section"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='section-card'>
            <h3>📌 About This Project</h3>
            <p>This platform forecasts agricultural yield (tons/hectare) with a production-ready ML stack.</p>
            <div style='display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; margin-top: 12px;'>
                <div style='color:#cbd5e1;'>🌱 Soil Type</div>
                <div style='color:#cbd5e1;'>🌾 Crop Type</div>
                <div style='color:#cbd5e1;'>🌧️ Rainfall (mm)</div>
                <div style='color:#cbd5e1;'>🌡️ Temperature (°C)</div>
                <div style='color:#cbd5e1;'>🧪 Fertilizer</div>
                <div style='color:#cbd5e1;'>🚰 Irrigation</div>
                <div style='color:#cbd5e1;'>⛅ Weather Condition</div>
                <div style='color:#cbd5e1;'>📅 Days to Harvest</div>
            </div>
            <p style='margin-top: 12px; color:#93c5fd; font-weight:700;'>🎯 Target: Yield (tons/ha)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        df = load_dataset()
        if df is not None:
            st.markdown("""
            <div class='section-card'>
                <h3>📊 Dataset Stats</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class='stat-card' style='margin-top:12px;'>
                <div class='stat-label'>Total Samples</div>
                <div class='stat-value'>{df.shape[0]:,}</div>
            </div>
            <div class='stat-card' style='margin-top:12px;'>
                <div class='stat-label'>Total Features</div>
                <div class='stat-value'>{df.shape[1] - 1}</div>
            </div>
            <div class='stat-card' style='margin-top:12px;'>
                <div class='stat-label'>Mean Yield</div>
                <div class='stat-value'>{df['Yield_tons_per_hectare'].mean():.2f} t/ha</div>
            </div>
            <div class='stat-card' style='margin-top:12px;'>
                <div class='stat-label'>Max Yield</div>
                <div class='stat-value'>{df['Yield_tons_per_hectare'].max():.2f} t/ha</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Dataset not found!")


def _render_quick_stats():
    """Render quick statistics"""
    st.subheader("📊 Quick Dataset Overview")
    
    df = load_dataset()
    if df is not None:
        samples = df.shape[0]
        features = df.shape[1] - 1
        mean_yield = df['Yield_tons_per_hectare'].mean()
        std_yield = df['Yield_tons_per_hectare'].std()
        crops = df['Crop'].nunique()

        stats_html = f"""
        <div class='stats-grid'>
            <div class='stat-card'>
                <div class='stat-label'>Samples</div>
                <div class='stat-value'>{samples:,}</div>
            </div>
            <div class='stat-card'>
                <div class='stat-label'>Features</div>
                <div class='stat-value'>{features}</div>
            </div>
            <div class='stat-card'>
                <div class='stat-label'>Avg Yield (t/ha)</div>
                <div class='stat-value'>{mean_yield:.2f}</div>
            </div>
            <div class='stat-card'>
                <div class='stat-label'>Std Dev</div>
                <div class='stat-value'>{std_yield:.2f}</div>
            </div>
            <div class='stat-card'>
                <div class='stat-label'>Crop Types</div>
                <div class='stat-value'>{crops}</div>
            </div>
        </div>
        """
        st.markdown(stats_html, unsafe_allow_html=True)

        st.markdown("<div class='section-card' style='padding: 12px;'>", unsafe_allow_html=True)
        with st.expander("📋 View Sample Data", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _render_model_performance():
    """Render model performance summary"""
    st.subheader("🤖 Model Performance Overview")
    
    metrics_df = load_metrics()
    if metrics_df is not None and len(metrics_df) > 0:
        r2_col = 'R2' if 'R2' in metrics_df.columns else ('R²' if 'R²' in metrics_df.columns else None)
        if r2_col is None:
            st.warning("Metrics file missing R2 column; please refresh metrics.")
            return
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=metrics_df['Model'],
            y=metrics_df[r2_col],
            name='R² Score',
            marker=dict(
                color='#7dd3fc',
                line=dict(color='#e0f2fe', width=1.6),
                opacity=1.0
            ),
            text=metrics_df[r2_col].round(4),
            textposition='auto',
            textfont=dict(color='white', size=12, family='Inter')
        ))
        
        fig.update_layout(
            title='Model R² Score Comparison',
            xaxis_title='Model',
            yaxis_title='R² Score',
            height=400,
            showlegend=False,
            hovermode='x unified',
            plot_bgcolor='#0e1626',
            paper_bgcolor='#0e1626',
            bargap=0.25,
            font=dict(color='#e5e7eb', family='Inter'),
            margin=dict(t=40, l=40, r=20, b=40),
            xaxis=dict(gridcolor='#1f2937', zerolinecolor='#1f2937', showgrid=False, tickfont=dict(color='#e5e7eb')),
            yaxis=dict(gridcolor='#1f2937', zerolinecolor='#1f2937', range=[0, 1], tickfont=dict(color='#e5e7eb'))
        )
        
        st.plotly_chart(fig, key='home_perf_chart', use_container_width=True)
        
        st.markdown("<div class='section-card' style='padding: 12px;'>", unsafe_allow_html=True)
        with st.expander("📊 Detailed Metrics Table", expanded=False):
            st.dataframe(metrics_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _render_call_to_action():
    """Render call to action section"""
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("<div id='explore-features'></div>", unsafe_allow_html=True)
    st.markdown("### 🎯 Explore the toolkit")
    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="large")

    with col1:
        st.markdown("""
        <div id='single-prediction'></div>
        <div class='rail-card'>
            <h4>🔮 Single Prediction</h4>
            <p>Rapid scenario testing for one farm setup.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open", key="btn_pred", use_container_width=True, type="primary"):
            st.query_params['page'] = 'prediction'
            st.rerun()

    with col2:
        st.markdown("""
        <div id='data-visualization'></div>
        <div class='rail-card'>
            <h4>📈 Visualization</h4>
            <p>Interactive EDA and feature correlations.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore", key="btn_viz", use_container_width=True, type="primary"):
            st.query_params['page'] = 'visualization'
            st.rerun()

    with col3:
        st.markdown("""
        <div id='model-comparison'></div>
        <div class='rail-card'>
            <h4>⚖️ Model Comparison</h4>
            <p>Head-to-head metrics and prediction overlay.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Compare", key="btn_comp", use_container_width=True, type="primary"):
            st.query_params['page'] = 'comparison'
            st.rerun()

    with col4:
        st.markdown("""
        <div id='batch-prediction'></div>
        <div class='rail-card'>
            <h4>🤖 Batch Upload</h4>
            <p>Bulk predictions for CSV workloads.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Upload", key="btn_batch", use_container_width=True, type="primary"):
            st.query_params['page'] = 'batch'
            st.rerun()

    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

    st.markdown("### 🧭 Workflow overview")
    st.markdown("""
    <div class='workflow'>
        <div class='workflow-step'><strong>01 · Explore</strong><br>EDA, distributions, correlations.</div>
        <div class='workflow-step'><strong>02 · Train</strong><br>Model tuning and evaluation.</div>
        <div class='workflow-step'><strong>03 · Explain</strong><br>SHAP importance and local decisions.</div>
        <div class='workflow-step'><strong>04 · Deploy</strong><br>Single runs or batch CSV scoring.</div>
    </div>
    """, unsafe_allow_html=True)
