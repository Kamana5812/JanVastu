import requests
import time

BOT_URL = "http://localhost:8085/webhook"
SENDER_ID = "919876543210"

def send_message(text):
    print(f"\n[You]: {text}")
    response = requests.post(
        BOT_URL,
        json={
            "sender_id": SENDER_ID,
            "message_type": "text",
            "payload": text,
            "language_hint": "English"
        }
    )
    if response.status_code == 200:
        bot_reply = response.json().get("text", "")
        print(f"[Bot]: {bot_reply}")
    else:
        print(f"[Error]: Bot responded with status {response.status_code}")

if __name__ == "__main__":
    print("=== JanVastu WhatsApp Simulation ===")
    print("Simulating a new conversation...")
    time.sleep(1)

    # 1. Initiate contact
    send_message("Hi")
    time.sleep(1.5)

    # 2. Grant consent
    send_message("YES")
    time.sleep(1.5)

    # 3. Send feedback
    send_message("There is a massive pothole outside the primary school.")
    time.sleep(1)
    
    print("\n=== Simulation Complete ===")
