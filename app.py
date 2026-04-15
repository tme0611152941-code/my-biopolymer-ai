import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้ากระดาษ Streamlit
st.set_page_config(page_title="The Copycat Challenge", layout="centered")

# ส่วนของ HTML/JavaScript เกม
game_html = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;500&display=swap');
        body {
            font-family: 'Kanit', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 90vh;
            margin: 0;
            color: white;
            text-align: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            width: 100%;
        }
        #display-area {
            height: 120px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 15px;
        }
        button {
            background: #ff4b2b;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.2rem;
            border-radius: 50px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="display-area">กดเริ่มเลย!</div>
        <button onclick="startGame()">สุ่มท่าทาง!</button>
    </div>

    <script>
        const poses = [
    "🐒 ลิง (เกาหัวเกาสีข้าง)",
    "🐘 ช้าง (เอาแขนทำงวง)",
    "🐰 กระต่าย (ชูสองนิ้วเป็นหู)",
    "🐱 แมว (มือกวักข้างหู)",
    "🐶 สุนัข (หูตกแลบลิ้น)",
    "🦁 สิงโต (กางเล็บคำราม)",
    "🐍 งู (ฉกมือพุ่งไปข้างหน้า)",
    "🦒 ยีราฟ (ชูแขนสุดตัวเป็นคอยาว)",
    "🐦 นก (กางปีกบิน)",
    "🐔 ไก่ (มือกุมเป็นหงอนบนหัว)",
    "🦆 เป็ด (ทำปากเป็ดแล้วส่ายตูด)",
    "🐧 เพนกวิน (แนบแขนข้างลำตัวเดินเตาะแตะ)",
    "🐸 กบ (ทำท่ากระโดดหยองๆ)",
    "🐊 จระเข้ (เอาแขนงับกัน)",
    "🦀 ปู (ทำนิ้วเป็นก้ามหนีบๆ)",
    "🦞 กุ้ง (ตัวงอเอามือแตะหลัง)",
    "🐎 ม้า (ควบม้า ฮี้ๆ)",
    "🐂 วัว (เอานิ้วชี้เป็นเขาข้างหัว)",
    "🦇 ค้างคาว (นอนห้อยหัว/หุบปีก)",
    "🦍 คิงคอง (ทุบอกตัวเอง)"
];
    function startGame() {
            const display = document.getElementById('display-area');
            let count = 3;
            const timer = setInterval(() => {
                if (count > 0) {
                    display.innerText = count;
                    count--;
                } else {
                    clearInterval(timer);
                    display.innerText = poses[Math.floor(Math.random() * poses.length)];
                }
            }, 800);
        }
    </script>
</body>
</html>
"""

# แสดงชื่อหัวข้อใน Streamlit
st.title("🎭 The Copycat Challenge")
st.write("ท้าดวลท่าทาง! ใครทำไม่เหมือนเพื่อน...เตรียมตัวโดน!")

# ฝังโค้ด HTML เข้าไปในหน้าเว็บ
components.html(game_html, height=500)

# แถมท้ายด้วยปุ่มกลับหน้าหลักหรือข้อมูลอื่นๆ ได้ตามใจชอบ
st.info("💡 ทริค: เปิดผ่านมือถือแล้วถือไว้ในมือตอนเล่น จะสะดวกกว่านะ!")
