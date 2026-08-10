"""
Evaluation and Monitoring with CrewAI
======================================
A QA agent evaluates another agent's output for accuracy,
helpfulness, and response quality.
"""

from crewai import Agent, Task, Crew, Process

responder = Agent(
    role="Customer Support Agent",
    goal="Answer customer questions accurately",
    backstory="You handle customer queries.",
    verbose=True,
)

evaluator = Agent(
    role="QA Evaluator",
    goal="Evaluate response quality on a 1-5 scale across multiple dimensions",
    backstory=(
        "You evaluate AI responses for: (1) Accuracy, (2) Completeness, "
        "(3) Helpfulness, (4) Clarity. Score each 1-5 and provide feedback."
    ),
    verbose=True,
)

task_respond = Task(
    description="Customer asks: 'How do I reset my password if I don't have access to my email?'",
    expected_output="A helpful response to the customer.",
    agent=responder,
)

task_evaluate = Task(
    description=(
        "Evaluate the response above on: Accuracy (1-5), Completeness (1-5), "
        "Helpfulness (1-5), Clarity (1-5). Provide an overall score and improvement suggestions."
    ),
    expected_output="Structured evaluation with scores and feedback.",
    agent=evaluator,
    context=[task_respond],
)

crew = Crew(agents=[responder, evaluator], tasks=[task_respond, task_evaluate], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    print(crew.kickoff())
