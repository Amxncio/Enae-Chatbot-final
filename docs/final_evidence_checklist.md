# Final Evidence Checklist (ENAE)

Usa esta lista para entregar al profesor pruebas **homogéneas** y trazables.

## Cómo generar texto de apoyo

- **Transcripción Markdown** (misma API que la UI):  
  `python scripts/capture_acceptance_transcript.py --phase all > docs/evidence/transcript.md`  
  Definir `BASE_URL` (Vercel o local). El script reenvía `slot_state` en cada POST.
- **Tool `check_availability` (payload + JSON):**  
  `python -m pytest tests/test_availability_tool.py -v`  
  Los tests invocan la tool directamente y muestran `mode: mock_fallback` o `real_calendly` (mockeado).

## 1) Base chatbot (Conversations 1-7)

- [ ] Ejecutar conversaciones 1-7 en el **mismo** `session_id`.
- [ ] Mostrar memoria (especie gata recordada en recogida sin repetir “cat”).
- [ ] Mostrar derivación en urgencia (fuera de alcance → clínico / otro centro).
- [ ] Guardar capturas de pantalla **o** pegar `docs/evidence/transcript.md` (bloque base).

**Guion:** [`docs/acceptance_conversations.md`](acceptance_conversations.md) — sección *Guion literal*.

Por conversación (rellenar):

- Conversation: `#1` … `#7`
- Input(s):
- Expected behavior:
- Observed output:
- Evidence file/link:

## 2) Tool availability (Conversations 8-9)

- [ ] Conversación 8 (gato): flujo guiado completo hasta `yes` **o** evidencia de `check_availability` vía pytest.
- [ ] Conversación 9 (perro): idem; debe reflejarse **peso** y duración coherente con reglas de hembra/perro.
- [ ] La respuesta final de cita incluye **ventana de entrega**, **recogida** y **duración** de cirugía.
- [ ] Indicar modo de calendario: en confirmación puede aparecer “(calendario real)” si `CALENDLY_*` está configurado en Vercel; si no, mock es válido — documentar cuál entorno usaste.

**Nota de implementación:** El flujo guiado confirma con `create_booking`, que aplica las mismas reglas Tetris y el mismo backend Calendly que `check_availability`. Para demostrar la **tool** explícitamente, adjunta salida de `pytest tests/test_availability_tool.py -v`.

Evidence fields:

- Tool call payload: *(pegar del test o de logs si tienes trace)*
- Tool response JSON:
- Why result is coherent with Tetris rules:
- Screenshot or log:

## 3) RAG (Conversation 10)

- [ ] Pregunta preoperatoria anclada en la URL oficial (p. ej. ayuno).
- [ ] Comprobar que la respuesta cita reglas 8–12 h / agua 1–2 h (u equivalente).
- [ ] Transcripción corta o captura.

Evidence fields:

- User question: *(ej.: `What fasting rules should I follow before my cat's surgery?`)*
- Retrieved/grounded points:
- Final assistant answer:
- Screenshot or log:

## 4) Deploy and infrastructure

- [x] Vercel URL responde en `/`.
- [x] `POST /ask_bot` funciona en producción.
- [ ] Variables de entorno solo en panel Vercel (captura parcial sin secretos, o declaración explícita en el texto de entrega).

Evidence fields:

- **URL tested:** `https://enae-chatbot-final.vercel.app`
- **Date/time:** 2026-04-05 (verificación automatizada)
- **Result:**
  - `GET /` → HTTP 200
  - `POST /ask_bot` con `msg=Hello&session_id=evidence-probe` → JSON con `msg` y `slot_state` (respuesta del asistente sin error 5xx)

## 5) Jira and traceability

- [ ] Ticket de calendario real cerrado (`EV-17`) — marcar cuando lo tengas en Jira.
- [ ] Comentarios de enriquecimiento en tickets VET (alcance).
- [x] Commits en `main` con mensajes claros (ej.: integración Calendar, UI sin enlace GCal en chat).

Evidence fields:

- Jira issue links:
  - `https://amxncio.atlassian.net/browse/EV-17`
- **Commit hash(es) (referencia repo):** `11bd016050e14de38a5b6d3f4b5d1a89d74692c9` *(actualizar si haces más commits después de la entrega)*
- Notes:
