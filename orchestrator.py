"""
Orchestrator
Central coordinator for the Financial Analysis Multi-Agent System
Aggregates agent outputs into a single Final Answer
"""

from typing import Dict, Any
from agents.market_data_agent import MarketDataAgent
from agents.fundamental_news_agent import FundamentalNewsAgent
from agents.portfolio_risk_agent import PortfolioRiskAgent
from tools.tabular_demo import answer_highest_net_income, TABULAR_DATA


class Orchestrator:
    """
    Orchestrator - Coordinates all agents and aggregates their outputs
    """
    
    def __init__(self):
        self.market_data_agent = MarketDataAgent()
        self.fundamental_news_agent = FundamentalNewsAgent()
        self.portfolio_risk_agent = PortfolioRiskAgent()
    
    def process_query(
        self,
        symbol: str,
        risk_profile: str,
        horizon_months: int
    ) -> Dict[str, Any]:
        """
        Process a financial analysis query through all agents
        
        Args:
            symbol: Stock ticker symbol
            risk_profile: User risk profile (conservative, moderate, aggressive)
            horizon_months: Investment horizon in months
            
        Returns:
            Complete analysis with all agent outputs and final answer
        """
        # Step 1: Market Data Agent
        market_result = self.market_data_agent.analyze(symbol, horizon_months)
        market_data = market_result.get("action", {})
        
        # Step 2: Fundamental & News Agent
        fundamental_result = self.fundamental_news_agent.analyze(symbol)
        fundamental_data = fundamental_result.get("action", {})
        fundamentals = fundamental_data.get("fundamentals", {})
        
        # Step 3: Portfolio & Risk Agent (requires outputs from other agents)
        portfolio_result = self.portfolio_risk_agent.analyze(
            symbol,
            risk_profile,
            horizon_months,
            market_data,
            fundamentals
        )
        
        # Step 4: Generate Final Answer
        final_answer = self._generate_final_answer(
            symbol,
            risk_profile,
            horizon_months,
            market_result,
            fundamental_result,
            portfolio_result
        )
        
        return {
            "query": {
                "symbol": symbol,
                "risk_profile": risk_profile,
                "horizon_months": horizon_months
            },
            "agents": {
                "market_data": market_result,
                "fundamental_news": fundamental_result,
                "portfolio_risk": portfolio_result
            },
            "final_answer": final_answer
        }
    
    def _generate_final_answer(
        self,
        symbol: str,
        risk_profile: str,
        horizon_months: int,
        market_result: Dict[str, Any],
        fundamental_result: Dict[str, Any],
        portfolio_result: Dict[str, Any]
    ) -> str:
        """
        Aggregate all agent outputs into a coherent final answer
        
        Args:
            symbol: Stock ticker symbol
            risk_profile: User risk profile
            horizon_months: Investment horizon
            market_result: Market Data Agent output
            fundamental_result: Fundamental & News Agent output
            portfolio_result: Portfolio & Risk Agent output
            
        Returns:
            Final answer string
        """
        # Extract key information
        market_output = market_result.get("output", "")
        fundamental_output = fundamental_result.get("output", "")
        portfolio_output = portfolio_result.get("output", "")
        
        # Extract recommendation
        portfolio_action = portfolio_result.get("action", {})
        recommendation = portfolio_action.get("recommendation", {})
        action = recommendation.get("action", "HOLD")
        allocation = recommendation.get("allocation", "N/A")
        
        # Build final answer
        final_answer = f"""
#### Final Answer - Financial Analysis for {symbol}

**Query Parameters:**
- Symbol: {symbol}
- Risk Profile: {risk_profile.upper()}
- Investment Horizon: {horizon_months} months

---

##### Agent Analysis Summary

**1. Market Data Analysis:**
{market_output}

**2. Fundamental & News Analysis:**
{fundamental_output}

**3. Portfolio & Risk Analysis:**
{portfolio_output}

---

##### Investment Recommendation

**Action:** {action}  
**Suggested Portfolio Allocation:** {allocation}

**Justification:**
The recommendation is based on:
- Market data trends and volatility assessment
- Fundamental financial health metrics
- Alignment with your {risk_profile} risk profile
- {horizon_months}-month investment horizon considerations
"""
        
        return final_answer.strip()
    
    def process_tabular_demo(self) -> dict:
        """
        Hard+ Tabular reasoning demo:
        deterministic answer from structured table with evidence.
        """
        tab_res = answer_highest_net_income(TABULAR_DATA)

        # Keep the return shape UI-friendly
        return {
            "mode": "hard_plus_tabular",
            "tabular_data": tab_res["table"],
            "question": tab_res["question"],
            "answer": tab_res["answer"],
            "final_answer": tab_res["final_answer"],
            "confidence": tab_res["confidence"],
            "reason_summary": tab_res["reason_summary"],
            "act_summary": tab_res["act_summary"],
            "evidence": tab_res["evidence"],
            "checks": tab_res["checks"],
        }

