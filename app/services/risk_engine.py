from app.models.models import RiskLevel
from typing import Tuple

class RiskEngine:
    @staticmethod
    def calculate_risk(
        rainfall: float, 
        soil_moisture: float, 
        displacement: float, 
        slope_factor: float
    ) -> Tuple[RiskLevel, float, str]:
        """
        Calculates the risk level, risk score, and an explanation.
        """
        # Weighted score calculation
        # Max score is ~100
        # Rainfall (40%), Soil Moisture (30%), Displacement (20%), Slope (10%)
        
        rainfall_score = min((rainfall / 200.0) * 40, 40)
        moisture_score = min((soil_moisture / 100.0) * 30, 30)
        displacement_score = min((displacement / 10.0) * 20, 20)
        slope_score = min((slope_factor / 10.0) * 10, 10)
        
        total_score = rainfall_score + moisture_score + displacement_score + slope_score
        
        # Determine Level
        if total_score >= 80 or (displacement > 8 and rainfall > 100):
            level = RiskLevel.CRITICAL
            explanation = "Critical risk caused by extreme rainfall, high soil saturation, and significant slope displacement."
        elif total_score >= 60:
            level = RiskLevel.HIGH
            explanation = "High risk due to heavy rainfall and elevated soil saturation levels."
        elif total_score >= 35:
            level = RiskLevel.MODERATE
            explanation = "Moderate risk. Increasing rainfall and rising soil moisture levels detected."
        else:
            level = RiskLevel.LOW
            explanation = "Low risk. Environmental conditions are within stable parameters."
            
        return level, total_score, explanation
