"""
Market Data Agent
Retrieves and normalizes market-related data following ReAct pattern
"""

from typing import Dict, Any
from tools.data_fetcher import DataFetcher


class MarketDataAgent:
    """
    Market Data Agent - Responsible for market data retrieval and normalization
    Follows ReAct pattern: Reason → Act
    """
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
    
    def analyze(self, symbol: str, horizon_months: int) -> Dict[str, Any]:
        """
        Analyze market data for a given symbol
        
        Args:
            symbol: Stock ticker symbol
            horizon_months: Investment horizon in months
            
        Returns:
            Dictionary with analysis results
        """
        # REASON: Determine required data parameters
        reason = self._reason(symbol, horizon_months)
        
        # ACT: Fetch and process market data
        action_result = self._act(symbol, horizon_months)
        
        # OUTPUT: Generate summary
        output = self._generate_output(action_result, reason)
        
        return {
            "agent": "Market Data Agent",
            "reason": reason,
            "action": action_result,
            "output": output
        }
    
    def _reason(self, symbol: str, horizon_months: int) -> str:
        """
        Reason: Determine what data is needed
        
        Args:
            symbol: Stock ticker symbol
            horizon_months: Investment horizon
            
        Returns:
            Reasoning string
        """
        # Determine period based on horizon
        if horizon_months >= 24:
            period = "2y"
        elif horizon_months >= 12:
            period = "1y"
        else:
            period = "6mo"
        
        reason = (
            f"Required data for {symbol}:\n"
            f"- Investment horizon: {horizon_months} months → using period: {period}\n"
            f"- Need: price data, returns, volatility metrics\n"
            f"- Data quality check: verify sufficient data points\n"
            f"- Trend analysis: identify price direction and momentum"
        )
        
        return reason
    
    def _act(self, symbol: str, horizon_months: int) -> Dict[str, Any]:
        """
        Act: Fetch market data
        
        Args:
            symbol: Stock ticker symbol
            horizon_months: Investment horizon
            
        Returns:
            Market data dictionary
        """
        # Determine period
        if horizon_months >= 24:
            period = "2y"
        elif horizon_months >= 12:
            period = "1y"
        else:
            period = "6mo"
        
        # Fetch data
        market_data = self.data_fetcher.get_market_data(symbol, period)
        
        return market_data
    
    def _generate_output(self, market_data: Dict[str, Any], reason: str) -> str:
        """
        Generate output summary
        
        Args:
            market_data: Fetched market data
            reason: Reasoning string
            
        Returns:
            Formatted output string
        """
        if "error" in market_data:
            return f"Error: {market_data['error']}"
        
        output = (
            f"Market Data Summary for {market_data.get('symbol', 'N/A')}:\n"
            f"- Current Price: ${market_data.get('current_price', 0):.2f}\n"
            f"- Price Change: {market_data.get('price_change', 0):+.2f} "
            f"({market_data.get('price_change_pct', 0):+.2f}%)\n"
            f"- Annualized Volatility: {market_data.get('volatility', 0):.2f}%\n"
            f"- Trend: {market_data.get('trend', 'unknown').upper()}\n"
            f"- Data Quality: {market_data.get('data_quality', 'unknown')} "
            f"({market_data.get('data_points', 0)} data points)\n"
            f"- Observation: {'High volatility detected' if market_data.get('volatility', 0) > 30 else 'Moderate volatility'}"
        )
        
        return output

