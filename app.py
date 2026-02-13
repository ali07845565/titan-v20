import time, random, threading, os
from flask import Flask, request, render_template_string
from playwright.sync_api import sync_playwright
import google.generativeai as genai

# --- CONFIGURATION ---
APP_NAME = "Traffic Bot with Ali Abbas"
GEMINI_KEY = "AIzaSyBs3-vbv7XF_8uCGcKRjQxEQVBCVYCh1G0"  # Aapka Key

# Gemini Setup
try:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-pro')
    ai_active = True
except:
    ai_active = False

app = Flask(__name__)

# --- GLOBAL STATE ---
state = {
    "running": False,
    "stats": {"VIEWS": 0, "CLICKS": 0, "ERRORS": 0, "PROXIES": 0},
    "targets": {"URL": "", "DURATION": "30"},
    "logs": ["System Initialized... Waiting for command."],
    "proxy_list": []
}

def add_log(msg):
    t = time.strftime("%H:%M:%S")
    state["logs"].insert(0, f"[{t}] {msg}")
    state["logs"] = state["logs"][:15]

# --- PROXY ENGINE (MULTI-SOURCE) ---
def fetch_proxies():
    sources = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
    ]
    temp_proxies = []
    add_log("🔄 Fetching Fresh Proxies...")
    
    for url in sources:
        try:
            import requests
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                lines = r.text.splitlines()
                temp_proxies.extend([p.strip() for p in lines if ":" in p])
        except:
            pass
    
    state["proxy_list"] = list(set(temp_proxies)) # Remove duplicates
    state["stats"]["PROXIES"] = len(state["proxy_list"])
    add_log(f"✅ Loaded {len(state['proxy_list'])} Active Proxies")

# --- AI BEHAVIOR ENGINE ---
def get_ai_action():
    if not ai_active: return "Watching Video silently..."
    try:
        response = model.generate_content("Write a very short, positive 3-word comment about a video.")
        return response.text.strip()
    except:
        return "Nice video!"

# --- MAIN TRAFFIC BOT ENGINE ---
def run_bot():
    while True:
        if state["running"]:
            if len(state["proxy_list"]) < 5:
                fetch_proxies()
            
            if not state["targets"]["URL"]:
                add_log("⚠️ No URL Set! Pausing...")
                state["running"] = False
                continue

            try:
                proxy_ip = random.choice(state["proxy_list"])
                target = state["targets"]["URL"]
                duration = int(state["targets"]["DURATION"])

                with sync_playwright() as p:
                    # Browser Launch (Headless=True for server, but logic mimics real user)
                    browser = p.chromium.launch(
                        headless=True,
                        args=['--no-sandbox', '--disable-setuid-sandbox']
                    )
                    
                    # Real User Fingerprint
                    context = browser.new_context(
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
                        viewport={'width': 1366, 'height': 768},
                        device_scale_factor=1
                    )
                    
                    page = context.new_page()
                    
                    # AI Log
                    action = get_ai_action()
                    add_log(f"🤖 AI Action: {action}")
                    
                    # Navigation
                    add_log(f"🚀 Visiting via {proxy_ip[:12]}...")
                    page.goto(target, timeout=60000)
                    
                    # Human Behavior (Mouse Move to play video)
                    page.mouse.move(random.randint(100, 500), random.randint(100, 500))
                    
                    # Try clicking play button if Youtube/Video
                    try:
                        page.click("video", timeout=2000)
                        page.click(".ytp-play-button", timeout=2000)
                    except:
                        pass

                    # Stay for Duration
                    time.sleep(duration)
                    
                    state["stats"]["VIEWS"] += 1
                    add_log("✅ View Counted Successfully!")
                    browser.close()

            except Exception as e:
                state["stats"]["ERRORS"] += 1
                # Remove bad proxy
                if proxy_ip in state["proxy_list"]:
                    state["proxy_list"].remove(proxy_ip)
        
        time.sleep(5)

