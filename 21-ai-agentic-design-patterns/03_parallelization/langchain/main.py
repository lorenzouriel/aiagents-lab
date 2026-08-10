"""
Parallelization with LangChain
================================
Uses RunnableParallel to execute three independent research chains
concurrently, then synthesizes results in a final chain.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
parser = StrOutputParser()

# --- Three Independent Research Chains ---

def make_research_chain(domain):
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are an expert researcher in {domain}."),
        ("human", f"Write a 100-word summary of the top 3 {domain} trends in 2025."),
    ])
    return prompt | llm | parser

ai_chain = make_research_chain("artificial intelligence")
energy_chain = make_research_chain("renewable energy")
ev_chain = make_research_chain("electric vehicles")

# --- Run in Parallel ---

parallel = RunnableParallel(
    ai_summary=ai_chain,
    energy_summary=energy_chain,
    ev_summary=ev_chain,
)

# --- Synthesis Chain ---

synthesis_prompt = ChatPromptTemplate.from_messages([
    ("system", "You create executive briefs that find connections across domains."),
    ("human",
     "Combine these research summaries into a 200-word executive brief:\n\n"
     "AI Trends:\n{ai_summary}\n\n"
     "Energy Trends:\n{energy_summary}\n\n"
     "EV Trends:\n{ev_summary}"),
])
synthesis_chain = synthesis_prompt | llm | parser

# --- Full Pipeline: Parallel Research → Sequential Synthesis ---

full_chain = parallel | synthesis_chain

if __name__ == "__main__":
    # RunnableParallel expects a dict input; our chains ignore it
    result = full_chain.invoke({})
    print("\n" + "=" * 60)
    print("SYNTHESIZED REPORT:")
    print("=" * 60)
    print(result)
