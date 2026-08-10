"""
Advanced Reasoning with CrewAI
===============================
Demonstrates Chain-of-Thought and ReAct-style reasoning where agents
think step-by-step and alternate between reasoning and action.
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

@tool("Search Knowledge Base")
def search_kb(query: str) -> str:
    """Search a knowledge base for information."""
    kb = {
        "python gc": "Python uses reference counting and a cyclic garbage collector.",
        "rust memory": "Rust uses ownership and borrowing — no garbage collector needed.",
        "go gc": "Go uses a concurrent, tri-color mark-and-sweep garbage collector.",
    }
    for key, val in kb.items():
        if key in query.lower():
            return val
    return "No relevant information found."

reasoner = Agent(
    role="Technical Reasoning Agent",
    goal="Solve complex technical questions using step-by-step reasoning",
    backstory=(
        "You are a senior engineer who thinks through problems methodically. "
        "Always break complex questions into sub-questions, research each one, "
        "then synthesize a conclusion. Show your reasoning at every step."
    ),
    tools=[search_kb],
    verbose=True,
)

task = Task(
    description=(
        "Question: How do Python, Rust, and Go handle memory management differently? "
        "Think step by step: (1) Research each language's approach, "
        "(2) Compare the approaches, (3) Summarize the trade-offs."
    ),
    expected_output="A structured comparison with clear reasoning steps shown.",
    agent=reasoner,
)

crew = Crew(agents=[reasoner], tasks=[task], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\nResult:", result)
