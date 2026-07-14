import os
from dotenv import load_dotenv
from groq import Groq

# Load API key
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("API Key not found!")
else:
    client = Groq(api_key=api_key)
    try:
        models = client.models.list()
        print("Available Groq models:")
        for m in models.data:
            print(f" - {m.id}")
    except Exception as e:
        print(f"Error: {e}")
