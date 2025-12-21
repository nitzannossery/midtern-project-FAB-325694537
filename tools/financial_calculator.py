"""
Financial Calculator Tool
Computes risk metrics and portfolio recommendations
"""

from typing import Dict, List
import numpy as np


class FinancialCalculator:
    """Calculates financial metrics and risk assessments"""
    
    @staticmethod
    def calculate_risk_score(fundamentals: Dict, volatility: float, risk_profile: str) -> float:
        """
        Calculate risk score based on fundamentals and volatility
        
        Args:
            fundamentals: Fundamental data dictionary
            volatility: Annualized volatility percentage
            risk_profile: User risk profile (conservative, moderate, aggressive)
            
        Returns:
            Risk score (0-100)
        """
        score = 0
        
        # Volatility component (0-40 points)
        if volatility < 15:
            score += 10
        elif volatility < 25:
            score += 20
        elif volatility < 35:
            score += 30
        else:
            score += 40
        
        # P/E ratio component (0-20 points)
        pe = fundamentals.get("pe_ratio")
        if pe:
            if pe < 15:
                score += 5
            elif pe < 25:
                score += 15
            else:
                score += 20
        
        # Debt-to-equity component (0-20 points)
        debt_equity = fundamentals.get("debt_to_equity")
        if debt_equity:
            if debt_equity < 0.5:
                score += 5
            elif debt_equity < 1.0:
                score += 15
            else:
                score += 20
        
        # Profit margin component (0-20 points)
        profit_margin = fundamentals.get("profit_margin")
        if profit_margin:
            if profit_margin > 0.15:
                score += 5
            elif profit_margin > 0.05:
                score += 15
            else:
                score += 20
        
        return min(score, 100)
    
    @staticmethod
    def generate_recommendation(
        risk_score: float,
        risk_profile: str,
        horizon_months: int,
        fundamentals: Dict,
        market_data: Dict
    ) -> Dict:
        """
        Generate investment recommendation
        
        Args:
            risk_score: Calculated risk score
            risk_profile: User risk profile
            horizon_months: Investment horizon in months
            fundamentals: Fundamental data
            market_data: Market data
            
        Returns:
            Recommendation dictionary
        """
        # Determine recommendation based on risk profile
        if risk_profile == "conservative":
            if risk_score < 30:
                action = "BUY"
                allocation = "5-10%"
                reasoning = "Low risk score aligns with conservative profile"
            elif risk_score < 50:
                action = "HOLD"
                allocation = "3-5%"
                reasoning = "Moderate risk, limited exposure recommended"
            else:
                action = "AVOID"
                allocation = "0%"
                reasoning = "High risk score incompatible with conservative profile"
        
        elif risk_profile == "moderate":
            if risk_score < 40:
                action = "BUY"
                allocation = "10-15%"
                reasoning = "Acceptable risk for moderate profile"
            elif risk_score < 60:
                action = "HOLD"
                allocation = "5-10%"
                reasoning = "Moderate risk, standard allocation"
            else:
                action = "REDUCE"
                allocation = "0-5%"
                reasoning = "Elevated risk, reduce exposure"
        
        else:  # aggressive
            if risk_score < 60:
                action = "BUY"
                allocation = "15-20%"
                reasoning = "Risk acceptable for aggressive profile"
            else:
                action = "HOLD"
                allocation = "10-15%"
                reasoning = "High risk but manageable for aggressive investors"
        
        # Adjust for horizon
        if horizon_months >= 24:
            reasoning += f". Long-term horizon ({horizon_months} months) supports position."
        elif horizon_months >= 12:
            reasoning += f". Medium-term horizon ({horizon_months} months) appropriate."
        else:
            reasoning += f". Short-term horizon ({horizon_months} months) requires caution."
        
        return {
            "action": action,
            "allocation": allocation,
            "risk_score": round(risk_score, 1),
            "reasoning": reasoning,
            "horizon_months": horizon_months
        }


