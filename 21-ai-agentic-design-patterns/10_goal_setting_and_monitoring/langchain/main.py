"""
Goal Setting and Monitoring with LangChain
============================================
Demonstrates goal definition, execution tracking, and progress
monitoring with a feedback loop for course correction.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
parser = StrOutputParser()

goal_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You define SMART goals with specific KPIs and thresholds."),
        ("human", "Define 3 SMART goals for: {objective}"),
    ]) | llm | parser
)

execute_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You simulate task execution and report progress metrics."),
        ("human", "Goals:\n{goals}\n\nSimulate week 1 progress and report metrics."),
    ]) | llm | parser
)

monitor_chain = (
    ChatPromptTemplate.from_messages([
        ("system",
         "You are a progress monitor. Compare metrics to goals, identify "
         "risks, and recommend adjustments."),
        ("human", "Goals:\n{goals}\n\nProgress:\n{progress}\n\nAnalyze and recommend."),
    ]) | llm | parser
)


def goal_monitor_loop(objective: str):
    print("[Goal Setter] Defining goals...")
    goals = goal_chain.invoke({"objective": objective})
    print(goals)

    print("\n[Executor] Running week 1...")
    progress = execute_chain.invoke({"goals": goals})
    print(progress)

    print("\n[Monitor] Evaluating progress...")
    analysis = monitor_chain.invoke({"goals": goals, "progress": progress})
    print(analysis)


if __name__ == "__main__":
    goal_monitor_loop("A content marketing campaign launching next month")
