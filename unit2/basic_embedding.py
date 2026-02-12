from time import time
from openai import Client
from dotenv import load_dotenv
from usage import print_usage
import matplotlib.pyplot as plt
import numpy as np
import re
import json
import numpy as np
from pathlib import Path
from typing import List, Tuple

from time import time
from openai import Client
from dotenv import load_dotenv
from usage import print_usage
import matplotlib.pyplot as plt
import numpy as np

model = 'text-embedding-3-small'

def embed(content: list[str], model:str) -> np.array:
    response = Client().embeddings.create(
        input=content,
        model=model
    )
    return np.array([emb.embedding for emb in response.data])

def compare_embeddings_plot(phrase:str, phrases):
    phrases.insert(0,phrase)
    data = embed(phrases, model)
    sims = data @ data.T
    index = 0
    ax = plt.bar(x=range(len(phrases)), height=sims[index,:])
    plt.xticks(range(len(phrases)), phrases, rotation=45, ha='right', rotation_mode='anchor')
    plt.title('Embedding similiarity for ' + phrases[index])
    plt.ylim([0, 1])
    plt.show()

def search_phrases(query, phrases: list[str]):
    # Embeddings for all phrases and the query
    phrase_embeddings = embed(phrases, model)
    query_embedding = embed([query], model)  # shape (1, d)

    return search_embeddings(query_embedding, phrases, phrase_embeddings)


def embed_chunked(content: list[str], model: str, batch_size: int = 100) -> np.array:
    """
    Generate embeddings for a list of strings, processing in batches to avoid token limits.
    
    Args:
        content: List of strings to embed
        model: OpenAI embedding model name
        batch_size: Number of strings to process per API call (default 100)
    
    Returns:
        Numpy array of embeddings
    """
    client = Client()
    all_embeddings = []
    
    # Process in batches
    for i in range(0, len(content), batch_size):
        batch = content[i:i + batch_size]
        response = client.embeddings.create(
            input=batch,
            model=model
        )
        batch_embeddings = [emb.embedding for emb in response.data]
        all_embeddings.extend(batch_embeddings)
        
        # Optional: print progress for large datasets
        if len(content) > batch_size:
            print(f"Processed {min(i + batch_size, len(content))}/{len(content)} items")
    
    return np.array(all_embeddings)


def search_embeddings(query_embedding, phrases: list[str], phrase_embeddings):
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
    

def chunk_text(file_path: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Read a text file and chunk it into appropriately sized pieces.
    
    Args:
        file_path: Path to the text file
        chunk_size: Target size of each chunk in characters
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Clean up excessive whitespace while preserving paragraph breaks
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If this isn't the last chunk, try to break at a sentence or paragraph
        if end < len(text):
            # Look for paragraph break first
            paragraph_break = text.rfind('\n\n', start, end)
            if paragraph_break > start + chunk_size // 2:
                end = paragraph_break + 2
            else:
                # Look for sentence ending
                sentence_end = max(
                    text.rfind('. ', start, end),
                    text.rfind('! ', start, end),
                    text.rfind('? ', start, end)
                )
                if sentence_end > start + chunk_size // 2:
                    end = sentence_end + 2
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = end - overlap if end < len(text) else end
    
    return chunks

def save_embeddings(chunks: List[str], embeddings: np.ndarray, output_path: str) -> None:
    """
    Save text chunks and their embeddings to a file.
    
    Args:
        chunks: List of text chunks
        embeddings: Numpy array of embeddings (shape: n_chunks x embedding_dim)
        output_path: Path where the file should be saved
    """
    data = {
        'chunks': chunks,
        'embeddings': embeddings.tolist()
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def search_from_file(query: str, embeddings_file: str, search_embeddings_func) -> List[str]:
    """
    Load chunks and embeddings from file and search using existing search function.
    
    Args:
        query: Search query string
        embeddings_file: Path to the file containing chunks and embeddings
        search_embeddings_func: The existing search_embeddings function
    
    Returns:
        List of top matching chunks
    """
    with open(embeddings_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = data['chunks']
    embeddings = np.array(data['embeddings'])  # Not needed for search_embeddings
    return search_embeddings_func(embed(query, model), chunks, embeddings)


# Example usage workflow
if __name__ == '__main__':
    from openai import Client
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("starting embeddings process")
    # Step 1: Chunk the text
    chunks = chunk_text('././books/King_James_Bible.txt', chunk_size=500, overlap=200)
    print(f"Created {len(chunks)} chunks")
    
    # Step 2: Generate embeddings
    from time import time
    start = time()
    embeddings = embed_chunked(chunks, 'text-embedding-3-small', 100)
    print(f"Generated embeddings in {time() - start:.2f}s")
    
    # Step 3: Save to file
    save_embeddings(chunks, embeddings, './unit2/Embeddings/king_james_bible_embeddings.json')
    print("Saved embeddings to file")
    
    # Step 4: Search from file
    query = "The Lord has more to tell us, but He waits for our faith/receptivity to grow first."
    results = search_from_file(query, './unit2/Embeddings/king_james_bible_embeddings.json', search_embeddings)
    
    print(f"\nTop results for query: '{query}'")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result}...")

        

# if __name__ == '__main__':
#     load_dotenv()

#     # initial testing used the following
#     # phrases = ['hi', 'como estas?', 'howdy', 'wenas', 'boo', 'buenas', 'holis', 'chow', 'bark','I would like a grilled cheese sandwhich']
#     # phrase = "hola"


#     # print(search_embeddings(phrase, phrases))
