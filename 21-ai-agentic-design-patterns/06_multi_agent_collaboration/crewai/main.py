"""
Multi-Agent Collaboration with CrewAI
=======================================
A team of specialized agents collaborates to produce a blog post:
Researcher → Writer → Editor → Final output.
"""

from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Content Researcher",
    goal="Find key facts and talking points about a topic",
    backstory="You are a thorough researcher who gathers accurate, relevant information.",
    verbose=True,
)

writer = Agent(
    role="Blog Writer",
    goal="Write engaging, well-structured blog posts",
    backstory="You are a skilled writer who turns research into compelling narratives.",
    verbose=True,
)

editor = Agent(
    role="Content Editor",
    goal="Polish content for clarity, grammar, and engagement",
    backstory="You are a meticulous editor who ensures content is publication-ready.",
    verbose=True,
)

# --- Sequential Collaboration Pipeline ---

task_research = Task(
    description="Research the topic 'The Future of Edge AI' — gather 5 key points with supporting data.",
    expected_output="A structured list of 5 key points about Edge AI.",
    agent=researcher,
)

task_write = Task(
    description="Using the research, write a 300-word blog post about 'The Future of Edge AI'.",
    expected_output="A well-structured 300-word blog post.",
    agent=writer,
    context=[task_research],
)

task_edit = Task(
    description="Edit and polish the blog post for clarity, flow, and grammar. Provide the final version.",
    expected_output="A polished, publication-ready blog post.",
    agent=editor,
    context=[task_write],
)

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[task_research, task_write, task_edit],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("FINAL BLOG POST:")
    print("=" * 60)
    print(result)
