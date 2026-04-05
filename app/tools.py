"""Availability tool — Tetris rules + optional real Calendly availability (VET-13)."""

from __future__ import annotations

import json
import zoneinfo
from datetime import date, datetime, time, timedelta, timezone

import requests
from langchain_core.tools import tool

from app.config import (
    CALENDLY_EVENT_TYPE_CAT_URI,
    CALENDLY_EVENT_TYPE_DOG_URI,
    CALENDLY_TOKEN,
)

SURGERY_TIMES: dict[tuple[str, str, str], int] = {
    ("cat", "male", ""): 12,
    ("cat", "female", ""): 15,
    ("dog", "male", ""): 30,
    ("dog", "female", "0-10"): 45,
    ("dog", "female", "10-20"): 50,
    ("dog", "female", "20-30"): 60,
    ("dog", "female", "30-40"): 60,
    ("dog", "female", "40+"): 70,
}

DELIVERY_WINDOWS = {
    "cat": "08:00–09:00",
    "dog": "09:00–10:30",
}

PICKUP_TIMES = {
    "cat": "approximately 15:00 (1:30 PM)",
    "dog": "approximately 12:00 (noon)",
}

MAX_DAILY_MINUTES = 240
MAX_DOGS_PER_DAY = 2

CLINIC_TZ = zoneinfo.ZoneInfo("Europe/Madrid")

# Hour at which each species' delivery window opens.
# If the current local time is at or past this hour, today's slot is already gone.
_DELIVERY_CUTOFF_HOUR = {
    "cat": 8,   # cats: 08:00–09:00
    "dog": 9,   # dogs: 09:00–10:30
}


def _earliest_bookable_date(species: str) -> date:
    """Return today if the delivery window hasn't opened yet, otherwise tomorrow."""
    now = datetime.now(CLINIC_TZ)
    cutoff = _DELIVERY_CUTOFF_HOUR.get(species.lower(), 9)
    if now.hour >= cutoff:
        return now.date() + timedelta(days=1)
    return now.date()


def _build_mock_schedule() -> dict[str, dict]:
    """Generate a 3-week mock schedule starting from today, Mon–Thu only."""
    schedule: dict[str, dict] = {}
    patterns = [
        {"minutes_used": 90, "dogs": 1},
        {"minutes_used": 210, "dogs": 2},
        {"minutes_used": 42, "dogs": 0},
        {"minutes_used": 120, "dogs": 1},
        {"minutes_used": 0, "dogs": 0},
        {"minutes_used": 60, "dogs": 1},
        {"minutes_used": 0, "dogs": 0},
        {"minutes_used": 180, "dogs": 2},
    ]
    today = date.today()
    idx = 0
    for offset in range(21):
        d = today + timedelta(days=offset)
        if d.weekday() in (0, 1, 2, 3):
            schedule[d.isoformat()] = patterns[idx % len(patterns)]
            idx += 1
    return schedule


_mock_schedule = _build_mock_schedule()


def _weight_bucket(weight_kg: float) -> str:
    if weight_kg <= 10:
        return "0-10"
    if weight_kg <= 20:
        return "10-20"
    if weight_kg <= 30:
        return "20-30"
    if weight_kg <= 40:
        return "30-40"
    return "40+"


def _get_surgery_minutes(species: str, sex: str, weight_kg: float) -> int:
    sp = species.lower().strip()
    sx = sex.lower().strip()
    bucket = _weight_bucket(weight_kg) if sp == "dog" and sx == "female" else ""
    key = (sp, sx, bucket)
    return SURGERY_TIMES.get(key, 30)


def _is_operative_day(d: date) -> bool:
    return d.weekday() in (0, 1, 2, 3)  # Mon–Thu


def _find_available_date(
    species: str, surgery_minutes: int, start: date, max_lookahead: int = 14
) -> date | None:
    for offset in range(max_lookahead):
        candidate = start + timedelta(days=offset)
        if not _is_operative_day(candidate):
            continue
        key = candidate.isoformat()
        day_data = _mock_schedule.get(key, {"minutes_used": 0, "dogs": 0})
        if day_data["minutes_used"] + surgery_minutes > MAX_DAILY_MINUTES:
            continue
        if species.lower() == "dog" and day_data["dogs"] >= MAX_DOGS_PER_DAY:
            continue
        return candidate
    return None


def _calendly_event_type_for_species(species: str) -> str:
    return CALENDLY_EVENT_TYPE_CAT_URI if species == "cat" else CALENDLY_EVENT_TYPE_DOG_URI


def _to_iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _calendly_available_times(event_type_uri: str, from_day: date, lookahead_days: int = 14) -> list[dict]:
    """Fetch real Calendly availability slots.

    Docs: GET /event_type_available_times
    """
    if not CALENDLY_TOKEN or not event_type_uri:
        return []

    # Calendly requires:
    # 1) start_time/end_time in the future
    # 2) each query window <= 7 days
    now_utc = datetime.now(timezone.utc) + timedelta(minutes=5)
    requested_start = datetime.combine(from_day, time(0, 0), tzinfo=timezone.utc)
    cursor = max(now_utc, requested_start)
    hard_end = cursor + timedelta(days=lookahead_days)
    slots: list[dict] = []

    while cursor < hard_end:
        next_end = min(cursor + timedelta(days=7), hard_end)
        resp = requests.get(
            "https://api.calendly.com/event_type_available_times",
            headers={
                "Authorization": f"Bearer {CALENDLY_TOKEN}",
                "Content-Type": "application/json",
            },
            params={
                "event_type": event_type_uri,
                "start_time": _to_iso_z(cursor),
                "end_time": _to_iso_z(next_end),
            },
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        slots.extend(data.get("collection", []))
        cursor = next_end + timedelta(seconds=1)

    return slots


def _first_operational_calendly_slot(species: str, from_day: date) -> dict | None:
    event_type_uri = _calendly_event_type_for_species(species)
    slots = _calendly_available_times(event_type_uri, from_day)
    for slot in slots:
        start_at = slot.get("start_time")
        if not start_at:
            continue
        dt = datetime.fromisoformat(start_at.replace("Z", "+00:00"))
        d = dt.date()
        if _is_operative_day(d):
            return slot
    return None


@tool
def check_availability(
    species: str,
    sex: str,
    weight_kg: float = 0.0,
    preferred_date: str = "",
) -> str:
    """Check available surgery dates for a pet sterilisation appointment.

    Uses Tetris domain rules first; then tries real Calendly availability (VET-13).
    Falls back to mock data if Calendly credentials/config are missing.
    """
    sp = species.lower().strip()
    sx = sex.lower().strip()

    if sp not in ("cat", "dog"):
        return json.dumps({"error": "Species must be 'cat' or 'dog'."})
    if sx not in ("male", "female"):
        return json.dumps({"error": "Sex must be 'male' or 'female'."})
    if sp == "dog" and sx == "female" and weight_kg <= 0:
        return json.dumps({"error": "Weight in kg is required for female dogs."})

    surgery_min = _get_surgery_minutes(sp, sx, weight_kg)

    start = _earliest_bookable_date(sp)
    if preferred_date:
        try:
            requested = date.fromisoformat(preferred_date)
            # Never go back in time: use whichever is later
            start = max(start, requested)
        except ValueError:
            pass

    # Step 1: enforce domain constraints (Tetris) via local occupancy model
    local_candidate = _find_available_date(sp, surgery_min, start)
    if local_candidate is None:
        return json.dumps(
            {
                "available": False,
                "message": "No available slots found in the next 14 days according to clinic Tetris rules.",
            }
        )

    # Step 2: try real Calendly slot (VET-13)
    calendly_mode = bool(CALENDLY_TOKEN and _calendly_event_type_for_species(sp))
    calendly_slot = None
    calendly_error = None
    if calendly_mode:
        try:
            calendly_slot = _first_operational_calendly_slot(sp, local_candidate)
        except Exception as exc:  # noqa: BLE001
            calendly_error = str(exc)

    window = DELIVERY_WINDOWS[sp]
    pickup = PICKUP_TIMES[sp]

    if calendly_slot:
        start_time = calendly_slot.get("start_time")
        slot_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        real_date = slot_dt.date()
        return json.dumps(
            {
                "available": True,
                "mode": "real_calendly",
                "date": real_date.isoformat(),
                "day_of_week": real_date.strftime("%A"),
                "calendar_slot_start_utc": start_time,
                "surgery_duration_minutes": surgery_min,
                "delivery_window": window,
                "pickup_time": pickup,
                "fasting_instructions": "Last meal 8-12 hours before surgery. Water allowed until 1-2 hours before.",
                "reminder": "Bring signed consent form and animal documentation (European passport or health card).",
            }
        )

    # Step 3: fallback mock
    response = {
        "available": True,
        "mode": "mock_fallback",
        "date": local_candidate.isoformat(),
        "day_of_week": local_candidate.strftime("%A"),
        "surgery_duration_minutes": surgery_min,
        "delivery_window": window,
        "pickup_time": pickup,
        "fasting_instructions": "Last meal 8-12 hours before surgery. Water allowed until 1-2 hours before.",
        "reminder": "Bring signed consent form and animal documentation (European passport or health card).",
    }
    if not calendly_mode:
        response["note"] = "Calendly not configured; using mock availability."
    elif calendly_error:
        response["note"] = f"Calendly check failed; using mock availability. Error: {calendly_error}"
    else:
        response["note"] = "No Calendly slot found in window; using mock availability."

    return json.dumps(response)
