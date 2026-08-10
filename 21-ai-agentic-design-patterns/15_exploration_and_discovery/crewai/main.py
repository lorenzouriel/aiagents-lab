"""
Exploration and Discovery with CrewAI
=======================================
Multiple agents explore a topic from different angles, debate findings,
and synthesize novel insights — mimicking scientific discovery.
"""

from crewai import Agent, Task, Crew, Process

explorer = Agent(
    role="Research Explorer",
    goal="Generate novel hypotheses about a topic",
    backstory="You explore uncharted territory and propose creative ideas.",
    verbose=True,
)

critic = Agent(
    role="Research Critic",
    goal="Evaluate hypotheses for feasibility and novelty",
    backstory="You rigorously evaluate ideas for scientific merit.",
    verbose=True,
)

synthesizer = Agent(
    role="Insight Synthesizer",
    goal="Combine the best ideas into actionable insights",
    backstory="You find connections others miss.",
    verbose=True,
)

t1 = Task(
    description="Generate 3 novel hypotheses about how AI could accelerate drug discovery.",
    expected_output="3 creative hypotheses.",
    agent=explorer,
)

t2 = Task(
    description="Evaluate each hypothesis for feasibility, novelty, and potential impact.",
    expected_output="Ranked evaluation of hypotheses.",
    agent=critic,
    context=[t1],
)

t3 = Task(
    description="Synthesize the top ideas into a research proposal outline.",
    expected_output="A brief research proposal.",
    agent=synthesizer,
    context=[t1, t2],
)

crew = Crew(
    agents=[explorer, critic, synthesizer],
    tasks=[t1, t2, t3],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    print(crew.kickoff())
