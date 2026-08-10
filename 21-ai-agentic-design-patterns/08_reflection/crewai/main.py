"""
Reflection with CrewAI
=======================
Producer-Critic model: a writer drafts content, a critic evaluates it,
and the writer refines based on feedback.
"""

from crewai import Agent, Task, Crew, Process

producer = Agent(
    role="Technical Writer",
    goal="Write clear, accurate technical explanations",
    backstory="You write first drafts of technical content.",
    verbose=True,
)

critic = Agent(
    role="Senior Technical Reviewer",
    goal="Provide detailed, constructive feedback on technical writing",
    backstory=(
        "You are a senior engineer who reviews content for accuracy, "
        "completeness, clarity, and technical depth. You are thorough but fair."
    ),
    verbose=True,
)

refiner = Agent(
    role="Technical Writer (Refinement)",
    goal="Incorporate feedback to produce a polished final version",
    backstory="You revise drafts based on reviewer feedback.",
    verbose=True,
)

# --- Reflection Loop (Draft → Critique → Refine) ---

task_draft = Task(
    description="Write a 200-word explanation of how database indexing works.",
    expected_output="A 200-word technical explanation.",
    agent=producer,
)

task_critique = Task(
    description=(
        "Review the draft for: (1) Technical accuracy, (2) Completeness, "
        "(3) Clarity, (4) Missing examples. Provide specific, actionable feedback."
    ),
    expected_output="Structured feedback with specific improvement suggestions.",
    agent=critic,
    context=[task_draft],
)

task_refine = Task(
    description="Incorporate the reviewer's feedback to produce a polished final version.",
    expected_output="A refined, publication-ready explanation.",
    agent=refiner,
    context=[task_draft, task_critique],
)

crew = Crew(
    agents=[producer, critic, refiner],
    tasks=[task_draft, task_critique, task_refine],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("FINAL (REFINED) OUTPUT:")
    print("=" * 60)
    print(result)
