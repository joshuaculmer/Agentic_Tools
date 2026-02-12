I have this file with a function that is incomplete. Please finish the search embeddings function to return the top 10 closest phrases if there are more than 10 phrases, or all the phrases, in the order that they match the embeddings of the query phrase. 
-----------------------
from time import time
from openai import Client
from dotenv import load_dotenv
from usage import print_usage
import matplotlib.pyplot as plt
import numpy as np

def embed(content: list[str], model:str) -> np.array:
    response = Client().embeddings.create(
        input=content,
        model=model
    )
    return np.array([emb.embedding for emb in response.data])

def compare_embeddings_plot(phrase:str, phrases):
    phrases.insert(0,phrase)
    data = embed(phrases, 'text-embedding-3-small')
    sims = data @ data.T
    index = 0
    ax = plt.bar(x=range(len(phrases)), height=sims[index,:])
    plt.xticks(range(len(phrases)), phrases, rotation=45, ha='right', rotation_mode='anchor')
    plt.title('Embedding similiarity for ' + phrases[index])
    plt.ylim([0, 1])
    plt.show()

def search_embeddings(query, phrases:list[str]):
    embeddings = embed(phrases)
    query = embed(phrase)




if __name__ == '__main__':
    load_dotenv()

    phrases = ['hi', 'como estas?', 'howdy', 'wenas', 'boo', 'buenas', 'holis', 'chow', 'bark','I would like a grilled cheese sandwhich']
    phrase = "hola"
    compare_embeddings_plot(phrase, phrases )
