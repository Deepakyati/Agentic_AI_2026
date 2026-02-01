import streamlit as st
from langgraph_backend import research_app

# UI Config
st.set_page_config(page_title="Agentic Document & Web Synthesizer", layout="wide")
st.title("🤖 Agentic_Document_Web_Synthesizer")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Project Info")
    st.write("📄 **Internal Source:** attention.pdf")
    st.write("🌐 **External Source:** DuckDuckGo Web")
    st.write("🧠 **Logic:** Multi-Agent Synthesis")

# Input field
user_query = st.chat_input("Ask about the paper or a general AI topic...")

if user_query:
    st.chat_message("user").write(user_query)
    
    with st.spinner("Agents are collaborating to synthesize findings..."):
        # Invoke the LangGraph Backend
        inputs = {
            "question": user_query, 
            "pdf_summary": "", 
            "web_summary": "",
            "final_report": ""
        }
        result = research_app.invoke(inputs)
        
        # 1. Show the Master Synthesized Report at the Top
        st.header("✨ Final Synthesized Report")
        st.success(result["final_report"])
        
        st.markdown("---")
        
        # 2. Show the Source Breakdowns in Columns
        st.subheader("Source Details")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("### 📄 PDF Agent Findings")
            st.write(result["pdf_summary"])
            
        with col2:
            st.warning("### 🌐 Web Agent Findings")
            st.write(result["web_summary"])