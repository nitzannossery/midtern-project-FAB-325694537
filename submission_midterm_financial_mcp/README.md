# Financial Analysis Multi-Agent System

A **Multi-Agent Control Project (MCP)** system for financial analysis that coordinates specialized agents to provide comprehensive investment recommendations.

## Overview

This system operates as a Financial Analysis Multi-Agent System with a central Orchestrator that coordinates three specialized agents:

1. **Market Data Agent** - Retrieves and normalizes market-related data
2. **Fundamental & News Agent** - Analyzes company fundamentals and recent news
3. **Portfolio & Risk Agent** - Generates investment recommendations under risk constraints

Each agent follows the **ReAct pattern** (Reason → Act → Output) to ensure explainable and structured decision-making.

## Architecture

```
┌─────────────────────────────────────────┐
│         Orchestrator                    │
│  (Coordinates & Aggregates Outputs)    │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼──────┐
│Market │ │Fund.  │ │Portfolio │
│Data   │ │& News │ │& Risk    │
│Agent  │ │Agent  │ │Agent     │
└───────┘ └───────┘ └──────────┘
```

### Agent Responsibilities

#### 1. Market Data Agent
- **Role**: Retrieve and normalize market-related data (prices, returns, benchmarks, FX)
- **Reason**: Determine required symbols, investment horizon, data types, and potential data quality issues
- **Act**: Fetch a minimal, clean, and structured time-series dataset
- **Output**: Short summary of trends and relevant observations

#### 2. Fundamental & News Agent
- **Role**: Analyze company fundamentals and recent news
- **Reason**: Decide which financial ratios, statements, and news signals are relevant to the query
- **Act**: Compute key metrics and produce a concise fundamental snapshot, including sentiment
- **Output**: Structured summary of financial health and qualitative signals

#### 3. Portfolio & Risk Agent
- **Role**: Generate investment recommendations under risk constraints
- **Reason**: Assess user risk profile, constraints, and scenario sensitivity
- **Act**: Compute risk-aware recommendations and stress considerations
- **Output**: Clear recommendation aligned with the specified risk profile

## ReAct Pattern

Each agent follows the ReAct (Reasoning and Acting) pattern:

1. **Reason**: Analyze the query and determine what information/actions are needed
2. **Act**: Execute the necessary data retrieval or computation
3. **Output**: Generate a structured, explainable result

This ensures:
- No hallucination of missing data
- All conclusions are based on provided inputs or retrieved structured data
- Professional, concise, and explainable outputs suitable for academic evaluation

## Metadata Usage

The system relies on structured metadata such as asset symbol, risk profile, and investment horizon to guide retrieval and reasoning. This allows handling complex queries that cannot be resolved via pure semantic similarity.

The metadata structure includes:
- **Asset Symbol**: Stock ticker (e.g., AAPL, TSLA, NVDA)
- **Risk Profile**: User's risk tolerance (conservative, moderate, aggressive)
- **Investment Horizon**: Time frame in months for the investment decision

This structured approach enables:
- Precise data retrieval from financial APIs
- Context-aware reasoning based on user constraints
- Personalized recommendations aligned with risk profiles
- Handling of both simple factual queries and complex investment questions

## Installation

**Note:** Use `python3` (not `python`) on macOS.

1. Clone the repository:
```bash
git clone <repository-url>
cd "Financial Analyst bot- midtern project"
```

2. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

3. Run the Streamlit UI:
```bash
python3 -m streamlit run ui/app.py
```

## Usage

### Two query types

The system supports two main query types:

#### Simple Query
- **Symbol**: AAPL
- **Risk Profile**: moderate
- **Investment Horizon**: 12 months

#### Complex Query
- **Symbol**: TSLA
- **Risk Profile**: conservative
- **Investment Horizon**: 24 months

### How to Run

1. Start the Streamlit application:
```bash
python3 -m streamlit run ui/app.py
```

2. Enter query parameters in the sidebar:
   - Stock symbol (e.g., AAPL, TSLA)
   - Risk profile (conservative, moderate, aggressive)
   - Investment horizon in months

3. Click "Run Analysis" to process the query

4. View results in organized tabs:
   - **Final Answer**: Aggregated recommendation
   - **Market Data Agent**: Market analysis output
   - **Fundamental & News Agent**: Fundamentals and news analysis
   - **Portfolio & Risk Agent**: Risk-aware recommendation

## Evaluation

The system is evaluated on three key metrics:

### 1. Correctness
- Outputs match known or provided ground truth
- Accurate data retrieval and computation
- Proper alignment with risk profiles

### 2. Faithfulness
- No unsupported assumptions or hallucinations
- All conclusions based on retrieved data
- Transparent reasoning process

### 3. Coverage
- All relevant inputs and constraints are considered
- Complete agent coordination
- Comprehensive final answer aggregation

## Hard+ Tabular Demo

The system includes a Hard+ Tabular Demo feature that demonstrates reasoning over structured tabular financial data. This bonus feature showcases the system's ability to:

- Process structured tabular data (quarterly financial metrics)
- Answer factual questions about the data (e.g., "Which quarter has the highest net income?")
- Provide explainable reasoning with evidence
- Return ground truth comparisons

### Using the Tabular Demo

1. In the Streamlit UI, enable the **"Hard+ Tabular Demo (Bonus)"** checkbox in the sidebar
2. The system will display:
   - The financial data table
   - The question being answered
   - The computed answer (e.g., "Q4")
   - Detailed reasoning and evidence
   - Ground truth comparison

The demo uses a sample dataset with quarterly revenue and net income data, and demonstrates that Q4 has the highest net income (30M) compared to other quarters.

## Bonus: Advanced Reasoning

The system supports advanced reasoning over tabular financial data. When provided with structured financial tables, the system can answer factual questions such as:

- "Which quarter has the highest net income?"
- "What was the revenue growth rate?"
- "Compare debt levels across periods"

## Project Structure

```
Financial Analyst bot- midtern project/
├── agents/
│   ├── __init__.py
│   ├── market_data_agent.py
│   ├── fundamental_news_agent.py
│   └── portfolio_risk_agent.py
├── tools/
│   ├── __init__.py
│   ├── data_fetcher.py
│   └── financial_calculator.py
├── ui/
│   └── app.py
├── evaluation/
│   ├── ground_truth.md
│   └── screenshots/
├── orchestrator.py
├── requirements.txt
└── README.md
```

## Dependencies

- `streamlit` - Web UI framework
- `yfinance` - Financial data retrieval
- `pandas` - Data manipulation
- `numpy` - Numerical computations

## Final Answer Requirements

The Orchestrator aggregates all agent outputs into a coherent Final Answer that:

- Reflects differences between simple and complex queries
- Clearly justifies recommendations based on agent reasoning
- Demonstrates modular multi-agent reasoning
- Shows ReAct-based decision making
- Is suitable for academic assessment

## License

This project is developed for academic purposes as part of a midterm project.

## Author

Financial Analysis Multi-Agent System - MCP Implementation

