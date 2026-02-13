from time import time

from openai import Client
from dotenv import load_dotenv
from usage import print_usage


def single_query(input:str, system_prompt:str=None, RAG:str=None, reasoning:str="low", model="gpt-5-nano", history=[]):
    client = Client()
    history = history
    if system_prompt:
        history.append({'role': 'system', 'content': system_prompt + RAG})
    history.append({'role':'user', 'content':input})
    print(system_prompt + RAG)
    start = time()
    response = client.responses.create(
        model=model,
        input=history,
    reasoning={'effort': reasoning})
    print(f'Took {round(time() - start, 2)} seconds')
    print_usage(model, response.usage)
    print(response.output_text)


#TODO Flesh out other methods that could be called...potentially abstract into
# a class depending on articecture needs, not currently needed