from time import time

from openai import Client
from dotenv import load_dotenv
from usage import print_usage


def main(input:str):
    client = Client()
    start = time()
    # model = "gpt-5-nano"
    model = "gpt-5-nano"
    response = client.responses.create(
        model=model,
        input = input,
    reasoning={'effort': 'low'})
    print(f'Took {round(time() - start, 2)} seconds')
    print_usage(model, response.usage)
    print(response.output_text)


if __name__ == '__main__':
    load_dotenv()
    # input = """What is the 1000th number in the fibanacci sequence. Assume F0 = 0, F1 = 1. Please return only the number. Instead of returning text or some other type of response, only respond with the full 300 digit number.
    # """

    with open("unit1/prompts/sequential_task4.md", 'r') as f:
        input = f.read()
        f.close()

    main(input)
