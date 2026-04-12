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
from app.tools import create_booking

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
    r"when should i bring",
    r"bring my",
    r"drop[- ]?off",
    r"surgery day",
    r"blood test",
    r"pre[- ]?op",
    r"years old",
    r"how old",
    r"bleeding",
    r"injury",
    r"injured",
    r"emergency",
    r"urgent",
    r"spayed",
    r"spay next",
    r"sterilis",
    r"can she be",
    r"can he be",
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
    r"anal[ií]tic",
    r"does she need",
    r"does my",
    r"does he need",
]

_HUMAN_HANDOFF_PATTERNS = [
    r"i need to speak",
    r"speak with a human",
    r"talk to",
    r"transfer me",
    r"\bhuman\b",
    r"hablar con",
    r"habla con",
    r"persona humana",
    r"humano",
]

SERVICE_KEYWORDS = (
    "esteril",
    "steril",
    "castra",
    "spay",
    "neuter",
    "vacun",
    "vaccination",
    "vaccine",
    "microchip",
    "chip",
)


def _default_slots() -> dict:
    return {
        "in_flow": False,
        "service": "",         # sterilisation | vaccination | microchip
        "species": "",         # cat | dog
        "pet_name": "",        # name of the animal
        "sex": "",             # male | female
        "age_years": None,     # integer — needed for blood-test rule (>6 years)
        "weight_kg": None,     # float — needed for female dogs only
        "preferred_date": "",
        "owner_name": "",
        "owner_phone": "",
        "last_asked": "",
        "lang": "",
        "awaiting_confirm": False,
    }


def _get_slots(session_id: str) -> dict:
    if session_id not in _slot_store:
        _slot_store[session_id] = _default_slots()
    return _slot_store[session_id]


_ALLOWED_SLOT_KEYS = frozenset(_default_slots().keys())


def apply_slots_from_client(session_id: str, data: dict | None) -> None:
    """Restore slot state from the client (needed on Vercel: each request may be a cold instance)."""
    if not data or not isinstance(data, dict):
        return
    slots = _default_slots()
    for k in _ALLOWED_SLOT_KEYS:
        if k in data:
            slots[k] = data[k]
    _slot_store[session_id] = slots


def export_slots_for_client(session_id: str) -> dict:
    """Return a JSON-serializable copy of slots for the client to send on the next request."""
    s = _get_slots(session_id)
    return {k: s[k] for k in _ALLOWED_SLOT_KEYS}


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


def _is_human_handoff(msg: str) -> bool:
    """True when the user explicitly asks to speak with a human."""
    text = msg.lower()
    return any(re.search(p, text) for p in _HUMAN_HANDOFF_PATTERNS)


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

    # Service detection — explicit keywords take priority over auto-fill
    if re.search(r"\b(vacun|vaccination|vaccine|vacuna)\w*", text):
        slots["service"] = "vaccination"
    elif re.search(r"\b(microchip|chip)\b", text):
        slots["service"] = "microchip"
    elif any(k in text for k in ("esteril", "steril", "castra", "spay", "neuter")):
        slots["service"] = "sterilisation"

    if re.search(r"\b(cat|cats|gato|gata|gatos|gatas)\b", text):
        slots["species"] = "cat"
    elif re.search(r"\b(dog|dogs|perro|perra|perros|perras)\b", text):
        slots["species"] = "dog"

    if re.search(r"\b(male|macho)\b", text):
        slots["sex"] = "male"
    elif re.search(r"\b(female|hembra)\b", text):
        slots["sex"] = "female"
    # Gendered species words also imply sex
    if re.search(r"\b(perra|perras)\b", text):
        slots["sex"] = "female"
    if re.search(r"\b(gata|gatas)\b", text):
        slots["sex"] = "female"

    # Age extraction: "3 años", "3 years", "3 years old", "tiene 3", "aged 3"
    age_match = re.search(
        r"\b(\d{1,2})\s*(?:años?|years?(?:\s+old)?)\b"
        r"|\b(?:tiene|aged?|has)\s+(\d{1,2})\b",
        text,
    )
    if age_match:
        raw_age = age_match.group(1) or age_match.group(2)
        try:
            slots["age_years"] = int(raw_age)
        except (ValueError, TypeError):
            pass

    # Weight: kg only (not shared with age)
    weight_match = re.search(r"\b(\d{1,3}(?:[.,]\d{1,2})?)\s*(?:kg|kgs|kilos?)\b", text)
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
    if not slots.get("pet_name"):
        return "pet_name"
    if not slots["sex"]:
        return "sex"
    if slots["age_years"] is None:
        return "age_years"
    if slots["species"] == "dog" and slots["sex"] == "female" and not slots["weight_kg"]:
        return "weight_kg"
    if not slots.get("owner_name"):
        return "owner_name"
    if not slots.get("owner_phone"):
        return "owner_phone"
    return None


_QUESTIONS: dict[str, dict[str, str]] = {
    "en": {
        "service":     "What service do you need?\n(1) Sterilisation/neutering\n(2) Vaccination\n(3) Microchip",
        "species":     "Is your pet a cat or a dog?",
        "pet_name":    "What's your pet's name?",
        "sex":         "Is {pet_name} male or female?",
        "age_years":   "How old is {pet_name}? (in years)",
        "weight_kg":   "How much does {pet_name} weigh? (kg)",
        "owner_name":  "Almost there! Could I get your name to confirm the booking?",
        "owner_phone": "And your phone number or email so we can reach you?",
    },
    "es": {
        "service":     "¿Qué servicio necesitas?\n(1) Esterilización/castración\n(2) Vacunación\n(3) Microchip",
        "species":     "¿Tu mascota es gato o perro?",
        "pet_name":    "¿Cómo se llama tu mascota?",
        "sex":         "¿{pet_name} es macho o hembra?",
        "age_years":   "¿Cuántos años tiene {pet_name}?",
        "weight_kg":   "¿Cuánto pesa {pet_name}? (kg)",
        "owner_name":  "¡Casi listo! ¿Me puedes dar tu nombre para confirmar la cita?",
        "owner_phone": "¿Y tu número de teléfono o email para contactarte?",
    },
}


def _question_for_field(field: str, lang: str = "en", slots: dict | None = None) -> str:
    template = _QUESTIONS.get(lang, _QUESTIONS["en"]).get(
        field, "Could you give me a bit more information?"
    )
    pet_name = (slots or {}).get("pet_name") or ("your pet" if lang == "en" else "tu mascota")
    return template.replace("{pet_name}", pet_name)


_YES_RE = re.compile(
    r"\b(yes|sí|si|confirm|confirmar|confirmo|ok|dale|adelante|correcto|claro|proceed)\b",
    re.IGNORECASE,
)
_NO_RE = re.compile(
    r"\b(no|nope|cancel|cancelar|cancelo|negativo)\b",
    re.IGNORECASE,
)


def _is_affirmative(msg: str) -> bool:
    return bool(_YES_RE.search(msg))


def _is_negative(msg: str) -> bool:
    return bool(_NO_RE.search(msg))


def _confirmation_card(slots: dict) -> str:
    es = slots["lang"] == "es"

    species_label = {
        ("cat", "male"):   "Gato (macho)"   if es else "Cat (male)",
        ("cat", "female"): "Gata (hembra)"  if es else "Cat (female)",
        ("dog", "male"):   "Perro (macho)"  if es else "Dog (male)",
        ("dog", "female"): "Perra (hembra)" if es else "Dog (female)",
    }.get((slots["species"], slots["sex"]), slots["species"])

    age = slots.get("age_years")
    age_line = (f"\n🎂 Edad: {age} años" if es else f"\n🎂 Age: {age} years") if age else ""

    weight_line = ""
    if slots["weight_kg"]:
        weight_line = (
            f"\n⚖️ Peso: {slots['weight_kg']} kg"
            if es else f"\n⚖️ Weight: {slots['weight_kg']} kg"
        )

    blood_test_warning = ""
    if age and age > 6:
        blood_test_warning = (
            "\n\n⚠️ *Analítica preoperatoria obligatoria* — tu mascota tiene más de 6 años."
            if es else
            "\n\n⚠️ *Mandatory pre-op blood test* — your pet is over 6 years old."
        )

    pet_name = slots.get("pet_name", "")
    pet_name_line = (f"\n🏷️ Nombre: {pet_name}" if es else f"\n🏷️ Name: {pet_name}") if pet_name else ""

    if es:
        return (
            "📋 *Confirmemos la cita*\n\n"
            f"👤 Nombre del dueño/a: {slots['owner_name']}\n"
            f"📞 Contacto: {slots['owner_phone']}\n"
            f"🐶 Animal: {species_label}"
            f"{pet_name_line}"
            f"{age_line}"
            f"{weight_line}\n"
            f"💉 Servicio: Esterilización"
            f"{blood_test_warning}\n\n"
            "¿Quieres confirmar la cita? (sí / no)"
        )
    return (
        "📋 *Appointment Summary*\n\n"
        f"👤 Owner: {slots['owner_name']}\n"
        f"📞 Contact: {slots['owner_phone']}\n"
        f"🐶 Animal: {species_label}"
        f"{pet_name_line}"
        f"{age_line}"
        f"{weight_line}\n"
        f"💉 Service: Sterilisation"
        f"{blood_test_warning}\n\n"
        "Shall I confirm this appointment? (yes / no)"
    )


