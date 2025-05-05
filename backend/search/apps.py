from django.apps import AppConfig
from .chroma_client import get_chroma_client

class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'

    def ready(self):
        # Initialize the ChromaDB collection on startup
        client = get_chroma_client()
        try:
            client.get_collection("pdf_texts")
            print("Collection [pdf_texts] already exists.")
        except Exception:
            print("Collection [pdf_texts] does not exist. Creating it...")
            client.create_collection("pdf_texts")
