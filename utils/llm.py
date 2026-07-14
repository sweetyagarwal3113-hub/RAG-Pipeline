from langchain_huggingface import HuggingFaceEndpoint
from config import HF_TOKEN

def load_llm():
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        temperature=0.1,
        huggingfacehub_api_token=HF_TOKEN
    )
    return llm