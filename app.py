
import os
import time
import random
import threading
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Global Stats
stats = {"WEB": 0, "YT": 0, "TT": 0, "FB": 0, "PRX": 0}

# Default Targets
targets = {
    "WEB": "https://www.effectivegatecpm.com/jwqbgif9n7?key=840b62a568849f92cdfe1f2173ce072b",
    "YT": "https://www.youtube.com/watch?v=your_video_id",
    "TT": "https://www.tiktok.com/@user/video/id",
    "FB": "https://www.facebook.com/watch/?v=id"
}

# --- TITAN ENGINE ---
def titan_engine():
    while True:
        try:
            # Proxy Fetching
            r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite", timeout=10)
            proxies = [p.strip() for p in r.text.splitlines() if ":" in p]
            stats["PRX"] = len(proxies)
            
            if proxies:
                p = random.choice(proxies)
                proxy_dict = {"http": f"http://{p}", "https": f"http://{p}"}
                
                # Device Rotation Logic
                ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.{random.randint(1000,9999)} Safari/537.36"
                
                # Pick Platform
                plat = random.choice(["WEB", "YT", "TT", "FB"])
                url = targets[plat]
                
                if url and url.startswith("http"):
                    headers = {
                        'User-Agent': ua,
                        'Referer': random.choice(['https://google.com/', 'https://bing.com/', 'https://duckduckgo.com/']),
                        'Accept-Language': 'en-US,en;q=0.9'
                    }
                    requests.get(url, headers=headers, proxies=proxy_dict, timeout=12)
                    stats[plat] += 1
        except:
            pass
        time.sleep(15) # Safe gap for free tier stability

# --- MINIMAL UI ---
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>TITAN V20 PRO</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { background: #000; color: #0f0; font-family: monospace; text-align: center; padding: 20px; }
        .box { border: 1px solid #0f0; padding: 15px; display: inline-block; margin: 10px; min-width: 120px; }
        input { width: 80%; padding: 10px; margin: 10px 0; background: #111; border: 1px solid #0f0; color: #fff; }
        button { padding: 10px 20px; background: #0f0; color: #000; border: none; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h1>TITAN OMNIVERSE V20</h1>
    <div>
        <div class="box">WEB<br>{{stats['WEB']}}</div>
        <div class="box">YT<br>{{stats['YT']}}</div>
        <div class="box">TT<br>{{stats['TT']}}</div>
        <div class="box">FB<br>{{stats['FB']}}</div>
        <div class="box">PROXIES<br>{{stats['PRX']}}</div>
    </div>
    <hr>
    <form method="POST">
        <input type="text" name="WEB" value="{{targets['WEB']}}" placeholder="Web Link"><br>
        <input type="text" name="YT" value="{{targets['YT']}}" placeholder="YouTube Link"><br>
        <input type="text" name="TT" value="{{targets['TT']}}" placeholder="TikTok Link"><br>
        <input type="text" name="FB" value="{{targets['FB']}}" placeholder="Facebook Link"><br>
        <button type="submit">UPDATE TARGETS</button>
    </form>
    <p>Status: RUNNING | Port: 8000</p>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        targets["WEB"] = request.form.get("WEB")
        targets["YT"] = request.form.get("YT")
        targets["TT"] = request.form.get("TT")
        targets["FB"] = request.form.get("FB")
    return render_template_string(HTML_UI, stats=stats, targets=targets)

if __name__ == "__main__":
    threading.Thread(target=titan_engine, daemon=True).start()
    # Koyeb default port is 8000
    app.run(host='0.0.0.0', port=8000)
