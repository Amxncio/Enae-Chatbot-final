# Evidencia — Conversaciones 8–9 (disponibilidad / Tetris / calendario)

## En la aplicación

El flujo guiado de cita recopila datos y, al confirmar con **sí**, llama a **`create_booking`** en `app/tools.py`. Esa función aplica las mismas reglas **Tetris** (240 min/día, máx. 2 perros) y la misma integración **Calendly** (si está configurada en variables de entorno) que `check_availability`.

**Guion paso a paso:** [`docs/acceptance_conversations.md`](../acceptance_conversations.md) — bloques 8 (gato) y 9 (perro).

**Transcripción automática:**

```bash
export BASE_URL=https://enae-chatbot-final.vercel.app   # o http://127.0.0.1:8000
python scripts/capture_acceptance_transcript.py --phase tool_cat > /tmp/cat.md
python scripts/capture_acceptance_transcript.py --phase tool_dog > /tmp/dog.md
```

*(El cliente reenvía `slot_state` en cada POST, necesario en Vercel.)*

## Demostración explícita de la tool `check_availability`

El enunciado pide que la **tool** sea invocable; los tests llaman a `check_availability` directamente:

```bash
python -m pytest tests/test_availability_tool.py -v
```

Incluye casos de validación de entrada, `mock_fallback` y modo `real_calendly` (con mock).

## Qué debe verse en la respuesta final

- Ventana de **entrega** coherente con especie (gato vs perro).
- **Duración** quirúrgica coherente (p. ej. hembra perro con peso → bucket Tetris).
- Hora de **recogida** acorde al dominio.
- Indicación **(calendario real)** si Calendly responde en producción; si no, **mock** documentado en el texto de entrega.
