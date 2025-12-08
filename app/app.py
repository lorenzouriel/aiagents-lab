import streamlit as st

from app.graph.rag_graph import run_streaming_rag

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Forensic RAG Assistant",
    layout="wide",
)

st.title("🧬 Forensic Doctor Assistant (RAG + Self-Query)")
st.write(
    "Ask questions in natural language about forensic cases. "
    "The system will automatically generate filters and perform semantic retrieval over the case documents."
)

# -------------------------------
# Chat History Management
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# User Input
# -------------------------------
if prompt := st.chat_input(
    "Example: What was the cause of death in Case 002?"
):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # -------------------------------
    # Assistant Streaming Response
    # -------------------------------
    with st.chat_message("assistant"):

        # Real-time UI placeholders
        details_expander = st.expander("🔎 **Search Details (Self-Query)**", expanded=False)
        query_placeholder = details_expander.empty()
        filter_placeholder = details_expander.empty()

        answer_placeholder = st.empty()
        full_answer = ""

        # -------------------------------
        # Backend Streaming Call
        # -------------------------------
        for event in run_streaming_rag(prompt):

            # --- Display generated query & filters
            if event["type"] == "details":
                data = event["data"]

                query_placeholder.markdown(
                    f"**Semantic Query:** `{data['query']}`"
                )

                filter_placeholder.markdown(
                    f"**Metadata Filter:** `{data['filter']}`"
                )

            # --- Display streaming tokens
            elif event["type"] == "token":
                token = event["data"]
                full_answer += token
                answer_placeholder.markdown(full_answer + "▌")  # Typing cursor effect

            # --- Display sources at the end
            elif event["type"] == "sources":
                answer_placeholder.markdown(full_answer)

                sources = event["data"]
                if sources:
                    with st.expander("📚 **Sources Used**"):
                        for source in sources:
                            st.markdown(
                                f"""
                                - **File:** `{source.get('pdf_name')}`
                                - **Case ID:** `{source.get('num_sumula')}`
                                - **Chunk Type:** `{source.get('chunk_type')}`
                                - **Status:** `{source.get('status_atual')}`
                                - **Document Date:** `{source.get('data_status')}`
                                """
                            )

    # -------------------------------
    # Store final assistant message
    # -------------------------------
    st.session_state.messages.append(
        {"role": "assistant", "content": full_answer}
    )