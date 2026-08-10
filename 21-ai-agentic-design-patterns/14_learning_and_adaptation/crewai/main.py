"""
Learning and Adaptation with CrewAI
=====================================
Agent reviews past performance and adapts its strategy accordingly.
"""

from crewai import Agent, Task, Crew, Process

learner = Agent(
    role="Adaptive Content Strategist",
    goal="Learn from past campaign results and adapt future strategies",
    backstory="You analyze historical data and adjust your approach based on what worked.",
    verbose=True,
)

task_review = Task(
    description=(
        "Review these past campaign results:\n"
        "- Campaign A (email): 12% open rate, 2% conversion\n"
        "- Campaign B (social): 25% engagement, 5% conversion\n"
        "- Campaign C (blog): 8,000 views, 1% conversion\n\n"
        "Identify what worked, what didn't, and extract 3 key lessons."
    ),
    expected_output="Analysis of past results with 3 key lessons learned.",
    agent=learner,
)

task_adapt = Task(
    description="Based on your lessons learned, design an adapted strategy for next quarter's campaign.",
    expected_output="An adapted campaign strategy informed by past performance.",
    agent=learner,
    context=[task_review],
)

crew = Crew(agents=[learner], tasks=[task_review, task_adapt], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    print(crew.kickoff())
