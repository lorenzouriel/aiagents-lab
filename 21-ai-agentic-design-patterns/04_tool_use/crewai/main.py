"""
Tool Use with CrewAI
=====================
Agents use custom tools to fetch weather data and perform calculations.
Demonstrates how CrewAI agents call external functions.
"""

import ast
import operator as op

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# --- Custom Tools ---

@tool("Get Weather")
def get_weather(city: str) -> str:
    """Get current weather for a city. Returns temperature and conditions."""
    # Simulated API response
    weather_data = {
        "new york": {"temp": 42, "condition": "Cloudy", "humidity": 65},
        "los angeles": {"temp": 72, "condition": "Sunny", "humidity": 30},
        "london": {"temp": 38, "condition": "Rainy", "humidity": 85},
    }
    data = weather_data.get(city.lower(), {"temp": 60, "condition": "Unknown", "humidity": 50})
    return f"{city}: {data['temp']}°F, {data['condition']}, Humidity: {data['humidity']}%"


_OPERATORS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg,
}

def _safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.n
    elif isinstance(node, ast.BinOp):
        return _OPERATORS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        return _OPERATORS[type(node.op)](_safe_eval(node.operand))
    raise ValueError(f"Unsupported operation: {type(node).__name__}")


@tool("Calculate")
def calculate(expression: str) -> str:
    """Evaluate a math expression and return the result."""
    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree.body)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {e}"


# --- Agent with Tools ---

assistant = Agent(
    role="Travel Weather Assistant",
    goal="Help users plan trips by checking weather and calculating travel costs",
    backstory="You are a helpful travel assistant with access to weather data and a calculator.",
    tools=[get_weather, calculate],
    verbose=True,
)

task = Task(
    description=(
        "The user is deciding between New York and Los Angeles for a weekend trip. "
        "Check the weather in both cities, then calculate the total cost if "
        "NY flights are $350 round-trip and LA flights are $280 round-trip, "
        "with 2 nights hotel at $200/night for both. Recommend the better option."
    ),
    expected_output="Weather comparison, cost breakdown, and a recommendation.",
    agent=assistant,
)

crew = Crew(agents=[assistant], tasks=[task], process=Process.sequential, verbose=True)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(result)
