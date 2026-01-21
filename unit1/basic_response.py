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
    input = """# GUI for chatgpt via API

I want a one file executable bash script for setting up a simple typescript boiler plate. 

Start by making a new folder, navigating to that folder and using npm install the necessary typescript dependencies.

At the end of the executable, instead of asking me for input on what next steps to take, include a code to open the new folder in vscode.

I want the folder location relative to the current location to be the following:
-------------------
../GUI
    """
    main(input)
