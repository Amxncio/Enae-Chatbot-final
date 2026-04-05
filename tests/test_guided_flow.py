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
    assert "servicio" in r1.lower() or "esteriliz" in r1.lower()

    r2 = bot.ask("1", sid)
    assert "gato o perro" in r2.lower()

    # "perra" infiere especie + sexo → siguiente paso es nombre de mascota
    r3 = bot.ask("Perra", sid)
    assert "llama" in r3.lower() or "nombre" in r3.lower()

    r4 = bot.ask("Luna", sid)
    assert "años" in r4.lower() or "cuántos" in r4.lower()

    r5 = bot.ask("3 años", sid)
    assert "peso" in r5.lower() or "kg" in r5.lower()


def test_guided_flow_calls_create_booking_on_confirm(monkeypatch):
    sid = "test-guided-complete"
    bot._slot_store.pop(sid, None)

    class FakeCreateBooking:
        @staticmethod
        def invoke(payload):
            return (
                '{"booked": true, "mode": "mock_fallback", "date": "2026-04-03", '
                '"day_of_week": "Thursday", "delivery_window": "09:00–10:30", '
                '"pickup_time": "approximately 12:00 (noon)", '
                '"surgery_duration_minutes": 45, "gcal_event_link": null, '
                '"gcal_error": ""}'
            )

    monkeypatch.setattr(bot, "create_booking", FakeCreateBooking())

    # Gato macho: sin peso; flujo hasta tarjeta + sí → create_booking
    bot.ask("Quiero una cita", sid)
    bot.ask("1", sid)
    bot.ask("gato", sid)
    bot.ask("Miau", sid)
    bot.ask("macho", sid)
    bot.ask("2 años", sid)
    bot.ask("Ana Test", sid)
    bot.ask("600000000", sid)
    final = bot.ask("sí", sid)

    assert "2026-04-03" in final
    assert "45" in final
