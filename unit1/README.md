# Unit 1: LLM Fundamentals

## What you will learn

- How to call the OpenAI API directly (no frameworks)
- How reasoning effort levels affect output quality and cost
- How to track token usage and USD cost per API call with `usage.py`
- Prompt engineering basics: personas, structured output, sequential tasks
- How to build a simple stateful multi-turn chatbot

## Prerequisites

Complete [SETUP.md](../SETUP.md) first. Unit 1 only needs:
```bash
pip install openai python-dotenv
```

## Key files

| File | Purpose |
|------|---------|
| `basic_response.py` | Minimal API call — the simplest possible starting point |
| `response.py` | More structured response handling |
| `usage.py` | Shared utility: prints token counts and USD cost after each call. Used by every unit. |
| `chatbot.py` | Stateful multi-turn chatbot (Gradio UI) |
| `text_processor.py` | Text transformation examples |
| `prime_number_sum.py` | Math reasoning task — good for testing reasoning effort levels |

## The `prompts/` folder

Prompt files loaded by `basic_response.py` and other scripts. Key ones to look at:

| File | What it tests |
|------|--------------|
| `Reasoning/` | Logic puzzles (list primes, long division, grandma puzzle) |
| `Philosophy/` | Open-ended reasoning |
| `game-*.md` | Classification and summarization tasks |
| `gandalf/` | Prompt injection / jailbreak resistance |
| `hallucination_attempt*.md` | Testing model honesty and refusal |
| `persona/roles/` | System prompt persona examples (student, therapist) |

## Learning Reports 1–6

These are personal reflections written during the course. Read them after trying the code yourself.

- **Report 1–2:** First API calls, exploring multilingual robustness, early jailbreak attempts
- **Report 3–4:** Structured output, sequential tasks, chatbot behavior
- **Report 5–6:** Reasoning effort levels (minimal/medium/high), token cost comparison across models

## Try it yourself

1. Run the simplest example from the repo root:
   ```bash
   python unit1/basic_response.py
   ```

2. Open `basic_response.py` and swap the model name (e.g., from `gpt-5-nano` to `gpt-5-mini`). Re-run and compare the cost printed by `usage.py`.

3. Edit any prompt file in `unit1/prompts/` and re-run to immediately see the effect — no Python changes needed.

4. In `prime_number_sum.py`, look for the `reasoning` parameter and try changing the effort level. Observe how the output and token count change.
