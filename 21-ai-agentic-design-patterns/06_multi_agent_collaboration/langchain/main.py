"""
Multi-Agent Collaboration with LangChain
==========================================
Three specialized chains (research, write, edit) collaborate
in a sequential pipeline to produce a polished blog post.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
parser = StrOutputParser()

# --- Agent Chains ---

research_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a thorough content researcher."),
        ("human", "Research '{topic}' and provide 5 key points with supporting data."),
    ]) | llm | parser
)

write_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a skilled blog writer."),
        ("human", "Using this research, write a 300-word blog post:\n\n{research}"),
    ]) | llm | parser
)

edit_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a meticulous content editor."),
        ("human", "Edit and polish this blog post for publication:\n\n{draft}"),
    ]) | llm | parser
)

# --- Collaboration Pipeline ---

def collaborate(topic: str) -> str:
    print("[Researcher] Gathering information...")
    research = research_chain.invoke({"topic": topic})

    print("[Writer] Drafting blog post...")
    draft = write_chain.invoke({"research": research})

    print("[Editor] Polishing final version...")
    final = edit_chain.invoke({"draft": draft})

    return final


if __name__ == "__main__":
    result = collaborate("The Future of Edge AI")
    print("\n" + "=" * 60)
    print("FINAL BLOG POST:")
    print("=" * 60)
    print(result)
