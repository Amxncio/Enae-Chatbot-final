---
name: enrich-jira-ticket
description: Enriches Jira tickets for the ENAE veterinary chatbot project with acceptance criteria, risks, dependencies, and evidence format. Use when the user asks to enrich tickets, prepare Jira stories, or improve issue quality before implementation.
---

# Enrich Jira Ticket (ENAE Veterinary Chatbot)

## Cuándo usar esta skill

Úsala cuando el usuario pida:
- "enriquecer tickets"
- "preparar historias de Jira"
- "dejar listos los VET-*"
- "mejorar criterios de aceptación"

## Contexto obligatorio

Antes de enriquecer, revisar:
- `docs/SDD_PROJECT_RULES.md`
- `docs/business_rules.md`
- `docs/intents_catalog.md`
- `README.md`

## Flujo

1. Leer ticket actual (resumen + descripción).
2. Reescribir en formato claro:
   - Objetivo
   - Alcance
   - Criterios de aceptación (numerados, testeables)
   - Dependencias (VET previos)
   - Riesgos
   - Evidencia esperada
3. Añadir trazabilidad:
   - Repo: `https://github.com/Amxncio/Enae-Chatbot-final`
   - URL app: `https://enae-chatbot-final.vercel.app`
   - Jira board: `https://amxncio.atlassian.net/jira/software/projects/EV/boards/34`

## Plantilla de enriquecimiento

Usar esta estructura exacta:

```markdown
## Objetivo
[Qué valor aporta este ticket]

## Alcance
[Qué entra / qué no entra]

## Criterios de aceptación
1. ...
2. ...
3. ...

## Dependencias
- ...

## Riesgos
- ...

## Evidencia esperada
- URL/commit/captura/log
```

## Reglas específicas ENAE

- Mantener alineación con scoring 10/10:
  - Base 5 pt (memoria + prompt + conv 1-7)
  - +1 Vercel
  - +1 Jira
  - +1 RAG URL oficial
  - +1 Tool disponibilidad
  - +1 Intents
- No incluir secretos en tickets/comentarios.
- Un ticket = un frente implementable.

## Mapeo rápido de dependencias VET

- SETUP: VET-1 → VET-2 → VET-3, y VET-14 en paralelo
- SDD: VET-4 → (VET-5, VET-6)
- CHATBOT: VET-7 → VET-8 → VET-9 → VET-10 → (VET-11, VET-12) → VET-13
