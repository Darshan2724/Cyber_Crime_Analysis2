"""
Enhanced Data Loader Module for DarkSentinel V2
Handles loading and validation of the new cybersecurity attack data
"""

import pandas as pd
import streamlit as st
from datetime import datetime

@st.cache_data(ttl=3600)
def load_data(file_path='cybersecurity_large_synthesized_data.csv'):
    """
    Load cybersecurity attack data from CSV file
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
        
    Returns:
    --------
    pd.DataFrame
        Loaded and validated dataframe
    """
    try:
        # Always try to use the data adapter first to get the best available dataset
        import sys
        from pathlib import Path
        
        # Add the parent directory to Python path to enable imports
        root_dir = Path(__file__).parent.parent
        if str(root_dir) not in sys.path:
            sys.path.append(str(root_dir))
            
        try:
            from modules.data_adapter import load_best_dataset
            # Silently use data adapter to locate the best available dataset
            df = load_best_dataset(root_dir=str(root_dir))
        except Exception as e:
            st.error(f"Data adapter error: {str(e)}")
            # Fallback: try to load the file directly
            requested = Path(file_path)
            if requested.exists():
                df = pd.read_csv(requested)
            else:
                # Last resort: try to find any suitable CSV
                csv_files = list(root_dir.glob("*.csv"))
                if csv_files:
                    df = pd.read_csv(csv_files[0])
                    st.info(f"Using found dataset: {csv_files[0].name}")
                else:
                    raise FileNotFoundError(f"No suitable dataset found in {root_dir}")
        
        # Handle different possible timestamp column names and create a clean datetime 'timestamp' column
        timestamp_candidates = ['timestamp', 'Timestamp', 'Year']
        timestamp_col = None
        
        for col in timestamp_candidates:
            if col in df.columns:
                timestamp_col = col
                break
        
        if timestamp_col is None:
            st.warning("No timestamp column found. Creating one with current time.")
            df['timestamp'] = pd.Timestamp.now()
        elif timestamp_col == 'Year':
            # Convert Year to a proper timestamp (Jan 1st of that year)
            df['timestamp'] = pd.to_datetime(df['Year'].astype(str) + '-01-01', errors='coerce')
        else:
            # Parse the found timestamp column into datetime
            df['timestamp'] = pd.to_datetime(df[timestamp_col], errors='coerce')
        
        # Drop rows where timestamp could not be parsed to avoid defaulting everything to 'now'
        if df['timestamp'].isna().any():
            df = df.dropna(subset=['timestamp']).reset_index(drop=True)
        
        # Add computed columns based on timestamp
        df['date'] = df['timestamp'].dt.date
        df['year'] = df['timestamp'].dt.year
        df['month'] = df['timestamp'].dt.month
        df['month_name'] = df['timestamp'].dt.month_name()
        df['day'] = df['timestamp'].dt.day
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_name'] = df['timestamp'].dt.day_name()
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute
        
        # Ensure required columns exist with default values
        required_columns = {
            'attack_type': 'Unknown',
            'target_system': 'Generic System',
            'location': 'Unknown Location',
            'industry': 'Various',
            'attack_severity': 5,  # Medium severity default
            'data_compromised_GB': 0,
            'outcome': 'Unknown',
            'attacker_ip': '0.0.0.0',
            'target_ip': '0.0.0.0',
            'user_role': 'User',
            'security_tools_used': 'Basic Security Suite',
            'mitigation_method': 'Standard Protocol',
            'attack_duration_min': 30,  # Default 30 minutes
            'response_time_min': 15,    # Default 15 minutes
        }
        
        for col, default_value in required_columns.items():
            if col not in df.columns:
                df[col] = default_value

        # If dataset provides 'target_industry', map it into the expected 'industry' column
        if 'target_industry' in df.columns:
            df['industry'] = df['industry'].where(df['industry'].ne('Various'), df['target_industry'])
        
        # Add success rate
        df['is_successful'] = (df['outcome'] == 'Success').astype(int)
        
        # Add severity category
        df['severity_category'] = pd.cut(
            df['attack_severity'],
            bins=[0, 3, 6, 10],
            labels=['Low', 'Medium', 'High']
        )
        
        # Add data loss category
        df['data_loss_category'] = pd.cut(
            df['data_compromised_GB'],
            bins=[-0.01, 25, 50, 75, 100],
            labels=['Minimal', 'Moderate', 'Significant', 'Critical']
        )
        
        # Add response efficiency (lower is better)
        df['response_efficiency'] = df['response_time_min'] / df['attack_duration_min']
        
        return df
        
    except FileNotFoundError:
        st.error(f"❌ Data file not found: {file_path}")
        st.info("Please ensure a dataset CSV is in the project directory. The app will also try other CSVs via the data adapter.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

def get_data_summary(df):
    """
    Get comprehensive summary statistics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    dict
        Summary statistics
    """
    summary = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'date_range_start': df['timestamp'].min(),
        'date_range_end': df['timestamp'].max(),
        'total_days': (df['timestamp'].max() - df['timestamp'].min()).days,
        'unique_attackers': df['attacker_ip'].nunique(),
        'unique_targets': df['target_ip'].nunique(),
        'total_data_compromised_TB': df['data_compromised_GB'].sum() / 1024,
        'avg_attack_duration_hours': df['attack_duration_min'].mean() / 60,
        'avg_response_time_hours': df['response_time_min'].mean() / 60,
        'success_rate': (df['outcome'] == 'Success').mean() * 100,
        'avg_severity': df['attack_severity'].mean(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024**2)
    }
    return summary

