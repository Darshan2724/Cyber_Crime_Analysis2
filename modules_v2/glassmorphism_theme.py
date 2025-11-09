"""
Glassmorphism Cyber Theme Module
Advanced CSS styling with glassmorphic effects, animations, and cyber aesthetics
"""

import streamlit as st

# Color Palette - Glassmorphism Cyber Theme (Updated for better visibility)
COLORS = {
    'bg_primary': '#050816',
    'bg_secondary': '#0a0f1e',
    'glass_bg': 'rgba(255, 255, 255, 0.05)',
    'glass_border': 'rgba(255, 255, 255, 0.1)',
    'gradient_start': '#4dd0e1',  # Softer cyan for better visibility
    'gradient_mid': '#7b2ff7',
    'gradient_end': '#ff006e',
    'cyan': '#4dd0e1',  # Softer cyan - easier on eyes
    'cyan_bright': '#00f5ff',  # Keep bright cyan for accents
    'purple': '#7b2ff7',
    'pink': '#ff006e',
    'green': '#00ff88',
    'orange': '#ffaa00',
    'text_primary': '#ffffff',  # Solid white for title
    'text_secondary': '#b8c5d6',
    'shadow': 'rgba(77, 208, 225, 0.3)',  # Updated shadow for softer cyan
}

def apply_glassmorphism_theme():
    """Apply complete glassmorphism cyber theme with animations"""
    
    st.markdown(f"""
    <style>
    /* ========== GLOBAL STYLES ========== */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    :root {{
        --bg-primary: {COLORS['bg_primary']};
        --bg-secondary: {COLORS['bg_secondary']};
        --glass-bg: {COLORS['glass_bg']};
        --glass-border: {COLORS['glass_border']};
        --cyan: {COLORS['cyan']};
        --purple: {COLORS['purple']};
        --pink: {COLORS['pink']};
        --green: {COLORS['green']};
        --orange: {COLORS['orange']};
    }}
    
    /* Main Background with Animated Gradient */
    .stApp {{
        background: linear-gradient(135deg, #050816 0%, #0a0f1e 50%, #050816 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* ========== GLASSMORPHIC CARDS ========== */
    .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .glass-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px 0 rgba(0, 245, 255, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.3);
    }}
    
    /* ========== TYPOGRAPHY ========== */
    h1, h2, h3 {{
        font-family: 'Orbitron', sans-serif !important;
        color: #ffffff !important;
        font-weight: 700;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.4), 0 0 20px rgba(0, 245, 255, 0.2);
    }}
    
    p, div, span, label {{
        font-family: 'Rajdhani', sans-serif !important;
        color: {COLORS['text_secondary']};
    }}
    
    /* ========== ANIMATED METRICS ========== */
    .stMetric {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .stMetric:before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 245, 255, 0.2), transparent);
        animation: shimmer 3s infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
    }}
    
    .stMetric:hover {{
        transform: scale(1.05);
        border: 1px solid {COLORS['cyan']};
        box-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
    }}
    
    .stMetric label {{
        color: {COLORS['cyan']} !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .stMetric [data-testid="stMetricValue"] {{
        font-size: 36px !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, {COLORS['cyan']}, {COLORS['purple']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 2s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    /* ========== SIDEBAR STYLING ========== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(5, 8, 22, 0.95) 0%, rgba(10, 15, 30, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 245, 255, 0.2);
    }}
    
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] .stMultiSelect {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    /* Fix multiselect tag visibility - White background with black text */
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
        background-color: white !important;
        color: black !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span {{
        color: black !important;
    }}
    
    /* X button in tags */
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] svg {{
        fill: black !important;
    }}
    
    /* ========== BUTTONS ========== */
    .stButton > button {{
        background: linear-gradient(90deg, {COLORS['cyan']}, {COLORS['purple']});
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 245, 255, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 245, 255, 0.5);
        background: linear-gradient(90deg, {COLORS['purple']}, {COLORS['pink']});
    }}
    
    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 12px 24px;
        color: {COLORS['text_secondary']};
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(0, 245, 255, 0.1);
        border: 1px solid {COLORS['cyan']};
        transform: translateY(-2px);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, {COLORS['cyan']}, {COLORS['purple']}) !important;
        color: white !important;
        border: 1px solid {COLORS['cyan']} !important;
        box-shadow: 0 5px 20px rgba(0, 245, 255, 0.4);
    }}
    
    /* ========== DATAFRAME STYLING ========== */
    .stDataFrame {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    /* ========== PLOTLY CHARTS ========== */
    .js-plotly-plot {{
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 10px;
    }}
    
    /* ========== LOADING SPINNER ========== */
    .stSpinner > div {{
        border-top-color: {COLORS['cyan']} !important;
        border-right-color: {COLORS['purple']} !important;
        border-bottom-color: {COLORS['pink']} !important;
    }}
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, {COLORS['cyan']}, {COLORS['purple']});
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, {COLORS['purple']}, {COLORS['pink']});
    }}
    
    /* ========== NEON GLOW EFFECT ========== */
    .neon-text {{
        color: {COLORS['cyan']};
        text-shadow: 
            0 0 10px {COLORS['cyan']},
            0 0 20px {COLORS['cyan']},
            0 0 30px {COLORS['cyan']},
            0 0 40px {COLORS['purple']};
        animation: neonPulse 2s ease-in-out infinite;
    }}
    
    @keyframes neonPulse {{
        0%, 100% {{ 
            text-shadow: 
                0 0 10px {COLORS['cyan']},
                0 0 20px {COLORS['cyan']},
                0 0 30px {COLORS['cyan']};
        }}
        50% {{ 
            text-shadow: 
                0 0 20px {COLORS['cyan']},
                0 0 30px {COLORS['cyan']},
                0 0 40px {COLORS['cyan']},
                0 0 50px {COLORS['purple']};
        }}
    }}
    
    /* ========== FLOATING ANIMATION ========== */
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    .floating {{
        animation: float 3s ease-in-out infinite;
    }}
    
    /* ========== HIDE STREAMLIT BRANDING ========== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* ========== CUSTOM ALERT BOXES ========== */
    .alert-success {{
        background: rgba(0, 255, 136, 0.1);
        border-left: 4px solid {COLORS['green']};
        padding: 15px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }}
    
    .alert-warning {{
        background: rgba(255, 170, 0, 0.1);
        border-left: 4px solid {COLORS['orange']};
        padding: 15px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }}
    
    .alert-danger {{
        background: rgba(255, 0, 110, 0.1);
        border-left: 4px solid {COLORS['pink']};
        padding: 15px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }}
    </style>
    """, unsafe_allow_html=True)

