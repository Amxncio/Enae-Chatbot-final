# Acceptance Conversations — Reference

Reference document: *Conversaciones de aceptación — Chatbot clínica veterinaria* (course material, Session 6).

## Summary of the 10 conversations

### Base (5 pt) — Conversations 1–7 (without availability tool)

| Conv | Topic | Key test |
|------|-------|----------|
| 1 | Greeting and scope | Bot explains what it can help with |
| 2 | Delivery windows | Cat vs dog times; second turn requires remembering species |
| 3 | Pre-op blood test | Mandatory for animals >6 years |
| 4 | Emergency triage | Bot recognises emergency, redirects (out of scope) |
| 5 | Heat rejection | Female dog in heat → bot refuses, explains 2-month wait |
| 6 | Pick-up times | Dog (~12:00) vs cat (~15:00); may require memory |
| 7 | Human handoff | Bot acknowledges and offers transfer to human |

### +1 Tool — Conversations 8–9 (with availability tool)

| Conv | Topic | Key test |
|------|-------|----------|
| 8 | Availability check (cat) | Tool invocation, coherent result with Tetris rules |
| 9 | Availability check (dog) | Tool invocation, weight-based duration, dog limits |

### +1 RAG — Conversation 10

| Conv | Topic | Key test |
|------|-------|----------|
| 10 | Pre-surgery instructions (RAG) | Answers grounded in retrieved content from official URL |

## Testing guidance

- Conversations 1–7 are tested **in order**, each in the **same session** to verify memory.
- Domain knowledge can come from **system prompt and/or RAG** — both are acceptable.
- Tool conversations (8–9) verify the tool is **invocable** and returns **coherent** data.
- RAG conversation (10) verifies the **pipeline** retrieves from the official URL.

## Matriz Doc VET (trazabilidad con el backlog del curso)

Alineado con `Jira_Backlog_Caso_Veterinario_ES.md` / tablero Jira del equipo. Lista completa de tickets y SP: tabla **Backlog / Tickets** en [`README.md`](../README.md).

| Conv. | Doc VET (historias / frentes relacionados) | Implementación en repo |
|-------|---------------------------------------------|-------------------------|
| 1–7 | VET-7 (API), VET-8 (UI), VET-9 (`ask_bot` + LLM + prompt), VET-10 (memoria `session_id`) | `app/main.py`, `app/bot.py`, `app/prompt.py` — sin tool de disponibilidad en la cadena informativa |
| 8–9 | VET-12 (tool mock), VET-13 (calendario real), flujo guiado + `create_booking` | `app/tools.py`, `app/bot.py` (`slot_state`) |
| 10 | VET-11 (RAG URL oficial) | `app/rag.py`, `app/config.py` (`RAG_SOURCE_URL`) |

## Guion literal (inglés, alineado al MVP)

Usa **un solo `session_id`** para el bloque 1–7. Para 8, 9 y 10 conviene **sesiones distintas** para no mezclar memoria de cita.

### Bloque 1–7 (misma sesión)

| Paso | Mensaje del usuario |
|------|---------------------|
| 1a | `Hello` |
| 1b | `What can you help me with?` |
| 2a | `When should I bring my cat for drop-off on surgery day?` |
| 2b | `What time can I pick her up after the procedure?` |
| 3 | `My cat is 8 years old. Does she need a blood test before sterilisation?` |
| 4 | `My dog is bleeding heavily after an injury. What should I do?` |
| 5 | `My female dog is in heat. Can she be spayed next week?` |
| 6 | `What time can I pick up my dog after surgery?` |
| 7 | `Can I speak with a human, please?` |

### Bloque 8 — Gato (flujo guiado hasta confirmación)

Misma secuencia que valida el repo en tests; al confirmar se llama a `create_booking` (mismas reglas Tetris / Calendly que la tool de disponibilidad).

| Turno | Mensaje |
|-------|---------|
| 1 | `I need an appointment for sterilisation` |
| 2 | `cat` |
| 3 | `Whiskers` |
| 4 | `male` |
| 5 | `3` |
| 6 | `Evidence Catowner` *(nombre ficticio para entrega)* |
| 7 | `+34 600 000 008` *(teléfono ficticio)* |
| 8 | `yes` |

### Bloque 9 — Perro (flujo guiado hasta confirmación)

| Turno | Mensaje |
|-------|---------|
| 1 | `I need an appointment for sterilisation` |
| 2 | `dog` |
| 3 | `Rex` |
| 4 | `female` |
| 5 | `5 years old` |
| 6 | `14 kg` |
| 7 | `Evidence Dogowner` |
| 8 | `+34 600 000 009` |
| 9 | `yes` |

### Bloque 10 — RAG

| Mensaje |
|---------|
| `What fasting rules should I follow before my cat's surgery?` |

*(Respuesta esperable: ayuno 8–12 h, agua hasta 1–2 h antes, alineado con la URL oficial de preoperatorio.)*

## Automatizar la transcripción

Desde la raíz del repo (con el servidor local o producción):

```bash
export BASE_URL=https://enae-chatbot-final.vercel.app   # o http://127.0.0.1:8000
python scripts/capture_acceptance_transcript.py --phase all > docs/evidence/transcript.md
```

Fases: `base`, `tool_cat`, `tool_dog`, `rag`, `all`. El cliente reenvía `slot_state` como exige Vercel.
