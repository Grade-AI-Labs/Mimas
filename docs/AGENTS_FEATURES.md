# Agent Instructions: Feature Areas & Documentation

All feature documentation lives under **`docs/features/`**:

- **Area-level docs** (`docs/features/<area>.md`): concept-first overview of a feature area — responsibilities, boundaries, key concepts.
- **Per-service docs** (`docs/features/<area>/<service>.md`): API contracts, request/response schemas, implementation details, changelogs.

`openspec/specs/features/` is **deprecated**; `docs/features/` is the single source of truth.

This document defines how agents must detect, document, and maintain feature knowledge as the codebase grows.

> This file is part of the agent instruction infrastructure.
> Do NOT create, delete, or modify this file unless explicitly instructed.

---

## What is a feature area?

A feature area is a named concept that:
- appears in API routes, domain services, or handlers
- has dedicated logic under `src/domains/` or related layers
- represents a coherent responsibility or capability

Feature areas are identified **by naming and behavior**, not by folder structure alone. Hyperion is organized by domains (generative, azure-ai-services, token, public, shared); feature areas may map to a domain or cut across them.

Examples:
- generative (recruitment, learning, talent, shared)
- azure-ai-services (PII, language-detection)
- token (authentication)
- public (public endpoints)

---

## Feature Documentation Contract (MANDATORY)

### When to create or update area-level docs (`docs/features/<slug>.md`)

- New feature area introduced → create `docs/features/<slug>.md` and add to `docs/FEATURES.md` (alphabetical).
- Changes to **responsibilities, boundaries, workflows, or high-level behavior** → update the relevant `docs/features/<slug>.md` in the same task.

### When to create or update per-service docs (`docs/features/<area>/<service>.md`)

- **API contracts change** (endpoints, request/response schemas, versioning) → update the corresponding doc under `docs/features/<area>/` (e.g. `docs/features/generative/recruitment/job-ad-generation.md`).
- **New API or capability** → create a per-service doc and link it from the area doc.
- **Implementation details, PII handling, model config, testing locations** → keep in per-service docs.

### When an existing feature area changes

If a change affects any of the following, update the **appropriate** doc in the same task — not as a follow-up:

- public API behavior or contracts → per-service doc under `docs/features/<area>/`
- schemas or shared types → per-service doc (and feature index in `docs/FEATURES.md` if needed)
- invariants or business rules → area-level doc for behavioral summary; per-service doc if there is an explicit requirement or scenario

### When a feature is renamed, merged, or split

You MUST:
- Create or update the new feature doc(s)
- Add a short note near the top (e.g. "Renamed from …" or "Merged from …")
- Update `docs/FEATURES.md` as needed
- Optionally keep a stub doc pointing to the new one if helpful

---

## How to write feature docs

**Area-level docs (`docs/features/<area>.md`):**
- concept-first, not file-path-first
- responsibilities and boundaries
- key concepts and vocabulary
- links to per-service docs for API and implementation detail

**Per-service docs (`docs/features/<area>/<service>.md`):**
- API endpoint, request/response, business logic, technical implementation, testing, changelog
- Use [`docs/features/feature-template.md`](./features/feature-template.md) as the canonical template when creating a new per-service doc

### Avoid:
- Duplicating process rules (TDD, typecheck, etc.) in feature docs
- Listing volatile file paths unless they are stable

### Progressive disclosure

If a feature grows complex:
- Split deep detail into focused per-service docs under `docs/features/<area>/`
- Link to them from the area-level doc
- Do NOT duplicate large sections of content between area and per-service docs