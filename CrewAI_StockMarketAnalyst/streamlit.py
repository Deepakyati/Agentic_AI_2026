import streamlit as st
from dotenv import load_dotenv
from FinanceCrew import run_finance_crew

load_dotenv()

st.set_page_config(page_title="AI Stock Analyst Team", layout="wide")

st.title("AI Stock Market Analysis Team")
st.markdown("Collaborative Multi-Agent System for Financial Intelligence")

with st.sidebar:
    st.header("Configuration")
    provider = st.selectbox("Select LLM Provider", ["Google Gemini", "Groq (Llama 3)", "OpenAI"])
    st.divider()
    st.info("The Manager Agent will review all worker outputs before the final advice is shown.")

stock_symbol = st.text_input("Enter Stock Ticker (e.g. NVDA, TSLA, AAPL):", placeholder="NVDA")

if st.button("Analyze Stock", type="primary"):
    if not stock_symbol:
        st.error("Please enter a stock ticker symbol.")
    else:
        with st.status(f"Analyzing {stock_symbol}...", expanded=True) as status:
            try:
                result = run_finance_crew(provider, stock_symbol)
                status.update(label="Analysis Complete", state="complete", expanded=False)
                
                st.subheader(f"Investment Report: {stock_symbol}")
                st.markdown(result)
            except Exception as e:
                status.update(label=" Analysis Failed", state="error")
                st.error(f"Error: {str(e)}")