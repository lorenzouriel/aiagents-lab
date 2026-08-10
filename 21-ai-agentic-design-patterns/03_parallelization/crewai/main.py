"""
Parallelization with CrewAI
============================
Three independent research agents work concurrently on different topics,
and a synthesis agent merges their findings into a unified report.
"""

from crewai import Agent, Task, Crew, Process

# --- Independent Research Agents ---

researcher_ai = Agent(
    role="AI Trends Researcher",
    goal="Research the latest trends in artificial intelligence",
    backstory="You are an AI industry analyst with deep technical knowledge.",
    verbose=True,
)

researcher_energy = Agent(
    role="Renewable Energy Researcher",
    goal="Research the latest trends in renewable energy",
    backstory="You are an energy sector specialist tracking clean tech innovations.",
    verbose=True,
)

researcher_ev = Agent(
    role="Electric Vehicle Researcher",
    goal="Research the latest trends in electric vehicles",
    backstory="You are an automotive industry analyst focused on EV technology.",
    verbose=True,
)

synthesizer = Agent(
    role="Report Synthesizer",
    goal="Combine multiple research summaries into a coherent executive brief",
    backstory="You excel at finding connections across different domains.",
    verbose=True,
)

# --- Independent Tasks (can run in parallel) ---

task_ai = Task(
    description="Write a 100-word summary of the top 3 AI trends in 2025.",
    expected_output="A concise summary of AI trends.",
    agent=researcher_ai,
)

task_energy = Task(
    description="Write a 100-word summary of the top 3 renewable energy trends in 2025.",
    expected_output="A concise summary of energy trends.",
    agent=researcher_energy,
)

task_ev = Task(
    description="Write a 100-word summary of the top 3 electric vehicle trends in 2025.",
    expected_output="A concise summary of EV trends.",
    agent=researcher_ev,
)

# --- Synthesis Task (sequential convergence) ---

task_synthesis = Task(
    description=(
        "Using the three research summaries, create a 200-word executive brief "
        "that highlights cross-domain connections and key takeaways."
    ),
    expected_output="A unified executive brief combining all research.",
    agent=synthesizer,
    context=[task_ai, task_energy, task_ev],
)

crew = Crew(
    agents=[researcher_ai, researcher_energy, researcher_ev, synthesizer],
    tasks=[task_ai, task_energy, task_ev, task_synthesis],
    process=Process.sequential,  # CrewAI handles parallel-capable tasks within sequential flow
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("SYNTHESIZED REPORT:")
    print("=" * 60)
    print(result)
