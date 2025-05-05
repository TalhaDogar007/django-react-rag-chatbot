from typing import List
from .chroma_client import get_chroma_client
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

def load_and_split_pdf(pdf_path: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List:
    """
    Loads a PDF and splits it into document chunks using LangChain's PyPDFLoader.
    Args:
        pdf_path (str): Path to the PDF file.
        chunk_size (int): Size of each chunk.
        chunk_overlap (int): Overlap between chunks.
    Returns:
        List[Document]: List of LangChain Document objects.
    """
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = splitter.split_documents(pages)
    return docs

def index_documents(document_id: str, docs: List) -> int:
    """
    Indexes document chunks into ChromaDB.
    Args:
        document_id (str): Unique document identifier.
        docs (List[Document]): List of LangChain Document objects.
    Returns:
        int: Number of chunks indexed.
    """
    client = get_chroma_client()
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Ensure collection exists
    try:
        collection = client.get_collection("pdf_texts")
    except Exception:
        collection = client.create_collection("pdf_texts", embedding_function=embedding_function)

    # Prepare data for ChromaDB
    chunks = [doc.page_content for doc in docs]
    ids = [f"{document_id}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": document_id, **(doc.metadata or {})} for doc in docs]

    # Add to collection
    if chunks:
        collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids,
        )