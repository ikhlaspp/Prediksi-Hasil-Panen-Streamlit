"""
Theme Configuration
Centralized theme settings for the entire application
"""

# Color Palette - Dark Mode
COLORS = {
    # Primary Colors - Electric Blue & Purple for dark surfaces
    'primary': '#60a5fa',
    'primary_dark': '#2563eb',
    'primary_light': '#93c5fd',
    'secondary': '#a78bfa',
    'secondary_dark': '#7c3aed',
    
    # Accent Colors
    'accent_emerald': '#34d399',
    'accent_amber': '#fbbf24',
    'accent_rose': '#fb7185',
    'accent_cyan': '#22d3ee',
    'accent_purple': '#c084fc',
    
    # Gradients - Dark Mode Friendly
    'gradient_primary': 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
    'gradient_success': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    'gradient_warning': 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)',
    'gradient_danger': 'linear-gradient(135deg, #fb7185 0%, #e11d48 100%)',
    'gradient_info': 'linear-gradient(135deg, #22d3ee 0%, #0891b2 100%)',
    'gradient_purple': 'linear-gradient(135deg, #7c3aed 0%, #312e81 100%)',
    
    # Background Colors - Dark Surfaces
    'bg_primary': '#0b1220',
    'bg_secondary': '#111827',
    'bg_tertiary': '#0f172a',
    'bg_card': '#0f172a',
    'bg_sidebar': '#0d1424',
    'bg_sidebar_hover': '#111827',
    
    # Text Colors
    'text_primary': '#e5e7eb',
    'text_secondary': '#cbd5e1',
    'text_tertiary': '#94a3b8',
    'text_light': '#64748b',
    
    # Border Colors
    'border_light': '#1f2937',
    'border_medium': '#374151',
    'border_dark': '#4b5563',
    
    # Status Colors
    'success': '#22c55e',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#38bdf8',
}

# Typography
TYPOGRAPHY = {
    'font_family': "'Poppins', sans-serif",
    'font_weights': {
        'light': 300,
        'regular': 400,
        'medium': 500,
        'semibold': 600,
        'bold': 700,
    },
    'font_sizes': {
        'xs': '0.75rem',
        'sm': '0.875rem',
        'base': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
        '5xl': '3rem',
    }
}

# Spacing
SPACING = {
    'xs': '0.5rem',
    'sm': '1rem',
    'md': '1.5rem',
    'lg': '2rem',
    'xl': '3rem',
    '2xl': '4rem',
}

# Border Radius - Modern Scale
BORDER_RADIUS = {
    'xs': '4px',
    'sm': '6px',
    'md': '8px',
    'lg': '12px',
    'xl': '16px',
    '2xl': '20px',
    '3xl': '24px',
    'full': '9999px',
}

# Shadows - Modern Elevation
SHADOWS = {
    'xs': '0 1px 2px rgba(0, 0, 0, 0.05)',
    'sm': '0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06)',
    'md': '0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.15)',
    'primary': '0 10px 25px -5px rgba(37, 99, 235, 0.3)',
    'primary_hover': '0 20px 40px -10px rgba(37, 99, 235, 0.4)',
    'card': '0 1px 3px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04)',
    'card_hover': '0 10px 20px -5px rgba(0, 0, 0, 0.1), 0 4px 8px -2px rgba(0, 0, 0, 0.06)',
}

# Animation
TRANSITIONS = {
    'fast': '0.15s ease',
    'normal': '0.3s ease',
    'slow': '0.5s ease',
}

from string import Template

