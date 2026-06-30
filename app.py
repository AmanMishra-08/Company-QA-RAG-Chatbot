import streamlit as st
from rag import ask_rag

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Cyfuture ChatBox",
    page_icon="images.jpg",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.image("logo.png", width=100)
st.sidebar.title("Cyfuture ChatBox")
st.sidebar.markdown("---")
st.sidebar.write("### Model")
st.sidebar.success("all-MiniLM-L6-v2")
st.sidebar.write("### Vector Database")
st.sidebar.success("FAISS")
st.sidebar.write("### LLM")
st.sidebar.success("Groq - Llama 3.1")
st.sidebar.markdown("---")
st.sidebar.write("Ask questions related to company.")
st.sidebar.markdown("---")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.session_state.suggestions = []
    st.rerun()

# -----------------------------
# Main Page
# -----------------------------
# CSS to center image
st.markdown("""
    <style>
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Main Page

import base64

def get_image_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_image_base64("logo.png")

st.markdown(f"""
    <div style='text-align: center; padding-top: 0px; margin-top: -60px;'>
        <img src='data:image/png;base64,{img_base64}' width='250'>
        <h1 style='margin-top: 5px; margin-bottom: 0px;'>Cyfuture ChatBox</h1>
        <p style='color: gray; margin-top: 0px;'>Your AI Company Assistant</p>
    </div>
""", unsafe_allow_html=True)

# st.markdown("""
#     <hr style='border: 1px solid blue;'>
# """, unsafe_allow_html=True)

# -----------------------------
# Initialize session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

# -----------------------------
# Chat History
# -----------------------------
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="©️"):
            st.markdown(message["content"])
# -----------------------------
# Show suggestions outside chat
# -----------------------------
if st.session_state.suggestions:
    st.markdown("**You might also want to ask:**")
    for i, suggestion in enumerate(st.session_state.suggestions):
        if st.button(suggestion, key=f"sugg_{i}"):
            st.session_state.suggestions = []
            st.session_state["pending_question"] = suggestion
            st.rerun()

# -----------------------------
# User Input
# -----------------------------
question = st.chat_input("Ask your question...")

if "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")

if question:
    st.session_state.suggestions = []
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching ..."):
            result = ask_rag(question)
            answer, context, suggestions = result

        st.markdown(answer)

        with st.expander(" Retrieved Context"):
            st.write(context)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.suggestions = suggestions
    st.rerun()
