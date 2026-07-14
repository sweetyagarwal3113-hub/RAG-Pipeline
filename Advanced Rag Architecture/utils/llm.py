from langchain_groq import ChatGroq
from config import GROQ_API_KEY

def load_llm():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY,
        temperature=0
    )
    return llm
