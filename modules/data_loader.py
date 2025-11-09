"""
Data Loader Module for DarkSentinel
Handles loading and initial validation of cybersecurity attack data
"""

import pandas as pd
import streamlit as st
from pathlib import Path

# Prefer the adapter which will detect available CSVs and make a best-effort
# mapping so the UI code (app.py) doesn't need to change. The adapter is
# conservative and creates placeholders for missing columns.
try:
    from .data_adapter import load_best_dataset
except Exception:
    load_best_dataset = None


@st.cache_data
def load_data(file_path: str = 'cybersecurity_attacks.csv'):
    """
    Load cybersecurity attack data from CSV.

    Behavior:
    - If the requested file exists, load and return it.
    - Otherwise, delegate to the data adapter (if available) which will
      search for known CSV files and map their schema to what the app
      expects (safe placeholders are created for missing fields).
    """
    requested = Path(file_path)
    # If explicit file exists, load it directly
    if requested.exists():
        try:
            df = pd.read_csv(requested)
            # Try to ensure Timestamp column is proper datetime if present
            if 'Timestamp' in df.columns:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce').fillna(pd.Timestamp.now())
            return df
        except Exception as e:
            st.error(f"❌ Error loading requested data file {file_path}: {e}")
            st.stop()

    # If requested file not found, try adapter
    if load_best_dataset is not None:
        try:
            df = load_best_dataset(root_dir='.')
            return df
        except Exception as e:
            st.error(f"❌ Adapter failed to load dataset: {e}")
            st.stop()

    # Fallback: show a helpful error
    st.error(f"❌ Data file not found: {file_path}. No alternate dataset detected.")
    st.info("Place a CSV (e.g. 'cybersecurity_attacks.csv' or 'Global_Cybersecurity_Threats_2015-2024.csv') in the project root.")
    st.stop()

def get_data_summary(df):
    """
    Get basic summary statistics of the dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    dict
        Dictionary containing summary statistics
    """
    summary = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'date_range': (df['Timestamp'].min(), df['Timestamp'].max()) if 'Timestamp' in df.columns else None,
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
    }
    return summary
