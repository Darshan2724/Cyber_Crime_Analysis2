"""
Data adapter to load available CSV datasets and map them to the canonical
schema expected by the original Streamlit UI (`app.py`).

This module is intentionally conservative: it will not change UI code, but
will provide a dataframe with the columns the app expects (creating safe
placeholders where necessary). It logs informational messages via Streamlit
when used from the app.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st


CANONICAL_COLUMNS = [
    'Timestamp', 'Device Information', 'Attack Type', 'Anomaly Scores',
    'Packet Length', 'Source Port', 'Destination Port', 'Source IP Address',
    'Destination IP Address', 'Protocol', 'Action Taken', 'IDS/IPS Alerts',
    'Malware Indicators', 'Firewall Logs', 'Proxy Information', 'Attack Signature',
    'Severity Level'
]


def find_dataset(root: Path):
    """Return path to the first existing known dataset or None."""
    candidates = [
        root / 'Global_Cybersecurity_Threats_2015-2024_LARGE.csv',  # Try the large dataset first
        root / 'Global_Cybersecurity_Threats_2015-2024.csv',        # Then the regular dataset
        root / 'cybersecurity_large_synthesized_data.csv',          # Legacy filenames as fallback
        root / 'cybersecurity_attacks.csv'
    ]
    for p in candidates:
        if p.exists():
            return p
    # try any csv in folder as last resort
    for p in root.glob('*.csv'):
        return p
    return None


def map_global_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Map the 'Global_Cybersecurity_Threats' style schema to the canonical
    schema used by app.py and app_v2.py. This will create safe placeholders 
    for missing fields and synthesize additional fields needed for v2 visualizations.
    """
    mapped = df.copy()

    # Create or map Timestamp: use Year if present otherwise use now
    if 'Timestamp' not in mapped.columns:
        if 'Year' in mapped.columns:
            # set to Jan 1 of the Year to create a datetime column
            mapped['Timestamp'] = pd.to_datetime(mapped['Year'].astype(str) + '-01-01')
        else:
            mapped['Timestamp'] = pd.Timestamp.now()

    # Device Information with enhanced detail
    if 'Device Information' not in mapped.columns:
        # Create synthetic device types
        device_types = ['Network Sensor', 'Firewall', 'IDS', 'Server', 'Workstation', 'IoT Device']
        mapped['Device Information'] = pd.Series(np.random.choice(device_types, size=len(mapped)))

    # Attack Type with enriched categorization
    if 'Attack Type' in mapped.columns:
        mapped['Attack Type'] = mapped['Attack Type']
    elif 'attack_type' in mapped.columns:
        mapped['Attack Type'] = mapped['attack_type']
    else:
        attack_types = ['DDoS', 'SQL Injection', 'XSS', 'Malware', 'Phishing', 'Zero-day Exploit']
        mapped['Attack Type'] = pd.Series(np.random.choice(attack_types, size=len(mapped)))

    # Advanced metrics for ML/Analytics
    if 'Anomaly Scores' not in mapped.columns:
        # Generate realistic anomaly scores between 0-1
        mapped['Anomaly Scores'] = np.random.beta(2, 5, size=len(mapped))
    
    # Network metrics
    if 'Packet Length' not in mapped.columns:
        mapped['Packet Length'] = np.random.randint(64, 1500, size=len(mapped))
    if 'Source Port' not in mapped.columns:
        mapped['Source Port'] = np.random.randint(1024, 65535, size=len(mapped))
    if 'Destination Port' not in mapped.columns:
        common_ports = [80, 443, 22, 21, 25, 53] + list(range(1024, 65535))
        mapped['Destination Port'] = pd.Series(np.random.choice(common_ports, size=len(mapped)))

    # Enhanced IP address generation
    if 'Source IP Address' not in mapped.columns:
        # Generate realistic private and public IPs
        def generate_ip():
            if np.random.random() < 0.3:  # 30% private IPs
                return f"192.168.{np.random.randint(0, 255)}.{np.random.randint(1, 255)}"
            return f"{np.random.randint(1, 223)}.{np.random.randint(0, 255)}.{np.random.randint(0, 255)}.{np.random.randint(1, 255)}"
        mapped['Source IP Address'] = [generate_ip() for _ in range(len(mapped))]
    
    if 'Destination IP Address' not in mapped.columns:
        mapped['Destination IP Address'] = [generate_ip() for _ in range(len(mapped))]

    # Protocol with common values
    if 'Protocol' not in mapped.columns:
        protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'DNS', 'SMTP']
        mapped['Protocol'] = pd.Series(np.random.choice(protocols, size=len(mapped)))

    # Enhanced action mapping
    if 'Action Taken' not in mapped.columns:
        if 'outcome' in mapped.columns:
            mapped['Action Taken'] = mapped['outcome']
        else:
            actions = ['Blocked', 'Allowed', 'Quarantined', 'Logged', 'Alerted', 'Escalated']
            mapped['Action Taken'] = pd.Series(np.random.choice(actions, size=len(mapped)))

    # Security system outputs
    if 'IDS/IPS Alerts' not in mapped.columns:
        alert_types = ['Signature Match', 'Anomaly Detected', 'Policy Violation', 'No Alert', 'False Positive']
        mapped['IDS/IPS Alerts'] = pd.Series(np.random.choice(alert_types, size=len(mapped)))
    
    if 'Malware Indicators' not in mapped.columns:
        indicators = ['None Detected', 'Suspicious Binary', 'Known Malware', 'Potential Backdoor', 'Ransomware Pattern']
        mapped['Malware Indicators'] = pd.Series(np.random.choice(indicators, size=len(mapped)))
    
    if 'Firewall Logs' not in mapped.columns:
        log_types = ['Connection Blocked', 'Traffic Allowed', 'Rate Limited', 'NAT Translation', 'VPN Access']
        mapped['Firewall Logs'] = pd.Series(np.random.choice(log_types, size=len(mapped)))
    
    if 'Proxy Information' not in mapped.columns:
        proxy_info = ['Direct Connection', 'Via Corporate Proxy', 'VPN Endpoint', 'TOR Exit Node', 'Unknown Proxy']
        mapped['Proxy Information'] = pd.Series(np.random.choice(proxy_info, size=len(mapped)))

    # Enriched attack signatures and severity
    if 'Attack Signature' not in mapped.columns:
        mapped['Attack Signature'] = mapped['Attack Type'].apply(
            lambda x: f"{x}_{np.random.randint(1000, 9999)}"
        )
    
    if 'Severity Level' not in mapped.columns:
        if 'attack_severity' in mapped.columns:
            mapped['Severity Level'] = mapped['attack_severity'].apply(
                lambda x: 'Critical' if x >= 8 else ('High' if x >= 6 else ('Medium' if x >= 4 else 'Low'))
            )
        elif 'Financial Loss (in Million $)' in mapped.columns:
            mapped['Severity Level'] = mapped['Financial Loss (in Million $)'].apply(
                lambda x: 'Critical' if x > 100 else ('High' if x > 50 else ('Medium' if x > 10 else 'Low'))
            )
        else:
            severity_levels = ['Low', 'Medium', 'High', 'Critical']
            weights = [0.4, 0.3, 0.2, 0.1]  # Weighted distribution
            mapped['Severity Level'] = pd.Series(np.random.choice(severity_levels, size=len(mapped), p=weights))

    # V2-specific enrichments for advanced visualizations
    # Geographic data for globe visualization
    if 'Country' in mapped.columns and 'Latitude' not in mapped.columns:
        # Use a basic mapping of countries to approximate coordinates
        country_coords = {
            'USA': (37.0902, -95.7129),
            'China': (35.8617, 104.1954),
            'Russia': (61.5240, 105.3188),
            'UK': (55.3781, -3.4360),
            'India': (20.5937, 78.9629),
            # Add more as needed
        }
        coord_df = pd.DataFrame.from_dict(country_coords, orient='index', columns=['lat', 'lon'])
        merged = mapped.merge(coord_df, left_on='Country', right_index=True, how='left')
        mapped['Latitude'] = merged['lat'].fillna(0)
        mapped['Longitude'] = merged['lon'].fillna(0)

    # Ensure Timestamp is datetime for time-based visualizations
    mapped['Timestamp'] = pd.to_datetime(mapped['Timestamp'], errors='coerce').fillna(pd.Timestamp.now())

    # Keep canonical columns plus any original columns
    # But for safety, ensure canonical columns exist
    for c in CANONICAL_COLUMNS:
        if c not in mapped.columns:
            mapped[c] = pd.Series([None] * len(mapped), index=mapped.index)

    # Helper to convert a value or Series to a Series aligned with mapped
    def _as_series(val, default=None):
        if isinstance(val, pd.Series):
            return val.reindex(mapped.index)
        if val is None:
            val = default
        return pd.Series([val] * len(mapped), index=mapped.index)

    # Standardize column names for app_v2 expectations (lowercase keys)
    # Map common source names to v2 expected names
    standardized = pd.DataFrame(index=mapped.index)

    # Timestamp
    if 'Timestamp' in mapped.columns:
        standardized['timestamp'] = pd.to_datetime(mapped['Timestamp'], errors='coerce').fillna(pd.Timestamp.now())
    elif 'timestamp' in mapped.columns:
        standardized['timestamp'] = pd.to_datetime(mapped['timestamp'], errors='coerce').fillna(pd.Timestamp.now())
    elif 'Year' in mapped.columns:
        standardized['timestamp'] = pd.to_datetime(mapped['Year'].astype(str) + '-01-01')
    else:
        standardized['timestamp'] = _as_series(pd.Timestamp.now())

    # Attack type
    if 'Attack Type' in mapped.columns:
        standardized['attack_type'] = _as_series(mapped['Attack Type'])
    elif 'attack_type' in mapped.columns:
        standardized['attack_type'] = _as_series(mapped['attack_type'])
    else:
        standardized['attack_type'] = _as_series(mapped.get('Attack Signature', 'Unknown'))

    # Target system / device (prefer device info, fall back to Target or Target Industry)
    standardized['target_system'] = _as_series(
        mapped.get('Device Information', mapped.get('Target', mapped.get('Target Industry', 'Unknown System')))
    )

    # Location / country
    if 'location' in mapped.columns:
        standardized['location'] = _as_series(mapped['location'])
    elif 'Country' in mapped.columns:
        standardized['location'] = _as_series(mapped['Country'])
    else:
        standardized['location'] = _as_series('Unknown')

    # Industry (map Target Industry if present)
    standardized['industry'] = _as_series(mapped.get('Industry', mapped.get('industry', mapped.get('Target Industry', 'Various'))))

    # Severity numeric
    if 'attack_severity' in mapped.columns:
        standardized['attack_severity'] = pd.to_numeric(mapped['attack_severity'], errors='coerce').fillna(5)
    elif 'Severity Level' in mapped.columns:
        # Map categorical severity to numeric
        lvl = mapped['Severity Level'].astype(str).str.lower()
        def sev_to_num(x):
            if 'critical' in x:
                return 9
            if 'high' in x:
                return 7
            if 'medium' in x:
                return 5
            if 'low' in x:
                return 2
            return 5
        standardized['attack_severity'] = lvl.apply(sev_to_num).reindex(mapped.index)
    elif 'Financial Loss (in Million $)' in mapped.columns:
        loss = pd.to_numeric(mapped['Financial Loss (in Million $)'], errors='coerce').fillna(0)
        def loss_to_sev(x):
            if x > 100:
                return 9
            if x > 50:
                return 7
            if x > 10:
                return 5
            return 3
        standardized['attack_severity'] = loss.apply(loss_to_sev).reindex(mapped.index)
    elif 'Number of Affected Users' in mapped.columns:
        users = pd.to_numeric(mapped['Number of Affected Users'], errors='coerce').fillna(0)
        standardized['attack_severity'] = users.apply(lambda x: 7 if x > 100000 else (5 if x > 10000 else 3)).reindex(mapped.index)
    else:
        standardized['attack_severity'] = _as_series(5)

    # Data compromised in GB
    if 'data_compromised_GB' in mapped.columns:
        standardized['data_compromised_GB'] = pd.to_numeric(mapped['data_compromised_GB'], errors='coerce').fillna(0)
    elif 'Financial Loss (in Million $)' in mapped.columns:
        # heuristic: convert financial loss (millions $) to GB for visuals to have numeric values
        loss = pd.to_numeric(mapped['Financial Loss (in Million $)'], errors='coerce').fillna(0)
        standardized['data_compromised_GB'] = (loss * 0.5).reindex(mapped.index)
    elif 'Number of Affected Users' in mapped.columns:
        users = pd.to_numeric(mapped['Number of Affected Users'], errors='coerce').fillna(0)
        standardized['data_compromised_GB'] = (users * 0.001).reindex(mapped.index)
    else:
        standardized['data_compromised_GB'] = _as_series(0)

    # Outcome - prefer Action Taken, otherwise derive from Incident Resolution Time if available
    if 'Action Taken' in mapped.columns:
        standardized['outcome'] = _as_series(mapped['Action Taken'])
    elif 'outcome' in mapped.columns:
        standardized['outcome'] = _as_series(mapped['outcome'])
    elif 'Incident Resolution Time (in Hours)' in mapped.columns:
        hrs = pd.to_numeric(mapped['Incident Resolution Time (in Hours)'], errors='coerce').fillna(0)
        standardized['outcome'] = hrs.apply(lambda x: 'Resolved' if x > 0 else 'Unknown').reindex(mapped.index)
    else:
        standardized['outcome'] = _as_series('Unknown')

    # Attacker/Target IPs
    standardized['attacker_ip'] = _as_series(mapped.get('Source IP Address', mapped.get('attacker_ip', '0.0.0.0')))
    standardized['target_ip'] = _as_series(mapped.get('Destination IP Address', mapped.get('target_ip', '0.0.0.0')))

    # Mitigation and durations - prefer Defense Mechanism Used
    standardized['mitigation_method'] = _as_series(mapped.get('Defense Mechanism Used', mapped.get('Defense Mechanism', mapped.get('mitigation_method', mapped.get('Attack Signature', 'Standard Protocol')))))
    standardized['attack_duration_min'] = pd.to_numeric(_as_series(mapped.get('attack_duration_min', mapped.get('Duration (min)', 30))), errors='coerce').fillna(30)
    standardized['response_time_min'] = pd.to_numeric(_as_series(mapped.get('response_time_min', mapped.get('Response Time (min)', 15))), errors='coerce').fillna(15)

    # Security tools and user roles
    standardized['security_tools_used'] = _as_series(mapped.get('Defense Mechanism Used', mapped.get('security_tools_used', 'Basic Security Suite')))
    standardized['user_role'] = _as_series(mapped.get('user_role', 'User'))

    # Ensure types
    standardized['attack_type'] = standardized['attack_type'].astype(str)
    standardized['target_system'] = standardized['target_system'].astype(str)
    standardized['location'] = standardized['location'].astype(str)

    return standardized


def load_best_dataset(root_dir: str = '.') -> pd.DataFrame:
    """Find and load the best dataset available under root_dir and return a
    dataframe compatible with `app.py`.

    The function will display a small Streamlit info box describing which
    dataset was loaded and what column mappings were applied.
    """
    root = Path(root_dir)
    ds = find_dataset(root)
    if ds is None:
        st.error('No CSV dataset found in project directory.')
        st.stop()

    st.info(f"Loading dataset: {ds.name}")
    df = pd.read_csv(ds)

    # Heuristics: if this looks like the global dataset, map accordingly
    if 'Country' in df.columns and 'Financial Loss (in Million $)' in df.columns:
        mapped = map_global_schema(df)
        st.info('Applied mapping from Global_Cybersecurity_Threats schema to canonical schema.')
        return mapped

    # If it already contains some canonical columns, try to make minimal adjustments
    if 'Timestamp' in df.columns and 'Attack Type' in df.columns:
        # ensure Timestamp is datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce').fillna(pd.Timestamp.now())
        st.info('Loaded dataset with Timestamp and Attack Type; minimal mapping applied.')
        return df

    # Fallback: map minimally using global mapper
    st.info('Unknown CSV schema detected — applying best-effort mapping.')
    return map_global_schema(df)
