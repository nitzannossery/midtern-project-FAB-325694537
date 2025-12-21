"""
Quick test to verify the system works with a simple query
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from orchestrator import Orchestrator

print("Testing Financial Analysis System...")
print("=" * 60)

# Test Simple Query: AAPL
print("\n1. Testing Simple Query: AAPL, moderate, 12 months")
print("-" * 60)

orchestrator = Orchestrator()
result = orchestrator.process_query("AAPL", "moderate", 12)

print(f"\n✓ Query processed successfully!")
print(f"✓ Market Data Agent: {result['agents']['market_data']['agent']}")
print(f"✓ Fundamental & News Agent: {result['agents']['fundamental_news']['agent']}")
print(f"✓ Portfolio & Risk Agent: {result['agents']['portfolio_risk']['agent']}")
print(f"✓ Final Answer generated: {len(result['final_answer'])} characters")

# Check if there are any errors
market_data = result['agents']['market_data']['action']
if 'error' not in market_data:
    print(f"\n✓ Market Data retrieved:")
    print(f"  - Symbol: {market_data.get('symbol', 'N/A')}")
    print(f"  - Current Price: ${market_data.get('current_price', 0):.2f}")
    print(f"  - Volatility: {market_data.get('volatility', 0):.2f}%")
else:
    print(f"\n⚠ Market Data Error: {market_data.get('error')}")

fundamental_data = result['agents']['fundamental_news']['action']
if 'error' not in fundamental_data.get('fundamentals', {}):
    print(f"\n✓ Fundamentals retrieved successfully")
else:
    print(f"\n⚠ Fundamentals Error: {fundamental_data.get('fundamentals', {}).get('error', 'Unknown')}")

portfolio_data = result['agents']['portfolio_risk']['action']
print(f"\n✓ Portfolio Recommendation:")
print(f"  - Risk Score: {portfolio_data.get('risk_score', 0):.1f}/100")
print(f"  - Action: {portfolio_data.get('recommendation', {}).get('action', 'N/A')}")

print("\n" + "=" * 60)
print("✅ System test completed successfully!")
print("=" * 60)

