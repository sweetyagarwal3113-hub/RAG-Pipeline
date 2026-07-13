from config import PDF_PATH
from config import CHROMA_PATH

from utils.loader import load_documents
from utils.splitter import split_documents
from utils.embedding import get_embedding
from utils.vectordb import create_vector_db

documents = load_documents(PDF_PATH)

chunks = split_documents(documents)

embedding = get_embedding()

db = create_vector_db(

    chunks,

    embedding,

    CHROMA_PATH

)

print("Vector Database Created Successfully")