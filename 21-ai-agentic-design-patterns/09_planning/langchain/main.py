"""
Planning with LangChain
========================
Demonstrates a plan-and-execute pattern: an LLM generates a plan,
then each step is executed sequentially with status tracking.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
parser = StrOutputParser()

# --- Planning Chain ---
plan_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a strategic planner. Given a goal, produce a numbered "
     "step-by-step plan. Each step should be concrete and actionable."),
    ("human", "Goal: {goal}\n\nCreate a detailed plan with 6+ steps."),
])
plan_chain = plan_prompt | llm | parser

# --- Step Executor ---
exec_prompt = ChatPromptTemplate.from_messages([
    ("system", "You execute plan steps and report results concisely."),
    ("human", "Execute this step and report status:\n\nPlan context: {plan}\n\nCurrent step: {step}"),
])
exec_chain = exec_prompt | llm | parser


def plan_and_execute(goal: str):
    print("[Planner] Generating plan...")
    plan = plan_chain.invoke({"goal": goal})
    print(f"\n{plan}\n")

    # Parse steps (simple line-based parsing)
    steps = [line.strip() for line in plan.split("\n") if line.strip() and line.strip()[0].isdigit()]

    print("=" * 50)
    print("[Executor] Executing plan...")
    for step in steps[:6]:
        result = exec_chain.invoke({"plan": plan, "step": step})
        print(f"\n  {step}")
        print(f"  → {result[:150]}...")

    print("\n✓ Plan execution complete.")


if __name__ == "__main__":
    plan_and_execute(
        "Organize a 2-day team offsite for 15 people in Austin, TX with a $10,000 budget."
    )
