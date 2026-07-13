import streamlit as st
from config import CHROMA_PATH
from utils.embedding import get_embedding
from utils.db_loader import load_vector_db
from utils.retriever import create_retriever
from utils.llm import load_llm
from prompts.rag_prompt import prompt
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import os
from utils.loader import load_documents
from utils.splitter import split_documents
from utils.vectordb import create_vector_db

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("RAG Chatbot")

with st.sidebar:
    st.header("Document Management")
    uploaded_file = st.file_uploader("Upload a new PDF to update the knowledge base", type=["pdf"])
    if uploaded_file is not None:
        if st.button("Process & Update Database"):
            with st.spinner("Processing PDF and updating database..."):
                # Save the uploaded file
                os.makedirs("data", exist_ok=True)
                pdf_path = os.path.join("data", uploaded_file.name)
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Run the ingestion logic
                documents = load_documents(pdf_path)
                chunks = split_documents(documents)
                embedding = get_embedding()
                create_vector_db(chunks, embedding, CHROMA_PATH)
                
                st.success("Database updated successfully!")
                st.cache_resource.clear() # Clear cache so chain is reloaded
                st.rerun()


# Cache the heavy initialization so it doesn't run on every rerun
@st.cache_resource
def load_rag_chain():
    embedding = get_embedding()
    db = load_vector_db(CHROMA_PATH, embedding)
    retriever = create_retriever(db)
    llm = load_llm()
    document_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, document_chain)
    return rag_chain

rag_chain = load_rag_chain()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt_input := st.chat_input("Ask a question about the document..."):
    # Display user message
    st.chat_message("user").markdown(prompt_input)
    # Add to history
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    
    # Get bot response
    with st.spinner("Thinking..."):
        response = rag_chain.invoke({"input": prompt_input})
        answer = response["answer"]
        
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)
    # Add to history
    st.session_state.messages.append({"role": "assistant", "content": answer})
