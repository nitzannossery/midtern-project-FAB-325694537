"""
Quick setup verification script
Run this to verify all components are working
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        sys.path.append(str(Path(__file__).parent))
        from orchestrator import Orchestrator
        print("✓ Orchestrator imported successfully")
        
        from agents.market_data_agent import MarketDataAgent
        print("✓ MarketDataAgent imported successfully")
        
        from agents.fundamental_news_agent import FundamentalNewsAgent
        print("✓ FundamentalNewsAgent imported successfully")
        
        from agents.portfolio_risk_agent import PortfolioRiskAgent
        print("✓ PortfolioRiskAgent imported successfully")
        
        from tools.data_fetcher import DataFetcher
        print("✓ DataFetcher imported successfully")
        
        from tools.financial_calculator import FinancialCalculator
        print("✓ FinancialCalculator imported successfully")
        
        # Test tabular demo
        from tools.tabular_demo import answer_highest_net_income
        tabular_result = answer_highest_net_income()
        assert tabular_result["answer"] == "Q4", f"Expected Q4, got {tabular_result['answer']}"
        assert tabular_result["final_answer"] == "Q4 has the highest net income (30M).", f"Unexpected final_answer: {tabular_result['final_answer']}"
        print("✓ Tabular demo test passed")
        
        print("\n✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nPlease install dependencies:")
        print("  pip3 install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)

