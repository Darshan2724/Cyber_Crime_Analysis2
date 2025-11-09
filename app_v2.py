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
if 'filters_applied' not in st.session_state:
    st.session_state.filters_applied = False

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
    
    # Load data
    df = load_and_cache_data()

    # Data preview removed per user request
    
    # Notification removed per user request
    
    # Sidebar - Advanced Filters
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: {COLORS['cyan']};">⚙️ CONTROL PANEL</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Time period filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>📅 TIME PERIOD</p>", unsafe_allow_html=True)
        
        # Preset time ranges
        time_preset = st.selectbox(
            "Quick Select",
            options=['All Time', 'Past 2 Weeks', 'Past Month', 'Past 6 Months', 'Past Year', 'Custom Year Range'],
            index=0,
            label_visibility="collapsed",
            key="time_preset_selector"
        )
        
        # Store previous selection to detect changes
        if 'prev_time_preset' not in st.session_state:
            st.session_state.prev_time_preset = 'All Time'
        
        # Auto-apply if preset changed (data will auto-refresh)
        if time_preset != st.session_state.prev_time_preset:
            st.session_state.prev_time_preset = time_preset
            # Only auto-rerun for non-custom ranges
            if time_preset != 'Custom Year Range':
                st.rerun()
        
        # Calculate date range based on preset
        max_date = df['timestamp'].max()
        min_date = df['timestamp'].min()
        
        if time_preset == 'Past 2 Weeks':
            start_date = (max_date - pd.Timedelta(days=14)).date()
            end_date = max_date.date()
        elif time_preset == 'Past Month':
            start_date = (max_date - pd.Timedelta(days=30)).date()
            end_date = max_date.date()
        elif time_preset == 'Past 6 Months':
            start_date = (max_date - pd.Timedelta(days=180)).date()
            end_date = max_date.date()
        elif time_preset == 'Past Year':
            start_date = (max_date - pd.Timedelta(days=365)).date()
            end_date = max_date.date()
        elif time_preset == 'Custom Year Range':
            # Year range selector
            min_year = min_date.year
            max_year = max_date.year
            col_y1, col_y2 = st.columns(2)
            with col_y1:
                start_year = st.selectbox("From", range(min_year, max_year + 1), index=0, key="start_year")
            with col_y2:
                end_year = st.selectbox("To", range(min_year, max_year + 1), index=max_year - min_year, key="end_year")
            start_date = pd.Timestamp(year=start_year, month=1, day=1).date()
            end_date = pd.Timestamp(year=end_year, month=12, day=31).date()
        else:  # All Time
            start_date = min_date.date()
            end_date = max_date.date()
        
        date_range = (start_date, end_date)
        
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
            st.session_state.filters_applied = True
            st.rerun()
        
        # Reset filters button
        if st.button("🔄 RESET ALL", use_container_width=True):
            st.session_state.filters_applied = False
            st.rerun()
    
    # Apply filters
    # Ensure date_range is a tuple with both values
    valid_date_range = None
    if isinstance(date_range, tuple) and len(date_range) == 2:
        if date_range[0] is not None and date_range[1] is not None:
            valid_date_range = date_range
    
    filters = {
        'date_range': valid_date_range,
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
    # Top attacks display (full width, system status removed per user request)
    st.markdown(create_top_attacks(filtered_df, n=10), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Metrics Dashboard
    st.markdown(create_section_header("📊 COMMAND CENTER METRICS", ""), unsafe_allow_html=True)
    
    # Calculate metrics with robust error handling
    total_attacks = len(filtered_df)
    
    # Convert severity to numeric FIRST - this is crucial
    filtered_df_copy = filtered_df.copy()
    filtered_df_copy['severity_num'] = pd.to_numeric(filtered_df_copy['attack_severity'], errors='coerce')
    
    # Fill NaN with 5 and ensure numeric type
    filtered_df_copy['severity_num'] = filtered_df_copy['severity_num'].fillna(5).astype(float)
    
    # Critical attacks - count severity >= 8
    # If no attacks >= 8, show top 20% as critical based on severity
    critical_attacks = int((filtered_df_copy['severity_num'] >= 8).sum())
    if critical_attacks == 0:
        # Show top 20% of attacks by severity as critical
        threshold = filtered_df_copy['severity_num'].quantile(0.80)
        critical_attacks = int((filtered_df_copy['severity_num'] >= threshold).sum())
    
    # Average severity
    avg_severity = float(filtered_df_copy['severity_num'].mean())
    
    # Convert data loss to numeric
    filtered_df_copy['data_loss_num'] = pd.to_numeric(filtered_df_copy['data_compromised_GB'], errors='coerce').fillna(0)
    total_data_loss = float(filtered_df_copy['data_loss_num'].sum())
    
    # Calculate mitigation rate from outcomes
    defensive_keywords = ['block', 'quarantine', 'prevent', 'stop', 'resolve', 'mitigat', 'logged']
    defensive_count = filtered_df_copy['outcome'].astype(str).str.lower().apply(
        lambda x: any(keyword in x for keyword in defensive_keywords)
    ).sum()
    
    # Fallback: use low data loss as proxy for mitigation
    if defensive_count == 0:
        defensive_count = (filtered_df_copy['data_loss_num'] < 10).sum()
    
    mitigation_rate = (defensive_count / total_attacks * 100) if total_attacks > 0 else 0
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
            "MITIGATION RATE",
            f"{mitigation_rate:.1f}%",
            icon="🛡️"
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
        # Top locations - dynamic based on filtered data
        top_locations = filtered_df['location'].value_counts().head(10)
        
        # Create custom colors for the top 3 locations
        colors = []
        for i in range(len(top_locations)):
            if i == 0:
                colors.append(COLORS['pink'])  # 1st place
            elif i == 1:
                colors.append(COLORS['purple'])  # 2nd place
            elif i == 2:
                colors.append(COLORS['cyan'])  # 3rd place
            else:
                colors.append(COLORS['text_secondary'])  # Other locations
        
        fig_loc = go.Figure(go.Bar(
            x=top_locations.values,
            y=top_locations.index,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color=COLORS['cyan'], width=1)
            ),
            text=top_locations.values,
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Total Attacks: %{x:,d}<extra></extra>'
        ))
        
        fig_loc.update_layout(
            title=dict(
                text='🗺️ Top Attack Locations',
                font=dict(size=20, color=COLORS['cyan']),
                x=0.5,
                xanchor='center'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255, 255, 255, 0.03)',
            font=dict(color=TEXT_COLOR),
            showlegend=False,
            height=600,
            xaxis=dict(
                title='Number of Attacks',
                gridcolor='rgba(255, 255, 255, 0.1)',
                showgrid=True
            ),
            yaxis=dict(
                title='',
                autorange='reversed'  # Highest on top
            ),
            margin=dict(l=0, r=0, t=40, b=20)
        )
        st.plotly_chart(fig_loc, use_container_width=True, key="top_locations")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Attack Analysis Section
    st.markdown(create_section_header("📈 ATTACK PATTERN ANALYSIS", ""), unsafe_allow_html=True)
    
    # Create columns for the charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Sunburst chart in a glass card
        st.markdown("<div class='glass-card' style='padding: 15px; height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: " + COLORS['cyan'] + "; text-align: center;'>🌐 Attack Distribution</h3>", unsafe_allow_html=True)
        fig_sunburst = create_sunburst_chart(filtered_df)
        st.plotly_chart(fig_sunburst, use_container_width=True, key="sunburst_chart")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Treemap in a glass card
        st.markdown("<div class='glass-card' style='padding: 15px; height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: " + COLORS['cyan'] + "; text-align: center;'>🌳 Attack Categories</h3>", unsafe_allow_html=True)
        fig_treemap = create_treemap(filtered_df)
        st.plotly_chart(fig_treemap, use_container_width=True, key="treemap")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3D Scatter Analysis
    st.markdown(create_section_header("🔮 3D ATTACK CORRELATION", ""), unsafe_allow_html=True)
    fig_3d = create_3d_scatter(filtered_df)
    st.plotly_chart(fig_3d, use_container_width=True, key="3d_scatter")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Security Posture
    st.markdown(create_section_header("🛡️ SECURITY POSTURE ANALYSIS", ""), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_mitigation = create_mitigation_chart(filtered_df)
        st.plotly_chart(fig_mitigation, use_container_width=True, key="mitigation_chart")
    
    with col2:
        fig_waterfall = create_waterfall_chart(filtered_df)
        st.plotly_chart(fig_waterfall, use_container_width=True, key="waterfall_chart")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Temporal Analysis
    st.markdown(create_section_header("⏰ TEMPORAL ATTACK PATTERNS", ""), unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_calendar = create_heatmap_calendar(filtered_df)
        st.plotly_chart(fig_calendar, use_container_width=True, key="calendar_heatmap")
    
    with col2:
        # Time period distribution - clearer visualization
        # Group hours into time periods for better clarity
        def get_time_period(hour):
            if 0 <= hour < 6:
                return 'Night\n(12AM-6AM)'
            elif 6 <= hour < 12:
                return 'Morning\n(6AM-12PM)'
            elif 12 <= hour < 18:
                return 'Afternoon\n(12PM-6PM)'
            else:
                return 'Evening\n(6PM-12AM)'
        
        # Group by time period
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['time_period'] = filtered_df_copy['hour'].apply(get_time_period)
        
        period_order = ['Night\n(12AM-6AM)', 'Morning\n(6AM-12PM)', 'Afternoon\n(12PM-6PM)', 'Evening\n(6PM-12AM)']
        period_data = filtered_df_copy['time_period'].value_counts().reindex(period_order, fill_value=0)
        
        # Find peak period
        peak_period = period_data.idxmax()
        peak_count = period_data.max()
        
        # Create color gradient
        colors_periods = [COLORS['pink'] if period == peak_period else COLORS['cyan'] for period in period_order]
        
        fig_period = go.Figure(go.Bar(
            x=period_order,
            y=period_data.values,
            marker=dict(
                color=colors_periods,
                line=dict(color=COLORS['cyan'], width=2)
            ),
            text=period_data.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Attacks: %{y}<extra></extra>'
        ))
        
        fig_period.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255, 255, 255, 0.03)',
            font=dict(color=TEXT_COLOR),
            title=dict(
                text=f'🕐 Attack Distribution by Time<br><sub>Peak Period: {peak_period.split(chr(10))[0]} with {peak_count} attacks</sub>',
                font=dict(size=16, color=COLORS['cyan'])
            ),
            xaxis=dict(
                title='',
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            yaxis=dict(
                title='Number of Attacks',
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            showlegend=False,
            height=450
        )
        st.plotly_chart(fig_period, use_container_width=True, key="time_period_chart")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Attack Flow
    st.markdown(create_section_header("🔀 ATTACK FLOW DIAGRAM", ""), unsafe_allow_html=True)
    fig_sankey = create_sankey_flow(filtered_df)
    st.plotly_chart(fig_sankey, use_container_width=True, key="sankey_chart")
    
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
        width='stretch',
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
