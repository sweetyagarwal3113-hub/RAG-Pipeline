import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    try:
        import streamlit as st
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass

CHROMA_PATH = "db/chroma_db"

PDF_PATH = "data/Demo.pdf"