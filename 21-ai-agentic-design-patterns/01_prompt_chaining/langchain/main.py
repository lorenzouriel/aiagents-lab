"""
Prompt Chaining with LangChain
===============================
Demonstrates sequential prompt chaining using LCEL (LangChain Expression Language).
Each step is a focused prompt whose output feeds into the next.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
parser = StrOutputParser()

# Step 1: Summarize 
summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert market analyst. Summarize reports into concise bullet points."),
    ("human", "Summarize this market report into 3-4 key findings:\n{report}"),
])

# Step 2: Extract Trends
trends_prompt = ChatPromptTemplate.from_messages([
    ("system", "You identify emerging market trends from summaries."),
    ("human", "From this summary, identify the top 3 trends with supporting data:\n{summary}"),
])

# Step 3: Draft Email
email_prompt = ChatPromptTemplate.from_messages([
    ("system", "You write concise executive emails. Keep it under 150 words."),
    ("human", "Draft an email to the VP of Marketing about these trends:\n{trends}"),
])

# Chain them together with LCEL
chain = (
    summarize_prompt | llm | parser |               # Step 1 → summary
    (lambda summary: {"summary": summary}) |
    trends_prompt | llm | parser |                   # Step 2 → trends
    (lambda trends: {"trends": trends}) |
    email_prompt | llm | parser                      # Step 3 → email
)

SAMPLE_REPORT = """
Q4 2025 Consumer Tech Report: AI-powered personalization drove 73% of consumer
purchasing decisions. Sustainable product lines grew 28% YoY. Voice commerce
reached $19.4B in transaction volume. AR try-before-you-buy features reduced
returns by 34%. Privacy-first brands saw 2.1x higher customer retention.
"""

if __name__ == "__main__":
    result = chain.invoke({"report": SAMPLE_REPORT})
    print("\n" + "=" * 60)
    print("FINAL OUTPUT (Executive Email):")
    print("=" * 60)
    print(result)
