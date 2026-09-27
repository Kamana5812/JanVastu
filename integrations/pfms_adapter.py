import requests
import time
from datetime import datetime, timedelta

API_URL = "http://localhost:8000/api/v1/integrations/sync-accountability"

MOCK_RECORDS = [
    {
        "asset_id": 1,
        "contractor_name": "L&T Infrastructure",
        "sanctioned_cost": 50000000.0,
        "actual_cost": 55000000.0,
        "planned_completion_date": (datetime.now() + timedelta(days=90)).isoformat(),
        "actual_completion_date": None,
        "responsible_official": "Dr. A. Sharma",
        "department": "Ministry of Health & Family Welfare"
    },
    {
        "asset_id": 2,
        "contractor_name": "Jal Jeevan Contractors Ltd.",
        "sanctioned_cost": 15000000.0,
        "actual_cost": 12000000.0,
        "planned_completion_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "actual_completion_date": None,
        "responsible_official": "B. Patnaik",
        "department": "Ministry of Jal Shakti"
    },
    {
        "asset_id": 3,
        "contractor_name": "NHAI Subcontractors",
        "sanctioned_cost": 120000000.0,
        "actual_cost": 125000000.0,
        "planned_completion_date": (datetime.now() - timedelta(days=10)).isoformat(),
        "actual_completion_date": (datetime.now() - timedelta(days=5)).isoformat(),
        "responsible_official": "S. Gupta",
        "department": "Ministry of Road Transport"
    }
]

def sync_financials():
    print("Starting PFMS Adapter Sync...")
    for record in MOCK_RECORDS:
        try:
            response = requests.post(API_URL, json=record)
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Synced Accountability Record for Asset ID: {data['asset_id']}")
            else:
                print(f"[ERR] Failed to sync record for Asset {record['asset_id']}: {response.text}")
        except Exception as e:
            print(f"[ERR] Error connecting to API: {e}")
        time.sleep(1)

if __name__ == "__main__":
    sync_financials()
