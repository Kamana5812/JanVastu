from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, Dict
import httpx

app = FastAPI(title="JanVastu WhatsApp Bot Mock", version="0.1.0")

# In-memory session store (sender_id -> session_data)
# { "919999999999": {"state": "PENDING_CONSENT", "language": "English", "consent_id": None} }
sessions: Dict[str, dict] = {}

CORE_BACKEND_URL = "http://localhost:8000/api/v1"

class IncomingMessage(BaseModel):
    sender_id: str
    message_type: str = "text"
    payload: str
    language_hint: str = "English"

class OutgoingMessage(BaseModel):
    recipient_id: str
    text: str

@app.post("/webhook", response_model=OutgoingMessage)
async def webhook(message: IncomingMessage):
    sender_id = message.sender_id
    text = message.payload.strip().lower()

    # 1. New User
    if sender_id not in sessions:
        sessions[sender_id] = {
            "state": "PENDING_CONSENT",
            "language": message.language_hint,
            "consent_id": None
        }
        consent_notice = (
            "Welcome to JanVastu (जनवास्तु)! \n"
            "By proceeding, you consent to sharing this feedback to help map public infrastructure. "
            "Your identity will be anonymized. \n\n"
            "Reply 'YES' to accept or 'NO' to decline."
        )
        return OutgoingMessage(recipient_id=sender_id, text=consent_notice)

    session = sessions[sender_id]

    # 2. Pending Consent
    if session["state"] == "PENDING_CONSENT":
        if text in ["yes", "y", "haan", "ha"]:
            # Register consent with backend
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{CORE_BACKEND_URL}/consent",
                    json={
                        "purpose": "Infrastructure Feedback",
                        "language": session["language"],
                        "channel": "WhatsApp"
                    }
                )
                if resp.status_code == 200:
                    consent_id = resp.json().get("consent_id")
                    session["consent_id"] = consent_id
                    session["state"] = "CONSENT_GRANTED"
                    return OutgoingMessage(
                        recipient_id=sender_id, 
                        text="Consent granted! You can now send photos, videos, or text describing the infrastructure issue."
                    )
                else:
                    return OutgoingMessage(recipient_id=sender_id, text="Error registering consent with backend. Please try again later.")
        elif text in ["no", "n", "nahi"]:
            del sessions[sender_id]
            return OutgoingMessage(recipient_id=sender_id, text="Consent declined. We have deleted your session. Thank you.")
        else:
            return OutgoingMessage(recipient_id=sender_id, text="Please reply 'YES' or 'NO'.")

    # 3. Consent Granted - Forward Feedback
    if session["state"] == "CONSENT_GRANTED":
        # Forward to core backend
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{CORE_BACKEND_URL}/feedback",
                json={
                    "category": None, # Will be filled by AI pipeline later
                    "description_text": message.payload, # Raw text
                    "language": session["language"],
                    "consent_id": session["consent_id"],
                    "lat": 0.0, # Stub for mock
                    "lon": 0.0,
                    "media_urls": []
                }
            )
            
            if resp.status_code == 200:
                feedback_id = resp.json().get("feedback_id")
                return OutgoingMessage(
                    recipient_id=sender_id, 
                    text=f"Thank you! Your feedback has been recorded securely. Tracking ID: #{feedback_id}"
                )
            else:
                return OutgoingMessage(recipient_id=sender_id, text="Failed to submit feedback to backend.")

    return OutgoingMessage(recipient_id=sender_id, text="Unknown state error.")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "whatsapp-bot-adapter"}
