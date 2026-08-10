"""
Exception Handling and Recovery with LangChain
================================================
Demonstrates retry logic, fallback chains, and graceful degradation.
"""

import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# --- Simulated APIs with failure ---

call_count = 0

def primary_api(query: str) -> str:
    global call_count
    call_count += 1
    if call_count <= 2:
        raise ConnectionError(f"API timeout (attempt {call_count})")
    return f"Primary data: Revenue $2.3M for {query}"

def fallback_api(query: str) -> str:
    return f"Cached data: Revenue ~$2M for {query} (approximate)"


def resilient_fetch(query: str, max_retries: int = 3) -> str:
    """Fetch with retry + fallback pattern."""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"  Attempt {attempt}: Trying primary API...")
            return primary_api(query)
        except ConnectionError as e:
            print(f"  ⚠ {e}")
            if attempt < max_retries:
                time.sleep(0.5)  # Backoff
            else:
                print("  Falling back to secondary API...")
                return fallback_api(query)

# --- Chain with error handling ---

prompt = ChatPromptTemplate.from_messages([
    ("system", "You summarize data. Mention the data source reliability."),
    ("human", "Data: {data}\nSummarize the findings."),
])
chain = prompt | llm | parser

if __name__ == "__main__":
    data = resilient_fetch("Q4 2025")
    print(f"\nRetrieved: {data}")
    print(f"Summary: {chain.invoke({'data': data})}")
