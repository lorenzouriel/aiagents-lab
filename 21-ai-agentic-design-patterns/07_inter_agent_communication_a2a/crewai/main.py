"""
Inter-Agent Communication (A2A) Concept with CrewAI
=====================================================
Simulates A2A protocol concepts: Agent Cards, discovery, and
cross-framework task delegation between independent agent services.
"""

import json
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# --- Simulated Agent Cards (A2A Discovery) ---

AGENT_CARDS = {
    "weather-agent": {
        "name": "WeatherAgent",
        "url": "http://weather.agents.local/a2a",
        "version": "1.0.0",
        "capabilities": {"streaming": False},
        "skills": [{"id": "get_forecast", "name": "Get Forecast"}],
    },
    "booking-agent": {
        "name": "BookingAgent",
        "url": "http://booking.agents.local/a2a",
        "version": "2.1.0",
        "capabilities": {"streaming": True},
        "skills": [
            {"id": "book_flight", "name": "Book Flight"},
            {"id": "book_hotel", "name": "Book Hotel"},
        ],
    },
}


@tool("Discover Remote Agents")
def discover_agents(query: str) -> str:
    """Discover remote agents via A2A Agent Cards. Returns available agents and their skills."""
    results = []
    for agent_id, card in AGENT_CARDS.items():
        if query.lower() in agent_id or query.lower() in card["name"].lower():
            skills = ", ".join(s["name"] for s in card["skills"])
            results.append(f"[{card['name']}] URL: {card['url']} | Skills: {skills}")
    return "\n".join(results) if results else "No agents found matching query."


@tool("Send A2A Task")
def send_a2a_task(agent_url: str, skill_id: str, params: str) -> str:
    """Send a task to a remote agent via A2A protocol."""
    # Simulated A2A JSON-RPC response
    return json.dumps({
        "task_id": "task-001",
        "status": "completed",
        "result": f"[Simulated] {skill_id} executed with params: {params}",
    })


# --- Coordinator Agent ---

coordinator = Agent(
    role="A2A Coordinator",
    goal="Discover and delegate tasks to specialized remote agents via A2A",
    backstory="You coordinate between multiple independent agent services using the A2A protocol.",
    tools=[discover_agents, send_a2a_task],
    verbose=True,
)

task = Task(
    description=(
        "The user wants to plan a trip: discover available agents, check weather "
        "for Tokyo, and book a flight from NYC to Tokyo."
    ),
    expected_output="Results from weather check and flight booking via A2A agents.",
    agent=coordinator,
)

crew = Crew(agents=[coordinator], tasks=[task], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\nResult:", result)