def get_attack_statistics(df):
    """
    Get detailed attack statistics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    dict
        Attack statistics
    """
    stats = {
        'by_type': df['attack_type'].value_counts().to_dict(),
        'by_target': df['target_system'].value_counts().to_dict(),
        'by_location': df['location'].value_counts().to_dict(),
        'by_industry': df['industry'].value_counts().to_dict(),
        'by_outcome': df['outcome'].value_counts().to_dict(),
        'by_severity': df['severity_category'].value_counts().to_dict(),
        'by_user_role': df['user_role'].value_counts().to_dict(),
        'by_security_tool': df['security_tools_used'].value_counts().to_dict(),
        'by_mitigation': df['mitigation_method'].value_counts().to_dict(),
    }
    return stats

def get_real_time_metrics(df, last_n_hours=24):
    """
    Get real-time metrics for the last N hours
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    last_n_hours : int
        Number of hours to look back
        
    Returns:
    --------
    dict
        Real-time metrics
    """
    cutoff_time = df['timestamp'].max() - pd.Timedelta(hours=last_n_hours)
    recent_df = df[df['timestamp'] >= cutoff_time]
    
    metrics = {
        'recent_attacks': len(recent_df),
        'recent_successful': (recent_df['outcome'] == 'Success').sum(),
        'recent_critical': (recent_df['attack_severity'] >= 8).sum(),
        'recent_data_loss_gb': recent_df['data_compromised_GB'].sum(),
        'most_targeted_system': recent_df['target_system'].mode()[0] if len(recent_df) > 0 else 'N/A',
        'most_common_attack': recent_df['attack_type'].mode()[0] if len(recent_df) > 0 else 'N/A',
        'hotspot_location': recent_df['location'].mode()[0] if len(recent_df) > 0 else 'N/A',
    }
    return metrics

def filter_data(df, filters):
    """
    Apply multiple filters to dataframe
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    filters : dict
        Filter criteria
        
    Returns:
    --------
    pd.DataFrame
        Filtered dataframe
    """
    filtered = df.copy()
    
    if filters.get('date_range') and len(filters['date_range']) == 2:
        start_date, end_date = filters['date_range']
        # Convert to datetime for proper comparison
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)  # Include full end day
        filtered = filtered[
            (filtered['timestamp'] >= start_dt) &
            (filtered['timestamp'] <= end_dt)
        ]
    
    if filters.get('attack_types'):
        filtered = filtered[filtered['attack_type'].isin(filters['attack_types'])]
    
    if filters.get('target_systems'):
        filtered = filtered[filtered['target_system'].isin(filters['target_systems'])]
    
    if filters.get('locations'):
        filtered = filtered[filtered['location'].isin(filters['locations'])]
    
    if filters.get('industries'):
        filtered = filtered[filtered['industry'].isin(filters['industries'])]
    
    if filters.get('outcomes'):
        filtered = filtered[filtered['outcome'].isin(filters['outcomes'])]
    
    if filters.get('severity_range'):
        min_sev, max_sev = filters['severity_range']
        # Convert severity to numeric for comparison
        severity_numeric = pd.to_numeric(filtered['attack_severity'], errors='coerce').fillna(5)
        filtered = filtered[
            (severity_numeric >= min_sev) &
            (severity_numeric <= max_sev)
        ]
    
    if filters.get('user_roles'):
        filtered = filtered[filtered['user_role'].isin(filters['user_roles'])]
    
    if filters.get('security_tools'):
        filtered = filtered[filtered['security_tools_used'].isin(filters['security_tools'])]
    
    return filtered

def get_top_threats(df, n=10):
    """
    Get top N threats by various criteria
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    n : int
        Number of top items to return
        
    Returns:
    --------
    dict
        Top threats
    """
    return {
        'top_attackers': df.groupby('attacker_ip').size().nlargest(n).to_dict(),
        'top_targets': df.groupby('target_ip').size().nlargest(n).to_dict(),
        'most_data_loss': df.nlargest(n, 'data_compromised_GB')[
            ['timestamp', 'attack_type', 'target_system', 'data_compromised_GB', 'location']
        ].to_dict('records'),
        'longest_attacks': df.nlargest(n, 'attack_duration_min')[
            ['timestamp', 'attack_type', 'attack_duration_min', 'outcome']
        ].to_dict('records'),
        'slowest_response': df.nlargest(n, 'response_time_min')[
            ['timestamp', 'attack_type', 'response_time_min', 'mitigation_method']
        ].to_dict('records'),
    }
