import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    try:
        import streamlit as st
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    except KeyError:
        raise ValueError("GOOGLE_API_KEY not found in Streamlit Secrets! Please add it in Advanced Settings.")

if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
CHROMA_PATH = "db/chroma_db"

PDF_PATH = "data/Demo.pdf"