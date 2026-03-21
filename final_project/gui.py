import asyncio
import json
import logging

import websockets

# Suppress noisy EOFError spam from browser probe connections
logging.getLogger('websockets.server').setLevel(logging.CRITICAL)

_agent_to_gui: asyncio.Queue
_gui_to_agent: asyncio.Queue
_connected: set = set()

_END_SENTINEL = object()
_RESTART_SENTINEL = object()


class ConversationEndedError(Exception):
    pass


class ConversationRestartError(Exception):
    pass


async def _handler(websocket):
    _connected.add(websocket)
    try:
        async for raw in websocket:
            data = json.loads(raw)
            if data.get('type') == 'end':
                await _gui_to_agent.put(_END_SENTINEL)
            elif data.get('type') == 'restart':
                await _gui_to_agent.put(_RESTART_SENTINEL)
            else:
                await _gui_to_agent.put(data['text'])
    finally:
        _connected.discard(websocket)


async def _broadcast_loop():
    global _connected
    while True:
        msg = await _agent_to_gui.get()
        if isinstance(msg, dict):
            payload = json.dumps(msg)
        else:
            payload = json.dumps({'text': msg})
        dead = set()
        for ws in list(_connected):
            try:
                await ws.send(payload)
            except Exception:
                dead.add(ws)
        _connected -= dead


async def start_server(host: str = 'localhost', port: int = 8765):
    global _agent_to_gui, _gui_to_agent
    _agent_to_gui = asyncio.Queue()
    _gui_to_agent = asyncio.Queue()
    server = await websockets.serve(_handler, host, port)
    asyncio.create_task(_broadcast_loop())
    return server


async def send(msg: str):
    await _agent_to_gui.put(msg)


async def send_status(text: str):
    await _agent_to_gui.put({'type': 'status', 'text': text})


def drain_input_queue():
    """Discard any queued user messages (call before restarting the agent)."""
    while not _gui_to_agent.empty():
        try:
            _gui_to_agent.get_nowait()
        except asyncio.QueueEmpty:
            break


async def receive() -> str:
    msg = await _gui_to_agent.get()
    if msg is _END_SENTINEL:
        raise ConversationEndedError()
    if msg is _RESTART_SENTINEL:
        raise ConversationRestartError()
    return msg
