import requests, random, time, threading, os, re
from flask import Flask

# --- BRANDING ---
APP_NAME = "EPIC BOT WITH ALI ABBAS"
VERSION = "V7.0 - WEB UI EDITION"

app = Flask(__name__)

# --- GLOBAL DATA ---
GLOBAL_PROXIES = []
TOTAL_HITS = 0
CURRENT_LOCATION = "Searching..."

@app.route('/')
def dashboard():
    # Ye HTML code aapke link par VIP look dikhayega
    return f"""
    <html>
    <head>
        <title>{APP_NAME}</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{ background-color: #0a0a0a; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding: 50px; }}
            .box {{ border: 2px solid #00ff00; padding: 20px; display: inline-block; background: rgba(0, 255, 0, 0.05); box-shadow: 0 0 20px #00ff00; }}
            h1 {{ text-shadow: 0 0 10px #00ff00; }}
            .stats {{ font-size: 24px; margin: 20px 0; }}
            .map {{ color: #0088ff; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🚀 {APP_NAME}</h1>
            <p>System Status: <span style="color:white">RUNNING (VIP MODE)</span></p>
            <hr>
            <div class="stats">
                📈 Total Successful Hits: <b>{TOTAL_HITS}</b><br>
                📡 Active Proxy Pool: <b>{len(GLOBAL_PROXIES)} IPs</b><br>
                🌍 Current Target: <span class="map">{CURRENT_LOCATION}</span>
            </div>
            <p style="color: #555;">Auto-refreshing every 5 seconds...</p>
        </div>
    </body>
    </html>
    """

def fish_proxies():
    global GLOBAL_PROXIES
    sources = ["https://api.proxyscrape.com/v2/?request=getproxies&protocol=http", "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"]
    while True:
        temp = []
        for s in sources:
            try:
                r = requests.get(s, timeout=10)
                temp.extend(re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text))
            except: continue
        if temp: GLOBAL_PROXIES = list(set(temp))
        time.sleep(600)

def worker():
    global TOTAL_HITS, CURRENT_LOCATION
    targets = ["https://newswirhbot.blogspot.com/"]
    while True:
        if not GLOBAL_PROXIES:
            time.sleep(5); continue
        proxy = random.choice(GLOBAL_PROXIES)
        try:
            res = requests.get(random.choice(targets), proxies={"http":f"http://{proxy}"}, timeout=10)
            if res.status_code == 200:
                TOTAL_HITS += 1
                CURRENT_LOCATION = f"IP: {proxy[:12]}... (USA/UK)"
        except: pass
        time.sleep(2)

if __name__ == "__main__":
    threading.Thread(target=fish_proxies, daemon=True).start()
    for _ in range(10): threading.Thread(target=worker, daemon=True).start()
    # Flask ko 8000 par chalana taake link work kare
    app.run(host='0.0.0.0', port=8000)
