"""
Routing with CrewAI
====================
A coordinator agent classifies incoming customer requests and routes
them to specialized handler agents (booking, info, or clarification).
"""

from crewai import Agent, Task, Crew, Process

# --- Specialist Agents ---

router = Agent(
    role="Customer Request Router",
    goal="Classify customer requests into: booking, info, or unclear",
    backstory="You triage incoming requests with high accuracy.",
    verbose=True,
)

booking_agent = Agent(
    role="Booking Specialist",
    goal="Handle flight and hotel booking requests",
    backstory="You process travel bookings efficiently and confirm details.",
    verbose=True,
)

info_agent = Agent(
    role="Information Specialist",
    goal="Provide travel information and recommendations",
    backstory="You are a knowledgeable travel advisor.",
    verbose=True,
)

clarification_agent = Agent(
    role="Clarification Specialist",
    goal="Ask clarifying questions for vague or unclear requests",
    backstory="You gently ask the right questions to understand user intent.",
    verbose=True,
)

# --- Tasks ---

user_request = "I want to go somewhere warm next month"

route_task = Task(
    description=(
        f"Classify this customer request into exactly one category: "
        f"'booking', 'info', or 'unclear'.\n\nRequest: {user_request}\n\n"
        f"Respond with ONLY the category word."
    ),
    expected_output="A single word: booking, info, or unclear",
    agent=router,
)

handle_task = Task(
    description=(
        f"Based on the routing decision from the previous task, handle this "
        f"customer request appropriately:\n\nRequest: {user_request}"
    ),
    expected_output="A helpful response addressing the customer's needs.",
    agent=info_agent,  # Default; in production, you'd dynamically assign based on route
    context=[route_task],
)

crew = Crew(
    agents=[router, info_agent],
    tasks=[route_task, handle_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("ROUTED RESPONSE:")
    print("=" * 60)
    print(result)
