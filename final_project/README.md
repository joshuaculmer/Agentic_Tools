# Final Project: Logic Checker

## What it is

A Socratic dialogue agent that helps you articulate and strengthen your personal beliefs through structured questioning. It does **not** tell you what to believe or fix your arguments for you. Instead, it identifies logical gaps and lets you close them yourself.

The goal is productive friction — a tool that deepens your reasoning rather than automating it.

## How it works

- Single YAML config (`agents.yaml`) with one main agent
- Uses the same `run_agent.py` engine from Unit 3
- Pure CLI interaction via the `talk_to_user` tool (no web UI)
- The agent follows a 4-step Socratic process defined in its system prompt:
  1. Ask what you believe
  2. Clarify your position with follow-up questions
  3. Have you establish your premises explicitly
  4. Surface logical gaps or fallacies — without providing corrections

## How to run

From the repo root:

```bash
python final_project/main.py
```

The agent will open with: *"What do you believe? What do you wish you could articulate better?"*

You respond with any belief you hold. It will probe your premises, surface unstated assumptions, and name any logical fallacies it finds. Only you can correct your own reasoning.

## Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point (mirrors `unit3/agents.py`) |
| `agents.yaml` | The Logic Checker agent definition and full Socratic system prompt |
| `run_agent.py` | Copy of the agent execution engine from unit3 |
| `tools.py` | Tool definitions (`talk_to_user`, `conclude`) |
| `usage.py` | Token cost tracking |

## Design documents

These files capture the prompt design process and iterations:

| File | What it contains |
|------|-----------------|
| `Argument_training_prompt.md` | Initial prompt design and training examples |
| `Focus_training_prompt.md` | A variant focused on keeping the user on-topic |
| `Idea_Consolodation_prompt.md` | A variant for consolidating related ideas |
| `Argument_training.md` | Extended design notes and example sessions |

## Example output

`Outputs/AI_Replacing_Developers.md` — A sample session analyzing the argument "AI will replace software developers."

## Project report

`Project_Report_16.md` documents the full design process: brainstorming study tool ideas, researching existing tools (NotebookLM, Studley.ai), deciding on argument mapping, iterating on the Socratic prompt, and reflecting on the result.

Read this report to understand *why* the agent is designed the way it is — particularly the deliberate choice to withhold answers.
