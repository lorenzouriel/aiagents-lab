"""
Knowledge Retrieval (RAG) with CrewAI
======================================
An agent uses a search tool to retrieve knowledge from an external
source before generating a grounded response.
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# --- Simulated Vector Store / Knowledge Base ---

KNOWLEDGE_BASE = [
    {"id": 1, "content": "Our return policy allows returns within 30 days with receipt.", "topic": "returns"},
    {"id": 2, "content": "Free shipping on orders over $50. Standard shipping takes 5-7 business days.", "topic": "shipping"},
    {"id": 3, "content": "Loyalty members earn 2 points per dollar. 500 points = $10 reward.", "topic": "loyalty"},
    {"id": 4, "content": "We accept Visa, Mastercard, PayPal, and Apple Pay.", "topic": "payment"},
]

@tool("Search Knowledge Base")
def search_knowledge(query: str) -> str:
    """Search the company knowledge base for relevant information."""
    results = [doc for doc in KNOWLEDGE_BASE if any(w in doc["content"].lower() for w in query.lower().split())]
    if results:
        return "\n".join(f"[Doc {r['id']}] {r['content']}" for r in results[:3])
    return "No relevant documents found."

agent = Agent(
    role="Customer Support Agent",
    goal="Answer customer questions using only information from the knowledge base",
    backstory="You are a support agent. Always search the knowledge base first, then answer based on retrieved facts.",
    tools=[search_knowledge],
    verbose=True,
)

task = Task(
    description="Customer asks: 'What is your return policy and do you offer free shipping?'",
    expected_output="An accurate answer grounded in knowledge base documents.",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\nResult:", result)
