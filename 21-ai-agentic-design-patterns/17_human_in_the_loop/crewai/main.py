"""
Human-in-the-Loop with CrewAI
==============================
Agent requires human approval before executing high-stakes actions.
"""

from crewai import Agent, Task, Crew, Process

analyst = Agent(
    role="Financial Analyst",
    goal="Analyze trades and prepare recommendations for human approval",
    backstory="You prepare detailed trade recommendations. All trades require human approval before execution.",
    verbose=True,
)

task_analyze = Task(
    description=(
        "Analyze whether to buy 100 shares of AAPL at $198. Consider market conditions, "
        "P/E ratio, and recent earnings. Prepare a recommendation with risk assessment."
    ),
    expected_output="A trade recommendation with buy/hold/sell decision and risk level.",
    agent=analyst,
    human_input=True,  # CrewAI's built-in HITL — pauses for human approval
)

crew = Crew(agents=[analyst], tasks=[task_analyze], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    print("NOTE: This will pause for human input during execution.")
    print(crew.kickoff())
