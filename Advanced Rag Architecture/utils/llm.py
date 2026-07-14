from langchain_groq import ChatGroq
from config import GROQ_API_KEY

def load_llm():
    llm = ChatGroq(
        model="gemma2-9b-it",
        api_key=GROQ_API_KEY,
        temperature=0
    )
    return llm
