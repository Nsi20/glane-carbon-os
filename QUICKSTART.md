# 🚀 AgLane Quick-Start (5 Minutes)

## Option 1: Run with API Key (Full Features)

### Step 1: Set API Key
```bash
# macOS/Linux:
export ANTHROPIC_API_KEY="sk-ant-your-actual-api-key-here"

# Windows PowerShell:
$env:ANTHROPIC_API_KEY = "sk-ant-your-actual-api-key-here"
```

### Step 2: Install & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

✅ Opens at `http://localhost:8501`

---

## Option 2: Demo Mode (No API Key)

### Step 1: Just Run It
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Step 2: In the App
- Click **"📥 Load Sample Data"** in sidebar
- Dashboard, farmer registry, and exports work perfectly
- AI reports will show a helpful message about API key

---

## 🎯 First 30 Seconds

1. **Load Demo Data**
   - Sidebar → Click "📥 Load Sample Data"
   - 💥 Instant: 4 farmers + 1,860 trees + 40.9 tons CO₂

2. **See the Dashboard**
   - Sidebar → Click "📊 Dashboard"
   - View total farmers, trees, carbon metrics

3. **Register Your Own Farmer**
   - Sidebar → "👨‍🌾 Register Farmer"
   - Enter name, location, farm size
   - Get auto-generated ID

4. **Add Trees**
   - Sidebar → "🌳 Add Plantation"
   - Select farmer → Enter tree count
   - Auto-calculates carbon

5. **Generate Report** (requires API key)
   - Sidebar → "📈 Reports"
   - Click "🚀 Generate Impact Report"
   - Download as text or JSON

---

## 📋 What Works Without API Key

✅ Farmer registration  
✅ Plantation data entry  
✅ Dashboard & metrics  
✅ Data export (CSV, JSON)  
✅ Sample data loading  
❌ AI report generation (requires API key)

---

## 🔑 Get API Key (2 Minutes)

1. Visit: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create new key
5. Copy and paste into terminal:

```bash
export ANTHROPIC_API_KEY="sk-ant-xxx..."
```

---

## 📦 Files Included

```
app.py              ← Main application (all-in-one)
requirements.txt    ← Dependencies to install
README.md          ← Full documentation
QUICKSTART.md      ← This file
```

---

## ⚡ Common Commands

### Start the app
```bash
streamlit run app.py
```

### Stop the app
```
Ctrl + C
```

### Clear all data
```
In app sidebar → "🗑️ Clear All Data"
```

### Download farmer data
```
Go to Dashboard → "📥 Download Farmer Data (CSV)"
```

---

## 🎓 Example Workflow

```
1. Load Sample Data
   ↓
2. See 4 farmers, 1,860 trees, 40.9 tons CO₂/year
   ↓
3. Register "Peter Njoka" from "Nairobi, Kenya" (3.0 ha)
   ↓
4. Add 500 trees to Peter's farm
   ↓
5. Dashboard shows: 5 farmers, 2,360 trees, 51.92 tons CO₂
   ↓
6. Generate AI report (with API key)
   ↓
7. Download report & data
```

---

## 🆘 Stuck?

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API Key error"
Set your key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Port 8501 in use
```bash
streamlit run app.py --server.port 8502
```

### App won't start
```bash
python --version  # Make sure Python 3.8+
pip --version     # Make sure pip works
```

---

## 📊 Dashboard Metrics Explained

| Metric | What It Means |
|--------|--------------|
| **Total Farmers** | Number of registered smallholder farmers |
| **Total Trees** | Sum of all trees across all farms |
| **Annual Carbon** | CO₂ equivalent sequestered per year (metric tons) |
| **Est. Credits** | Market value @ $20/ton (industry standard) |

---

## 💡 Tips

- **Sample Data** is great for demos — add your own to test!
- **Export Data** in CSV for Excel/Sheets analysis
- **API Key** unlocks AI reports for professional presentations
- **Refresh** the page if something looks wrong
- **Load Sample Data** repeatedly to reset to known state

---

## 🌍 Next Steps

1. **Play with the app** - Register farmers, add trees, explore
2. **Get an API key** - Unlock AI report generation
3. **Export data** - Use CSV for external analysis
4. **Deploy** - Share on Streamlit Cloud (see README.md)
5. **Customize** - Edit carbon rates, colors, report prompts

---

**You're ready! Run this:**

```bash
streamlit run app.py
```

**Then:**
- Open http://localhost:8501 in your browser
- Click "📥 Load Sample Data" in sidebar
- Explore! 🌱

---

Questions? See README.md for full documentation.
