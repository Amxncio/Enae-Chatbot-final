# Chatbot Clínica Veterinaria — ENAE Business School

> **Data Science e IA para la Toma de Decisiones**
> Caso final: chatbot para agendar esterilización/castración en una clínica veterinaria.

| Campo | Valor |
|-------|-------|
| **Equipo** | Amancio |
| **Repo** | [Enae-Chatbot-final](https://github.com/Amxncio/Enae-Chatbot-final) |
| **Jira** | [Board EV](https://amxncio.atlassian.net/jira/software/projects/EV/boards/34) |
| **Vercel** | [enae-chatbot-final.vercel.app](https://enae-chatbot-final.vercel.app) |

---

## Visión del producto (MVP)

Chatbot conversacional que **reduce el tiempo y la fricción** al coordinar citas de castración y esterilización. El bot conoce las reglas del dominio (tiempos quirúrgicos, ventanas de entrega, restricciones "Tetris"), puede consultar disponibilidad y responder dudas preoperatorias con información verificada vía RAG.

---

## Qué hemos implementado

| Tramo | Pts | Estado | Descripción |
|-------|-----|--------|-------------|
| Base (memoria + dominio) | 5 | Done | System prompt + memoria por sesión + dominio vía prompt y RAG |
| Vercel | +1 | Done | Deploy funcional, env vars en panel |
| Jira | +1 | Done | Board con tickets VET-1…VET-14, 3 EPICs |
| RAG (URL oficial) | +1 | Done | Pipeline BM25 desde la URL oficial de instrucciones preoperatorias |
| Tool disponibilidad | +1 | Done | Algoritmo Tetris (240 min, máx 2 perros, ventanas) + integración real Calendly con fallback mock |
| Intents | +1 | Done | 20 intents + mapa a conv. 1–10 |

---

## Instalación local

```bash
# 1. Clonar el repo
git clone https://github.com/Amxncio/Enae-Chatbot-final.git
cd Enae-Chatbot-final

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env y poner tu GROQ_API_KEY (gratis en https://console.groq.com/keys)

# 5. Arrancar el servidor
uvicorn app.main:app --reload --port 8000
```

Abre [http://localhost:8000](http://localhost:8000) para ver la UI del chat.

---

## Variables de entorno

| Variable | Descripción | Dónde |
|----------|-------------|-------|
| `GROQ_API_KEY` | Clave API de Groq (LLM) | `.env` local / panel Vercel |
| `CALENDLY_TOKEN` | Personal Access Token de Calendly | `.env` local / panel Vercel |
| `CALENDLY_EVENT_TYPE_CAT_URI` | URI del tipo de evento para gatos | `.env` local / panel Vercel |
| `CALENDLY_EVENT_TYPE_DOG_URI` | URI del tipo de evento para perros | `.env` local / panel Vercel |

> **`.env.example`** contiene placeholders sin secretos. Nunca subir claves reales al repo.

---

## API — OpenAPI / Swagger

Con el servidor levantado, la documentación interactiva está en:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | UI del chat (HTML) |
| `POST` | `/ask_bot` | Enviar mensaje al bot |

#### `POST /ask_bot`

```bash
curl -X POST http://localhost:8000/ask_bot \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "msg=Hello&session_id=test1"
```

---

## RAG — Pipeline de recuperación

**Fuente oficial:** [Pre-Surgery Instructions](https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation)

### Cómo funciona

1. **Fetch:** Se descarga el contenido de la URL oficial (con fallback a `app/data/rag_source.txt`).
2. **Chunking:** Se divide en fragmentos de ~300 caracteres con solapamiento.
3. **Indexación:** Se construye un índice BM25 (sin necesidad de embeddings externos).
4. **Retrieval:** Para cada pregunta del usuario, se recuperan los 3 chunks más relevantes.
5. **Inyección:** Los chunks se inyectan en el prompt como contexto antes de llamar al LLM.

### Preguntas de prueba

| Pregunta | Respuesta esperada |
|----------|--------------------|
| "What should I do before the surgery?" | Ayuno 8-12h, vacunación, desparasitación |
| "Can my cat be operated while in heat?" | Sí, los gatos pueden operarse en celo |
| "My dog is in heat, can she be sterilised?" | No, esperar 2 meses tras el celo |

---

## Tool de disponibilidad

- **`check_availability`:** misma lógica Tetris + Calendly; se demuestra con `pytest tests/test_availability_tool.py` (conv. 8–9 a nivel de criterio de tool).
- **`create_booking`:** la UI y `/ask_bot` confirman la cita tras el cuestionario guiado; aplica las mismas reglas de capacidad y calendario.

- **Algoritmo Tetris:** ≤240 min/día, máx 2 perros/día, ventanas de entrega por especie.
- **Modo real (VET-13):** consulta de slots reales con Calendly (`/event_type_available_times`).
- **Fallback seguro:** si Calendly falla o no está configurado, usa calendario mock lun–jue.
- **Evidencia:** Conv. 8 y 9 — ver [`docs/evidence/tool_conversations_8_9.md`](docs/evidence/tool_conversations_8_9.md).

**Conv. 1–7 (base):** el modelo de chat **no** tiene herramientas enlazadas; la disponibilidad no puede dispararse desde el LLM en preguntas informativas. El cuestionario de cita es aparte.

---

## Flujo guiado de cita (memoria real)

Orden de recogida de datos (un campo por turno), antes de la tarjeta de confirmación y `create_booking`:

1. Servicio (esterilización / vacunación / microchip; la esterilización es la que dispara Tetris).
2. Especie (gato/perro).
3. Nombre de la mascota.
4. Sexo (macho/hembra).
5. Edad en años (regla de analítica si tiene más de 6 años).
6. Peso en kg solo si es perra.
7. Nombre del titular y contacto (teléfono o email).
8. Confirmación sí/no → reserva.

La **UI** debe reenviar `slot_state` en cada `POST /ask_bot` (el JSON devuelto por la API) para que el flujo sobreviva a instancias frías en Vercel.

Las preguntas informativas del guion 1–7 (ventanas, recogida, urgencias, celo, humano) **no** siguen el cuestionario aunque el usuario hubiera dicho antes «cita»; el backend delega en el LLM sin tools.

Ejemplo breve (esterilización perro):

- User: "I need an appointment for sterilisation of my dog."
- Bot: pregunta especie / nombre / sexo / edad / peso (hembra) / titular / contacto.
- User: completa datos.
- Bot: muestra resumen y pide confirmación.
- User: "yes" → respuesta con fecha, ventana, recogida y duración.

**Rechazo automático en celo:** si el usuario menciona que la perra está en celo, el bot niega la cita y explica que debe esperar 2 meses tras el fin del ciclo (riesgo de pseudogestación). Los gatos sí pueden operarse en celo.

---

## Despliegue — Vercel

El proyecto se despliega como función serverless Python en Vercel.

- **URL:** [https://enae-chatbot-final.vercel.app](https://enae-chatbot-final.vercel.app)
- **Env vars:** Configuradas solo en el panel de Vercel (Settings → Environment Variables).
- **Build:** Automático al hacer push a `main`.

---

## Documentación del dominio

| Documento | Ruta |
|-----------|------|
| Material preparatorio | [`docs/preparatory.md`](docs/preparatory.md) |
| Event Storming (Mermaid) | [`docs/event_storming.md`](docs/event_storming.md) |
| Reglas de negocio | [`docs/business_rules.md`](docs/business_rules.md) |
| Catálogo de intents | [`docs/intents_catalog.md`](docs/intents_catalog.md) |
| Reglas SDD | [`docs/SDD_PROJECT_RULES.md`](docs/SDD_PROJECT_RULES.md) |
| Conversaciones de aceptación | [`docs/acceptance_conversations.md`](docs/acceptance_conversations.md) |
| Checklist final de evidencias | [`docs/final_evidence_checklist.md`](docs/final_evidence_checklist.md) |
| **Índice de entregables para el profesor** | [`docs/ENTREGABLES_PROFESOR.md`](docs/ENTREGABLES_PROFESOR.md) |
| Carpeta de evidencias (RAG, tool, transcript) | [`docs/evidence/`](docs/evidence/) |

---

## Paquete de entrega (nota 10)

Criterios alineados con [`Caso Final Cierre y Evaluación.pdf`](Caso%20Final%20Cierre%20y%20Evaluación.pdf) (Sesión 6). Si el repositorio es **privado**, añade al profesor como colaborador en GitHub: **`jmarco111`**.

| Criterio (PDF Sesión 6) | Evidencia en el repo |
|-------------------------|----------------------|
| Base 5 pts (conv. 1–7, memoria, sin tool en info) | [`docs/acceptance_conversations.md`](docs/acceptance_conversations.md) (incl. matriz Doc VET), [`docs/evidence/transcript.md`](docs/evidence/transcript.md) (*Bloque 1–7*), `tests/test_guided_flow.py` |
| +1 RAG (conv. 10) | [`docs/evidence/transcript.md`](docs/evidence/transcript.md) (*Bloque 10*), [`docs/evidence/rag_conversation_10.md`](docs/evidence/rag_conversation_10.md), [`app/rag.py`](app/rag.py) |
| +1 Tool (conv. 8–9) | [`docs/evidence/transcript.md`](docs/evidence/transcript.md) (*Bloques 8–9*), [`docs/evidence/tool_conversations_8_9.md`](docs/evidence/tool_conversations_8_9.md), `pytest tests/test_availability_tool.py -v` |
| +1 Vercel | URL arriba; smoke manual o script; **sin** `.env` en Git |
| +1 Jira | [Board EV](https://amxncio.atlassian.net/jira/software/projects/EV/boards/34); issues `EV-xx` = historias del proyecto; el prefijo **VET-n** en títulos es la etiqueta pedagógica del caso |
| +1 Intents | [`docs/intents_catalog.md`](docs/intents_catalog.md) (20 intents) |
| SDD / Skills | [`.cursor/skills/`](.cursor/skills/), [`docs/SDD_PROJECT_RULES.md`](docs/SDD_PROJECT_RULES.md) |

**Índice detallado para el profesor:** [`docs/ENTREGABLES_PROFESOR.md`](docs/ENTREGABLES_PROFESOR.md).

---

## Backlog / Tickets

| ID | Épica | Resumen | SP | Estado |
|----|-------|---------|----|--------|
| VET-1 | SET UP | Repo baseline y accesos | 1 | Done |
| VET-2 | SET UP | README maestro | 2 | Done |
| VET-3 | SET UP | Vercel + deploy | 2 | Done |
| VET-14 | SET UP | Docs dominio en repo | 2 | Done |
| VET-4 | SDD | Reglas SDD: repo + Jira | 1 | Done |
| VET-5 | SDD | Comando enrich | 2 | Done |
| VET-6 | SDD | Comando implementar | 2 | Done |
| VET-7 | CHATBOT | FastAPI 2 endpoints + Swagger | 1 | Done |
| VET-8 | CHATBOT | UI chat inyectable | 1 | Done |
| VET-9 | CHATBOT | ask_bot + LLM + prompt | 2 | Done |
| VET-10 | CHATBOT | Memoria por session_id | 2 | Done |
| VET-11 | CHATBOT | RAG URL oficial | 2 | Done |
| VET-12 | CHATBOT | Tool disponibilidad (mock) | 2 | Done |
| VET-13 | CHATBOT | Tool + calendario real | 3 | Done |

---

## Skills de Cursor (SDD)

Para que el profesor vea claramente la parte de Skills:

- Skill de enrich: `.cursor/skills/enrich-jira-ticket/SKILL.md`
- Skill de implementación: `.cursor/skills/implement-from-spec/SKILL.md`

Uso típico en Cursor:

1. Abrir el ticket en Jira (o pegar el contexto del ticket).
2. Ejecutar la skill **enrich-jira-ticket** para completar objetivo, criterios, dependencias, riesgos y evidencia.
3. Ejecutar la skill **implement-from-spec** para llevar el ticket enriquecido a cambios en código y verificación final.

---

## Evidencia VET-13 (Calendly real)

Respuesta real de la tool `check_availability` tras integrar Calendly:

```json
{
  "available": true,
  "mode": "real_calendly",
  "date": "2026-04-01",
  "calendar_slot_start_utc": "2026-04-01T17:00:00Z",
  "surgery_duration_minutes": 15
}
```

---

## Stack tecnológico

- **LLM:** Groq (`llama-3.3-70b-versatile`) — gratis
- **Framework:** FastAPI + Jinja2
- **Cadena:** LangChain (prompt + memoria + RAG + tools)
- **RAG:** BM25 (`rank_bm25`) — sin API key de embeddings
- **Deploy:** Vercel (Python serverless)

---

## Tests rápidos

Tests mínimos de disponibilidad y flujo guiado:

```bash
python -m pytest -q
```

**Evidencia de entrega (ENAE):** checklist en [`docs/final_evidence_checklist.md`](docs/final_evidence_checklist.md); guion y comando de transcripción en [`docs/acceptance_conversations.md`](docs/acceptance_conversations.md) y `scripts/capture_acceptance_transcript.py`.
