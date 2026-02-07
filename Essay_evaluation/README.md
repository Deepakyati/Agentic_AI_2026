AI Essay Evaluation & Feedback System
Overview
A sophisticated Agentic AI system designed to provide objective, multi-dimensional feedback on written essays. Unlike simple LLM wrappers, 
this system utilizes a State Management approach to evaluate essays across three distinct pillars: Language Proficiency, Depth of Analysis, and Clarity of Thought.

Technical Architecture
The project is built using a "Review-and-Summarize" workflow, ensuring that the final feedback is grounded in specific, categorized analysis rather than general impressions.
The Pillar System
The evaluator assesses the input based on:
Language Feedback: Vocabulary range, grammar, and stylistic tone.
Analysis Feedback: The strength of the argument and evidence provided.
Clarity Feedback: Structural flow and "Clarity of Thought."

Key Features
Structured State Management: Uses a state dictionary to track individual feedback pillars before final synthesis.
Automated Summarization: A dedicated summarization node that aggregates multi-pillar feedback into a cohesive "Executive Summary" for the student.
Factual Grounding: Implements strict prompt engineering to ensure feedback is derived directly from the essay text.
Validation: (Optional/Planned) Integration of Pydantic for scoring essay metrics on a scale of ge=0, le=10.

Tech Stack
Language: Python 3.10+
AI Orchestration: LangChain / LangGraph
LLM: Google Gemini 1.5 Flash (via langchain-google-genai)
Environment Management: python-dotenv, venv
