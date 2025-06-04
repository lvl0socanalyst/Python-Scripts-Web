import subprocess
import re
import requests
import time

api_key = "my-super-secure-free-tier-api-key"
headers = {"x-apikey": api_key}
rate_limit_delay = 15  #4 requests/min (free tier)

def extract_ips():
    result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
    ip_pattern = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}')
    ips = sorted({match for line in result.stdout.splitlines() 
                         for match in ip_pattern.findall(line)
                         if match not in ('0.0.0.0', '127.0.0.1')})
    
    with open('netstat.txt', 'w') as f:
        f.write('\n'.join(ips))
    print(f"{len(ips)} IPs saved to netstat.txt")

def api_call(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200 and "data" in r.json():
        stats = r.json()["data"]["attributes"]["last_analysis_stats"]
        print(f"→ {ip}\n   Malicious: {stats['malicious']}, Suspicious: {stats['suspicious']}, Harmless: {stats['harmless']}\n")
    else:
        print(f"No data or error for {ip}")

if __name__ == "__main__":
    extract_ips()
    with open('netstat.txt') as f:
        ips = [line.strip() for line in f if line.strip()]
    
    for i, ip in enumerate(ips):
        api_call(ip)
        if i < len(ips) - 1:
            time.sleep(rate_limit_delay)
