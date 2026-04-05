import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_GOOGLE_SA_FILE = _REPO_ROOT / "docs" / "molten-reach-485011-b2-3bbf6b15204e.json"


def _resolve_google_service_account_json() -> str:
    """Load service account JSON from env, GOOGLE_SERVICE_ACCOUNT_FILE, or default docs path."""
    env_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if env_json:
        return env_json

    file_env = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "").strip()
    candidates: list[Path] = []
    if file_env:
        p = Path(file_env)
        candidates.append(p if p.is_absolute() else _REPO_ROOT / file_env)
    if _DEFAULT_GOOGLE_SA_FILE.is_file():
        candidates.append(_DEFAULT_GOOGLE_SA_FILE)

    for path in candidates:
        if path.is_file():
            return path.read_text(encoding="utf-8")
    return ""


def get_google_service_account_json() -> str:
    """Read SA JSON at call time (Vercel/serverless: env is reliable per request, not only at import)."""
    return _resolve_google_service_account_json()


def get_google_calendar_id() -> str:
    return os.getenv("GOOGLE_CALENDAR_ID", "").strip()


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

# Google Calendar — also use get_google_*() in tools (lazy) for serverless
GOOGLE_SERVICE_ACCOUNT_JSON: str = _resolve_google_service_account_json()
GOOGLE_CALENDAR_ID: str = os.getenv("GOOGLE_CALENDAR_ID", "").strip()
