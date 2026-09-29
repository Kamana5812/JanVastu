"""Compatibility import for the inline pipeline. No polling service is required."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"backend"))
from app.services.ai_service import analyze
def mock_categorize_feedback(text):
    category=analyze(text)["category"]
    return "Education" if category=="school" else category.capitalize()
if __name__=="__main__":
    print("The active pipeline runs inside the API on report submission. See /api/v1/ai-ops/pipelines.")
