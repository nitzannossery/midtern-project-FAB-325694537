"""
Fundamental & News Agent
Analyzes company fundamentals and recent news following ReAct pattern
"""

from typing import Dict, Any, List
from tools.data_fetcher import DataFetcher


class FundamentalNewsAgent:
    """
    Fundamental & News Agent - Analyzes fundamentals and news sentiment
    Follows ReAct pattern: Reason → Act
    """
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
    
    def analyze(self, symbol: str) -> Dict[str, Any]:
        """
        Analyze fundamentals and news for a given symbol
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary with analysis results
        """
        # REASON: Determine relevant metrics and news signals
        reason = self._reason(symbol)
        
        # ACT: Fetch fundamentals and news
        action_result = self._act(symbol)
        
        # OUTPUT: Generate structured summary
        output = self._generate_output(action_result, reason)
        
        return {
            "agent": "Fundamental & News Agent",
            "reason": reason,
            "action": action_result,
            "output": output
        }
    
    def _reason(self, symbol: str) -> str:
        """
        Reason: Determine which metrics and news are relevant
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Reasoning string
        """
        reason = (
            f"Required analysis for {symbol}:\n"
            f"- Financial ratios: P/E, P/B, Debt/Equity, ROE, Profit Margin\n"
            f"- Growth metrics: Revenue growth, Earnings growth\n"
            f"- Liquidity: Current ratio\n"
            f"- News signals: Recent news sentiment and key events\n"
            f"- Sector/Industry context: Compare against sector averages"
        )
        
        return reason
    
    def _act(self, symbol: str) -> Dict[str, Any]:
        """
        Act: Fetch fundamentals and news
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary with fundamentals and news
        """
        fundamentals = self.data_fetcher.get_fundamentals(symbol)
        news = self.data_fetcher.get_news(symbol, limit=5)
        
        return {
            "fundamentals": fundamentals,
            "news": news
        }
    
    def _generate_output(self, data: Dict[str, Any], reason: str) -> str:
        """
        Generate structured output summary
        
        Args:
            data: Fetched fundamentals and news
            reason: Reasoning string
            
        Returns:
            Formatted output string
        """
        fundamentals = data.get("fundamentals", {})
        news = data.get("news", [])
        
        if "error" in fundamentals:
            return f"Error: {fundamentals['error']}"
        
        # Build fundamentals summary
        output = f"Fundamental Analysis for {fundamentals.get('symbol', 'N/A')}:\n\n"
        output += "Financial Health:\n"
        
        # Valuation metrics
        pe = fundamentals.get("pe_ratio")
        if pe:
            pe_status = "Undervalued" if pe < 15 else "Fairly valued" if pe < 25 else "Overvalued"
            output += f"- P/E Ratio: {pe:.2f} ({pe_status})\n"
        
        pb = fundamentals.get("price_to_book")
        if pb:
            output += f"- P/B Ratio: {pb:.2f}\n"
        
        # Profitability
        profit_margin = fundamentals.get("profit_margin")
        if profit_margin:
            margin_status = "Strong" if profit_margin > 0.15 else "Moderate" if profit_margin > 0.05 else "Weak"
            output += f"- Profit Margin: {profit_margin*100:.2f}% ({margin_status})\n"
        
        roe = fundamentals.get("roe")
        if roe:
            output += f"- ROE: {roe*100:.2f}%\n"
        
        # Growth
        revenue_growth = fundamentals.get("revenue_growth")
        if revenue_growth:
            output += f"- Revenue Growth: {revenue_growth*100:.2f}%\n"
        
        earnings_growth = fundamentals.get("earnings_growth")
        if earnings_growth:
            output += f"- Earnings Growth: {earnings_growth*100:.2f}%\n"
        
        # Financial strength
        debt_equity = fundamentals.get("debt_to_equity")
        if debt_equity:
            debt_status = "Low" if debt_equity < 0.5 else "Moderate" if debt_equity < 1.0 else "High"
            output += f"- Debt/Equity: {debt_equity:.2f} ({debt_status})\n"
        
        current_ratio = fundamentals.get("current_ratio")
        if current_ratio:
            output += f"- Current Ratio: {current_ratio:.2f}\n"
        
        # Sector info
        sector = fundamentals.get("sector", "Unknown")
        industry = fundamentals.get("industry", "Unknown")
        output += f"\nSector: {sector}\n"
        output += f"Industry: {industry}\n"
        
        # News summary
        output += "\n**Recent News:**\n\n"
        if news and len(news) > 0 and "error" not in (news[0] if news else {}):
            for i, item in enumerate(news[:5], 1):  # Show up to 5 news items
                title = item.get("title", "No title")
                publisher = item.get("publisher", "Unknown")
                link = item.get("link", "")
                if title and title != "No title":
                    output += f"{i}. **{title}**\n"
                    output += f"   Source: {publisher}\n"
                    if link:
                        output += f"   Link: {link}\n"
                    output += "\n"
        else:
            output += "No recent news available or error fetching news.\n\n"
        
        # Sentiment assessment
        output += "\nQualitative Signals: "
        if profit_margin and profit_margin > 0.1 and revenue_growth and revenue_growth > 0:
            output += "Positive fundamentals with growth trajectory"
        elif debt_equity and debt_equity > 1.0:
            output += "High debt levels require caution"
        else:
            output += "Mixed signals, requires deeper analysis"
        
        return output

