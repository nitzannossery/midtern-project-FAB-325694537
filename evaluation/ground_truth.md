# Ground Truth for Evaluation

This document contains expected outputs and evaluation criteria for the Financial Analysis Multi-Agent System.

## Evaluation Metrics

### 1. Correctness
- **Definition**: Outputs match known or provided ground truth
- **Criteria**:
  - Market data values are accurate (within reasonable tolerance)
  - Fundamental metrics are correctly computed
  - Risk scores align with expected ranges
  - Recommendations match risk profile constraints

### 2. Faithfulness
- **Definition**: No unsupported assumptions or hallucinations
- **Criteria**:
  - All data comes from actual API calls or provided inputs
  - No fabricated numbers or metrics
  - Reasoning is based on retrieved data
  - Clear distinction between data and inference

### 3. Coverage
- **Definition**: All relevant inputs and constraints are considered
- **Criteria**:
  - All three agents produce outputs
  - Risk profile is properly incorporated
  - Investment horizon affects recommendations
  - Final answer aggregates all agent outputs

## Test Cases

### Simple Query: AAPL
**Input:**
- Symbol: AAPL
- Risk Profile: moderate
- Investment Horizon: 12 months

**Expected Behavior:**
- Market Data Agent retrieves AAPL price data
- Fundamental & News Agent provides Apple fundamentals
- Portfolio & Risk Agent generates moderate-risk recommendation
- Final Answer aggregates all outputs coherently

**Validation Points:**
- ✓ Market data shows AAPL current price
- ✓ Fundamentals include P/E ratio, profit margin
- ✓ Recommendation aligns with "moderate" risk profile
- ✓ All agents produce non-empty outputs

### Complex Query: TSLA
**Input:**
- Symbol: TSLA
- Risk Profile: conservative
- Investment Horizon: 24 months

**Expected Behavior:**
- Market Data Agent retrieves TSLA data (higher volatility expected)
- Fundamental & News Agent analyzes Tesla fundamentals
- Portfolio & Risk Agent applies conservative constraints strictly
- Final Answer reflects conservative risk profile limitations

**Validation Points:**
- ✓ Market data shows TSLA volatility (likely >30%)
- ✓ Fundamentals include Tesla-specific metrics
- ✓ Recommendation is more cautious due to conservative profile
- ✓ Long-term horizon (24 months) is considered
- ✓ Risk score affects allocation recommendation

## Agent Output Validation

### Market Data Agent
- Must include: current_price, price_change, volatility, trend
- Data quality assessment should be present
- No errors for valid stock symbols

### Fundamental & News Agent
- Must include: P/E ratio, profit margin, debt/equity (if available)
- News items should be recent and relevant
- Sector/industry information included

### Portfolio & Risk Agent
- Must include: risk_score, recommendation action, allocation percentage
- Reasoning should reference risk profile
- Horizon considerations should be visible

## Screenshots Directory

Place evaluation screenshots in `evaluation/screenshots/`:
- `correctness.png` - Demonstrates accurate outputs
- `faithfulness.png` - Shows data-driven reasoning
- `coverage.png` - Illustrates complete agent coordination

## Notes

- Real-time data may vary, so focus on structure and reasoning rather than exact values
- Some fundamental metrics may be unavailable for certain stocks (handle gracefully)
- News items change frequently, so focus on presence/absence rather than specific articles

