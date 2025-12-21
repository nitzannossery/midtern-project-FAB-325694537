"""
Portfolio & Risk Agent
Generates investment recommendations under risk constraints following ReAct pattern
"""

from typing import Dict, Any
from tools.financial_calculator import FinancialCalculator


class PortfolioRiskAgent:
    """
    Portfolio & Risk Agent - Generates risk-aware investment recommendations
    Follows ReAct pattern: Reason → Act
    """
    
    def __init__(self):
        self.calculator = FinancialCalculator()
    
    def analyze(
        self,
        symbol: str,
        risk_profile: str,
        horizon_months: int,
        market_data: Dict[str, Any],
        fundamentals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze portfolio and risk considerations
        
        Args:
            symbol: Stock ticker symbol
            risk_profile: User risk profile (conservative, moderate, aggressive)
            horizon_months: Investment horizon in months
            market_data: Market data from Market Data Agent
            fundamentals: Fundamentals from Fundamental & News Agent
            
        Returns:
            Dictionary with recommendation results
        """
        # REASON: Assess risk profile and constraints
        reason = self._reason(symbol, risk_profile, horizon_months, market_data, fundamentals)
        
        # ACT: Compute risk metrics and recommendations
        action_result = self._act(risk_profile, horizon_months, market_data, fundamentals)
        
        # OUTPUT: Generate clear recommendation
        output = self._generate_output(action_result, reason)
        
        return {
            "agent": "Portfolio & Risk Agent",
            "reason": reason,
            "action": action_result,
            "output": output
        }
    
    def _reason(
        self,
        symbol: str,
        risk_profile: str,
        horizon_months: int,
        market_data: Dict[str, Any],
        fundamentals: Dict[str, Any]
    ) -> str:
        """
        Reason: Assess user constraints and scenario sensitivity
        
        Args:
            symbol: Stock ticker symbol
            risk_profile: User risk profile
            horizon_months: Investment horizon
            market_data: Market data
            fundamentals: Fundamentals data
            
        Returns:
            Reasoning string
        """
        # Helper function for safe formatting
        def fmt(x, spec=".2f", default="N/A"):
            return format(x, spec) if x is not None else default
        
        # Safe access with defaults
        market_data = market_data or {}
        fundamentals = fundamentals or {}
        
        volatility = market_data.get("volatility")
        debt_equity = fundamentals.get("debt_to_equity")
        profit_margin = fundamentals.get("profit_margin")
        
        reason = (
            f"Risk Assessment for {symbol}:\n"
            f"- User Risk Profile: {risk_profile.upper()}\n"
            f"- Investment Horizon: {horizon_months} months\n"
            f"- Market Volatility: {fmt(volatility, '.2f')}% (annualized)\n"
            f"- Financial Leverage: Debt/Equity = {fmt(debt_equity, '.2f')}\n"
            f"- Profitability: Margin = {fmt(profit_margin * 100 if profit_margin is not None else None, '.2f')}%\n"
            f"- Scenario Sensitivity: {'Long-term' if horizon_months >= 24 else 'Medium-term' if horizon_months >= 12 else 'Short-term'} horizon requires "
            f"{'stability focus' if risk_profile == 'conservative' else 'balanced approach' if risk_profile == 'moderate' else 'growth focus'}\n"
            f"- Constraints: Risk profile must align with portfolio allocation"
        )
        
        return reason
    
    def _act(
        self,
        risk_profile: str,
        horizon_months: int,
        market_data: Dict[str, Any],
        fundamentals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Act: Compute risk-aware recommendations
        
        Args:
            risk_profile: User risk profile
            horizon_months: Investment horizon
            market_data: Market data
            fundamentals: Fundamentals data
            
        Returns:
            Recommendation dictionary
        """
        volatility = market_data.get("volatility", 0)
        
        # Calculate risk score
        risk_score = self.calculator.calculate_risk_score(
            fundamentals,
            volatility,
            risk_profile
        )
        
        # Generate recommendation
        recommendation = self.calculator.generate_recommendation(
            risk_score,
            risk_profile,
            horizon_months,
            fundamentals,
            market_data
        )
        
        return {
            "risk_score": risk_score,
            "recommendation": recommendation,
            "volatility": volatility
        }
    
    def _generate_output(self, action_result: Dict[str, Any], reason: str) -> str:
        """
        Generate clear recommendation output
        
        Args:
            action_result: Action results
            reason: Reasoning string
            
        Returns:
            Formatted output string
        """
        # Helper function for safe formatting
        def fmt(x, spec=".2f", default="N/A"):
            return format(x, spec) if x is not None else default
        
        # Safe access with defaults
        action_result = action_result or {}
        recommendation = action_result.get("recommendation", {}) or {}
        risk_score = action_result.get("risk_score")
        volatility = action_result.get("volatility")
        
        output = (
            f"Portfolio & Risk Recommendation:\n\n"
            f"Risk Score: {fmt(risk_score, '.1f')}/100\n"
            f"Volatility: {fmt(volatility, '.2f')}%\n\n"
            f"Recommendation: {recommendation.get('action', 'HOLD')}\n"
            f"Suggested Allocation: {recommendation.get('allocation', 'N/A')}\n\n"
            f"Reasoning:\n{recommendation.get('reasoning', 'No reasoning provided')}\n\n"
        )
        
        # Add stress considerations
        if risk_score > 60:
            output += "⚠️ Stress Considerations: High risk score indicates elevated volatility and potential downside risk. "
            output += "Consider position sizing and stop-loss strategies.\n"
        elif risk_score < 30:
            output += "✓ Stress Considerations: Low risk score suggests relative stability. "
            output += "Suitable for risk-averse investors.\n"
        else:
            output += "⚠ Stress Considerations: Moderate risk level. "
            output += "Monitor market conditions and adjust position as needed.\n"
        
        return output

