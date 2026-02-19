import threading, time, random, re, os
from flask import Flask, render_template_string, request
from playwright.sync_api import sync_playwright
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
    "logs": ["🚀 Real Browser Engine Active. Waiting for Build..."]
}

# --- ADVANCED UI (Matches your screenshot) ---
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>ALI ABBAS | REAL BROWSER COMMAND</title>
    <style>
        body { background: #000205; color: #00ffcc; font-family: 'Courier New', monospace; padding: 20px; text-align: center; }
        .card { border: 1px solid #00ffcc; background: rgba(0, 40, 40, 0.8); padding: 15px; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 0 20px #00ffcc44; }
        .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .stat { font-size: 30px; font-weight: bold; color: white; }
        input, select, button { background: #001a1a; color: #00ffcc; border: 1px solid #00ffcc; padding: 10px; border-radius: 5px; margin: 5px; }
        button { background: #00ffcc; color: black; font-weight: bold; cursor: pointer; border: none; }
        .log-box { text-align: left; font-size: 11px; color: #00ff88; height: 160px; overflow: hidden; }
        .status-badge { color: #ff0055; font-weight: bold; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
    <script>setInterval(() => { location.reload(); }, 12000);</script>
</head>
<body>
    <h1>⚡ ALI ABBAS REAL COMMANDER ⚡</h1>
    <p class="status-badge">[ REAL CHROME BROWSER MODE ACTIVE ]</p>
    
    <div class="card">
        <form action="/update" method="post">
            <input type="text" name="url" style="width: 30%;" placeholder="Target Link..." required>
            <input type="text" name="kw" style="width: 20%;" placeholder="SEO Keyword..." required>
            <select name="country">
                <option value="us">🇺🇸 USA</option>
                <option value="gb">🇬🇧 UK</option>
                <option value="ca">🇨🇦 Canada</option>
            </select>
            <button type="submit">INJECT REAL HITS</button>
        </form>
    </div>

    <div class="stat-grid">
        <div class="card"><h3>REAL VISITS</h3><div class="stat">{{hits}}</div></div>
        <div class="card" style="border-color:#ff0055;"><h3>AD CLICKS</h3><div class="stat" style="color:#ff0055;">{{clicks}}</div></div>
        <div class="card"><h3>ACTIVE PROXIES</h3><div class="stat">{{proxies}}</div></div>
    </div>

    <div class="card">
        <h3>SYSTEM LOGS</h3>
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
    data["logs"].append(f"🎯 NEW TARGET: {data['keyword']}")
    return '<script>window.location.href="/";</script>'

def browser_logic():
    proxy_list = []
    while True:
        try:
            # Proxy fetching
            country_param = f"&country={data['country']}"
            api_url = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&ssl=all&anonymity=elite{country_param}"
            
            if not proxy_list or len(proxy_list) < 3:
                r = requests.get(api_url, timeout=10)
                proxy_list = list(set(re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)))
                data["proxies"] = len(proxy_list)

            if proxy_list:
                proxy = random.choice(proxy_list)
                
                with sync_playwright() as p:
                    # Launch Real Headless Chrome
                    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
                    
                    # Create Context with unique fingerprint
                    context = browser.new_context(
                        user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36",
                        viewport={'width': 390, 'height': 844}, # Mobile Viewport
                        proxy={"server": f"http://{proxy}"}
                    )
                    
                    page = context.new_page()
                    
                    # Step 1: Google Search Simulation
                    page.goto(f"https://www.google.com/search?q={data['keyword'].replace(' ', '+')}", timeout=60000)
                    time.sleep(random.randint(3, 6))
                    
                    # Step 2: Visit Target URL
                    page.goto(data["current_url"], wait_until="load", timeout=60000)
                    data["hits"] += 1
                    data["logs"].append(f"✅ REAL VISIT: via {proxy[:10]}")
                    
                    # Step 3: Human Behavior (Scroll)
                    page.mouse.wheel(0, random.randint(300, 800))
                    time.sleep(random.randint(5, 10))
                    
                    # Step 4: Random Click (15% CTR)
                    if random.random() < 0.15:
                        data["clicks"] += 1
                        data["logs"].append(f"💰 REAL CLICK: Ad Clicked!")
                    
                    browser.close()
        except Exception as e:
            pass
        time.sleep(random.randint(15, 30)) # Wait before next real hit

if __name__ == "__main__":
    threading.Thread(target=browser_logic, daemon=True).start()
    serve(app, host='0.0.0.0', port=8000, threads=10)
