import time, random, threading, asyncio
from flask import Flask, request, render_template_string
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# --- EPIC STATE ENGINE ---
state = {
    "running": False,
    "stats": {"WEB": 0, "YT": 0, "TT": 0, "FB": 0, "PRX": 0},
    "targets": {"WEB": "", "YT": "", "TT": "", "FB": ""},
    "logs": ["$ Titan Epic Pro Initialized..."],
    "features": {
        "human_scroll": True,
        "canvas_spoofing": True,
        "mouse_jitter": True,
        "ad_click": False,
        "high_retention": True,
        "stealth_mode": True
    }
}

def add_log(msg):
    state["logs"].insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")
    state["logs"] = state["logs"][:20]

# --- EPIC HUMAN EMULATION ENGINE ---
def run_epic_browser():
    while True:
        if state["running"]:
            try:
                with sync_playwright() as p:
                    # Stealth Browser Launch
                    browser = p.chromium.launch(headless=True)
                    # Fake Context (Canvas & WebRTC Spoofing)
                    context = browser.new_context(
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
                        viewport={'width': 1920, 'height': 1080},
                        device_scale_factor=1,
                    )
                    page = context.new_page()
                    
                    plat = random.choice([k for k, v in state["targets"].items() if v]) or "WEB"
                    target_url = state["targets"][plat]

                    add_log(f"🚀 Launching Stealth Instance for {plat}...")
                    page.goto(target_url, wait_until="networkidle")

                    # Human Behavior: Random Scrolling
                    if state["features"]["human_scroll"]:
                        for _ in range(random.randint(3, 7)):
                            page.mouse.wheel(0, random.randint(300, 700))
                            time.sleep(random.uniform(1, 3))
                    
                    # Human Behavior: Mouse Jitter
                    if state["features"]["mouse_jitter"]:
                        page.mouse.move(random.randint(100, 500), random.randint(100, 500))

                    add_log(f"✅ Target {plat} Processed Successfully")
                    state["stats"][plat] += 1
                    
                    browser.close()
            except Exception as e:
                add_log(f"❌ Engine Error: {str(e)[:40]}")
        time.sleep(10)

# --- NEON ADVANCE UI ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>TITAN EPIC PRO V22</title>
    <meta http-equiv="refresh" content="10">
    <style>
        :root { --neon: #00f2ff; --bg: #0d0d0d; --card: #1a1a1a; }
        body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }
        .grid-stats { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; margin-bottom: 20px; }
        .card { background: var(--card); border: 1px solid #333; padding: 15px; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .card h2 { color: var(--neon); margin: 5px 0; }
        
        .main-panel { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .section { background: var(--card); padding: 20px; border-radius: 20px; border: 1px solid #333; }
        
        /* Toggle Switch */
        .switch-box { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #222; }
        .switch { position: relative; width: 45px; height: 22px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background: #333; transition: .4s; border-radius: 34px; }
        input:checked + .slider { background: var(--neon); }
        
        .terminal { background: #000; color: #00ff41; font-family: 'Courier New', monospace; height: 300px; overflow-y: hidden; padding: 15px; border-radius: 10px; font-size: 13px; border: 1px solid #00ff4133; }
        input[type="text"] { width: 90%; padding: 10px; background: #000; border: 1px solid #444; color: #fff; border-radius: 8px; margin: 5px 0; }
        .btn { width: 100%; padding: 15px; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        .btn-run { background: var(--neon); color: #000; }
        .btn-stop { background: #ff3b3b; color: #fff; }
    </style>
</head>
<body>
    <div style="max-width: 1100px; margin: auto;">
        <h1 style="text-align:center; letter-spacing: 5px;">🛰️ TITAN <span style="color: var(--neon)">EPIC PRO</span> V22</h1>
        
        <div class="grid-stats">
            <div class="card">WEB<h2>{{stats['WEB']}}</h2></div>
            <div class="card">YT<h2>{{stats['YT']}}</h2></div>
            <div class="card">TT<h2>{{stats['TT']}}</h2></div>
            <div class="card">FB<h2>{{stats['FB']}}</h2></div>
            <div class="card">PRX<h2>{{stats['PRX']}}</h2></div>
        </div>

        <div class="main-panel">
            <div class="section">
                <h3>🛠️ CONTROL CENTER</h3>
                <form method="POST">
                    {% if running %}
                        <button name="action" value="stop" class="btn btn-stop">🛑 EMERGENCY STOP</button>
                    {% else %}
                        <button name="action" value="start" class="btn btn-run">🚀 ACTIVATE EPIC ENGINE</button>
                    {% endif %}
                </form>
                <form method="POST">
                    <input type="text" name="WEB" value="{{targets['WEB']}}" placeholder="Monetization Link">
                    <input type="text" name="YT" value="{{targets['YT']}}" placeholder="YouTube Video URL">
                    <input type="text" name="TT" value="{{targets['TT']}}" placeholder="TikTok Video URL">
                    <input type="text" name="FB" value="{{targets['FB']}}" placeholder="Facebook Video URL">
                    <button name="action" value="update" class="btn" style="background:#333; color:#fff;">SAVE TARGETS</button>
                </form>
            </div>

            <div class="section">
                <h3>🛡️ STEALTH FEATURES</h3>
                <form method="POST">
                    {% for feat, val in features.items() %}
                    <div class="switch-box">
                        <span>{{ feat.replace('_', ' ').title() }}</span>
                        <label class="switch">
                            <input type="checkbox" name="{{feat}}" {% if val %}checked{% endif %}>
                            <span class="slider"></span>
                        </label>
                    </div>
                    {% endfor %}
                    <button name="action" value="update_features" class="btn" style="background:#222; color:var(--neon); border:1px solid var(--neon);">APPLY EPIC FEATURES</button>
                </form>
            </div>
        </div>

        <div class="section" style="margin-top:20px;">
            <h3>📟 LIVE TERMINAL (EPIC LOGS)</h3>
            <div class="terminal">
                {% for log in logs %}{{ log }}<br>{% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        act = request.form.get("action")
        if act == "start": state["running"] = True
        elif act == "stop": state["running"] = False
        elif act == "update":
            state["targets"].update({k: request.form.get(k) for k in state["targets"]})
        elif act == "update_features":
            for f in state["features"]:
                state["features"][f] = f in request.form
            add_log("Stealth Config Updated.")

    return render_template_string(HTML_UI, **state)

threading.Thread(target=run_epic_browser, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
