<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Copycat Challenge! 🎭</title>
    <style>
        body {
            font-family: 'Kanit', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
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
            width: 90%;
            max-width: 400px;
        }
        h1 { font-size: 1.8rem; margin-bottom: 20px; }
        #display-area {
            height: 150px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 15px;
            padding: 10px;
        }
        button {
            background: #ff4b2b;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.2rem;
            border-radius: 50px;
            cursor: pointer;
            transition: 0.3s;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
        }
        button:hover { transform: scale(1.05); background: #ff416c; }
        button:disabled { background: #888; cursor: not-allowed; }
        .instruction { font-size: 0.9rem; margin-top: 15px; opacity: 0.8; }
    </style>
</head>
<body>

<div class="container">
    <h1>🎭 ท่านี้...มีใครต่าง?</h1>
    <div id="display-area">กดเริ่มเลย!</div>
    <button id="btn-spin" onclick="startGame()">สุ่มท่าทาง!</button>
    <p class="instruction">นับ 1 2 3 แล้วโพสต์ท่าพร้อมกัน!<br>ใครไม่เหมือนเพื่อน = <b>โดน!</b></p>
</div>

<script>
    const poses = [
        "🦸‍♂️ ซูเปอร์แมน",
        "🕷️ สไปเดอร์แมน",
        "🌸 คิ้วท์เกิร์ล",
        "🥊 นักมวย",
        "💃 นางแบบจิกกล้อง",
        "🔫 สายลับ 007",
        "🧘‍♂️ นั่งสมาธิ",
        "🐵 ลิงจั๊กๆ",
        "🐱 แมวกวัก",
        "🤟 ไอเลิฟยู",
        "👮‍♂️ ตะเบ๊ะ!",
        "🧟‍♂️ ซอมบี้"
    ];

    function startGame() {
        const btn = document.getElementById('btn-spin');
        const display = document.getElementById('display-area');
        btn.disabled = true;

        let count = 3;
        display.style.color = "#ffeb3b";
        
        // เสียงนับ (จำลอง)
        const timer = setInterval(() => {
            if (count > 0) {
                display.innerText = count;
                count--;
            } else {
                clearInterval(timer);
                display.style.color = "white";
                const randomPose = poses[Math.floor(Math.random() * poses.length)];
                display.innerText = randomPose;
                btn.disabled = false;
            }
        }, 800);
    }
</script>

</body>
</html>
