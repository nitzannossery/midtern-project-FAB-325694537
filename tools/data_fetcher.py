"""
Data Fetcher Tool
Retrieves market data, fundamentals, and news
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class DataFetcher:
    """Fetches financial data from various sources"""
    
    @staticmethod
    def get_market_data(symbol: str, period: str = "1y") -> Dict:
        """
        Fetch market data for a symbol
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1y, 2y, etc.)
            
        Returns:
            Dictionary with price data and statistics
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return {"error": f"No data found for {symbol}"}
            
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price) * 100 if prev_price > 0 else 0
            
            # Calculate returns
            returns = hist['Close'].pct_change().dropna()
            volatility = returns.std() * (252 ** 0.5) * 100  # Annualized volatility
            
            return {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "price_change": round(price_change, 2),
                "price_change_pct": round(price_change_pct, 2),
                "volatility": round(volatility, 2),
                "data_points": len(hist),
                "period": period,
                "trend": "upward" if price_change > 0 else "downward",
                "data_quality": "good" if len(hist) > 50 else "limited"
            }
        except Exception as e:
            return {"error": f"Error fetching market data: {str(e)}"}
    
    @staticmethod
    def get_fundamentals(symbol: str) -> Dict:
        """
        Fetch fundamental data for a symbol
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary with fundamental metrics
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract key metrics
            fundamentals = {
                "symbol": symbol,
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", None),
                "forward_pe": info.get("forwardPE", None),
                "peg_ratio": info.get("pegRatio", None),
                "price_to_book": info.get("priceToBook", None),
                "debt_to_equity": info.get("debtToEquity", None),
                "roe": info.get("returnOnEquity", None),
                "profit_margin": info.get("profitMargins", None),
                "revenue_growth": info.get("revenueGrowth", None),
                "earnings_growth": info.get("earningsGrowth", None),
                "current_ratio": info.get("currentRatio", None),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown")
            }
            
            return fundamentals
        except Exception as e:
            return {"error": f"Error fetching fundamentals: {str(e)}"}
    
    @staticmethod
    def get_news(symbol: str, limit: int = 5) -> List[Dict]:
        """
        Fetch recent news for a symbol
        
        Args:
            symbol: Stock ticker symbol
            limit: Maximum number of news items
            
        Returns:
            List of news dictionaries
        """
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news[:limit]
            
            if not news:
                return []
            
            news_list = []
            for item in news:
                # Handle different news formats from yfinance
                # New format has content nested
                if "content" in item and isinstance(item["content"], dict):
                    content = item["content"]
                    title = content.get("title", "")
                    # Try to get publisher from provider
                    provider = content.get("provider", {})
                    if isinstance(provider, dict):
                        publisher = provider.get("displayName", "Unknown")
                    else:
                        publisher = "Unknown"
                    # Get link from canonicalUrl or clickThroughUrl
                    link = ""
                    if "canonicalUrl" in content and isinstance(content["canonicalUrl"], dict):
                        link = content["canonicalUrl"].get("url", "")
                    elif "clickThroughUrl" in content and isinstance(content["clickThroughUrl"], dict):
                        link = content["clickThroughUrl"].get("url", "")
                    published = content.get("pubDate", "")
                else:
                    # Old format or direct format
                    title = item.get("title", "")
                    publisher = item.get("publisher", item.get("provider", {}).get("displayName", "Unknown") if isinstance(item.get("provider"), dict) else "Unknown")
                    link = item.get("link", item.get("canonicalUrl", {}).get("url", "") if isinstance(item.get("canonicalUrl"), dict) else "")
                    published = item.get("providerPublishTime", item.get("pubDate", ""))
                
                if title:  # Only add if we have a title
                    news_list.append({
                        "title": title,
                        "publisher": publisher if publisher else "Unknown",
                        "link": link,
                        "published": published
                    })
            
            return news_list if news_list else []
        except Exception as e:
            return [{"error": f"Error fetching news: {str(e)}"}]


