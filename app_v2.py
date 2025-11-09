"""
DarkSentinel V2 - Next-Gen Cybercrime Analytics Dashboard
Complete Glassmorphism Cyber Theme Redesign with Advanced Features
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Import custom modules
from modules_v2.glassmorphism_theme import (
    apply_glassmorphism_theme, create_metric_card, create_header,
    create_section_header, create_toast_notification, COLORS
)

# Define text color for convenience
TEXT_COLOR = COLORS['text_secondary']
from modules_v2.data_loader_v2 import (
    load_data, get_data_summary, get_attack_statistics,
    get_real_time_metrics, filter_data, get_top_threats
)
from modules_v2.advanced_visuals import (
    create_3d_globe, create_animated_timeline, create_sunburst_chart,
    create_3d_scatter, create_radar_chart, create_heatmap_calendar,
    create_gauge_chart, create_treemap, create_sankey_flow, create_waterfall_chart,
    create_mitigation_chart
)
from modules_v2.live_feed import (
    create_top_attacks, create_attack_ticker, create_status_board
)

# Page configuration
st.set_page_config(
    page_title="DarkSentinel V2 | Cyber Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply glassmorphism theme
apply_glassmorphism_theme()

# Initialize session state
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'dark'
if 'show_notifications' not in st.session_state:
    st.session_state.show_notifications = True
if 'fullscreen_chart' not in st.session_state:
    st.session_state.fullscreen_chart = None

# Load data
@st.cache_data(ttl=3600)
def load_and_cache_data():
    return load_data()

# Main app
def main():
    # Header
    st.markdown(create_header(
        "DARKSENTINEL V2",
        "CYBER COMMAND CENTER | REAL-TIME THREAT INTELLIGENCE"
    ), unsafe_allow_html=True)
    
    # Load data with loading animation
    with st.spinner('🔄 Initializing Threat Intelligence System...'):
        df = load_and_cache_data()
        time.sleep(0.5)  # Brief pause for effect

    # Small data preview to validate adapter mapping (collapsible)
    with st.expander("Data mapping preview (show/hide)"):
        st.markdown("**Adapted DataFrame Columns:**")
        st.write(list(df.columns))
        st.markdown("**Sample rows (first 5):**")
        st.dataframe(df.head(5), use_container_width=True)
    
    # Show success notification
    if st.session_state.show_notifications:
        st.markdown(create_toast_notification(
            "✅ System Online | 100,000 Records Loaded",
            "success"
        ), unsafe_allow_html=True)
    
    # Sidebar - Advanced Filters
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: {COLORS['cyan']};">⚙️ CONTROL PANEL</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Date range filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>📅 DATE RANGE</p>", unsafe_allow_html=True)
        date_range = st.date_input(
            "Select date range",
            value=(df['timestamp'].min().date(), df['timestamp'].max().date()),
            min_value=df['timestamp'].min().date(),
            max_value=df['timestamp'].max().date(),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Attack type filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>⚠️ ATTACK TYPES</p>", unsafe_allow_html=True)
        attack_types = st.multiselect(
            "Select attack types",
            options=sorted(df['attack_type'].unique()),
            default=sorted(df['attack_type'].unique()),
            label_visibility="collapsed"
        )
        
        # Target system filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>🎯 TARGET SYSTEMS</p>", unsafe_allow_html=True)
        target_systems = st.multiselect(
            "Select target systems",
            options=sorted(df['target_system'].unique()),
            default=sorted(df['target_system'].unique()),
            label_visibility="collapsed"
        )
        
        # Location filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>🌍 LOCATIONS</p>", unsafe_allow_html=True)
        locations = st.multiselect(
            "Select locations",
            options=sorted(df['location'].unique()),
            default=sorted(df['location'].unique()),
            label_visibility="collapsed"
        )
        
        # Industry filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>🏢 INDUSTRIES</p>", unsafe_allow_html=True)
        industries = st.multiselect(
            "Select industries",
            options=sorted(df['industry'].unique()),
            default=sorted(df['industry'].unique()),
            label_visibility="collapsed"
        )
        
        # Severity range
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>🚨 SEVERITY RANGE</p>", unsafe_allow_html=True)
        severity_range = st.slider(
            "Select severity",
            min_value=1,
            max_value=10,
            value=(1, 10),
            label_visibility="collapsed"
        )
        
        # Outcome filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>📊 OUTCOME</p>", unsafe_allow_html=True)
        outcomes = st.multiselect(
            "Select outcomes",
            options=sorted(df['outcome'].unique()),
            default=sorted(df['outcome'].unique()),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Apply filters button
        if st.button("🔍 APPLY FILTERS", use_container_width=True):
            st.session_state.show_notifications = True
        
        # Reset filters button
        if st.button("🔄 RESET ALL", use_container_width=True):
            st.rerun()
    
    # Apply filters
    filters = {
        'date_range': date_range if len(date_range) == 2 else None,
        'attack_types': attack_types,
        'target_systems': target_systems,
        'locations': locations,
        'industries': industries,
        'severity_range': severity_range,
        'outcomes': outcomes
    }
    
    filtered_df = filter_data(df, filters)
    
    # Display filter info
    st.sidebar.markdown(f"""
    <div style="
        background: rgba(0, 245, 255, 0.1);
        border: 1px solid {COLORS['cyan']};
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        text-align: center;
    ">
        <div style="color: {COLORS['cyan']}; font-size: 14px; font-weight: 600;">
            FILTERED RECORDS
        </div>
        <div style="color: white; font-size: 28px; font-weight: bold; margin-top: 5px;">
            {len(filtered_df):,}
        </div>
        <div style="color: {TEXT_COLOR}; font-size: 12px; margin-top: 5px;">
            of {len(df):,} total
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    
    # Critical Alerts Ticker
    st.markdown(create_attack_ticker(filtered_df, n_items=10), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Real-time Status Board and Live Feed
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(create_status_board(filtered_df), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_top_attacks(filtered_df, n=10), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Metrics Dashboard
    st.markdown(create_section_header("📊 COMMAND CENTER METRICS", ""), unsafe_allow_html=True)
    
    # Calculate metrics
    total_attacks = len(filtered_df)
    successful_attacks = (filtered_df['outcome'] == 'Success').sum()
    success_rate = (successful_attacks / total_attacks * 100) if total_attacks > 0 else 0
    total_data_loss = filtered_df['data_compromised_GB'].sum()
    avg_severity = filtered_df['attack_severity'].mean()
    critical_attacks = (filtered_df['attack_severity'] >= 8).sum()
    # removed avg_response_time and unique_attackers per user request
    
    # Display metrics in glassmorphic cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "TOTAL ATTACKS",
            f"{total_attacks:,}",
            icon="🎯"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "SUCCESS RATE",
            f"{success_rate:.1f}%",
            icon="⚠️"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "DATA COMPROMISED",
            f"{total_data_loss/1024:.2f} TB",
            icon="💾"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "AVG SEVERITY",
            f"{avg_severity:.1f}/10",
            icon="🚨"
        ), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_metric_card(
            "CRITICAL THREATS",
            f"{critical_attacks:,}",
            icon="🔴"
        ), unsafe_allow_html=True)
    
    # Top attack type
    top_attack_type = filtered_df['attack_type'].mode()[0] if len(filtered_df) > 0 else 'N/A'
    with col2:
        st.markdown(create_metric_card(
            "TOP ATTACK",
            f"{top_attack_type}",
            icon="⚠️"
        ), unsafe_allow_html=True)

    # Top industry
    top_industry = filtered_df['industry'].mode()[0] if len(filtered_df) > 0 else 'N/A'
    with col3:
        st.markdown(create_metric_card(
            "TOP INDUSTRY",
            f"{top_industry}",
            icon="🏢"
        ), unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Main Visualizations
    st.markdown(create_section_header("🌐 GLOBAL THREAT INTELLIGENCE", ""), unsafe_allow_html=True)
    
    # 3D Globe
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container():
            fig_globe = create_3d_globe(filtered_df)
            st.plotly_chart(fig_globe, use_container_width=True, key="globe_main")
    
    with col2:
        # Top locations
        top_locations = filtered_df['location'].value_counts().head(10)
        fig_loc = px.bar(
            x=top_locations.values,
            y=top_locations.index,
            orientation='h',
            title='🗺️ Top Attack Locations',
            labels={'x': 'Attacks', 'y': 'Location'},
            color=top_locations.values,
            color_continuous_scale=[[0, COLORS['cyan']], [0.5, COLORS['purple']], [1, COLORS['pink']]]
        )
        fig_loc.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255, 255, 255, 0.03)',
            font=dict(color=TEXT_COLOR),
            showlegend=False,
            height=600
        )
        st.plotly_chart(fig_loc, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Attack Analysis Section
    st.markdown(create_section_header("📈 ATTACK PATTERN ANALYSIS", ""), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sunburst chart
        fig_sunburst = create_sunburst_chart(filtered_df)
        st.plotly_chart(fig_sunburst, use_container_width=True)
    
    with col2:
        # Treemap
        fig_treemap = create_treemap(filtered_df)
        st.plotly_chart(fig_treemap, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3D Scatter Analysis
    st.markdown(create_section_header("🔮 3D ATTACK CORRELATION", ""), unsafe_allow_html=True)
    fig_3d = create_3d_scatter(filtered_df)
    st.plotly_chart(fig_3d, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Security Posture
    st.markdown(create_section_header("🛡️ SECURITY POSTURE ANALYSIS", ""), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_mitigation = create_mitigation_chart(filtered_df)
        st.plotly_chart(fig_mitigation, use_container_width=True)
    
    with col2:
        fig_waterfall = create_waterfall_chart(filtered_df)
        st.plotly_chart(fig_waterfall, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Temporal Analysis
    st.markdown(create_section_header("⏰ TEMPORAL ATTACK PATTERNS", ""), unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_calendar = create_heatmap_calendar(filtered_df)
        st.plotly_chart(fig_calendar, use_container_width=True)
    
    with col2:
        # Hourly distribution
        hourly_data = filtered_df.groupby('hour').size()
        fig_hourly = px.line_polar(
            r=hourly_data.values,
            theta=[f"{h}:00" for h in hourly_data.index],
            line_close=True,
            title='🕐 24-Hour Attack Distribution'
        )
        fig_hourly.update_traces(fill='toself', line_color=COLORS['cyan'])
        fig_hourly.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                radialaxis=dict(visible=True, gridcolor='rgba(255, 255, 255, 0.1)'),
                angularaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
            ),
            font=dict(color=TEXT_COLOR),
            height=400
        )
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Attack Flow
    st.markdown(create_section_header("🔀 ATTACK FLOW DIAGRAM", ""), unsafe_allow_html=True)
    fig_sankey = create_sankey_flow(filtered_df)
    st.plotly_chart(fig_sankey, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Data Explorer
    st.markdown(create_section_header("🔍 THREAT INTELLIGENCE DATABASE", ""), unsafe_allow_html=True)
    
    # Search functionality
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_ip = st.text_input("🔎 Search by IP Address", placeholder="Enter IP...")
    
    with col2:
        search_attack = st.selectbox(
            "⚠️ Filter by Attack Type",
            ['All'] + sorted(filtered_df['attack_type'].unique().tolist())
        )
    
    with col3:
        search_severity = st.selectbox(
            "🚨 Filter by Severity",
            ['All', 'Low (1-3)', 'Medium (4-6)', 'High (7-10)']
        )
    
    # Apply search filters
    display_df = filtered_df.copy()
    
    if search_ip:
        display_df = display_df[
            display_df['attacker_ip'].str.contains(search_ip, case=False) |
            display_df['target_ip'].str.contains(search_ip, case=False)
        ]
    
    if search_attack != 'All':
        display_df = display_df[display_df['attack_type'] == search_attack]
    
    if search_severity != 'All':
        if search_severity == 'Low (1-3)':
            display_df = display_df[display_df['attack_severity'] <= 3]
        elif search_severity == 'Medium (4-6)':
            display_df = display_df[(display_df['attack_severity'] >= 4) & (display_df['attack_severity'] <= 6)]
        elif search_severity == 'High (7-10)':
            display_df = display_df[display_df['attack_severity'] >= 7]
    
    # Display dataframe
    st.dataframe(
        display_df[[
            'timestamp', 'attack_type', 'target_system', 'outcome',
            'attacker_ip', 'target_ip', 'location', 'industry',
            'attack_severity', 'data_compromised_GB', 'mitigation_method'
        ]].head(100),
        use_container_width=True,
        height=400
    )
    
    # Export functionality
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 EXPORT TO CSV",
            data=csv,
            file_name=f"darksentinel_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("📊 GENERATE REPORT", use_container_width=True):
            st.markdown(create_toast_notification(
                "📄 Report generation initiated...",
                "info"
            ), unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 30px;
        background: rgba(255, 255, 255, 0.02);
        border-top: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 10px;
    ">
        <div style="color: {COLORS['cyan']}; font-size: 24px; font-weight: bold; margin-bottom: 10px;">
            🛡️ DARKSENTINEL V2
        </div>
        <div style="color: {TEXT_COLOR}; font-size: 14px;">
            Next-Generation Cyber Threat Intelligence Platform
        </div>
        <div style="color: {COLORS['purple']}; font-size: 12px; margin-top: 10px;">
            Powered by Advanced AI & Real-Time Analytics | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
