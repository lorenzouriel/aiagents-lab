"""
Routing with LangChain
=======================
Uses RunnableBranch to route customer requests to different handler
chains based on LLM classification.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# --- Router: classifies the intent ---
router_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify the user request into exactly one category: booking, info, or unclear. Respond with ONLY the category word."),
    ("human", "{request}"),
])
router_chain = router_prompt | llm | parser

# --- Handler chains ---
booking_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a booking specialist. Process this travel booking request."),
    ("human", "{request}"),
])
booking_chain = booking_prompt | llm | parser

info_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a travel information specialist. Provide helpful recommendations."),
    ("human", "{request}"),
])
info_chain = info_prompt | llm | parser

unclear_prompt = ChatPromptTemplate.from_messages([
    ("system", "The user's request is unclear. Ask 2-3 clarifying questions."),
    ("human", "{request}"),
])
unclear_chain = unclear_prompt | llm | parser

# --- Routing logic ---
def route(info):
    request = info["request"]
    category = router_chain.invoke({"request": request}).strip().lower()
    print(f"  [Router] Classified as: {category}")

    branch = RunnableBranch(
        (lambda _: "booking" in category, booking_chain),
        (lambda _: "info" in category, info_chain),
        unclear_chain,  # default fallback
    )
    return branch.invoke({"request": request})

if __name__ == "__main__":
    test_requests = [
        "Book me a flight from NYC to LA on March 25",
        "What are some good beaches in Thailand?",
        "I want to go somewhere warm next month",
    ]
    for req in test_requests:
        print(f"\nRequest: {req}")
        print(f"Response: {route({'request': req})}")
        print("-" * 50)
