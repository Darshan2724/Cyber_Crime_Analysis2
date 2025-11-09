"""
Live Attack Feed Module
Terminal-style scrolling feed of recent attacks
"""

import streamlit as st
import pandas as pd
from datetime import datetime

COLORS = {
    'cyan': '#00f5ff',
    'purple': '#7b2ff7',
    'pink': '#ff006e',
    'green': '#00ff88',
    'orange': '#ffaa00',
    'text': '#b8c5d6',
}

def create_terminal_feed(df, n_recent=20):
    """
    Create terminal-style live attack feed
    
    Parameters:
    -----------
    df : pd.DataFrame
        Attack data
    n_recent : int
        Number of recent attacks to show
        
    Returns:
    --------
    str
        HTML for terminal feed
    """
    
    # Get most recent attacks
    recent_attacks = df.nlargest(n_recent, 'timestamp')
    
    feed_html = f"""
    <div style="
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid {COLORS['cyan']};
        border-radius: 10px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        height: 500px;
        overflow-y: auto;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
    ">
        <div style="color: {COLORS['cyan']}; font-weight: bold; margin-bottom: 15px; font-size: 16px;">
            🖥️ LIVE ATTACK FEED - TERMINAL MODE
        </div>
        <div style="color: {COLORS['green']}; margin-bottom: 10px;">
            ┌─[darksentinel@security]─[~]
        </div>
    """
    
    for idx, attack in recent_attacks.iterrows():
        # Determine severity color
        severity = attack['attack_severity']
        if severity >= 8:
            sev_color = COLORS['pink']
            sev_icon = '🔴'
        elif severity >= 5:
            sev_color = COLORS['orange']
            sev_icon = '🟡'
        else:
            sev_color = COLORS['green']
            sev_icon = '🟢'
        
        # Determine outcome color
        outcome_color = COLORS['pink'] if attack['outcome'] == 'Success' else COLORS['green']
        outcome_icon = '⚠️' if attack['outcome'] == 'Success' else '✓'
        
        timestamp_str = attack['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        feed_html += f"""
        <div style="margin: 10px 0; padding: 10px; background: rgba(255, 255, 255, 0.02); border-left: 3px solid {sev_color}; border-radius: 5px;">
            <div style="color: {COLORS['cyan']};">
                └─$ [{timestamp_str}] {sev_icon} SEVERITY: {severity}/10
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ TYPE: <span style="color: {COLORS['pink']};">{attack['attack_type']}</span>
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ TARGET: <span style="color: white;">{attack['target_system']}</span> @ {attack['location']}
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ SOURCE: <span style="color: {COLORS['orange']};">{attack['attacker_ip']}</span> → {attack['target_ip']}
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ DATA LOSS: <span style="color: {COLORS['pink']};">{attack['data_compromised_GB']:.2f} GB</span>
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ DURATION: {attack['attack_duration_min']} min | RESPONSE: {attack['response_time_min']} min
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ MITIGATION: <span style="color: {COLORS['green']};">{attack['mitigation_method']}</span>
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                └─ STATUS: <span style="color: {outcome_color};">{outcome_icon} {attack['outcome']}</span>
            </div>
        </div>
        """
    
    feed_html += """
        <div style="color: #00ff88; margin-top: 15px;">
            └─[EOF] End of feed
        </div>
    </div>
    
    <style>
        /* Custom scrollbar for terminal */
        div::-webkit-scrollbar {
            width: 8px;
        }
        div::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.5);
        }
        div::-webkit-scrollbar-thumb {
            background: #00f5ff;
            border-radius: 4px;
        }
        div::-webkit-scrollbar-thumb:hover {
            background: #7b2ff7;
        }
    </style>
    """
    
    return feed_html

def create_attack_ticker(df, n_items=5):
    """
    Create scrolling ticker of critical attacks
    
    Parameters:
    -----------
    df : pd.DataFrame
        Attack data
    n_items : int
        Number of items in ticker
        
    Returns:
    --------
    str
        HTML for ticker
    """
    
    # Get critical attacks (severity >= 8)
    critical = df[df['attack_severity'] >= 8].nlargest(n_items, 'timestamp')
    
    ticker_items = []
    for idx, attack in critical.iterrows():
        ticker_items.append(
            f"🚨 {attack['attack_type']} on {attack['target_system']} "
            f"in {attack['location']} - {attack['data_compromised_GB']:.1f}GB lost"
        )
    
    ticker_text = " | ".join(ticker_items)
    
    ticker_html = f"""
    <div style="
        background: linear-gradient(90deg, rgba(255, 0, 110, 0.2), rgba(123, 47, 247, 0.2));
        border: 1px solid {COLORS['pink']};
        border-radius: 10px;
        padding: 15px;
        overflow: hidden;
        white-space: nowrap;
        position: relative;
    ">
        <div style="
            display: inline-block;
            padding-left: 100%;
            animation: scroll-left 30s linear infinite;
            color: white;
            font-weight: 600;
            font-size: 14px;
        ">
            {ticker_text}
        </div>
    </div>
    
    <style>
        @keyframes scroll-left {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-100%); }}
        }}
    </style>
    """
    
    return ticker_html


def create_top_attacks(df, n=10):
        """
        Create an HTML block listing top N attacks with concise info.
        """
        # Sort by severity then data loss
        if 'attack_severity' in df.columns:
                top = df.sort_values(['attack_severity', 'data_compromised_GB'], ascending=False).head(n)
        else:
                top = df.sort_values('data_compromised_GB', ascending=False).head(n)

        rows = []
        for _, a in top.iterrows():
                ts = pd.to_datetime(a.get('timestamp', pd.Timestamp.now()))
                rows.append(f"<tr>\n<td style='padding:8px'>{ts.strftime('%Y-%m-%d')}</td>\n<td style='padding:8px'>{a.get('attack_type','Unknown')}</td>\n<td style='padding:8px'>{a.get('target_system','Unknown')}</td>\n<td style='padding:8px'>{a.get('location','Unknown')}</td>\n<td style='padding:8px'>{a.get('attack_severity',0)}</td>\n<td style='padding:8px'>{a.get('data_compromised_GB',0):.1f} GB</td>\n</tr>")

        table_html = f"""
        <div style="background: rgba(0,0,0,0.6); border:1px solid {COLORS['cyan']}; border-radius:10px; padding:12px;">
            <div style="color: {COLORS['cyan']}; font-weight:700; margin-bottom:8px;">🏆 TOP {n} ATTACKS</div>
            <table style="width:100%; border-collapse:collapse; color: white; font-size:13px;">
                <thead>
                    <tr style="text-align:left; border-bottom:1px solid rgba(255,255,255,0.08)">
                        <th style="padding:8px">Date</th><th>Type</th><th>Target</th><th>Location</th><th>Severity</th><th>Data Loss</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        </div>
        """

        return table_html

def create_status_board(df):
    """
    Create real-time status board
    
    Parameters:
    -----------
    df : pd.DataFrame
        Attack data
        
    Returns:
    --------
    str
        HTML for status board
    """
    
    # Calculate real-time stats
    total_attacks = len(df)
    active_threats = (df['outcome'] == 'Success').sum()
    critical_count = (df['attack_severity'] >= 8).sum()
    total_data_loss = df['data_compromised_GB'].sum()
    
    # Create a compact status board (removed big threat banner per request)
    status_html = f"""
    <div style="background: rgba(0, 0, 0, 0.6); border-radius: 12px; padding: 14px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="color: {COLORS['cyan']}; font-weight:700;">⚡ SYSTEM STATUS</div>
        <div style="color: {COLORS['text']}; font-size:12px;">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <div style="background: rgba(255,255,255,0.03); padding:10px; border-radius:8px;">
          <div style="color:{COLORS['cyan']}; font-size:11px;">TOTAL ATTACKS</div>
          <div style="color:white; font-weight:700; font-size:20px;">{total_attacks:,}</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding:10px; border-radius:8px;">
          <div style="color:{COLORS['pink']}; font-size:11px;">SUCCESSFUL ATTACKS</div>
          <div style="color:white; font-weight:700; font-size:20px;">{active_threats:,}</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding:10px; border-radius:8px;">
          <div style="color:{COLORS['orange']}; font-size:11px;">CRITICAL SEVERITY</div>
          <div style="color:white; font-weight:700; font-size:20px;">{critical_count:,}</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding:10px; border-radius:8px;">
          <div style="color:{COLORS['purple']}; font-size:11px;">DATA COMPROMISED</div>
          <div style="color:white; font-weight:700; font-size:20px;">{total_data_loss/1024:.1f} TB</div>
        </div>
      </div>
    </div>
    """
    
    return status_html
