"""
Simple Query Handler
Handles simple factual questions about stocks
"""

from typing import Dict
from tools.data_fetcher import DataFetcher
import yfinance as yf


class SimpleQueryHandler:
    """Handles simple questions about stock data"""
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
    
    def handle(self, question_data: Dict) -> str:
        """
        Handle a simple question
        
        Args:
            question_data: Parsed question data
            
        Returns:
            Answer string
        """
        subtype = question_data.get("subtype")
        symbol = question_data.get("symbol")
        
        if not symbol:
            return "Error: Could not identify stock symbol in question."
        
        if subtype == "current_price":
            return self._get_current_price(symbol)
        elif subtype == "yesterday_price":
            return self._get_yesterday_price(symbol)
        elif subtype == "market_cap":
            return self._get_market_cap(symbol)
        else:
            return f"Unknown question type: {subtype}"
    
    def _get_current_price(self, symbol: str) -> str:
        """Get current price"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            current_price = info.get("currentPrice") or info.get("regularMarketPrice")
            
            if current_price:
                return f"The current price of {symbol} is ${current_price:.2f}"
            else:
                # Fallback to historical data
                hist = ticker.history(period="1d")
                if not hist.empty:
                    price = hist['Close'].iloc[-1]
                    return f"The current price of {symbol} is ${price:.2f}"
                else:
                    return f"Could not retrieve current price for {symbol}"
        except Exception as e:
            return f"Error retrieving price for {symbol}: {str(e)}"
    
    def _get_yesterday_price(self, symbol: str) -> str:
        """Get yesterday's closing price"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")
            
            if len(hist) >= 2:
                yesterday_price = hist['Close'].iloc[-2]  # Second to last is yesterday
                date = hist.index[-2].strftime("%Y-%m-%d")
                return f"{symbol}'s closing price yesterday ({date}) was ${yesterday_price:.2f}"
            elif len(hist) == 1:
                yesterday_price = hist['Close'].iloc[-1]
                date = hist.index[-1].strftime("%Y-%m-%d")
                return f"{symbol}'s most recent closing price ({date}) was ${yesterday_price:.2f}"
            else:
                return f"Could not retrieve yesterday's price for {symbol}"
        except Exception as e:
            return f"Error retrieving yesterday's price for {symbol}: {str(e)}"
    
    def _get_market_cap(self, symbol: str) -> str:
        """Get market capitalization"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            market_cap = info.get("marketCap")
            
            if market_cap:
                # Format market cap
                if market_cap >= 1e12:
                    formatted_cap = f"${market_cap/1e12:.2f}T"
                elif market_cap >= 1e9:
                    formatted_cap = f"${market_cap/1e9:.2f}B"
                elif market_cap >= 1e6:
                    formatted_cap = f"${market_cap/1e6:.2f}M"
                else:
                    formatted_cap = f"${market_cap:,.0f}"
                
                return f"{symbol}'s market cap is {formatted_cap}"
            else:
                return f"Could not retrieve market cap for {symbol}"
        except Exception as e:
            return f"Error retrieving market cap for {symbol}: {str(e)}"

