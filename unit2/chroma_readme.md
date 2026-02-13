# chroma_ingest.py

A command-line tool for indexing local files into a [ChromaDB](https://www.trychroma.com/) vector database and querying them with semantic search, powered by OpenAI embeddings.

---

## Requirements

```bash
pip install chromadb openai langchain-text-splitters python-dotenv fire
```

Create a `.env` file in the same directory with your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

---

## Usage

### Ingest a folder

Scans a folder recursively, splits files into chunks, and stores them in ChromaDB.

```bash
python chroma_ingest.py ingest \
  --persist_dir=./mydb \
  --chroma_collection_name=myproject \
  --folder=./my_project
```

| Option | Default | Description |
|---|---|---|
| `--persist_dir` | *(required)* | Path to the local ChromaDB storage directory |
| `--chroma_collection_name` | *(required)* | Name of the collection to ingest into |
| `--folder` | *(required)* | Path to the folder you want to index |
| `--openai_model` | `text-embedding-3-small` | OpenAI embedding model to use |
| `--chunk_size` | `1200` | Max characters per chunk |
| `--chunk_overlap` | `150` | Overlap between consecutive chunks |
| `--batch_size` | `256` | Number of chunks written per batch |

---

### Query the database

Searches the indexed files and returns the most relevant documents for your query.

```bash
python chroma_ingest.py query \
  --chroma_dir=./mydb \
  --collection=myproject \
  --query="how is authentication handled"
```

| Option | Default | Description |
|---|---|---|
| `--chroma_dir` | *(required)* | Path to the ChromaDB storage directory |
| `--collection` | *(required)* | Name of the collection to search |
| `--query` | *(required)* | Natural language search query |
| `--n_results` | `5` | Number of matching documents to return |

The output prints the first 300 characters of each matched document.

---

## Supported File Types

`.txt` `.md` `.rst` `.py` `.js` `.ts` `.java` `.go` `.rs` `.html` `.css` `.json` `.yaml` `.yml` `.toml` `.ini` `.cfg`

---

## How It Works

1. **Ingest** — Files are split into overlapping chunks using a recursive text splitter. Each chunk is embedded via the OpenAI API and stored in ChromaDB with metadata (filename, chunk index, relative path).

2. **Query** — The query is embedded and matched against stored chunks. The tool then reassembles the **full source file** for each match (all chunks in order), so you get complete document context rather than isolated fragments.