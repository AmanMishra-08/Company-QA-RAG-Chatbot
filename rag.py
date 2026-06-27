
import inspect
import faiss
import pickle
import os

from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# Load .env Groq KEY
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# cache extra work
from functools import lru_cache
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Load FAISS
index = faiss.read_index(
    "faiss_index.bin"
)
print("FAISS vectors:", index.ntotal)

# Load Chunks
with open(
    "chunks.pkl",
    "rb"
) as f:

    chunks = pickle.load(f)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# retrieve_context()

def retrieve_context(query, k=3):
    print("--- TIMING START ---")
    try:
        query_embedding = embedding_model.encode(
            [query],
            convert_to_numpy=True
        )

        distances, indices = index.search(query_embedding, k)


        context = ""

        for idx in indices[0]:
            chunk = chunks[idx]

            # Handle both dict chunks and plain string chunks
            if isinstance(chunk, dict):
                text = chunk.get("text", str(chunk))
            else:
                text = str(chunk)

            context += text
            context += "\n\n"

        return context

    except Exception as e:
        print("ERROR OCCURRED:")
        print(type(e))
        print(e)
        raise

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


# ask_rag()

def ask_rag(query):
    t3 = time.time() # extra
    # Retrieve context
    context = retrieve_context(query)
    print(f"Retrieval total: {time.time()-t3:.2f}s") #extra

    prompt = f"""
You are a professional assistant for Cyfuture company.

Rules:
- Answer in a friendly and professional tone
- Keep answers short and clear
- Use bullet points where needed
- If answer not in context say "I don't have information about that"

Context:
{context}

Question: {query}

If answer is not in context, say "Not found in document".

Answer:
"""
    t4 = time.time() # extra
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print(f"Groq API time: {time.time()-t4:.2f}s")  # extra
    answer = response.choices[0].message.content

    return answer, context

