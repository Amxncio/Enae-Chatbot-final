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

HEAT_KEYWORDS = (
    "in heat",
    "en celo",
    "in oestrus",
    "in estrus",
    "en calor",
    "está en celo",
    "esta en celo",
    "currently in heat",
    "is in heat",
    "está en calor",
)

# Messages that are general info questions, not active booking requests.
# When these patterns appear, bypass the slot flow and let the LLM answer.
_INFO_BYPASS_PATTERNS = [
    r"what time",
    r"when can i pick",
    r"when do i pick",
    r"pick.?up",
    r"\bcollect\b",
    r"i need to speak",
    r"speak with a human",
    r"talk to",
    r"transfer me",
    r"\bhuman\b",
    r"hablar con",
    r"habla con",
    r"persona humana",
    r"recoger",
    r"recogida",
    r"a qué hora",
    r"a que hora",
]

SERVICE_KEYWORDS = (
    "esteril",
    "steril",   # matches sterilisation / sterilization / sterilise / sterilize
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
        "owner_name": "",
        "owner_phone": "",
        "last_asked": "",
        "lang": "",        # detected on first Spanish/English message; persists for session
    }


def _get_slots(session_id: str) -> dict:
    if session_id not in _slot_store:
        _slot_store[session_id] = _default_slots()
    return _slot_store[session_id]


def _detect_scheduling_intent(msg: str) -> bool:
    text = msg.lower()
    return any(k in text for k in SCHEDULING_KEYWORDS)


def _detect_heat(msg: str) -> bool:
    text = msg.lower()
    return any(k in text for k in HEAT_KEYWORDS)


def _is_info_question(msg: str) -> bool:
    """True when the message is a general info question, not an active booking request."""
    text = msg.lower()
    return any(re.search(p, text) for p in _INFO_BYPASS_PATTERNS)


_SPANISH_RE = re.compile(
    r"\b(quiero|para|cita|una|hola|mi\b|agendar|perra|perro|gata|gato|macho|hembra|peso|"
    r"nombre|teléfono|telefono|correo|llamo|soy|cuánto|cuanto|kilos?|gracias|buenos)\b",
    re.IGNORECASE,
)


def _detect_lang(msg: str) -> str:
    """Return 'es' if the message appears to be Spanish, otherwise 'en'."""
    return "es" if _SPANISH_RE.search(msg) else "en"


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
    # Gendered species words also imply sex: perra/gata → female
    if re.search(r"\b(perra|perras)\b", text):
        slots["sex"] = "female"
    if re.search(r"\b(gata|gatas)\b", text):
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
    if not slots["species"]:
        return "species"
    if not slots["sex"]:
        return "sex"
    if slots["species"] == "dog" and slots["sex"] == "female" and not slots["weight_kg"]:
        return "weight_kg"
    if not slots.get("owner_name"):
        return "owner_name"
    if not slots.get("owner_phone"):
        return "owner_phone"
    return None


_QUESTIONS: dict[str, dict[str, str]] = {
    "en": {
        "species":     "Is your pet a cat or a dog?",
        "sex":         "Is your pet male or female?",
        "weight_kg":   "Since she is a female dog, I need her weight in kg. How much does she weigh?",
        "owner_name":  "Almost there! Could I get your name to confirm the booking?",
        "owner_phone": "And your phone number or email so we can reach you?",
    },
    "es": {
        "species":     "¿Tu mascota es gato o perro?",
        "sex":         "¿Tu mascota es macho o hembra?",
        "weight_kg":   "Al ser perra, necesito su peso en kg para calcular el tiempo quirúrgico. ¿Cuánto pesa?",
        "owner_name":  "¡Casi listo! ¿Me puedes dar tu nombre para confirmar la cita?",
        "owner_phone": "¿Y tu número de teléfono o email para contactarte?",
    },
}


def _question_for_field(field: str, lang: str = "en") -> str:
    return _QUESTIONS.get(lang, _QUESTIONS["en"]).get(
        field, "Could you give me a bit more information?"
    )


def _render_availability_reply(result_json: str, slots: dict | None = None) -> str:
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

    appt_date = data.get("date", "")
    delivery = data.get("delivery_window", "")
    pickup = data.get("pickup_time", "")
    duration = data.get("surgery_duration_minutes", "")
    mode = data.get("mode", "")
    mode_note = " (disponibilidad real de calendario)" if mode == "real_calendly" else ""

    owner_name = slots.get("owner_name", "") if slots else ""
    owner_phone = slots.get("owner_phone", "") if slots else ""
    lead_line = ""
    if owner_name or owner_phone:
        lead_line = f" Cita registrada para {owner_name} — {owner_phone}."

    return (
        f"Excelente, he encontrado una fecha disponible{mode_note}: {appt_date}. "
        f"Trae a tu mascota en la ventana de entrega {delivery}. "
        f"La cirugia dura aproximadamente {duration} minutos y la recogida es {pickup}. "
        f"Recuerda ayuno de 8-12 horas (agua hasta 1-2 horas antes) y traer consentimiento firmado y documentacion."
        f"{lead_line}"
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
    # Detect language once and persist it for the session so short replies (names,
    # phone numbers) don't accidentally switch back to English.
    detected = _detect_lang(user_msg)
    if detected == "es" or not slots["lang"]:
        slots["lang"] = detected
    lang = slots["lang"]

    # Capture free-text answers for owner_name / owner_phone based on what was last asked.
    last_asked = slots.get("last_asked", "")
    if last_asked == "owner_name" and not slots["owner_name"]:
        slots["owner_name"] = user_msg.strip()
    elif last_asked == "owner_phone" and not slots["owner_phone"]:
        slots["owner_phone"] = user_msg.strip()

    _extract_slots(user_msg, slots)

    # Heat rejection: female dogs in heat cannot be booked — explain and reset flow.
    is_dog_context = slots["species"] == "dog" or bool(
        re.search(r"\b(dog|dogs|perro|perra|perros|perras)\b", user_msg.lower())
    )
    if is_dog_context and _detect_heat(user_msg):
        _slot_store[session_id] = _default_slots()
        if lang == "es":
            return (
                "Lo sentimos, no podemos agendar la esterilización mientras tu perra esté en celo. "
                "Las perras deben esperar al menos 2 meses tras el fin del celo antes de la cirugía "
                "(para evitar el riesgo de pseudogestación). ¡Contáctanos cuando llegue el momento!"
            )
        return (
            "I'm afraid we cannot schedule a sterilisation while your dog is in heat. "
            "Female dogs must wait at least 2 months after the end of the heat cycle "
            "before surgery (to avoid the risk of pseudopregnancy). "
            "Feel free to contact us again when the time is right!"
        )

    if _detect_scheduling_intent(user_msg):
        slots["in_flow"] = True
        # This clinic only does sterilisation — auto-fill service so we never ask for it.
        if not slots["service"]:
            slots["service"] = "sterilisation"

    # General info questions bypass the slot flow even if in_flow is True.
    if slots["in_flow"] and _is_info_question(user_msg):
        pass  # fall through to the LLM path below
    elif slots["in_flow"]:
        missing = _next_missing_field(slots)
        if missing:
            slots["last_asked"] = missing
            return _question_for_field(missing, lang)

        result = check_availability.invoke(
            {
                "species": slots["species"],
                "sex": slots["sex"],
                "weight_kg": float(slots["weight_kg"] or 0),
                "preferred_date": slots["preferred_date"],
            }
        )
        slots["in_flow"] = False
        slots["last_asked"] = ""
        return _render_availability_reply(result, slots)

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
