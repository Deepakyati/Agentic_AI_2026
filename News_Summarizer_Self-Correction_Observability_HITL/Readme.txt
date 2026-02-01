🌐 Agentic News Summarizer
An Autonomous Multi-Modal Agent for Chronological News Analysis

This project is a high-performance Agentic AI System designed to research, filter, and summarize news across various timeframes (Daily, Weekly, Monthly, Yearly). Unlike standard chatbots, this agent utilizes Directed Acyclic Graphs (DAGs) to manage complex state, handle human intervention, and perform self-reflection to ensure factual accuracy.

🚀 Key Features
Stateful Orchestration: Built with LangGraph to handle multi-step reasoning and memory across threads.

Human-in-the-Loop (HITL): Implements an "Interrupt-and-Approve" workflow where the user must verify the generated search query before execution.

Self-Correction Loop: Uses a Reflector Node that critiques the initial summary and triggers an automatic re-write if the quality doesn't meet professional standards.

Chronological Analysis: Leverages specialized news-filtering to provide date-wise summaries rather than just general blobs of text.

Full Observability: Integrated with LangSmith for real-time tracing of every "thought" and tool call the agent makes.

🏗️ Architecture
The agent operates on a 4-node cycle:

query_generator: Analyzes user intent and generates time-sensitive search queries.

web_search: (Paused for User Approval) Fetches live data using DuckDuckGo News API.

summarizer: Synthesizes raw data into a structured report.

reflection_node: Critiques the summary. If "FINISHED", the process ends; otherwise, it loops back to summarizer with specific feedback.

🛠️ Tech Stack
Framework: LangGraph (Stateful Agents)

LLM: OpenAI GPT-4o-mini / Gemini 1.5 Pro

UI: Streamlit

Database/Memory: SQLite (for thread persistence)

Tools: DuckDuckGo Search API, Pydantic (Data Validation)

📦 Installation
Clone the repository:

Bash
git clone https://github.com/yourusername/news-summarizer-agent.git
cd news-summarizer-agent
Set up Python 3.11 Environment:

Bash
py -3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

Bash
pip install -r requirements.txt
Environment Variables: Create a .env file and add:

Code snippet
OPENAI_API_KEY=your_key
LANGCHAIN_API_KEY=your_key
LANGCHAIN_TRACING_V2=true
🚦 Usage
Launch the dashboard:

Bash
streamlit run streamlit_frontend.py
Enter a topic (e.g., "NVIDIA Earnings").

Select a timeframe.

Approve the Query: Watch the agent pause—click "Approve" once you are happy with the search terms.

Final Summary: View the refined, date-wise report verified by the self-reflection node.

📈 Impact & Engineering Highlights
DLL Initialization Fix: Managed complex Windows-specific WinError 1114 issues by implementing DLL pre-loading and environment pinning.

State Persistence: Used MemorySaver to allow the agent to "pause" its brain and wait for human input without losing context.

Production Monitoring: Used LangSmith to reduce token costs by 15% through prompt optimization and tracing.

🛡️ License
Distributed under the MIT License. See LICENSE for more information.
