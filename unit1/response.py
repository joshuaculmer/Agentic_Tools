import argparse
import sys
from pathlib import Path
from time import time

from openai import OpenAI

from usage import print_usage
from dotenv import load_dotenv


def main(model: str, prompt: str, structure:str, example:str):
    client = OpenAI()
    start = time()
    response = client.responses.create(
        model=model,
        input=prompt + structure + example,
        reasoning={'effort': 'low'}
    )
    print(response.output_text)

    print(f'{round(time()-start, 2)} seconds elapsed', file=sys.stderr)
    print_usage(model, response.usage)


# Launch app
if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser('AI Response')
    parser.add_argument('--prompt_file', type=Path)
    parser.add_argument('--model', default='gpt-5-nano')
    args = parser.parse_args()

    if  args.prompt_file:
        prompt =  args.prompt_file.read_text()
    else:
        file_path = "unit1/prompts/secret_phrase.md"
        with open(file_path, 'r') as f:
            prompt = f.read()
            f.close()


        file_path = "unit1/json_structure.md" 
        with open(file_path, 'r') as f:
            structure = f.read()
            f.close()

        file_path = "unit1/json_example.md" 
        with open(file_path, 'r') as f:
            example = f.read()
            f.close()
    main(args.model, prompt, structure, example)
