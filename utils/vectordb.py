from langchain_chroma import Chroma

def create_vector_db(chunks, embedding, persist_directory):

    db = Chroma.from_documents(

        documents=chunks,

        embedding=embedding,

        persist_directory=persist_directory

    )

    return db