def get_custom_css():
    """Generate custom CSS from theme configuration without f-string brace issues"""
    css_template = Template("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --color-primary: $primary;
            --color-primary-dark: $primary_dark;
            --color-secondary: $secondary;
            --shadow-card: $shadow_card;
            --shadow-card-hover: $shadow_card_hover;
        }

        .stApp, .main {
            background: radial-gradient(circle at 20% 20%, rgba(96,165,250,0.08), transparent 32%),
                        radial-gradient(circle at 80% 0%, rgba(124,58,237,0.08), transparent 30%),
                        linear-gradient(145deg, $bg_primary 0%, $bg_secondary 45%, $bg_primary 100%) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: $text_primary;
            min-height: 100vh;
        }

        .block-container {
            padding: 2.25rem 1.25rem 4rem;
            max-width: 1280px;
        }

        header[data-testid="stHeader"], [data-testid="stToolbar"] {
            background: transparent !important;
            border-bottom: 1px solid $border_light;
            backdrop-filter: blur(12px);
        }

        [data-testid="stDecoration"] {
            background: $gradient_primary !important;
            height: 4px;
        }

        /* Reusable glass surface */
        .glass-panel {
            background: rgba(15,23,42,0.65);
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 24px 60px rgba(0,0,0,0.35);
            backdrop-filter: blur(14px) saturate(125%);
            -webkit-backdrop-filter: blur(14px) saturate(125%);
        }

        /* Typography */
        h1 {
            color: $text_primary !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em;
            line-height: 1.15 !important;
        }

        h2, h3 {
            color: $text_primary !important;
            font-weight: 700 !important;
        }

        p {
            color: $text_secondary !important;
            line-height: 1.7;
        }

        /* Buttons */
        .stButton > button,
        .stDownloadButton > button,
        .stFormSubmitButton > button,
        button[data-testid="baseButton"] {
            background: linear-gradient(120deg, rgba(37,99,235,0.92) 0%, rgba(124,58,237,0.92) 100%);
            color: #f8fafc !important;
            font-weight: 700 !important;
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: $radius_lg !important;
            padding: 0.85rem 1.8rem !important;
            font-size: 0.98rem !important;
            backdrop-filter: blur(12px) saturate(130%);
            -webkit-backdrop-filter: blur(12px) saturate(130%);
            box-shadow: 0 18px 45px rgba(37,99,235,0.35);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
            text-shadow: 0 1px 2px rgba(0,0,0,0.25);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        .stFormSubmitButton > button:hover,
        button[data-testid="baseButton"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 22px 55px rgba(124,58,237,0.38);
            border-color: rgba(255,255,255,0.35);
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(165deg, rgba(12,18,32,0.9) 0%, rgba(12,18,32,0.6) 60%, rgba(20,30,48,0.7) 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.06);
            backdrop-filter: blur(16px);
            min-width: 320px;
            max-width: 320px;
        }

        /* Keep sidebar open by hiding the collapse toggle */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        button[title="Hide sidebar"],
        button[title="Show sidebar"],
        button[aria-label="Toggle sidebar"],
        button[aria-label="Hide sidebar"],
        button[aria-label="Show sidebar"],
        button:has(svg[data-testid="stSidebarCollapseIcon"]),
        svg[data-testid="stSidebarCollapseIcon"] {
            display: none !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 2rem;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            background: rgba(255,255,255,0.04);
            padding: 0.9rem 1.2rem;
            border-radius: $radius_lg;
            margin: 0.3rem 0;
            transition: all 0.2s ease;
            cursor: pointer;
            border: 1px solid rgba(255,255,255,0.06);
            color: $text_secondary !important;
            font-weight: 600;
            font-size: 0.95rem;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255,255,255,0.08);
            border-color: rgba(255,255,255,0.12);
            transform: translateX(4px);
            color: $text_primary !important;
        }

        [data-testid="stSidebar"] [data-checked="true"] {
            background: linear-gradient(120deg, rgba(37,99,235,0.9) 0%, rgba(124,58,237,0.9) 100%) !important;
            color: #ffffff !important;
            border-color: transparent !important;
            box-shadow: 0 14px 35px rgba(37,99,235,0.25);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p {
            color: $text_secondary !important;
        }

        /* Cards */
        .feature-card, div[data-testid="stMetric"], .stDataFrame, .streamlit-expanderHeader, .streamlit-expanderContent {
            background: rgba(15,23,42,0.7) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: $radius_xl !important;
            box-shadow: 0 16px 50px rgba(0,0,0,0.35) !important;
            backdrop-filter: blur(14px) saturate(120%) !important;
            -webkit-backdrop-filter: blur(14px) saturate(120%) !important;
            padding: 1.25rem 1.5rem;
            min-height: 100%;
        }

        .feature-card {
            padding: 2rem;
            position: relative;
            overflow: hidden;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(37,99,235,0.15) 0%, rgba(124,58,237,0.12) 60%, rgba(34,211,238,0.1) 100%);
            opacity: 0;
            transition: opacity 0.25s ease;
        }

        .feature-card:hover::before {
            opacity: 1;
        }

        div[data-testid="stMetricValue"] {
            font-size: 2.6rem;
            font-weight: 800;
            background: $gradient_primary;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        div[data-testid="stMetricLabel"] {
            color: $text_secondary;
            font-weight: $font_medium;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.6rem;
            background: rgba(255,255,255,0.04);
            padding: 0.4rem;
            border-radius: $radius_lg;
            border: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(12px);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: $radius_md;
            padding: 0.65rem 1.5rem;
            font-weight: 600;
            color: $text_secondary;
            border: none;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(255,255,255,0.08) !important;
            color: #f8fafc !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.35);
        }

        /* DataFrame/Table */
        .stDataFrame thead tr th {
            background: rgba(255,255,255,0.06) !important;
            color: $text_primary !important;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid rgba(255,255,255,0.08) !important;
        }

        .stDataFrame tbody tr:hover {
            background: rgba(255,255,255,0.04) !important;
        }

        /* Form controls */
        .stSelectbox > div > div,
        .stTextInput > div > div,
        .stNumberInput > div > div,
        .stDateInput > div > div {
            border-radius: $radius_lg;
            border: 1px solid rgba(255,255,255,0.10);
            background: rgba(15,23,42,0.65);
            color: $text_primary;
            transition: border 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
        }

        .stSelectbox > div > div:focus-within,
        .stTextInput > div > div:focus-within,
        .stNumberInput > div > div:focus-within,
        .stDateInput > div > div:focus-within {
            border-color: rgba(96,165,250,0.65);
            box-shadow: 0 0 0 3px rgba(37,99,235,0.25);
            background: rgba(15,23,42,0.85);
        }

        /* Slider */
        .stSlider > div > div > div > div {
            background: $gradient_purple !important;
        }

        /* Alerts */
        .stAlert {
            border-radius: $radius_lg;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.04);
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            color: $text_primary;
        }

        [data-baseweb="notification"][kind="success"] {
            background: linear-gradient(135deg, rgba(16,185,129,0.16) 0%, rgba(16,185,129,0.08) 100%);
            border-left: 4px solid $success;
            color: #d1fae5;
        }

        [data-baseweb="notification"][kind="error"] {
            background: linear-gradient(135deg, rgba(239,68,68,0.16) 0%, rgba(239,68,68,0.08) 100%);
            border-left: 4px solid $danger;
            color: #fee2e2;
        }

        [data-baseweb="notification"][kind="warning"] {
            background: linear-gradient(135deg, rgba(245,158,11,0.18) 0%, rgba(245,158,11,0.08) 100%);
            border-left: 4px solid $warning;
            color: #fef3c7;
        }

        [data-baseweb="notification"][kind="info"] {
            background: linear-gradient(135deg, rgba(56,189,248,0.18) 0%, rgba(56,189,248,0.08) 100%);
            border-left: 4px solid $info;
            color: #e0f2fe;
        }

        /* Plotly Charts - Minimal Styling */
        div[data-testid="stPlotlyChart"] {
            background: transparent;
        }
        
        div[data-testid="stPlotlyChart"] > div {
            background: transparent;
        }

        /* File Uploader */
        [data-testid="stFileUploader"] {
            border: 2px dashed rgba(255,255,255,0.14);
            border-radius: $radius_xl;
            padding: 2rem;
            background: rgba(15,23,42,0.65);
            transition: all 0.2s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: rgba(96,165,250,0.6);
            background: rgba(15,23,42,0.8);
        }

        /* Progress */
        .stProgress > div > div {
            background: $gradient_purple;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(15,23,42,0.4);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.12);
            border-radius: $radius_full;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255,255,255,0.2);
        }

        /* Streamlit chrome */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
    """)

    values = {
        'primary': COLORS['primary'],
        'primary_dark': COLORS['primary_dark'],
        'secondary': COLORS['secondary'],
        'bg_primary': COLORS['bg_primary'],
        'bg_secondary': COLORS['bg_secondary'],
        'bg_card': COLORS['bg_card'],
        'text_primary': COLORS['text_primary'],
        'text_secondary': COLORS['text_secondary'],
        'border_light': COLORS['border_light'],
        'gradient_primary': COLORS['gradient_primary'],
        'gradient_purple': COLORS['gradient_purple'],
        'success': COLORS['success'],
        'warning': COLORS['warning'],
        'danger': COLORS['danger'],
        'info': COLORS['info'],
        'shadow_card': SHADOWS['card'],
        'shadow_card_hover': SHADOWS['card_hover'],
        'radius_md': BORDER_RADIUS['md'],
        'radius_lg': BORDER_RADIUS['lg'],
        'radius_xl': BORDER_RADIUS['xl'],
        'radius_full': BORDER_RADIUS['full'],
        'font_medium': TYPOGRAPHY['font_weights']['medium'],
    }

    return css_template.substitute(values)
