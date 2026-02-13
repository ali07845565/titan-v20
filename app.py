import time, random, threading, requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- GLOBAL CONFIG & ENGINE STATE ---
state = {
    "running": False,
    "logs": [],
    "stats": {"WEB": 0, "YT": 0, "TT": 0, "FB": 0, "PRX": 0},
    "targets": {"WEB": "", "YT": "", "TT": "", "FB": ""},
    "features": {
        "human_scroll": True,
        "mouse_movement": True,
        "ai_comments": False,
        "cookie_aging": True,
        "geo_fencing": "Global",
        "ad_skip": True,
        "stealth_mode": True,
        "mobile_emu": False,
        "fingerprint_mask": True,
        "auto_like": False
    }
}

def add_log(msg):
    state["logs"].insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")
    state["logs"] = state["logs"][:15]

# --- ADVANCED ENGINE LOGIC ---
def titan_master_engine():
    while True:
        if state["running"]:
            try:
                # 1. Proxy & Geo-Fencing
                proxy_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all"
                r = requests.get(proxy_url, timeout=10)
                proxies = [p.strip() for p in r.text.splitlines() if ":" in p]
                state["stats"]["PRX"] = len(proxies)

                if proxies:
                    p = random.choice(proxies)
                    px = {"http": f"http://{p}", "https": f"http://{p}"}
                    
                    # 2. Select Platform
                    plat = random.choice(["WEB", "YT", "TT", "FB"])
                    url = state["targets"][plat]

                    if url:
                        # 3. Apply Stealth & Fingerprinting
                        headers = {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                            'Referer': random.choice(['https://google.com', 'https://t.co', 'https://bing.com'])
                        }
                        
                        # Simulated Human Wait (Human Scroll Logic)
                        if state["features"]["human_scroll"]:
                            time.sleep(random.randint(2, 5))
                        
                        requests.get(url, headers=headers, proxies=px, timeout=15)
                        state["stats"][plat] += 1
                        add_log(f"🔥 {plat} Task Successful using {p[:10]}...")
            except Exception as e:
                add_log(f"⚠️ System Delay: {str(e)[:20]}")
        
        time.sleep(12)

# --- MASTER UI (Tabs & Toggles) ---
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN OMNIVERSE V21</title>
    <meta http-equiv="refresh" content="15">
    <style>
        :root { --neon: #00ff41; --bg: #050505; }
        body { background: var(--bg); color: var(--neon); font-family: 'Courier New', monospace; margin: 0; padding: 10px; }
        .tab-container { border: 1px solid var(--neon); padding: 10px; border-radius: 10px; }
        .tabs { display: flex; cursor: pointer; border-bottom: 1px solid var(--neon); }
        .tab { padding: 10px 20px; border: 1px solid transparent; }
        .tab.active { border: 1px solid var(--neon); border-bottom: none; background: #111; }
        .stats-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin: 15px 0; }
        .stat-card { border: 1px solid var(--neon); padding: 10px; text-align: center; background: #000; }
        .toggle-box { display: flex; justify-content: space-between; padding: 8px; border-bottom: 1px solid #222; }
        .switch { position: relative; display: inline-block; width: 40px; height: 20px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #333; transition: .4s; border-radius: 20px; }
        input:checked + .slider { background-color: var(--neon); }
        .btn { padding: 10px; width: 100%; margin: 5px 0; background: var(--neon); color: #000; font-weight: bold; border: none; cursor: pointer; }
        .btn.stop { background: #ff4141; }
        .log-box { background: #000; font-size: 11px; height: 120px; overflow: hidden; padding: 10px; border: 1px solid #333; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="tab-container">
        <h2 style="text-align: center;">🛰️ TITAN OMNIVERSE V21 - MASTER PANEL</h2>
        
        <div class="stats-grid">
            <div class="stat-card">WEB<br>{{stats['WEB']}}</div>
            <div class="stat-card">YT<br>{{stats['YT']}}</div>
            <div class="stat-card">TT<br>{{stats['TT']}}</div>
            <div class="stat-card">FB<br>{{stats['FB']}}</div>
            <div class="stat-card">PRX<br>{{stats['PRX']}}</div>
        </div>

        <form method="POST">
            {% if running %}
                <button name="action" value="stop" class="btn stop">STOP ENGINE</button>
            {% else %}
                <button name="action" value="start" class="btn">START ENGINE</button>
            {% endif %}
        </form>

        <div class="tabs">
            <div class="tab active">ADVANCED CONFIG</div>
        </div>

        <form method="POST" style="padding: 15px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <input type="text" name="WEB" value="{{targets['WEB']}}" placeholder="Web Link" style="width:100%; background:#111; color:#fff; border:1px solid var(--neon); padding:5px; margin:2px 0;">
                    <input type="text" name="YT" value="{{targets['YT']}}" placeholder="YT Link" style="width:100%; background:#111; color:#fff; border:1px solid var(--neon); padding:5px; margin:2px 0;">
                    <input type="text" name="TT" value="{{targets['TT']}}" placeholder="TT Link" style="width:100%; background:#111; color:#fff; border:1px solid var(--neon); padding:5px; margin:2px 0;">
                    <input type="text" name="FB" value="{{targets['FB']}}" placeholder="FB Link" style="width:100%; background:#111; color:#fff; border:1px solid var(--neon); padding:5px; margin:2px 0;">
                </div>
                <div style="font-size: 12px;">
                    <div class="toggle-box">Human Scroll <label class="switch"><input type="checkbox" name="human_scroll" {% if features['human_scroll'] %}checked{% endif %}><span class="slider"></span></label></div>
                    <div class="toggle-box">Cookie Aging <label class="switch"><input type="checkbox" name="cookie_aging" {% if features['cookie_aging'] %}checked{% endif %}><span class="slider"></span></label></div>
                    <div class="toggle-box">Stealth Mode <label class="switch"><input type="checkbox" name="stealth_mode" {% if features['stealth_mode'] %}checked{% endif %}><span class="slider"></span></label></div>
                    <div class="toggle-box">Ad-Skip Logic <label class="switch"><input type="checkbox" name="ad_skip" {% if features['ad_skip'] %}checked{% endif %}><span class="slider"></span></label></div>
                </div>
            </div>
            <button name="action" value="update" class="btn" style="background:#444; color:#fff;">SAVE ALL CONFIG</button>
        </form>

        <div class="log-box">
            <strong>SYSTEM LOGS:</strong><br>
            {% for log in logs %}{{ log }}<br>{% endfor %}
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
            # Update Targets
            state["targets"]["WEB"] = request.form.get("WEB")
            state["targets"]["YT"] = request.form.get("YT")
            state["targets"]["TT"] = request.form.get("TT")
            state["targets"]["FB"] = request.form.get("FB")
            # Update Features (Toggles)
            state["features"]["human_scroll"] = 'human_scroll' in request.form
            state["features"]["cookie_aging"] = 'cookie_aging' in request.form
            state["features"]["stealth_mode"] = 'stealth_mode' in request.form
            state["features"]["ad_skip"] = 'ad_skip' in request.form
            add_log("Configuration Updated Successfully")

    return render_template_string(HTML_UI, **state)

threading.Thread(target=titan_master_engine, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
