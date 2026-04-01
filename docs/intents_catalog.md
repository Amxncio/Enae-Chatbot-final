# Intents — Veterinary Chatbot Catalog

## 20 Intents

| # | Intent ID | Description | Example user message |
|---|-----------|-------------|---------------------|
| 1 | `greeting` | User greets the bot | "Hello", "Hi there" |
| 2 | `ask_scope` | User asks what the bot can help with | "What can you do?" |
| 3 | `ask_delivery_window` | User asks about drop-off times by species | "When should I bring my cat?" |
| 4 | `ask_pickup_time` | User asks about pick-up times after surgery | "What time can I pick up my dog?" |
| 5 | `ask_preop_bloodwork` | User asks about pre-operative blood tests | "Does my cat need a blood test before surgery?" |
| 6 | `emergency_triage` | User reports an emergency or urgent situation | "My dog is bleeding, help!" |
| 7 | `heat_rejection` | User mentions their female dog is in heat | "My dog is in heat, can she be sterilised?" |
| 8 | `human_handoff` | User asks to speak with a human | "Can I talk to someone?" |
| 9 | `check_availability` | User wants to check available dates | "Are there any free slots next week?" |
| 10 | `book_appointment` | User wants to book a sterilisation appointment | "I'd like to schedule my cat's neutering" |
| 11 | `ask_fasting` | User asks about fasting instructions | "What about food before the operation?" |
| 12 | `ask_extras` | User asks about microchip or rabies vaccine | "Can you do the microchip during surgery?" |
| 13 | `ask_procedure_info` | User asks what sterilisation involves | "What exactly is a spay?" |
| 14 | `ask_medication` | User asks about post-surgery medication | "What medication will my cat need?" |
| 15 | `ask_recovery` | User asks about post-surgery recovery care | "How should I care for my dog after?" |
| 16 | `ask_cost` | User asks about pricing or fees | "How much does it cost?" |
| 17 | `ask_cancel_policy` | User asks about cancellation rules | "What if I can't make the appointment?" |
| 18 | `ask_vaccination` | User asks about vaccination requirements | "Does my dog need to be vaccinated first?" |
| 19 | `confirm_booking` | User confirms a proposed appointment | "Yes, that date works" |
| 20 | `farewell` | User says goodbye | "Thanks, bye!" |

## Conversation → Intents mapping

| Conv. | Topic | Intents triggered |
|-------|-------|-------------------|
| 1 | Greeting and bot scope | `greeting`, `ask_scope` |
| 2 | Delivery windows (cat vs dog), memory of species | `book_appointment`, `ask_delivery_window`, `ask_pickup_time` |
| 3 | Pre-operative blood test (>6 years) | `book_appointment`, `ask_preop_bloodwork` |
| 4 | Emergency → triage, out of scope | `emergency_triage` |
| 5 | Booking impossible (dog in heat) → rejection | `book_appointment`, `heat_rejection` |
| 6 | Pick-up times (dog vs cat) | `ask_pickup_time`, `ask_delivery_window` |
| 7 | Human handoff | `human_handoff` |
| 8 | Check availability with tool (cat) | `book_appointment`, `check_availability`, `confirm_booking`, `ask_fasting` |
| 9 | Check availability with tool (dog) | `book_appointment`, `check_availability`, `confirm_booking`, `ask_extras` |
| 10 | RAG-based pre-surgery questions | `ask_procedure_info`, `ask_fasting`, `ask_recovery`, `ask_medication` |
