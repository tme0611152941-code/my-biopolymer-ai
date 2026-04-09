import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px

# --- การตั้งค่าเบื้องต้น ---
st.set_page_config(page_title="SUT Polymer AI", layout="wide")
st.title("🤖 SUT Bioplastic AI Predictor")

# --- ส่วนการโหลดข้อมูล ---
@st.cache_data
def get_data():
    # ในการใช้งานจริง ให้ใช้: return pd.read_csv('polymer_data.csv')
    # ตอนนี้ผมสร้างข้อมูลจำลองขึ้นมาให้ในตัวโค้ดก่อน
    data = []
    for i in range(100):
        f_pc = i % 51  # 0-50%
        temp = 170 + (i % 30) # 170-200C
        ts = 60 - (f_pc * 0.7) + (temp * 0.05) + np.random.normal(0, 2)
        im = 3.5 + (f_pc * 0.04) - (temp * 0.01) + np.random.normal(0, 0.2)
        data.append([f_pc, temp, ts, im])
    return pd.DataFrame(data, columns=['Filler_Percent', 'Temp', 'Tensile', 'Impact'])

import numpy as np
df = get_data()

# --- ส่วนฝึกสอน AI (Training) ---
X = df[['Filler_Percent', 'Temp']]
y_ts = df['Tensile']
y_im = df['Impact']

model_ts = RandomForestRegressor(n_estimators=100).fit(X, y_ts)
model_im = RandomForestRegressor(n_estimators=100).fit(X, y_im)

# --- ส่วนหน้าตาแอป (UI) ---
st.sidebar.header("🛠 ปรับสูตรผสม (Input)")
f_input = st.sidebar.slider("ปริมาณ Bio-Filler (%)", 0, 50, 15)
t_input = st.sidebar.slider("อุณหภูมิ (°C)", 160, 210, 180)

# ทำนายผล
p_ts = model_ts.predict([[f_input, t_input]])[0]
p_im = model_im.predict([[f_input, t_input]])[0]

# แสดงผลแบบ Dashboard
st.subheader("📊 ผลการวิเคราะห์จาก AI")
c1, c2 = st.columns(2)
c1.metric("Tensile Strength (MPa)", f"{p_ts:.2f}")
c2.metric("Impact Strength (kJ/m²)", f"{p_im:.2f}")

# กราฟความสัมพันธ์
st.subheader("📈 กราฟแสดงแนวโน้มสมบัติวัสดุ")
fig = px.scatter(df, x="Filler_Percent", y="Tensile", color="Temp", title="ความสัมพันธ์ของสัดส่วนผสมต่อแรงดึง")
st.plotly_chart(fig)

# ส่วนการวิเคราะห์ปัญหา (Logic-Based)
st.info("💡 **คำแนะนำทางวิศวกรรม:**")
if f_input > 25:
    st.warning("พบความเสี่ยง: ความหนืด (Viscosity) อาจสูงเกินไปจนฉีดงานยาก แนะนำให้ตรวจสอบค่า MFR")
else:
    st.success("สูตรนี้มีแนวโน้มที่จะฉีดงานได้ง่ายและผิวชิ้นงานสม่ำเสมอ")