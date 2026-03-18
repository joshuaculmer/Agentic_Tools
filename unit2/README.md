# Unit 2: Embeddings, RAG, Tools, and MCP

## What you will learn

- What embeddings are and how to compute them via the OpenAI API
- How to chunk large text files for embedding
- Semantic search: finding text by meaning, not keyword
- Storing and querying embeddings with Chroma vector DB
- Giving an LLM access to external tools (function calling)
- Building a web chatbot with Gradio
- MCP (Model Context Protocol) server basics

## Prerequisites

Complete [SETUP.md](../SETUP.md) first. Unit 2 needs:
```bash
pip install openai python-dotenv chromadb langchain-text-splitters matplotlib numpy gradio fire
```

## Key files

| File | Purpose |
|------|---------|
| `basic_embedding.py` | Core embedding utilities: `embed()`, `chunk_text()`, `search_embeddings()`. Start here. |
| `chroma_demo.py` | Chroma ingest + semantic query with a `fire` CLI. See `chroma_readme.md` for usage. |
| `chatbot_with_weather.py` | LLM + tool calling (live weather API) + Gradio web UI |
| `scripturebot.py` | RAG chatbot over scripture texts using BYU Scripture API |
| `statsbot.py` | Statistical analysis chatbot with tool calling |
| `tools.py` | Reusable tool schema definitions (`FunctionToolParam`) |
| `Conference_Chatbot.py` | RAG chatbot over 2025 General Conference talks |
| `fastmcp_server/` | FastMCP server examples |
| `aws_mcp_server/` | AWS integration MCP server (Docker + Terraform) |

## The `books/` folder (repo root)

Three large plain-text books used as embedding targets in experiments:
- `King_James_Bible.txt`
- `Book_Of_Mormon.txt`
- `The_Count_Of_Monte_Cristo.txt`

These are sourced from Project Gutenberg.

## The `Embeddings/` folder

Pre-computed embeddings (JSON) for the three books above. These are large files. If they are missing or you want to regenerate them, run `basic_embedding.py` with the `__main__` block pointing at the `books/` directory.

## Chroma CLI (`chroma_demo.py`)

This file exposes a `fire` CLI. See [chroma_readme.md](chroma_readme.md) for full documentation. Quick reference:

```bash
# Ingest a folder of text files into Chroma
python unit2/chroma_demo.py ingest \
  --persist_dir=./unit2/db \
  --chroma_collection_name=my_docs \
  --folder=./books

# Query the collection
python unit2/chroma_demo.py query \
  --chroma_dir=./unit2/db \
  --collection=my_docs \
  --query="divine justice"
```

## The `Conf/` folder

Contains 2025 General Conference talk texts (68+ talks) used by `Conference_Chatbot.py`. Organized into `2025_Apr/` and `2025_Oct/` subfolders.

## Learning Reports 7–13

Personal reflections written during the course. Highlights:

- **Report 7:** First embeddings experiment — chunking The Count of Monte Cristo, querying for "What happened to Edmond Dantes"
- **Report 8:** RAG applications research — legal and religious domain use cases
- **Report 9:** Tool calling fundamentals — Statsbot and ISS coordinates bot
- **Report 10:** Mixed agents with tools — comparing results with and without tool access
- **Report 11–12:** Conference chatbot with Chroma, vector DB setup
- **Report 13:** Ethical considerations — appropriate vs inappropriate AI uses

## Try it yourself

1. Run the basic embedding search:
   ```bash
   python unit2/basic_embedding.py
   ```

2. Change the query string at the bottom of `basic_embedding.py` to something else and re-run.

3. Run the weather chatbot (opens a Gradio UI in your browser):
   ```bash
   python unit2/chatbot_with_weather.py
   ```

4. Try ingesting a folder into Chroma and querying it:
   ```bash
   python unit2/chroma_demo.py ingest --persist_dir=./unit2/mydb --chroma_collection_name=test --folder=./unit1/prompts
   python unit2/chroma_demo.py query --chroma_dir=./unit2/mydb --collection=test --query="logic puzzle"
   ```
