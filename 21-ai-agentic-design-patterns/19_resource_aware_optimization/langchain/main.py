"""
Resource-Aware Optimization with LangChain
============================================
Dynamic model selection based on query complexity assessment.
Routes simple queries to a cheaper model and complex ones to premium.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

# --- Model Tiers ---
models = {
    "simple": ChatOpenAI(model="gpt-4o-mini", temperature=0),      # Fast, cheap
    "complex": ChatOpenAI(model="gpt-4o-mini", temperature=0.3),    # In production: gpt-4o
}

def assess_complexity(query: str) -> str:
    if len(query.split()) < 10:
        return "simple"
    if any(w in query.lower() for w in ["analyze", "compare", "evaluate", "strategy"]):
        return "complex"
    return "simple"

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{query}"),
])

def resource_aware_query(query: str) -> str:
    complexity = assess_complexity(query)
    model = models.get(complexity, models["simple"])
    model_name = {"simple": "gpt-4o-mini (fast)", "complex": "gpt-4o (premium)"}.get(complexity, "gpt-4o-mini")
    print(f"  Complexity: {complexity} → Model: {model_name}")
    chain = prompt | model | parser
    return chain.invoke({"query": query})

if __name__ == "__main__":
    print(resource_aware_query("What is 2+2?"))
    print()
    print(resource_aware_query("Analyze the competitive landscape of the EV market and recommend a 3-year investment strategy."))
