# Entregables — Caso chatbot clínica veterinaria (ENAE)

**Alumno:** Amancio  
**Rama principal:** `main`  
**Repositorio (público):** [Amxncio/Enae-Chatbot-final](https://github.com/Amxncio/Enae-Chatbot-final)

**Documento normativo en este repo:** [`Caso Final Cierre y Evaluación.pdf`](../Caso%20Final%20Cierre%20y%20Evaluación.pdf) (Sesión 6: *Cierre, entrega del caso y criterios de evaluación*, 27 marzo 2026 — Prof. Jaime Marco, ENAE Business School). En la plataforma del curso el mismo material puede figurar como `viewer/assets/documents/ENAE - Sesión 6_ Cierre, entrega del caso y criterios de evaluación.pdf` (véase `viewer/data/course-data.js` en el export del aula).

---

## Puntuación (10 pt) — resumen del PDF

| Tramo | Pt | Qué se evalúa (según PDF) | Guiones / evidencia |
|-------|---:|---------------------------|---------------------|
| **Base:** memoria + dominio, **sin** tool de disponibilidad | **5** | Misma sesión; system prompt claro; dominio vía **prompt y/o RAG** (compatibles; pueden solaparse). **Sin** memoria de sesión + prompt claro en código/repo → la base **no** se considera aprobada. | **Conv. 1 → 7** en orden (`Conversaciones_Aceptacion_Chatbot_Veterinario_ES.md`). Conv. **8–10 no cuentan** para estos 5 pt. |
| **+ Vercel** | **1** | Deploy (preview o prod); variables solo en panel; **sin** API keys en el repo. | — |
| **+ Jira** | **1** | Board visible; tareas enlazadas al repo; trazabilidad. **1 ticket = 1 frente.** | — |
| **+ RAG (URL oficial)** | **1** | Pipeline + retriever **demostrable** desde la URL; **conv. 10** (guion típico ayuno/preoperatorio); solapamiento con prompt **válido**. | Conv. 10 |
| **+ Tool disponibilidad** | **1** | Tool invocable; salida coherente con Tetris/cupo y reglas del dominio. | Conv. 8 y 9 |
| **+ Intents** | **1** | Catálogo en `Intents_Veterinary_Chatbot_Catalog_EN.md`: **20 intents** + mapa a conv. | Conv. 1–10 |

**Total:** 5 + 5×1 = **10 pt**.

### Base (5 pt) — conversaciones 1 a 7 (extracto del PDF)

- **Conv. 1:** saludo y alcance del bot.  
- **Conv. 2:** ventanas de entrega (gato vs perro); el segundo turno exige **memoria** de especie.  
- **Conv. 3:** analítica preoperatoria (>6 años).  
- **Conv. 4:** emergencia → triaje, fuera de alcance.  
- **Conv. 5:** reserva imposible (celo) → rechazo motivado desde reglas del caso.  
- **Conv. 6:** horarios de recogida (perro vs gato).  
- **Conv. 7:** derivación a humano.  

**Conv. 8 y 9:** tool de disponibilidad. **Conv. 10:** ayuno/preoperatorio — guion típico para el **+1 RAG** (hay que **demostrar** el retriever).

### MVP y alcance (PDF)

- Problema del MVP: **reducir tiempo y fricción** al coordinar citas de **castración/esterilización**.  
- Identificación de usuario (login, perfiles, CRM): **opcional**, fuera del núcleo del MVP; **no penaliza** no implementarlo.

---

## Tres documentos de referencia (Sesión 6) ↔ archivos en este repo

| Nombre en el material del curso | En este repositorio |
|----------------------------------|---------------------|
| `Conversaciones_Aceptacion_Chatbot_Veterinario_ES.md` | [docs/acceptance_conversations.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/acceptance_conversations.md) |
| `Jira_Backlog_Caso_Veterinario_ES.md` (Doc VET-1…VET-14, 3 EPIC) | Tablero Jira + trazabilidad; estructura alineada con el backlog del caso |
| `Intents_Veterinary_Chatbot_Catalog_EN.md` (20 intents + mapa conv. 1–10) | [docs/intents_catalog.md](https://github.com/Amxncio/Enae-Chatbot-final/blob/main/docs/intents_catalog.md) |

---

## Checklist de entregables (PDF — «ENTREGABLES (CHECKLIST)»)

- [x] Enlace al repositorio **público** con README (**cómo ejecutar** + **qué está implementado**).  
- [x] *(PDF: si el repo fuera privado, colaborador `jmarco111`.)* — No aplica: repo abierto.  
- [x] **URL de Vercel** documentada en README y en este índice.  
- [x] **Tablero Jira** [EV](https://amxncio.atlassian.net/jira/software/projects/EV/boards/34): tickets VET cerrados con **comentario de resolución** (repo + evidencias).  
- [x] **Evidencias breves (repo):** preguntas RAG en README; transcripción completa conv. 1–10 en [`docs/evidence/transcript.md`](evidence/transcript.md) (producción); tests y guías en `docs/evidence/`.  
- [x] **Sin secretos en Git:** `.env` en `.gitignore`, `.env.example` con placeholders; claves solo en panel Vercel / `.env` local.

---

## Testing que realizará el profesor (resumen del PDF)

- **Repo:** clonar o abrir enlace; seguir README en entorno limpio (o revisar URL pública).  
- **Base (5 pt):** memoria + dominio; conv. **1 a 7 en orden** sin tool de disponibilidad; conocimiento vía prompt y/o RAG según el doc de conversaciones.  
- **Vercel (+1):** URL producción/preview; carga sin errores evidentes de configuración.  
- **Jira (+1):** tickets concretos que correspondan a trabajo real (no tablero vacío el día de entrega).  
- **RAG (+1):** README y evidencia de retriever con la **URL oficial**; recuperación observable. Coherencia con prompt no invalida el punto si el pipeline RAG está demostrado.  
- **Tool (+1):** flujo que invoca la tool; salida coherente con reglas del caso.  
- **Intents (+1):** contraste con catálogo y conversaciones; 2–3 diálogos reales frente al chatbot.

---

## Fuente obligatoria para el RAG (+1 pt)

- **URL:** [https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation](https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation)  
- Debe quedar claro en el README **cómo** se obtiene, trocea, indexa y recupera ese texto/HTML antes de responder, y debe poder **demostrarse** el retriever (log, captura o prueba acordada).  
- **No vale** un RAG solo con PDFs genéricos si no incorpora esta URL como fuente principal del caso.

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

## Referencia de código de clase (PDF)

- Baseline sugerido en el curso: [https://github.com/kuuli/veterinary-clinic-chatbot](https://github.com/kuuli/veterinary-clinic-chatbot) (fork permitido).

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

*Criterios y entregables según `Caso Final Cierre y Evaluación.pdf`. Commit de referencia: `git rev-parse HEAD` antes de la entrega.*
