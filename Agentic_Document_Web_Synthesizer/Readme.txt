Agentic_Document_Web_Synthesizer 🤖📄🌐
A Multi-Agent Orchestration System for Hybrid Intelligence.

This project demonstrates a production-grade Agentic AI Workflow built with LangGraph. It bridges the gap between static internal documents (PDFs) and the dynamic external web by coordinating three specialized agents to produce a single, synthesized research report.

🌟 Key Features
Stateful Multi-Agent Orchestration: Uses a Directed Acyclic Graph (DAG) to manage shared state across multiple LLM agents.

Hybrid RAG Architecture: Combines FAISS vector search with Google Gemini Embeddings for high-precision document retrieval.

Real-time Web Integration: Leverages DuckDuckGo Search and Groq (Llama 3.3) for ultra-low latency external data fetching.

Conflict Resolution & Synthesis: A dedicated Synthesizer Agent cross-references sources to identify contradictions and provide a unified conclusion.

Streamlit UI: A professional dashboard featuring side-by-side agent findings and a master executive summary.

🏗️ System Architecture
The project follows a sequential agentic flow:

START: The user query enters the AgentState.

PDF Agent: Performs RAG to extract internal context from attention.pdf.

Web Agent: Queries the live web for the latest updates and external benchmarks.

Synthesizer Agent: Analyzes outputs from both agents to resolve discrepancies and generate the final report.

END: The synthesized state is returned to the Streamlit UI.

🛠️ Tech Stack
Framework: LangGraph, LangChain

LLMs: Groq (Llama 3.3-70B), Gemini 1.5 Flash

Vector DB: FAISS

Frontend: Streamlit

Environment: Python 3.10+, PowerShell

🚀 Getting Started
1. Clone the Repository
Bash
git clone https://github.com/your-username/Agentic_Document_Web_Synthesizer.git
cd Agentic_Document_Web_Synthesizer
2. Set Up Environment
Create a .env file in the root directory:

Plaintext
GOOGLE_API_KEY=your_google_key
GROQ_API_KEY=your_groq_key
3. Install Dependencies
PowerShell
pip install -r requirements.txt
4. Run the Application
PowerShell
streamlit run streamlit_app.py
📝 Interview Talk Tracks
Why LangGraph? "I used LangGraph to move beyond simple linear chains. It allows for a stateful 'shared brain' where agents can build upon each other's work."

The Synthesizer Node: "This is the system's 'Senior Manager.' It doesn't just display data; it performs reasoning to ensure internal and external sources are aligned."

