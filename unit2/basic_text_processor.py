import argparse
import sys
from dotenv import load_dotenv
import yaml
from pathlib import Path
from time import time
from openai import OpenAI
from usage import print_usage

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
    model = "gpt-5-nano"
    load_dotenv()

    with open("unit1/sports-articles.yaml", "r") as f:
        sports_data = yaml.safe_load(f)

    with open("unit1/game-classification-instructions.md", 'r') as f:
        prompt = f.read()
        f.close()

    main(model, prompt, sports_data)
