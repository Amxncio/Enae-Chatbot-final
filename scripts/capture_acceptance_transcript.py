#!/usr/bin/env python3
"""Generate a Markdown transcript against /ask_bot for ENAE acceptance evidence.

Usage:
  export BASE_URL=https://enae-chatbot-final.vercel.app   # or http://127.0.0.1:8000
  python scripts/capture_acceptance_transcript.py --phase all > docs/evidence/transcript.md

Echoes slot_state between turns (required on Vercel serverless).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urljoin

import requests

DEFAULT_BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def post_message(
    base: str,
    session_id: str,
    msg: str,
    slot_state: dict[str, Any],
    timeout: int,
) -> tuple[str, dict[str, Any]]:
    url = urljoin(base + "/", "ask_bot")
    data = {
        "msg": msg,
        "session_id": session_id,
        "slot_state": json.dumps(slot_state),
    }
    r = requests.post(url, data=data, timeout=timeout)
    r.raise_for_status()
    body = r.json()
    return body.get("msg", str(body)), body.get("slot_state") or {}


def run_section(
    base: str,
    title: str,
    session_id: str,
    turns: list[tuple[str | None, str]],
    timeout: int,
) -> list[str]:
    lines: list[str] = [f"## {title}", "", f"**session_id:** `{session_id}`", ""]
    slot_state: dict[str, Any] = {}
    for label, user_msg in turns:
        if label:
            lines.append(f"### {label}")
            lines.append("")
        lines.append("**Usuario:**")
        lines.append("")
        lines.append(textwrap.indent(user_msg, "> "))
        lines.append("")
        try:
            reply, slot_state = post_message(
                base, session_id, user_msg, slot_state, timeout
            )
        except Exception as e:
            reply = f"*(error: {e})*"
        lines.append("**Asistente:**")
        lines.append("")
        lines.append(textwrap.indent(reply.strip(), "> "))
        lines.append("")
    return lines


def main() -> int:
    p = argparse.ArgumentParser(description="Capture /ask_bot transcript for acceptance evidence.")
    p.add_argument(
        "--base-url",
        default=DEFAULT_BASE,
        help="API root (default: BASE_URL env or http://127.0.0.1:8000)",
    )
    p.add_argument(
        "--phase",
        choices=("base", "tool_cat", "tool_dog", "rag", "all"),
        default="all",
    )
    p.add_argument("--timeout", type=int, default=120)
    args = p.parse_args()
    base = args.base_url.rstrip("/")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

    out: list[str] = [
        "# Transcript — acceptance runs",
        "",
        f"- **Base URL:** `{base}`",
        f"- **UTC time:** {stamp}",
        "",
    ]

    base_turns: list[tuple[str | None, str]] = [
        ("Conversación 1 — saludo y alcance", "Hello"),
        (None, "What can you help me with?"),
        (
            "Conversación 2 — ventanas gato + memoria (recogida sin repetir especie)",
            "When should I bring my cat for drop-off on surgery day?",
        ),
        (None, "What time can I pick her up after the procedure?"),
        (
            "Conversación 3 — analítica preoperatoria (>6 años)",
            "My cat is 8 years old. Does she need a blood test before sterilisation?",
        ),
        (
            "Conversación 4 — urgencia / fuera de alcance",
            "My dog is bleeding heavily after an injury. What should I do?",
        ),
        (
            "Conversación 5 — perra en celo",
            "My female dog is in heat. Can she be spayed next week?",
        ),
        (
            "Conversación 6 — hora de recogida perro",
            "What time can I pick up my dog after surgery?",
        ),
        (
            "Conversación 7 — derivación a humano",
            "Can I speak with a human, please?",
        ),
    ]

    # Flujo guiado en inglés hasta confirmación (misma lógica que tests; create_booking al confirmar).
    tool_cat: list[tuple[str | None, str]] = [
        (
            "Conversación 8 — disponibilidad / cita gato (flujo guiado)",
            "I need an appointment for sterilisation",
        ),
        (None, "cat"),
        (None, "Whiskers"),
        (None, "male"),
        (None, "3"),
        (None, "Evidence Catowner"),
        (None, "+34 600 000 008"),
        (None, "yes"),
    ]

    tool_dog: list[tuple[str | None, str]] = [
        (
            "Conversación 9 — disponibilidad / cita perro (flujo guiado)",
            "I need an appointment for sterilisation",
        ),
        (None, "dog"),
        (None, "Rex"),
        (None, "female"),
        (None, "5 years old"),
        (None, "14 kg"),
        (None, "Evidence Dogowner"),
        (None, "+34 600 000 009"),
        (None, "yes"),
    ]

    rag_turns: list[tuple[str | None, str]] = [
        (
            "Conversación 10 — RAG (instrucciones preoperatorias)",
            "What fasting rules should I follow before my cat's surgery?",
        ),
    ]

    if args.phase in ("base", "all"):
        out.extend(
            run_section(
                base,
                "Bloque 1–7 (misma sesión — memoria)",
                f"enae-acceptance-base-{stamp[:10]}",
                base_turns,
                args.timeout,
            )
        )
        out.append("")

    if args.phase in ("tool_cat", "all"):
        out.extend(
            run_section(
                base,
                "Bloque 8 — gato",
                f"enae-acceptance-cat-{stamp[:10]}",
                tool_cat,
                args.timeout,
            )
        )
        out.append("")

    if args.phase in ("tool_dog", "all"):
        out.extend(
            run_section(
                base,
                "Bloque 9 — perro",
                f"enae-acceptance-dog-{stamp[:10]}",
                tool_dog,
                args.timeout,
            )
        )
        out.append("")

    if args.phase in ("rag", "all"):
        out.extend(
            run_section(
                base,
                "Bloque 10 — RAG",
                f"enae-acceptance-rag-{stamp[:10]}",
                rag_turns,
                args.timeout,
            )
        )

    sys.stdout.write("\n".join(out).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
