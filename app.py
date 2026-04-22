import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="SUT Bio-Material Hub", page_icon="🌍", layout="wide")
st.markdown("""<style>
    .stMetric { background: #ffffff; padding: 20px; border-radius: 15px; border-left: 5px solid #00e5ff; }
    .main { background-color: #f7f9fc; }
</style>""", unsafe_allow_html=True)

# --- 2. MULTI-LANGUAGE DICTIONARY ---
LANG = {
    "TH": {"title": "ระบบ AI ออกแบบวัสดุชีวภาพ มทส.", "login": "🛡️ เข้าสู่ระบบ", "user": "ชื่อวิศวกร", "key": "รหัสผ่าน", "nav_db": "📊 Dashboard AI", "nav_lib": "📚 คลังข้อมูลวัสดุ", "nav_cfp": "🌱 วิเคราะห์คาร์บอน", "nav_expert": "🧠 ปรึกษาปัญหาผลิต"},
    "EN": {"title": "SUT Bio-Material Intelligence Hub", "login": "🛡️ Secure Login", "user": "Engineer Name", "key": "Security Key", "nav_db": "📊 AI Dashboard", "nav_lib": "📚 Materials Library", "nav_cfp": "🌱 Carbon Hub", "nav_expert": "🧠 Troubleshooting"}
}

# --- 3. DATABASE & AI ENGINE ---
MATERIALS_DB = {
    "PLA": {"Full": "Polylactic Acid", "CFP": 1.58, "Pros": "High strength, Clear", "Cons": "Brittle"},
    "PBS": {"Full": "Polybutylene Succinate", "CFP": 1.85, "Pros": "Tough, Flexible", "Cons": "High cost"}
}

@st.cache_resource
def get_ai_engine():
    # ข้อมูล DOE จำลอง
    np.random.seed(42)
    m_ids, g_ids, pcs, ts_vals = [], [], [], []
    for m in [0, 1]:
        for g in [0, 1, 2]:
            for p in [0, 10, 20, 30, 40, 50]:
                m_ids.append(m); g_ids.append(g); pcs.append(p)
                ts_vals.append((62 if m == 0 else 40) - (p * 0.5) + np.random.normal(0, 1))
    X = pd.DataFrame({'M': m_ids, 'G': g_ids, 'P': pcs})
    model = RandomForestRegressor(n_estimators=100).fit(X, ts_vals)
    return model

# --- 4. MAIN APP LOGIC ---
def main():
    lang = st.sidebar.radio("🌐 Language / ภาษา", ["TH", "EN"], horizontal=True)
    t = LANG[lang]

    if 'auth' not in st.session_state: st.session_state.auth = False

    if not st.session_state.auth:
        st.title(t["login"])
        with st.form("login"):
            name = st.text_input(t["user"])
            pwd = st.text_input(t["key"], type="password")
            if st.form_submit_button("Authenticate"):
                if pwd == "SUT2026": 
                    st.session_state.auth = True
                    st.session_state.user = name
                    st.rerun()
    else:
        st.sidebar.title(f"👤 {st.session_state.user}")
        menu = st.sidebar.radio("Navigation", [t["nav_db"], t["nav_lib"], t["nav_cfp"], t["nav_expert"]])
        
        if menu == t["nav_db"]:
            st.title(t["nav_db"])
            col1, col2 = st.columns([1, 2])
            with col1:
                m = st.selectbox("Matrix", ["PLA", "PBS"])
                p = st.slider("Filler (%)", 0, 50, 15)
            with col2:
                model = get_ai_engine()
                pred = model.predict([[0 if m=="PLA" else 1, 0, p]])[0]
                st.metric("Tensile Strength", f"{pred:.2f} MPa")
                
                fig = go.Figure(go.Scatterpolar(r=[pred, 70, 40], theta=['Strength', 'Process', 'Cost'], fill='toself'))
                st.plotly_chart(fig)
        
        elif menu == t["nav_lib"]:
            st.title(t["nav_lib"])
            sel = st.selectbox("Select", ["PLA", "PBS"])
            st.json(MATERIALS_DB[sel])

        elif menu == t["nav_cfp"]:
            st.title(t["nav_cfp"])
            w = st.number_input("Weight (kg)", 1.0, 1000.0, 10.0)
            st.metric("Total CO2e", f"{w * 1.58:.2f} kg")

        elif menu == t["nav_expert"]:
            st.title(t["nav_expert"])
            prob = st.selectbox("Problem", ["Burn Marks", "Warpage"])
            st.error("Solution: Increase cooling time or adjust melt temp.")

        if st.sidebar.button("Logout"):
            st.session_state.auth = False
            st.rerun()

if __name__ == "__main__":
    main()
