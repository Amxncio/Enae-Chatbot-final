---
name: implement-from-spec
description: Implements ENAE veterinary chatbot tickets from an enriched Jira story or spec, following spec-first workflow, acceptance criteria verification, and repo/Jira traceability. Use when the user asks to implement a VET ticket or build from documented requirements.
---

# Implement From Spec (ENAE Veterinary Chatbot)

## Cuándo usar esta skill

Úsala cuando el usuario diga:
- "implementa VET-X"
- "haz este ticket"
- "desarrolla desde la spec"
- "lleva esto a código"

## Contexto mínimo requerido

Leer antes de tocar código:
- Ticket Jira (objetivo + AC)
- `docs/SDD_PROJECT_RULES.md`
- `README.md`
- Documentación funcional relacionada (`docs/*.md`)

## Flujo de implementación

1. **Spec first**
   - Entender AC y restricciones.
   - Detectar dependencias técnicas.
2. **Plan corto**
   - Archivos a crear/modificar.
   - Validación esperada.
3. **Implementar**
   - Backend: `app/`
   - UI: `app/templates/`
   - Deploy/config: raíz (`vercel.json`, `requirements.txt`, `.env.example`)
4. **Verificar**
   - Compila y corre local.
   - AC cubiertos explícitamente.
5. **Cerrar trazabilidad**
   - Actualizar README si aplica.
   - Dejar evidencia para Jira (commit/hash/url/log).

## Checklist de calidad (obligatorio)

- [ ] No secretos en repo.
- [ ] `.env.example` actualizado sin claves reales.
- [ ] Endpoint/UI funcional si el ticket lo exige.
- [ ] Prueba mínima reproducible documentada.
- [ ] Compatible con Vercel (si aplica).

## Criterios por tipo de ticket

### API / FastAPI
- `/docs` operativo
- Contrato request/response claro
- Manejo de errores coherente

### LLM / Memoria / RAG
- Variables de entorno correctamente leídas
- Memoria aislada por `session_id`
- RAG con fuente oficial y evidencia de recuperación

### Tools
- Tool invocable desde agente
- Resultado estructurado y verificable
- Reglas de negocio respetadas (Tetris)

## Formato de reporte de cierre

```markdown
### Implementación completada
- Ticket: VET-X
- Archivos modificados: [...]
- AC cubiertos: 1,2,3
- Evidencia: commit/hash/url/captura
- Riesgos abiertos: [si aplica]
```

## Referencias de proyecto

- Repo: `https://github.com/Amxncio/Enae-Chatbot-final`
- Jira: `https://amxncio.atlassian.net/jira/software/projects/EV/boards/34`
- Deploy: `https://enae-chatbot-final.vercel.app`
