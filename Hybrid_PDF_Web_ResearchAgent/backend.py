import os
import sys
import ctypes
import time

# 1. CRITICAL WINDOWS & DLL FIXES
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
if sys.platform == "win32":
    try:
        ctypes.CDLL("vcruntime140.dll")
        ctypes.CDLL("msvcp140.dll")
    except Exception:
        pass

from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from duckduckgo_search import DDGS  # Using direct library for stability
from langgraph.graph import StateGraph, START, END

load_dotenv()

# 2. State Definition
class AgentState(TypedDict):
    question: str
    pdf_context: str
    web_context: str
    final_response: str
    documents: List

# 3. Define Nodes
def pdf_retriever(state: AgentState):
    """RAG Node: Performs semantic search on uploaded PDFs using FAISS."""
    if not state.get('documents'):
        return {"pdf_context": "No documents provided."}
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splits = text_splitter.split_documents(state['documents'])
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(splits, embeddings)
    
    relevant_docs = vectorstore.similarity_search(state['question'], k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    return {"pdf_context": context}

def web_researcher(state: AgentState):
    """Web Node: Uses DDGS directly to avoid 'No Results Found' errors."""
    query = state['question']
    results_list = []
    
    try:
        # Use a cleaner search syntax for DuckDuckGo
        search_query = f"{query} latest news"
        
        with DDGS() as ddgs:
            # max_results=5 keeps it fast and avoids rate limits
            ddgs_results = ddgs.text(search_query, max_results=5)
            for r in ddgs_results:
                results_list.append(f"Title: {r['title']}\nSource: {r['href']}\nContent: {r['body']}\n")
        
        web_context = "\n---\n".join(results_list) if results_list else "No web results found."
    except Exception as e:
        web_context = f"Web search failed: {str(e)}"
        
    return {"web_context": web_context}

def final_synthesizer(state: AgentState):
    """Synthesis Node: The brain that compares PDF data vs Live Web data."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    prompt = f"""
    You are a Fact-Checking Research Agent. 
    Compare the PDF knowledge with Live Web information.
    
    QUESTION: {state['question']}
    
    PDF DATA: {state['pdf_context']}
    WEB DATA: {state['web_context']}
    
    TASK:
    - Answer based on the PDF.
    - Check if the Web data adds newer or contradictory info.
    - If there is a conflict (e.g. PDF says 'active' but Web says 'deprecated'), highlight it.
    - End with a 'Verified Conclusion'.
    """
    
    response = llm.invoke(prompt)
    return {"final_response": response.content}

# 4. Build the Graph
builder = StateGraph(AgentState)

builder.add_node("pdf_retriever", pdf_retriever)
builder.add_node("web_researcher", web_researcher)
builder.add_node("final_synthesizer", final_synthesizer)

builder.add_edge(START, "pdf_retriever")
builder.add_edge("pdf_retriever", "web_researcher")
builder.add_edge("web_researcher", "final_synthesizer")
builder.add_edge("final_synthesizer", END)

graph = builder.compile()