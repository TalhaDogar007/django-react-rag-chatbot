from django.shortcuts import render
from django.http import JsonResponse
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from .models import PDF
from .serializers import PDFSerializer
from .utils import load_and_split_pdf, index_documents
from .chroma_client import get_chroma_client  # Import the singleton getter

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma


# Load once at start
EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


LLM = LlamaCpp(
    model_path=os.environ.get("LLM_MODEL_PATH", "/models/mistral-7b-instruct-v0.1.Q2_K.gguf"),
    n_ctx=int(os.environ.get("LLM_N_CTX", 2048)),
    n_batch=int(os.environ.get("LLM_N_BATCH", 512)),
    n_threads=int(os.environ.get("LLM_N_THREADS", 8)),
    temperature=float(os.environ.get("LLM_TEMPERATURE", 0.7)),
    verbose=True, 
)

client = get_chroma_client()
VECTORSTORE = Chroma(
    client=client,
    collection_name="pdf_texts",
    embedding_function=EMBEDDINGS,
)

RETRIEVER = VECTORSTORE.as_retriever(search_type="similarity", search_kwargs={"k": 5})

QA_CHAIN = RetrievalQA.from_chain_type(llm=LLM, retriever=RETRIEVER)


def test_view(request):
    return JsonResponse({"message": "Backend is working!"})

class PDFUploadView(APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, *args, **kwargs):
        file = request.data.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        pdf = PDF.objects.create(file=file)
        pdf_path = pdf.file.path


        return Response({"message": "File uploaded and indexed successfully"}, status=status.HTTP_201_CREATED)

class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        if not query:
            return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = QA_CHAIN.run(query)
            return Response({"response": response})
        except Exception as e:
            print("Error during search:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
