"""
Exploration and Discovery with LangChain
==========================================
Generate-Debate-Evolve cycle: hypotheses are generated, critiqued,
and evolved iteratively to discover novel insights.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
parser = StrOutputParser()

generate = (
    ChatPromptTemplate.from_messages([
        ("system", "Generate creative, novel hypotheses."),
        ("human", "Topic: {topic}\nGenerate 3 novel hypotheses."),
    ]) | llm | parser
)

debate = (
    ChatPromptTemplate.from_messages([
        ("system", "Critically evaluate hypotheses for feasibility and novelty."),
        ("human", "Hypotheses:\n{hypotheses}\nRank and critique each."),
    ]) | llm | parser
)

evolve = (
    ChatPromptTemplate.from_messages([
        ("system", "Improve hypotheses based on critique. Make them stronger."),
        ("human", "Original:\n{hypotheses}\nCritique:\n{critique}\nProduce improved versions."),
    ]) | llm | parser
)


def explore(topic: str, cycles: int = 2) -> str:
    """Run the Generate-Debate-Evolve discovery loop."""
    print(f"[Generator] Generating initial hypotheses for: {topic}")
    hypotheses = generate.invoke({"topic": topic})

    for i in range(cycles):
        print(f"\n--- Cycle {i + 1} ---")
        print("[Critic] Debating hypotheses...")
        critique = debate.invoke({"hypotheses": hypotheses})
        print("[Evolver] Improving hypotheses...")
        hypotheses = evolve.invoke({"hypotheses": hypotheses, "critique": critique})

    return hypotheses


if __name__ == "__main__":
    result = explore("How AI could accelerate drug discovery")
    print("\n" + "=" * 60)
    print("FINAL HYPOTHESES:")
    print("=" * 60)
    print(result)
