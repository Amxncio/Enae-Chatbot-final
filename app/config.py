import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
RAG_SOURCE_URL: str = (
    "https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation"
)
