"""
Prompt Chaining with CrewAI
===========================
Demonstrates sequential task decomposition where each task's output
feeds into the next task. A market report is summarized, trends are
extracted, and an executive email is drafted.
"""

from crewai import Agent, Task, Crew, Process

# Agents (each handles one step in the chain)

summarizer = Agent(
    role="Market Research Summarizer",
    goal="Produce a concise summary of market research reports",
    backstory="You are an expert analyst who distills complex reports into clear summaries.",
    verbose=True,
)

trend_analyst = Agent(
    role="Trend Analyst",
    goal="Identify the top 3 emerging trends from a market summary",
    backstory="You specialize in spotting patterns and emerging market movements.",
    verbose=True,
)

email_writer = Agent(
    role="Executive Communications Writer",
    goal="Draft concise, actionable emails for leadership",
    backstory="You write clear, professional emails that executives actually read.",
    verbose=True,
)

# Tasks (chained sequentially)

SAMPLE_REPORT = """
Q4 2025 Consumer Tech Report: AI-powered personalization drove 73% of consumer
purchasing decisions. Sustainable product lines grew 28% YoY. Voice commerce
reached $19.4B in transaction volume. AR try-before-you-buy features reduced
returns by 34%. Privacy-first brands saw 2.1x higher customer retention.
"""

task_summarize = Task(
    description=f"Summarize the following market report into 3-4 key bullet points:\n{SAMPLE_REPORT}",
    expected_output="A concise bullet-point summary of the report's key findings.",
    agent=summarizer,
)

task_trends = Task(
    description=(
        "Using the summary from the previous task, identify the top 3 emerging "
        "trends. For each trend, provide a name and one supporting data point."
    ),
    expected_output="A structured list of 3 trends with supporting data.",
    agent=trend_analyst,
    context=[task_summarize],  # <-- chaining: uses output from task_summarize
)

task_email = Task(
    description=(
        "Draft a concise email to the VP of Marketing outlining the 3 trends "
        "identified in the previous task. Keep it under 150 words."
    ),
    expected_output="A professional email ready to send.",
    agent=email_writer,
    context=[task_trends],  # <-- chaining: uses output from task_trends
)

#  Crew (sequential process enforces the chain)

crew = Crew(
    agents=[summarizer, trend_analyst, email_writer],
    tasks=[task_summarize, task_trends, task_email],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("FINAL OUTPUT (Executive Email):")
    print("=" * 60)
    print(result)
