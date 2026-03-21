# AGENTS.md — Logic Helper

## Project Purpose
Logic Helper is a Socratic reasoning coach. It guides users through clarifying their beliefs, constructing explicit premises, and stress-testing their arguments via a multi-agent pipeline. The main agent asks probing questions; a secondary "devils-advocate" agent surfaces logical fallacies and weak premises without giving away corrections—forcing the user to fix their own reasoning.

## How to Run
```bash
# Install Python deps (first time)
pip install -r requirements.txt   # or: pip install openai websockets python-dotenv pyyaml

# Install frontend deps (first time)
cd gui && npm install && cd ..

# Set your API key
export OPENAI_API_KEY=sk-...       # or add to .env

# Launch
python main.py                     # opens browser automatically
python main.py agents.yaml "I believe X"   # optional initial message
python main.py --debug             # verbose logging
```

## Environment Requirements
| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Required. OpenAI API key used by all agents. |

A `.env` file in `final_project/` is loaded automatically via `python-dotenv`.

## Architecture

```
Browser (React)  ←─WebSocket──→  gui.py  ←─queues──→  main.py / run_agent.py
                                                              │
                                                    ┌─────────┴──────────┐
                                                    │   agents.yaml       │
                                                    │  ┌──────────────┐   │
                                                    │  │   main agent  │   │
                                                    │  │  (Socratic)   │   │
                                                    │  └──────┬───────┘   │
                                                    │         │ tool call  │
                                                    │  ┌──────▼───────┐   │
                                                    │  │devils-advocate│   │
                                                    │  │ (fallacy scan)│   │
                                                    │  └──────────────┘   │
                                                    └────────────────────┘
```

### Key Components

| File | Role |
|---|---|
| `main.py` | Entry point. Starts Vite dev server + WebSocket server, orchestrates agents. |
| `gui.py` | Async WebSocket server. Two queues: agent→GUI and GUI→agent. |
| `run_agent.py` | Agent execution loop. Calls OpenAI, handles tool calls, loops until done. |
| `tools.py` | `ToolBox` class — registers Python functions as agent tools. |
| `agents.yaml` | YAML definitions for all agents (name, model, prompt, tools). |
| `usage.py` | Tracks and prints token usage + cost after each run. |
| `gui/src/App.tsx` | React chat UI. WebSocket client, message bubbles, input box. |
| `gui/src/App.css` | Styling for the chat interface. |

## Agent Descriptions

### `main` (Socratic coach)
- Drives the conversation using Socratic questioning
- Asks what the user believes, then probes premises iteratively
- Calls `devils-advocate` as a tool when the user's argument needs stress-testing
- Uses `talk_to_user` for all user-facing messages
- Ends the session with the `conclude` tool

### `devils-advocate`
- Receives the user's argument as input
- Returns a list of counter-arguments, logical fallacies, and weak premises
- Takes an adversarial but professional tone
- Deliberately does NOT provide corrections — the user must revise their own reasoning

## WebSocket Protocol
All messages are JSON sent over `ws://localhost:8765`.

| Direction | Shape | Meaning |
|---|---|---|
| Agent → GUI | `{"text": "..."}` | Agent message to display |
| Agent → GUI | `{"type": "status", "text": "..."}` | Status bar update (e.g. "Thinking…") |
| GUI → Agent | `{"text": "..."}` | User's message |
| GUI → Agent | `{"type": "end"}` | User clicked "End" — triggers graceful shutdown |

## Frontend Stack
- **React 19** + **TypeScript**
- **Vite** dev server on `http://localhost:5173`
- Custom CSS (no UI library)
- Auto-reconnects to WebSocket every 2 seconds if disconnected

## Conversation Flow
1. User runs `python main.py`
2. Vite dev server starts, browser opens automatically
3. WebSocket connects (status badge turns green)
4. Main agent sends its opening question via `talk_to_user`
5. User types a response and presses Enter (or clicks Send)
6. Agent processes, may call `devils-advocate`, sends follow-up
7. Loop continues until agent calls `conclude` or user clicks "End"
