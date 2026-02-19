import requests, random, time, threading, os

# --- BRANDING ---
APP_NAME = "EPIC BOT WITH ALI ABBAS"
VERSION = "V5.0 - REAL-TIME TRACKER"

# --- TARGETS ---
LINKS = [
    "https://newswirhbot.blogspot.com/2026/01/the-ultimate-2026-buying-guide-why.html?m=1",
    "https://newswirhbot.blogspot.com/2026/01/best-price-in-pakistan-2026-shop.html",
    "https://newswirhbot.blogspot.com/2026/01/electronics-accessories-on-asmveocom.html",
    "https://newswirhbot.blogspot.com/2026/01/Asmveo.com.html",
    "https://newswirhbot.blogspot.com/2026/02/discover-best-deals-on-asmveo.html",
    "https://youtu.be/K9ihEWJn4Go?si=SYn8IuvLw2cKfr4W"
]

KEYWORDS = ["Best Price Pakistan", "Asmveo Gadgets", "Ali Abbas Bot", "Tech Deals 2026"]

BROWSERS = [
    "Chrome/121.0.0.0 (Windows NT 10.0)", 
    "Safari/605.1.15 (Macintosh)", 
    "Firefox/122.0 (Ubuntu)", 
    "Edge/121.0.2277.128"
]

def get_ip_info(proxy):
    try:
        # Proxy ke zariye location check karna
        response = requests.get(f"https://ipapi.co/json/", proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
        data = response.json()
        return f"{data.get('city', 'Unknown')}, {data.get('country_name', 'Unknown')}"
    except:
        return "Location Hidden/Private"

def get_proxies():
    try:
        r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=US,GB,CA&ssl=yes&anonymity=elite")
        return r.text.splitlines()
    except: return []

def worker():
    proxy_list = get_proxies()
    while True:
        if not proxy_list: proxy_list = get_proxies()
        
        target = random.choice(LINKS)
        proxy = random.choice(proxy_list)
        keyword = random.choice(KEYWORDS)
        browser = random.choice(BROWSERS)
        
        # Real Location Fetching
        location = get_ip_info(proxy)
        
        headers = {
            "User-Agent": f"Mozilla/5.0 {browser}",
            "Referer": f"https://www.google.com/search?q={keyword.replace(' ', '+')}",
            "X-Forwarded-For": proxy.split(':')[0]
        }
        
        try:
            with requests.get(target, headers=headers, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=12) as r:
                if r.status_code == 200:
                    print(f"\n[🔥 NEW HIT] ------------------------------")
                    print(f"📡 IP       : {proxy}")
                    print(f"📍 LOCATION : {location}")
                    print(f"🌐 BROWSER  : {browser.split('/')[0]}")
                    print(f"🔑 KEYWORD  : {keyword}")
                    print(f"🔗 TARGET   : {target[-30:]}")
                    print(f"✅ STATUS   : SUCCESS (200 OK)")
                    print(f"-------------------------------------------")
        except:
            if proxy in proxy_list: proxy_list.remove(proxy)
            continue
        time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    os.system('clear')
    print(f"🚀 {APP_NAME} Started...")
    print("Monitoring Live Traffic Flow...\n")
    # 15 threads for stability and accuracy
    for _ in range(15):
        threading.Thread(target=worker, daemon=True).start()
    while True: time.sleep(10)
