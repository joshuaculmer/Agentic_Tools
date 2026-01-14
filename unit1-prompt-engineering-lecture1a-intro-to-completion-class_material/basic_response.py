from time import time

from openai import Client
from dotenv import load_dotenv
from usage import print_usage


def main():
    client = Client()
    start = time()
    model = "gpt-5-nano"
    response = client.responses.create(
        model=model,
        input="Hello, what is the average velocity of un unladen swallow?",
        reasoning={'effort': 'low'}
    )
    print(f'Took {round(time() - start, 2)} seconds')
    print_usage(model, response.usage)
    print(response.output_text)


if __name__ == '__main__':
    load_dotenv()
    main()
