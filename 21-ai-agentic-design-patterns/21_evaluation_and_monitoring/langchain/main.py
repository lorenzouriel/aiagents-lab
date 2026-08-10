"""
Evaluation and Monitoring with LangChain
==========================================
LLM-as-a-Judge: evaluates agent responses on multiple quality
dimensions with structured scoring.
"""

import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# --- Agent Response ---
response_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a customer support agent."),
        ("human", "{question}"),
    ]) | llm | parser
)

# --- LLM-as-a-Judge Evaluator ---
eval_chain = (
    ChatPromptTemplate.from_messages([
        ("system",
         "You evaluate AI responses. Score each dimension 1-5.\n"
         "Return ONLY valid JSON: "
         '{{"accuracy": N, "completeness": N, "helpfulness": N, "clarity": N, "overall": N, "feedback": "..."}}'),
        ("human", "Question: {question}\nResponse: {response}\nEvaluate:"),
    ]) | llm | parser
)

def evaluate_response(question: str):
    response = response_chain.invoke({"question": question})
    print(f"Response: {response[:200]}...\n")

    eval_raw = eval_chain.invoke({"question": question, "response": response})
    try:
        scores = json.loads(eval_raw.replace("```json", "").replace("```", "").strip())
    except json.JSONDecodeError:
        scores = {"raw": eval_raw}

    print("Evaluation Scores:")
    for k, v in scores.items():
        if k != "feedback":
            print(f"  {k}: {v}")
    if "feedback" in scores:
        print(f"  Feedback: {scores['feedback']}")

if __name__ == "__main__":
    evaluate_response("How do I reset my password if I don't have access to my email?")
