import requests
import time
import random

API_URL = "http://localhost:8000/api/v1/integrations/sync-asset"

MOCK_ASSETS = [
    {
        "name": "New Primary Health Center (Bhubaneswar)",
        "type": "Health",
        "source_system": "IIG",
        "status": "Planned",
        "latitude": 20.2961,
        "longitude": 85.8245
    },
    {
        "name": "Rural Water Pipeline Extension (Cuttack)",
        "type": "Water",
        "source_system": "IIG",
        "status": "Under Construction",
        "latitude": 20.4625,
        "longitude": 85.8830
    },
    {
        "name": "State Highway 12 Expansion",
        "type": "Road",
        "source_system": "IIG",
        "status": "Active",
        "latitude": 28.6139,
        "longitude": 77.2090
    }
]

def sync_assets():
    print("Starting IIG Adapter Sync...")
    for asset in MOCK_ASSETS:
        try:
            response = requests.post(API_URL, json=asset)
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Synced Asset: {data['name']} (ID: {data['id']})")
            else:
                print(f"[ERR] Failed to sync {asset['name']}: {response.text}")
        except Exception as e:
            print(f"[ERR] Error connecting to API: {e}")
        time.sleep(1)
        
if __name__ == "__main__":
    sync_assets()
