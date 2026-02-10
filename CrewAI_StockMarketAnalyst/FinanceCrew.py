import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

def get_llm(provider):
    if provider == "Google Gemini":
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    elif provider == "Groq (Llama 3)":
        return ChatGroq(model_name="llama-3.3-70b-versatile")
    else:
        return ChatOpenAI(model="gpt-4o-mini")

# --- Custom Tool for Financial News ---
@tool("StockMarketSearch")
def stock_search(query: str):
    """Useful for searching latest stock market news, earnings reports, and market sentiment."""
    return DuckDuckGoSearchRun().run(query)

def run_finance_crew(provider, stock_symbol):
    llm = get_llm(provider)

    # 1. Agents: Defining Financial Personas
    data_scout = Agent(
        role='Financial Data Researcher',
        goal='Gather recent news, earnings summaries, and price trends for {stock_symbol}.',
        backstory="You are a specialist in scanning financial news outlets and regulatory filings.",
        tools=[stock_search],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    analyst = Agent(
        role='Technical Analyst',
        goal='Analyze the sentiment and data provided to identify market trends for {stock_symbol}.',
        backstory="You are an expert at interpreting market sentiment and identifying bullish or bearish signals.",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    manager = Agent(
        role='Senior Investment Manager',
        goal='Synthesize all analysis into a final "Buy/Sell/Hold" recommendation for {stock_symbol}.',
        backstory="""You are the ultimate decision-maker. You review the research and the technical analysis 
        to ensure the final advice is balanced, data-driven, and includes a Risk Assessment section.""",
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

    # 2. Tasks
    research_task = Task(
        description="Compile a report of the last 7 days of news and events for {stock_symbol}.",
        expected_output="A summary of key financial events and current price action.",
        agent=data_scout
    )

    analysis_task = Task(
        description="Based on the research, evaluate the sentiment and potential risks.",
        expected_output="A technical breakdown of market sentiment (Positive/Negative/Neutral).",
        agent=analyst
    )

    # 3. The Crew
    crew = Crew(
        agents=[data_scout, analyst],
        tasks=[research_task, analysis_task],
        manager_agent=manager,
        process=Process.hierarchical,
        verbose=True
    )

    return crew.kickoff(inputs={'stock_symbol': stock_symbol})