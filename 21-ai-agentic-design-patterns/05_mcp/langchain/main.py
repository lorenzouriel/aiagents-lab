"""
Model Context Protocol (MCP) Concept with LangChain
=====================================================
Demonstrates MCP-style dynamic tool discovery and invocation.
Tools are registered in a simulated MCP server and discovered at runtime.
"""

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

# --- Simulated MCP Server ---

class MCPServer:
    """Simulates an MCP server that exposes tools and resources."""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self._tools = {}

    def register_tool(self, tool_id: str, description: str, handler):
        self._tools[tool_id] = {"description": description, "handler": handler}

    def discover(self) -> dict:
        """MCP discovery endpoint — returns available tools."""
        return {
            "name": self.name,
            "version": self.version,
            "tools": {tid: info["description"] for tid, info in self._tools.items()},
        }

    def invoke(self, tool_id: str, params: dict) -> str:
        """Execute a tool on this MCP server."""
        if tool_id not in self._tools:
            return f"Error: Tool '{tool_id}' not found on {self.name}"
        return self._tools[tool_id]["handler"](params)


# --- Set up MCP servers ---

weather_server = MCPServer("WeatherBot", "1.0.0")
weather_server.register_tool(
    "get_forecast",
    "Get weather forecast for a city",
    lambda p: f"Weather in {p.get('city', 'Unknown')}: 72°F, Sunny, Humidity 30%"
)

# --- LangChain Tools wrapping MCP ---

@tool
def mcp_discover(server_name: str) -> str:
    """Discover available tools on an MCP server."""
    servers = {"weather": weather_server}
    server = servers.get(server_name.lower())
    if not server:
        return f"No MCP server found: {server_name}"
    info = server.discover()
    tools_list = "\n".join(f"  - {tid}: {desc}" for tid, desc in info["tools"].items())
    return f"Server: {info['name']} v{info['version']}\nTools:\n{tools_list}"


@tool
def mcp_invoke(server_name: str, tool_id: str, city: str) -> str:
    """Invoke a tool on an MCP server with parameters."""
    servers = {"weather": weather_server}
    server = servers.get(server_name.lower())
    if not server:
        return f"No MCP server found: {server_name}"
    return server.invoke(tool_id, {"city": city})


# --- Agent ---

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [mcp_discover, mcp_invoke]
llm_with_tools = llm.bind_tools(tools)


def run_mcp_agent(query: str) -> str:
    messages = [HumanMessage(content=query)]
    for _ in range(5):
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        if not response.tool_calls:
            return response.content
        for tc in response.tool_calls:
            fn = {"mcp_discover": mcp_discover, "mcp_invoke": mcp_invoke}[tc["name"]]
            result = fn.invoke(tc["args"])
            messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
    return messages[-1].content


if __name__ == "__main__":
    print(run_mcp_agent("Discover the weather MCP server, then get the forecast for Los Angeles."))
