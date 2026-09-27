def compute_gap_ratio(demand_score: float, infra_stock: float, planned_investment: float) -> float:
    """
    Computes the infrastructure gap ratio for a given area.
    
    Formula:
        Gap Ratio = Demand Score / (Existing Infra Stock + Planned Investment)
        
    Args:
        demand_score: A normalized score representing citizen demand (e.g. from feedback volume).
        infra_stock: A normalized score representing existing infrastructure capacity.
        planned_investment: A normalized score representing upcoming sanctioned projects.
        
    Returns:
        float: The gap ratio. Higher means greater infrastructure deficit.
               Returns float("inf") if the denominator is zero.
    """
    denominator = infra_stock + planned_investment
    if denominator <= 0:
        return float("inf")
    
    return demand_score / denominator
