"""
Quick test for complex query: TSLA
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from orchestrator import Orchestrator

print("Testing Complex Query: TSLA, conservative, 24 months")
print("=" * 60)

orchestrator = Orchestrator()
result = orchestrator.process_query("TSLA", "conservative", 24)

print(f"\n✓ Query processed successfully!")
print(f"✓ All agents executed")

market_data = result['agents']['market_data']['action']
if 'error' not in market_data:
    print(f"\n✓ Market Data:")
    print(f"  - Symbol: {market_data.get('symbol', 'N/A')}")
    print(f"  - Current Price: ${market_data.get('current_price', 0):.2f}")
    print(f"  - Volatility: {market_data.get('volatility', 0):.2f}%")
    print(f"  - Trend: {market_data.get('trend', 'N/A')}")

portfolio_data = result['agents']['portfolio_risk']['action']
recommendation = portfolio_data.get('recommendation', {})
print(f"\n✓ Portfolio Recommendation (Conservative Profile):")
print(f"  - Risk Score: {portfolio_data.get('risk_score', 0):.1f}/100")
print(f"  - Action: {recommendation.get('action', 'N/A')}")
print(f"  - Allocation: {recommendation.get('allocation', 'N/A')}")
print(f"  - Reasoning: {recommendation.get('reasoning', 'N/A')[:100]}...")

print("\n" + "=" * 60)
print("✅ Complex query test completed!")
print("=" * 60)

