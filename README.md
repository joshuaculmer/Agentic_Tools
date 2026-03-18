# Agentic Engineering Course — CS301r

A hands-on learning journal from a university course on building agentic AI systems. This repo documents a full curriculum progression: from raw OpenAI API calls to multi-agent pipelines, embeddings-based retrieval, and a capstone Logic Checker project. All examples are real, working code used during the course.

## Who this is for

- Developers new to the OpenAI API who want grounded, runnable examples
- Students who want to see how agentic concepts build on each other unit by unit
- Anyone curious how multi-agent YAML configs, async tool-calling, and RAG pipelines work in practice

## Prerequisites

- Python 3.11+
- An OpenAI API key (with access to `gpt-4o-mini` or equivalent)

See [SETUP.md](SETUP.md) for full environment setup instructions.

## Learning Path

| Unit | Topic | Start Here |
|------|-------|-----------|
| [unit1](unit1/) | LLM basics, prompt engineering, token costs | `unit1/basic_response.py` |
| [unit2](unit2/) | Embeddings, RAG, tool calling, Chroma, MCP | `unit2/basic_embedding.py` |
| [unit3](unit3/) | Multi-agent workflows, YAML configs, guardrails | `unit3/agents.py` |
| [final_project](final_project/) | Logic Checker capstone (Socratic argument improver) | `final_project/main.py` |

## Repository Structure

```
Agentic_Tools/
├── README.md               <- You are here
├── SETUP.md                <- Start here for environment setup
│
├── unit1/                  <- LLM fundamentals and prompting
│   ├── basic_response.py   <- Minimal OpenAI API call
│   ├── chatbot.py          <- Stateful multi-turn chatbot
│   ├── usage.py            <- Shared token cost tracker (used by all units)
│   └── prompts/            <- Prompt files for experiments
│
├── unit2/                  <- Embeddings, RAG, tools, MCP
│   ├── basic_embedding.py  <- Embedding generation and semantic search
│   ├── chroma_demo.py      <- Chroma vector DB ingest + query CLI
│   ├── chatbot_with_weather.py <- Tool-calling chatbot with Gradio UI
│   └── Embeddings/         <- Pre-computed embeddings for books/
│
├── unit3/                  <- Multi-agent workflows
│   ├── run_agent.py        <- Core async agent execution engine
│   ├── agents.py           <- YAML config loader and entry point
│   ├── deep_research.yaml  <- 5-agent deep research pipeline
│   └── *.yaml              <- Agent config files
│
├── final_project/          <- Logic Checker capstone
│   ├── main.py             <- Entry point
│   └── agents.yaml         <- Socratic argument agent definition
│
└── books/                  <- Plain-text books used as embedding targets
```

## A Note on Learning Reports

Each unit contains `Learning_Report_N.md` files. These are the original author's personal reflections written during the course — what worked, what was surprising, what failed. They are **not instructions**. Read them after you have tried the code yourself to see how someone else thought through the same problems.

## Cost Awareness

All scripts use `usage.py`, which prints token counts and approximate USD cost after every API call. The cheapest model (`gpt-5-nano`) costs roughly $0.0001–$0.001 per run. Most experiments in this repo cost well under $0.01 total.
