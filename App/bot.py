import requests, random, time, threading, os, re
from flask import Flask

app = Flask(__name__)

# --- GLOBAL DATA ---
TOTAL_HITS = 0
ACTIVE_IPS = 0
LAST_TARGET = "Awaiting Uplink..."

@app.route('/')
def cyber_ui():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>EPIC BOT | ALI ABBAS</title>
        <meta http-equiv="refresh" content="4">
        <style>
            body {{ background-color: #000b1a; color: #00e5ff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; overflow: hidden; }}
            .container {{ display: grid; grid-template-columns: 1fr 2fr 1fr; height: 100vh; padding: 20px; gap: 20px; }}
            
            /* Left & Right Panels */
            .panel {{ border: 1px solid #004d66; background: rgba(0, 20, 40, 0.8); padding: 15px; border-radius: 5px; box-shadow: inset 0 0 20px #00e5ff33; }}
            
            /* Center Map Section */
            .map-section {{ position: relative; border: 1px solid #00e5ff; border-radius: 10px; overflow: hidden; background: url('https://upload.wikimedia.org/wikipedia/commons/8/80/World_map_-%28_blue_dots_%29.svg') center center no-repeat; background-size: contain; }}
            
            /* Animations */
            .scan-line {{ position: absolute; width: 100%; height: 2px; background: rgba(0, 229, 255, 0.5); top: 0; animation: scan 4s linear infinite; }}
            @keyframes scan {{ from {{ top: 0; }} to {{ top: 100%; }} }}

            .ping {{ position: absolute; width: 10px; height: 10px; background: #00e5ff; border-radius: 50%; animation: pulse 2s infinite; }}
            @keyframes pulse {{ 0% {{ transform: scale(1); opacity: 1; }} 100% {{ transform: scale(5); opacity: 0; }} }}

            .stat-value {{ font-size: 2.5em; font-weight: bold; color: #fff; text-shadow: 0 0 10px #00e5ff; }}
            .header {{ text-align: center; grid-column: span 3; border-bottom: 2px solid #00e5ff; padding-bottom: 10px; letter-spacing: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚡ EPIC BOT WITH ALI ABBAS ⚡</h1>
            </div>

            <div class="panel">
                <h3>SYSTEM METRICS</h3>
                <p>Uptime: <span style="color:white">24:00:00</span></p>
                <div class="stat-value">{TOTAL_HITS}</div>
                <p>TOTAL HITS SUCCESS</p>
                <hr border-color="#004d66">
                <div class="stat-value">{ACTIVE_IPS}</div>
                <p>ACTIVE PROXIES</p>
            </div>

            <div class="map-section">
                <div class="scan-line"></div>
                <div class="ping" style="top:30%; left:20%;"></div>
                <div class="ping" style="top:50%; left:70%;"></div>
                <div class="ping" style="top:45%; left:45%;"></div>
                <div style="position:absolute; bottom:20px; width:100%; text-align:center; font-size:1.2em;">
                    TARGETING: <span style="color:white">{LAST_TARGET}</span>
                </div>
            </div>

            <div class="panel">
                <h3>NETWORK LOGS</h3>
                <ul style="list-style:none; padding:0; font-size:0.8em; line-height:2;">
                    <li>[OK] Request Sent to Blogger</li>
                    <li>[OK] Proxy Rotation Completed</li>
                    <li>[OK] User-Agent Spoofing: ACTIVE</li>
                    <li>[OK] SSL Handshake: SUCCESS</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

def run_bot():
    global TOTAL_HITS, ACTIVE_IPS, LAST_TARGET
    # Asli logic yahan (Pichla wala hunter logic)
    while True:
        # Simulation for UI Update (Yahan aapka asli traffic code chalega)
        ACTIVE_IPS = random.randint(1500, 5000)
        TOTAL_HITS += random.randint(1, 5)
        LAST_TARGET = "blogger.com/post/xyz..."
        time.sleep(3)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=8000)
