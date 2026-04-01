from app import bot


def test_detect_scheduling_intent():
    assert bot._detect_scheduling_intent("Quiero una cita")
    assert not bot._detect_scheduling_intent("Que cuidados postoperatorios hay?")


def test_extract_slots_species_sex_weight():
    slots = bot._default_slots()
    bot._extract_slots("Tengo una perra hembra de 12 kg", slots)
    assert slots["species"] == "dog"
    assert slots["sex"] == "female"
    assert slots["weight_kg"] == 12.0


def test_guided_flow_asks_missing_fields_in_order():
    sid = "test-guided-order"
    bot._slot_store.pop(sid, None)

    r1 = bot.ask("Quiero una cita", sid)
    assert "servicio" in r1.lower() or "esterilizacion" in r1.lower()

    r2 = bot.ask("Si, esterilizacion", sid)
    assert "gato o perro" in r2.lower()

    r3 = bot.ask("Perra", sid)
    assert "macho o hembra" in r3.lower()

    r4 = bot.ask("Hembra", sid)
    assert "peso" in r4.lower()


def test_guided_flow_calls_tool_when_required_data_is_complete(monkeypatch):
    sid = "test-guided-complete"
    bot._slot_store.pop(sid, None)

    class FakeTool:
        @staticmethod
        def invoke(payload):
            return (
                '{"available": true, "mode": "real_calendly", "date": "2026-04-03", '
                '"delivery_window": "09:00-10:30", "pickup_time": "approximately 12:00 (noon)", '
                '"surgery_duration_minutes": 45}'
            )

    monkeypatch.setattr(bot, "check_availability", FakeTool())

    bot.ask("Quiero una cita", sid)
    bot.ask("Esterilizacion", sid)
    bot.ask("Perra", sid)
    bot.ask("Hembra", sid)
    final = bot.ask("12 kg", sid)

    assert "2026-04-03" in final
    assert "45" in final
