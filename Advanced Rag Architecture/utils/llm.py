from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY

def load_llm():
    # We use gemini-1.5-pro for advanced reasoning if possible, else 1.5-flash
    # Since earlier 1.5 wasn't working due to the SDK, we use 3.5-flash
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key=GOOGLE_API_KEY,
        temperature=0
    )
    return llm
