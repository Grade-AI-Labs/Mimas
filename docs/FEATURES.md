# Feature Areas

This index represents the known feature areas in the system.

It must stay accurate as new features are introduced, renamed, merged, or removed.

---

## Feature list (alphabetical)

- [azure-ai-services](./features/azure-ai-services.md) — PII, language detection
- [generative](./features/generative.md) — AI content generation (recruitment, learning, talent, shared, feedback)
- [public](./features/public.md) — documentation page, OpenAPI JSON, health check
- [test](./features/test.md) — test endpoint for prompt/runnable experiments
- [token](./features/token.md) — JWT authentication

Each area doc links to per-service documentation under `docs/features/<area>/`.

For a full inventory of generative services, see [generative domain features map](./features/generative/generative-domain-features.md).

---

## Rules for agents

- Introducing a new feature area requires:
  - creating `docs/features/<feature>.md`
  - adding it to this list (alphabetical)
- Per-service docs live under `docs/features/<area>/` and are linked from the area doc
- Renaming or merging features requires updating links and notes
- This file should remain concise and navigable