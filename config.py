import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    try:
        import streamlit as st
        GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        pass
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    try:
        import streamlit as st
        HF_TOKEN = st.secrets["HF_TOKEN"]
    except KeyError:
        raise ValueError("HF_TOKEN not found in Streamlit Secrets! Please add it in Advanced Settings.")
if HF_TOKEN:
    os.environ["HF_TOKEN"] = HF_TOKEN
CHROMA_PATH = "db/chroma_db"

PDF_PATH = "data/Demo.pdf"