import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

# Proxy list (extracted directly)
proxies = [
    {"name": "BDIX5 SAM FTP 50 mbps", "type": "http", "server": "175.29.178.42", "port": 49516},
    {"name": "BDIX10 CIRCLE FTP 50 mbps", "type": "http", "server": "202.136.89.28", "port": 43770},
    {"name": "BDIX12 GENERAL 50 mbps", "type": "http", "server": "117.58.241.133", "port": 34362},
    {"name": "BDIX58b GENERAL 50 mbps", "type": "socks5", "server": "103.129.213.97", "port": 9169, "username": "speedb", "password": "speedb"},
    {"name": "BDIX62 GENERAL 100 mbps", "type": "socks5", "server": "114.130.82.32", "port": 9169, "username": "speedb", "password": "speedb"},
    {"name": "BDIX63 GENERAL 100 mbps", "type": "socks5", "server": "103.87.138.44", "port": 9169, "username": "speedb", "password": "speedb"},
    {"name": "BDIX68 GENERAL 100 mbps", "type": "socks5", "server": "103.111.227.252", "port": 9169, "username": "speedb", "password": "speedb"},
]

# Test URL for connectivity
TEST_URL = "https://www.google.com"

def check_proxy(proxy):
    proxy_url = f"{proxy['type']}://{proxy['server']}:{proxy['port']}"
    if 'username' in proxy and 'password' in proxy:
        proxy_url = f"{proxy['type']}://{proxy['username']}:{proxy['password']}@{proxy['server']}:{proxy['port']}"

    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }

    start_time = time.time()
    try:
        response = requests.get(TEST_URL, proxies=proxies, timeout=5)
        response.raise_for_status()
        latency = round((time.time() - start_time) * 1000, 2)
        speed = round(len(response.content) / (time.time() - start_time) / 1024, 2)  # Speed in KB/s
        return {
            'name': proxy['name'],
            'status': '✅ Working',
            'latency': f"{latency} ms",
            'speed': f"{speed} KB/s"
        }
    except Exception as e:
        return {
            'name': proxy['name'],
            'status': f"❌ Failed ({str(e)})",
            'latency': '-',
            'speed': '-'
        }

def main():
    print("Testing proxies...")

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        for future in as_completed(future_to_proxy):
            result = future.result()
            results.append(result)
            print(f"{result['name']}: {result['status']} (Latency: {result['latency']}, Speed: {result['speed']})")

    print("\n=== Summary ===")
    for result in results:
        print(f"{result['name']}: {result['status']} (Latency: {result['latency']}, Speed: {result['speed']})")

if __name__ == "__main__":
    main()
