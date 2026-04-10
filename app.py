import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# --- 1. การตั้งค่าหน้าจอ (Configuration) ---
st.set_page_config(page_title="SUT Bioplast AI Expert", page_icon="🌱", layout="wide")

# --- 2. ฟังก์ชันโหลดข้อมูลและ Train AI ---
@st.cache_data
def load_and_train():
    # ข้อมูลจำลองที่ครอบคลุมทุกหัวข้อทางวิศวกรรม
    data = {
        'Matrix': ['PLA', 'PLA', 'PLA', 'PLA', 'PBS', 'PBS', 'PBS', 'PBS'],
        'Filler_Group': ['Natural_Fiber', 'Natural_Fiber', 'Starch_Based', 'Starch_Based', 
                        'Natural_Fiber', 'Natural_Fiber', 'Starch_Based', 'Starch_Based'],
        'Filler_Percent': [0, 10, 20, 30, 0, 15, 25, 35],
        'Tensile': [62, 54, 46, 38, 40, 34, 29, 24],
        'Elongation': [4.2, 3.1, 2.5, 1.8, 15.0, 9.2, 6.5, 4.0],
        'Modulus': [3.5, 3.8, 4.2, 4.6, 0.6, 1.1, 1.5, 1.9],
        'Impact': [3.4, 3.8, 4.1, 4.4, 6.8, 7.5, 8.0, 8.3]
    }
    df = pd.DataFrame(data)
    
    # แปลงหมวดหมู่เป็นตัวเลขเพื่อ Train AI
    df['Matrix_ID'] = df['Matrix'].factorize()[0]
    df['Group_ID'] = df['Filler_Group'].factorize()[0]
    
    X = df[['Matrix_ID', 'Group_ID', 'Filler_Percent']]
    
    # สร้าง Model แยกตามสมบัติ
    m_ts = RandomForestRegressor(n_estimators=100).fit(X, df['Tensile'])
    m_el = RandomForestRegressor(n_estimators=100).fit(X, df['Elongation'])
    m_mo = RandomForestRegressor(n_estimators=100).fit(X, df['Modulus'])
    m_im = RandomForestRegressor(n_estimators=100).fit(X, df['Impact'])
    
    return m_ts, m_el, m_mo, m_im

# โหลดโมเดล
model_ts, model_el, model_mo, model_im = load_and_train()

# --- 3. ส่วนจัดการสถานะการเข้าใช้งาน (Login) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🌱 SUT Bioplastic AI Expert System")
    st.subheader("ระบบพยากรณ์และแนะนำสูตรผสมพอลิเมอร์คอมโพสิต")
    
    with st.container():
        name = st.text_input("ชื่อ-นามสกุล ผู้ใช้งาน")
        unit = st.text_input("รหัสนักศึกษา / หน่วยงานวิจัย")
        if st.button("เข้าสู่ระบบ (Login)"):
            if name and unit:
                st.session_state['logged_in'] = True
                st.session_state['user'] = name
                st.rerun()
            else:
                st.error("กรุณากรอกข้อมูลให้ครบถ้วน")
