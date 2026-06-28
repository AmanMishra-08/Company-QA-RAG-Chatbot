
import inspect
import faiss
import pickle
import os

# Handle wrong word 
from textblob import TextBlob, Word

def correct_query(query):
    # Manual corrections for common mistakes
    manual_corrections = {
        "foundr": "founder",
        "foundre": "founder",
        "waht": "what",
        "compnay": "company",
        "servces": "services"
    }
    
    ignore_words = ["cyfuture", "anuj", "bairathi", "faiss", "groq"]
    
    words = query.split()
    corrected_words = []
    
    for word in words:
        if word.lower() in ignore_words:
            corrected_words.append(word)
        elif word.lower() in manual_corrections:
            corrected_words.append(manual_corrections[word.lower()])
        else:
            corrected_words.append(str(Word(word).correct()))
    
    corrected = " ".join(corrected_words)
    print(f"Original: {query}")
    print(f"Corrected: {corrected}")
    return corrected

#add follow up suggestions 
def get_followup_suggestions(query):
    suggestions = {
        "founder": [
            "When was Cyfuture founded?",
            "Where is Cyfuture headquartered?",
            "What is the CEO's vision?"
        ],
        "services": [
            "What is Cyfuture's cloud service?",
            "Does Cyfuture provide BPO services?",
            "What industries does Cyfuture serve?"
        ],
        "contact": [
            "Where is Cyfuture located?",
            "What is Cyfuture's email?",
            "What is Cyfuture's phone number?"
        ],
        "default": [
            "Who is the founder of Cyfuture?",
            "What services does Cyfuture provide?",
            "Where is Cyfuture located?"
        ]
    }
    
    query_lower = query.lower()
    
    if "founder" in query_lower or "ceo" in query_lower:
        return suggestions["founder"]
    elif "service" in query_lower or "provide" in query_lower:
        return suggestions["services"]
    elif "contact" in query_lower or "phone" in query_lower:
        return suggestions["contact"]
    else:
        return suggestions["default"]


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

    
    # Handle greetings
    greetings = ["hi", "hii", "hello", "hey"]
    thanks = ["thanks", "thankyou", "thank you", "ty"]
    bye_words = ["bye", "goodbye", "see you"]

    if query.strip().lower() in greetings:
     return "Hello! How can I help you with Cyfuture today?", "", []

    if query.strip().lower() in thanks:
     return "You're welcome! Feel free to ask more questions about Cyfuture.", "", []

    if query.strip().lower() in bye_words:
     return "Goodbye! Have a great day! 😊", "", []

# HAndle wrong word (Correct spelling first)
    query = correct_query(query)

    # Handle short inputs
    if len(query.strip()) < 3:
        return "Please ask a proper question about Cyfuture.", "", []

    # rest of your code...
    context = retrieve_context(query)
   

    prompt = f"""
You are a professional assistant for Cyfuture company.

Rules:
- Answer directly without any commentary
- Never say things like "Not a question requiring" or "Good question"
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
  
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
   
    answer = response.choices[0].message.content

    suggestions = get_followup_suggestions(query)
    return answer, context, suggestions

