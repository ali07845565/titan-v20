import requests, random, time, threading, os, re
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- GLOBAL SETTINGS ---
data = {
    "hits": 0,
    "proxies": 0,
    "current_url": "https://newswirhbot.blogspot.com/",
    "logs": ["System Booted...", "Awaiting Command..."]
}

# --- FUTURISTIC UI HTML ---
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>ALI ABBAS | COMMAND CENTER</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { background: #000b1a; color: #00e5ff; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; }
        .header { width: 100%; border-bottom: 2px solid #00e5ff; text-align: center; padding: 10px; box-shadow: 0 0 15px #00e5ff; }
        .main-grid { display: grid; grid-template-columns: 1fr 2fr 1fr; width: 95%; gap: 20px; margin-top: 20px; }
        .panel { border: 1px solid #00e5ff; background: rgba(0, 20, 40, 0.9); padding: 15px; border-radius: 10px; box-shadow: inset 0 0 10px #00e5ff; }
        .map-bg { background: url('https://upload.wikimedia.org/wikipedia/commons/8/80/World_map_-%28_blue_dots_%29.svg') center no-repeat; background-size: contain; height: 300px; position: relative; }
        input[type="text"] { width: 80%; padding: 10px; background: transparent; border: 1px solid #00e5ff; color: white; border-radius: 5px; }
        button { padding: 10px 20px; background: #00e5ff; color: black; border: none; font-weight: bold; cursor: pointer; }
        .stat { font-size: 2.5em; color: white; text-shadow: 0 0 10px #00e5ff; }
        .log-list { font-size: 0.8em; color: #00ff88; list-style: none; padding: 0; }
    </style>
</head>
<body>
    <div class="header"><h1>⚡ EPIC BOT WITH ALI ABBAS v9.0 ⚡</h1></div>
    
    <div class="panel" style="width: 90%; margin-top: 20px;">
        <form action="/update_link" method="post">
            <input type="text" name="new_url" placeholder="Paste Custom Link (YouTube, FB, TikTok)...">
            <button type="submit">START TRAFFIC</button>
        </form>
        <p>Currently Targeting: <span style="color:white">{{url}}</span></p>
    </div>

    <div class="main-grid">
        <div class="panel">
            <h3>METRICS</h3>
            <div class="stat">{{hits}}</div><p>REAL SUCCESS HITS</p>
            <div class="stat">{{proxies}}</div><p>ACTIVE PROXIES</p>
        </div>

        <div class="panel">
            <div class="map-bg">
                <div style="position:absolute; top:20%; left:30%; width:10px; height:10px; background:red; border-radius:50%; box-shadow:0 0 10px red;"></div>
            </div>
            <h3 style="text-align:center;">GLOBAL ATTACK MAP</h3>
        </div>

        <div class="panel">
            <h3>NETWORK LOGS</h3>
            <ul class="log-list">
                {% for log in logs %} <li>> {{log}}</li> {% endfor %}
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_UI, hits=data["hits"], proxies=data["proxies"], url=data["current_url"], logs=data["logs"][-10:])

@app.route('/update_link', methods=['POST'])
def update_link():
    new_url = request.form.get('new_url')
    if new_url:
        data["current_url"] = new_url
        data["logs"].append(f"Target Changed to: {new_url}")
    return """<script>window.location.href='/';</script>"""

def traffic_engine():
    # Asli Hunter Logic yahan hai
    proxy_list = []
    while True:
        try:
            if not proxy_list:
                r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000", timeout=10)
                proxy_list = list(set(re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)))
                data["proxies"] = len(proxy_list)

            proxy = random.choice(proxy_list)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0"}
            
            # Asli Request
            res = requests.get(data["current_url"], headers=headers, proxies={"http": f"http://{proxy}"}, timeout=8)
            if res.status_code == 200:
                data["hits"] += 1
                data["logs"].append(f"SUCCESS: Hit via {proxy[:10]}...")
        except:
            pass
        time.sleep(random.randint(1, 3))

if __name__ == "__main__":
    threading.Thread(target=traffic_engine, daemon=True).start()
    app.run(host='0.0.0.0', port=8000)
