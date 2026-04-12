# Evidencia — Conversación 10 (RAG)

**Pregunta del usuario (guion de aceptación):**

> What fasting rules should I follow before my cat's surgery?

**Fuente configurada:** URL oficial en `app/config.py` (`RAG_SOURCE_URL`) + fallback `app/data/rag_source.txt`.

**Fragmentos recuperados (BM25, muestra local tras `init_rag()`):**

> …Animals must arrive fasting: the last meal should be 8–12 hours before the operation. They may have water until 1–2 hours before surgery…

**Puntos que deben reflejarse en la respuesta del asistente:**

- Ayuno de comida **8–12 h** antes de la cirugía.
- **Agua** permitida hasta **1–2 h** antes (con matices de calor si el contexto lo menciona).

**Cómo reproducir la recuperación (sin LLM):**

```bash
cd /ruta/al/repo
python -c "from app.rag import init_rag, retrieve; init_rag(); print(retrieve('What fasting rules before cat surgery?'))"
```

**Respuesta final del chat (producción):** ver transcripción fijada en [`transcript.md`](transcript.md) — sección *Bloque 10 — RAG* (generada con `capture_acceptance_transcript.py --phase all` contra Vercel).

Para regenerar solo RAG:

```bash
export BASE_URL=https://enae-chatbot-final.vercel.app
python scripts/capture_acceptance_transcript.py --phase rag > /tmp/rag-only.md
```
