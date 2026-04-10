import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# --- 1. การตั้งค่าหน้าจอ ---
st.set_page_config(page_title="SUT Bio-Material Hub & AI", page_icon="🌍", layout="wide")

# --- 2. ฐานข้อมูลความรู้ (Data Sheet) ---
bio_info = {
    "PLA": {
        "Full Name": "Polylactic Acid",
        "Source": "Corn starch, Sugarcane",
        "Degradability": "Industrial Compostable",
        "Pros": "High stiffness, Clear, Easy to print/mold",
        "Cons": "Brittle, Low heat resistance (Tg ~55-60°C)",
        "CFP_Value": 1.5  # kg CO2e / kg material (Approx)
    },
    "PBS": {
        "Full Name": "Polybutylene Succinate",
        "Source": "Bio-based Succinic acid",
        "Degradability": "Soil & Home Compostable",
        "Pros": "High toughness, Heat resistance, Processable",
        "Cons": "Lower strength than PLA, Higher cost",
        "CFP_Value": 1.8  # kg CO2e / kg material (Approx)
    }
}

# พลาสติกทั่วไปเพื่อเปรียบเทียบ (Petroleum-based)
petro_cfp = {"PP": 2.0, "PE": 2.1, "PET": 2.3}

# --- 3. ฟังก์ชัน AI (เหมือนเดิมแต่ปรับปรุงข้อมูล) ---
@st.cache_data
def load_and_train():
    data = {
        'Matrix': ['PLA', 'PLA', 'PLA', 'PBS', 'PBS', 'PBS'],
        'Filler_Group': ['Natural_Fiber', 'Natural_Fiber', 'Starch_Based', 'Natural_Fiber', 'Natural_Fiber', 'Starch_Based'],
        'Filler_Percent': [0, 15, 30, 0, 15, 30],
        'Tensile': [62, 48, 38, 40, 32, 26],
        'Impact': [3.4, 4.0, 4.5, 6.8, 7.8, 8.2]
    }
    df = pd.DataFrame(data)
    df['Matrix_ID'] = df['Matrix'].factorize()[0]
    df['Group_ID'] = df['Filler_Group'].factorize()[0]
    X = df[['Matrix_ID', 'Group_ID', 'Filler_Percent']]
    m_ts = RandomForestRegressor().fit(X, df['Tensile'])
    m_im = RandomForestRegressor().fit(X, df['Impact'])
    return m_ts, m_im

m_ts, m_im = load_and_train()

# --- 4. ระบบจัดการ Login ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🌍 SUT Bio-Material Intelligence Hub")
    name = st.text_input("ชื่อ-นามสกุล")
    unit = st.text_input("หน่วยงาน")
    if st.button("เข้าสู่ระบบ"):
        st.session_state['logged_in'] = True
        st.session_state['user'] = name
        st.rerun()
else:
    # --- 5. หน้าแอปหลัก ---
    st.sidebar.title(f"ผู้ใช้งาน: {st.session_state['user']}")
    menu = st.sidebar.selectbox("เมนูหลัก", ["🏠 หน้าแรก & ฐานความรู้", "🤖 ทำนายสูตรผสม AI", "🌱 คำนวณ Carbon Footprint"])

    if menu == "🏠 หน้าแรก & ฐานความรู้":
        st.title("📚 Bio-Material Data Sheet")
        st.write("เลือกวัสดุเพื่อดูสมบัติพื้นฐานและข้อมูลทางเทคนิค")
        
        target_bio = st.selectbox("เลือกชนิดพอลิเมอร์ชีวภาพ", ["PLA", "PBS"])
        info = bio_info[target_bio]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**ชื่อเต็ม:** {info['Full Name']}")
            st.info(f"**ที่มา:** {info['Source']}")
            st.warning(f"**การย่อยสลาย:** {info['Degradability']}")
        with col2:
            st.write(f"✅ **ข้อดี:** {info['Pros']}")
            st.write(f"❌ **ข้อจำกัด:** {info['Cons']}")
        
        st.divider()
        st.subheader("📖 เกร็ดความรู้: Bio-based vs Biodegradable")
        st.write("วัสดุบางชนิดมาจากพืชแต่ไม่ย่อยสลาย (Bio-based) และบางชนิดมาจากน้ำมันแต่ย่อยสลายได้ (Biodegradable) โปรเจกต์นี้เราเน้นวัสดุที่ **มาจากพืชและย่อยสลายได้** เป็นหลักครับ")

    elif menu == "🤖 ทำนายสูตรผสม AI":
        st.title("🤖 AI Prediction System")
        m_select = st.sidebar.selectbox("Matrix", ["PLA", "PBS"])
        f_select = st.sidebar.selectbox("Filler", ["Rice Husk", "Cassava", "Sugarcane"])
        f_pc = st.sidebar.slider("ปริมาณผสม (%)", 0, 50, 15)
        
        m_id = 0 if m_select == "PLA" else 1
        g_id = 0 if f_select in ["Rice Husk", "Sugarcane"] else 1
        
        res_ts = m_ts.predict([[m_id, g_id, f_pc]])[0]
        res_im = m_im.predict([[m_id, g_id, f_pc]])[0]
        
        c1, c2 = st.columns(2)
        c1.metric("Predicted Tensile", f"{res_ts:.1f} MPa")
        c2.metric("Predicted Impact", f"{res_im:.1f} kJ/m²")

    elif menu == "🌱 คำนวณ Carbon Footprint":
        st.title("🌱 Carbon Footprint Calculator")
        st.write("เปรียบเทียบการปล่อยก๊าซเรือนกระจกของสูตรผสมปัจจุบันเทียบกับพลาสติกทั่วไป")
        
        weight = st.number_input("ปริมาณงานที่ผลิต (กิโลกรัม)", 1.0, 10000.0, 1.0)
        compare_to = st.selectbox("เปรียบเทียบกับพลาสติกทั่วไป", ["PP", "PE", "PET"])
        
        # คำนวณ CFP (ใช้ตัวเลขประมาณการต่อกิโลกรัม)
        bio_val = 1.5 if "PLA" in st.session_state.get('m_select', "PLA") else 1.8
        total_bio_cfp = weight * bio_val
        total_petro_cfp = weight * petro_cfp[compare_to]
        saving = total_petro_cfp - total_bio_cfp
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Carbon ของสูตรนี้", f"{total_bio_cfp:.2f} kgCO2e")
        col2.metric(f"Carbon ของ {compare_to}", f"{total_petro_cfp:.2f} kgCO2e")
        col3.metric("คาร์บอนที่ลดได้ (Saving)", f"{saving:.2f} kgCO2e", delta_color="normal")
        
        st.success(f"🌟 การใช้สูตรนี้แทน {compare_to} ช่วยลดคาร์บอนได้เทียบเท่ากับการปลูกต้นไม้ประมาณ {int(saving/10)} ต้น!")
