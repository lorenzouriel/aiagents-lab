"""
Learning and Adaptation with LangChain
========================================
Demonstrates experience-based adaptation: the agent reviews past
outcomes stored in memory and adjusts future behavior.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
parser = StrOutputParser()

# --- Experience Store ---
experience_log = [
    {"action": "Email campaign", "result": "12% open rate, 2% conversion", "lesson": "Subject lines were too generic"},
    {"action": "Social media push", "result": "25% engagement, 5% conversion", "lesson": "Visual content outperformed text"},
    {"action": "Blog series", "result": "8,000 views, 1% conversion", "lesson": "Missing clear CTAs"},
]

review_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You learn from past experience. Analyze results and extract actionable lessons."),
        ("human", "Past experiences:\n{experiences}\n\nExtract top 3 lessons."),
    ]) | llm | parser
)

adapt_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You design strategies based on lessons learned. Never repeat past mistakes."),
        ("human", "Lessons:\n{lessons}\n\nDesign next quarter's campaign strategy."),
    ]) | llm | parser
)

if __name__ == "__main__":
    exp_text = "\n".join(f"- {e['action']}: {e['result']} (Lesson: {e['lesson']})" for e in experience_log)
    lessons = review_chain.invoke({"experiences": exp_text})
    print("Lessons:", lessons)
    strategy = adapt_chain.invoke({"lessons": lessons})
    print("\nAdapted Strategy:", strategy)