else:
    # --- 4. ส่วนหน้าแอปหลัก (Main Application) ---
    st.sidebar.image("https://www.sut.ac.th/2012/images/logo_sut_en.png", width=100)
    st.sidebar.title(f"ผู้ใช้งาน: {st.session_state['user']}")
    
    if st.sidebar.button("Log out"):
        st.session_state['logged_in'] = False
        st.rerun()

    # --- ส่วนรับข้อมูล (Input) ---
    st.sidebar.divider()
    st.sidebar.header("🛠 ปรับตั้งค่าสูตรผสม")
    
    m_choice = st.sidebar.selectbox("1. เลือก Matrix", ["PLA", "PBS"])
    f_choice = st.sidebar.selectbox("2. เลือก Filler", ["Rice Husk", "Cassava", "Sugarcane", "วัสดุใหม่ (Unknown)"])
    
    # กรณีวัสดุใหม่ ให้ระบุกลุ่มเพื่อ AI วิเคราะห์เทียบเคียง
    if f_choice == "วัสดุใหม่ (Unknown)":
        f_group = st.sidebar.radio("กลุ่มวัสดุใหม่นี้คือ?", ["Natural_Fiber", "Starch_Based"])
    else:
        # กำหนดกลุ่มตามชนิด Filler
        f_group = "Natural_Fiber" if f_choice in ["Rice Husk", "Sugarcane"] else "Starch_Based"
    
    f_pc = st.sidebar.slider("3. ปริมาณการผสม (%)", 0, 50, 15)
    
    # --- ส่วนคัดกรองการขึ้นรูป ---
    st.sidebar.divider()
    method = st.sidebar.selectbox("4. วิธีการขึ้นรูปหลัก", ["Injection Molding", "Extrusion", "3D Printing"])
    target = st.sidebar.selectbox("5. เป้าหมายการใช้งาน", ["General Purpose", "High Strength", "High Toughness"])

    # --- 5. การประมวลผล AI (Processing) ---
    m_id = 0 if m_choice == "PLA" else 1
    g_id = 0 if f_group == "Natural_Fiber" else 1
    
    p_ts = model_ts.predict([[m_id, g_id, f_pc]])[0]
    p_el = model_el.predict([[m_id, g_id, f_pc]])[0]
    p_mo = model_mo.predict([[m_id, g_id, f_pc]])[0]
    p_im = model_im.predict([[m_id, g_id, f_pc]])[0]

    # --- 6. ส่วนแสดงผล (Output Dashboard) ---
    st.title("📊 ผลการพยากรณ์สมบัติวัสดุ")
    st.info(f"สูตรผสม: **{m_choice}** ผสมกับ **{f_choice}** ({f_group}) ที่สัดส่วน **{f_pc}%**")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tensile Strength", f"{p_ts:.1f} MPa")
    c2.metric("Elongation at Break", f"{p_el:.1f} %")
    c3.metric("Young's Modulus", f"{p_mo:.1f} GPa")
    c4.metric("Impact Strength", f"{p_im:.1f} kJ/m²")

    st.divider()

    # --- 7. ระบบแนะนำอัจฉริยะ (Smart Advisory) ---
    st.header("💡 วิเคราะห์และคำแนะนำทางวิศวกรรม")
    
    col_adv1, col_adv2 = st.columns(2)
    
    with col_adv1:
        st.subheader("⚙️ การขึ้นรูป (Processing)")
        if method == "Injection Molding" and f_pc > 30:
            st.warning(f"**คำเตือน:** ปริมาณ Filler สูงเกินไปสำหรับการฉีด ({method}) อาจทำให้ความหนืดสูงและผิวชิ้นงานไม่สวย")
            st.info("💡 **แนะนำ:** เพิ่มอุณหภูมิที่ Nozzle 5-10°C และใช้ Back Pressure ต่ำ")
        elif method == "3D Printing" and f_pc > 20:
            st.error("**ระวัง:** Filler อาจอุดตันหัวฉีดขนาดเล็ก แนะนำให้ใช้หัวฉีด 0.6 mm ขึ้นไป")
        else:
            st.success(f"✅ สภาวะนี้เหมาะสมกับการขึ้นรูปด้วย {method}")

    with col_adv2:
        st.subheader("🎯 ความเหมาะสม (Application)")
        if target == "High Strength" and p_ts < 40:
            st.error(f"❌ **ไม่ผ่านเกณฑ์:** แรงดึงต่ำเกินไปสำหรับ {target}")
        elif target == "High Toughness" and p_el < 5:
            st.warning(f"⚠️ **ระวัง:** วัสดุอาจเปราะเกินไปสำหรับ {target}")
        else:
            st.success(f"✅ วัสดุนี้ตอบโจทย์เป้าหมาย {target}")

    # ส่วนก้างปลา (Fishbone Logic)
    with st.expander("🔍 วิเคราะห์สาเหตุปัญหา (Root Cause Analysis)"):
        st.write("**หากสมบัติไม่เป็นไปตามคาดการณ์ ให้ตรวจสอบ:**")
        st.markdown("""
        * **Material:** ความชื้นใน Filler (แนะนำให้อบที่ 80°C เป็นเวลา 4-6 ชม.)
        * **Machine:** แรงเฉือน (Shear) ในสกรูสูงเกินไปทำให้สายโซ่พอลิเมอร์ขาด
        * **Method:** การกระจายตัว (Dispersion) ไม่สม่ำเสมอ แนะนำให้ใช้ Twin-screw Extruder
        """)
