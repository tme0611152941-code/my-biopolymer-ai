import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# --- การตั้งค่าหน้าจอ ---
st.set_page_config(page_title="SUT Bioplast AI", layout="wide")

# --- ส่วนจัดการสถานะ (Login) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- ฟังก์ชันโหลดข้อมูลและ Train AI ---
@st.cache_data
def train_ai():
    # โหลดไฟล์ (ในการใช้งานจริงใช้ pd.read_csv('polymer_data.csv'))
    # จำลองข้อมูลเพื่อทดสอบระบบทันที
    data = {
        'Matrix': ['PLA', 'PLA', 'PLA', 'PLA', 'PBS', 'PBS'],
        'Filler_Type': ['Rice_Husk', 'Rice_Husk', 'Cassava', 'Cassava', 'Sugarcane', 'Sugarcane'],
        'Filler_Group': ['Natural_Fiber', 'Natural_Fiber', 'Starch_Based', 'Starch_Based', 'Natural_Fiber', 'Natural_Fiber'],
        'Filler_Percent': [10, 20, 10, 20, 15, 25],
        'Tensile': [52, 45, 48, 42, 35, 30],
        'Impact': [3.8, 4.2, 3.6, 3.9, 5.5, 6.2]
    }
    df = pd.DataFrame(data)
    
    # Train AI โดยใช้ Group เป็นตัวช่วย (กรณีเจอวัสดุใหม่)
    # แปลงตัวหนังสือเป็นตัวเลข (Encoding)
    df['Matrix_ID'] = df['Matrix'].factorize()[0]
    df['Group_ID'] = df['Filler_Group'].factorize()[0]
    
    model_ts = RandomForestRegressor(n_estimators=100).fit(df[['Matrix_ID', 'Group_ID', 'Filler_Percent']], df['Tensile'])
    model_im = RandomForestRegressor(n_estimators=100).fit(df[['Matrix_ID', 'Group_ID', 'Filler_Percent']], df['Impact'])
    
    return model_ts, model_im, df

model_ts, model_im, raw_df = train_ai()

# --- หน้าจอ Login ---
if not st.session_state['logged_in']:
    st.title("🌱 ระบบลงทะเบียนงานวิจัย Biopolymer")
    user = st.text_input("ชื่อนักศึกษา/นักวิจัย")
    if st.button("เข้าสู่ระบบเพื่อเริ่มผสมวัสดุ"):
        if user:
            st.session_state['logged_in'] = True
            st.session_state['user'] = user
            st.rerun()
else:
    # --- หน้าจอหลัก (Main App) ---
    st.sidebar.title(f"ผู้ใช้งาน: {st.session_state['user']}")
    menu = st.sidebar.radio("เมนู", ["ผสมวัสดุ & AI", "ข้อมูลทางเทคนิค"])

    if menu == "ผสมวัสดุ & AI":
        st.header("🧪 ระบบจำลองการผสมวัสดุคอมโพสิต")
        
        col1, col2 = st.columns(2)
        with col1:
            m_select = st.selectbox("เลือก Matrix", ["PLA", "PBS"])
            f_select = st.selectbox("เลือกสารเติมแต่ง (Filler)", ["Rice_Husk", "Cassava", "Sugarcane", "วัสดุใหม่ (Unknown)"])
        
        with col2:
            # กรณีเลือกวัสดุใหม่ ให้ระบุกลุ่มเพื่อความแม่นยำของ AI
            if f_select == "วัสดุใหม่ (Unknown)":
                f_group = st.selectbox("วัสดุใหม่ของคุณจัดอยู่ในกลุ่มใด?", ["Natural_Fiber", "Starch_Based"])
                st.warning("⚠️ AI จะวิเคราะห์โดยเทียบเคียงจากสมบัติของกลุ่มวัสดุที่คุณเลือก")
            else:
                f_group = raw_df[raw_df['Filler_Type'] == f_select]['Filler_Group'].values[0]
            
            f_percent = st.slider("ปริมาณการผสม (%)", 0, 50, 10)

        # ประมวลผล AI
        m_id = 0 if m_select == "PLA" else 1
        g_id = 0 if f_group == "Natural_Fiber" else 1
        
        res_ts = model_ts.predict([[m_id, g_id, f_percent]])[0]
        res_im = model_im.predict([[m_id, g_id, f_percent]])[0]

        st.divider()
        res_col1, res_col2 = st.columns(2)
        res_col1.metric("คาดการณ์ Tensile Strength", f"{res_ts:.2f} MPa")
        res_col2.metric("คาดการณ์ Impact Strength", f"{res_im:.2f} kJ/m²")
        
        # ก้างปลาวิเคราะห์ปัญหา
        with st.expander("🔍 วิเคราะห์ปัญหาที่เป็นไปได้ (Root Cause Analysis)"):
            if f_percent > 30:
                st.error("ปัญหา: การกระจายตัวต่ำ (Poor Dispersion) และความหนืดสูง")
            else:
                st.success("สถานะ: สูตรผสมมีความเป็นไปได้สูงในการขึ้นรูป")

---

### 🟢 ขั้นตอนที่ 3: ทำให้เป็นแอปออนไลน์ (Deploy)

1.  **ไฟล์ `requirements.txt`:** สร้างไฟล์นี้ใน GitHub ใส่แค่:
    ```text
    streamlit
    pandas
    scikit-learn
    numpy
    ```
2.  **อัปโหลดขึ้น GitHub:** เอาไฟล์ `app.py` และ `requirements.txt` ขึ้นไป (ทำเหมือนเดิมที่คุณเพิ่งแก้ผ่าน)
3.  **Deploy:** ไปที่หน้า Streamlit Cloud แล้วกด Deploy ใหม่จาก Repository นั้น

---

### 💎 สิ่งที่คุณจะได้ในเวอร์ชันนี้:
1.  **Registration:** เก็บชื่อคนใช้งานก่อนเริ่ม (โชว์พาวเวอร์เรื่องการเก็บ Data)
2.  **Selection System:** เลือกคู่ผสมได้เป็นระบบ
3.  **AI Generalization:** ถ้าเลือก "วัสดุใหม่" AI จะไม่เอ๋อ แต่มันจะถามหา "กลุ่มวัสดุ" (Filler Group) เพื่อเอาไปเทียบเคียงกับข้อมูลที่มีอยู่ (นี่คือจุดที่โชว์ว่า AI ของคุณฉลาดแบบวิศวกร)



**ลองเอาโค้ดนี้ไปรันใน Thonny ดูก่อนครับ!** ถ้าหน้าตาผ่านและระบบทำงานตามที่คุณต้องการแล้ว ค่อยอัปโหลดขึ้น GitHub เพื่อปิดจบโปรเจกต์ครับ มีจุดไหนอยากให้ปรับชื่อ หรือเพิ่มโลโก้ มทส. ตรงไหนบอกได้เลย!
