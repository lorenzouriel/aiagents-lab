"""
Reflection with LangChain
===========================
Implements a Producer-Critic reflection loop that iteratively
improves content through structured feedback cycles.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
parser = StrOutputParser()

# --- Producer Chain ---
producer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a technical writer. Write clear, accurate explanations."),
    ("human", "{instruction}"),
])
producer_chain = producer_prompt | llm | parser

# --- Critic Chain ---
critic_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a senior technical reviewer. Evaluate the draft for: "
     "(1) accuracy, (2) completeness, (3) clarity, (4) missing examples. "
     "Provide specific, actionable feedback."),
    ("human", "Review this draft:\n\n{draft}"),
])
critic_chain = critic_prompt | llm | parser

# --- Refiner Chain ---
refine_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a technical writer incorporating reviewer feedback."),
    ("human",
     "Original draft:\n{draft}\n\nReviewer feedback:\n{feedback}\n\n"
     "Produce an improved version addressing all feedback."),
])
refine_chain = refine_prompt | llm | parser


def reflect(instruction: str, max_iterations: int = 2) -> str:
    """Run the reflection loop: produce → critique → refine."""
    print(f"[Producer] Generating initial draft...")
    draft = producer_chain.invoke({"instruction": instruction})

    for i in range(max_iterations):
        print(f"\n[Critic] Iteration {i + 1} — reviewing...")
        feedback = critic_chain.invoke({"draft": draft})
        print(f"  Feedback: {feedback[:100]}...")

        print(f"[Refiner] Incorporating feedback...")
        draft = refine_chain.invoke({"draft": draft, "feedback": feedback})

    return draft


if __name__ == "__main__":
    result = reflect("Write a 200-word explanation of how database indexing works.")
    print("\n" + "=" * 60)
    print("FINAL OUTPUT:")
    print("=" * 60)
    print(result)
