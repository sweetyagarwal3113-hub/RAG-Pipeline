from langchain_chroma import Chroma

def load_vector_db(path, embedding):

    db = Chroma(

        persist_directory=path,

        embedding_function=embedding

    )

    return db