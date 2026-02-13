import os
import time
import random
import threading
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Global Stats
stats = {"WEB": 0, "YT": 0, "TT": 0, "FB": 0, "PRX": 0}

# Default Targets (Aap dashboard se badal sakte hain)
targets = {
    "WEB": "https://www.effectivegatecpm.com/jwqbgif9n7?key=840b62a568849f92cdfe1f2173ce072b",
    "YT": "https://youtube.com/watch?v=example",
    "TT": "https://tiktok.com/@user/video/id",
    "FB": "https://facebook.com/watch/?v=id"
}

# --- ADVANCED ENGINE ---
def titan_engine():
    while True:
        try:
            # 1. Fetch Elite Proxies
            r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite", timeout=10)
            proxies = [p.strip() for p in r.text.splitlines() if ":" in p]
            stats["PRX"] = len(proxies)
            
            if proxies:
                p = random.choice(proxies)
                proxy_dict = {"http": f"http://{p}", "https": f"http://{p}"}
                
                # Advance Device Fingerprinting
                ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.{random.randint(1000,9999)} Safari/537.36"
                
                # Platform selection
                plat = random.choice(["WEB", "YT", "TT", "FB"])
                url = targets[plat]
                
                if url and url.startswith("http"):
                    # Heavy Headers for Monetization Safety
                    headers = {
                        'User-Agent': ua,
                        'Referer': random.choice(['https://google.com/', 'https://twitter.com/', 'https://bing.com/']),
                        'Accept-Language': 'en-US,en;q=0.9'
                    }
                    requests.get(url, headers=headers, proxies=proxy_dict, timeout=12)
                    stats[plat] += 1
        except:
            pass
        time.sleep(15) # Safe interval to prevent pausing

# --- ADVANCED UI ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITAN OMNIVERSE V20</title>
    <meta http-equiv="refresh" content="45">
    <style>
        body { background-color: #0a0a0a; color: #00ff00; font-family: 'Courier New', monospace; margin: 0; padding: 20px; text-align: center; }
        .container { border: 2px solid #00ff00; padding: 20px; border-radius: 10px; max-width: 800px; margin: auto; box-shadow: 0 0 15px #00ff00; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 30px; }
        .card { border: 1px solid #333; padding: 15px; background: #111; border-radius: 5px; }
        .card h2 { margin: 5px 0; font-size: 24px; color: #fff; }
        input { width: 90%; padding: 10px; margin: 10px 0; background: #222; border: 1px solid #00ff00; color: #fff; border-radius: 5px; }
        button { padding: 12px 30px; background: #00ff00; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; }
        button:hover { background: #008800; }
        .status { color: #ffcc00; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌌 TITAN OMNIVERSE PRO V20</h1>
        <p>Advanced Global Traffic & Monetization System</p>
        
        <div class="grid">
            <div class="card"><p>WEB</p><h2>{{stats['WEB']}}</h2></div>
            <div class="card"><p>YOUTUBE</p><h2>{{stats['YT']}}</h2></div>
            <div class="card"><p>TIKTOK</p><h2>{{stats['TT']}}</h2></div>
            <div class="card"><p>FACEBOOK</p><h2>{{stats['FB']}}</h2></div>
            <div class="card"><p>PROXIES</p><h2>{{stats['PRX']}}</h2></div>
        </div>

        <form method="POST">
            <input type="text" name="WEB" value="{{targets['WEB']}}" placeholder="Website/Ad Link">
            <input type="text" name="YT" value="{{targets['YT']}}" placeholder="YouTube Video Link">
            <input type="text" name="TT" value="{{targets['TT']}}" placeholder="TikTok Video Link">
            <input type="text" name="FB" value="{{targets['FB']}}" placeholder="Facebook Video Link">
            <br><br>
            <button type="submit">UPDATE & RUN ENGINE</button>
        </form>
        <p class="status">System Status: 24/7 ACTIVE | Auto-Refreshes every 45s</p>
    </div>
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
    app.run(host='0.0.0.0', port=7860)
