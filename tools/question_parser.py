"""
Question Parser
Identifies question type and extracts parameters from natural language questions
"""

import re
from typing import Dict, Optional, Tuple


class QuestionParser:
    """Parses natural language questions and extracts relevant parameters"""
    
    # Simple question patterns
    SIMPLE_PATTERNS = {
        'current_price': [
            r"what is the current price of (\w+)",
            r"current price of (\w+)",
            r"price of (\w+)",
            r"how much is (\w+)",
        ],
        'yesterday_price': [
            r"what was (\w+)'s closing price yesterday",
            r"(\w+) closing price yesterday",
            r"yesterday's closing price for (\w+)",
        ],
        'market_cap': [
            r"what is (\w+)'s market cap",
            r"market cap of (\w+)",
            r"(\w+) market capitalization",
        ],
    }
    
    # Complex question patterns
    COMPLEX_PATTERNS = {
        'investment_recommendation': [
            r"is (\w+) a good investment",
            r"should i invest in (\w+)",
            r"investment recommendation for (\w+)",
            r"buy recommendation for (\w+)",
        ],
        'comparison': [
            r"compare (\w+) and (\w+)",
            r"(\w+) vs (\w+)",
            r"difference between (\w+) and (\w+)",
        ],
        'portfolio': [
            r"build.*portfolio.*\$?(\d+[km]?)",
            r"conservative portfolio.*\$?(\d+[km]?)",
            r"portfolio.*\$?(\d+[km]?)",
        ],
        'data_based_recommendation': [
            r"based.*data.*news.*market.*recommendation",
            r"suggest.*buy.*recommendation",
            r"recommendation.*based.*data",
        ],
    }
    
    @staticmethod
    def parse(question: str) -> Dict:
        """
        Parse a natural language question
        
        Args:
            question: Natural language question string
            
        Returns:
            Dictionary with question type and extracted parameters
        """
        question_lower = question.lower().strip()
        
        # Check for simple questions
        for q_type, patterns in QuestionParser.SIMPLE_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, question_lower)
                if match:
                    symbol = match.group(1).upper()
                    return {
                        "type": "simple",
                        "subtype": q_type,
                        "symbol": symbol,
                        "original_question": question
                    }
        
        # Check for complex questions
        for q_type, patterns in QuestionParser.COMPLEX_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, question_lower)
                if match:
                    if q_type == "comparison":
                        # Extract two symbols
                        symbols_match = re.search(r"(\w+)\s+(?:and|vs)\s+(\w+)", question_lower)
                        if symbols_match:
                            return {
                                "type": "complex",
                                "subtype": q_type,
                                "symbols": [symbols_match.group(1).upper(), symbols_match.group(2).upper()],
                                "original_question": question
                            }
                    elif q_type == "portfolio":
                        # Extract amount
                        amount_match = re.search(r"\$?(\d+[km]?)", question_lower)
                        amount = amount_match.group(1) if amount_match else None
                        # Extract risk profile
                        risk_profile = "moderate"
                        if "conservative" in question_lower:
                            risk_profile = "conservative"
                        elif "aggressive" in question_lower:
                            risk_profile = "aggressive"
                        return {
                            "type": "complex",
                            "subtype": q_type,
                            "amount": amount,
                            "risk_profile": risk_profile,
                            "original_question": question
                        }
                    elif q_type == "investment_recommendation":
                        # Extract symbol and horizon
                        symbol_match = re.search(r"(\w+)", question_lower)
                        symbol = symbol_match.group(1).upper() if symbol_match else None
                        # Extract horizon
                        horizon_match = re.search(r"(\d+)\s*(?:month|months|year|years)", question_lower)
                        horizon = int(horizon_match.group(1)) if horizon_match else 12
                        if "year" in question_lower.lower():
                            horizon = horizon * 12
                        # Extract risk profile
                        risk_profile = "moderate"
                        if "conservative" in question_lower:
                            risk_profile = "conservative"
                        elif "aggressive" in question_lower:
                            risk_profile = "aggressive"
                        return {
                            "type": "complex",
                            "subtype": q_type,
                            "symbol": symbol,
                            "horizon_months": horizon,
                            "risk_profile": risk_profile,
                            "original_question": question
                        }
                    elif q_type == "data_based_recommendation":
                        # Extract symbol if mentioned
                        symbol_match = re.search(r"for (\w+)", question_lower)
                        symbol = symbol_match.group(1).upper() if symbol_match else None
                        return {
                            "type": "complex",
                            "subtype": q_type,
                            "symbol": symbol,
                            "original_question": question
                        }
        
        # Default: treat as complex investment question
        # Try to extract symbol
        symbol_match = re.search(r"\b([A-Z]{2,5})\b", question.upper())
        symbol = symbol_match.group(1) if symbol_match else None
        
        return {
            "type": "complex",
            "subtype": "investment_recommendation",
            "symbol": symbol,
            "horizon_months": 12,
            "risk_profile": "moderate",
            "original_question": question
        }

