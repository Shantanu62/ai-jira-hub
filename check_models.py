import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Groq client initialize karein
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    print("Aapke API key ke liye available models ki list:")
    models = client.models.list()
    for model in models.data:
        print(f"- {model.id}")
except Exception as e:
    print(f"Error aaya: {e}")