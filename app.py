import streamlit as st
import pandas as pd
import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="VSP Mainframe Ops", 
    page_icon="🏭", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Embedded CSS Styling (Dark/Modern Theme)
st.markdown("""
    <style>
        /* Base configuration */
        .reportview-container {
            background: #0e1117;
        }
        
        /* Glassmorphism KPI Cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: #4A90E2;
        }
        
        /* Modernized Headers */
        h1 {
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        /* Custom clean buttons */
        .stButton>button {
            background-color: #4A90E2 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover {
            background-color: #357ABD !important;
            box-shadow: 0 0 12px rgba(74, 144, 226, 0.4);
        }
    </style>
""", unsafe_allow_html=True)

# 3. Main Dashboard Header
st.title("🏭 Visakha Steel Mainframe Operations")
st.markdown("<p style='color: #8A99AD; font-size: 1.1rem; margin-top: -15px;'>Enterprise Core Monitoring & Automated Excursion Registry</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin-top: 0;'/>", unsafe_allow_html=True)

# 4. Initialize Stateful In-Memory Database
if 'plant_data' not in st.session_state:
    st.session_state.plant_data = pd.DataFrame([
        {"Timestamp": "2026-10-10 10:00", "Unit": "Blast Furnace 1", "Temperature (°C)": 1550, "Pressure (bar)": 2.4, "Status": "Normal"},
        {"Timestamp": "2026-10-10 11:30", "Unit": "Blast Furnace 2", "Temperature (°C)": 1650, "Pressure (bar)": 2.8, "Status": "Critical Alert"},
        {"Timestamp": "2026-10-10 12:15", "Unit": "Steel Melting Shop", "Temperature (°C)": 1600, "Pressure (bar)": 1.9, "Status": "Normal"},
        {"Timestamp": "2026-10-11 01:00", "Unit": "Blast Furnace 1", "Temperature (°C)": 1580, "Pressure (bar)": 2.2, "Status": "Normal"},
    ])

# 5. Modular Sidebar Layout
st.sidebar.markdown("<h2 style='color: white; font-size: 1.3rem;'>Control Console</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("Navigation", ["📊 Real-Time Operations", "📝 Log Core Parameters"])

st.sidebar.markdown("---")
st.sidebar.markdown("### System Telemetry")
st.sidebar.caption("Telemetry Engine: v2.4.1-Stable")
st.sidebar.caption("Server Node: Localhost")

# 6. PAGE 1: Enhanced Real-Time Analytics
if page == "📊 Real-Time Operations":
    
    # Grid Layout for Custom Styled Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <p style="color: #8A99AD; font-size: 0.85rem; margin:0; text-transform: uppercase;">Active Node Status</p>
                <h2 style="color: #2ecc71; margin: 10px 0 0 0; font-size: 2.2rem;">ONLINE</h2>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        max_temp = st.session_state.plant_data["Temperature (°C)"].max()
        st.markdown(f"""
            <div class="metric-card">
                <p style="color: #8A99AD; font-size: 0.85rem; margin:0; text-transform: uppercase;">Peak Thermal Level</p>
                <h2 style="color: #e74c3c; margin: 10px 0 0 0; font-size: 2.2rem;">{max_temp} °C</h2>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        total_logs = len(st.session_state.plant_data)
        st.markdown(f"""
            <div class="metric-card">
                <p style="color: #8A99AD; font-size: 0.85rem; margin:0; text-transform: uppercase;">Total Registry Entries</p>
                <h2 style="color: #3498db; margin: 10px 0 0 0; font-size: 2.2rem;">{total_logs} Logs</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dynamic Layout Split: Left Table, Right Visualization
    graph_col, data_col = st.columns(2)
    
    with graph_col:
        st.markdown("### 📈 Thermal Progression Trend")
        chart_data = st.session_state.plant_data.pivot_table(
            index="Timestamp", 
            columns="Unit", 
            values="Temperature (°C)"
        ).ffill()
        st.line_chart(chart_data, height=260)

    with data_col:
        st.markdown("### 📋 Active Registry Matrix")
        st.dataframe(
            st.session_state.plant_data, 
            use_container_width=True, 
            hide_index=True,
            height=260
        )
        
        # System Export Feature [filegen-via-code]
        csv = st.session_state.plant_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Registry to CSV",
            data=csv,
            file_name=f"VSP_Ops_Export_{datetime.date.today()}.csv",
            mime="text/csv",
        )

    # Automated Background Incident Alerts
    st.markdown("---")
    if "Critical Alert" in st.session_state.plant_data["Status"].values:
        st.error("🚨 **System Alert:** Thermal or Barometric excursions detected in active cells. Immediate supervision ordered.")
    else:
        st.success("🛡️ **System Status:** All telemetry units report operations within acceptable parameters.")

# 7. PAGE 2: Modernized Input Form
elif page == "📝 Log Core Parameters":
    st.markdown("### 📝 Mainframe Data Entry Panel")
    st.markdown("Submit authenticated telemetry logs below to update the system framework.")
    
    # Center the form layout neatly
    form_container = st.container(border=True)
    with form_container:
        with st.form("modern_log_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            
            with f_col1:
                unit_name = st.selectbox("🎯 Target Operational Unit", ["Blast Furnace 1", "Blast Furnace 2", "Steel Melting Shop", "Rolling Mills"])
                temp = st.number_input("🔥 Core Temperature (°C)", min_value=800, max_value=2200, value=1500)
            
            with f_col2:
                pressure = st.number_input("💨 Chamber Pressure (bar)", min_value=0.5, max_value=6.0, value=2.1, step=0.1)
                st.markdown("<br>", unsafe_allow_html=True)
                submit_btn = st.form_submit_button("⚡ Commit Data To Node")
            
            if submit_btn:
                # Conditional Logic Engine
                status_check = "Normal"
                if temp > 1620 or pressure > 2.6:
                    status_check = "Critical Alert"
                    
                new_entry = {
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Unit": unit_name,
                    "Temperature (°C)": temp,
                    "Pressure (bar)": pressure,
                    "Status": status_check
                }
                
                # Append structural data row seamlessly
                st.session_state.plant_data = pd.concat([st.session_state.plant_data, pd.DataFrame([new_entry])], ignore_index=True)
                st.toast(f"Data packet for {unit_name} successfully verified!", icon="✅")
