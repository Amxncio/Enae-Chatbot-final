# Material Preparatorio — Caso Clínica Veterinaria

## Perfil de la clínica

Clínica dedicada **casi en exclusiva** a medicina preventiva:

- Esterilización canina y felina (castración / ovariohisterectomía)
- Vacunación e identificación por microchip

**No** ofrece consultas rutinarias ni urgencias. Si el animal presenta un problema de salud no relacionado con la esterilización, debe acudir a otro centro.

## Alcance del MVP

El producto mínimo viable (MVP) ataca un problema concreto: **reducir el tiempo y la fricción al coordinar citas de castración y esterilización**.

### Dentro del alcance

- Información sobre el proceso de esterilización (preoperatorio, postoperatorio)
- Consulta de disponibilidad quirúrgica (algoritmo Tetris)
- Reserva de cita respetando las reglas del dominio
- Reglas de entrega por especie (ventanas horarias)
- Instrucciones de ayuno y preparación
- Derivación a humano cuando el caso excede al bot

### Fuera del alcance (no penaliza)

- Identificación robusta de usuario (login, OAuth, perfiles persistentes)
- Gestión de emergencias médicas (se deriva)
- Consultas rutinarias o de especialidades no ofrecidas
- Más de una mascota por conversación (se deriva a llamada telefónica)

## Supuestos del MVP

1. El usuario tiene **una sola mascota** por conversación.
2. El bot opera en **inglés** (mensajes) con conocimiento del dominio en ambos idiomas.
3. La disponibilidad se consulta sobre un **calendario mock** (lun–jue).
4. No se requiere autenticación ni datos personales reales.

## Herramientas del equipo

| Herramienta | Uso |
|-------------|-----|
| Cursor | Editor asistido por IA |
| GitHub | Repositorio del proyecto |
| Vercel | Despliegue (preview/producción) |
| Jira (Atlassian) | Gestión de tickets y backlog |
| Groq | Proveedor LLM (gratis) |

## Enlaces útiles

- [Repo baseline](https://github.com/kuuli/veterinary-clinic-chatbot)
- [URL oficial preoperatorio (RAG)](https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation)
- [Documentación del curso — Canvas ENAE](https://enae.instructure.com)
