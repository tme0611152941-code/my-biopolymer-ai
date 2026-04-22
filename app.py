import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

# --- การตั้งค่าหน้าจอและ UI ---
st.set_page_config(page_title="SUT Bio-Material Hub", page_icon="🧬", layout="wide")

# Custom CSS เพื่อความพรีเมียม (Neon Metric)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #00e5ff; /* Cyan Neon */
    }
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนจัดการสถานะการเข้าใช้งาน (Login) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- หน้าจอลงทะเบียน / Login ---
if not st.session_state.auth:
    st.title("🛡️ Secure Access: SUT Bio-Material Intelligence Hub")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("### ยินดีต้อนรับสู่ระบบจำลองปัญญาประดิษฐ์เพื่อการออกแบบพอลิเมอร์ชีวภาพ")
        # 👉 แปะรูปทีมวิศวกรต้นฉบับตรงนี้ (ต้องชื่อ team_photo.jpg และอยู่ใน Folder เดียวกัน)
        try:
            st.image("team_photo.jpg", use_container_width=True)
            st.caption("ทีมผู้นำทางด้านไบโอ-วิศวกรรม มทส. (v4.5 Apex Design)")
        except:
            st.error("❌ ไม่พบไฟล์รูปภาพ 'team_photo.jpg' กรุณาตรวจสอบตำแหน่งไฟล์")

    with col2:
        with st.form("registration_form"):
            st.write("### ลงทะเบียนเข้าใช้งานระบบ")
            user_in = st.text_input("ชื่อนักวิจัย (Engineer Name)")
            id_in = st.text_input("หน่วยงาน (Institute)")
            pwd = st.text_input("รหัสความปลอดภัย (Security Key)", type="password")
            if st.form_submit_button("Authenticate / ลงทะเบียน"):
                if pwd == "SUT2026": # รหัสผ่านลับ
                    st.session_state.auth = True
                    st.session_state.user = user_in
                    st.rerun()
                else:
                    st.error("❌ Key Incorrect / กรุณาใส่รหัสที่ถูกต้อง")

else:
    # --- 6. AI ENGINE (ฝัง DOE Data มาในโค้ด) ---
    @st.cache_resource
    def get_ai():
        np.random.seed(42)
        m_ids, g_ids, pcs, ts_vals, el_vals = [], [], [], [], []
        # จำลองข้อมูล DOE (Design of Experiments) จาก Paper จริง
        for m in [0, 1]: # PLA, PBS
            for g in [0, 1, 2]: # Natural, Starch, Mineral
                for p in [0, 10, 20, 30, 40, 50]:
                    m_ids.append(m); g_ids.append(g); pcs.append(p)
                    # Logic วิศวกรรม: PLA (0) แข็งกว่า PBS (1) | Natural (0) มักลด Tensile
                    base = 62.5 if m == 0 else 40.0
                    ts_vals.append(base - (p * 0.5) + np.random.normal(0, 1.5))
                    el_vals.append((4.2 if m == 0 else 150) * (1 - p/120))
        
        X = pd.DataFrame({'M': m_ids, 'G': g_ids, 'P': pcs})
        m_ts = RandomForestRegressor(n_estimators=100).fit(X, ts_vals)
        m_el = RandomForestRegressor(n_estimators=100).fit(X, el_vals)
        return m_ts, m_el

    m_ts, m_el = get_ai()

    # --- หน้า Dashboard AI (หลัง Login) ---
    st.sidebar.title(f"👤 {st.session_state.user}")
    
    # เมนูเลือกภาษา
    lang = st.sidebar.radio("🌐 Language / ภาษา", ["ไทย", "English"], horizontal=True)
    t_nav = {"ไทย": "🤖 แผงควบคุม AI", "English": "🤖 AI Dashboard"}
    menu = st.sidebar.radio("Navigation", [t_nav[lang], "LCA Analysis", "Expert Advisory"])
    
    if st.sidebar.button("Log out"):
        st.session_state.auth = False
        st.rerun()

    if menu == t_nav[lang]:
        st.title("🤖 Bio-Material Intelligence Dashboard v4.5")
        # (โค้ดส่วน Dashboard เหมือนเดิม...)
