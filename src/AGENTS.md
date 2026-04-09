# Source Package Instructions

This directory contains the Hyperion Fastify backend.

You MUST follow:
- Root TDD & typecheck rules (see `/AGENTS.md`)
- `docs/ENGINEERING.md` standards

Focus here on:
- API contracts & route definitions (`src/routes/`)
- Domain services & controllers (`src/domains/`)
- Validation & Fastify schemas
- Database correctness (Kysely migrations & queries)
- Security implications (API key auth, rate limiting)
- Generative AI services (LangChain, Langfuse, prompt management)

If a change introduces or modifies a feature area,
follow `docs/AGENTS_FEATURES.md`.