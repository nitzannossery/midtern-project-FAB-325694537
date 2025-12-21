"""
Complex Query Handler
Handles complex investment questions requiring multi-agent analysis
"""

from typing import Dict, List


class ComplexQueryHandler:
    """Handles complex investment questions"""
    
    def __init__(self):
        # Import here to avoid circular import
        from orchestrator import Orchestrator
        self.orchestrator = Orchestrator()
    
    def handle(self, question_data: Dict) -> Dict:
        """
        Handle a complex question
        
        Args:
            question_data: Parsed question data
            
        Returns:
            Analysis result dictionary
        """
        subtype = question_data.get("subtype")
        
        if subtype == "investment_recommendation":
            return self._handle_investment_recommendation(question_data)
        elif subtype == "comparison":
            return self._handle_comparison(question_data)
        elif subtype == "portfolio":
            return self._handle_portfolio(question_data)
        elif subtype == "data_based_recommendation":
            return self._handle_data_based_recommendation(question_data)
        else:
            return {
                "error": f"Unknown complex question type: {subtype}",
                "answer": f"I don't understand this type of question yet."
            }
    
    def _handle_investment_recommendation(self, question_data: Dict) -> Dict:
        """Handle investment recommendation question"""
        symbol = question_data.get("symbol")
        horizon_months = question_data.get("horizon_months", 12)
        risk_profile = question_data.get("risk_profile", "moderate")
        
        if not symbol:
            return {
                "error": "Could not identify stock symbol",
                "answer": "Please specify a stock symbol in your question."
            }
        
        result = self.orchestrator.process_query(symbol, risk_profile, horizon_months)
        
        return {
            "type": "investment_recommendation",
            "symbol": symbol,
            "result": result,
            "answer": result["final_answer"]
        }
    
    def _handle_comparison(self, question_data: Dict) -> Dict:
        """Handle comparison question"""
        symbols = question_data.get("symbols", [])
        
        if len(symbols) < 2:
            return {
                "error": "Need at least 2 symbols for comparison",
                "answer": "Please specify two stocks to compare."
            }
        
        # Analyze both symbols
        symbol1, symbol2 = symbols[0], symbols[1]
        result1 = self.orchestrator.process_query(symbol1, "moderate", 12)
        result2 = self.orchestrator.process_query(symbol2, "moderate", 12)
        
        # Generate comparison
        comparison = self._generate_comparison(symbol1, symbol2, result1, result2)
        
        return {
            "type": "comparison",
            "symbols": symbols,
            "result1": result1,
            "result2": result2,
            "answer": comparison
        }
    
    def _handle_portfolio(self, question_data: Dict) -> Dict:
        """Handle portfolio building question"""
        amount_str = question_data.get("amount", "50000")
        risk_profile = question_data.get("risk_profile", "moderate")
        
        # Parse amount
        amount = self._parse_amount(amount_str)
        
        # For now, suggest a single stock based on risk profile
        # In a full implementation, this would suggest multiple stocks
        if risk_profile == "conservative":
            symbol = "AAPL"  # Example conservative stock
        elif risk_profile == "aggressive":
            symbol = "NVDA"  # Example aggressive stock
        else:
            symbol = "MSFT"  # Example moderate stock
        
        result = self.orchestrator.process_query(symbol, risk_profile, 12)
        recommendation = result["agents"]["portfolio_risk"]["action"]["recommendation"]
        
        portfolio_answer = f"""
#### Portfolio Recommendation for ${amount:,.0f}

**Risk Profile:** {risk_profile.upper()}

**Suggested Allocation:**
- {symbol}: {recommendation.get('allocation', '10-15%')}
- Action: {recommendation.get('action', 'BUY')}

**Reasoning:**
{recommendation.get('reasoning', '')}

**Note:** This is a simplified recommendation. A full portfolio should include diversification across multiple stocks and asset classes.
"""
        
        return {
            "type": "portfolio",
            "amount": amount,
            "risk_profile": risk_profile,
            "result": result,
            "answer": portfolio_answer.strip()
        }
    
    def _handle_data_based_recommendation(self, question_data: Dict) -> Dict:
        """Handle data-based recommendation question"""
        symbol = question_data.get("symbol", "AAPL")  # Default to AAPL if not specified
        
        result = self.orchestrator.process_query(symbol, "moderate", 12)
        
        # Extract key data points
        market_data = result["agents"]["market_data"]["action"]
        fundamentals = result["agents"]["fundamental_news"]["action"]["fundamentals"]
        portfolio_rec = result["agents"]["portfolio_risk"]["action"]["recommendation"]
        
        answer = f"""
#### Data-Based Recommendation for {symbol}

**Market Data:**
- Current Price: ${market_data.get('current_price', 0):.2f}
- Volatility: {market_data.get('volatility', 0):.2f}%
- Trend: {market_data.get('trend', 'unknown').upper()}

**Fundamentals:**
- P/E Ratio: {fundamentals.get('pe_ratio', 'N/A')}
- Profit Margin: {fundamentals.get('profit_margin', 0)*100 if fundamentals.get('profit_margin') else 'N/A':.2f}%
- Revenue Growth: {fundamentals.get('revenue_growth', 0)*100 if fundamentals.get('revenue_growth') else 'N/A':.2f}%

**Recommendation:** {portfolio_rec.get('action', 'HOLD')}
**Allocation:** {portfolio_rec.get('allocation', 'N/A')}

**Reasoning:** {portfolio_rec.get('reasoning', '')}
"""
        
        return {
            "type": "data_based_recommendation",
            "symbol": symbol,
            "result": result,
            "answer": answer.strip()
        }
    
    def _generate_comparison(self, symbol1: str, symbol2: str, result1: Dict, result2: Dict) -> str:
        """Generate comparison between two stocks"""
        market1 = result1["agents"]["market_data"]["action"]
        market2 = result2["agents"]["market_data"]["action"]
        fund1 = result1["agents"]["fundamental_news"]["action"]["fundamentals"]
        fund2 = result2["agents"]["fundamental_news"]["action"]["fundamentals"]
        rec1 = result1["agents"]["portfolio_risk"]["action"]["recommendation"]
        rec2 = result2["agents"]["portfolio_risk"]["action"]["recommendation"]
        
        comparison = f"""
#### Comparison: {symbol1} vs {symbol2}

**Price Comparison:**
- {symbol1}: ${market1.get('current_price', 0):.2f} (Volatility: {market1.get('volatility', 0):.2f}%)
- {symbol2}: ${market2.get('current_price', 0):.2f} (Volatility: {market2.get('volatility', 0):.2f}%)

**Valuation:**
- {symbol1} P/E: {fund1.get('pe_ratio', 'N/A')}
- {symbol2} P/E: {fund2.get('pe_ratio', 'N/A')}

**Recommendations:**
- {symbol1}: {rec1.get('action', 'HOLD')} - {rec1.get('allocation', 'N/A')}
- {symbol2}: {rec2.get('action', 'HOLD')} - {rec2.get('allocation', 'N/A')}

**Summary:**
Based on the analysis, {'both stocks show potential' if rec1.get('action') == rec2.get('action') else f'{symbol1} shows {rec1.get("action")} signal while {symbol2} shows {rec2.get("action")} signal'}.
"""
        
        return comparison.strip()
    
    def _parse_amount(self, amount_str: str) -> int:
        """Parse amount string (e.g., '50k' -> 50000)"""
        amount_str = amount_str.lower().replace('$', '').replace(',', '')
        
        if 'k' in amount_str:
            return int(float(amount_str.replace('k', '')) * 1000)
        elif 'm' in amount_str:
            return int(float(amount_str.replace('m', '')) * 1000000)
        else:
            return int(float(amount_str))

