import os
import ctypes
import sys

# Prevent Intel OpenMP conflict and fix DLL search path
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

if sys.platform == "win32":
    # This adds the torch bin directory to the search path manually
    import torch
    torch_dll_path = os.path.join(os.path.dirname(torch.__file__), 'lib')
    os.add_dll_directory(torch_dll_path)

from datetime import datetime
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver 
from langchain_openai import ChatOpenAI
from duckduckgo_search import DDGS 
from dotenv import load_dotenv

# Load API keys and enable LangSmith Tracing
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "News-Summarizer-Agent"

# 1. Define State
class AgentState(TypedDict):
    topic: str
    timeframe: str
    search_query: str
    raw_results: str
    summary: str
    critique: str

# 2. Define Nodes
def query_generator(state: AgentState):
    topic = state['topic']
    time = state['timeframe']
    mapping = {"daily": "d", "weekly": "w", "monthly": "m", "yearly": "y"}
    return {
        "search_query": f"{topic} latest news",
        "timeframe": mapping.get(time, "d")
    }

def web_search(state: AgentState):
    query = state['search_query']
    time_limit = state['timeframe']
    results_text = []
    try:
        with DDGS() as ddgs:
            results = ddgs.news(query, timelimit=time_limit, max_results=5)
            for r in results:
                date = r.get('date', 'N/A')
                results_text.append(f"Date: {date}\nTitle: {r['title']}\nSnippet: {r['body']}\n")
        raw_results = "\n---\n".join(results_text) if results_text else "No news found."
    except Exception as e:
        raw_results = f"Search failed: {str(e)}"
    return {"raw_results": raw_results}

def summarizer(state: AgentState):
    llm = ChatOpenAI(model="gpt-4o-mini") 
    prompt = f"""
    Analyze these news results for '{state['topic']}':
    {state['raw_results']}
    
    Critique to address (if any): {state.get('critique', 'None')}
    
    Provide a chronological summary with bullet points and a 'Strategic Insight' section.
    """
    response = llm.invoke(prompt)
    return {"summary": response.content}

def reflection_node(state: AgentState):
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = f"Review this summary:\n{state['summary']}\n\nIf it covers the main points and has dates, reply 'FINISHED'. Otherwise, suggest 1 improvement."
    response = llm.invoke(prompt)
    return {"critique": response.content}

def should_continue(state: AgentState) -> Literal["summarize", "__end__"]:
    if "FINISHED" in state["critique"]:
        return "__end__"
    return "summarize"

# 3. Build Graph
memory = MemorySaver()
builder = StateGraph(AgentState)

builder.add_node("generate_query", query_generator)
builder.add_node("search", web_search)
builder.add_node("summarize", summarizer)
builder.add_node("reflect", reflection_node)

builder.add_edge(START, "generate_query")
builder.add_edge("generate_query", "search")
builder.add_edge("search", "summarize")
builder.add_edge("summarize", "reflect")
builder.add_conditional_edges("reflect", should_continue)

# HITL: Pause before searching to let the human approve the query
graph = builder.compile(checkpointer=memory, interrupt_before=["search"])