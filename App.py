import requests, random, time, threading, os
from fake_useragent import UserAgent

# --- 100x ADVANCED CONFIG ---
LINKS = [
    "https://newswirhbot.blogspot.com/2026/01/the-ultimate-2026-buying-guide-why.html?m=1",
    "https://newswirhbot.blogspot.com/2026/01/best-price-in-pakistan-2026-shop.html",
    "https://newswirhbot.blogspot.com/2026/01/electronics-accessories-on-asmveocom.html",
    "https://newswirhbot.blogspot.com/2026/01/Asmveo.com.html",
    "https://newswirhbot.blogspot.com/2026/02/discover-best-deals-on-asmveo.html",
    "https://youtu.be/K9ihEWJn4Go?si=SYn8IuvLw2cKfr4W"
]

# Advanced Keywords for Organic Growth
KEYWORDS = [
    "Asmveo electronics review 2026", "how to find best prices in pakistan", 
    "latest tech gadgets 2026 buying guide", "asmveo.com legit or not",
    "predator badlands 2 movie watch online", "cheapest accessories shop pakistan"
]

# Diverse Referrers to mix traffic sources
REFERRERS = [
    "https://www.google.com/search?q={k}",
    "https://www.bing.com/search?q={k}",
    "https://duckduckgo.com/?q={k}",
    "https://t.co/{r}", # Twitter shortener
    "https://m.facebook.com/",
    "https://www.youtube.com/results?search_query={k}"
]

ua = UserAgent()

def get_super_proxies():
    # Multi-Source Proxy Aggregator
    sources = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&country=US,GB,CA,AU&ssl=yes&anonymity=elite",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://proxyspace.pro/http.txt"
    ]
    all_proxies = []
    for s in sources:
        try:
            r = requests.get(s, timeout=15)
            if r.status_code == 200:
                all_proxies.extend(r.text.splitlines())
        except: continue
    return list(set(all_proxies))

def engine_worker():
    proxy_pool = get_super_proxies()
    print(f"✅ Engine Primed: {len(proxy_pool)} Premium IPs Loaded.")
    
    while True:
        if not proxy_pool or len(proxy_pool) < 20:
            proxy_pool = get_super_proxies()
            
        target = random.choice(LINKS)
        proxy = random.choice(proxy_pool)
        keyword = random.choice(KEYWORDS).replace(" ", "+")
        
        # Super Advanced Header Spoofing
        headers = {
            "User-Agent": ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": random.choice(REFERRERS).format(k=keyword, r=os.urandom(4).hex()),
            "DNT": "1", # Do Not Track request
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }
        
        try:
            p_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            # Initial Hit
            with requests.Session() as s:
                s.proxies = p_dict
                s.headers.update(headers)
                
                # Step 1: Visit Link
                res = s.get(target, timeout=12)
                
                # Step 2: Realistic "Internal Navigation" Simulation
                # Website ko lagega ke user link par ruk kar doosre pages bhi dekh raha hai
                if res.status_code == 200:
                    print(f"🔥 [ULTRA HIT] {target[-20:]} | IP: {proxy[:12]} | Key: {keyword[:10]}")
                    time.sleep(random.randint(20, 45)) # Time on site
                
        except:
            if proxy in proxy_pool: proxy_pool.remove(proxy)
            continue

if __name__ == "__main__":
    # Max Power for Koyeb (30 Parallel Workers)
    for _ in range(30):
        t = threading.Thread(target=engine_worker, daemon=True)
        t.start()
        time.sleep(0.2)
    
    while True:
        time.sleep(100)
