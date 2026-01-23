from time import time

from openai import Client

from usage import print_usage

from dotenv import load_dotenv


def main(system_prompt):
    client = Client()
    model = "gpt-5-nano"
    history = [{'role':'system', 'content':system_prompt}]
    usages = []
    try:
        while True:
            message = input('User: ')
            history.append({'role': 'user', 'content': message})
            start = time()
            response = client.responses.create(
                model=model,
                input=history,
                reasoning={'effort': 'low'}
            )
            history.append({'role': 'assistant', 'content': response.output_text})
            usages.append(response.usage)
            print(f'Took {round(time() - start, 2)} seconds')
            print('Agent:', response.output_text)
    except KeyboardInterrupt:
        pass

    print_usage(model, usages)


if __name__ == '__main__':
    load_dotenv()
    file_path = "unit1/persona/roles/therapistv1.md"
    with open(file_path, 'r') as f:
        system_prompt = f.read()
        f.close()
    main(system_prompt)
# "I want to better understand my emotions and don't know where to start. I don't always know how to express how I feel and when I feel down I sometimes struggle to recognize it. What resources would you reccomend for me?"
# "I will teach you about learning strategies, memory strategies, life planning strategies, whatever is most useful for living a fulfilled life"