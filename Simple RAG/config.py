import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    try:
        import streamlit as st
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass
if GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

CHROMA_PATH = "db/chroma_db"

PDF_PATH = "data/Demo.pdf"