"""
Advanced Visualizations Module for DarkSentinel V2
3D visualizations, animated charts, and interactive components
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Glassmorphism Cyber Theme Colors
COLORS = {
    'bg': '#050816',
    'cyan': '#00f5ff',
    'purple': '#7b2ff7',
    'pink': '#ff006e',
    'green': '#00ff88',
    'orange': '#ffaa00',
    'text': '#b8c5d6',
}

# Country coordinates for 3D globe
COUNTRY_COORDS = {
    'USA': {'lat': 37.0902, 'lon': -95.7129},
    'UK': {'lat': 55.3781, 'lon': -3.4360},
    'Germany': {'lat': 51.1657, 'lon': 10.4515},
    'France': {'lat': 46.2276, 'lon': 2.2137},
    'China': {'lat': 35.8617, 'lon': 104.1954},
    'India': {'lat': 20.5937, 'lon': 78.9629},
    'Brazil': {'lat': -14.2350, 'lon': -51.9253},
    'Russia': {'lat': 61.5240, 'lon': 105.3188},
    'Australia': {'lat': -25.2744, 'lon': 133.7751},
    'Canada': {'lat': 56.1304, 'lon': -106.3468},
    'Japan': {'lat': 36.2048, 'lon': 138.2529},
    'South Korea': {'lat': 35.9078, 'lon': 127.7669},
    'Mexico': {'lat': 23.6345, 'lon': -102.5528},
    'Italy': {'lat': 41.8719, 'lon': 12.5674},
    'Spain': {'lat': 40.4637, 'lon': -3.7492},
    'Netherlands': {'lat': 52.1326, 'lon': 5.2913},
    'Singapore': {'lat': 1.3521, 'lon': 103.8198},
    'UAE': {'lat': 23.4241, 'lon': 53.8478},
    'Vietnam': {'lat': 14.0583, 'lon': 108.2772},
    'Viet Nam': {'lat': 14.0583, 'lon': 108.2772},  # Alternative spelling
}

PLOTLY_TEMPLATE = {
    'layout': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(255, 255, 255, 0.03)',
        'font': {'color': COLORS['text'], 'family': 'Rajdhani, sans-serif', 'size': 12},
        'xaxis': {
            'gridcolor': 'rgba(255, 255, 255, 0.1)',
            'linecolor': COLORS['cyan'],
            'zerolinecolor': 'rgba(255, 255, 255, 0.1)',
        },
        'yaxis': {
            'gridcolor': 'rgba(255, 255, 255, 0.1)',
            'linecolor': COLORS['cyan'],
            'zerolinecolor': 'rgba(255, 255, 255, 0.1)',
        },
        'hoverlabel': {
            'bgcolor': 'rgba(0, 0, 0, 0.8)',
            'font_size': 12,
            'font_family': 'Rajdhani'
        }
    }
}

def apply_theme(fig, title=None, height=None):
    """Apply theme to figure with optional title and height"""
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    if title:
        fig.update_layout(title={'text': title, 'font': {'size': 20, 'color': COLORS['cyan'], 'family': 'Orbitron'}})
    if height:
        fig.update_layout(height=height)
    return fig

def create_3d_globe(df, title='🌍 Global Attack Distribution'):
    """Create 3D globe visualization with attack locations"""
    
    # Aggregate data by location
    location_data = df.groupby('location').agg({
        'attack_type': 'count',
        'data_compromised_GB': 'sum',
        'attack_severity': 'mean'
    }).reset_index()
    location_data.columns = ['location', 'attack_count', 'total_data_loss', 'avg_severity']
    
    # Add coordinates
    location_data['lat'] = location_data['location'].map(lambda x: COUNTRY_COORDS.get(x, {}).get('lat', 0))
    location_data['lon'] = location_data['location'].map(lambda x: COUNTRY_COORDS.get(x, {}).get('lon', 0))
    
    # Calculate marker sizes - much smaller and more balanced
    min_size = 2  # Very small minimum size
    max_size = 15  # Smaller maximum size
    
    # Use square root scaling for better visibility of differences
    sqrt_counts = np.sqrt(location_data['attack_count'])
    sqrt_min = sqrt_counts.min()
    sqrt_range = sqrt_counts.max() - sqrt_min if sqrt_counts.max() > sqrt_min else 1
    
    # Scale between min and max size
    marker_sizes = min_size + (max_size - min_size) * ((sqrt_counts - sqrt_min) / sqrt_range)
    
    # Create 3D scatter on globe
    fig = go.Figure(data=go.Scattergeo(
        lon=location_data['lon'],
        lat=location_data['lat'],
        text=location_data['location'],
        mode='markers',
        marker=dict(
            size=marker_sizes,
            sizemode='diameter',
            sizeref=0.5,  # Increased sizeref to make all markers smaller
            color=location_data['avg_severity'],
            colorscale=[[0, COLORS['green']], [0.5, COLORS['orange']], [1, COLORS['pink']]],
            colorbar=dict(title="Avg Severity", thickness=15),
            line=dict(width=1, color=COLORS['cyan']),
            showscale=True
        ),
        customdata=location_data[['location', 'attack_count', 'avg_severity']],
        hovertemplate='<b>%{customdata[0]}</b><br>' +
                     'Total Attacks: %{customdata[1]:,d}<br>' +
                     'Avg Severity: %{customdata[2]:.1f}<br>' +
                     '<extra></extra>'
    ))
    
    fig.update_geos(
        projection_type='orthographic',
        showcountries=True,
        countrycolor=COLORS['cyan'],
        showcoastlines=True,
        coastlinecolor=COLORS['purple'],
        showland=True,
        landcolor='rgba(10, 15, 30, 0.8)',
        showocean=True,
        oceancolor='rgba(5, 8, 22, 0.9)',
        bgcolor='rgba(0,0,0,0)',
    )
    
    apply_theme(fig, title=title, height=600)
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    
    return fig

def create_animated_timeline(df, title='📈 Attack Timeline Animation'):
    """Create animated timeline showing attacks over time"""
    
    # Aggregate by date and attack type
    timeline_data = df.groupby([df['timestamp'].dt.date, 'attack_type']).size().reset_index(name='count')
    timeline_data.columns = ['date', 'attack_type', 'count']
    
    fig = px.scatter(
        timeline_data,
        x='date',
        y='count',
        color='attack_type',
        size='count',
        animation_frame=timeline_data['date'].astype(str),
        title=title,
        labels={'count': 'Number of Attacks', 'date': 'Date'},
        color_discrete_sequence=[COLORS['cyan'], COLORS['purple'], COLORS['pink'], 
                                COLORS['green'], COLORS['orange']]
    )
    
    apply_theme(fig, title=title, height=500)
    
    return fig

def create_sunburst_chart(df, title='🎯 Attack Hierarchy'):
    """Create sunburst chart for hierarchical attack data"""
    
    # Create hierarchy: Industry -> Attack Type -> Target System
    hierarchy_data = df.groupby(['industry', 'attack_type', 'target_system']).size().reset_index(name='count')
    
    fig = px.sunburst(
        hierarchy_data,
        path=['industry', 'attack_type', 'target_system'],
        values='count',
        title=title,
        color='count',
        color_continuous_scale=[[0, COLORS['cyan']], [0.5, COLORS['purple']], [1, COLORS['pink']]]
    )
    
    apply_theme(fig, title=title, height=600)
    
    return fig

def create_3d_scatter(df, title='🔮 3D Attack Correlation Analysis'):
    """Create 3D scatter plot with even distribution across all axes"""
    
    # Sample attacks
    sample_size = min(600, len(df))
    sample_df = df.sample(sample_size, random_state=42).copy()
    
    # Convert to numeric
    sample_df['attack_duration_min'] = pd.to_numeric(sample_df['attack_duration_min'], errors='coerce').fillna(30)
    sample_df['data_compromised_GB'] = pd.to_numeric(sample_df['data_compromised_GB'], errors='coerce').fillna(10)
    sample_df['attack_severity'] = pd.to_numeric(sample_df['attack_severity'], errors='coerce').fillna(5)
    
    # Generate realistic variable response times (5-120 minutes) based on severity
    sample_df['response_time_min'] = pd.to_numeric(sample_df['response_time_min'], errors='coerce')
    # For missing values, generate based on severity (higher severity = faster response)
    mask_missing = sample_df['response_time_min'].isna()
    if mask_missing.any():
        np.random.seed(42)
        # Base response time inversely proportional to severity (high severity = fast response)
        base_response = 120 - (sample_df.loc[mask_missing, 'attack_severity'] * 10)
        # Add randomness
        random_factor = np.random.uniform(0.5, 1.5, mask_missing.sum())
        sample_df.loc[mask_missing, 'response_time_min'] = (base_response * random_factor).clip(5, 120)
    
    # Use simple rank-based approach with aggressive jitter for even distribution
    # This is more reliable than quantile binning
    
    # Create rank positions (0 to sample_size-1)
    sample_df = sample_df.reset_index(drop=True)
    sample_df['duration_rank'] = sample_df['attack_duration_min'].rank(method='first') 
    sample_df['data_rank'] = sample_df['data_compromised_GB'].rank(method='first')
    
    # Normalize to 0-1 scale then scale to display ranges
    sample_df['duration_display'] = (sample_df['duration_rank'] / sample_size) * 35
    sample_df['data_display'] = (sample_df['data_rank'] / sample_size) * 28
    
    # Severity: keep as actual values
    sample_df['severity_display'] = sample_df['attack_severity'].copy()
    
    # Add aggressive random jitter to spread points
    np.random.seed(42)
    sample_df['duration_display'] = sample_df['duration_display'] + np.random.uniform(-1.5, 1.5, sample_size)
    sample_df['data_display'] = sample_df['data_display'] + np.random.uniform(-1.2, 1.2, sample_size)
    sample_df['severity_display'] = sample_df['severity_display'] + np.random.uniform(-0.5, 0.5, sample_size)
    
    # Clip to valid ranges
    sample_df['duration_display'] = sample_df['duration_display'].clip(lower=0, upper=40)
    sample_df['data_display'] = sample_df['data_display'].clip(lower=0, upper=30)
    sample_df['severity_display'] = sample_df['severity_display'].clip(lower=1, upper=10)
    
    # Variable marker sizes
    sample_df['marker_size'] = (sample_df['response_time_min'].clip(lower=1, upper=180) / 30) + 3
    
    fig = px.scatter_3d(
        sample_df,
        x='duration_display',
        y='data_display',
        z='severity_display',
        color='attack_type',
        size='marker_size',
        hover_data=['location', 'target_system', 'outcome', 'response_time_min', 
                    'attack_duration_min', 'data_compromised_GB', 'attack_severity'],
        title=title,
        labels={
            'duration_display': 'Attack Duration',
            'data_display': 'Data Loss',
            'severity_display': 'Severity (1-10)',
            'marker_size': 'Response Time'
        },
        color_discrete_sequence=[COLORS['cyan'], COLORS['purple'], COLORS['pink'], 
                                COLORS['green'], COLORS['orange']]
    )
    
    # Enhanced hover template showing actual values
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Duration: %{customdata[4]:.0f} min<br>' +
                      'Data Loss: %{customdata[5]:.1f} GB<br>' +
                      'Severity: %{customdata[6]:.1f}/10<br>' +
                      'Location: %{customdata[0]}<br>' +
                      'Target: %{customdata[1]}<br>' +
                      'Outcome: %{customdata[2]}<br>' +
                      'Response Time: %{customdata[3]:.0f} min<br>' +
                      '<extra></extra>'
    )
    
    # Update layout with better camera angle and axis settings
    fig.update_layout(
        scene=dict(
            xaxis_title='Attack Duration<br>(Low → High)',
            yaxis_title='Data Compromised<br>(Low → High)',
            zaxis_title='Severity<br>(1-10)',
            xaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)', 
                backgroundcolor='rgba(10, 10, 30, 0.3)',
                showbackground=True,
                range=[0, 40],
                tickmode='array',
                tickvals=[0, 10, 20, 30, 40],
                ticktext=['Minimal', 'Low', 'Med', 'High', 'Max']
            ),
            yaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)', 
                backgroundcolor='rgba(10, 10, 30, 0.3)',
                showbackground=True,
                range=[0, 30],
                tickmode='array',
                tickvals=[0, 7.5, 15, 22.5, 30],
                ticktext=['Min', 'Low', 'Med', 'High', 'Max']
            ),
            zaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)', 
                backgroundcolor='rgba(10, 10, 30, 0.3)',
                showbackground=True,
                range=[0, 11],
                tickvals=[1, 3, 5, 7, 9, 10]
            ),
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.5),
                center=dict(x=0, y=0, z=-0.1)
            ),
            aspectmode='cube'
        ),
        annotations=[
            dict(
                text=f'Showing {sample_size} attacks evenly distributed | Bubble size = Response Time | Hover for actual values',
                xref='paper',
                yref='paper',
                x=0.5,
                y=-0.05,
                showarrow=False,
                font=dict(size=10, color=COLORS['text'])
            )
        ],
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0, 0, 0, 0.7)',
            font=dict(size=10)
        )
    )
    
    apply_theme(fig, title=title, height=700)
    
    return fig

def create_radar_chart(df, title='📡 Security Posture Radar'):
    """Create radar chart for security metrics"""
    
    # Calculate metrics by security tool
    tool_metrics = df.groupby('security_tools_used').agg({
        'outcome': lambda x: (x == 'Success').mean() * 100,
        'response_time_min': 'mean',
        'attack_severity': 'mean',
        'data_compromised_GB': 'mean'
    }).reset_index()
    
    # Normalize metrics to 0-100 scale
    for col in ['response_time_min', 'attack_severity', 'data_compromised_GB']:
        max_val = tool_metrics[col].max()
        if max_val > 0:
            tool_metrics[col] = (1 - tool_metrics[col] / max_val) * 100  # Invert so higher is better
    
    fig = go.Figure()
    
    for idx, row in tool_metrics.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row['outcome'], row['response_time_min'], row['attack_severity'], row['data_compromised_GB']],
            theta=['Success Rate', 'Response Speed', 'Severity Control', 'Data Protection'],
            fill='toself',
            name=row['security_tools_used'],
            line=dict(color=[COLORS['cyan'], COLORS['purple'], COLORS['pink'], 
                           COLORS['green'], COLORS['orange']][idx % 5])
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255, 255, 255, 0.1)'),
            angularaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
        )
    )
    apply_theme(fig, title=title, height=500)
    
    return fig

def create_heatmap_calendar(df, title='📅 Attack Patterns by Day of Week'):
    """Create simple bar chart showing attack distribution by day of week"""
    
    # Get day of week distribution
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_data = df['day_name'].value_counts().reindex(dow_order, fill_value=0)
    
    # Find peak day
    peak_day = dow_data.idxmax()
    peak_count = dow_data.max()
    
    # Create colors based on values
    colors_scaled = [COLORS['cyan'] if day == peak_day else COLORS['purple'] for day in dow_data.index]
    
    fig = go.Figure(go.Bar(
        x=dow_data.index,
        y=dow_data.values,
        marker=dict(
            color=colors_scaled,
            line=dict(color=COLORS['cyan'], width=2)
        ),
        text=dow_data.values,
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Attacks: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f'{title}<br><sub>Peak Activity: {peak_day} with {peak_count} attacks</sub>',
            font=dict(size=18, color=COLORS['cyan'])
        ),
        xaxis_title='Day of Week',
        yaxis_title='Number of Attacks',
        showlegend=False
    )
    
    apply_theme(fig, height=450)
    
    return fig

def create_gauge_chart(value, title='Threat Level', max_value=100):
    """Create animated gauge chart"""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24, 'color': COLORS['cyan']}},
        delta={'reference': max_value * 0.5},
        gauge={
            'axis': {'range': [None, max_value], 'tickcolor': COLORS['cyan']},
            'bar': {'color': COLORS['pink']},
            'bgcolor': 'rgba(255, 255, 255, 0.05)',
            'borderwidth': 2,
            'bordercolor': COLORS['cyan'],
            'steps': [
                {'range': [0, max_value * 0.33], 'color': 'rgba(0, 255, 136, 0.2)'},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': 'rgba(255, 170, 0, 0.2)'},
                {'range': [max_value * 0.66, max_value], 'color': 'rgba(255, 0, 110, 0.2)'}
            ],
            'threshold': {
                'line': {'color': COLORS['cyan'], 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    apply_theme(fig, title=title, height=300)
    
    return fig

def create_treemap(df, title='🗂️ Attack Distribution Treemap'):
    """Create treemap visualization"""
    
    treemap_data = df.groupby(['industry', 'attack_type']).size().reset_index(name='count')
    
    fig = px.treemap(
        treemap_data,
        path=['industry', 'attack_type'],
        values='count',
        title=title,
        color='count',
        color_continuous_scale=[[0, COLORS['cyan']], [0.5, COLORS['purple']], [1, COLORS['pink']]]
    )
    
    apply_theme(fig, title=title, height=500)
    
    return fig

def create_sankey_flow(df, title='🔀 Attack Flow Diagram'):
    """Create Sankey diagram"""
    
    # Create flow: Attack Type -> Target System -> Outcome
    flow_data = df.groupby(['attack_type', 'target_system', 'outcome']).size().reset_index(name='count')
    
    # Create node labels
    attack_types = df['attack_type'].unique().tolist()
    target_systems = df['target_system'].unique().tolist()
    outcomes = df['outcome'].unique().tolist()
    
    all_nodes = attack_types + target_systems + outcomes
    
    # Create links
    source = []
    target = []
    value = []
    
    for _, row in flow_data.iterrows():
        # Attack Type -> Target System
        source.append(all_nodes.index(row['attack_type']))
        target.append(all_nodes.index(row['target_system']))
        value.append(row['count'])
    
    fig = go.Figure(data=[go.Sankey(
        arrangement='perpendicular',
        node=dict(
            pad=30,
            thickness=30,
            line=dict(color=COLORS['cyan'], width=1),
            label=all_nodes,
            color=[COLORS['cyan']] * len(attack_types) + 
                  [COLORS['purple']] * len(target_systems) + 
                  [COLORS['pink']] * len(outcomes)
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=['rgba(0, 245, 255, 0.25)' for _ in value]
        )
    )])
    
    fig.update_layout(
        font=dict(size=12, color=COLORS['text']),
        margin=dict(l=10, r=10, t=60, b=10),
        height=700
    )
    apply_theme(fig, title=title, height=700)
    
    return fig


def create_mitigation_chart(df, title='🛠️ Mitigation Methods Used'):
    """Simple and clear chart showing most common mitigation methods"""
    
    # Count mitigation methods
    mitigation_counts = df['mitigation_method'].value_counts().head(10)
    
    # Handle empty data
    if mitigation_counts.empty:
        mitigation_counts = pd.Series([len(df)], index=['Standard Protocol'])
    
    # Create simple horizontal bar chart
    fig = go.Figure(go.Bar(
        y=mitigation_counts.index,
        x=mitigation_counts.values,
        orientation='h',
        marker=dict(
            color=mitigation_counts.values,
            colorscale=[[0, COLORS['cyan']], [0.5, COLORS['purple']], [1, COLORS['pink']]],
            showscale=False
        ),
        text=mitigation_counts.values,
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Used %{x} times<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=title + '<br><sub>Top 10 Most Frequently Used Security Measures</sub>',
            font=dict(size=18, color=COLORS['cyan'])
        ),
        xaxis_title="Number of Times Used",
        yaxis_title="Mitigation Method",
        showlegend=False,
        yaxis=dict(autorange='reversed')
    )
    
    apply_theme(fig, height=450)
    
    return fig

def create_waterfall_chart(df, title='📊 Attack Outcomes by Type'):
    """Create stacked bar chart showing attack outcomes"""
    
    # Calculate outcomes by attack type
    outcome_data = df.groupby(['attack_type', 'outcome']).size().unstack(fill_value=0)
    
    # Get top attack types
    top_attacks = df['attack_type'].value_counts().head(8).index
    outcome_data = outcome_data.loc[top_attacks] if len(outcome_data) > 0 else outcome_data
    
    # Handle empty data
    if outcome_data.empty:
        outcome_data = pd.DataFrame({'Unknown': [len(df)]}, index=['Various Attacks'])
    
    fig = go.Figure()
    
    colors_list = [COLORS['green'], COLORS['orange'], COLORS['pink'], COLORS['cyan'], COLORS['purple']]
    
    for idx, outcome in enumerate(outcome_data.columns):
        fig.add_trace(go.Bar(
            name=outcome,
            x=outcome_data.index,
            y=outcome_data[outcome],
            marker_color=colors_list[idx % len(colors_list)],
            hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>'
        ))
    
    fig.update_layout(
        barmode='stack',
        xaxis_title="Attack Type",
        yaxis_title="Number of Attacks",
        title=dict(
            text=title + '<br><sub>Distribution of Attack Outcomes by Type</sub>',
            font=dict(size=18, color=COLORS['cyan'])
        ),
        legend=dict(
            title="Outcome",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    apply_theme(fig, height=450)
    
    return fig
