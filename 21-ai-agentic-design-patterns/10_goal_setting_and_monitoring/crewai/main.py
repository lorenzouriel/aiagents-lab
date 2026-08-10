"""
Goal Setting and Monitoring with CrewAI
========================================
An agent sets measurable goals, executes tasks, monitors progress,
and adjusts strategy when goals are at risk.
"""

from crewai import Agent, Task, Crew, Process

goal_setter = Agent(
    role="Goal Strategist",
    goal="Define SMART goals and success criteria for a project",
    backstory="You specialize in defining clear, measurable objectives with KPIs.",
    verbose=True,
)

executor = Agent(
    role="Task Executor",
    goal="Execute tasks and report progress metrics",
    backstory="You execute assigned tasks and report quantitative progress.",
    verbose=True,
)

monitor = Agent(
    role="Progress Monitor",
    goal="Evaluate progress against goals and recommend adjustments",
    backstory="You track KPIs, detect deviations, and suggest corrective actions.",
    verbose=True,
)

task_goals = Task(
    description=(
        "Define 3 SMART goals for a content marketing campaign launching next month. "
        "Include specific KPIs and success thresholds for each goal."
    ),
    expected_output="3 SMART goals with measurable KPIs.",
    agent=goal_setter,
)

task_execute = Task(
    description="Simulate executing the first week of the campaign. Report progress metrics for each goal.",
    expected_output="Progress report with metrics for each goal.",
    agent=executor,
    context=[task_goals],
)

task_monitor = Task(
    description=(
        "Compare progress against goals. Identify any goals at risk and "
        "recommend specific adjustments to get back on track."
    ),
    expected_output="Monitoring report with risk assessment and recommendations.",
    agent=monitor,
    context=[task_goals, task_execute],
)

crew = Crew(
    agents=[goal_setter, executor, monitor],
    tasks=[task_goals, task_execute, task_monitor],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\nResult:", result)
