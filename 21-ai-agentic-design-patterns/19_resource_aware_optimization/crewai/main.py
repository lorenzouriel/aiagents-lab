"""
Resource-Aware Optimization with CrewAI
========================================
Routes tasks to different "models" based on complexity assessment.
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

@tool("Assess Complexity")
def assess_complexity(query: str) -> str:
    """Assess query complexity: simple, moderate, or complex."""
    if len(query.split()) < 10:
        return "simple"
    elif any(w in query.lower() for w in ["analyze", "compare", "evaluate", "strategy"]):
        return "complex"
    return "moderate"

router = Agent(
    role="Resource Router",
    goal="Route queries to the appropriate model tier based on complexity",
    backstory=(
        "You assess query complexity and route to: "
        "simple → fast/cheap model, moderate → balanced model, complex → premium model. "
        "Always check complexity first."
    ),
    tools=[assess_complexity],
    verbose=True,
)

task = Task(
    description=(
        "Assess and route this query: 'Analyze the competitive landscape of the "
        "EV market and recommend a 3-year investment strategy.' "
        "Report which model tier should handle it and why."
    ),
    expected_output="Complexity assessment and model tier recommendation.",
    agent=router,
)

crew = Crew(agents=[router], tasks=[task], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    print(crew.kickoff())
