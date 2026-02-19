import requests, random, time, threading, os, re
from flask import Flask, render_template_string, request
from waitress import serve

app = Flask(__name__)

# --- GLOBAL DATA ---
data = {
    "hits": 0,
    "proxies": 0,
    "current_url": "https://newswirhbot.blogspot.com/",
    "source": "https://www.google.com/",
    "logs": ["⚡ System Ready. Ali Abbas Command Center Active."]
}

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>ALI ABBAS | COMMAND CENTER</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { background: #000814; color: #00f2ff; font-family: 'Courier New', monospace; margin: 0; padding: 20px; }
        .grid { display: grid; grid-template-columns: 1fr 2fr 1fr; gap: 15px; }
        .card { border: 1px solid #00f2ff; background: rgba(0, 30, 60, 0.7); padding: 15px; border-radius: 8px; box-shadow: 0 0 10px #00f2ff55; }
        .map-box { background: url('https://upload.wikimedia.org/wikipedia/commons/8/80/World_map_-%28_blue_dots_%29.svg') no-repeat center; background-size: contain; height: 350px; position: relative; border: 1px solid #00f2ff; }
        input, select, button { background: #001a33; color: #00f2ff; border: 1px solid #00f2ff; padding: 10px; margin: 5px 0; border-radius: 4px; width: 100%; }
        button { background: #00f2ff; color: #000; font-weight: bold; cursor: pointer; }
        .stat { font-size: 30px; font-weight: bold; text-align: center; color: #fff; }
        .log-box { height: 200px; overflow-y: hidden; font-size: 11px; color: #00ff88; }
        .radar { position: absolute; width: 100%; height: 2px; background: rgba(0,242,255,0.3); animation: move 4s linear infinite; }
        @keyframes move { from { top: 0; } to { top: 100%; } }
    </style>
</head>
<body>
    <h1 style="text-align:center; text-shadow: 0 0 10px #00f2ff;">⚡ ALI ABBAS COMMAND CENTER ⚡</h1>
    
    <div class="card" style="margin-bottom:15px;">
        <form action="/update" method="post" style="display: flex; gap: 10px;">
            <input type="text" name="url" placeholder="Enter Target Link (YouTube, FB, etc.)" required>
            <select name="source">
                <option value="https://www.google.com/">Google Search</option>
                <option value="https://www.facebook.com/">Facebook Mobile</option>
                <option value="https://t.co/">Twitter / X</option>
                <option value="https://l.instagram.com/">Instagram</option>
                <option value="https://wa.me/">WhatsApp Chat</option>
            </select>
            <button type="submit" style="width:200px;">DEPLOY ATTACK</button>
        </form>
        <p style="font-size:12px;">TARGETING: <span style="color:white">{{url}}</span> | SOURCE: <span style="color:white">{{source}}</span></p>
    </div>

    <div class="grid">
        <div class="card">
            <h3>REAL-TIME METRICS</h3>
            <div class="stat">{{hits}}</div><p align="center">SUCCESS HITS</p>
            <div class="stat">{{proxies}}</div><p align="center">LIVE PROXIES</p>
        </div>

        <div class="map-box">
            <div class="radar"></div>
            <div style="position:absolute; top:40%; left:50%; width:8px; height:8px; background:red; border-radius:50%; box-shadow:0 0 10px red;"></div>
        </div>

        <div class="card">
            <h3>SYSTEM LOGS</h3>
            <div class="log-box">
                {% for log in logs %} <div>> {{log}}</div> {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_UI, hits=data["hits"], proxies=data["proxies"], url=data["current_url"], source=data["source"], logs=data["logs"][-12:])

@app.route('/update', methods=['POST'])
def update():
    data["current_url"] = request.form.get('url')
    data["source"] = request.form.get('source')
    data["logs"].append(f"RE-TARGETED: {data['current_url'][:30]}...")
    return """<script>window.location.href='/';</script>"""

def traffic_engine():
    proxy_list = []
    while True:
        try:
            if not proxy_list or len(proxy_list) < 10:
                r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000", timeout=10)
                proxy_list = list(set(re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)))
                data["proxies"] = len(proxy_list)

            proxy = random.choice(proxy_list)
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
                "Referer": data["source"]
            }
            
            with requests.get(data["current_url"], headers=headers, proxies={"http":f"http://{proxy}", "https":f"http://{proxy}"}, timeout=10) as res:
                if res.status_code == 200:
                    data["hits"] += 1
                    data["logs"].append(f"SUCCESS: Hit via {proxy[:12]}")
        except:
            pass
        time.sleep(random.randint(1, 2))

if __name__ == "__main__":
    threading.Thread(target=traffic_engine, daemon=True).start()
    # Flask warning khatam karne ke liye Waitress use kiya
    print("🚀 Ali Abbas Server Starting on Port 8000...")
    serve(app, host='0.0.0.0', port=8000)
