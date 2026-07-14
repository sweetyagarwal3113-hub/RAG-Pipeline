import streamlit as st
import os
import sys

# Ensure Python can find the utils folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import CHROMA_PATH, PDF_PATH
from utils.embedding import get_embedding
from utils.vectordb import setup_parent_document_retriever, setup_bm25_retriever
from utils.retriever import create_advanced_retriever
from utils.llm import load_llm
from utils.agent import create_rag_agent
from langchain_community.document_loaders import PyPDFLoader

st.set_page_config(page_title="Advanced Agentic RAG", page_icon="🧠")
st.title("Advanced Agentic RAG Pipeline")
st.markdown("Features: Agentic Routing, Multi-Query Expansion, Hybrid Search, Parent Document Mapping, Cross-Encoder Re-ranking.")

@st.cache_resource
def load_advanced_pipeline():
    # 1. Load Data
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"Missing PDF at {PDF_PATH}. Please add a document to the data folder.")
        
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    # 2. Setup Vector DB & Retrievers
    embedding = get_embedding()
    # In a real app, you wouldn't ingest on every startup, but for this demo we build it in-memory/cache
    parent_retriever, _ = setup_parent_document_retriever(docs, embedding, CHROMA_PATH)
    bm25_retriever = setup_bm25_retriever(docs)

    # 3. Setup LLM & Advanced Retriever
    llm = load_llm()
    advanced_retriever = create_advanced_retriever(llm, parent_retriever, bm25_retriever)

    # 4. Setup Agent
    agent_executor = create_rag_agent(llm, advanced_retriever)
    
    return agent_executor

try:
    agent_executor = load_advanced_pipeline()
except Exception as e:
    st.error(f"Error loading pipeline: {e}")
    st.stop()

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt_input := st.chat_input("Ask a complex question..."):
    st.chat_message("user").markdown(prompt_input)
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    
    with st.spinner("Agent is analyzing, expanding queries, searching, re-ranking, and synthesizing..."):
        # AgentExecutor expects "input" as the key
        response = agent_executor.invoke({"input": prompt_input})
        answer = response["output"]
        
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
