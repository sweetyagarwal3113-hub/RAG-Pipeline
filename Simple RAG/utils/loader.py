from langchain_community.document_loaders import PyPDFLoader

def load_documents(path):
    loader = PyPDFLoader(path)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages")

    return documents