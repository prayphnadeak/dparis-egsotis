import urllib.request
import sys

token = "YOUR_HF_TOKEN_HERE"
url_build = "https://huggingface.co/api/spaces/prayphnadeak/dparis-egsotis/logs/build"
url_run = "https://huggingface.co/api/spaces/prayphnadeak/dparis-egsotis/logs/run"

def get_logs(url, name):
    print(f"\n--- {name} LOGS ---")
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    try:
        with urllib.request.urlopen(req) as response:
            count = 0
            for line in response:
                decoded = line.decode('utf-8').strip()
                if decoded:
                    print(decoded)
                    count += 1
                if count > 100:  # Prevent infinite hanging on SSE
                    break
    except Exception as e:
        print(f"Error reading {name} logs: {e}")

get_logs(url_build, "BUILD")
get_logs(url_run, "RUN")
