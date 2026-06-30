
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
        "servces": "services",
        "cifuture": "cyfuture",
        "cyfture": "cyfuture",
        "cyffuture": "cyfuture",
        "locat": "location",
        "locatd": "located",
        "offce": "office",
        "servc": "service",
        "employe": "employee",
        "employes": "employees",
        "prodcut": "product",
        "prodcuts": "products",
        "contct": "contact",
        "addrss": "address",
        "phon": "phone",
        "numbr": "number",
        "websit": "website",
        "ceo": "ceo",
        "founderr": "founder",
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
def get_followup_suggestions(query, answer):
    query_lower = query.lower()
    answer_lower = answer.lower()
    
    all_suggestions = {
        "founder": [
            "When was Cyfuture founded?",
            "Where is Cyfuture headquartered?",
            "What is the CEO's vision?"
        ],
        "services": [
            "What cloud services does Cyfuture offer?",
            "Does Cyfuture provide BPO services?",
            "What industries does Cyfuture serve?"
        ],
        "location": [
            "How many offices does Cyfuture have?",
            "Where is Cyfuture headquartered?",
            "Does Cyfuture have international offices?"
        ],
        "contact": [
            "What is Cyfuture's email address?",
            "What is Cyfuture's phone number?",
            "Where is Cyfuture's main office?"
        ],
        "cloud": [
            "What is Cyfuture's cloud pricing?",
            "Does Cyfuture offer GPU cloud?",
            "What is Cyfuture's uptime guarantee?"
        ],
        "employee": [
            "How many employees does Cyfuture have?",
            "How to apply for a job at Cyfuture?",
            "What is Cyfuture's work culture?"
        ],
        "default": [
            "Who is the founder of Cyfuture?",
            "What services does Cyfuture provide?",
            "Where is Cyfuture located?"
        ]
    }
    
    if "founder" in query_lower or "ceo" in query_lower:
        return all_suggestions["founder"]
    elif "service" in query_lower or "provide" in query_lower:
        return all_suggestions["services"]
    elif "locat" in query_lower or "office" in query_lower or "where" in query_lower:
        return all_suggestions["location"]
    elif "contact" in query_lower or "phone" in query_lower or "email" in query_lower:
        return all_suggestions["contact"]
    elif "cloud" in query_lower or "gpu" in query_lower or "server" in query_lower:
        return all_suggestions["cloud"]
    elif "employee" in query_lower or "staff" in query_lower or "team" in query_lower:
        return all_suggestions["employee"]
    else:
        return all_suggestions["default"]


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
- Answer directly without unnecessary commentary.
- Answer ONLY using the provided context.
- Never use your own knowledge or assumptions.
- Summarize and rephrase descriptive information in your own words.
- Do NOT summarize, modify, or invent factual information such as names, addresses, phone numbers, email addresses, URLs, dates, or identification numbers.
- Preserve factual information exactly as it appears in the context.
- If any part of the answer is not present in the context, do not include it.
- Use a friendly, professional, and concise tone.
- Never say phrases like "Good question", "According to the context", or "Not a question requiring...".
- If the context does not contain enough information to answer the question, reply exactly:
  "I don't have information about that."

Formatting:
- Use short paragraphs for readability.
- Use headings when they improve clarity.
- Use bullet points for lists, services, features, benefits, or multiple items.
- For addresses, display each address component on a separate line without changing any details.
- For contact information, display each item on a separate line.
- For definitions ("What is X?"), provide a clear definition followed by a brief explanation if needed.
- For "How" questions, explain the process in simple numbered steps.
- For yes/no questions, answer first, then briefly explain why.
- Keep simple factual answers (name, date, location, etc.) within 1–2 lines unless more detail is requested.


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

    suggestions = get_followup_suggestions(query,answer)
    return answer, context, suggestions

