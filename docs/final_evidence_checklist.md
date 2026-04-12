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
- [ ] Ejecutar conversaciones 1-7 en el **mismo** `session_id` en UI o transcript y guardar captura o `docs/evidence/transcript.md`.

**Guion:** [`docs/acceptance_conversations.md`](acceptance_conversations.md) — sección *Guion literal*.

Por conversación (rellenar tras tu captura):

- Conversation: `#1` … `#7`
- Input(s):
- Expected behavior:
- Observed output:
- Evidence file/link:

## 2) Tool availability (Conversations 8-9)

- [x] Documentación: [`docs/evidence/tool_conversations_8_9.md`](evidence/tool_conversations_8_9.md)
- [ ] Transcripción `tool_cat` / `tool_dog` o capturas de la UI hasta confirmación.
- [x] Tests de `check_availability`: `pytest tests/test_availability_tool.py`

## 3) RAG (Conversation 10)

- [x] Plantilla con recuperación real: [`docs/evidence/rag_conversation_10.md`](evidence/rag_conversation_10.md)
- [ ] Captura de la respuesta del asistente en producción o `--phase rag` del script.

## 4) Deploy and infrastructure

- [x] URL pública documentada: `https://enae-chatbot-final.vercel.app`
- [x] Smoke (2026-04-12): `GET /` → 200; `POST /ask_bot` con `msg=Hello` → 200 y JSON con `msg` + `slot_state`.
- [ ] Tras tu próximo deploy, repetir smoke en incógnito si cambias dependencias o `vercel.json`.
- [ ] Variables solo en panel Vercel: `GROQ_API_KEY`, `CALENDLY_*` (y otras si las usas). Sin capturar valores secretos.

## 5) Jira and traceability

- [ ] Tablero [EV](https://amxncio.atlassian.net/jira/software/projects/EV/boards/34): 3 EPICs, historias enlazadas al repo.
- [x] Nota README: claves **EV-xx** en Jira vs etiqueta **VET-n** en títulos de caso.
- [x] Comentario de trazabilidad en `EV-17` (entrega nota 10 / rutas de evidencia en repo).
- [ ] Ticket calendario real (`EV-17` / VET-13) revisado por ti: estado *Finalizada* si el profe lo exige visible.

## 6) Intents (+1)

- [x] 20 intents + mapa 1–10: [`docs/intents_catalog.md`](intents_catalog.md)

## 7) Contraste con PDF Sesión 6

- [ ] Abrir el PDF de cierre en tu máquina y marcar aquí cualquier requisito extra (plazo, vídeo, entregable único):

*(Notas:)* 

---

**Commit de referencia (actualizar si haces push nuevo):** ejecutar `git rev-parse HEAD` antes de entregar.
