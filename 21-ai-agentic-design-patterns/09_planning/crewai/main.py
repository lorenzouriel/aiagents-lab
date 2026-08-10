"""
Planning with CrewAI
=====================
A planning agent decomposes a high-level goal into an actionable
step-by-step plan, then an executor agent carries it out.
"""

from crewai import Agent, Task, Crew, Process

planner = Agent(
    role="Strategic Planner",
    goal="Decompose complex goals into detailed, actionable step-by-step plans",
    backstory="You are an expert project planner who breaks down complex objectives into clear milestones.",
    verbose=True,
)

executor = Agent(
    role="Plan Executor",
    goal="Execute each step of a plan and report results",
    backstory="You follow plans precisely and report on each step's completion.",
    verbose=True,
)

plan_task = Task(
    description=(
        "Goal: Organize a 2-day team offsite for 15 people in Austin, TX with a "
        "$10,000 budget. Create a detailed plan with at least 6 steps, including "
        "venue selection, logistics, activities, and budget allocation."
    ),
    expected_output="A numbered, actionable plan with timeline and budget per step.",
    agent=planner,
)

execute_task = Task(
    description="Execute the plan step by step. For each step, describe what you would do and confirm completion.",
    expected_output="A status report for each step of the plan.",
    agent=executor,
    context=[plan_task],
)

crew = Crew(
    agents=[planner, executor],
    tasks=[plan_task, execute_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\nResult:", result)
