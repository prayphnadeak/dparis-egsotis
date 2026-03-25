import requests
import json
import sys

token = "YOUR_HF_TOKEN_HERE"
url_build = "https://huggingface.co/api/spaces/prayphnadeak/dparis-egsotis/logs/build"
url_run = "https://huggingface.co/api/spaces/prayphnadeak/dparis-egsotis/logs/run"

def fetch_logs(url, name):
    print(f"\n===== {name} LOGS =====")
    try:
        response = requests.get(url, headers={'Authorization': f'Bearer {token}'}, stream=True, timeout=10)
        lines = []
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data:'):
                    try:
                        data = json.loads(decoded_line[5:])
                        lines.append(data)
                    except:
                        lines.append(decoded_line)
            if len(lines) > 50:
                break
        for l in lines:
            print(l)
    except Exception as e:
        print(f"Error fetching {name} logs: {e}")

fetch_logs(url_build, "BUILD")
fetch_logs(url_run, "RUN")
