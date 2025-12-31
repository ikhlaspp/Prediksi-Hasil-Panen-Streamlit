"""
Reusable UI Components
"""
import streamlit as st
from config.theme import COLORS, BORDER_RADIUS, SHADOWS, TYPOGRAPHY


def gradient_card(title, description, icon, gradient_colors):
    """Create a modern gradient card component"""
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {gradient_colors[0]} 0%, {gradient_colors[1]} 100%); 
                padding: 2.5rem 2rem; 
                border-radius: 16px; 
                text-align: center;
                box-shadow: 0 18px 48px rgba(0, 0, 0, 0.28), 0 8px 24px rgba(0, 0, 0, 0.2);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                border: 1px solid rgba(255, 255, 255, 0.12);
                position: relative;
                overflow: hidden;
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);'
         onmouseover="this.style.transform='translateY(-6px) scale(1.02)'; this.style.boxShadow='0 20px 60px rgba(0, 0, 0, 0.32), 0 8px 20px rgba(0, 0, 0, 0.16)'"
         onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 18px 48px rgba(0, 0, 0, 0.28), 0 8px 24px rgba(0, 0, 0, 0.2)'">
        <div style='font-size: 3rem; margin-bottom: 1.25rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));'>{icon}</div>
        <h3 style='color: white; margin-bottom: 0.875rem; font-weight: 700; font-size: 1.25rem; letter-spacing: -0.01em;'>{title}</h3>
        <p style='color: rgba(255, 255, 255, 0.95); font-size: 0.9rem; line-height: 1.6; font-weight: 400;'>{description}</p>
    </div>
    """, unsafe_allow_html=True)


def feature_card(icon, title, description, button_text, button_key):
    """Create a modern feature card with navigation button"""
    st.markdown(f"""
    <div class='feature-card' style='text-align: center;'>
        <div style='
            font-size: 3rem; 
            margin-bottom: 1.25rem;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 2px 4px rgba(37, 99, 235, 0.2));
        '>{icon}</div>
        <h3 style='
            text-align: center; 
            color: {COLORS['text_primary']}; 
            font-weight: 700;
            font-size: 1.25rem;
            margin-bottom: 0.875rem;
            letter-spacing: -0.01em;
        '>{title}</h3>
        <p style='
            text-align: center; 
            color: {COLORS['text_secondary']}; 
            margin: 0 0 1.5rem;
            line-height: 1.7;
            font-size: 0.95rem;
        '>
            {description}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    return st.button(f"{icon} {button_text}", key=button_key, use_container_width=True)


def metric_card(label, value, delta=None, help_text=None):
    """Create a styled metric card"""
    st.metric(label, value, delta=delta, help=help_text)


def info_box(content, box_type='info'):
    """Create a modern alert/info box with glass effect"""
    colors = {
        'info': ('rgba(56,189,248,0.16)', 'rgba(56,189,248,0.08)', COLORS['info'], '#e0f2fe'),
        'success': ('rgba(16,185,129,0.16)', 'rgba(16,185,129,0.08)', COLORS['success'], '#d1fae5'),
        'warning': ('rgba(245,158,11,0.18)', 'rgba(245,158,11,0.08)', COLORS['warning'], '#fef3c7'),
        'danger': ('rgba(239,68,68,0.16)', 'rgba(239,68,68,0.08)', COLORS['danger'], '#fee2e2')
    }
    
    gradient = colors.get(box_type, colors['info'])
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {gradient[0]} 0%, {gradient[1]} 100%); 
        padding: 1.25rem 1.5rem; 
        border-radius: 14px; 
        color: {gradient[3]}; 
        margin: 1rem 0;
        box-shadow: 0 14px 38px rgba(0, 0, 0, 0.25);
        font-weight: 600;
        font-size: 0.95rem;
        line-height: 1.6;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid {gradient[2]};
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    '>
        {content}
    </div>
    """, unsafe_allow_html=True)


def success_badge(text):
    """Create a success badge"""
    st.markdown(f"""
    <span class='success-badge'>{text}</span>
    """, unsafe_allow_html=True)


def loading_spinner(text="Loading..."):
    """Create a loading spinner"""
    return st.spinner(text)


def progress_indicator(progress, text=""):
    """Create a progress indicator"""
    progress_bar = st.progress(progress)
    if text:
        st.text(text)
    return progress_bar


def custom_button(text, key, button_type='primary', use_full_width=True):
    """Create a custom styled button"""
    return st.button(text, key=key, type=button_type, use_container_width=use_full_width)
