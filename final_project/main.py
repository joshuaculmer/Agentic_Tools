import argparse
import asyncio
import json
import logging
import os
import shutil
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import gui
import yaml
from openai import AsyncOpenAI

from gui import ConversationEndedError, ConversationRestartError
from run_agent import run_agent, as_tool, Agent, current_agent, conclude
from tools import ToolBox
from usage import print_usage

LOG_FORMAT = '%(filename)-10.10s %(levelname)-4.4s %(asctime)s %(message)s'

OUTPUTS_DIR = Path(__file__).parent / 'Outputs'

_conversation_log: list[dict] = []


def _save_and_clear_log() -> None:
    if not _conversation_log:
        return
    OUTPUTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = OUTPUTS_DIR / f'conversation_{timestamp}.json'
    path.write_text(json.dumps(_conversation_log, indent=2), encoding='utf-8')
    print(f'Saved conversation to {path}')
    _conversation_log.clear()


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
    _conversation_log.append({'role': 'agent', 'name': name, 'text': message})
    response = await gui.receive()
    _conversation_log.append({'role': 'user', 'text': response})
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

    initial_message = message
    while True:
        try:
            response = await run_agent(
                client, toolbox, main_agent,
                initial_message, usage=usages
            )
        except ConversationRestartError:
            gui.drain_input_queue()
            _save_and_clear_log()
            initial_message = None
            print('Restarting conversation…')
            continue
        except ConversationEndedError:
            _save_and_clear_log()
            print('Conversation ended by user.')
            break

        if response:
            print(response)
            print()
        _save_and_clear_log()
        break

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


async def _wait_for_port(host: str, port: int, timeout: float = 30.0) -> None:
    start = asyncio.get_event_loop().time()
    while True:
        try:
            _, writer = await asyncio.open_connection(host, port)
            writer.close()
            await writer.wait_closed()
            return
        except (ConnectionRefusedError, OSError):
            if asyncio.get_event_loop().time() - start > timeout:
                raise TimeoutError(f"Frontend not ready after {timeout}s")
            await asyncio.sleep(0.25)


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('agent_config', type=Path, nargs='?', default=Path('agents.yaml'))
    parser.add_argument('message', nargs='?', default=None)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    _configure_logging(args.debug)

    async def _run():
        gui_dir = Path(__file__).parent / 'gui'
        npm = shutil.which('npm') or ('npm.cmd' if sys.platform == 'win32' else 'npm')
        vite_proc = subprocess.Popen(
            [npm, 'run', 'dev'],
            cwd=gui_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            print('Starting frontend...', flush=True)
            await _wait_for_port('localhost', 5173)
            await gui.start_server()
            webbrowser.open('http://localhost:5173')
            await main(args.agent_config, args.message)
            print("Main is up and running")
        finally:
            if vite_proc.poll() is None:
                if sys.platform == 'win32':
                    subprocess.run(
                        ['taskkill', '/F', '/T', '/PID', str(vite_proc.pid)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                else:
                    vite_proc.terminate()
                try:
                    vite_proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    vite_proc.kill()

    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        pass
