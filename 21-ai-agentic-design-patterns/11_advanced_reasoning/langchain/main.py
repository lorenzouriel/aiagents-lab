"""
Advanced Reasoning with LangChain
===================================
Demonstrates Chain-of-Thought prompting and a ReAct-style loop
where the agent alternates between thinking, acting, and observing.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
parser = StrOutputParser()

# --- Chain-of-Thought Example ---

cot_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert problem solver. Always think step by step. "
     "For each sub-question, show your reasoning before giving the answer. "
     "Format: Step 1: [reasoning]... Step 2: [reasoning]... Conclusion: ..."),
    ("human", "{question}"),
])
cot_chain = cot_prompt | llm | parser


# --- ReAct-Style Loop (simplified) ---

def react_loop(question: str, max_steps: int = 4) -> str:
    """Simplified ReAct: Thought → Action → Observation loop."""

    # Simulated knowledge base
    kb = {
        "python memory": "Python uses reference counting + cyclic GC.",
        "rust memory": "Rust uses ownership/borrowing, no GC.",
        "go memory": "Go uses concurrent tri-color mark-and-sweep GC.",
    }

    context = f"Question: {question}\n"

    for i in range(max_steps):
        # Thought
        thought_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are reasoning step by step. Based on context, decide what to research next or if you have enough info to conclude."),
            ("human", f"{context}\nStep {i+1} — What should you think about or look up next? If ready, write CONCLUDE."),
        ])
        thought = (thought_prompt | llm | parser).invoke({})
        context += f"\nThought {i+1}: {thought}"

        if "CONCLUDE" in thought.upper():
            break

        # Action: search KB
        for key, val in kb.items():
            if key.split()[0] in thought.lower():
                context += f"\nObservation {i+1}: {val}"
                break

    # Final synthesis
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "Synthesize your reasoning into a clear, structured answer."),
        ("human", context),
    ])
    return (final_prompt | llm | parser).invoke({})


if __name__ == "__main__":
    q = "How do Python, Rust, and Go handle memory management differently?"

    print("=== Chain-of-Thought ===")
    print(cot_chain.invoke({"question": q}))

    print("\n=== ReAct Loop ===")
    print(react_loop(q))
