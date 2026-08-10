"""
Human-in-the-Loop with LangChain
==================================
Demonstrates an approval gate: the agent prepares actions but
requires human confirmation before executing high-stakes operations.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

analyze_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a financial analyst. Prepare trade recommendations."),
        ("human", "Analyze: Buy 100 shares of {ticker} at ${price}. Provide recommendation and risk level."),
    ]) | llm | parser
)

def human_approval_gate(recommendation: str) -> bool:
    """Pause for human approval before executing."""
    print(f"\n{'='*50}")
    print("HUMAN APPROVAL REQUIRED")
    print(f"{'='*50}")
    print(recommendation)
    print(f"{'='*50}")
    response = input("Approve this action? (yes/no): ").strip().lower()
    return response in ("yes", "y")

def execute_trade(ticker: str, shares: int, price: float):
    print(f"\n✓ EXECUTED: Bought {shares} shares of {ticker} at ${price}")

if __name__ == "__main__":
    rec = analyze_chain.invoke({"ticker": "AAPL", "price": "198"})
    if human_approval_gate(rec):
        execute_trade("AAPL", 100, 198.0)
    else:
        print("\n✗ Trade cancelled by human reviewer.")
