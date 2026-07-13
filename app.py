from config import CHROMA_PATH

from utils.embedding import get_embedding
from utils.db_loader import load_vector_db
from utils.retriever import create_retriever
from utils.llm import load_llm

from prompts.rag_prompt import prompt

from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_classic.chains import create_retrieval_chain

embedding = get_embedding()

db = load_vector_db(

    CHROMA_PATH,

    embedding

)

retriever = create_retriever(db)

llm = load_llm()

document_chain = create_stuff_documents_chain(

    llm,

    prompt

)

rag_chain = create_retrieval_chain(

    retriever,

    document_chain

)

while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":

        break

    response = rag_chain.invoke(

        {"input": question}

    )

    print("\nAnswer:\n")

    print(response["answer"])