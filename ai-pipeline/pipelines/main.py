import asyncio
import httpx
from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-pipeline")

app = FastAPI(title="JanVastu AI Pipeline", version="0.1.0")

CORE_BACKEND_URL = "http://localhost:8000/api/v1"

def mock_categorize_feedback(text: str) -> str:
    """
    Mock AI categorizer. 
    In the future, this is where you'd call Gemini:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(...)
    """
    text = text.lower()
    if "pothole" in text or "road" in text:
        return "Road"
    elif "pipe" in text or "water" in text or "leak" in text:
        return "Water"
    elif "school" in text or "teacher" in text:
        return "Education"
    elif "hospital" in text or "clinic" in text:
        return "Health"
    elif "light" in text or "electricity" in text or "power" in text:
        return "Electricity"
    elif "garbage" in text or "waste" in text or "sanitation" in text:
        return "Sanitation"
    elif "house" in text or "building" in text:
        return "Housing"
    else:
        return "Other"

async def process_feedback_batch():
    async with httpx.AsyncClient() as client:
        try:
            # 1. Fetch untriaged feedback
            resp = await client.get(f"{CORE_BACKEND_URL}/feedback/untriaged")
            if resp.status_code != 200:
                logger.error(f"Failed to fetch untriaged feedback: {resp.text}")
                return

            feedbacks = resp.json()
            if not feedbacks:
                return

            logger.info(f"Found {len(feedbacks)} untriaged feedback items.")

            for fb in feedbacks:
                fb_id = fb["id"]
                text = fb["description_text"]
                
                # 2. Categorize
                category = mock_categorize_feedback(text)
                logger.info(f"Feedback #{fb_id} categorized as: {category}")

                # 3. Update backend
                patch_resp = await client.patch(
                    f"{CORE_BACKEND_URL}/feedback/{fb_id}",
                    json={"category": category, "status": "triaged"}
                )
                
                if patch_resp.status_code == 200:
                    logger.info(f"Successfully updated Feedback #{fb_id}")
                else:
                    logger.error(f"Failed to update Feedback #{fb_id}: {patch_resp.text}")
                    
        except Exception as e:
            logger.error(f"Error in processing loop: {e}")

async def polling_loop():
    while True:
        await process_feedback_batch()
        await asyncio.sleep(5)  # Poll every 5 seconds

@app.on_event("startup")
async def startup_event():
    logger.info("Starting AI categorization background task...")
    asyncio.create_task(polling_loop())

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-pipeline"}
