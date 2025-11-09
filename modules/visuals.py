"""
Visualization Module for DarkSentinel
Contains all chart and graph generation functions
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Cyber Dark Neon Theme Colors
COLORS = {
    'background': '#0b0f14',
    'primary': '#00e5ff',
    'secondary': '#ff2f92',
    'success': '#7CFF00',
    'text': '#d0d7de',
    'card': '#1a1f26'
}

PLOTLY_TEMPLATE = {
    'layout': {
        'paper_bgcolor': COLORS['background'],
        'plot_bgcolor': COLORS['card'],
        'font': {'color': COLORS['text'], 'family': 'Roboto Mono'},
        'title': {'font': {'size': 20, 'color': COLORS['primary']}},
        'xaxis': {'gridcolor': '#2d3748', 'linecolor': COLORS['primary']},
        'yaxis': {'gridcolor': '#2d3748', 'linecolor': COLORS['primary']}
    }
}

def create_time_series_chart(df, date_col='Date', title='Attacks Over Time'):
    """Create time series chart of attacks with improved scaling and visibility"""
    # Resample to monthly data if we have daily data
    if pd.api.types.is_datetime64_any_dtype(df[date_col]):
        time_data = df.set_index(date_col).resample('M').size().reset_index(name='count')
        time_data[date_col] = time_data[date_col].dt.strftime('%Y-%m')
    else:
        time_data = df.groupby(date_col).size().reset_index(name='count')
    
    # Calculate 3-month moving average for trend line
    time_data['moving_avg'] = time_data['count'].rolling(window=3, min_periods=1).mean()
    
    # Create figure with secondary y-axis for better scaling
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    
    # Add bar chart for actual counts
    fig.add_trace(
        go.Bar(
            x=time_data[date_col],
            y=time_data['count'],
            name='Monthly Attacks',
            marker_color=COLORS['primary'],
            opacity=0.7,
            hovertemplate='<b>%{x}</b><br>Attacks: %{y:,d}<extra></extra>'
        ),
        secondary_y=False,
    )
    
    # Add line for moving average
    fig.add_trace(
        go.Scatter(
            x=time_data[date_col],
            y=time_data['moving_avg'],
            name='3-Month Trend',
            line=dict(color=COLORS['success'], width=3),
            hovertemplate='<b>%{x}</b><br>3-Month Avg: %{y:,.1f}<extra></extra>'
        ),
        secondary_y=False,
    )
    
    # Update layout for better visibility
    fig.update_layout(
        **PLOTLY_TEMPLATE['layout'],
        title=title,
        xaxis=dict(
            title='Date',
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickangle=45
        ),
        yaxis=dict(
            title='Number of Attacks',
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            type='log' if time_data['count'].max() > 5 * time_data['count'].min() > 0 else 'linear',
            autorange=True
        ),
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add range slider for better navigation
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    
    return fig

def create_attack_type_chart(df, color_by='Year', title='Attack Types Distribution'):
    """Create histogram of attack types"""
    fig = px.histogram(
        df, 
        x='Attack Type', 
        color=color_by,
        title=title,
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success'], '#FFD700']
    )
    
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    
    return fig

def create_severity_pie_chart(df, title='Severity Level Distribution'):
    """Create pie chart for severity levels"""
    severity_counts = df['Severity Level'].value_counts()
    
    fig = px.pie(
        values=severity_counts.values,
        names=severity_counts.index,
        title=title,
        color_discrete_sequence=[COLORS['success'], '#FFD700', COLORS['secondary'], COLORS['primary']]
    )
    
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

def create_device_os_chart(df, title='Device/OS Distribution'):
    """Create pie chart for device/OS distribution"""
    device_counts = df['Device/OS'].value_counts()
    
    fig = px.pie(
        values=device_counts.values,
        names=device_counts.index,
        title=title,
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

def create_protocol_attack_chart(df, title='Protocol vs Attack Type'):
    """Create histogram of protocols by attack type"""
    fig = px.histogram(
        df,
        x='Protocol',
        color='Attack Type',
        title=title,
        barmode='group',
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success']]
    )
    
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    
    return fig

def create_action_taken_chart(df, title='Actions Taken Distribution'):
    """Create bar chart for actions taken"""
    action_counts = df['Action Taken'].value_counts()
    
    fig = px.bar(
        x=action_counts.index,
        y=action_counts.values,
        title=title,
        labels={'x': 'Action', 'y': 'Count'},
        color=action_counts.values,
        color_continuous_scale=[[0, COLORS['secondary']], [0.5, '#FFD700'], [1, COLORS['success']]]
    )
    
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    
    return fig

def create_geo_map(df, title='Attack Distribution by Location'):
    """Create geographic scatter map"""
    geo_data = df.groupby(['City', 'State']).size().reset_index(name='count')
    
    # For demonstration, we'll create a simple bar chart of top cities
    # In production, you'd use actual lat/lon coordinates
    top_cities = geo_data.nlargest(20, 'count')
    
    fig = px.bar(
        top_cities,
        x='count',
        y='City',
        orientation='h',
        title=title,
        labels={'count': 'Number of Attacks', 'City': 'City'},
        color='count',
        color_continuous_scale=[[0, COLORS['primary']], [1, COLORS['secondary']]]
    )
    
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    
    return fig

def create_hourly_heatmap(df, title='Attack Patterns by Hour and Day'):
    """Create heatmap of attacks by hour and day of week"""
    heatmap_data = df.groupby(['DayofWeek', 'Hour']).size().reset_index(name='count')
    heatmap_pivot = heatmap_data.pivot(index='DayofWeek', columns='Hour', values='count').fillna(0)
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=[day_names[i] for i in heatmap_pivot.index],
        colorscale=[[0, COLORS['background']], [0.5, COLORS['primary']], [1, COLORS['secondary']]],
        hoverongaps=False
    ))
    
    fig.update_layout(
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        **PLOTLY_TEMPLATE['layout']
    )
    fig.update_layout(title=title)
    
    return fig

def create_monthly_trend_chart(df, title='Monthly Attack Trends'):
    """Create line chart showing monthly trends"""
    monthly_data = df.groupby(['Year', 'Month']).size().reset_index(name='count')
    monthly_data['YearMonth'] = monthly_data['Year'].astype(str) + '-' + monthly_data['Month'].astype(str).str.zfill(2)
    
    fig = px.line(
        monthly_data,
        x='YearMonth',
        y='count',
        title=title,
        labels={'count': 'Number of Attacks', 'YearMonth': 'Year-Month'},
        markers=True
    )
    
    fig.update_traces(line_color=COLORS['success'], marker=dict(size=8, color=COLORS['primary']))
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    
    return fig

def create_browser_traffic_chart(df, title='Traffic Type by Browser'):
    """Create stacked bar chart of traffic types by browser"""
    fig = px.histogram(
        df,
        x='Traffic Type',
        color='Browser',
        title=title,
        barmode='stack',
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary']]
    )
    
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    
    return fig

def create_packet_length_distribution(df, title='Packet Length Distribution'):
    """Create histogram of packet lengths"""
    fig = px.histogram(
        df,
        x='Packet Length',
        nbins=50,
        title=title,
        labels={'Packet Length': 'Packet Length (bytes)'},
        color_discrete_sequence=[COLORS['primary']]
    )
    
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    
    return fig

def create_ids_firewall_chart(df, title='IDS/IPS Alerts vs Action Taken'):
    """Create grouped bar chart for IDS alerts and actions"""
    fig = px.histogram(
        df,
        x='Action Taken',
        color='IDS/IPS Alerts',
        title=title,
        barmode='group',
        color_discrete_sequence=[COLORS['secondary'], COLORS['primary']]
    )
    
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    
    return fig

def create_sankey_diagram(df, title='Attack Flow: Protocol → Attack Type → Action'):
    """Create Sankey diagram showing flow from protocol to attack type to action"""
    # Prepare data for Sankey
    # Limit to top categories to avoid clutter
    top_protocols = df['Protocol'].value_counts().head(3).index.tolist()
    top_attacks = df['Attack Type'].value_counts().head(3).index.tolist()
    
    filtered_df = df[df['Protocol'].isin(top_protocols) & df['Attack Type'].isin(top_attacks)]
    
    # Create node labels
    protocols = filtered_df['Protocol'].unique().tolist()
    attacks = filtered_df['Attack Type'].unique().tolist()
    actions = filtered_df['Action Taken'].unique().tolist()
    
    all_nodes = protocols + attacks + actions
    
    # Create links
    links = []
    
    # Protocol to Attack Type
    for protocol in protocols:
        for attack in attacks:
            count = len(filtered_df[(filtered_df['Protocol'] == protocol) & (filtered_df['Attack Type'] == attack)])
            if count > 0:
                links.append({
                    'source': all_nodes.index(protocol),
                    'target': all_nodes.index(attack),
                    'value': count
                })
    
    # Attack Type to Action
    for attack in attacks:
        for action in actions:
            count = len(filtered_df[(filtered_df['Attack Type'] == attack) & (filtered_df['Action Taken'] == action)])
            if count > 0:
                links.append({
                    'source': all_nodes.index(attack),
                    'target': all_nodes.index(action),
                    'value': count
                })
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color=COLORS['primary'], width=0.5),
            label=all_nodes,
            color=COLORS['primary']
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
            color='rgba(0, 229, 255, 0.3)'
        )
    )])
    
    fig.update_layout(
        title=title,
        font=dict(size=12, color=COLORS['text']),
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background']
    )
    
    return fig

def create_anomaly_score_distribution(df, title='Anomaly Score Distribution'):
    """Create histogram of anomaly scores with threshold line"""
    mean_score = df['Anomaly Scores'].mean()
    std_score = df['Anomaly Scores'].std()
    threshold = mean_score + 2 * std_score
    
    fig = px.histogram(
        df,
        x='Anomaly Scores',
        nbins=50,
        title=title,
        labels={'Anomaly Scores': 'Anomaly Score'},
        color_discrete_sequence=[COLORS['primary']]
    )
    
    # Add threshold line
    fig.add_vline(
        x=threshold,
        line_dash="dash",
        line_color=COLORS['secondary'],
        annotation_text=f"Threshold: {threshold:.2f}",
        annotation_position="top"
    )
    
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    
    return fig
