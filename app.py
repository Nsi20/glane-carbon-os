import streamlit as st
import pandas as pd
import uuid
import os
import random
import io
import base64
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
import datetime
import plotly.express as px
import plotly.graph_objects as go


# -----------------------------------
# CONFIGURATION & INITIALIZATION
# -----------------------------------
st.set_page_config(
    page_title="AgLane Carbon Aggregation OS",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main {
        background: #121212;
    }
    .stMetric {
        background: #1e1e1e;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border-left: 4px solid #2ecc71;
    }
    .stMetric label {
        color: #a0a0a0 !important;
    }
    .stMetric div {
        color: #e0e0e0 !important;
    }
    h1 {
        color: #2ecc71;
        font-weight: 700;
    }
    h2, h3 {
        color: #a8e6cf;
    }
    .report-section {
        background: #1e1e1e;
        color: #e0e0e0;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .registration-slip {
        background: #1e1e1e;
        border: 2px solid #2ecc71;
        border-radius: 15px;
        padding: 20px;
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        margin-top: 20px;
    }
    .slip-header {
        text-align: center;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .slip-title {
        color: #2ecc71;
        font-size: 1.1rem;
        font-weight: 800;
        margin: 0;
    }
    .slip-subtitle {
        color: #a0a0a0;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .passport-space {
        width: 100px;
        height: 120px;
        border: 2px dashed #444;
        background: #252525;
        margin: 0 auto 15px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #666;
        font-size: 0.6rem;
        text-align: center;
    }
    .slip-field {
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
    }
    .field-label {
        color: #888;
        font-weight: 500;
    }
    .field-value {
        color: #ffffff;
        font-weight: 600;
        text-align: right;
    }
    .slip-footer {
        margin-top: 15px;
        border-top: 1px solid #333;
        padding-top: 10px;
        text-align: center;
        font-size: 0.6rem;
        color: #666;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for farmers data
if 'farmers' not in st.session_state:
    st.session_state.farmers = []

if 'impact_report' not in st.session_state:
    st.session_state.impact_report = ""

# Coordinates for map visualization (Approximate center of Nigerian States)
NIGERIA_STATE_COORDS = {
    "Kano State, Nigeria": [11.9964, 8.5167],
    "Kaduna State, Nigeria": [10.5105, 7.4165],
    "Oyo State, Nigeria": [8.1574, 3.6147],
    "Ogun State, Nigeria": [7.1500, 3.3500],
    "Enugu State, Nigeria": [6.4520, 7.5103],
    "Anambra State, Nigeria": [6.2209, 7.0068],
    "Katsina State, Nigeria": [12.9816, 7.6223],
    "Plateau State, Nigeria": [9.1758, 9.9322],
    "Benue State, Nigeria": [7.3369, 8.7360],
    "Niger State, Nigeria": [9.9322, 5.5975],
    "Ondo State, Nigeria": [7.1000, 5.0500],
    "Osun State, Nigeria": [7.5629, 4.5200],
    "Borno State, Nigeria": [11.8333, 13.1500],
    "Sokoto State, Nigeria": [13.0609, 5.2390],
    "Delta State, Nigeria": [5.5325, 5.8987]
}

def process_csv_upload(uploaded_file):
    """Processes bulk CSV upload for farmers."""
    try:
        new_df = pd.read_csv(uploaded_file)
        # Validate columns
        required = ["Name", "NIN", "Location", "Farm Size (ha)", "Trees Planted"]
        if not all(col in new_df.columns for col in required):
            st.error(f"CSV missing required columns: {required}")
            return
            
        for _, row in new_df.iterrows():
            add_farmer(
                name=row["Name"],
                location=row["Location"] if row["Location"] in NIGERIA_STATE_COORDS else random.choice(list(NIGERIA_STATE_COORDS.keys())),
                size=row["Farm Size (ha)"],
                trees=row["Trees Planted"],
                nin=str(row["NIN"]),
                project_id=row.get("Project ID", "ACAL-BULK-001"),
                verification_status=row.get("Verification Status", "Pending"),
                ownership_status=row.get("Ownership Status", "Verified owner"),
                carbon_lifecycle=row.get("Carbon Lifecycle", "Estimated"),
                source_connection=row.get("Source Connection", "Direct Registration")
            )
        st.success(f"Successfully imported {len(new_df)} farmers!")
    except Exception as e:
        st.error(f"Error processing CSV: {e}")

# -----------------------------------
# CONSTANTS & UTILS
# -----------------------------------
CARBON_PER_TREE_KG = 22.0

def generate_farmer_id():
    """Generates a unique Farmer ID format: AGL-XXXX"""
    return f"AGL-{str(uuid.uuid4().int)[:4].zfill(4)}"

def generate_serial_number():
    """Generates a registration serial number."""
    return f"SN-{random.randint(100000, 999999)}"

def calculate_carbon_tons(trees):
    """Calculate carbon credits in tons based on number of trees."""
    return (trees * CARBON_PER_TREE_KG) / 1000.0

def generate_id_image(slip_data):
    """Generates a professional ID card image for the farmer."""
    # Constants for layout
    W, H = 400, 600
    bg_color = (30, 30, 30)  # #1e1e1e
    primary_color = (46, 204, 113)  # #2ecc71
    text_color = (224, 224, 224)  # #e0e0e0
    label_color = (136, 136, 136)  # #888888
    
    # Create canvas
    img = Image.new('RGB', (W, H), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts
    try:
        # Try common font paths across platforms
        _font_candidates = [
            "C:\\Windows\\Fonts\\arial.ttf",          # Windows
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux (Render)
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
        ]
        _bold_candidates = [
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        ]
        _reg = next((f for f in _font_candidates if os.path.exists(f)), None)
        _bold = next((f for f in _bold_candidates if os.path.exists(f)), None)
        if _reg and _bold:
            title_font = ImageFont.truetype(_bold, 24)
            subtitle_font = ImageFont.truetype(_reg, 14)
            label_font = ImageFont.truetype(_reg, 16)
            value_font = ImageFont.truetype(_bold, 16)
            footer_font = ImageFont.truetype(_reg, 12)
        else:
            raise FileNotFoundError("No system fonts found")
    except:
        # Fallback to default
        title_font = subtitle_font = label_font = value_font = footer_font = ImageFont.load_default()

    # Draw border
    draw.rectangle([10, 10, W-10, H-10], outline=primary_color, width=3)
    
    # Header
    draw.text((W//2, 40), "AGLANE CLIMATE", fill=primary_color, font=title_font, anchor="mm")
    draw.text((W//2, 70), "Registry Identification Slip", fill=label_color, font=subtitle_font, anchor="mm")
    
    # Passport Photo Space
    passport_y = 100
    passport_w, passport_h = 120, 150
    passport_x = (W - passport_w) // 2
    
    if slip_data.get('passport_photo'):
        try:
            p_img = Image.open(io.BytesIO(slip_data['passport_photo']))
            p_img = p_img.resize((passport_w, passport_h), Image.Resampling.LANCZOS)
            img.paste(p_img, (passport_x, passport_y))
        except:
            draw.rectangle([passport_x, passport_y, passport_x+passport_w, passport_y+passport_h], outline=label_color, width=1)
            draw.text((W//2, passport_y + passport_h//2), "PHOTO ERROR", fill=label_color, font=subtitle_font, anchor="mm")
    else:
        draw.rectangle([passport_x, passport_y, passport_x+passport_w, passport_y+passport_h], outline=label_color, width=1)
        draw.text((W//2, passport_y + passport_h//2), "NO PHOTO", fill=label_color, font=subtitle_font, anchor="mm")

    # Fields
    fields = [
        ("NAME", slip_data['name']),
        ("NIN", slip_data['nin']),
        ("LOCATION", slip_data['location']),
        ("FARM SIZE", f"{slip_data['size']} ha"),
        ("TREES", str(slip_data['trees'])),
        ("CLUSTER ID", slip_data['project_id']),
        ("SERIAL", slip_data['serial_number']),
        ("REG. ID", slip_data['farmer_id'])
    ]
    
    start_y = 280
    line_height = 30
    
    for i, (label, value) in enumerate(fields):
        curr_y = start_y + (i * line_height)
        draw.text((30, curr_y), label, fill=label_color, font=label_font)
        # Handle long names/values by truncating if necessary (simplified)
        draw.text((W-30, curr_y), str(value), fill=text_color, font=value_font, anchor="ra")

    # Footer
    draw.line([30, H-60, W-30, H-60], fill=label_color, width=1)
    draw.text((W//2, H-40), "Verified Climate Asset Aggregator", fill=label_color, font=footer_font, anchor="mm")
    draw.text((W//2, H-25), "*Keep this slip for your records*", fill=label_color, font=footer_font, anchor="mm")

    # Convert to bytes
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=95)
    return buf.getvalue()

def add_farmer(name, location, size, trees, nin, project_id, verification_status, ownership_status, carbon_lifecycle, source_connection, passport_photo=None, reg_date=None):
    """Adds a new farmer to the registry and calculates carbon offset."""
    farmer_id = generate_farmer_id()
    serial_number = generate_serial_number()
    carbon = calculate_carbon_tons(trees)
    
    if reg_date is None:
        reg_date = datetime.date.today().strftime("%Y-%m-%d")
    
    st.session_state.farmers.append({
        "Registration Date": reg_date,
        "Project ID": project_id,
        "Serial Number": serial_number,
        "Farmer ID": farmer_id,
        "NIN": nin,
        "Name": name,
        "Location": location,
        "Verification Status": verification_status,
        "Ownership Status": ownership_status,
        "Carbon Lifecycle": carbon_lifecycle,
        "Source Connection": source_connection,
        "Farm Size (ha)": float(size),
        "Trees Planted": int(trees),
        "Est. Carbon (Tons/Year)": carbon,
        "Passport Photo": passport_photo,
        "Awareness Score": random.randint(1, 10)  # Dummy ACAF metric
    })
    return farmer_id, serial_number

def generate_dummy_data():
    """Generates a realistic sample dataset for demonstration purposes."""
    first_names = ["Aisha", "Samuel", "Grace", "David", "Fatima", "Emmanuel", "Mercy", "Peter", "Esther", "Joseph", "Mary", "Isaac", "Sarah", "Musa", "Zainab", "Ibrahim", "Joy", "Daniel", "Oluwaseun", "Chidi", "Ngozi", "Emeka", "Amina", "Abubakar", "Funke"]
    last_names = ["Bello", "Aliyu", "Adebayo", "Okafor", "Eze", "Ogunleye", "Ibrahim", "Abubakar", "Danladi", "Okeke", "Adeyemi", "Nwachukwu", "Umar", "Olawale", "Nwankwo", "Adeleke", "Lawal", "Okonkwo", "Sani"]
    
    locations = list(NIGERIA_STATE_COORDS.keys())
    
    # Generate 30 realistic farmers
    for i in range(30):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        location = random.choice(locations)
        
        # Determine Project ID based on location to group properly
        state_prefix = location.split()[0][:4].upper()
        project_id = f"ACAL-{state_prefix}-001"
        
        size = round(random.uniform(0.5, 3.5), 2)
        tree_density = random.randint(200, 800)
        trees = int(size * tree_density)
        
        # Randomize statuses for realistic data spread
        verification_status = random.choice(["Pending", "Verified (Drone)"])
        ownership_status = random.choices(["Verified owner", "Community land", "Disputed"], weights=[70, 25, 5])[0]
        carbon_lifecycle = random.choice(["Estimated", "Under Verification", "Issued"])
        source_connection = random.choices(["ACAF Programme", "Direct Registration"], weights=[60, 40])[0]
        
        # Spread dates over the last 6 months
        random_days = random.randint(0, 180)
        reg_date = (datetime.date.today() - datetime.timedelta(days=random_days)).strftime("%Y-%m-%d")
        
        add_farmer(
            name=name,
            location=location,
            size=size,
            trees=trees,
            nin=f"{random.randint(10000000000, 99999999999)}",
            project_id=project_id,
            verification_status=verification_status,
            ownership_status=ownership_status,
            carbon_lifecycle=carbon_lifecycle,
            source_connection=source_connection,
            reg_date=reg_date
        )

# -----------------------------------
# UI COMPONENTS: SIDEBAR
# -----------------------------------
# Display Logo if available (check local paths, then fallback)
_logo_paths = [
    os.path.join(os.path.dirname(__file__), "logo.png"),
    "C:\\Users\\nsi_d\\.gemini\\antigravity\\brain\\10961e98-aa97-44af-83a1-c3f300d047af\\aglane_logo_1778409593744.png",
]
_logo_found = next((p for p in _logo_paths if os.path.exists(p)), None)
if _logo_found:
    st.sidebar.image(_logo_found, use_container_width=True)
else:
    st.sidebar.title("🌱 AgLane Registry")

st.sidebar.markdown("### 🧬 Asset Aggregation")
st.sidebar.markdown("Register farmers & track climate assets.")

with st.sidebar.form("farmer_registration_form"):
    st.subheader("1. Farmer Details")
    name = st.text_input("Farmer Name")
    nin = st.text_input("National Identification Number (NIN)", max_chars=11)
    location = st.selectbox("Location (State)", list(NIGERIA_STATE_COORDS.keys()))
    
    st.markdown("---")
    st.subheader("2. Compliance & Verification")
    project_id = st.text_input("Project Cluster ID", value="ACAL-GEN-001")
    verification_status = st.selectbox("Verification Status", ["Pending", "Verified (Drone)", "Verified (Field Agent)"])
    ownership_status = st.selectbox("Land Ownership Status", ["Verified owner", "Community land", "Disputed"])
    carbon_lifecycle = st.selectbox("Carbon Lifecycle Status", ["Estimated", "Under Verification", "Issued", "Sold"])
    source_connection = st.selectbox("Farmer Source", ["ACAF Programme", "Direct Registration"])
    
    st.markdown("---")
    st.subheader("3. Plantation Data Input")
    size = st.number_input("Farm Size (hectares)", min_value=0.1, step=0.1)
    trees = st.number_input("Tree Count (Drone/ML verified)", min_value=1, step=1)
    
    st.markdown("---")
    st.subheader("4. Identification")
    passport_file = st.file_uploader("Upload Passport Photo", type=["jpg", "jpeg", "png"])
    
    submit = st.form_submit_button("Register Farmer & Assets", use_container_width=True)
    
    if submit:
        if not name.strip() or not nin.strip():
            st.error("Please fill in all mandatory details (Name, NIN).")
        else:
            passport_data = None
            if passport_file is not None:
                passport_data = passport_file.read()
            
            farmer_id, serial_number = add_farmer(name, location, size, trees, nin, project_id, verification_status, ownership_status, carbon_lifecycle, source_connection, passport_photo=passport_data)
            st.session_state.last_registered = {
                "name": name,
                "farmer_id": farmer_id,
                "serial_number": serial_number,
                "nin": nin,
                "location": location,
                "size": size,
                "trees": trees,
                "project_id": project_id,
                "passport_photo": passport_data
            }
            st.success(f"Successfully registered {name} to {project_id}!")

if 'last_registered' in st.session_state:
    st.sidebar.markdown("---")
    slip_data = st.session_state.last_registered
    
    # Process image for display
    img_display = '<div class="passport-space">PASSPORT<br>PHOTO<br>SPACE</div>'
    if slip_data.get('passport_photo'):
        b64_img = base64.b64encode(slip_data['passport_photo']).decode()
        img_display = f'<div class="passport-space" style="border: none;"><img src="data:image/png;base64,{b64_img}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px;"></div>'
    
    # HTML-based professional slip
    slip_html = f"""<div class="registration-slip">
<div class="slip-header">
<div class="slip-title">AGLANE CLIMATE</div>
<div class="slip-subtitle">Registry Identification Slip</div>
</div>
{img_display}
<div class="slip-field">
<span class="field-label">NAME</span>
<span class="field-value">{slip_data['name']}</span>
</div>
<div class="slip-field">
<span class="field-label">NIN</span>
<span class="field-value">{slip_data['nin']}</span>
</div>
<div class="slip-field">
<span class="field-label">LOCATION</span>
<span class="field-value">{slip_data['location']}</span>
</div>
<div class="slip-field">
<span class="field-label">FARM SIZE</span>
<span class="field-value">{slip_data['size']} ha</span>
</div>
<div class="slip-field">
<span class="field-label">TREES</span>
<span class="field-value">{slip_data['trees']}</span>
</div>
<div class="slip-field">
<span class="field-label">CLUSTER ID</span>
<span class="field-value">{slip_data['project_id']}</span>
</div>
<div class="slip-field">
<span class="field-label">SERIAL</span>
<span class="field-value">{slip_data['serial_number']}</span>
</div>
<div class="slip-field">
<span class="field-label">REG. ID</span>
<span class="field-value">{slip_data['farmer_id']}</span>
</div>
<div class="slip-footer">
Verified Climate Asset Aggregator<br>
*Keep this slip for your records*
</div>
</div>"""
    st.sidebar.markdown(slip_html, unsafe_allow_html=True)
    
    # Generate ID Image for download
    id_img_bytes = generate_id_image(slip_data)
    
    st.sidebar.download_button(
        label="🖼️ Download ID Card (JPG)",
        data=id_img_bytes,
        file_name=f"AgLane_ID_{slip_data['serial_number']}.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### Prototyping Tools")
if st.sidebar.button("Load Sample Dummy Data", use_container_width=True):
    generate_dummy_data()
    st.sidebar.success("Loaded 30 realistic sample farmers with cluster aggregations.")

# MAIN DASHBOARD STRUCTURE
# -----------------------------------
st.title("AgLane Carbon Aggregation OS 🌍")
st.markdown("### *Unified Climate Infrastructure for Smallholder Aggregation*")

total_farmers = len(st.session_state.farmers)
total_trees = sum(f["Trees Planted"] for f in st.session_state.farmers) if total_farmers > 0 else 0
total_carbon = sum(f["Est. Carbon (Tons/Year)"] for f in st.session_state.farmers) if total_farmers > 0 else 0.0

# Metrics Header
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("Aggregated Farmers", f"{total_farmers:,}")
m_col2.metric("Verified Trees", f"{total_trees:,}")
m_col3.metric("Est. CO2 Offset (Tons)", f"{total_carbon:,.2f}")

# Tabs for organization
tab_dash, tab_registry, tab_acaf, tab_esg = st.tabs(["📍 Overview", "📋 Registry", "💡 ACAF Impact", "📄 ESG Reporting"])

with tab_dash:
    if total_farmers > 0:
        st.subheader("Geographic Asset Distribution")
        map_data = []
        for f in st.session_state.farmers:
            loc = f["Location"]
            if loc in NIGERIA_STATE_COORDS:
                lat = NIGERIA_STATE_COORDS[loc][0] + random.uniform(-0.1, 0.1)
                lon = NIGERIA_STATE_COORDS[loc][1] + random.uniform(-0.1, 0.1)
                map_data.append({"lat": lat, "lon": lon})
        st.map(pd.DataFrame(map_data))
        
        # Aggregation Narrative
        st.info("**Aggregation Strategy**: We group farmers into 'Project Clusters' (e.g., ACAL-KANO-001) to achieve economies of scale for carbon verification and MRV (Measurement, Reporting, and Verification).")
    else:
        st.info("Load sample data or register a farmer to see the overview.")

with tab_registry:
    st.subheader("Core Aggregation Ledger")
    if total_farmers > 0:
        df = pd.DataFrame(st.session_state.farmers)
        # Drop columns not for table display
        display_df = df.drop(columns=["Passport Photo"])
        st.dataframe(display_df, use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                display_df.to_excel(writer, index=False, sheet_name='Ledger')
            st.download_button("📥 Export to Excel", data=buffer.getvalue(), file_name="AgLane_Ledger.xlsx")
        with c2:
            st.button("🔄 Refresh Data", type="secondary")
    else:
        st.warning("Registry is empty.")

with tab_acaf:
    st.subheader("ACAF Impact Module")
    st.markdown("Tracking social awareness and programme participation from the AgLane Climate Awareness Foundation (ACAF).")
    
    # Bulk Upload
    with st.expander("⬆️ Bulk CSV Upload (Google Forms / Field Surveys)"):
        uploaded_csv = st.file_uploader("Upload Questionnaire Data", type=["csv"])
        if uploaded_csv:
            process_csv_upload(uploaded_csv)
            
    if total_farmers > 0:
        df = pd.DataFrame(st.session_state.farmers)
        
        col_v1, col_v2 = st.columns(2)
        
        # Visual 1: Source Connection
        source_counts = df["Source Connection"].value_counts().reset_index()
        fig1 = px.pie(source_counts, values='count', names='Source Connection', 
                     title="Farmer Onboarding Source", 
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        col_v1.plotly_chart(fig1, use_container_width=True)
        
        # Visual 2: Awareness Score Trend
        fig2 = px.histogram(df, x="Awareness Score", nbins=10, 
                           title="Climate Awareness Score Distribution",
                           color_discrete_sequence=['#2ecc71'])
        col_v2.plotly_chart(fig2, use_container_width=True)
        
        st.success("**Impact Insight**: The ACAF Programme provides 60% of our high-quality, verified farmer leads, ensuring deep community engagement.")
    else:
        st.info("Visualizations will appear once data is loaded.")

with tab_esg:
    st.subheader("AI ESG Compliance Reporting")
    st.markdown("Generate Verra-aligned impact reports using our AI engine.")
    
    # API KEY check
    api_key = os.getenv("GROQ_API_KEY", "")

if st.button("Generate Compliance Report", type="primary"):
    if total_farmers == 0:
        st.error("Cannot generate report. No farmer data available on the platform.")
    else:
        with st.spinner("Analyzing project clusters and generating Verra-aligned ESG impact report using Groq..."):
            try:
                client = Groq(api_key=api_key)
                
                # Analyze Data for Prompt
                df = pd.DataFrame(st.session_state.farmers)
                unique_projects = df["Project ID"].nunique()
                acaf_count = len(df[df["Source Connection"] == "ACAF Programme"])
                issued_count = len(df[df["Carbon Lifecycle"] == "Issued"])
                verified_drone = len(df[df["Verification Status"] == "Verified (Drone)"])
                disputed_land = len(df[df["Ownership Status"] == "Disputed"])
                
                prompt = f"""
                You are a senior ESG and Carbon Market Analyst. Generate a professional, investor-grade climate impact report for 'AgLane Carbon Aggregation Limited (ACAL)'.
                
                The report MUST be aligned with voluntary carbon market standards (e.g., Verra concepts).
                
                Here is the current real-time aggregated portfolio data:
                - Total Farmers Aggregated: {total_farmers}
                - Active Project Clusters: {unique_projects}
                - Total Trees Planted & Verified: {total_trees}
                - Total Estimated Carbon Sequestration: {total_carbon:.2f} Tons of CO2 per year.
                
                Impact & Social Metrics (AgLane Climate Awareness Foundation - ACAF):
                - Farmers Sourced from ACAF Programme: {acaf_count}
                - Average Community Awareness Score: {df["Awareness Score"].mean():.2f} / 10
                
                Key Compliance & Trust Metrics:
                - Carbon Credits Issued: {issued_count} farmers have moved to the Issued stage.
                - Drone Verified Farmers: {verified_drone}
                - Land Disputes Identified: {disputed_land} farmers flagged.
                
                Please write a concise, professional report including:
                1. Executive Portfolio Overview
                2. Social Impact Narrative (Highlight the ACAF education to registration pipeline)
                3. Technical MRV & Carbon Lifecycle Analysis
                4. Risk Mitigation (Land ownership & verification protocols)
                5. Strategic Conclusion
                
                Keep the tone extremely professional for institutional buyers.
                """
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a professional ESG and Carbon Market reporting assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                
                st.session_state.impact_report = response.choices[0].message.content
            except Exception as e:
                st.error(f"Error generating report: {e}")

if st.session_state.impact_report:
    st.markdown("### AgLane Aggregated Compliance Report")
    st.markdown(f"<div class='report-section'>{st.session_state.impact_report}</div>", unsafe_allow_html=True)
    
    st.download_button(
        label="⬇️ Download Report as Text (.txt)",
        data=st.session_state.impact_report,
        file_name="AgLane_Compliance_Report.txt",
        mime="text/plain",
        use_container_width=True
    )
