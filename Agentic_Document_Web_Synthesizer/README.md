Hybrid-Agentic Research Orchestrator (HARO)
HARO is a sophisticated multi-agent research tool built with LangGraph, Python, and Streamlit. 
It leverages a "Cognitive Architecture" to intelligently route queries between local document analysis (RAG), real-time web research, 
and conversational chat.

Key Features
Intent-Based Routing: Uses an LLM supervisor to classify user queries and trigger only the necessary agents, optimizing performance and token usage.
Agentic RAG: Implements a full RAG pipeline (Ingestion -> Chunking -> Embedding -> Retrieval) to analyze the "Attention is All You Need" paper.
Live Web Intelligence: Independent agents collaborate to fetch and summarize real-time data from the web using DuckDuckGo.
High-Performance Inference: Powered by Groq (Llama 3.3) for blazing-fast reasoning and Google Gemini for high-dimensional embeddings.
Human-Centric UI: A clean, responsive Streamlit interface that displays comparative research reports from multiple sources.

Tech Stack
Frameworks: LangGraph (Orchestration), LangChain (Tools), Streamlit (Frontend)
LLMs: Groq Llama 3.3-70b (Logic), Google Gemini 1.5 Flash (Embeddings)
Vector Database: FAISS (Local Similarity Search)
Data Processing: PyPDF2, RecursiveCharacterTextSplitter
Search API: DuckDuckGo Search

Project Structure
Plaintext
├── attention.pdf          
├── .env                 
├── langgraph_backend.py   
└── streamlit_app.py   


Cognitive Architecture
Router Node: Analyzes the query. If you say "Thanks," it routes to the Chat Agent. If you ask about Transformers, it routes to the PDF Agent.

PDF Agent: Performs a similarity search in the FAISS vector store to find relevant context from the research paper.

Web Agent: Simultaneously (or sequentially) gathers live data to provide a modern perspective.

State Management: A global TypedDict manages the flow of information between agents, ensuring no context is lost.