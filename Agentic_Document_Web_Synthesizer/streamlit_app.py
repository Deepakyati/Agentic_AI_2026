import streamlit as st
from langgraph_backend import research_app

# UI Config
st.set_page_config(page_title="Agentic Research Tool", layout="wide")
st.title("🤖 Specialized Research Agents")
st.markdown("---")

# Sidebar for Status
with st.sidebar:
    st.header("Project Info")
    st.write("📄 **Internal Source:** attention.pdf")
    st.write("🌐 **External Source:** DuckDuckGo Web Search")
    st.write("🧠 **Model:** Groq / Gemini 1.5 Flash")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input field
user_query = st.chat_input("Ask about the paper or a general AI topic...")

if user_query:
    # Add user message to UI
    st.chat_message("user").write(user_query)
    
    with st.spinner("Agents are collaborating..."):
        # Invoke the LangGraph Backend
        inputs = {"question": user_query, "pdf_summary": "", "web_summary": ""}
        result = research_app.invoke(inputs)
        
        # Display Results in a clear, comparative layout
        st.subheader("Final Research Report")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("### 📄 PDF Summary")
            st.write(result["pdf_summary"])
            
        with col2:
            st.success("### 🌐 Web Summary")
            st.write(result["web_summary"])

        # Optional: Save to history
        st.session_state.messages.append({"role": "assistant", "content": result})