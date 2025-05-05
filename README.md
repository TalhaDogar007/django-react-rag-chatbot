# RAG Chatbot System

A Retrieval-Augmented Generation (RAG) system built with Django, React, and LangChain.

## Features

- PDF document upload and processing
- Document indexing using ChromaDB vector store
- Natural language querying using Mistral 7B
- React-based chat interface

## Prerequisites

- Python 3.9+
- Node.js 18+
- Mistral 7B model (GGUF format)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```
   
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   
4. Set environment variables:
   ```
   export LLM_MODEL_PATH=/path/to/your/model.gguf
   export DJANGO_DEBUG=True  # Set to False in production
   export DJANGO_SECRET_KEY=your_secret_key
   ```
   
5. Run migrations:
   ```
   python manage.py migrate
   ```
   
6. Start the server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
   
2. Install dependencies:
   ```
   npm install
   ```
   
3. Create a .env file:
   ```
   VITE_API_URL=http://localhost:8000/api
   ```
   
4. Start the development server:
   ```
   npm run dev
   ```
   
5. Access the application at http://localhost:5173