from time import time

from openai import Client
from dotenv import load_dotenv
from usage import print_usage


def main(input:str):
    client = Client()
    start = time()
    model = "gpt-5-nano"
    response = client.responses.create(
        model=model,
        input = input,
    reasoning={'effort': 'medium'})
    print(f'Took {round(time() - start, 2)} seconds')
    print_usage(model, response.usage)
    print(response.output_text)


if __name__ == '__main__':
    load_dotenv()


    # from file
    # with open("unit1/prompts/Philosophy/Divine_Attributes_in_Humanity.md", 'r') as f:
    #     input = f.read()
    #     f.close()

    # from direct input
    input= 'hi'

    # from multiple prompts
    input = ['howdy', 'wenas', 'boo', 'bark','I would like a grilled cheese sandwhich']
    main(input)
