# 🛡️ DarkSentinel - Global Cyber Threat Intelligence Dashboard

> **A comprehensive cybersecurity threat analysis platform** that transforms global cyber attack data into actionable intelligence with advanced visualizations and real-time analytics.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) 
![Python](https://img.shields.io/badge/Python-3.8%2B-blue) 
![License](https://img.shields.io/badge/License-MIT-orange)

## 🌟 Key Features

### 📊 Interactive Visualizations
- **3D Globe View**: Geographic distribution of cyber attacks with interactive rotation and zoom
- **Temporal Analysis**: 10-year trends (2015-2024) with dynamic filtering
- **Attack Flow**: Interactive Sankey diagrams showing attack source → type → industry
- **Defense Effectiveness**: Compare security mechanisms with radar and bar charts

### 📈 Advanced Analytics
- **50,000+ Records**: Comprehensive dataset of major cyber incidents
- **Multi-dimensional Filters**: Drill down by time period, country, attack type, and industry
- **Correlation Analysis**: 3D visualization of financial impact, affected users, and resolution time
- **Real-time Updates**: Dashboard responds instantly to filter changes

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Sleek, professional interface with cyber aesthetics
- **Responsive Layout**: Works on desktop and tablet
- **Dark/Light Mode**: Easy on the eyes during extended analysis
- **Interactive Elements**: Hover tooltips, zoomable charts, and export capabilities

## 📋 Dataset Overview

- **Records**: 50,000+ cyber incidents (2015-2024)
- **Coverage**: 10 countries, 7 industries, 6 attack types
- **Financial Impact**: $858.9 billion total losses analyzed
- **Affected Users**: 17.8 billion user accounts impacted

### Data Points Tracked
- **Attack Details**: Type, source, target industry, financial loss
- **Impact Metrics**: Number of affected users, resolution time
- **Defense Analysis**: Security mechanisms and their effectiveness
- **Geographic Data**: Country-level attack distribution
8. **Anomalies & Reports** - ML-based anomaly detection with exportable reports

### 🎨 Visual Theme

- **Theme**: Cyber Dark Neon
- **Primary Color**: `#00e5ff` (Neon Cyan)
- **Secondary Color**: `#ff2f92` (Magenta)
- **Success Color**: `#7CFF00` (Neon Green)
- **Background**: `#0b0f14` (Dark)

### 🔍 Filters

Dynamic sidebar filters for:
- Year
- Month
- Attack Type
- Severity Level
- Device/OS
- Protocol
- Action Taken

## 📁 Project Structure

```
Cyber_Crime_Analysis/
│
├── Global_Cybersecurity_Threats_2015-2024_LARGE.csv  # Main dataset (50,000+ records)
├── Global_Cybersecurity_Threats_2015-2024.csv        # Regular dataset
├── app_v2.py                     # Enhanced Streamlit application (current)
├── app.py                        # Original version
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── modules/                      # Core modules
│   ├── data_adapter.py          # Dataset schema mapping
│   ├── data_loader.py           # Basic data loading
│   ├── preprocess.py            # Data preprocessing
│   └── visuals.py               # Basic visualizations
│
└── modules_v2/                  # Enhanced modules for v2
    ├── advanced_visuals.py      # 3D globe, Sankey, etc.
    ├── data_loader_v2.py        # Enhanced data processing
    ├── glassmorphism_theme.py   # UI theme and styling
    └── live_feed.py             # Real-time updates
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download

```bash
cd "C:\DAV project\Cyber_Crime_Analysis"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`

## 📊 Data Overview

**Dataset**: `Global_Cybersecurity_Threats_2015-2024_LARGE.csv`
- **Records**: 50,000+ cyber attack events
- **Time Range**: 2015-2024
- **Core Fields**:
  - Country and Year
  - Attack Type and Target Industry
  - Financial Loss (in Million $)
  - Number of Affected Users
  - Attack Source
  - Security Vulnerability Type
  - Defense Mechanism Used
  - Incident Resolution Time (in Hours)
- **Derived Analytics**:
  - Attack severity scores
  - Data compromised estimates
  - Geographic coordinates
  - Network identifiers (IPs)
  - Temporal patterns

## 🧠 Data Processing

The preprocessing pipeline (from `Cyber_crime_analysis.ipynb`) includes:

1. **Null Value Handling**
   - `Alerts/Warnings` → 'Alert Triggered' or 'None'
   - `IDS/IPS Alerts` → 'No Data' or 'Alert Data'
   - `Malware Indicators` → 'IoC Detected' or 'No Detection'
   - `Firewall Logs` → 'Log Data' or 'No Data'
   - `Proxy Information` → IP or 'No Proxy Data'

2. **Feature Engineering**
   - Extract `Device/OS` from user agent strings (Windows, Linux, Macintosh, iPad, etc.)
   - Extract `Browser` (Mozilla, Opera)
   - Parse `Timestamp` into Year, Month, Day, Hour, DayOfWeek, etc.
   - Split `Geo-location Data` into City and State

3. **Data Validation**
   - No duplicate records
   - All timestamps converted to datetime
   - Categorical encoding for ML models

## 🤖 Anomaly Detection

DarkSentinel uses **Isolation Forest** algorithm to detect unusual attack patterns:

- **Features Used**: Anomaly Scores, Packet Length, Source Port, Destination Port
- **Contamination**: 10% (configurable)
- **Output**: Anomaly flag, ML anomaly score, top anomalous records
- **Insights**: Most common attack types, devices, protocols in anomalies

## 📈 Key Insights from Analysis

From the Jupyter notebook analysis:

- **2023**: Least attacks overall, but DDoS was most frequent
- **2022**: Malware attacks peaked
- **March**: Highest attack month (3,678 attacks)
- **December**: Lowest attack month (2,675 attacks)
- **Monday**: Most attacks occur on Mondays
- **Windows**: Most targeted OS (44.9%)
- **Mozilla**: Most vulnerable browser (79.9%)

## 🎯 Use Cases

1. **Security Operations Centers (SOC)**: Real-time threat monitoring
2. **Incident Response Teams**: Pattern analysis and anomaly investigation
3. **Cybersecurity Training**: Educational demonstrations
4. **Research & Analysis**: Attack trend studies
5. **Executive Reporting**: High-level security metrics

## 🔧 Customization

### Modify Theme Colors

Edit `app.py` CSS section:

```python
st.markdown("""
<style>
    .main {
        background-color: #0b0f14;  /* Change background */
        color: #d0d7de;             /* Change text color */
    }
    /* ... */
</style>
""", unsafe_allow_html=True)
```

### Add New Visualizations

Add functions to `modules/visuals.py`:

```python
def create_custom_chart(df, title='My Chart'):
    fig = px.bar(df, x='column', y='value', title=title)
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    return fig
```

### Adjust Anomaly Detection

Modify contamination parameter in `app.py`:

```python
model, scaler, features = train_anomaly_detector(
    filtered_df, 
    contamination=0.05  # Change from 0.1 to 0.05 for stricter detection
)
```

## 📦 Deployment Options

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Render / Railway / Heroku

Follow platform-specific deployment guides for Streamlit apps.

## 🛠️ Troubleshooting

### Issue: "Module not found"
```bash
pip install --upgrade -r requirements.txt
```

### Issue: "Data file not found"
Ensure `cybersecurity_attacks.csv` is in the same directory as `app.py`

### Issue: Slow performance
- Reduce data size by filtering years
- Adjust `@st.cache_data` decorators
- Use smaller contamination value for anomaly detection

## 📚 Technologies Used

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning (Isolation Forest)
- **NumPy**: Numerical computing
- **Matplotlib**: Additional plotting

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Real-time data ingestion via API
- [ ] User authentication and role-based access
- [ ] PDF report generation
- [ ] Email alerting for high-severity anomalies
- [ ] Integration with SIEM tools
- [ ] Advanced ML models (LSTM, Autoencoders)

## 📄 License

This project is for educational and demonstration purposes.

## 👨‍💻 Author

Created as part of cybersecurity data analysis project.

## 🙏 Acknowledgments

- Dataset: Synthetic cybersecurity attack data
- Inspiration: Modern SOC dashboards and threat intelligence platforms
- Theme: Inspired by cyberpunk aesthetics

---

**⚡ DarkSentinel - Illuminating the Dark Web of Cyber Threats**

For questions or support, please open an issue in the repository.
