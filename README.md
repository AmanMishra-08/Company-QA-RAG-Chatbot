#Company Policy Assistant (RAG Chatbot)
A Retrieval-Augmented Generation (RAG) chatbot that answers questions from company policy documents using FAISS, Sentence Transformers, Groq Llama 3.1, and Streamlit.

## Live Demo
[Click here to use the chatbot](https://company-app-rag-chatbot-hcy82yntbf846tdqjly95y.streamlit.app/)

## Features
- Intelligent text chunking and semantic search
- Spell correction for user queries
- Greeting and farewell handler
- Follow-up question suggestions
- Cyfuture logo and professional UI
- Chat-style Streamlit interface
- Displays retrieved document context
- Clear chat button
- Deployed on Streamlit Cloud

##  Tech Stack

| Component | Technology |
|---|---|
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| LLM | Groq - LLaMA 3.1 8B Instant |
| Frontend | Streamlit |
| Spell Correction | TextBlob |
| Language | Python |

## Project Structure

LLM_RAG/

│

├── app.py              # Streamlit UI

├── rag.py              # RAG pipeline

├── faiss_index.bin     # FAISS vector database

├── chunks.pkl          # Stored document chunks

├── logo.png            # Cyfuture logo

├── .env                # Groq API Key (not uploaded)

├── requirements.txt    # Dependencies

└── README.md

## RAG Workflow

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





