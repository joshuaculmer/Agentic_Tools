I have written an application for computing embeddings and comparing them to queries. I would now also like a library or algorithm that will help me chunk text. I have the count of monte cristo in a .txt file and I would like to be able to run a query against it. 

I want three functions. The first will read the text file and chunk it into appropriate sizes, returning a list of strings from the text file. I want another function to take a list of strings, their embeddings, and a file path/name as parameters, and then output the pairing of strings and embeddings to a file. The third will be able to read in the strings and embeddings from a file formatted like the output from the second function and then call the preexisting search embeddings function.

I have attatched my existing file for your reference. Instead of asking questions make an assumption and output code. I will be doing this as single shot, so there won't be a chance to ask clarifying questions.
-----------------------------
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

def search_embeddings(query, phrases: list[str]):
    model = 'text-embedding-3-small'
    # Embeddings for all phrases and the query
    phrase_embeddings = embed(phrases, model)
    query_embedding = embed([query], model)  # shape (1, d)

    # Normalize to compute cosine similarity
    def normalize(mat):
        norms = np.linalg.norm(mat, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return mat / norms

    phrase_norm = normalize(phrase_embeddings)          # (n, d)
    query_norm = normalize(query_embedding)             # (1, d)

    # Similarities: (n, 1)
    sims = phrase_norm @ query_norm.T
    sims = sims.flatten()

    # Order by descending similarity
    order = np.argsort(-sims)

    # Return top 10, or all if fewer
    top_n = min(10, len(phrases))
    ordered_phrases = [phrases[i] for i in order[:top_n]]

    return ordered_phrases


if __name__ == '__main__':
    load_dotenv()

    # initial testing used the following
    # phrases = ['hi', 'como estas?', 'howdy', 'wenas', 'boo', 'buenas', 'holis', 'chow', 'bark','I would like a grilled cheese sandwhich']
    # phrase = "hola"


    # print(search_embeddings(phrase, phrases))
