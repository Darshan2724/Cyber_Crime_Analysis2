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
    
    # Create 3D scatter on globe
    fig = go.Figure(data=go.Scattergeo(
        lon=location_data['lon'],
        lat=location_data['lat'],
        text=location_data['location'],
        mode='markers',
        marker=dict(
            size=location_data['attack_count'] / 100,
            color=location_data['avg_severity'],
            colorscale=[[0, COLORS['green']], [0.5, COLORS['orange']], [1, COLORS['pink']]],
            colorbar=dict(title="Avg Severity", thickness=15),
            line=dict(width=1, color=COLORS['cyan']),
            sizemode='diameter',
            showscale=True
        ),
        hovertext=location_data['location'],
        hovertemplate='<b>%{hovertext}</b><br>' +
                      'Attacks: %{marker.size:.0f}<br>' +
                      'Avg Severity: %{marker.color:.1f}<br>' +
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

def create_3d_scatter(df, title='🔮 3D Attack Analysis'):
    """Create 3D scatter plot"""
    
    sample_df = df.sample(min(1000, len(df)))  # Sample for performance
    
    fig = px.scatter_3d(
        sample_df,
        x='attack_duration_min',
        y='data_compromised_GB',
        z='attack_severity',
        color='attack_type',
        size='response_time_min',
        hover_data=['location', 'target_system', 'outcome'],
        title=title,
        labels={
            'attack_duration_min': 'Duration (min)',
            'data_compromised_GB': 'Data Loss (GB)',
            'attack_severity': 'Severity'
        },
        color_discrete_sequence=[COLORS['cyan'], COLORS['purple'], COLORS['pink'], 
                                COLORS['green'], COLORS['orange']]
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

def create_heatmap_calendar(df, title='📅 Attack Calendar Heatmap'):
    """Create calendar heatmap"""
    
    # Aggregate by date
    daily_attacks = df.groupby(df['timestamp'].dt.date).size().reset_index(name='count')
    daily_attacks.columns = ['date', 'count']
    daily_attacks['date'] = pd.to_datetime(daily_attacks['date'])
    daily_attacks['day_of_week'] = daily_attacks['date'].dt.dayofweek
    daily_attacks['week'] = daily_attacks['date'].dt.isocalendar().week
    
    # Pivot for heatmap
    heatmap_data = daily_attacks.pivot_table(
        index='day_of_week',
        columns='week',
        values='count',
        fill_value=0
    )
    
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=[day_names[i] for i in heatmap_data.index],
        colorscale=[[0, COLORS['bg']], [0.5, COLORS['purple']], [1, COLORS['pink']]],
        hoverongaps=False,
        hovertemplate='Week %{x}<br>%{y}<br>Attacks: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Week of Year',
        yaxis_title='Day of Week'
    )
    apply_theme(fig, title=title, height=400)
    
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


def create_mitigation_chart(df, title='🛠️ Mitigation Methods Breakdown'):
    """Simple bar chart showing top mitigation methods and counts"""
    data = df.groupby('mitigation_method').size().reset_index(name='count').nlargest(10, 'count')
    if data.empty:
        # fallback to default placeholder
        data = pd.DataFrame({'mitigation_method': ['Standard Protocol'], 'count': [len(df)]})

    fig = px.bar(
        data,
        x='count',
        y='mitigation_method',
        orientation='h',
        title=title,
        color='count',
        color_continuous_scale=[[0, COLORS['cyan']], [0.5, COLORS['purple']], [1, COLORS['pink']]]
    )
    fig.update_layout(showlegend=False)
    apply_theme(fig, title=title, height=400)
    return fig

def create_waterfall_chart(df, title='💧 Cumulative Attack Impact'):
    """Create waterfall chart"""
    
    # Calculate cumulative data loss by attack type
    attack_impact = df.groupby('attack_type')['data_compromised_GB'].sum().sort_values(ascending=False)
    
    fig = go.Figure(go.Waterfall(
        name="Data Loss",
        orientation="v",
        measure=["relative"] * len(attack_impact),
        x=attack_impact.index.tolist(),
        y=attack_impact.values.tolist(),
        connector={"line": {"color": COLORS['cyan']}},
        increasing={"marker": {"color": COLORS['pink']}},
        decreasing={"marker": {"color": COLORS['green']}},
        totals={"marker": {"color": COLORS['purple']}}
    ))
    
    fig.update_layout(
        xaxis_title="Attack Type",
        yaxis_title="Data Compromised (GB)"
    )
    apply_theme(fig, title=title, height=500)
    
    return fig
