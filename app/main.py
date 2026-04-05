"""FastAPI application — two endpoints as per Chatbot v4 OpenAPI spec."""

from __future__ import annotations

import json

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.rag import init_rag

app = FastAPI(
    title="Chatbot v4 — Veterinary Clinic",
    version="0.1.0",
    description="Chatbot for scheduling sterilisation appointments at a veterinary clinic.",
)

_templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

_rag_ready = False


@app.on_event("startup")
async def _startup():
    global _rag_ready
    init_rag()
    _rag_ready = True


@app.get("/", response_class=HTMLResponse, summary="Home")
async def home(request: Request):
    """Serve the chat UI."""
    # Starlette/FastAPI current signature expects request first.
    return _templates.TemplateResponse(request=request, name="chat.html")


@app.post("/ask_bot", summary="Ask Bot")
async def ask_bot(
    msg: str = Form(default=""),
    session_id: str = Form(default="default"),
    slot_state: str = Form(default=""),
):
    """Send a message to the chatbot and receive a response.

    Clients should echo back ``slot_state`` from the previous response so booking
    flow survives serverless cold starts (e.g. Vercel).
    """
    user_msg = msg.strip()
    sid = session_id.strip() or "default"

    if not user_msg:
        return JSONResponse(
            status_code=422,
            content={"error": "msg must be a non-empty string."},
        )

    from app.bot import apply_slots_from_client, ask, export_slots_for_client

    if slot_state.strip():
        try:
            parsed = json.loads(slot_state)
            apply_slots_from_client(sid, parsed)
        except (json.JSONDecodeError, TypeError):
            pass

    reply = ask(user_msg, sid)
    return {
        "msg": reply,
        "session_id": sid,
        "slot_state": export_slots_for_client(sid),
    }
