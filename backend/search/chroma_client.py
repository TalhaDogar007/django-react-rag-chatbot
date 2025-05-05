import os
from functools import lru_cache
from chromadb import Client, Settings

@lru_cache(maxsize=1)
def get_chroma_client():
    """Get a singleton instance of the ChromaDB client."""
    print("Initializing ChromaDB client...")
    persist_dir = os.environ.get("CHROMA_PERSIST_DIR", "./chroma_db")
    settings = Settings(persist_directory=persist_dir)
    return Client(settings)