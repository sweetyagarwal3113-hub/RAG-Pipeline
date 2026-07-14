import os
from dotenv import load_dotenv
from google import genai

# Load API key
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("API Key not found!")
else:
    client = genai.Client(api_key=api_key)
    try:
        models = client.models.list()
        print("Available models:")
        for m in models:
            if "generateContent" in m.supported_actions:
                print(f" - {m.name}")
    except Exception as e:
        print(f"Error: {e}")
