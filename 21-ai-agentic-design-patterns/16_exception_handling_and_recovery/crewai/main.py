"""
Exception Handling and Recovery with CrewAI
============================================
Agent with fallback tools and retry logic for handling failures.
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

call_count = {"primary": 0}

@tool("Primary API")
def primary_api(query: str) -> str:
    """Primary data API — may fail intermittently."""
    call_count["primary"] += 1
    if call_count["primary"] <= 1:
        raise Exception("API timeout: service temporarily unavailable")
    return f"Data for '{query}': Revenue $2.3M, Growth 15% YoY"

@tool("Fallback API")
def fallback_api(query: str) -> str:
    """Fallback data source — always available but less detailed."""
    return f"Cached data for '{query}': Revenue ~$2M (approximate, from cache)"

agent = Agent(
    role="Resilient Data Agent",
    goal="Retrieve data using primary API; fall back to secondary if primary fails",
    backstory="You always try the primary API first. If it fails, use the fallback. Report which source was used.",
    tools=[primary_api, fallback_api],
    verbose=True,
)

task = Task(
    description="Retrieve Q4 revenue data. Try the primary API first; if it fails, use the fallback.",
    expected_output="Revenue data with source attribution.",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    print(crew.kickoff())
