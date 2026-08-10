"""
Guardrails and Safety with LangChain
======================================
Multi-layer safety: input validation, behavioral constraints via
system prompt, and output filtering before delivery.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# --- Layer 1: Input Validation ---
BLOCKED_PATTERNS = [r"hack", r"exploit", r"bypass.{0,10}security", r"illegal"]

def validate_input(text: str) -> tuple:
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False, f"Input blocked: matches prohibited pattern '{pattern}'"
    return True, "safe"

# --- Layer 2: Behavioral Constraints (System Prompt) ---
safe_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant. RULES: "
     "1. Never provide instructions for harmful activities. "
     "2. Never generate content that is discriminatory. "
     "3. If uncertain about safety, err on the side of caution. "
     "4. Always recommend consulting professionals for medical/legal/financial advice."),
    ("human", "{input}"),
])
safe_chain = safe_prompt | llm | parser

# --- Layer 3: Output Filtering ---
def filter_output(text: str) -> str:
    # Remove any PII patterns (simplified)
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
    text = re.sub(r"\b\d{16}\b", "[REDACTED-CC]", text)
    return text

# --- Full Pipeline ---
def safe_query(user_input: str) -> str:
    is_safe, reason = validate_input(user_input)
    if not is_safe:
        return f"⚠ {reason}"
    raw_output = safe_chain.invoke({"input": user_input})
    return filter_output(raw_output)

if __name__ == "__main__":
    print(safe_query("How can I improve my Python code performance?"))
    print()
    print(safe_query("How can I hack into a database?"))
