import requests, random, time, threading, os, re

# --- BRANDING ---
APP_NAME = "EPIC BOT WITH ALI ABBAS"
VERSION = "V6.0 - PROXY HUNTER"

LINKS = [
    "https://newswirhbot.blogspot.com/2026/01/the-ultimate-2026-buying-guide-why.html?m=1",
    "https://newswirhbot.blogspot.com/2026/01/best-price-in-pakistan-2026-shop.html",
    "https://newswirhbot.blogspot.com/2026/01/electronics-accessories-on-asmveocom.html",
    "https://newswirhbot.blogspot.com/2026/01/Asmveo.com.html",
    "https://newswirhbot.blogspot.com/2026/02/discover-best-deals-on-asmveo.html",
    "https://youtu.be/K9ihEWJn4Go?si=SYn8IuvLw2cKfr4W"
]

KEYWORDS = ["Best Price Pakistan", "Asmveo Gadgets", "Ali Abbas Bot", "Tech Deals 2026"]

# --- 40K+ PROXY FISHING SOURCES ---
PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxyscan.io/download?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy.txt"
]

GLOBAL_PROXIES = []

def fish_proxies():
    global GLOBAL_PROXIES
    while True:
        temp_list = []
        print(f"\n[🎣 FISHING] Ali Abbas Hunter is searching for 40k+ proxies...")
        for source in PROXY_SOURCES:
            try:
                r = requests.get(source, timeout=15)
                if r.status_code == 200:
                    found = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
                    temp_list.extend(found)
            except: continue
        
        if temp_list:
            GLOBAL_PROXIES = list(set(temp_list))
            print(f"✅ SUCCESS: {len(GLOBAL_PROXIES)} Real IPs Hooked!")
        
        # Re-fish every 15 minutes to keep list fresh
        time.sleep(900)

def worker():
    while True:
        if not GLOBAL_PROXIES:
            time.sleep(5)
            continue
            
        proxy = random.choice(GLOBAL_PROXIES)
        target = random.choice(LINKS)
        kw = random.choice(KEYWORDS)
        
        headers = {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/{random.randint(100,122)}.0.0.0",
            "Referer": f"https://www.google.com/search?q={kw.replace(' ', '+')}",
            "X-Forwarded-For": proxy.split(':')[0]
        }
        
        try:
            proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            with requests.get(target, headers=headers, proxies=proxies, timeout=10) as r:
                if r.status_code == 200:
                    # Real-time dashboard output
                    print(f"🚀 [HIT] IP: {proxy[:15]} | {kw} | {target[-15:]}")
        except:
            if proxy in GLOBAL_PROXIES: GLOBAL_PROXIES.remove(proxy)
            continue
        time.sleep(random.randint(2, 5))

if __name__ == "__main__":
    os.system('clear')
    print("="*50)
    print(f"🛡️  {APP_NAME} UI - V6.0")
    print("="*50)
    
    # Start Fishing Thread
    threading.Thread(target=fish_proxies, daemon=True).start()
    
    # Start 20 Traffic Workers
    for _ in range(20):
        threading.Thread(target=worker, daemon=True).start()
    
    while True: time.sleep(60)
