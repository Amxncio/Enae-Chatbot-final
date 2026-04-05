import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
RAG_SOURCE_URL: str = (
    "https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation"
)

# Calendly — kept for backward-compat availability checks (read-only)
CALENDLY_TOKEN: str = os.getenv("CALENDLY_TOKEN", "")
CALENDLY_USER_URI: str = os.getenv("CALENDLY_USER_URI", "")
CALENDLY_EVENT_TYPE_CAT_URI: str = os.getenv("CALENDLY_EVENT_TYPE_CAT_URI", "")
CALENDLY_EVENT_TYPE_DOG_URI: str = os.getenv("CALENDLY_EVENT_TYPE_DOG_URI", "")

# Google Calendar integration — used to create actual booking events
GOOGLE_SERVICE_ACCOUNT_JSON: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "")
GOOGLE_CALENDAR_ID: str = os.getenv("GOOGLE_CALENDAR_ID", "")
