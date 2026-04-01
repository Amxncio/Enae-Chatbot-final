import json
from unittest.mock import patch

from app.tools import check_availability


def _invoke(payload: dict) -> dict:
    raw = check_availability.invoke(payload)
    return json.loads(raw)


def test_invalid_species_returns_error():
    result = _invoke({"species": "bird", "sex": "male", "weight_kg": 1})
    assert "error" in result


def test_female_dog_requires_weight():
    result = _invoke({"species": "dog", "sex": "female", "weight_kg": 0})
    assert "error" in result
    assert "Weight" in result["error"]


@patch("app.tools.CALENDLY_TOKEN", "")
def test_mock_fallback_when_calendly_not_configured():
    result = _invoke({"species": "cat", "sex": "female", "weight_kg": 4})
    assert result["available"] is True
    assert result["mode"] == "mock_fallback"


@patch("app.tools._first_operational_calendly_slot")
@patch("app.tools.CALENDLY_TOKEN", "token")
@patch("app.tools.CALENDLY_EVENT_TYPE_CAT_URI", "https://api.calendly.com/event_types/cat")
def test_real_calendly_mode_when_slot_exists(mock_slot):
    mock_slot.return_value = {"start_time": "2026-04-01T17:00:00Z"}
    result = _invoke({"species": "cat", "sex": "female", "weight_kg": 4})
    assert result["available"] is True
    assert result["mode"] == "real_calendly"
    assert result["calendar_slot_start_utc"] == "2026-04-01T17:00:00Z"
