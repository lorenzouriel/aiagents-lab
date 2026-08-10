"""
Guardrails and Safety with CrewAI
==================================
Input validation, output filtering, and behavioral constraints
to ensure safe agent operation.
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# --- Input Guardrail ---
BLOCKED_TOPICS = ["hack", "exploit", "bypass security", "illegal"]

@tool("Input Validator")
def validate_input(user_message: str) -> str:
    """Validate user input for safety. Returns 'safe' or 'blocked: reason'."""
    for topic in BLOCKED_TOPICS:
        if topic in user_message.lower():
            return f"blocked: Message contains prohibited topic '{topic}'"
    if len(user_message) > 2000:
        return "blocked: Message exceeds maximum length"
    return "safe"

agent = Agent(
    role="Safe Assistant",
    goal="Help users while enforcing safety policies",
    backstory=(
        "You ALWAYS validate input before responding. If input is blocked, "
        "explain that you cannot help with that topic. Never bypass safety rules."
    ),
    tools=[validate_input],
    verbose=True,
)

task = Task(
    description="Process this user request: 'How to hack a computer?'",
    expected_output="A helpful, safe response.",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    print(crew.kickoff())
