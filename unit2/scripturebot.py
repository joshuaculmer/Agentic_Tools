# Before running this script:
# pip install gradio openai

import argparse
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv
import gradio as gr
from openai import AsyncOpenAI
from tools import ToolBox
from usage import print_usage, format_usage_markdown
import httpx
from bs4 import BeautifulSoup
from urllib.parse import quote


our_tools = ToolBox()

@our_tools.tool
async def search_byu_scriptures(query: str) -> str:
    """
    Search scriptures.byu.edu for LDS conference talks and scripture references. 
    
    Returns titles, talk IDs, and context snippets. 
    
    Use the talk ID with get_byu_talk to fetch full content.
    """
    encoded_query = quote(query)
    url = f"https://scriptures.byu.edu/citation_index/search_results_ajax/t&&1830&2026&gjt&r&30@0${encoded_query}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for item in soup.select("li.grid a"):
        # Extract talk ID from onclick="getTalk('8702', '', ...)"
        onclick = item.get("onclick", "")
        talk_id = ""
        if "getTalk(" in onclick:
            try:
                talk_id = onclick.split("getTalk('")[1].split("'")[0]
            except IndexError:
                pass

        title_el = item.select_one(".resultTitle")
        context_el = item.select_one(".resultContext")
        title = title_el.get_text(strip=True) if title_el else ""
        context = context_el.get_text(strip=True) if context_el else ""

        if title:
            results.append(f"ID: {talk_id}\nTITLE: {title}\nCONTEXT: {context}")

    total_el = soup.select_one(".qSummary")
    total = total_el.get_text(strip=True) if total_el else ""

    if not results:
        return "No results found."

    header = f"{total} for '{query}':\n\n"
    return header + "\n\n---\n\n".join(results)

@our_tools.tool
async def get_byu_talk(talk_id: str, slug: str) -> str:
    """
    Fetch the full text of a conference talk from scriptures.byu.edu. 
    Use the talk ID and a URL slug derived from the talk title (lowercase, hyphenated, e.g. 'think-celestial'). 
    Returns the full talk text with author and title.
    """
    url = f"https://scriptures.byu.edu/content/talks_ajax/{talk_id}/{slug}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.select_one("h1")
    author = soup.select_one(".byline")
    body_paragraphs = soup.select("#primary p")

    title_text = title.get_text(strip=True) if title else "Unknown Title"
    author_text = author.get_text(separator=" ", strip=True) if author else "Unknown Author"
    body_text = "\n\n".join(p.get_text(strip=True) for p in body_paragraphs if p.get_text(strip=True))

    return f"TITLE: {title_text}\nAUTHOR: {author_text}\n\n{body_text}"

class ChatAgent:
    def __init__(self, model: str, prompt: str, show_reasoning: bool, reasoning_effort: str | None):
        self._ai = AsyncOpenAI()
        self.model = model
        self.show_reasoning = show_reasoning
        self.reasoning = {}
        if show_reasoning:
            self.reasoning['summary'] = 'auto'
        if 'gpt-5' in self.model and reasoning_effort:
            self.reasoning['effort'] = reasoning_effort

        self.usage = []
        self.usage_markdown = format_usage_markdown(self.model, [])

        self._history = []
        self._prompt = prompt
        if prompt:
            self._history.append({'role': 'system', 'content': prompt})

    async def get_response(self, user_message: str):
        self._history.append({'role': 'user', 'content': user_message})

        while True:
            response = await self._ai.responses.create(
                input=self._history,
                model=self.model,
                reasoning=self.reasoning,
                tools=our_tools.tools
            )

            self.usage.append(response.usage)
            self.usage_markdown = format_usage_markdown(self.model, self.usage)
            self._history.extend(
                response.output
            )

            for item in response.output:
                if item.type == 'reasoning':
                    for chunk in item.summary:
                        yield 'reasoning', chunk.text

                elif item.type == 'function_call':
                    yield 'reasoning', f'{item.name}({item.arguments})'

                    func = our_tools.get_tool_function(item.name)
                    args = json.loads(item.arguments)
                    result = await func(**args)
                    self._history.append({
                        'type': 'function_call_output',
                        'call_id': item.call_id,
                        'output': str(result)
                    })
                    yield 'reasoning', str(result)

                elif item.type == 'message':
                    for chunk in item.content:
                        yield 'output', chunk.text
                    return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print_usage(self.model, self.usage)


async def _main_console(agent_args):
    with ChatAgent(**agent_args) as agent:
        while True:
            message = input('User: ')
            if not message or message == "exit":
                break

            reasoning_complete = True
            if agent.show_reasoning:
                print(' Reasoning '.center(30, '-'))
                reasoning_complete = False

            async for text_type, text in agent.get_response(message):
                if text_type == 'output' and not reasoning_complete:
                    print()
                    print('-' * 30)
                    print()
                    print('Agent: ')
                    reasoning_complete = True

                print(text, end='', flush=True)
            print()
            print()


def _main_gradio(agent_args):
    # Constrain width with CSS and center
    css = """
    /* limit overall Gradio app width and center it */
    .gradio-container, .gradio-app, .gradio-root {
      width: 120ch;
      max-width: 120ch !important;
      margin-left: auto !important;
      margin-right: auto !important;
      box-sizing: border-box !important;
    }
    
    #reasoning-md {
        max-height: 300px;
        overflow-y: auto;
    }
    """

    reasoning_view = gr.Markdown('', elem_id='reasoning-md')
    usage_view = gr.Markdown('')

    with gr.Blocks(css=css, theme=gr.themes.Monochrome()) as demo:
        agent = gr.State()

        async def get_response(message, chat_view_history, agent):
            output = ""
            reasoning = ""

            async for text_type, text in agent.get_response(message):
                if text_type == 'reasoning':
                    reasoning += text
                elif text_type == 'output':
                    output += text
                else:
                    raise NotImplementedError(text_type)

                yield output, reasoning, agent.usage_markdown, agent

            yield output, reasoning, agent.usage_markdown, agent

        with gr.Row():
            with gr.Column(scale=5):
                bot = gr.Chatbot(
                    label=' ',
                    height=600,
                    resizable=True,
                )
                chat = gr.ChatInterface(
                    chatbot=bot,
                    fn=get_response,
                    additional_inputs=[agent],
                    additional_outputs=[reasoning_view, usage_view, agent]
                )

            with gr.Column(scale=1):
                reasoning_view.render()
                usage_view.render()

        demo.load(fn=lambda: ChatAgent(**agent_args), outputs=[agent])

    demo.launch()


def main(prompt_path: Path, model: str, show_reasoning, reasoning_effort: str | None, use_web: bool):
    agent_args = dict(
        model=model,
        prompt=prompt_path.read_text() if prompt_path else '',
        show_reasoning=show_reasoning,
        reasoning_effort=reasoning_effort

    )

    if use_web:
        _main_gradio(agent_args)
    else:
        asyncio.run(_main_console(agent_args))


# Launch app
if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser('ChatBot')
    parser.add_argument('prompt_file', nargs='?', type=Path, default=None)
    parser.add_argument('--web', action='store_true')
    parser.add_argument('--model', default='gpt-5-nano')
    parser.add_argument('--show-reasoning', action='store_true')
    parser.add_argument('--reasoning-effort', default='low')
    args = parser.parse_args()
    main(args.prompt_file, args.model, args.show_reasoning, args.reasoning_effort, False)
