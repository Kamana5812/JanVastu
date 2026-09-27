import requests
import time

CORE_BACKEND_URL = "http://localhost:8000/api/v1"

def test_pipeline():
    print("=== Testing AI Pipeline ===")
    
    # 1. Create a dummy consent first
    print("1. Creating dummy consent...")
    consent_resp = requests.post(
        f"{CORE_BACKEND_URL}/consent",
        json={"purpose": "Test", "language": "English", "channel": "CLI"}
    )
    consent_id = consent_resp.json()["consent_id"]
    
    # 2. Submit raw feedback (no category)
    print("2. Submitting raw feedback (e.g., a burst pipe)...")
    feedback_text = "The water pipe broke outside the clinic."
    fb_resp = requests.post(
        f"{CORE_BACKEND_URL}/feedback",
        json={
            "consent_id": consent_id,
            "description_text": feedback_text,
            "language": "English",
            "lat": 0.0,
            "lon": 0.0,
            "status": "new"
        }
    )
    fb_id = fb_resp.json()["feedback_id"]
    print(f"   Created Feedback #{fb_id}")

    # 3. Wait for AI pipeline to poll (polls every 5s)
    print("3. Waiting 6 seconds for AI pipeline to process...")
    time.sleep(6)

    # 4. Fetch the feedback to verify updates
    print("4. Fetching feedback to verify AI categorization...")
    get_resp = requests.get(f"{CORE_BACKEND_URL}/feedback/{fb_id}")
    data = get_resp.json()
    
    print(f"\nResult:")
    print(f"  Category: {data['category']}")
    print(f"  Status:   {data['status']}")
    
    if data['category'] == "Water" and data['status'] == "triaged":
        print("\n✅ AI Pipeline test PASSED!")
    else:
        print("\n❌ AI Pipeline test FAILED.")

if __name__ == "__main__":
    test_pipeline()
