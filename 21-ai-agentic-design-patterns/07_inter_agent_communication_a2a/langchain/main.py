"""
Inter-Agent Communication (A2A) Concept with LangChain
=======================================================
Simulates A2A protocol: Agent Cards, discovery via well-known URIs,
and standardized task delegation between agent services.
"""

# --- A2A Agent Card & Server Simulation ---

class A2AServer:
    """Simulates an A2A-compliant agent server."""

    def __init__(self, agent_card: dict):
        self.card = agent_card
        self._handlers = {}

    def register_skill(self, skill_id: str, handler):
        self._handlers[skill_id] = handler

    def get_agent_card(self) -> dict:
        """GET /.well-known/agent.json"""
        return self.card

    def send_task(self, skill_id: str, params: dict) -> dict:
        """JSON-RPC: tasks/send"""
        if skill_id not in self._handlers:
            return {"status": "failed", "error": f"Unknown skill: {skill_id}"}
        result = self._handlers[skill_id](params)
        return {"task_id": "t-001", "status": "completed", "result": result}


# --- Set up A2A servers ---

weather_server = A2AServer({
    "name": "WeatherAgent", "version": "1.0.0",
    "skills": [{"id": "get_forecast", "name": "Get Forecast"}],
})
weather_server.register_skill(
    "get_forecast",
    lambda p: f"Tokyo forecast: 68°F, Partly Cloudy"
)

booking_server = A2AServer({
    "name": "BookingAgent", "version": "2.1.0",
    "skills": [{"id": "book_flight", "name": "Book Flight"}],
})
booking_server.register_skill(
    "book_flight",
    lambda p: f"Flight booked: {p.get('from', '?')} → {p.get('to', '?')}, Confirmation #BK-7892"
)

# --- A2A Client (Coordinator) ---

REGISTRY = {"weather": weather_server, "booking": booking_server}


def a2a_discover(server_name: str) -> dict:
    server = REGISTRY.get(server_name)
    return server.get_agent_card() if server else {"error": "Not found"}


def a2a_send_task(server_name: str, skill_id: str, params: dict) -> dict:
    server = REGISTRY.get(server_name)
    return server.send_task(skill_id, params) if server else {"error": "Not found"}


if __name__ == "__main__":
    # Step 1: Discover agents
    print("=== Agent Discovery ===")
    for name in REGISTRY:
        card = a2a_discover(name)
        skills = ", ".join(s["name"] for s in card.get("skills", []))
        print(f"  {card['name']} v{card['version']} — Skills: {skills}")

    # Step 2: Send tasks
    print("\n=== Task Execution ===")
    weather = a2a_send_task("weather", "get_forecast", {"city": "Tokyo"})
    print(f"  Weather: {weather['result']}")

    flight = a2a_send_task("booking", "book_flight", {"from": "NYC", "to": "Tokyo"})
    print(f"  Booking: {flight['result']}")
