"""Chat engine — LangChain chain with system prompt, memory, RAG context, and tools."""

from __future__ import annotations

import json
import re
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.prompt import SYSTEM_PROMPT
from app.rag import retrieve
from app.tools import check_availability

_store: dict[str, InMemoryChatMessageHistory] = {}
_slot_store: dict[str, dict] = {}

SCHEDULING_KEYWORDS = (
    "cita",
    "agendar",
    "reservar",
    "appointment",
    "schedule",
    "availability",
    "disponibilidad",
    "esteril",
    "castrar",
    "castration",
    "spay",
    "neuter",
)

SERVICE_KEYWORDS = (
    "esteril",
    "castra",
    "spay",
    "neuter",
)


def _default_slots() -> dict:
    return {
        "in_flow": False,
        "service": "",
        "species": "",
        "sex": "",
        "weight_kg": None,
        "preferred_date": "",
    }


def _get_slots(session_id: str) -> dict:
    if session_id not in _slot_store:
        _slot_store[session_id] = _default_slots()
    return _slot_store[session_id]


def _detect_scheduling_intent(msg: str) -> bool:
    text = msg.lower()
    return any(k in text for k in SCHEDULING_KEYWORDS)


def _extract_slots(msg: str, slots: dict) -> None:
    text = msg.lower()

    if any(k in text for k in SERVICE_KEYWORDS):
        slots["service"] = "sterilisation"

    if re.search(r"\b(cat|cats|gato|gata|gatos|gatas)\b", text):
        slots["species"] = "cat"
    elif re.search(r"\b(dog|dogs|perro|perra|perros|perras)\b", text):
        slots["species"] = "dog"

    if re.search(r"\b(male|macho)\b", text):
        slots["sex"] = "male"
    elif re.search(r"\b(female|hembra)\b", text):
        slots["sex"] = "female"

    weight_match = re.search(r"\b(\d{1,3}(?:[.,]\d{1,2})?)\s?(kg|kgs|kilos?)\b", text)
    if weight_match:
        raw = weight_match.group(1).replace(",", ".")
        try:
            slots["weight_kg"] = float(raw)
        except ValueError:
            pass

    date_match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", text)
    if date_match:
        slots["preferred_date"] = date_match.group(1)


def _next_missing_field(slots: dict) -> str | None:
    if not slots["service"]:
        return "service"
    if not slots["species"]:
        return "species"
    if not slots["sex"]:
        return "sex"
    if slots["species"] == "dog" and slots["sex"] == "female" and not slots["weight_kg"]:
        return "weight_kg"
    return None


def _question_for_field(field: str) -> str:
    if field == "service":
        return (
            "Perfecto, te ayudo con la cita. "
            "Para empezar, confirma el servicio: ¿quieres esterilizacion/castracion?"
        )
    if field == "species":
        return "Gracias. ¿Tu mascota es gato o perro?"
    if field == "sex":
        return "Entendido. ¿Es macho o hembra?"
    if field == "weight_kg":
        return "Al ser perra, necesito su peso en kg para calcular el tiempo quirurgico. ¿Cuanto pesa?"
    return "¿Me puedes dar un poco mas de informacion?"


def _render_availability_reply(result_json: str) -> str:
    try:
        data = json.loads(result_json)
    except json.JSONDecodeError:
        return "He encontrado disponibilidad, pero hubo un problema al formatear la respuesta."

    if data.get("error"):
        return f"Necesito ajustar los datos antes de buscar cita: {data['error']}"
    if not data.get("available"):
        return data.get(
            "message",
            "No he encontrado huecos en los proximos dias. ¿Quieres que lo revise con otra fecha?",
        )

    date = data.get("date", "")
    delivery = data.get("delivery_window", "")
    pickup = data.get("pickup_time", "")
    duration = data.get("surgery_duration_minutes", "")
    mode = data.get("mode", "")
    mode_note = ""
    if mode == "real_calendly":
        mode_note = " (disponibilidad real de calendario)"
    return (
        f"Excelente, he encontrado una fecha disponible{mode_note}: {date}. "
        f"Trae a tu mascota en la ventana de entrega {delivery}. "
        f"La cirugia dura aproximadamente {duration} minutos y la recogida es {pickup}. "
        "Recuerda ayuno de 8-12 horas (agua hasta 1-2 horas antes) y traer consentimiento firmado y documentacion."
    )


def _get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


def _build_chain():
    if not GROQ_API_KEY:
        return None

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0.3,
    )

    llm_with_tools = llm.bind_tools([check_availability])

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{context}\n\nUser: {input}"),
    ])

    chain = prompt | llm_with_tools

    return RunnableWithMessageHistory(
        chain,
        _get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )


_chain = None


def _get_chain():
    global _chain
    if _chain is None:
        _chain = _build_chain()
    return _chain


def ask(user_msg: str, session_id: str = "default") -> str:
    """Process a user message and return the bot reply."""
    slots = _get_slots(session_id)
    _extract_slots(user_msg, slots)

    if _detect_scheduling_intent(user_msg):
        slots["in_flow"] = True

    if slots["in_flow"]:
        missing = _next_missing_field(slots)
        if missing:
            return _question_for_field(missing)

        result = check_availability.invoke(
            {
                "species": slots["species"],
                "sex": slots["sex"],
                "weight_kg": float(slots["weight_kg"] or 0),
                "preferred_date": slots["preferred_date"],
            }
        )
        slots["in_flow"] = False
        return _render_availability_reply(result)

    chain = _get_chain()
    if chain is None:
        return "Error: GROQ_API_KEY is not configured. Set it in .env or Vercel environment variables."

    context = retrieve(user_msg)
    context_block = f"Context from knowledge base:\n{context}" if context else ""

    config = {"configurable": {"session_id": session_id}}

    try:
        response = chain.invoke(
            {"input": user_msg, "context": context_block},
            config=config,
        )

        if hasattr(response, "tool_calls") and response.tool_calls:
            tool_results = []
            for tc in response.tool_calls:
                if tc["name"] == "check_availability":
                    result = check_availability.invoke(tc["args"])
                    tool_results.append(result)

            if tool_results:
                history = _get_session_history(session_id)
                history.add_message(response)

                tool_context = "\n".join(
                    f"Tool result: {r}" for r in tool_results
                )
                followup = chain.invoke(
                    {
                        "input": f"Based on the tool results below, provide a helpful response to the user.\n\n{tool_context}\n\nOriginal question: {user_msg}",
                        "context": context_block,
                    },
                    config=config,
                )
                return followup.content if hasattr(followup, "content") else str(followup)

        return response.content if hasattr(response, "content") else str(response)

    except Exception as e:
        return f"I encountered an error: {e}"
