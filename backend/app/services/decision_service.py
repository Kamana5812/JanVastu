from sqlalchemy.orm import Session
from sqlalchemy import func, cast
from geoalchemy2.types import Geography
from app.models.feedback import Feedback
from app.models.asset import Asset
import logging

class DecisionService:
    @staticmethod
    def calculate_gap_ratio(db: Session, lat: float, lon: float, radius_m: float = 5000) -> dict:
        """
        Calculates the Infrastructure Gap Ratio for a given area.
        Formula (mock): (Count of Feedback) / (Count of Assets + 1)
        High ratio means high demand/complaints but low infrastructure.
        """
        target_point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
        
        try:
            feedback_count = db.query(Feedback).filter(
                func.ST_DWithin(
                    cast(Feedback.location, Geography),
                    cast(target_point, Geography),
                    radius_m
                )
            ).count()
            
            asset_count = db.query(Asset).filter(
                func.ST_DWithin(
                    cast(Asset.location, Geography),
                    cast(target_point, Geography),
                    radius_m
                )
            ).count()
            
            gap_ratio = feedback_count / (asset_count + 1)
            
            return {
                "latitude": lat,
                "longitude": lon,
                "radius_m": radius_m,
                "feedback_count": feedback_count,
                "asset_count": asset_count,
                "gap_ratio": round(gap_ratio, 2)
            }
        except Exception as e:
            logging.error(f"Error calculating gap ratio: {e}")
            return {
                "latitude": lat,
                "longitude": lon,
                "radius_m": radius_m,
                "feedback_count": 0,
                "asset_count": 0,
                "gap_ratio": 0.0
            }

decision_service = DecisionService()
