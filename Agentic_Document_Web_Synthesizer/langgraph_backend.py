import os
from typing import TypedDict
from PyPDF2 import PdfReader
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, START, END

load_dotenv()

# --- 1. CONFIGURATION ---
# Using Google for Embeddings and Groq (Llama 3) for the "Brain"
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

search_tool = DuckDuckGoSearchRun()

# --- 2. RAG INGESTION (PDF Processing) ---
def initialize_retriever(pdf_path):
    """Loads PDF, splits into chunks, and creates a searchable Vector Store."""
    reader = PdfReader(pdf_path)
    raw_text = "".join([page.extract_text() for page in reader.pages])
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    chunks = text_splitter.split_text(raw_text)
    
    # Store in FAISS (Vector Database)
    vector_db = FAISS.from_texts(chunks, embeddings)
    return vector_db.as_retriever(search_kwargs={"k": 3})

# Initialize the retriever globally
retriever = initialize_retriever("attention.pdf")

# --- 3. STATE DEFINITION ---
class AgentState(TypedDict):
    question: str
    pdf_summary: str
    web_summary: str
    final_report: str  

# --- 4. THE AGENTS (NODES) ---

def pdf_rag_agent(state: AgentState):
    """Agent 1: Extracts facts from the local PDF document."""
    docs = retriever.invoke(state['question'])
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"Using this PDF context, answer the question: {state['question']}\n\nContext: {context}"
    response = llm.invoke(prompt)
    return {"pdf_summary": response.content}

def web_agent(state: AgentState):
    """Agent 2: Searches the live web for real-time information."""
    search_results = search_tool.run(state['question'])
    prompt = f"Summarize web results for: {state['question']}\n\nResults: {search_results}"
    response = llm.invoke(prompt)
    return {"web_summary": response.content}

def synthesizer_agent(state: AgentState):
    """Agent 3: The 'Manager' who combines PDF and Web insights into one report."""
    pdf_info = state['pdf_summary']
    web_info = state['web_summary']
    
    prompt = f"""
    You are a Senior Research Synthesizer. 
    You have two reports on the topic: {state['question']}

    1. PDF REPORT (Internal): {pdf_info}
    2. WEB REPORT (External): {web_info}

    TASK:
    Combine these into one Master Research Report. 
    - Mention if the Web info confirms or contradicts the PDF.
    - Provide a unified, clear conclusion.
    """
    response = llm.invoke(prompt)
    return {"final_report": response.content}

# --- 5. THE GRAPH ORCHESTRATION ---

def create_graph():
    # Define the graph with our state
    workflow = StateGraph(AgentState)
    
    # Add our 3 worker nodes
    workflow.add_node("pdf_agent", pdf_rag_agent)
    workflow.add_node("web_agent", web_agent)
    workflow.add_node("synthesizer", synthesizer_agent)
    
    # Define the arrows (Edges) using START and END
    workflow.add_edge(START, "pdf_agent")      # Start here
    workflow.add_edge("pdf_agent", "web_agent") # Then go here
    workflow.add_edge("web_agent", "synthesizer") # Then combine
    workflow.add_edge("synthesizer", END)      # Finish
    
    return workflow.compile()

# Compile the app
research_app = create_graph()