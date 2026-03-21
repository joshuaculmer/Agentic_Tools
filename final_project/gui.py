import asyncio
import json
import logging

import websockets

# Suppress noisy EOFError spam from browser probe connections
logging.getLogger('websockets.server').setLevel(logging.CRITICAL)

_agent_to_gui: asyncio.Queue
_gui_to_agent: asyncio.Queue
_connected: set = set()


async def _handler(websocket):
    _connected.add(websocket)
    try:
        async for raw in websocket:
            data = json.loads(raw)
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


async def receive() -> str:
    return await _gui_to_agent.get()