# --- DIGENZY STYLE UI (HTML/CSS) ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Traffic Bot with Ali Abbas</title>
    <meta http-equiv="refresh" content="5">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #5e72e4;
            --secondary: #f4f7fe;
            --text-dark: #2d3748;
            --text-light: #a0aec0;
            --white: #ffffff;
            --success: #2dce89;
            --danger: #f5365c;
        }
        body { margin: 0; font-family: 'Segoe UI', sans-serif; background: var(--secondary); display: flex; height: 100vh; overflow: hidden; }
        
        /* SIDEBAR */
        .sidebar { width: 250px; background: var(--white); padding: 20px; display: flex; flex-direction: column; box-shadow: 2px 0 10px rgba(0,0,0,0.05); }
        .brand { font-size: 20px; font-weight: bold; color: var(--primary); margin-bottom: 40px; display: flex; align-items: center; gap: 10px; }
        .menu-item { padding: 12px 15px; color: var(--text-light); border-radius: 10px; margin-bottom: 10px; cursor: pointer; transition: 0.3s; display: flex; align-items: center; gap: 10px; font-weight: 500; }
        .menu-item.active { background: var(--primary); color: var(--white); box-shadow: 0 4px 6px rgba(94, 114, 228, 0.3); }
        .menu-item:hover:not(.active) { background: #f6f9fc; color: var(--primary); }
        
        /* MAIN CONTENT */
        .main { flex: 1; padding: 30px; overflow-y: auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .user-profile { display: flex; align-items: center; gap: 10px; background: var(--white); padding: 8px 15px; border-radius: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
        
        /* STATS CARDS */
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .card { background: var(--white); padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); display: flex; justify-content: space-between; align-items: center; }
        .card-info h3 { margin: 0; color: var(--text-light); font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
        .card-info h1 { margin: 5px 0 0; color: var(--text-dark); font-size: 24px; }
        .icon-box { width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; color: white; }
        .bg-blue { background: linear-gradient(45deg, #5e72e4, #825ee4); }
        .bg-orange { background: linear-gradient(45deg, #fb6340, #fbb140); }
        .bg-green { background: linear-gradient(45deg, #2dce89, #2dcecc); }
        .bg-red { background: linear-gradient(45deg, #f5365c, #f56036); }

        /* CONTROL PANEL */
        .panel { background: var(--white); padding: 25px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #e2e8f0; border-radius: 8px; outline: none; background: #f7fafc; }
        input:focus { border-color: var(--primary); }
        
        .btn-group { display: flex; gap: 15px; margin-top: 15px; }
        button { flex: 1; padding: 12px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; color: white; transition: 0.3s; }
        .btn-start { background: var(--success); }
        .btn-stop { background: var(--danger); }
        .btn-update { background: var(--primary); }

        /* LOGS */
        .logs-box { background: #172b4d; color: #ced4da; padding: 20px; border-radius: 15px; height: 200px; overflow: hidden; font-family: monospace; font-size: 13px; }
        .log-entry { padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .log-entry:first-child { color: var(--success); font-weight: bold; }

    </style>
</head>
<body>
    <div class="sidebar">
        <div class="brand">
            <i class="fas fa-robot"></i> Ali Abbas Bot
        </div>
        <div class="menu-item active"><i class="fas fa-home"></i> Dashboard</div>
        <div class="menu-item"><i class="fas fa-chart-line"></i> Analytics</div>
        <div class="menu-item"><i class="fas fa-cog"></i> Settings</div>
    </div>

    <div class="main">
        <div class="header">
            <div>
                <h2 style="margin:0; color:var(--text-dark);">Dashboard Overview</h2>
                <span style="color:var(--text-light); font-size:14px;">Gemini AI: <span style="color:var(--success);">Active</span></span>
            </div>
            <div class="user-profile">
                <img src="https://ui-avatars.com/api/?name=Ali+Abbas&background=random" style="width:30px; border-radius:50%;">
                <span style="font-weight:600; font-size:14px;">Admin</span>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <div class="card-info"><h3>Total Views</h3><h1>{{stats['VIEWS']}}</h1></div>
                <div class="icon-box bg-blue"><i class="fas fa-eye"></i></div>
            </div>
            <div class="card">
                <div class="card-info"><h3>Proxies Live</h3><h1>{{stats['PROXIES']}}</h1></div>
                <div class="icon-box bg-green"><i class="fas fa-network-wired"></i></div>
            </div>
            <div class="card">
                <div class="card-info"><h3>Failed</h3><h1>{{stats['ERRORS']}}</h1></div>
                <div class="icon-box bg-red"><i class="fas fa-times-circle"></i></div>
            </div>
            <div class="card">
                <div class="card-info"><h3>Status</h3><h1>{% if running %}ON{% else %}OFF{% endif %}</h1></div>
                <div class="icon-box bg-orange"><i class="fas fa-power-off"></i></div>
            </div>
        </div>

        <div class="panel">
            <h3 style="margin-top:0;">Target Configuration</h3>
            <form method="POST">
                <div style="display:grid; grid-template-columns: 3fr 1fr; gap:15px;">
                    <input type="text" name="url" value="{{targets['URL']}}" placeholder="Enter YouTube/Website Link Here...">
                    <input type="number" name="duration" value="{{targets['DURATION']}}" placeholder="Seconds (e.g. 60)">
                </div>
                
                <div class="btn-group">
                    {% if running %}
                        <button name="action" value="stop" class="btn-stop"><i class="fas fa-pause"></i> STOP ENGINE</button>
                    {% else %}
                        <button name="action" value="start" class="btn-start"><i class="fas fa-rocket"></i> START ENGINE</button>
                    {% endif %}
                    <button name="action" value="update" class="btn-update"><i class="fas fa-save"></i> UPDATE TARGETS</button>
                </div>
            </form>
        </div>

        <div class="logs-box">
            <div style="margin-bottom:10px; font-weight:bold; color:white;">LIVE ACTIVITY LOGS (Gemini Enhanced)</div>
            {% for log in logs %}
                <div class="log-entry">{{ log }}</div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form.get("action")
        if action == "start":
            state["running"] = True
            add_log("Engine Started. Initializing AI...")
        elif action == "stop":
            state["running"] = False
            add_log("Engine Stopped.")
        elif action == "update":
            state["targets"]["URL"] = request.form.get("url")
            state["targets"]["DURATION"] = request.form.get("duration")
            add_log("Target Updated Successfully.")
    
    return render_template_string(HTML_UI, stats=state["stats"], targets=state["targets"], running=state["running"], logs=state["logs"])

# Background Thread Start
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
