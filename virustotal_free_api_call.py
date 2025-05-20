import requests
import base64
import time

#VT Key
api_key = "your-super-secure-not-encrypted-api-key"
headers = {"x-apikey": api_key}
rate_limit_delay = 15  #4 requests per minute as per free tier requirements

#VT base64 encodes API requests
def base64_encode(domain):
    return base64.urlsafe_b64encode(domain.encode()).decode().strip("=")

#API call to VT to iterate through domains
def api_call(domain):
    encoded_domain = base64_encode(domain)
    url = f"https://www.virustotal.com/api/v3/urls/{encoded_domain}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                stats = data["data"]["attributes"]["last_analysis_stats"]
                print(f"→ {domain}")
                print(f"   Malicious: {stats['malicious']}, Suspicious: {stats['suspicious']}, Harmless: {stats['harmless']}\n")
            else:
                print(f"No data found for {domain}\n")
        else:
            print(f"Error {response.status_code} for {domain}: {response.text}")
    except Exception as e:
        print(f"Incorrect format for{domain}: {e}")

#Reads domains from txt files only
def read_txt(txt_path):
    try:
        with open(txt_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error reading file {txt_path}: {e}")
        return []

if __name__ == "__main__":
    txt_path = input("Enter full path to txt file: ")
    domains = read_txt(txt_path)

    if domains:
        for i, domain in enumerate(domains):
            api_call(domain)
            if i < len(domains) - 1:
                time.sleep(rate_limit_delay)
    else:
        print("No domains")