from datetime import datetime, timedelta

def compute_demand_intensity(feedback_records) -> float:
    """
    Computes the demand intensity based on a list of feedback records.
    Applies a simple recency decay: newer feedback is weighted heavier than older feedback.
    
    Args:
        feedback_records: A list of feedback objects (must have `created_at` property).
        
    Returns:
        float: The demand intensity score.
    """
    if not feedback_records:
        return 0.0
        
    score = 0.0
    now = datetime.utcnow()
    
    for fb in feedback_records:
        # Calculate days ago
        days_ago = (now - fb.created_at).days
        
        # Simple decay: score = 1.0 / (days_ago + 1)
        # So feedback from today = 1.0, yesterday = 0.5, etc.
        weight = 1.0 / (max(0, days_ago) + 1.0)
        score += weight
        
    return score
