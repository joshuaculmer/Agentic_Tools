import argparse
import asyncio
import logging
import os
import sys
import webbrowser
from pathlib import Path

from dotenv import load_dotenv
import gui
import yaml
from openai import AsyncOpenAI

from run_agent import run_agent, as_tool, Agent, current_agent, conclude
from tools import ToolBox
from usage import print_usage

LOG_FORMAT = '%(filename)-10.10s %(levelname)-4.4s %(asctime)s %(message)s'

toolbox = ToolBox()
toolbox.tool(conclude)


@toolbox.tool
async def talk_to_user(message: str):
    """
    Use this function to communicate with the user.
    All communication to and from the user **MUST**
    be through this tool.
    :param message: The message to send to the user.
    :return: The user's response.
    """
    _agent = current_agent.get()
    name = _agent['name'] if _agent else 'Agent'
    await gui.send(f"{name}: {message}\n")
    response = await gui.receive()
    await gui.send_status('Thinking\u2026')
    return response

@toolbox.tool
async def send_message_to_user(message: str):
    """
    Use this function to send a message to user.
    All communication to and not from the user **MUST**
    be through this tool.
    :param message: The message to send to the user.
    :return: empty
    """
    _agent = current_agent.get()
    name = _agent['name'] if _agent else 'Agent'
    await gui.send(f"{name}: {message}\n")


async def main(agent_config: Path, message: str):
    client = AsyncOpenAI()
    usages = []

    def add_to_toolbox(_agent):
        if _agent['name'] == 'devils-advocate':
            _inner = as_tool(client, toolbox, _agent, usage=usages)
            async def _da_tool(input: str) -> str:
                await gui.send_status('Finding arguments\u2026')
                result = await _inner(input)
                await gui.send_status('Revising\u2026')
                return result
            _da_tool.__name__ = _agent['name']
            _da_tool.__doc__ = _agent.get('description', '')
            toolbox.tool(_da_tool)
        else:
            toolbox.tool(as_tool(client, toolbox, _agent, usage=usages))


    # with open(agent_config, 'rb') as f:
    #     content = f.read()
    
    # for i, byte in enumerate(content):
    #     try:
    #         bytes([byte]).decode('utf-8')
    #     except UnicodeDecodeError:
    #         # Grab surrounding context (30 chars either side)
    #         start = max(0, i - 30)
    #         end = min(len(content), i + 30)
    #         context = content[start:end].decode('latin-1')  # latin-1 never fails
            
    #         print(f"Position : {i}")
    #         print(f"Bad byte : {hex(byte)} (decimal: {byte})")
    #         print(f"Context  : ...{context}...")
    #         print(f"          {' ' * (i - start + 3)}^")
    #         print()
    # return
    agents: list[Agent] = list(yaml.safe_load_all(agent_config.read_text(encoding='utf-8')))

    for agent in agents:
        if agent['name'] == 'main':
            continue
        add_to_toolbox(agent)

    main_agent = next(agent for agent in agents if agent['name'] == 'main')

    response = await run_agent(
        client, toolbox, main_agent,
        message, usage=usages
    )

    if response:
        print(response)
        print()

    print_usage(usages)

    


def _configure_logging(debug: bool) -> None:
    local_level = logging.DEBUG if debug else logging.INFO
    use_dark_gray = (
        sys.stderr.isatty()
        and os.getenv('NO_COLOR') is None
        and os.getenv('TERM', '').lower() != 'dumb'
    )
    format_string = f'\x1b[90m{LOG_FORMAT}\x1b[0m' if use_dark_gray else LOG_FORMAT
    logging.basicConfig(
        level=logging.WARNING,
        format=format_string,
        datefmt='%H:%M:%S',
        force=True,
    )
    for logger_name in ('__main__', 'agents', 'run_agent', 'tools', 'usage'):
        logging.getLogger(logger_name).setLevel(local_level)


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('agent_config', type=Path, nargs='?', default=Path('agents.yaml'))
    parser.add_argument('message', nargs='?', default=None)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    _configure_logging(args.debug)

    async def _run():
        await gui.start_server()
        webbrowser.open('http://localhost:5173')
        await main(args.agent_config, args.message)

    asyncio.run(_run())
