# Final Evidence Checklist (ENAE)

Use this checklist to capture final proof for the professor in a consistent format.

## 1) Base chatbot (Conversations 1-7)

- [ ] Run conversations 1-7 in the same `session_id`.
- [ ] Show memory behavior (species kept between turns).
- [ ] Show emergency redirect behavior (out of scope -> human/clinic).
- [ ] Save screenshots or chat transcript snippets.

Suggested format per conversation:

- Conversation: `#1` ... `#7`
- Input(s):
- Expected behavior:
- Observed output:
- Evidence file/link:

## 2) Tool availability (Conversations 8-9)

- [ ] Conversation 8 (cat) uses `check_availability`.
- [ ] Conversation 9 (dog) uses `check_availability`.
- [ ] Response includes domain constraints (delivery/pickup + surgery duration).
- [ ] Response shows `mode: real_calendly` when real slots are available.

Evidence fields:

- Tool call payload:
- Tool response JSON:
- Why result is coherent with Tetris rules:
- Screenshot or log:

## 3) RAG (Conversation 10)

- [ ] Ask a pre-op question grounded in the official URL.
- [ ] Verify answer includes instructions from the retrieved context.
- [ ] Save a short transcript and explain grounding signal.

Evidence fields:

- User question:
- Retrieved/grounded points:
- Final assistant answer:
- Screenshot or log:

## 4) Deploy and infrastructure

- [ ] Vercel URL responds on `/`.
- [ ] `POST /ask_bot` works in production.
- [ ] Env vars are configured in Vercel dashboard (not in repo).

Evidence fields:

- URL tested:
- Date/time:
- Result:

## 5) Jira and traceability

- [ ] Ticket for real calendar integration is closed (`EV-17`).
- [ ] Ticket enrichment comments exist (VET-1..VET-14 scope).
- [ ] Commit references project objective and delivered scope.

Evidence fields:

- Jira issue links:
  - `https://amxncio.atlassian.net/browse/EV-17`
- Commit hash(es):
- Notes:
