# api-contract-sync

Stop hand-writing frontend types for a backend that already knows its own shape.

```bash
/plugin install api-contract-sync@llm-utils
```

## The problem

When frontend and backend are different languages, the API contract exists twice. Nothing
keeps the copies equal except discipline.

Rename a field in a Pydantic model; the frontend interface still has the old name.
TypeScript is perfectly happy — it is type-checking against a lie. The failure surfaces at
runtime as `undefined`.

**Hand-written client types do not catch API drift. They hide it.**

## The approach

```
FastAPI models ──► openapi.json ──► generated TS types ──► typed client
   (source of truth)                   (never edited)
```

One direction. The backend owns the contract. Commit `openapi.json` so contract changes
show up as diff lines in review — the moment a breaking change is cheapest to catch.

Then verify in CI: regenerate, fail on a diff. Generation you have to remember is
generation that stops happening within a month.

## What it does not cover

Generated types describe **shape**, not behaviour — and **SSE is a real gap**. OpenAPI
describes a streaming endpoint as returning a string, so event names and payloads must be
typed by hand. The skill covers how to keep that pairing honest.
