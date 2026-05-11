# 🌱 AgLane Climate Intelligence Platform

## Overview
AgLane is a production-quality Streamlit application designed for aggregating smallholder farmers and tracking carbon credit generation. It provides a unified platform for farmer registration, plantation data management, carbon estimation, and AI-powered impact reporting.

### Key Features
✅ **Farmer Registry System** - Register farmers with auto-generated unique IDs (AGL-XXXX format)  
✅ **Plantation Data Management** - Link tree counts and plantation data to each farmer  
✅ **Carbon Credit Estimation** - Automatic calculation of annual CO₂ sequestration (1 tree = 22 kg CO₂/year)  
✅ **Real-time Dashboard** - View total farmers, trees, and carbon metrics with interactive charts  
✅ **AI-Powered Reports** - Generate professional ESG-style impact reports using Claude AI  
✅ **Data Export** - Download farmer data and reports in CSV, JSON, or text formats  
✅ **Sample Data** - Load demo data for testing and demonstrations  

---

## 📋 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- An Anthropic API key (for AI-powered report generation)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up API Key

The application uses Claude (Anthropic API) for generating AI reports. You have two options:

#### Option A: Environment Variable (Recommended)
```bash
# On macOS/Linux:
export ANTHROPIC_API_KEY="your-api-key-here"

# On Windows (PowerShell):
$env:ANTHROPIC_API_KEY = "your-api-key-here"

# On Windows (Command Prompt):
set ANTHROPIC_API_KEY=your-api-key-here
```

#### Option B: Create .env File
Create a file named `.env` in the same directory as `app.py`:
```
ANTHROPIC_API_KEY=your-api-key-here
```

**Get your API key:** https://console.anthropic.com/

### Step 3: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 🎯 Quick Start Guide

### 1. Load Sample Data (First Time)
- Open the app
- In the left sidebar under "AgLane Control Panel", click **"📥 Load Sample Data"**
- This adds 4 sample farmers with plantation data
- Navigate to the **Dashboard** to see the metrics

### 2. Register Your First Farmer
- Click on **"👨‍🌾 Register Farmer"** in the sidebar
- Fill in:
  - **Farmer Name** (e.g., "John Mwale")
  - **Location** (e.g., "Lusaka, Zambia")
  - **Farm Size** (hectares, e.g., 2.5)
  - **Registration Date**
- Click **"✅ Register Farmer"**
- Your farmer receives a unique ID (e.g., AGL-0001)

### 3. Add Plantation Data
- Click on **"🌳 Add Plantation"** in the sidebar
- Select the farmer you registered
- Enter the number of trees (e.g., 450)
- Select plantation type (Agroforestry, Reforestation, etc.)
- The app automatically calculates:
  - Annual CO₂ sequestration
  - Estimated carbon credit value
- Click **"✅ Add Plantation Data"**

### 4. View Dashboard
- Click on **"📊 Dashboard"** in the sidebar
- See real-time metrics:
  - Total farmers registered
  - Total trees planted
  - Annual carbon sequestration (metric tons)
  - Estimated carbon credit value
- Download farmer data as CSV

### 5. Generate AI Report
- Click on **"📈 Reports"** in the sidebar
- Review current metrics summary
- Click **"🚀 Generate Impact Report"**
- The AI generates a professional ESG report including:
  - Executive overview
  - Key performance indicators
  - Environmental impact analysis
  - Carbon credit potential
  - Smallholder farmer benefits
  - Recommendations
- **Download** the report as:
  - 📄 Text file (for sharing)
  - 📊 JSON file (full data export)

---

## 🏗️ Application Architecture

### File Structure
```
.
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # API keys (create this file)
└── README.md             # This file
```

### Core Components

#### 1. **Session State Management**
- Maintains farmer registry in memory
- Tracks plantation data
- Stores generated reports

#### 2. **Farmer Registry System**
- Auto-generates unique IDs (AGL-0001, AGL-0002, etc.)
- Stores: Name, Location, Farm Size, Registration Date

#### 3. **Carbon Estimation Logic**
```
1 tree = 22 kg CO₂ per year
Carbon (tons) = (Tree Count × 22) / 1000
```

#### 4. **Dashboard Metrics**
- Total farmers
- Total trees
- Annual carbon sequestration (tons)
- Average trees per farmer
- Estimated carbon credit value ($20/ton market rate)

#### 5. **AI Report Generation**
- Uses Claude API (Anthropic)
- Generates professional ESG reports
- Includes metrics analysis and recommendations

