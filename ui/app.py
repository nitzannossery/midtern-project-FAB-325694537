"""
Streamlit UI for Financial Analysis Multi-Agent System
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from orchestrator import Orchestrator
from tools.question_parser import QuestionParser
from tools.simple_query_handler import SimpleQueryHandler
from tools.complex_query_handler import ComplexQueryHandler

# Page configuration
st.set_page_config(
    page_title="Financial Analysis Multi-Agent System",
    page_icon="📊",
    layout="wide"
)

# Initialize orchestrator
@st.cache_resource
def get_orchestrator():
    return Orchestrator()

orchestrator = get_orchestrator()

# Title and description
st.title("📊 Financial Analysis Multi-Agent System")
st.markdown("""
**Multi-Agent Control Project (MCP)** - Financial Analysis System
- Market Data Agent
- Fundamental & News Agent  
- Portfolio & Risk Agent
""")

st.divider()

# Sidebar for query input
with st.sidebar:
    st.header("Query Input")
    
    # Hard+ Tabular Demo toggle
    use_tabular_demo = st.checkbox(
        "Hard+ Tabular Demo (Bonus)",
        value=False,
        help="Demonstrate reasoning over structured tabular data"
    )
    
    st.divider()
    
    # Question mode selector (only if tabular demo is off)
    if not use_tabular_demo:
        query_mode = st.radio(
            "Query Mode",
            options=["Natural Language", "Form Input"],
            index=0,
            help="Choose how to input your query"
        )
    else:
        query_mode = None
    
    if query_mode == "Natural Language":
        question = st.text_area(
            "Ask a question",
            value="",
            height=100,
            help="Examples:\n- What is the current price of AAPL?\n- Is AAPL a good investment for the next 12 months given moderate risk?\n- Compare NVDA and AMD for long-term AI exposure"
        )
        
        st.markdown("### Example Questions")
        st.markdown("""
        **Simple:**
        - What is the current price of AAPL?
        - What was TSLA's closing price yesterday?
        - What is NVDA's market cap?
        
        **Complex:**
        - Is AAPL a good investment for the next 12 months given moderate risk?
        - Compare NVDA and AMD for long-term AI exposure
        - Build a conservative portfolio with $50,000
        """)
        
        run_button = st.button("🚀 Ask Question", type="primary", use_container_width=True)
        symbol = None
        risk_profile = None
        horizon_months = None
    else:
        st.header("Query Parameters")
        
        symbol = st.text_input(
            "Symbol",
            value="AAPL",
            help="Stock ticker symbol (e.g., AAPL, TSLA)"
        ).upper()
        
        risk_profile = st.selectbox(
            "Risk Profile",
            options=["conservative", "moderate", "aggressive"],
            index=1,
            help="Your risk tolerance level"
        )
        
        horizon_months = st.number_input(
            "Investment Horizon (months)",
            min_value=1,
            max_value=60,
            value=12,
            step=1,
            help="Investment time horizon in months"
        )
        
        st.divider()
        
        st.markdown("### Query Types")
        st.markdown("""
        **Simple Query:**
        - Symbol: AAPL
        - Risk: moderate
        - Horizon: 12
        
        **Complex Query:**
        - Symbol: TSLA
        - Risk: conservative
        - Horizon: 24
        """)
        
        run_button = st.button("🚀 Run Analysis", type="primary", use_container_width=True)
        question = None

# Main content area
if use_tabular_demo:
    st.title("Financial Analysis Multi-Agent System")
    st.subheader("Hard+ Tabular Reasoning Demo (Bonus)")

    result = orchestrator.process_tabular_demo()

    st.markdown("### Input Table")
    st.table(result["tabular_data"])

    st.markdown("### Question")
    st.write(result["question"])

    st.markdown("### ✅ Answer")
    st.write(result["answer"])

    st.markdown("### Evidence (from table)")
    st.json(result["evidence"])

    st.markdown("### ReAct Summary")
    st.write("**Reason:**", result["reason_summary"])
    st.write("**Act:**", result["act_summary"])

    st.markdown("### Final Answer")
    st.success(result["final_answer"])
    st.caption(f"Confidence: {result['confidence']:.2f}")

    st.markdown("### Evaluation")
    
    # Ground truth comparison
    expected_answer = "Q4"
    is_correct = result["answer"] == expected_answer
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Ground Truth:**")
        st.info(expected_answer)
    with col2:
        st.markdown("**Answer Match:**")
        if is_correct:
            st.success("✓ Correct")
        else:
            st.error("✗ Incorrect")
    
    # Evaluation checks (transparent)
    st.markdown("**Evaluation Checks (transparent):**")
    st.json(result["checks"])

    st.stop()

elif run_button:
    if query_mode == "Natural Language":
        if not question or not question.strip():
            st.error("Please enter a question")
        else:
            # Show loading spinner
            with st.spinner("Processing your question..."):
                try:
                    # Parse question
                    parser = QuestionParser()
                    question_data = parser.parse(question)
                    
                    # Handle based on question type
                    if question_data["type"] == "simple":
                        handler = SimpleQueryHandler()
                        answer = handler.handle(question_data)
                        
                        # Display simple answer
                        st.markdown("### Answer")
                        st.info(answer)
                        
                        # Show question details
                        with st.expander("Question Details"):
                            st.json(question_data)
                    else:
                        # Complex question - use orchestrator
                        handler = ComplexQueryHandler()
                        result = handler.handle(question_data)
                        
                        if "error" in result:
                            st.error(result["error"])
                            st.info(result.get("answer", ""))
                        else:
                            # Display results in tabs
                            tab1, tab2, tab3, tab4 = st.tabs([
                                "📈 Answer",
                                "💹 Market Data Agent",
                                "📰 Fundamental & News Agent",
                                "⚖️ Portfolio & Risk Agent"
                            ])
                            
                            # Tab 1: Answer
                            with tab1:
                                st.markdown("### Answer")
                                st.markdown(result.get("answer", ""))
                            
                            # Tab 2-4: Agent outputs (if available)
                            if "result" in result:
                                full_result = result["result"]
                                
                                with tab2:
                                    st.markdown("### Market Data Agent Output")
                                    market_agent = full_result["agents"]["market_data"]
                                    st.text(market_agent.get("output", ""))
                                
                                with tab3:
                                    st.markdown("### Fundamental & News Agent Output")
                                    fundamental_agent = full_result["agents"]["fundamental_news"]
                                    st.text(fundamental_agent.get("output", ""))
                                
                                with tab4:
                                    st.markdown("### Portfolio & Risk Agent Output")
                                    portfolio_agent = full_result["agents"]["portfolio_risk"]
                                    st.text(portfolio_agent.get("output", ""))
                            
                            # Show question details
                            with st.expander("Question Details"):
                                st.json(question_data)
                
                except Exception as e:
                    st.error(f"Error processing question: {str(e)}")
                    st.exception(e)
    else:
        # Form input mode
        if not symbol:
            st.error("Please enter a stock symbol")
        else:
            # Show loading spinner
            with st.spinner(f"Analyzing {symbol}..."):
                try:
                    # Process query
                    result = orchestrator.process_query(symbol, risk_profile, horizon_months)
                    
                    # Display results in tabs
                    tab1, tab2, tab3, tab4 = st.tabs([
                        "📈 Final Answer",
                        "💹 Market Data Agent",
                        "📰 Fundamental & News Agent",
                        "⚖️ Portfolio & Risk Agent"
                    ])
                    
                    # Tab 1: Final Answer
                    with tab1:
                        st.markdown("### Final Answer")
                        st.markdown(result["final_answer"])
                    
                    # Tab 2: Market Data Agent
                    with tab2:
                        st.markdown("### Market Data Agent Output")
                        market_agent = result["agents"]["market_data"]
                        
                        st.markdown("**Reasoning:**")
                        st.text(market_agent.get("reason", ""))
                        
                        st.markdown("**Action:**")
                        market_action = market_agent.get("action", {})
                        if "error" not in market_action:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Current Price", f"${market_action.get('current_price', 0):.2f}")
                            with col2:
                                st.metric("Price Change", f"{market_action.get('price_change_pct', 0):+.2f}%")
                            with col3:
                                st.metric("Volatility", f"{market_action.get('volatility', 0):.2f}%")
                        else:
                            st.error(market_action.get("error", "Unknown error"))
                        
                        st.markdown("**Output:**")
                        st.text(market_agent.get("output", ""))
                    
                    # Tab 3: Fundamental & News Agent
                    with tab3:
                        st.markdown("### Fundamental & News Agent Output")
                        fundamental_agent = result["agents"]["fundamental_news"]
                        
                        st.markdown("**Reasoning:**")
                        st.text(fundamental_agent.get("reason", ""))
                        
                        st.markdown("**Action:**")
                        fundamental_action = fundamental_agent.get("action", {})
                        fundamentals = fundamental_action.get("fundamentals", {})
                        
                        if "error" not in fundamentals:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                pe = fundamentals.get("pe_ratio")
                                if pe:
                                    st.metric("P/E Ratio", f"{pe:.2f}")
                            with col2:
                                profit_margin = fundamentals.get("profit_margin")
                                if profit_margin:
                                    st.metric("Profit Margin", f"{profit_margin*100:.2f}%")
                            with col3:
                                roe = fundamentals.get("roe")
                                if roe:
                                    st.metric("ROE", f"{roe*100:.2f}%")
                            
                            st.markdown("**News:**")
                            news = fundamental_action.get("news", [])
                            if news and not ("error" in news[0] if news else False):
                                for i, item in enumerate(news[:3], 1):
                                    with st.expander(f"News {i}: {item.get('title', 'No title')[:50]}..."):
                                        st.write(f"**Publisher:** {item.get('publisher', 'Unknown')}")
                                        st.write(f"**Link:** {item.get('link', 'N/A')}")
                        else:
                            st.error(fundamentals.get("error", "Unknown error"))
                        
                        st.markdown("**Output:**")
                        st.text(fundamental_agent.get("output", ""))
                    
                    # Tab 4: Portfolio & Risk Agent
                    with tab4:
                        st.markdown("### Portfolio & Risk Agent Output")
                        portfolio_agent = result["agents"]["portfolio_risk"]
                        
                        st.markdown("**Reasoning:**")
                        st.text(portfolio_agent.get("reason", ""))
                        
                        st.markdown("**Action:**")
                        portfolio_action = portfolio_agent.get("action", {})
                        recommendation = portfolio_action.get("recommendation", {})
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Risk Score", f"{portfolio_action.get('risk_score', 0):.1f}/100")
                        with col2:
                            action = recommendation.get("action", "HOLD")
                            st.metric("Recommendation", action)
                        
                        st.markdown(f"**Suggested Allocation:** {recommendation.get('allocation', 'N/A')}")
                        
                        st.markdown("**Output:**")
                        st.text(portfolio_agent.get("output", ""))
                
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
                    st.exception(e)
else:
    # Show instructions when not running
    st.info("👈 Enter query parameters in the sidebar and click 'Run Analysis' to begin")
    
    st.markdown("### System Architecture")
    st.markdown("""
    This system uses a **Multi-Agent Control Project (MCP)** architecture:
    
    1. **Orchestrator** - Coordinates all agents and aggregates outputs
    2. **Market Data Agent** - Retrieves and normalizes market data
    3. **Fundamental & News Agent** - Analyzes company fundamentals and news
    4. **Portfolio & Risk Agent** - Generates risk-aware recommendations
    
    Each agent follows the **ReAct pattern** (Reason → Act → Output).
    """)
    
    st.markdown("### Evaluation Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Correctness", "✓", help="Outputs match ground truth")
    with col2:
        st.metric("Faithfulness", "✓", help="No unsupported assumptions")
    with col3:
        st.metric("Coverage", "✓", help="All inputs considered")

