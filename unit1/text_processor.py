import argparse
import sys
import yaml
from pathlib import Path
from time import time
from openai import OpenAI
from usage import print_usage
from dotenv import load_dotenv


def main(model: str, prompt: str, sports_texts: dict):
    client = OpenAI()
    print(f"\nPROMPT: {prompt}")
    usages = []
    start = time()

    for url, text in sports_texts.items():
        print(f"\n{'-' * 60}\n{url}\n\n{text}\nRESPONSE: ")
        model_input = f"{prompt}\n{text}"
        response = client.responses.create(
            model=model,
            input=model_input,
            reasoning={'effort': 'low'}
        )
        print(response.output_text)
        usages.append(response.usage)

    print(f'\n\n{round(time()-start, 2)} seconds elapsed', file=sys.stdout)
    print_usage(model, usages, file=sys.stdout)


# Launch app
if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser('AI Response')
    # parser.add_argument('prompt_file', type=Path)
    parser.add_argument('--model', default='gpt-5-nano')
    args = parser.parse_args()
    with open('unit1\sports-articles.yaml', "r") as f:
        sports_data = yaml.safe_load(f)

    main("gpt-5-nano", "Determine the winner of the match and output who you think was happiest about the win", sports_data)
