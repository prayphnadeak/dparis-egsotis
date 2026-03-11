import requests
import sys

API_BASE = "http://localhost:8001" # As per run_backend.bat

endpoints = {
    "tourism": "/api/v1/tourism/",
    "culinary": "/api/v1/culinary/",
    "souvenirs": "/api/v1/souvenirs/",
    "accommodations": "/api/v1/accommodations/"
}

expected_counts = {
    "tourism": 24,
    "culinary": 48,
    "souvenirs": 20,
    "accommodations": 45
}

def verify():
    all_ok = True
    for name, path in endpoints.items():
        try:
            url = f"{API_BASE}{path}"
            print(f"Checking {url}...")
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                count = len(data)
                expected = expected_counts[name]
                if count >= expected:
                    print(f"✅ {name}: Found {count} items (Expected at least {expected})")
                else:
                    print(f"❌ {name}: Found {count} items (Expected {expected})")
                    all_ok = False
            else:
                print(f"❌ {name}: HTTP {res.status_code}")
                all_ok = False
        except Exception as e:
            print(f"❌ {name}: Error {e}")
            all_ok = False
    
    if all_ok:
        print("\n🎉 All verification checks passed!")
    else:
        print("\n⚠️ Some checks failed. Make sure the backend server is running on port 7860.")

if __name__ == "__main__":
    verify()
