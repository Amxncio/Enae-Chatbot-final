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
