"""
Memory with LangChain
======================
Demonstrates short-term (conversation buffer) and long-term
(vector store) memory patterns for maintaining agent context.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

# --- Short-Term Memory: Conversation History ---

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use conversation history to personalize responses."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm

# Simple in-memory conversation store
history = []


def chat(user_input: str) -> str:
    """Chat with short-term memory (conversation history)."""
    response = chain.invoke({"input": user_input, "history": history})
    # Update history
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response.content))
    return response.content


if __name__ == "__main__":
    print("=== Short-Term Memory Demo ===")
    print("User: My name is Lorenzo and I'm a data engineer at TechCorp.")
    print(f"AI: {chat('My name is Lorenzo and I work as a data engineer at TechCorp.')}")

    print("\nUser: What technologies should I learn given my role?")
    print(f"AI: {chat('What technologies should I learn given my role?')}")

    print("\nUser: What's my name and where do I work?")
    print(f"AI: {chat('Can you remind me what I told you about myself?')}")
