# SDD Project Rules

## Repository

- **GitHub repo:** [https://github.com/Amxncio/Enae-Chatbot-final](https://github.com/Amxncio/Enae-Chatbot-final)
- **Main branch:** `main`
- **Convention:** Feature branches named `feature/VET-XX-short-description`

## Jira Board

- **Jira project:** [https://amxncio.atlassian.net/jira/software/projects/EV/boards/34](https://amxncio.atlassian.net/jira/software/projects/EV/boards/34)
- **Project key:** VET
- **EPICs:** SET UP, SDD / CONTEXT, CHATBOT

## Rules

1. **Always include the repository** in the working context of the AI assistant (Cursor).
2. **Always include the Jira board** — every implementable story links repo ↔ Jira.
3. **Never close an implementation** without updating or referencing the corresponding Jira ticket.
4. The `enrich` and `implement` commands (see below) must cite this document as their source of norms.
5. **No secrets in commits** — use `.env` locally and Vercel panel for production.
6. **One ticket = one front** — at closing, README/Jira updated and commit in repo.

## Commands

### `enrich` (VET-5)

Documented in `.cursor/rules/enrich.mdc`. Takes a skeletal ticket and expands it with:
- Acceptance criteria
- Risks and dependencies
- References to veterinary domain (Tetris rules, intents)

### `implement` (VET-6)

Documented in `.cursor/rules/implement.mdc`. Takes a ticket/spec and guides implementation with:
- Spec-first approach (read spec, then code)
- Context: backend engineer, frontend engineer, PM skills
- Cross-reference to VET-4 (this document)

## Team

| Role | Member |
|------|--------|
| Developer + PM | Amancio |
| Professor | Jaime Marco (`jmarco111` on GitHub) |
