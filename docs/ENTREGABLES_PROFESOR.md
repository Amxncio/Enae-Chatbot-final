# Entregables — Caso chatbot clínica veterinaria (ENAE)

**Alumno:** Amancio  
**Rama principal:** `main`  
**Repositorio:** `Amxncio/Enae-Chatbot-final`

---

## Marco normativo (Sesión 6)

El documento oficial de **cierre del caso y criterios de evaluación** del curso es el PDF que figura en el material descargado como:

**`viewer/assets/documents/ENAE - Sesión 6_ Cierre, entrega del caso y criterios de evaluación.pdf`**

(Referencia en el índice del viewer: `viewer/data/course-data.js`, ítem con ese título.)

En muchas exportaciones ZIP del aula **no viaja el binario** de `viewer/assets/documents/`; en ese caso hay que abrir el mismo archivo desde la plataforma o copiarlo a esa ruta. **No se asume aquí ninguna rúbrica ni lista de entregables** que no esté en ese PDF: lo siguiente es un **mapa de navegación** al código y a la documentación del proyecto para localizar evidencias **después** de contrastar con lo que pida el PDF.

---

## Entregables y criterios (según el PDF — completar literalmente)

Abre el PDF de la Sesión 6 y **trascribe en esta tabla** los criterios, entregables, formatos y ponderaciones tal como aparecen (títulos y porcentajes sin parafrasear). En la última columna enlaza a la evidencia concreta en el repo o en la demo.

| # | Criterio / entregable (texto del PDF) | Peso / nota (si figura) | Evidencia en este trabajo |
|---|----------------------------------------|-------------------------|----------------------------|
| 1 | *(copiar del PDF)* | | |
| 2 | | | |
| 3 | | | |

*(Añade filas según el número de apartados del PDF.)*

---

## Accesos operativos (revisión del entregable)

| Qué revisar | Enlace |
|-------------|--------|
| **Repositorio GitHub** | [https://github.com/Amxncio/Enae-Chatbot-final](https://github.com/Amxncio/Enae-Chatbot-final) |
| **Aplicación desplegada (Vercel)** | [https://enae-chatbot-final.vercel.app](https://enae-chatbot-final.vercel.app) |
| **Tablero Jira (proyecto EV)** | [https://amxncio.atlassian.net/jira/software/projects/EV/boards/34](https://amxncio.atlassian.net/jira/software/projects/EV/boards/34) |
| **Ejemplo de issue calendario real (VET-13)** | [https://amxncio.atlassian.net/browse/EV-17](https://amxncio.atlassian.net/browse/EV-17) |

> En Jira la clave del proyecto es **EV-xx**; en títulos y descripciones se mantiene la etiqueta pedagógica **VET-n** del caso.

---

## Documentación en el repo (rama `main`)

| Documento | Enlace (vista en GitHub) |
|-----------|---------------------------|
| **README del proyecto** | [README.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/README.md) |
| **Tabla “Paquete de entrega (nota 10)”** | Incluida en el README (sección homónima) |
| **Reglas SDD / convenciones repo–Jira** | [docs/SDD_PROJECT_RULES.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/SDD_PROJECT_RULES.md) |
| **Conversaciones de aceptación** | [docs/acceptance_conversations.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/acceptance_conversations.md) |
| **Checklist de evidencias** | [docs/final_evidence_checklist.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/final_evidence_checklist.md) |
| **Catálogo de 20 intents** | [docs/intents_catalog.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/intents_catalog.md) |
| **Reglas de negocio / Tetris** | [docs/business_rules.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/business_rules.md) |
| **Event Storming** | [docs/event_storming.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/event_storming.md) |
| **Material preparatorio** | [docs/preparatory.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/preparatory.md) |
| **Índice carpeta evidencias** | [docs/evidence/README.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/evidence/README.md) |
| **Evidencia RAG (conv. 10)** | [docs/evidence/rag_conversation_10.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/evidence/rag_conversation_10.md) |
| **Evidencia tool / citas (conv. 8–9)** | [docs/evidence/tool_conversations_8_9.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/evidence/tool_conversations_8_9.md) |
| **Plantilla variables de entorno** | [.env.example](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/.env.example) |

---

## Código y API (referencia rápida)

| Componente | Enlace |
|--------------|--------|
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

### API en producción

- **Swagger:** [https://enae-chatbot-final.vercel.app/docs](https://enae-chatbot-final.vercel.app/docs)  
- **ReDoc:** [https://enae-chatbot-final.vercel.app/redoc](https://enae-chatbot-final.vercel.app/redoc)  

---

## RAG — fuente oficial del enunciado

| Recurso | Enlace |
|---------|--------|
| **URL oficial de instrucciones preoperatorias** | [https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation](https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation) |
| **Caché / fallback en repo** | [app/data/rag_source.txt](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/app/data/rag_source.txt) |

---

## Skills Cursor (SDD / tickets)

| Skill | Enlace |
|-------|--------|
| **Enriquecer ticket Jira** | [.cursor/skills/enrich-jira-ticket/SKILL.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/.cursor/skills/enrich-jira-ticket/SKILL.md) |
| **Implementar desde spec** | [.cursor/skills/implement-from-spec/SKILL.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/.cursor/skills/implement-from-spec/SKILL.md) |

---

## Servicios externos (configuración, sin secretos)

| Recurso | Enlace |
|---------|--------|
| **Claves Groq** | [https://console.groq.com/keys](https://console.groq.com/keys) |
| **Panel Vercel** | [https://vercel.com/dashboard](https://vercel.com/dashboard) |
| **Calendly developers** | [https://developer.calendly.com/](https://developer.calendly.com/) |

---

## Comandos de verificación

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

*Índice de navegación al repo; los criterios de calificación son solo los del PDF de Sesión 6. Commit de referencia: anotar con `git rev-parse HEAD` antes de la entrega.*
