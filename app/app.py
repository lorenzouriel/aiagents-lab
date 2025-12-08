import streamlit as st
from app.graph.rag_graph import run_streaming_rag

st.set_page_config(
    page_title="Forensic Doctor AI",
)
st.title("AI assistant for Forensic Doctors")
st.write(
    "Welcome to the Forensic Doctor AI assistant. This tool is designed to help forensic doctors with their tasks by providing intelligent assistance based on relevant data and documents."
)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture the question and start the RAG process
if prompt := st.chat_input("Ask your question about forensic medicine..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Start the RAG process and stream the response
    with st.chat_message("assistant"):
        # Placeholder for the assistant's response
        details_expander = st.expander("Search Details")
        query_placeholder = details_expander.empty()
        filter_expander = details_expander.empty()
        answer_placeholder = st.empty()

        full_answer = ""

        # Call the backend function to run the RAG process

