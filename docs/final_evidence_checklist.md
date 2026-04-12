# Final Evidence Checklist (ENAE)

Lista para entregar al profesor con trazabilidad **criterio → prueba**.

## Resumen técnico (implementado en código)

| Requisito | Cómo queda cubierto |
|-----------|---------------------|
| Conv. 1–7 sin tool de disponibilidad vía LLM | `app/bot.py`: cadena sin `bind_tools`; bypass de cuestionario si `_is_info_question` con `in_flow`. |
| Memoria + sesión | `session_id` + historial LangChain; flujo de cita: `slot_state` en `POST /ask_bot` (Vercel). |
| Conv. 8–9 (Tetris / calendario) | `create_booking` en UI; `check_availability` en `pytest`. |
| Conv. 10 (RAG) | `app/rag.py` + URL en `app/config.py`; ver [`docs/evidence/rag_conversation_10.md`](evidence/rag_conversation_10.md). |

## Cómo generar texto de apoyo

- **Transcripción Markdown** (misma API que la UI):  
  `python scripts/capture_acceptance_transcript.py --phase all > docs/evidence/transcript.md`  
  Definir `BASE_URL` (Vercel o local). El script reenvía `slot_state` en cada POST.
- **Tool `check_availability`:**  
  `python -m pytest tests/test_availability_tool.py -v`
- **Flujo guiado + bypass base:**  
  `python -m pytest tests/test_guided_flow.py -v`

## 1) Base chatbot (Conversations 1-7)

- [x] Criterio técnico: el LLM no invoca `check_availability` (cadena sin tools).
- [x] Patrones de bypass alineados al guion literal (tests en `test_guided_flow.py`).
- [x] Conv. 1–7 en el **mismo** `session_id` contra producción: [`docs/evidence/transcript.md`](evidence/transcript.md) — sección *Bloque 1–7*.

**Guion:** [`docs/acceptance_conversations.md`](acceptance_conversations.md) — sección *Guion literal* y *Matriz Doc VET*.

## 2) Tool availability (Conversations 8-9)

- [x] Documentación: [`docs/evidence/tool_conversations_8_9.md`](evidence/tool_conversations_8_9.md)
- [x] Transcripción flujo guiado hasta confirmación (producción): [`docs/evidence/transcript.md`](evidence/transcript.md) — *Bloque 8 — gato* y *Bloque 9 — perro*.
- [x] Tests de `check_availability`: `pytest tests/test_availability_tool.py`

## 3) RAG (Conversation 10)

- [x] Plantilla con recuperación real: [`docs/evidence/rag_conversation_10.md`](evidence/rag_conversation_10.md)
- [x] Respuesta del asistente en producción (misma API que la UI): [`docs/evidence/transcript.md`](evidence/transcript.md) — *Bloque 10 — RAG*.

## 4) Deploy and infrastructure

- [x] URL pública documentada: `https://enae-chatbot-final.vercel.app`
- [x] Smoke (2026-04-12): `GET /` → 200; `POST /ask_bot` con `msg=Hello` → 200 y JSON con `msg` + `slot_state`.
- [x] Evidencia de extremo a extremo en producción: transcripción completa [`docs/evidence/transcript.md`](evidence/transcript.md) (UTC en cabecera del archivo).
- [ ] Tras un **nuevo** deploy que toque dependencias o `vercel.json`, repetir smoke en incógnito.
- [ ] Confirmar en panel Vercel: variables solo allí (`GROQ_API_KEY`, `CALENDLY_*`, etc.); nunca valores reales en el repo.

## 5) Jira and traceability

- [ ] **Revisión manual antes de entregar:** tablero [EV](https://amxncio.atlassian.net/jira/software/projects/EV/boards/34) con **3 EPICs** (SET UP, SDD, CHATBOT), issues que reflejen trabajo real y, si el repo es privado, **invitación al profesor** o export.
- [x] Nota README: claves **EV-xx** en Jira vs etiqueta **VET-n** en títulos de caso.
- [x] Comentario de trazabilidad en `EV-17` (entrega nota 10 / rutas de evidencia en repo).
- [ ] Ticket calendario real (`EV-17` / VET-13): dejar en estado **Finalizada** (o el estado que pida el profesor) si debe verse cerrado en la revisión.

## 6) Intents (+1)

- [x] 20 intents + mapa 1–10: [`docs/intents_catalog.md`](intents_catalog.md)

## 7) Contraste con PDF Sesión 6

- [x] PDF en el repo: [`Caso Final Cierre y Evaluación.pdf`](../Caso%20Final%20Cierre%20y%20Evaluación.pdf) (mismo contenido que *Sesión 6 — Cierre y criterios* del aula).
- [ ] Si Canvas/plataforma pide **formato adicional** no recogido en ese PDF (vídeo, ZIP, plazo distinto), anótalo aquí:

*(Notas:)* 

---

**Commit de referencia (actualizar tras `git push`):** `git rev-parse HEAD` → anotar aquí antes de entregar.
