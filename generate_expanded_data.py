"""
Data Generator for Cyber Attack Dataset
Generates realistic cybersecurity attack data with proper variation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility (but not for timestamps)
np.random.seed(42)
random.seed(42)

# Major countries with higher weight (USA, China, Russia, UK, EU countries, etc.)
MAJOR_COUNTRIES = {
    'USA': 3.5, 'China': 3.5, 'Russia': 3, 'UK': 2.5, 'Germany': 2.5,
    'France': 2.5, 'India': 2.5, 'Japan': 2, 'South Korea': 2,
    'Brazil': 2, 'Canada': 2, 'Australia': 2, 'Italy': 2,
    'Spain': 2, 'Netherlands': 2, 'Poland': 1.5, 'Sweden': 1.5,
    'Belgium': 1.5, 'Switzerland': 1.5, 'Israel': 1.5, 'Turkey': 1.5
}

# Configuration
NUM_RECORDS = 30000  # Generate 30,000 attack records (5,000 per year for 6 years)
START_DATE = datetime(2019, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Data options
COUNTRIES = [
    'USA', 'UK', 'Germany', 'France', 'China', 'India', 'Brazil', 'Russia', 
    'Australia', 'Canada', 'Japan', 'South Korea', 'Mexico', 'Italy', 'Spain',
    'Netherlands', 'Singapore', 'UAE', 'Saudi Arabia', 'Turkey', 'Poland',
    'Sweden', 'Norway', 'Denmark', 'Finland', 'Belgium', 'Switzerland',
    'Argentina', 'Chile', 'Colombia', 'Peru', 'Indonesia', 'Thailand',
    'Vietnam', 'Philippines', 'Malaysia', 'Pakistan', 'Bangladesh', 'Egypt',
    'Nigeria', 'South Africa', 'Kenya', 'Morocco', 'Israel', 'New Zealand'
]

ATTACK_TYPES = [
    'Malware', 'Ransomware', 'Phishing', 'DDoS', 'SQL Injection',
    'Man-in-the-Middle', 'Zero-Day Exploit', 'Brute Force',
    'Cross-Site Scripting', 'Password Attack', 'DNS Spoofing',
    'Session Hijacking', 'Trojan', 'Spyware', 'Backdoor',
    'APT', 'Cryptojacking', 'IoT Attack', 'Supply Chain Attack',
    'Business Email Compromise', 'Credential Stuffing', 'Rootkit', 'Worm'
]

TARGET_INDUSTRIES = [
    'Finance', 'Healthcare', 'Government', 'Retail', 'Education',
    'Technology', 'Manufacturing', 'Energy', 'Telecommunications',
    'Transportation', 'Media', 'Legal', 'Insurance', 'Real Estate',
    'Hospitality', 'Agriculture', 'Defense', 'Aerospace'
]

TARGET_SYSTEMS = [
    'Web Server', 'Database', 'Email Server', 'File Server',
    'Application Server', 'Cloud Storage', 'Network Router',
    'Firewall', 'VPN Gateway', 'DNS Server', 'Active Directory',
    'IoT Device', 'Mobile App', 'Desktop Application', 'API Gateway'
]

ATTACK_SOURCES = [
    'Hacker Group', 'Nation State', 'Insider Threat', 'Cybercriminal',
    'Hacktivist', 'Bot Network', 'Script Kiddie', 'APT Group',
    'Organized Crime', 'Competitor', 'Disgruntled Employee'
]

SECURITY_VULNERABILITIES = [
    'Unpatched Software', 'Weak Password', 'Misconfiguration',
    'Social Engineering', 'Zero-Day', 'SQL Injection', 'XSS',
    'Default Credentials', 'Missing Encryption', 'Open Port',
    'Outdated Protocol', 'Poor Access Control', 'No MFA',
    'Unsecured API', 'Legacy System'
]

DEFENSE_MECHANISMS = [
    'Firewall', 'IDS/IPS', 'Antivirus', 'WAF', 'DLP', 'SIEM',
    'Endpoint Protection', 'Network Segmentation', 'MFA',
    'Encryption', 'Patch Management', 'Access Control',
    'Security Monitoring', 'Threat Intelligence', 'VPN'
]

ACTION_TAKEN = [
    'Blocked', 'Quarantined', 'Logged', 'Alerted', 'Isolated',
    'Patched', 'Investigated', 'Remediated', 'Escalated',
    'Monitored', 'Contained', 'Restored'
]

def generate_timestamp():
    """Generate random timestamp between start and end dates with better distribution"""
    # Don't use fixed seed for timestamps to get better distribution across years
    delta = END_DATE - START_DATE
    total_seconds = delta.days * 86400
    random_offset = random.randint(0, total_seconds)
    return START_DATE + timedelta(seconds=random_offset)

def generate_attack_record():
    """Generate a single attack record with realistic correlations"""
    
    # Basic info with weighted country selection
    # Favor major countries (USA, China, Russia, UK, EU, etc.)
    if random.random() < 0.7:  # 70% chance of major country
        country_weights = [MAJOR_COUNTRIES.get(c, 0.5) for c in COUNTRIES]
        country = random.choices(COUNTRIES, weights=country_weights, k=1)[0]
    else:
        country = random.choice(COUNTRIES)
    
    year = random.randint(2019, 2024)
    attack_type = random.choice(ATTACK_TYPES)
    target_industry = random.choice(TARGET_INDUSTRIES)
    target_system = random.choice(TARGET_SYSTEMS)
    
    # Attack severity (1-10) - some attack types are more severe
    severity_weights = {
        'Ransomware': (7, 10),
        'Zero-Day Exploit': (8, 10),
        'APT': (8, 10),
        'Supply Chain Attack': (7, 10),
        'Rootkit': (7, 9),
        'SQL Injection': (6, 9),
        'Malware': (5, 9),
        'Worm': (5, 8),
        'Backdoor': (6, 9),
        'DDoS': (4, 8),
        'Trojan': (5, 8),
        'IoT Attack': (4, 7),
        'Cryptojacking': (3, 6),
        'Phishing': (3, 7),
        'Business Email Compromise': (5, 8),
        'Credential Stuffing': (4, 7),
        'Brute Force': (3, 6),
        'Spyware': (4, 7)
    }
    severity_range = severity_weights.get(attack_type, (3, 8))
    attack_severity = random.randint(*severity_range)
    
    # Financial loss - correlated with severity
    base_loss = random.uniform(1000, 50000)
    financial_loss = base_loss * (attack_severity / 5) * random.uniform(0.5, 2.0)
    
    # Number of affected users - correlated with target industry
    industry_user_multiplier = {
        'Finance': 10,
        'Healthcare': 8,
        'Government': 15,
        'Retail': 20,
        'Education': 12,
        'Technology': 5
    }
    multiplier = industry_user_multiplier.get(target_industry, 7)
    affected_users = int(random.randint(10, 500) * multiplier * random.uniform(0.5, 1.5))
    
    # Attack source
    attack_source = random.choice(ATTACK_SOURCES)
    
    # Security vulnerability
    vulnerability = random.choice(SECURITY_VULNERABILITIES)
    
    # Defense mechanism
    defense = random.choice(DEFENSE_MECHANISMS)
    
    # Action taken
    action = random.choice(ACTION_TAKEN)
    
    # Incident resolution time (hours) - inversely correlated with severity
    # Higher severity = faster response
    base_resolution = random.uniform(2, 72)
    if attack_severity >= 8:
        resolution_time = base_resolution * random.uniform(0.3, 0.7)  # Fast response
    elif attack_severity >= 5:
        resolution_time = base_resolution * random.uniform(0.6, 1.2)  # Medium response
    else:
        resolution_time = base_resolution * random.uniform(1.0, 1.8)  # Slower response
    
    # Data compromised (GB) - correlated with severity and attack type
    if attack_type in ['Ransomware', 'SQL Injection', 'Supply Chain Attack', 'APT']:
        data_loss = random.uniform(1, 100) * (attack_severity / 3)  # High data loss
    elif attack_type in ['Business Email Compromise', 'Credential Stuffing']:
        data_loss = random.uniform(0.5, 20) * (attack_severity / 4)  # Medium data loss
    elif attack_type in ['DDoS', 'Brute Force', 'Cryptojacking']:
        data_loss = random.uniform(0.1, 5)  # Minimal data loss
    elif attack_type in ['Backdoor', 'Rootkit', 'Trojan', 'Spyware']:
        data_loss = random.uniform(5, 80) * (attack_severity / 4)  # Variable data loss
    else:
        data_loss = random.uniform(0.5, 50) * (attack_severity / 5)  # Standard data loss
    
    # Attack duration (minutes) - some attacks are longer
    if attack_type in ['DDoS', 'Ransomware', 'Worm']:
        attack_duration = random.uniform(30, 180)  # Long duration attacks
    elif attack_type in ['APT', 'Supply Chain Attack', 'Rootkit']:
        attack_duration = random.uniform(60, 240)  # Very long, sophisticated attacks
    elif attack_type in ['Cryptojacking', 'IoT Attack']:
        attack_duration = random.uniform(120, 300)  # Persistent attacks
    elif attack_type in ['Phishing', 'Business Email Compromise']:
        attack_duration = random.uniform(5, 30)  # Quick social engineering
    else:
        attack_duration = random.uniform(10, 90)  # Standard attacks
    
    # Generate outcome based on action taken
    if action in ['Blocked', 'Quarantined', 'Contained']:
        outcome = 'Mitigated'
    elif action in ['Logged', 'Monitored']:
        outcome = 'Detected'
    else:
        outcome = 'Resolved'
    
    timestamp = generate_timestamp()
    
    return {
        'timestamp': timestamp,
        'year': timestamp.year,  # Explicit year column for easier filtering
        'location': country,
        'attack_type': attack_type,
        'target_industry': target_industry,
        'target_system': target_system,
        'attack_severity': attack_severity,
        'attack_duration_min': round(attack_duration, 2),
        'data_compromised_GB': round(data_loss, 2),
        'financial_impact_USD': round(financial_loss, 2),
        'response_time_min': round(resolution_time * 60, 2),  # Convert hours to minutes
        'mitigation_method': defense,
        'outcome': outcome,
        'attack_vector': vulnerability,
        'attacker_origin': 'External' if 'Insider' not in attack_source else 'Internal',
        'affected_users': affected_users
    }

def generate_dataset(num_records):
    """Generate complete dataset"""
    print(f"Generating {num_records} attack records...")
    
    records = []
    for i in range(num_records):
        if (i + 1) % 1000 == 0:
            print(f"Generated {i + 1} records...")
        records.append(generate_attack_record())
    
    df = pd.DataFrame(records)
    
    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    print(f"\nDataset generated successfully!")
    print(f"Total records: {len(df)}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"Countries: {df['location'].nunique()}")
    print(f"Attack types: {df['attack_type'].nunique()}")
    
    return df

def main():
    """Main function"""
    print("=" * 60)
    print("Cyber Attack Data Generator")
    print("=" * 60)
    
    # Generate dataset
    df = generate_dataset(NUM_RECORDS)
    
    # Save to CSV
    output_file = 'expanded_cyber_attacks.csv'
    df.to_csv(output_file, index=False)
    print(f"\nDataset saved to: {output_file}")
    
    # Display sample
    print("\n" + "=" * 60)
    print("Sample records:")
    print("=" * 60)
    print(df.head(10))
    
    # Statistics
    print("\n" + "=" * 60)
    print("Dataset Statistics:")
    print("=" * 60)
    print(f"Total Attacks: {len(df)}")
    print(f"Average Severity: {df['attack_severity'].mean():.2f}")
    print(f"Total Financial Loss: ${df['financial_impact_USD'].sum():,.2f}")
    print(f"Average Data Loss: {df['data_compromised_GB'].mean():.2f} GB")
    print(f"\nYear Distribution: {df['year'].value_counts().sort_index().to_dict()}")
    print(f"\nTop 10 Countries: {df['location'].value_counts().head(10).to_dict()}")
    print(f"\nTop 5 Attack Types: {df['attack_type'].value_counts().head().to_dict()}")
    print(f"\nTop 5 Industries: {df['target_industry'].value_counts().head().to_dict()}")
    
    print("\n" + "=" * 60)
    print("✅ Data generation complete!")
    print("=" * 60)
    print(f"\nTo use this data:")
    print(f"1. Replace your existing CSV file with '{output_file}'")
    print(f"2. Or rename '{output_file}' to match your dataset name")
    print(f"3. Restart your Streamlit app")

if __name__ == "__main__":
    main()
