import streamlit as st
from langgraph_backend import graph

st.set_page_config(page_title="Agentic News", layout="wide")

# Persistent Thread ID
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"

config = {"configurable": {"thread_id": st.session_state.thread_id}}

st.title("🌐 Agentic News Summarizer")
st.caption("Advanced Workflow: HITL Approval -> Search -> Reflection Loop")

with st.sidebar:
    st.header("Research Parameters")
    topic = st.text_input("Topic", placeholder="e.g. NVIDIA Earnings")
    timeframe = st.radio("Range", ["daily", "weekly", "monthly", "yearly"])
    
    if st.button("Initialize Agent", type="primary"):
        # Clear old session data
        st.session_state.summary_done = False
        # Start the graph (it will stop at 'search')
        graph.invoke({"topic": topic, "timeframe": timeframe}, config)

# Fetch current graph state
state = graph.get_state(config)

# --- HUMAN-IN-THE-LOOP SECTION ---
if state.next and state.next[0] == "search":
    st.warning(f"🤔 The Agent wants to search for: **{state.values.get('search_query')}**")
    if st.button("✅ Approve & Execute Search"):
        with st.spinner("Searching and Refining..."):
            # Resume the graph
            graph.invoke(None, config)
            st.rerun()

# --- DISPLAY OUTPUT ---
final_state = graph.get_state(config)
if "summary" in final_state.values:
    st.success("✨ Final Verified Summary")
    st.markdown(final_state.values["summary"])
    
    with st.expander("Internal Reflection Log"):
        st.write(f"**Critique:** {final_state.values.get('critique')}")