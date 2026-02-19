import requests, random, time, threading, os, re
from flask import Flask, render_template_string, request
from waitress import serve

app = Flask(__name__)

# --- GLOBAL DATA ---
data = {
    "hits": 0,
    "clicks": 0,
    "proxies": 0,
    "current_url": "https://newswirhbot.blogspot.com/",
    "keyword": "High CPC Insurance",
    "country": "us",
    "logs": ["👻 History Spoofing ACTIVE. Bot is now a 'High-Intent' shopper."]
}

# --- HISTORY TRACE DATABASE ---
SPOOFED_HISTORY = [
    "https://www.amazon.com/dp/B0CHX2F5QT",
    "https://www.ebay.com/b/Apple-iPhone/9355/bn_319677",
    "https://www.forbes.com/advisor/insurance/car-insurance-quotes/",
    "https://www.booking.com/searchresults.html",
    "https://www.walmart.com/search?q=laptop"
]

DEVICES = [
    {"ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X)", "mem": "8", "plat": "iPhone"},
    {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0", "mem": "16", "plat": "Win32"}
]

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>ALI ABBAS | STEALTH GHOST</title>
    <style>
        body { background: #000205; color: #00ffcc; font-family: 'Courier New', monospace; padding: 20px; text-align: center; }
        .card { border: 1px solid #00ffcc; background: rgba(0, 40, 40, 0.8); padding: 15px; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 0 20px #00ffcc44; }
        .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .stat { font-size: 30px; font-weight: bold; color: white; }
        input, select, button { background: #001a1a; color: #00ffcc; border: 1px solid #00ffcc; padding: 10px; border-radius: 5px; margin: 5px; }
        button { background: #00ffcc; color: black; font-weight: bold; cursor: pointer; border: none; }
        .log-box { text-align: left; font-size: 11px; color: #00ff88; height: 160px; overflow: hidden; }
        .ghost-mode { color: #ff0055; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; }
    </style>
    <script>setInterval(() => { location.reload(); }, 10000);</script>
</head>
<body>
    <h1>⚡ ALI ABBAS GHOST COMMANDER ⚡</h1>
    <p class="ghost-mode">[ STATUS: HISTORY SPOOFING & HIGH-INTENT ACTIVE ]</p>
    
    <div class="card">
        <form action="/update" method="post">
            <input type="text" name="url" style="width: 30%;" placeholder="Target Link..." required>
            <input type="text" name="kw" style="width: 20%;" placeholder="SEO Keyword..." required>
            <select name="country">
                <option value="us">🇺🇸 USA (High Intent)</option>
                <option value="gb">🇬🇧 UK</option>
                <option value="ca">🇨🇦 Canada</option>
            </select>
            <button type="submit">DEPLOY GHOST TRAFFIC</button>
        </form>
    </div>

    <div class="stat-grid">
        <div class="card"><h3>VISITS</h3><div class="stat">{{hits}}</div></div>
        <div class="card" style="border-color:#ff0055;"><h3>REVENUE CLICKS</h3><div class="stat" style="color:#ff0055;">{{clicks}}</div></div>
        <div class="card"><h3>ACTIVE IPs</h3><div class="stat">{{proxies}}</div></div>
    </div>

    <div class="card">
        <h3>LIVE GHOST LOGS</h3>
        <div class="log-box">
            {% for log in logs %} <div>> {{log}}</div> {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_UI, hits=data["hits"], clicks=data["clicks"], proxies=data["proxies"], kw=data["keyword"], country=data["country"], logs=data["logs"][-12:])

@app.route('/update', methods=['POST'])
def update():
    data["current_url"] = request.form.get('url')
    data["keyword"] = request.form.get('kw')
    data["country"] = request.form.get('country')
    data["logs"].append(f"👻 GHOST RE-DEPLOYED: Targeting {data['country'].upper()}")
    return '<script>window.location.href="/";</script>'

def ghost_engine():
    proxy_list = []
    while True:
        try:
            country_param = f"&country={data['country']}"
            api_url = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&ssl=all&anonymity=elite{country_param}"
            
            if not proxy_list or len(proxy_list) < 5:
                r = requests.get(api_url, timeout=15)
                proxy_list = list(set(re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)))
                data["proxies"] = len(proxy_list)

            if proxy_list:
                proxy = random.choice(proxy_list)
                device = random.choice(DEVICES)
                
                # --- HISTORY SPOOFING LOGIC ---
                # Pehle kisi bari site ka referer dikhana, phir Google ka
                fake_prev_site = random.choice(SPOOFED_HISTORY)
                google_search = f"https://www.google.com/search?q={data['keyword'].replace(' ', '+')}"
                
                headers = {
                    "User-Agent": device["ua"],
                    "Referer": google_search,
                    "Cookie": f"visitor_id={random.randint(1000,9999)}; original_referer={fake_prev_site}",
                    "X-Forwarded-For": proxy.split(':')[0],
                    "Device-Memory": device["mem"]
                }
                
                # Visit Website
                res = requests.get(data["current_url"], headers=headers, proxies={"http":f"http://{proxy}"}, timeout=12)
                if res.status_code == 200:
                    data["hits"] += 1
                    
                    # 10% CTR with high-intent delay
                    if random.random() < 0.10:
                        time.sleep(random.randint(12, 25)) # Simulation of reading ads
                        data["clicks"] += 1
                        data["logs"].append(f"💰 PAID CLICK: [{device['plat']}] History: {fake_prev_site.split('/')[2]}")
                    else:
                        data["logs"].append(f"👤 GHOST VISIT: {proxy[:10]} | Intent: Active")
        except:
            pass
        time.sleep(random.randint(2, 4))

if __name__ == "__main__":
    threading.Thread(target=ghost_engine, daemon=True).start()
    serve(app, host='0.0.0.0', port=8000, threads=12)
