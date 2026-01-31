import os
from typing import TypedDict
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# LangChain & Gemini Imports
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

load_dotenv()

# 1. Configuration & Model Setup

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
#llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)
search_tool = DuckDuckGoSearchRun()

# 2. THE RAG INGESTION PROCESS
def initialize_retriever(pdf_path):
    # A. Ingestion: Load the PDF
    reader = PdfReader(pdf_path)
    raw_text = "".join([page.extract_text() for page in reader.pages])
    
    # B. Chunking: Split text into manageable pieces
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    chunks = text_splitter.split_text(raw_text)
    
    # C. Embedding & Storage: Convert to vectors and store in FAISS
    vector_db = FAISS.from_texts(chunks, embeddings)
    
    # D. Retrieval: Return the retriever object
    return vector_db.as_retriever(search_kwargs={"k": 3})

# Initialize the retriever globally
retriever = initialize_retriever("attention.pdf")

# 3. LANGGRAPH LOGIC
class AgentState(TypedDict):
    question: str
    pdf_summary: str
    web_summary: str

def pdf_rag_agent(state: AgentState):
    """Retriever Agent: Finds relevant chunks and generates summary."""
    # Retrieve only relevant chunks (The 'R' in RAG)
    docs = retriever.invoke(state['question'])
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"Using this PDF context, answer the question: {state['question']}\n\nContext: {context}"
    response = llm.invoke(prompt)
    return {"pdf_summary": response.content}

def web_agent(state: AgentState):
    """Web Agent: Searches live data."""
    search_results = search_tool.run(state['question'])
    prompt = f"Summarize web results for: {state['question']}\n\nResults: {search_results}"
    response = llm.invoke(prompt)
    return {"web_summary": response.content}

def create_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("pdf_agent", pdf_rag_agent)
    workflow.add_node("web_agent", web_agent)
    
    workflow.set_entry_point("pdf_agent")
    workflow.add_edge("pdf_agent", "web_agent")
    workflow.add_edge("web_agent", END)
    
    return workflow.compile()

research_app = create_graph()