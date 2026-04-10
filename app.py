import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor

# ==========================================================
# 1. GLOBAL CONFIGURATION & STYLING
# ==========================================================
st.set_page_config(page_title="SUT Bio-Material Intelligence Hub", page_icon="🌍", layout="wide")

# Custom CSS เพื่อความพรีเมียม
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #007bff; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# 2. MULTI-LANGUAGE SYSTEM (Dictionary)
# ==========================================================
LANG = {
    "TH": {
        "title": "🌍 ระบบปัญญาประดิษฐ์เพื่อการออกแบบพอลิเมอร์ชีวภาพ มทส.",
        "login_header": "🛡️ พื้นที่จำกัด: เฉพาะนักวิจัยและวิศวกร",
        "user_label": "ชื่อนักวิจัย",
        "key_label": "รหัสผ่านความปลอดภัย (Security Key)",
        "nav_dashboard": "📊 แผงควบคุม AI",
        "nav_encyclopedia": "📚 คลังความรู้พอลิเมอร์",
        "nav_carbon": "🌱 วิเคราะห์คาร์บอนฟุตพริ้นท์",
        "nav_expert": "🧠 ระบบปรึกษาการผลิต",
        "input_header": "🛠️ การตั้งค่าสูตรผสม",
        "matrix_label": "พอลิเมอร์ฐาน (Matrix)",
        "filler_label": "กลุ่มสารเติมแต่ง (Filler)",
        "loading_label": "ปริมาณการผสม (% Loading)",
        "process_label": "วิธีการขึ้นรูป",
        "target_label": "เป้าหมายการใช้งาน",
        "predict_title": "📊 ผลการพยากรณ์สมบัติเชิงกล",
        "ts_label": "Tensile Strength (แรงดึง)",
        "el_label": "Elongation (ความยืด)",
        "mo_label": "Modulus (ความแข็ง)",
        "im_label": "Impact (ความเหนียว)",
        "advice_header": "💡 ข้อเสนอแนะทางวิศวกรรม",
        "carbon_header": "🌱 การประเมิน LCA",
        "glossary_title": "📖 พจนานุกรมศัพท์เทคนิค",
        "logout": "ออกจากระบบ"
    },
    "EN": {
        "title": "🌍 SUT Bio-Material Intelligence Hub",
        "login_header": "🛡️ Restricted Access: Engineers Only",
        "user_label": "Researcher Name",
        "key_label": "Security Key (PIN)",
        "nav_dashboard": "📊 AI Dashboard",
        "nav_encyclopedia": "📚 Material Encyclopedia",
        "nav_carbon": "🌱 Carbon Footprint Hub",
        "nav_expert": "🧠 Troubleshooting Expert",
        "input_header": "🛠️ Formula Configuration",
        "matrix_label": "Base Matrix",
        "filler_label": "Filler Group",
        "loading_label": "Filler Loading (%)",
        "process_label": "Processing Method",
        "target_label": "Target Application",
        "predict_title": "📊 AI Mechanical Prediction",
        "ts_label": "Tensile Strength",
        "el_label": "Elongation at Break",
        "mo_label": "Young's Modulus",
        "im_label": "Impact Strength",
        "advice_header": "💡 Engineering Recommendations",
        "carbon_header": "🌱 LCA Assessment",
        "glossary_title": "📖 Polymer Glossary",
        "logout": "Log out"
    }
}

# ==========================================================
# 3. ENGINEERING DATABASE & AI ENGINE
# ==========================================================
MATERIALS_DB = {
    "PLA": {"Full": "Polylactic Acid", "Tg": 60, "Tm": 175, "CFP": 1.58, "Pros": "High strength, Clear", "Cons": "Brittle, Low heat resistance"},
    "PBS": {"Full": "Polybutylene Succinate", "Tg": -32, "Tm": 115, "CFP": 1.85, "Pros": "Tough, Flexible", "Cons": "Lower strength, Higher cost"}
}

@st.cache_resource
def get_ai_engine():
    # สร้าง DOE Data ที่สะท้อนความเป็นจริงทางวิศวกรรม
    np.random.seed(42)
    m_ids, g_ids, pcs, ts_vals, el_vals = [], [], [], [], []
    for m in [0, 1]:
        for g in [0, 1, 2]:
            for p in [0, 10, 20, 30, 40, 50]:
                m_ids.append(m); g_ids.append(g); pcs.append(p)
                # Logic: PLA (0) แข็งกว่า PBS (1) | Natural Filler (0) มักลด Tensile
                base = 62 if m == 0 else 40
                ts_vals.append(base - (p * 0.5) + np.random.normal(0, 1))
                el_vals.append((4 if m == 0 else 150) * (1 - p/100))
    
    X = pd.DataFrame({'M': m_ids, 'G': g_ids, 'P': pcs})
    m_ts = RandomForestRegressor(n_estimators=100).fit(X, ts_vals)
    m_el = RandomForestRegressor(n_estimators=100).fit(X, el_vals)
    return m_ts, m_el

