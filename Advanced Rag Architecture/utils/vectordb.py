import os
import pickle
from langchain_chroma import Chroma
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever

def setup_parent_document_retriever(documents, embedding, persist_directory):
    # The parent document retriever stores the original large chunks (parents)
    # in an InMemoryStore, and the smaller chunks (children) in ChromaDB
    
    # We will use large chunks for the parents
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    # And small chunks for the children to get highly specific vector matches
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

    # Initialize Chroma vector store for child documents
    vectorstore = Chroma(
        collection_name="split_parents",
        embedding_function=embedding,
        persist_directory=persist_directory
    )

    # Initialize in-memory store for parent documents
    store = InMemoryStore()

    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )

    # Ingest documents
    retriever.add_documents(documents, ids=None)
    
    return retriever, vectorstore

def setup_bm25_retriever(documents):
    # Initialize BM25 for sparse/keyword search
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = 4
    return bm25_retriever
