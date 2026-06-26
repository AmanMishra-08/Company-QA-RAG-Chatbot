import streamlit as st
from rag import ask_rag
import importlib
import rag
importlib.reload(rag)
from rag import ask_rag

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Cyfuture ChatBox",
    page_icon="https://www.trustpilot.com/review/cyfuture.ai",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Cyfuture ChatBox")

st.sidebar.markdown("---")

st.sidebar.write("### Model")
st.sidebar.success("all-MiniLM-L6-v2")

st.sidebar.write("### Vector Database")
st.sidebar.success("FAISS")

st.sidebar.write("### LLM")
st.sidebar.success("Groq - Llama 3.1")

st.sidebar.markdown("---")
st.sidebar.write("Ask questions related to comapany.")
st.sidebar.markdown("---")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -----------------------------
# Main Page
# -----------------------------
st.title("Cyfuture ChatBox")

st.write("Ask question related to the company.")

st.markdown("---")

# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# User Input
# -----------------------------
question = st.chat_input("Ask your question...")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching ..."):

            result = ask_rag(question)

            print("=" * 50)
            print("RESULT TYPE:", type(result))
            print("RESULT:", result)
            print("=" * 50)

            answer, context = result

        st.markdown(answer)

        with st.expander(" Retrieved Context"):
            st.write(context)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )