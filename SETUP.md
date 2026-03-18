# Environment Setup

## Step 1: Clone and enter the repo

```bash
git clone <repo-url>
cd Agentic_Tools
```

## Step 2: Create a Python virtual environment

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Git Bash):**
```bash
python -m venv .venv
source .venv/Scripts/activate
```

## Step 3: Add your API key

Create a file named `.env` in the **root of the repo** (not inside any unit folder):

```
OPENAI_API_KEY=sk-your-key-here
```

Never commit this file. Add it to `.gitignore` if it isn't already:
```
echo ".env" >> .gitignore
```

## Step 4: Install dependencies

Install only what you need for the unit you are working in.

**Unit 1 — LLM basics:**
```bash
pip install openai python-dotenv
```

**Unit 2 — Embeddings, RAG, Chroma, Gradio:**
```bash
pip install openai python-dotenv chromadb langchain-text-splitters matplotlib numpy gradio fire
```

**Unit 3 — Multi-agent workflows:**
```bash
pip install openai python-dotenv pyyaml
```

**Final Project:**
```bash
pip install openai python-dotenv pyyaml
```

## Step 5: Running scripts

**IMPORTANT: Always run scripts from the repo root directory**, not from inside a unit folder.

```bash
# Correct
python unit1/basic_response.py
python unit2/chroma_demo.py ingest --help
python unit3/agents.py unit3/single-agent.yaml

# Wrong — will fail with ModuleNotFoundError
cd unit1
python basic_response.py
```

This matters because every unit imports `usage.py` from the parent directory. Running from the repo root ensures Python can find it.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'usage'` | Running from inside a unit folder | `cd` back to repo root, then run again |
| `OPENAI_API_KEY not set` or similar | `.env` file missing or in wrong location | Create `.env` in the repo root (not inside a unit) |
| `ModuleNotFoundError: No module named 'chromadb'` | Unit 2 deps not installed | `pip install chromadb langchain-text-splitters` |
| `ModuleNotFoundError: No module named 'yaml'` | Unit 3 deps not installed | `pip install pyyaml` |
| `ModuleNotFoundError: No module named 'gradio'` | Gradio not installed | `pip install gradio` |
