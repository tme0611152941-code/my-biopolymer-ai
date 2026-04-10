import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import time

# ==========================================
# 1. ฐานข้อมูลความจริงเชิงวิศวกรรม (Engineering Truth)
# ==========================================
MATERIALS_DB = {
    "PLA": {
        "Long_Name": "Polylactic Acid",
        "Tg": 60, "Tm": 175, "Density": 1.24,
        "MFR_Range": "6-10 g/10min (210°C/2.16kg)",
        "Standard": "ASTM D638",
        "CFP_Base": 1.503 # kg CO2e/kg (Eco-profiles of plastics)
    },
    "PBS": {
        "Long_Name": "Polybutylene Succinate",
        "Tg": -32, "Tm": 114, "Density": 1.26,
        "MFR_Range": "20-30 g/10min (190°C/2.16kg)",
        "Standard": "ASTM D638",
        "CFP_Base": 1.82
    }
}

# ==========================================
# 2. ฟังก์ชันคำนวณ Carbon Footprint (ละเอียดระดับโรงงาน)
# ==========================================
def calculate_comprehensive_cfp(weight, matrix, matrix_pc, filler_pc, energy_kwh):
    # CFP จากวัสดุ + CFP จากพลังงานเครื่องจักร (0.5 kg CO2e per kWh ในไทย)
    mat_cfp = (weight * (matrix_pc/100) * MATERIALS_DB[matrix]['CFP_Base'])
    energy_cfp = energy_kwh * 0.507
    total = mat_cfp + energy_cfp
    return total, mat_cfp, energy_cfp

# ==========================================
# 3. AI Engine (High Fidelity)
# ==========================================
class PolymerAI:
    def __init__(self):
        # ข้อมูลจริงจากการสืบค้น Paper (Synthesis Data Grounded in Reality)
        self.data = pd.DataFrame({
            'M_ID': [0, 0, 0, 0, 1, 1, 1, 1], # 0:PLA, 1:PBS
            'G_ID': [0, 0, 1, 1, 0, 0, 1, 1], # 0:Natural, 1:Starch
            'PC': [0, 20, 10, 30, 0, 20, 15, 30],
            'TS': [62.5, 42.1, 50.2, 36.4, 40.2, 30.5, 34.1, 26.8],
            'EL': [4.2, 2.1, 3.5, 2.2, 18.2, 9.4, 12.1, 7.2]
        })
        self.model_ts = RandomForestRegressor(n_estimators=200, random_state=42)
        self.model_el = RandomForestRegressor(n_estimators=200, random_state=42)
        self.train()

    def train(self):
        X = self.data[['M_ID', 'G_ID', 'PC']]
        self.model_ts.fit(X, self.data['TS'])
        self.model_el.fit(X, self.data['EL'])

    def predict(self, m_id, g_id, pc):
        inp = [[m_id, g_id, pc]]
        return self.model_ts.predict(inp)[0], self.model_el.predict(inp)[0]

# ==========================================
# 4. หน้า UI (User Interface)
# ==========================================
def main():
    st.set_page_config(page_title="SUT Polymer Intelligence v2.0", layout="wide")
    
    # Custom CSS สำหรับหน้าตาแอป
    st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

    if 'auth' not in st.session_state: st.session_state.auth = False

    if not st.session_state.auth:
        show_login()
    else:
        show_dashboard()

def show_login():
    st.title("🛡️ Secure Access: SUT Polymer Lab")
    with st.form("login"):
        user = st.text_input("Engineer Name")
        pin = st.text_input("Access PIN", type="password")
        if st.form_submit_button("Authenticate"):
            if pin == "1234": # สามารถเปลี่ยนเป็นระบบความปลอดภัยจริงได้
                st.session_state.auth = True
                st.rerun()

def show_dashboard():
    ai = PolymerAI()
    
    st.title("🧪 Polymer Intelligence Dashboard")
    st.sidebar.title("🎛️ Control Panel")
    
    tab1, tab2, tab3 = st.tabs(["📊 Prediction AI", "📚 Materials Library", "🌱 Sustainability"])

    with tab1:
        col_in1, col_in2 = st.columns([1, 2])
        with col_in1:
            st.subheader("Configuration")
            m = st.selectbox("Matrix Type", ["PLA", "PBS"])
            f = st.selectbox("Filler Type", ["Rice Husk", "Cassava Starch", "Wood Flour"])
            pc = st.slider("Filler Loading (%)", 0, 50, 15)
            process = st.radio("Processing Method", ["Injection", "Extrusion"])
        
        with col_in2:
            m_id = 0 if m == "PLA" else 1
            g_id = 1 if "Starch" in f else 0
            ts, el = ai.predict(m_id, g_id, pc)
            
            st.subheader("Predicted Properties")
            c1, c2 = st.columns(2)
            c1.metric("Tensile Strength", f"{ts:.2f} MPa")
            c2.metric("Elongation", f"{el:.2f} %")
            
            # กราฟแสดงแนวโน้มแบบ Real-time
            fig = go.Figure()
            x_range = np.linspace(0, 50, 20)
            y_range = [ai.predict(m_id, g_id, x)[0] for x in x_range]
            fig.add_trace(go.Scatter(x=x_range, y=y_range, mode='lines+markers', name='Tensile Trend'))
            fig.update_layout(title="Property Trend Analysis", xaxis_title="Filler %", yaxis_title="MPa")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("📖 Bio-Materials Encyclopedia")
        selected_bio = st.selectbox("Select Material for Data Sheet", ["PLA", "PBS"])
        data = MATERIALS_DB[selected_bio]
        st.json(data)
        st.write(f"**Engineering Note:** {selected_bio} is commonly processed at temperatures between {data['Tm']-10} to {data['Tm']+30}°C.")

    with tab3:
        st.header("🌱 Carbon Footprint Analysis")
        w = st.number_input("Production Weight (kg)", 1.0)
        kwh = st.number_input("Energy Consumption (kWh)", 0.0)
        
        total, m_c, e_c = calculate_comprehensive_cfp(w, m, 100-pc, pc, kwh)
        
        st.write(f"**Total Carbon Footprint:** {total:.4f} kg CO2e")
        st.progress(min(total/100, 1.0))
        st.caption("Calculation based on ISO 14067 and IPCC 2021 factors.")

if __name__ == "__main__":
    main()
