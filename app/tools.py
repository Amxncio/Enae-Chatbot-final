"""Availability tool — implements the Tetris scheduling algorithm with mock data."""

from __future__ import annotations

import json
from datetime import date, timedelta
from typing import Literal

from langchain_core.tools import tool

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


@tool
def check_availability(
    species: str,
    sex: str,
    weight_kg: float = 0.0,
    preferred_date: str = "",
) -> str:
    """Check available surgery dates for a pet sterilisation appointment.

    Args:
        species: "cat" or "dog"
        sex: "male" or "female"
        weight_kg: Weight in kg (required for female dogs to calculate surgery time)
        preferred_date: Optional preferred date in YYYY-MM-DD format
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

    start = date.today()
    if preferred_date:
        try:
            start = date.fromisoformat(preferred_date)
        except ValueError:
            pass

    available = _find_available_date(sp, surgery_min, start)

    if available is None:
        return json.dumps({
            "available": False,
            "message": "No available slots found in the next 14 days. Please call the clinic.",
        })

    window = DELIVERY_WINDOWS[sp]
    pickup = PICKUP_TIMES[sp]

    return json.dumps({
        "available": True,
        "date": available.isoformat(),
        "day_of_week": available.strftime("%A"),
        "surgery_duration_minutes": surgery_min,
        "delivery_window": window,
        "pickup_time": pickup,
        "fasting_instructions": (
            "Last meal 8-12 hours before surgery. "
            "Water allowed until 1-2 hours before."
        ),
        "reminder": (
            "Bring signed consent form and animal documentation "
            "(European passport or health card)."
        ),
    })
