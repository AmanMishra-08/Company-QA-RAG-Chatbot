#Company Policy Assistant (RAG Chatbot)
A Retrieval-Augmented Generation (RAG) chatbot that answers questions from company policy documents using FAISS, Sentence Transformers, Groq Llama 3.1, and Streamlit.

## Live Demo
[Click here to use the chatbot](https://company-app-rag-chatbot-hcy82yntbf846tdqjly95y.streamlit.app/)

## Features
-  Intelligent text chunking
-  Semantic search using FAISS
-  embedding model
-  Groq Llama 3.1 for answer generation
-  Chat-style Streamlit interface
-  Displays retrieved document context
-  Fast and accurate document question answering

## 🛠 Tech Stack
- Python
- Streamlit
- FAISS
- Sentence Transformers
- BAAI/bge-m3
- Groq API
- Llama 3.1-8B Instant
- LangChain Text Splitters
- PyPDF

## Project Structure

```
LLM_RAG/
│
├── app.py                 # Streamlit UI
├── rag.py                 # RAG pipeline
├── faiss_index.bin        # FAISS vector database
├── chunks.pkl             # Stored document chunks
├── .env                   # Groq API Key
├── requirements.txt
└── README.md
```

## Create FAISS Index

Run your notebook or preprocessing script to:
- Load PDF documents
- Split into chunks
- Generate embeddings
- Create FAISS index
- Save

## 🔄 RAG Workflow

```
User Question
       │
       ▼
Sentence Transformer (BGE-M3)
       │
       ▼
Generate Query Embedding
       │
       ▼
FAISS Similarity Search
       │
       ▼
Retrieve Relevant Chunks
       │
       ▼
Build Prompt
       │
       ▼
Groq Llama 3.1
       │
       ▼
Generated Answer

## 📷 User Interface

Features include:

- Chat interface
- Sidebar model information
- Retrieved context viewer
- Chat history
- Clear chat button