def create_metric_card(label, value, delta=None, icon="📊"):
    """Create animated glassmorphic metric card"""
    delta_html = f'<div style="color: {COLORS["green"]}; font-size: 14px;">▲ {delta}</div>' if delta else ''
    
    return f"""
    <div class="glass-card" style="text-align: center;">
        <div style="font-size: 40px; margin-bottom: 10px;">{icon}</div>
        <div style="color: {COLORS['cyan']}; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
            {label}
        </div>
        <div style="font-size: 36px; font-weight: 700; background: linear-gradient(90deg, {COLORS['cyan']}, {COLORS['purple']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {value}
        </div>
        {delta_html}
    </div>
    """

def create_header(title, subtitle=""):
    """Create header with solid white title and subtle glow"""
    return f"""
    <div style="text-align: center; padding: 30px 0;">
        <h1 style="
            font-size: 48px; 
            margin-bottom: 10px;
            color: #ffffff;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            letter-spacing: 3px;
            text-shadow: 0 0 10px rgba(0, 245, 255, 0.4), 0 0 20px rgba(0, 245, 255, 0.2);
        ">
            🛡️ {title}
        </h1>
        <p style="font-size: 18px; color: {COLORS['cyan']}; letter-spacing: 2px; font-weight: 600;">
            {subtitle}
        </p>
    </div>
    """

def create_section_header(title, icon=""):
    """Create section header with gradient"""
    return f"""
    <div style="margin: 30px 0 20px 0;">
        <h2 style="font-size: 28px; display: inline-block;">
            {icon} {title}
        </h2>
        <div style="height: 3px; background: linear-gradient(90deg, {COLORS['cyan']}, {COLORS['purple']}, {COLORS['pink']}); border-radius: 2px; margin-top: 10px;"></div>
    </div>
    """

def create_toast_notification(message, type="info"):
    """Create toast notification"""
    colors = {
        'info': COLORS['cyan'],
        'success': COLORS['green'],
        'warning': COLORS['orange'],
        'error': COLORS['pink']
    }
    color = colors.get(type, COLORS['cyan'])
    
    return f"""
    <div style="
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid {color};
        border-radius: 10px;
        padding: 15px 20px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        z-index: 9999;
        animation: slideIn 0.3s ease-out;
    ">
        <div style="color: {color}; font-weight: 600;">{message}</div>
    </div>
    <style>
        @keyframes slideIn {{
            from {{ transform: translateX(400px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
    </style>
    """