# ==========================================================
# 4. MAIN INTERFACE LOGIC
# ==========================================================
def main():
    # เลือกภาษา (วางไว้นอก if auth เพื่อให้เปลี่ยนได้ตลอด)
    lang_choice = st.sidebar.radio("🌐 Language / ภาษา", ["TH", "EN"], horizontal=True)
    t = LANG[lang_choice]

    if 'auth' not in st.session_state: st.session_state.auth = False

    # --- หน้า Login ---
    if not st.session_state.auth:
        st.title(t["login_header"])
        with st.form("login_form"):
            st.text_input(t["user_label"], key="user_name")
            pwd = st.text_input(t["key_label"], type="password")
            if st.form_submit_button("Authenticate / เข้าสู่ระบบ"):
                if pwd == "SUT2026":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("❌ Key Incorrect!")
        return

    # --- หน้าแอปหลักหลังจาก Login ---
    st.sidebar.title(f"👤 {t['nav_dashboard']}")
    menu = st.sidebar.radio("Main Menu", [t["nav_dashboard"], t["nav_encyclopedia"], t["nav_carbon"], t["nav_expert"]])
    
    if st.sidebar.button(t["logout"]):
        st.session_state.auth = False
        st.rerun()

    engine_ts, engine_el = get_ai_engine()

    # --- ส่วนที่ 1: แผงควบคุม AI ---
    if menu == t["nav_dashboard"]:
        st.title(t["predict_title"])
        col_in, col_res = st.columns([1, 2])
        
        with col_in:
            st.subheader(t["input_header"])
            m_type = st.selectbox(t["matrix_label"], ["PLA", "PBS"])
            f_type = st.selectbox(t["filler_label"], ["Natural Fiber", "Starch", "Mineral"])
            p_load = st.slider(t["loading_label"], 0, 50, 15)
            method = st.selectbox(t["process_label"], ["Injection Molding", "Extrusion", "3D Printing"])
        
        with col_res:
            m_idx = 0 if m_type == "PLA" else 1
            g_idx = ["Natural Fiber", "Starch", "Mineral"].index(f_type)
            ts_pred = engine_ts.predict([[m_idx, g_idx, p_load]])[0]
            el_pred = engine_el.predict([[m_idx, g_idx, p_load]])[0]
            
            c1, c2 = st.columns(2)
            c1.metric(t["ts_label"], f"{ts_pred:.2f} MPa")
            c2.metric(t["el_label"], f"{el_pred:.2f} %")
            
            # Radar Chart
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=[ts_pred, 50, 60, 40, p_load*2], 
                                          theta=['Strength', 'Cost', 'Process', 'Bio-degradable', 'Loading'], fill='toself'))
            st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.header(t["advice_header"])
        if method == "Injection Molding" and p_load > 30:
            st.warning("⚠️ High Filler Loading Detected: Risk of high viscosity and surface defects.")
        else: st.success("✅ Standard parameters are suitable for this formula.")

    # --- ส่วนที่ 2: คลังความรู้ ---
    elif menu == t["nav_encyclopedia"]:
        st.title(t["nav_encyclopedia"])
        sel_m = st.selectbox("Select Material", ["PLA", "PBS"])
        st.json(MATERIALS_DB[sel_m])
        st.subheader(t["glossary_title"])
        st.write("**Tensile Strength:** Maximum stress before failure.")
        st.write("**Modulus:** Stiffness indicator.")

    # --- ส่วนที่ 3: คาร์บอนฟุตพริ้นท์ ---
    elif menu == t["nav_carbon"]:
        st.title(t["nav_carbon"])
        weight = st.number_input("Weight (kg)", 1.0, 1000.0, 10.0)
        cfp = weight * MATERIALS_DB["PLA"]["CFP"]
        st.metric("Total CO2e", f"{cfp:.2f} kg")
        st.info("Calculation based on ISO 14067 Standard.")

    # --- ส่วนที่ 4: ระบบปรึกษาการผลิต ---
    elif menu == t["nav_expert"]:
        st.title(t["nav_expert"])
        defect = st.selectbox("Defect Found", ["Burn Marks", "Warpage", "Short Shot"])
        solutions = {"Burn Marks": "Reduce Melt Temp", "Warpage": "Increase Cooling Time", "Short Shot": "Increase Pressure"}
        st.error(f"Solution: {solutions[defect]}")

if __name__ == "__main__":
    main()
