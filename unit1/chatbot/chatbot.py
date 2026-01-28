# Before running this script:
# pip install gradio openai python-dotenv pyyaml

import argparse
import asyncio
from pathlib import Path

import gradio as gr
import yaml
from openai import AsyncOpenAI
from dotenv import load_dotenv
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from usage import print_usage, format_usage_markdown


class ChatAgent:
    def __init__(self, model: str, prompt: str):
        self._ai = AsyncOpenAI()
        self.usage = []
        self.model = model
        self.reasoning = {'effort': 'low'}
        self._prompt = prompt
        self._history = []
        if prompt:
            self._history.append({'role': 'system', 'content': prompt})

    async def get_response(self, user_message: str):
        self._history.append({'role': 'user', 'content': user_message})

        response = await self._ai.responses.create(
            input=self._history,
            model=self.model,
            # reasoning=self.reasoning
        )
        self.usage.append(response.usage)
        self._history.extend(response.output)
        return response.output_text

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print_usage(self.model, self.usage)


async def _main_console(agent):
    print("Console mode - type your messages (empty line to quit)")
    while True:
        message = input('User: ')
        if not message:
            break
        response = await agent.get_response(message)
        print('Agent:', response)



def _main_gradio(agent):
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
    """

    usage_view = gr.Markdown(format_usage_markdown(agent.model, []))

    with gr.Blocks() as demo:
        async def get_response(message, chat_view_history):
            response = await agent.get_response(message)
            usage_content = format_usage_markdown(agent.model, agent.usage)
            return response, usage_content

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
                    additional_outputs=[usage_view]
                )

            with gr.Column(scale=1):
                usage_view.render()

    demo.launch(css=css, theme=gr.themes.Monochrome(), share=True)


def main(prompt_path: Path, model: str, use_web: bool):
    with ChatAgent(model, prompt_path.read_text() if prompt_path else '') as agent:
        if use_web:
            _main_gradio(agent)
        else:
            asyncio.run(_main_console(agent))
            
def load_config(config_path: Path) -> dict:
    """Load configuration from YAML file"""
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def create_default_config(config_path: Path):
    """Create a default config.yaml file"""
    default_config = {
        'model': 'gpt-5-nano',
        'prompt_file': 'unit1/prompts/secret_system_prompt.md',
        'use_web': True,
        'reasoning_effort': 'low'
    }
    with open(config_path, 'w') as f:
        yaml.dump(default_config, f, default_flow_style=False)
    print(f"Created default config at {config_path}")
    return default_config


def main():
    load_dotenv()
    
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='ChatBot with Gradio UI',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('config.yaml'),
        help='Path to config file'
    )
    parser.add_argument('--prompt_file', type=Path, help='Path to prompt file')
    parser.add_argument('--model', help='Model to use')
    parser.add_argument('--console', action='store_true', help='Use console mode instead of web')
    parser.add_argument('--create-config', action='store_true', help='Create default config file')
    
    args = parser.parse_args()
    
    # Create default config if requested
    if args.create_config:
        create_default_config(args.config)
        return
    
    # Load config file
    config = load_config(args.config)
    
    # Command line args override config file
    prompt_file = args.prompt_file or Path(config.get('prompt_file', 'unit1/prompts/secret_system_prompt.md'))
    model = args.model or config.get('model', 'gpt-4.1-nano')
    use_web = args.console if args.console else config.get('use_web', True)
    
    # Load prompt
    prompt = ""
    if prompt_file.exists():
        prompt = prompt_file.read_text()
    else:
        print(f"Warning: Prompt file not found at {prompt_file}")
    
    # Run chatbot
    with ChatAgent(model, prompt) as agent:
        agent.reasoning['effort'] = config.get('reasoning_effort', 'low')
        
        if use_web:
            print(f"Starting web interface with model: {model}")
            _main_gradio(agent)
        else:
            print(f"Starting console mode with model: {model}")
            asyncio.run(_main_console(agent))


if __name__ == "__main__":
    main()