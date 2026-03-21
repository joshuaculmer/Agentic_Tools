# GUI — Logic Helper Frontend

## Overview

This is the React + Vite + TypeScript frontend for the **Logic Helper** AI agent system. It renders a real-time chat interface that communicates with a Python WebSocket server (`gui.py`) over `ws://localhost:8765`.

The app is served by Vite's dev server at `http://localhost:5173`. The Python backend (`main.py`) opens this URL in the user's default browser automatically on startup.

## Architecture

```
main.py  ──(asyncio)──  gui.py  ──(WebSocket)──  gui/src/App.tsx
                         :8765                       :5173
```

- **`gui.py`** — asyncio WebSocket server. Bridges the Python agent loop and the browser.
- **`gui/src/App.tsx`** — Single-page chat UI. Manages WebSocket connection, message state, and status indicators.
- **`gui/src/App.css`** — All styling. Uses CSS custom properties defined in `index.css` for theming.

## WebSocket Message Protocol

### Backend → Frontend

| Shape | Meaning |
|---|---|
| `{ text: string }` | A chat message from the agent; rendered as a chat bubble. |
| `{ type: "status", text: string }` | A transient status update (e.g. "Thinking…", "Finding arguments…", "Revising…"). Shown as a subtle indicator, not a bubble. Cleared when the next chat message arrives. |

### Frontend → Backend

| Shape | Meaning |
|---|---|
| `{ text: string }` | The user's typed message; forwarded to the agent via `gui.receive()`. |

## Agent Status States

The backend emits status updates at key points in the agent loop:

| Status text | When it fires |
|---|---|
| `Thinking…` | Immediately after the user sends input, while the main agent processes it. |
| `Finding arguments…` | When the `devils-advocate` sub-agent is invoked. |
| `Revising…` | After `devils-advocate` returns, while the main agent re-evaluates. |

Status is automatically cleared in the frontend whenever a real chat message arrives.

## Project Context

The **Logic Helper** system is a multi-agent pipeline:

- **`main` agent** — Guides the user through formalizing a belief into logical premises, then critiques the argument structure using Socratic questioning.
- **`devils-advocate` agent** — Adversarial sub-agent that finds counter-arguments, logical fallacies, weak premises, and unsupported assumptions in the user's argument. Called by the main agent once the argument is developed enough.

The goal is to help users think more rigorously about things they personally care about — not to critique the beliefs themselves, only the logical structure of the argument.

## Development

```bash
# Install dependencies (run once)
npm install

# Start the Vite dev server
npm run dev
```

The Python backend must also be running (`python main.py`) for the WebSocket connection to succeed. The frontend will retry the connection every 2 seconds automatically.