#### 6. **Data Export**
- CSV export of farmer registry
- Text export of reports
- JSON export of full platform data

---

## 📊 Data Models

### Farmer Record
```python
{
    "name": "Moses Kamau",
    "location": "Kiambu, Kenya",
    "farm_size": 2.5,  # hectares
    "registration_date": "2024-01-15"
}
```

### Plantation Record
```python
{
    "tree_count": 450,
    "carbon_tons": 9.9,  # (450 × 22) / 1000
    "plantation_type": "Agroforestry",
    "last_updated": "2024-01-15"
}
```

---

## 🎨 UI/UX Features

### Responsive Design
- Clean, modern interface with green theme (climate-focused)
- Sidebar navigation for easy access
- Metric cards with color-coded indicators
- Professional data tables with sorting

### Visual Elements
- **Success Messages** - Green confirmation messages
- **Error Handling** - Clear error messages with solutions
- **Loading States** - Spinners during AI report generation
- **Metric Cards** - Large, readable KPI displays
- **Data Tables** - Sortable, filterable farmer registry

### Accessibility
- Clear labels for all inputs
- Helpful placeholder text
- Progress indicators
- Informative messages guiding users

---

## 🔧 Configuration & Customization

### Carbon Calculation
Edit the `calculate_carbon_tons()` function:
```python
# Default: 1 tree = 22 kg CO₂/year
return (tree_count * 22) / 1000
```

### Market Rate for Carbon Credits
In the Dashboard, the carbon credit value uses $20/ton:
```python
carbon_value = metrics['total_carbon'] * 20  # Change 20 to your rate
```

### AI Report Prompt
Edit the `generate_impact_report_with_ai()` function to customize the report structure and content.

### Color Scheme
Modify the CSS in `st.markdown()` to change colors:
```css
border-left-color: #2ecc71;  /* Green */
color: #1a472a;              /* Dark green */
```

---

## 📈 Sample Data

The "Load Sample Data" feature includes:
1. **Moses Kamau** - Kiambu, Kenya (2.5 ha, 450 trees)
2. **Grace Okonkwo** - Enugu, Nigeria (1.8 ha, 380 trees)
3. **Sarah Mwale** - Lusaka, Zambia (3.2 ha, 620 trees)
4. **James Kikwete** - Dar es Salaam, Tanzania (2.0 ha, 410 trees)

This demonstrates the platform with realistic African farmer data.

---

## 🚀 Deployment (Production)

### Local Server
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repo
4. Set `ANTHROPIC_API_KEY` in Secrets
5. Deploy

### Docker (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["streamlit", "run", "app.py"]
```

Run:
```bash
docker build -t aglane .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY="your-key" aglane
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

### Error: "ANTHROPIC_API_KEY not set"
**Solution:** Set your API key (see Installation Step 2)

### Reports not generating
**Solution:** 
- Ensure API key is set correctly
- Check internet connection
- Verify API key has access to Claude API

### Data disappears when refreshing
**Note:** This is expected! Data is stored in session state (memory). For persistence:
- Export your data before closing (CSV/JSON)
- Implement database storage if needed

### Port 8501 already in use
**Solution:** Specify a different port
```bash
streamlit run app.py --server.port 8502
```

---

## 📚 API Reference

### Main Functions

#### `generate_farmer_id()`
Generates unique farmer ID in format "AGL-XXXX"

#### `calculate_carbon_tons(tree_count: int) -> float`
Calculates annual CO₂ sequestration in metric tons

#### `get_dashboard_metrics() -> dict`
Returns aggregated platform metrics

#### `generate_impact_report_with_ai(metrics: dict) -> str`
Generates AI-powered ESG report using Claude API

#### `load_sample_data()`
Populates platform with demo farmer and plantation data

---

## 📝 License & Attribution

AgLane Climate Intelligence Platform  
Built for climate organizations aggregating smallholder farmers in Africa  
© 2024

---

## 🤝 Support & Contributions

For issues, suggestions, or contributions:
1. Check this guide for solutions
2. Review error messages carefully
3. Verify API key and dependencies

---

## 🌍 About AgLane

AgLane focuses on enabling climate impact through:
- 🌱 **Farmer Aggregation** - Building networks of smallholder farmers
- 🌳 **Carbon Tracking** - Accurate measurement of climate impact
- 💳 **Carbon Credits** - Monetizing environmental impact
- 📊 **Transparency** - Data-driven ESG reporting
- 🤝 **Community** - Supporting African agricultural development

---

**Ready to track climate impact? Launch the app and start registering farmers!**

```bash
streamlit run app.py
```
