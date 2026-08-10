"""
Memory with CrewAI
===================
Demonstrates CrewAI's built-in memory capabilities for maintaining
context across tasks within a crew execution.
"""

from crewai import Agent, Task, Crew, Process

# CrewAI supports memory natively — enable it at the Crew level.

assistant = Agent(
    role="Personal Assistant",
    goal="Help users with tasks while remembering context from earlier interactions",
    backstory="You are a helpful assistant with excellent memory.",
    verbose=True,
)

# --- Multi-turn tasks that require memory ---

task1 = Task(
    description="The user says: 'My name is Lorenzo and I work as a data engineer at TechCorp.'",
    expected_output="Acknowledge the user's name and role.",
    agent=assistant,
)

task2 = Task(
    description="The user asks: 'What technologies should I learn given my role?'",
    expected_output="Personalized technology recommendations based on the user's role.",
    agent=assistant,
    context=[task1],  # Explicit context passing
)

task3 = Task(
    description="The user asks: 'Can you remind me what I told you about myself?'",
    expected_output="Recall the user's name, role, and company from earlier.",
    agent=assistant,
    context=[task1, task2],
)

crew = Crew(
    agents=[assistant],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    memory=True,  # Enable CrewAI's memory system
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\nFinal:", result)
