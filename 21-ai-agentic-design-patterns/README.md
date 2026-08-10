# Agentic Design Patterns — Code Examples

A collection of practical examples demonstrating **21 agentic design patterns** using **CrewAI** and **LangChain**.

Each pattern folder contains two subdirectories:
- `crewai/` — Implementation using CrewAI framework
- `langchain/` — Implementation using LangChain / LangGraph

All credits to: [Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems](https://www.amazon.com.br/Agentic-Design-Patterns-Hands-Intelligent/dp/3032014018)

## Patterns

### Part I: Foundational Patterns
| # | Pattern | Description |
|---|---------|-------------|
| 01 | Prompt Chaining | Sequential sub-task decomposition |
| 02 | Routing | Conditional workflow selection |
| 03 | Parallelization | Concurrent independent task execution |
| 04 | Tool Use | External function calling and API integration |
| 05 | MCP | Model Context Protocol for standardized tool access |
| 06 | Multi-Agent Collaboration | Specialized agents working cooperatively |
| 07 | Inter-Agent Communication (A2A) | Cross-framework agent interoperability |

### Part II: Cognitive Patterns
| # | Pattern | Description |
|---|---------|-------------|
| 08 | Reflection | Self-evaluation and iterative improvement |
| 09 | Planning | Goal-directed action sequence generation |
| 10 | Goal Setting and Monitoring | Objective tracking with feedback loops |
| 11 | Advanced Reasoning | CoT, ReAct, Tree-of-Thought, and more |
| 12 | Memory | Short-term and long-term knowledge retention |
| 13 | Knowledge Retrieval (RAG) | External knowledge augmentation |
| 14 | Learning and Adaptation | Experience-based behavior modification |
| 15 | Exploration and Discovery | Autonomous knowledge-seeking |

### Part III: Production Patterns
| # | Pattern | Description |
|---|---------|-------------|
| 16 | Exception Handling and Recovery | Error detection, fallback, and recovery |
| 17 | Human-in-the-Loop | Human oversight and intervention |
| 18 | Guardrails and Safety | Input/output filtering and behavioral constraints |
| 19 | Resource-Aware Optimization | Dynamic model and resource selection |
| 20 | Prioritization | Task ranking and dynamic re-prioritization |
| 21 | Evaluation and Monitoring | Continuous performance assessment |

## Setup

```bash
pip install crewai langchain langchain-openai langchain-community langgraph faiss-cpu
export OPENAI_API_KEY="your-key-here"
```

> **Note:** These examples use `ChatOpenAI` as the default LLM. Replace with your preferred provider (Anthropic, Google, etc.) as needed. Some examples use simulated/mock responses for demonstration purposes.

## License
MIT
