"""
Prioritization with CrewAI
===========================
Agent evaluates and prioritizes a set of tasks based on urgency,
importance, and dependencies.
"""

from crewai import Agent, Task, Crew, Process

prioritizer = Agent(
    role="Task Prioritization Specialist",
    goal="Rank tasks by urgency, importance, and dependencies to determine optimal execution order",
    backstory="You are an expert at triaging work. You evaluate urgency, impact, and dependencies.",
    verbose=True,
)

task = Task(
    description=(
        "Prioritize these tasks for a software team:\n"
        "A. Fix critical login bug (blocks all users)\n"
        "B. Update API documentation\n"
        "C. Deploy new payment feature (demo to investors Friday)\n"
        "D. Refactor database queries (improves performance 40%)\n"
        "E. Set up monitoring dashboard\n\n"
        "Rank them P0-P4 with justification. Consider urgency, impact, and dependencies."
    ),
    expected_output="Prioritized task list with P0-P4 rankings and reasoning.",
    agent=prioritizer,
)

crew = Crew(agents=[prioritizer], tasks=[task], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    print(crew.kickoff())
