# Entregables — Caso chatbot clínica veterinaria (ENAE)

Documento índice con **enlaces directos** a lo que suele pedirse en el cierre del caso (repo, despliegue, Jira, documentación técnica, evidencias y criterios de aceptación).

**Alumno:** Amancio  
**Rama principal:** `main`  
**Repositorio:** `Amxncio/Enae-Chatbot-final`

---

## 1. Accesos operativos (lo primero que revisa el profesor)

| Entregable | Enlace |
|------------|--------|
| **Repositorio GitHub** | [https://github.com/Amxncio/Enae-Chatbot-final](https://github.com/Amxncio/Enae-Chatbot-final) |
| **Aplicación desplegada (Vercel)** | [https://enae-chatbot-final.vercel.app](https://enae-chatbot-final.vercel.app) |
| **Tablero Jira (proyecto EV)** | [https://amxncio.atlassian.net/jira/software/projects/EV/boards/34](https://amxncio.atlassian.net/jira/software/projects/EV/boards/34) |
| **Ejemplo de issue calendario real (VET-13)** | [https://amxncio.atlassian.net/browse/EV-17](https://amxncio.atlassian.net/browse/EV-17) |

> **Nota:** En Jira la clave del proyecto es **EV-xx**; en títulos/descripciones se mantiene la etiqueta pedagógica **VET-n** del caso.

---

## 2. Documentación maestra en el repo (GitHub, rama `main`)

| Entregable | Enlace (vista en GitHub) |
|------------|---------------------------|
| **README del proyecto** | [README.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/README.md) |
| **Tabla “Paquete de entrega (nota 10)”** | Incluida en el README (sección homónima) |
| **Reglas SDD / convenciones repo–Jira** | [docs/SDD_PROJECT_RULES.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/SDD_PROJECT_RULES.md) |
| **Conversaciones de aceptación (guion + fases script)** | [docs/acceptance_conversations.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/acceptance_conversations.md) |
| **Checklist de evidencias para entrega** | [docs/final_evidence_checklist.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/final_evidence_checklist.md) |
| **Catálogo de 20 intents (mapa conv. 1–10)** | [docs/intents_catalog.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/intents_catalog.md) |
| **Reglas de negocio / Tetris** | [docs/business_rules.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/business_rules.md) |
| **Event Storming** | [docs/event_storming.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/event_storming.md) |
| **Material preparatorio** | [docs/preparatory.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/preparatory.md) |
| **Índice carpeta evidencias** | [docs/evidence/README.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/evidence/README.md) |
| **Evidencia RAG (conv. 10)** | [docs/evidence/rag_conversation_10.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/evidence/rag_conversation_10.md) |
| **Evidencia tool / citas (conv. 8–9)** | [docs/evidence/tool_conversations_8_9.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/evidence/tool_conversations_8_9.md) |
| **Plantilla variables de entorno** | [.env.example](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/.env.example) |

---

## 3. Código y API (referencia rápida)

| Entregable | Enlace |
|------------|--------|
| **Entrada FastAPI** | [app/main.py](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/app/main.py) |
| **Motor del chat (memoria, slots, flujo)** | [app/bot.py](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/app/bot.py) |
| **System prompt** | [app/prompt.py](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/app/prompt.py) |
| **RAG (URL + BM25)** | [app/rag.py](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/app/rag.py) |
| **Config (incl. `RAG_SOURCE_URL`)** | [app/config.py](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/app/config.py) |
| **Tools: disponibilidad Tetris / Calendly / reserva** | [app/tools.py](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/app/tools.py) |
| **UI del chat** | [app/templates/chat.html](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/app/templates/chat.html) |
| **Deploy Vercel** | [vercel.json](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/vercel.json) · [api/index.py](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/api/index.py) |
| **Script transcripción aceptación** | [scripts/capture_acceptance_transcript.py](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/scripts/capture_acceptance_transcript.py) |
| **Tests** | [tests/](https://github.com/Amxncio/Enae-Chatbot-final/tree/main/tests) |

### API en producción (si Vercel expone OpenAPI)

- **Swagger:** [https://enae-chatbot-final.vercel.app/docs](https://enae-chatbot-final.vercel.app/docs)  
- **ReDoc:** [https://enae-chatbot-final.vercel.app/redoc](https://enae-chatbot-final.vercel.app/redoc)  

*(Si alguna ruta no respondiera tras un deploy, usar la misma ruta en local con `uvicorn`.)*

---

## 4. RAG — fuente oficial del enunciado

| Entregable | Enlace |
|------------|--------|
| **URL oficial de instrucciones preoperatorias** | [https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation](https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation) |
| **Caché / fallback en repo** | [app/data/rag_source.txt](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/app/data/rag_source.txt) |

---

## 5. Skills Cursor (SDD / enriquecimiento de tickets)

| Entregable | Enlace |
|------------|--------|
| **Skill enrich Jira** | [.cursor/skills/enrich-jira-ticket/SKILL.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/.cursor/skills/enrich-jira-ticket/SKILL.md) |
| **Skill implementar desde spec** | [.cursor/skills/implement-from-spec/SKILL.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/.cursor/skills/implement-from-spec/SKILL.md) |

---

## 6. Servicios externos (configuración, sin secretos)

| Recurso | Enlace |
|---------|--------|
| **Claves Groq** | [https://console.groq.com/keys](https://console.groq.com/keys) |
| **Panel Vercel (variables de entorno)** | [https://vercel.com/dashboard](https://vercel.com/dashboard) *(proyecto del alumno)* |
| **Calendly developers** | [https://developer.calendly.com/](https://developer.calendly.com/) |

---

## 7. PDF del curso (Sesión 6 — criterios de evaluación)

El PDF **“ENAE - Sesión 6_ Cierre, entrega del caso y criterios de evaluación”** suele estar en la plataforma del curso, no siempre en el repo exportado. **Contrasta** los requisitos de ese PDF con esta lista y añade aquí cualquier entrega adicional (vídeo, informe en PDF, fecha límite):

- *(Anotaciones del alumno:)*  

---

## 8. Comandos de verificación (para el profesor o el alumno)

```bash
git clone https://github.com/Amxncio/Enae-Chatbot-final.git && cd Enae-Chatbot-final
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # completar GROQ_API_KEY para prueba local
python -m pytest -q
```

Transcripción de conversaciones (con `BASE_URL` en Vercel o local):

```bash
export BASE_URL=https://enae-chatbot-final.vercel.app
python scripts/capture_acceptance_transcript.py --phase all > docs/evidence/transcript.md
```

---

*Última actualización del índice: generado como documento de entrega; el hash de commit concreto puede anotarse con `git rev-parse HEAD` antes de la fecha límite.*
