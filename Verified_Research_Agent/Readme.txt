📚 Verified Research Agent (Hybrid RAG)
An Agentic AI System for Cross-Referencing Static PDF Knowledge with Live Web Intelligence

Most RAG (Retrieval-Augmented Generation) systems suffer from "Knowledge Stale-ness"—they can only answer based on the documents provided. The Verified Research Agent solves this by using a multi-agent workflow to verify PDF content against the live web in real-time.

🧠 The "Conflict Resolution" Architecture
The agent doesn't just summarize; it cross-references. It identifies if your document is outdated by comparing it with live data from the Tavily/DuckDuckGo Search API.

Workflow:
PDF Retrieval (RAG): Extracts semantic context from uploaded PDFs using FAISS and OpenAI Embeddings.

Web Research: Autonomously generates search queries to find the most recent updates on the retrieved topics.

Synthesis & Conflict Detection: An LLM "Analyst" compares both sources. If the web contradicts the PDF, the agent highlights the discrepancy and provides a "Verified Conclusion."

🚀 Key Features
Hybrid Intelligence: Combines local PDF context with real-world live data.

Stateful Orchestration: Built with LangGraph to ensure reliable data flow between the RAG and Search nodes.

Production Stability: Implements OpenMP conflict management and DLL pre-loading for high reliability on Windows/Anaconda environments.

Vector Search: Optimized with FAISS-CPU for low-latency similarity retrieval.

🛠️ Tech Stack
Orchestration: LangGraph (StateGraph)

LLMs: OpenAI (GPT-4o-mini)

Vector Store: FAISS (Facebook AI Similarity Search)

Search Engine: Tavily API / DuckDuckGo

Frontend: Streamlit

📦 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/yourusername/verified-research-agent.git
cd verified-research-agent
Environment Configuration: Create a .env file:

Code snippet
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
Run the Application:

Bash
streamlit run frontend.py
📈 Engineering Highlights for Recruiters
Solved Data Staleness: Implemented a system that actively identifies "Outdated Documents" by comparing them with live APIs.

Environment Resilience: Debugged and resolved complex WinError 1114 and OMP: Error #15 issues during deployment on Windows systems.

Structured State Management: Used a unified AgentState to maintain context across disparate tools (Vector DBs and Search APIs).

🛡️ License
MIT License.
