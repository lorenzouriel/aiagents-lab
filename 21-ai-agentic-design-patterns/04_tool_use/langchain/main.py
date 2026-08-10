"""
Tool Use with LangChain
========================
Demonstrates function calling with LangChain tools and an agent executor.
"""

import ast
import operator as op

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

# --- Custom Tools ---

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city. Returns temperature and conditions."""
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


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression and return the result."""
    try:
        tree = ast.parse(expression, mode="eval")
        return str(_safe_eval(tree.body))
    except Exception as e:
        return f"Error: {e}"


# --- LLM with Tool Binding ---

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [get_weather, calculate]
llm_with_tools = llm.bind_tools(tools)

# --- Simple ReAct-style Tool Loop ---

def run_agent(query: str) -> str:
    """Run a simple tool-calling loop."""
    messages = [HumanMessage(content=query)]

    for _ in range(5):  # max iterations
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return response.content

        # Execute each tool call
        for tc in response.tool_calls:
            tool_fn = {"get_weather": get_weather, "calculate": calculate}[tc["name"]]
            result = tool_fn.invoke(tc["args"])
            messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))

    return messages[-1].content


if __name__ == "__main__":
    query = (
        "Check the weather in New York and Los Angeles. Then calculate the total "
        "trip cost for each: NY flights $350 + 2 nights at $200, LA flights $280 + "
        "2 nights at $200. Which city should I visit?"
    )
    print(run_agent(query))
