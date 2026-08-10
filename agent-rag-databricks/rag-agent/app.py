import streamlit as st
from main import get_rag_chain
import mlflow
import os

st.set_page_config(page_title="🤖 Databricks Financial RAG Bot", layout="centered")
st.title("💰 Databricks Financial RAG Bot")


# Usamos st.cache_resource para inicializar a chain UMA ÚNICA VEZ
# Isso evita que o Databricks Vector Search e LLM sejam inicializados a cada interação
@st.cache_resource
def initialize_chain():
    """Chama a função para obter e armazenar a chain LangChain."""
    return get_rag_chain()


# Inicializa a chain
chain = initialize_chain()

# 1. Inicializar o Histórico de Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Eu sou o analista financeiro. Pergunte sobre vendas, produtos ou clientes.",
        }
    ]

# 2. Exibir o Histórico de Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3. Capturar a Entrada do Usuário
if prompt := st.chat_input("Insira sua pergunta de análise financeira..."):
    # Adicionar a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Exibir a mensagem do usuário
    with st.chat_message("user"):
        st.write(prompt)

    # 4. Processar a Pergunta com o Agente RAG
    with st.chat_message("assistant"):
        with st.spinner("Buscando e analisando dados..."):
            # O MLflow Run deve ser iniciado AQUI para rastrear a invocação específica
            with mlflow.start_run(run_name="chat_workshop") as run:
                # Invocação da chain
                response = chain.invoke({"messages": prompt})
                st.write(response)

                # Logs do MLflow
                mlflow.log_param("user_query", prompt)
                mlflow.log_param("run_id", run.info.run_id)

    # 5. Adicionar a Resposta do Assistente ao Histórico
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configurações do Agente")
    st.write(f"**Endpoint do LLM:** `{os.getenv('LLM_ENDPOINT')}`")
    st.write(f"**Endpoint do Vector Search:** `{os.getenv('VS_ENDPOINT')}`")
    st.write(f"**Índice:** `{os.getenv('INDEX_NAME')}`")
    st.markdown("---")
    st.caption(
        "A Chain RAG é inicializada uma única vez usando `@st.cache_resource` para performance."
    )