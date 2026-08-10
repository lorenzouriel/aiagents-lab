"""
Model Context Protocol (MCP) Concept with CrewAI
==================================================
Demonstrates the MCP pattern conceptually: an agent discovers available
tools from a registry (simulating MCP server discovery) and uses them
dynamically. In production, this would connect to actual MCP servers.
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# --- Simulated MCP Server Registry ---
# In production, this would be an actual MCP server at /.well-known/agent.json

MCP_REGISTRY = {
    "weather_service": {
        "name": "WeatherBot",
        "version": "1.0.0",
        "capabilities": ["get_forecast", "get_alerts"],
        "endpoint": "http://weather-service.example.com/a2a",
    },
    "calendar_service": {
        "name": "CalendarBot",
        "version": "1.0.0",
        "capabilities": ["list_events", "create_event"],
        "endpoint": "http://calendar-service.example.com/a2a",
    },
}

@tool("Discover MCP Services")
def discover_services(query: str) -> str:
    """Discover available MCP services matching the query."""
    matches = []
    for sid, info in MCP_REGISTRY.items():
        if query.lower() in sid or query.lower() in info["name"].lower():
            matches.append(f"- {info['name']} (v{info['version']}): {', '.join(info['capabilities'])}")
    return "\n".join(matches) if matches else "No matching services found."


@tool("Call MCP Tool")
def call_mcp_tool(service_name: str, tool_name: str, params: str) -> str:
    """Call a tool on an MCP server. Params should be a JSON-like string."""
    # Simulated MCP server response
    return f"[MCP Response] {service_name}.{tool_name}({params}) → Success: Simulated result for demonstration."


# --- Agent ---

agent = Agent(
    role="MCP-Enabled Assistant",
    goal="Discover and use MCP services to fulfill user requests",
    backstory=(
        "You are an intelligent assistant that discovers available services "
        "via the Model Context Protocol before taking action."
    ),
    tools=[discover_services, call_mcp_tool],
    verbose=True,
)

task = Task(
    description=(
        "The user wants to know the weather forecast. First discover available "
        "weather services using MCP, then call the appropriate tool."
    ),
    expected_output="The weather forecast retrieved via MCP.",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(result)
