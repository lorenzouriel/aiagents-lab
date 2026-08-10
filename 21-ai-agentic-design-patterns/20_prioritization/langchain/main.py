"""
Prioritization with LangChain
===============================
Demonstrates task scoring and dynamic re-prioritization based on
weighted criteria (urgency, importance, dependencies).
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# --- Task definitions ---
tasks = [
    {"id": "A", "name": "Fix critical login bug", "urgency": 10, "importance": 10, "blocks": ["C", "E"]},
    {"id": "B", "name": "Update API documentation", "urgency": 2, "importance": 4, "blocks": []},
    {"id": "C", "name": "Deploy payment feature", "urgency": 8, "importance": 9, "blocks": []},
    {"id": "D", "name": "Refactor DB queries", "urgency": 3, "importance": 7, "blocks": []},
    {"id": "E", "name": "Set up monitoring", "urgency": 5, "importance": 6, "blocks": []},
]

def score_task(t):
    """Weighted priority score."""
    dep_bonus = len(t["blocks"]) * 2
    return 0.5 * t["urgency"] + 0.3 * t["importance"] + 0.2 * dep_bonus

def prioritize(task_list):
    scored = [(score_task(t), t) for t in task_list]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored

# --- LLM-enhanced justification ---
justify_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You explain task prioritization decisions concisely."),
        ("human", "Task: {name} (Score: {score:.1f}, Urgency: {urgency}, Importance: {importance}, Blocks: {blocks})\nExplain why this priority ranking is appropriate in 1-2 sentences."),
    ]) | llm | parser
)

if __name__ == "__main__":
    ranked = prioritize(tasks)
    for i, (score, t) in enumerate(ranked):
        label = f"P{i}"
        reason = justify_chain.invoke({**t, "score": score, "blocks": ", ".join(t["blocks"]) or "none"})
        print(f"{label}: [{t['id']}] {t['name']} (score: {score:.1f}) — {reason}")
