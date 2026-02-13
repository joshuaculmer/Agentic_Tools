from dotenv import load_dotenv
from chroma_demo import query_whole_documents
from response2 import single_query

if __name__ == '__main__':
    load_dotenv()

    # Get Prompt from file correctly
    with open("./prompts/Conference_Chatbot_prompt.md", 'r') as f:
        system_prompt = f.read()
        f.close()

    # User makes a Query
    query = input("Ask Conference Chatbot:")

    # Retrieve info from RAG
    rag_results = query_whole_documents('./db', 'mycode', query, 5)

    rag_compiled = ""
    for result in rag_results:
        rag_compiled += result
        rag_compiled += '\n\n\n\n'

    # Pass system prompt, RAG, query into basic request
    single_query(query, system_prompt, rag_compiled)

