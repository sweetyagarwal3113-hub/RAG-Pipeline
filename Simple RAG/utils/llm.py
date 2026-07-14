from langchain_groq import ChatGroq
from config import GROQ_API_KEY

def load_llm():
    llm = ChatGroq(
        model="llama3-8b-8192",
        api_key=GROQ_API_KEY,
        temperature=0
    )
    return llm