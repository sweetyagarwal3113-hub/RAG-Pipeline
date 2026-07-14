from langchain_huggingface import HuggingFaceEndpoint
from config import HF_TOKEN

def load_llm():
    llm = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        temperature=0.1,
        huggingfacehub_api_token=HF_TOKEN
    )
    return llm