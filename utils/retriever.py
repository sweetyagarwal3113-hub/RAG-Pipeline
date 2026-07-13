def create_retriever(vector_db):

    retriever = vector_db.as_retriever(

        search_type="similarity",

        search_kwargs={"k":4}

    )

    return retriever