def _render_booking_reply(result_json: str, slots: dict | None = None) -> str:
    """Render the final booking confirmation message (GCal link omitted; errors still surfaced)."""
    try:
        data = json.loads(result_json)
    except json.JSONDecodeError:
        return "Hubo un problema al registrar la cita. Por favor llama a la clínica."

    es = (slots or {}).get("lang") == "es"

    if not data.get("booked"):
        msg = data.get("message", "")
        return (
            f"Lo sentimos, no hay hueco disponible en los próximos días. {msg} Por favor llama a la clínica."
            if es else
            f"Sorry, no slots available in the coming days. {msg} Please call the clinic."
        )

    appt_date   = data.get("date", "")
    day_of_week = data.get("day_of_week", "")
    delivery    = data.get("delivery_window", "")
    pickup      = data.get("pickup_time", "")
    duration    = data.get("surgery_duration_minutes", "")
    pet         = data.get("pet_name", "")
    owner       = data.get("owner_name", "")
    gcal_err = (data.get("gcal_error") or "").strip()

    pet_ref = f" para {pet}" if pet else ""
    mode_note = " (calendario real)" if data.get("mode") == "real_calendly" else ""

    # El evento se crea en GCal igualmente; no mostramos el enlace largo en el chat.
    gcal_line = ""
    if gcal_err:
        # Ayuda a depurar en Vercel (403 = permisos, JSON inválido = pegado mal en env)
        hint = gcal_err[:350] + ("…" if len(gcal_err) > 350 else "")
        gcal_line = (
            f"\n\n⚠️ **No se pudo crear el evento en Google Calendar:** {hint}"
            if es else
            f"\n\n⚠️ **Google Calendar event was not created:** {hint}"
        )

    if es:
        return (
            f"✅ ¡Cita registrada{pet_ref}{mode_note}!\n\n"
            f"📆 Fecha: {day_of_week} {appt_date}\n"
            f"🚗 Entrega: {delivery}\n"
            f"🏠 Recogida: {pickup}\n"
            f"⏱️ Duración cirugía: {duration} min\n"
            f"👤 Titular: {owner}\n\n"
            "🍽️ Recuerda el ayuno de 8–12 h (agua hasta 1–2 h antes) y trae el "
            "consentimiento firmado y la documentación del animal."
            f"{gcal_line}"
        )
    return (
        f"✅ Appointment confirmed{pet_ref}{mode_note}!\n\n"
        f"📆 Date: {day_of_week} {appt_date}\n"
        f"🚗 Drop-off window: {delivery}\n"
        f"🏠 Pick-up: {pickup}\n"
        f"⏱️ Surgery duration: {duration} min\n"
        f"👤 Owner: {owner}\n\n"
        "🍽️ Remember: fast 8–12 h before surgery (water OK until 1–2 h before). "
        "Bring signed consent form and animal documentation."
        f"{gcal_line}"
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

    # No tool binding on the LLM path: conv. 1–7 must never trigger check_availability
    # from the model. Booking uses create_booking in the guided slot flow; availability
    # logic is covered by tests invoking check_availability directly.
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{context}\n\nUser: {input}"),
    ])

    chain = prompt | llm

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

    # Human handoff is a hard requirement: resolve it directly and avoid tool calls.
    if _is_human_handoff(user_msg):
        slots["in_flow"] = False
        slots["awaiting_confirm"] = False
        slots["last_asked"] = ""
        return (
            "Perfecto, te paso con una persona de la clínica para continuar la gestión."
            if lang == "es"
            else "Sure, I will transfer you to a member of the clinic team."
        )

    # Capture free-text / numeric answers based on what was last asked.
    last_asked = slots.get("last_asked", "")
    if last_asked == "pet_name" and not slots.get("pet_name"):
        slots["pet_name"] = user_msg.strip().capitalize()
    elif last_asked == "service" and not slots["service"]:
        t = user_msg.strip().lower()
        if t in ("1", "esterilización", "esterilizacion", "castración", "castracion",
                 "sterilisation", "sterilization", "spay", "neuter"):
            slots["service"] = "sterilisation"
        elif t in ("2", "vacunación", "vacunacion", "vaccination", "vaccine", "vacuna"):
            slots["service"] = "vaccination"
        elif t in ("3", "microchip", "chip"):
            slots["service"] = "microchip"
    elif last_asked == "age_years" and slots["age_years"] is None:
        age_match = re.search(r"\b(\d{1,2})\b", user_msg)
        if age_match:
            try:
                slots["age_years"] = int(age_match.group(1))
            except ValueError:
                pass
    elif last_asked == "owner_name" and not slots["owner_name"]:
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

    # If service was resolved to a non-sterilisation option, exit slot flow and
    # let the LLM handle it (vaccination / microchip are simpler, no Tetris needed).
    if slots["in_flow"] and slots["service"] in ("vaccination", "microchip"):
        slots["in_flow"] = False
        slots["awaiting_confirm"] = False

    # General info questions bypass slot questions even if in_flow is True (conv. 1–7).
    if slots.get("awaiting_confirm"):
        # User has seen the confirmation card — wait for yes/no.
        if _is_negative(user_msg):
            _slot_store[session_id] = _default_slots()
            return (
                "De acuerdo, cita cancelada. ¡Cuando quieras la retomamos!"
                if lang == "es"
                else "No problem — booking cancelled. Come back whenever you're ready!"
            )
        if _is_affirmative(user_msg):
            slots["awaiting_confirm"] = False
            result = create_booking.invoke(
                {
                    "species": slots["species"],
                    "sex": slots["sex"],
                    "weight_kg": float(slots["weight_kg"] or 0),
                    "preferred_date": slots["preferred_date"],
                    "owner_name": slots.get("owner_name", ""),
                    "owner_phone": slots.get("owner_phone", ""),
                    "pet_name": slots.get("pet_name", ""),
                }
            )
            slots["in_flow"] = False
            slots["last_asked"] = ""
            return _render_booking_reply(result, slots)
        # Unrecognised response — ask again.
        return (
            "¿Confirmas la cita? Responde *sí* o *no*."
            if lang == "es"
            else "Please reply *yes* to confirm or *no* to cancel."
        )
    elif slots["in_flow"] and not _is_info_question(user_msg):
        missing = _next_missing_field(slots)
        if missing:
            slots["last_asked"] = missing
            return _question_for_field(missing, lang, slots)

        # All data collected — show confirmation card before booking.
        slots["awaiting_confirm"] = True
        slots["in_flow"] = False
        return _confirmation_card(slots)

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

        return response.content if hasattr(response, "content") else str(response)

    except Exception as e:
        return f"I encountered an error: {e}"
