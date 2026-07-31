---
name: api-contract-sync
description: Keep a typed backend and its frontend client in sync by generating TypeScript types from an OpenAPI schema and failing CI when they drift. Use when frontend and backend types disagree, when adding an endpoint, when a runtime error comes from a response shape the client did not expect, or when setting up codegen for FastAPI, NestJS, or any OpenAPI-producing backend.
---

# API Contract Sync

When the backend and frontend are different languages, the API contract exists twice: once
in the server's models and once in the client's types. Nothing keeps them equal except
discipline, and discipline loses.

The fix is to stop writing the second one. Generate it.

## The failure this prevents

A field is renamed in a Pydantic model. The frontend's hand-written interface still has the
old name. TypeScript is perfectly happy — it is checking against a lie. The error appears
at runtime, as `undefined`, in whatever component happened to read that field.

**Hand-written client types do not catch API drift. They hide it.** Type safety against a
fiction is worse than no type safety, because it removes the suspicion that would otherwise
make you check.

## Approach

```
FastAPI models ──► /openapi.json ──► generated TS types ──► typed client
     (source of truth)                    (never edited by hand)
```

One direction only. The backend owns the contract; the frontend consumes it. Bidirectional
sync has no single source of truth and drifts in both directions.

### 1. Export the schema

```bash
python -c "
import json
from app.main import app
print(json.dumps(app.openapi(), indent=2))
" > openapi.json
```

Commit `openapi.json`. It makes contract changes **visible in review** — a renamed field
shows up as a diff line, which is exactly the moment to notice it.

### 2. Generate types

```bash
npx openapi-typescript openapi.json -o frontend/src/lib/api-types.ts
```

`openapi-typescript` emits types only, no runtime — a good default because it adds nothing
to the bundle. If you also want a runtime client, `openapi-fetch` pairs with it and stays
small.

Mark the output as generated so nobody edits it:

```ts
/**
 * GENERATED FILE — DO NOT EDIT.
 * Regenerate: npm run api:generate
 */
```

Add it to `.gitattributes` so reviews are not drowned in generated diff:

```
frontend/src/lib/api-types.ts linguist-generated=true
```

### 3. Use the generated types

```ts
import type { paths, components } from "./api-types";

type Quest = components["schemas"]["Quest"];
type QuestListResponse =
  paths["/api/v1/campaigns/{cid}/quests"]["get"]["responses"]["200"]["content"]["application/json"];

export async function listQuests(campaignId: string): Promise<QuestListResponse> {
  const res = await fetch(`/api/v1/campaigns/${campaignId}/quests`);
  if (!res.ok) throw new ApiError(res);
  return res.json();
}
```

Now renaming a backend field breaks the **build**, not production.

### 4. Detect drift in CI

Generation only helps if it is not forgotten. Regenerate in CI and fail on a diff:

```bash
#!/usr/bin/env bash
# scripts/check-api-drift.sh
set -euo pipefail

python -c "import json; from app.main import app; print(json.dumps(app.openapi(), indent=2))" \
  > /tmp/openapi-current.json

if ! diff -q openapi.json /tmp/openapi-current.json >/dev/null; then
  echo "openapi.json is stale. Run: npm run api:generate"
  diff openapi.json /tmp/openapi-current.json | head -40
  exit 1
fi

npx openapi-typescript openapi.json -o /tmp/api-types.ts
if ! diff -q frontend/src/lib/api-types.ts /tmp/api-types.ts >/dev/null; then
  echo "Generated types are stale. Run: npm run api:generate"
  exit 1
fi

echo "API contract in sync."
```

This is the step that makes the rest hold. Without it, the schema silently rots and you are
back to hand-written types with extra ceremony.

## Making the schema worth generating from

Generated types are only as good as the schema. FastAPI produces a poor one by default
unless you help it.

**Declare response models.** Without `response_model`, the schema says the endpoint returns
"something".

```python
@router.get("/quests", response_model=list[Quest])
async def list_quests(campaign_id: str) -> list[Quest]: ...
```

**Name your models.** Generated type names come from Pydantic class names. `QuestCreate`
and `QuestResponse` generate readable types; `Model1` does not.

**Declare error shapes.** Clients need them as much as success shapes:

```python
@router.get("/quests/{id}", response_model=Quest,
            responses={404: {"model": ErrorResponse}})
```

**Set `operation_id`** if your generator derives function names from it — FastAPI's default
is verbose and changes when you rename a handler.

**Use enums, not bare strings.** `status: QuestStatus` generates a union type the frontend
can exhaust-check; `status: str` generates `string` and loses the constraint.

```python
class QuestStatus(str, Enum):
    available = "available"
    inprogress = "inprogress"
    completed = "completed"
```

That single change turns a whole class of typo bug into a compile error.

## What generation does not cover

Be honest about the boundary. Generated types describe **shape**, not **behaviour**:

| Covered | Not covered |
|---------|-------------|
| Field names and types | Which fields are meaningful together |
| Required versus optional | Semantic validation rules |
| Enum values | Ordering and pagination behaviour |
| Status codes declared | Error semantics and retry safety |
| — | **Streaming endpoints (SSE)** |

**SSE is the notable gap.** OpenAPI describes an SSE endpoint as returning a string. Event
names and payloads must be typed by hand and kept in sync deliberately:

```ts
// hand-maintained — OpenAPI cannot express this
export type StreamEvent =
  | { event: "token";    data: { text: string } }
  | { event: "tool";     data: { label: string; status: "running" | "done" } }
  | { event: "citation"; data: { chunkId: number; filename: string } }
  | { event: "done";     data: { messageId: number } }
  | { event: "error";    data: { message: string; recoverable: boolean } };
```

Keep this next to the server's event emitter and note in both places that they are paired.
A test that asserts every emitted event name appears in the union is cheap and catches
drift.

## Workflow

Add scripts so nobody has to remember the commands:

```jsonc
{
  "scripts": {
    "api:export":   "cd backend && python -c \"import json; from app.main import app; print(json.dumps(app.openapi(), indent=2))\" > ../openapi.json",
    "api:generate": "npm run api:export && openapi-typescript openapi.json -o frontend/src/lib/api-types.ts",
    "api:check":    "./scripts/check-api-drift.sh"
  }
}
```

Then: change a model → `npm run api:generate` → commit both the schema and the types with
the backend change. One commit, one contract.

## Anti-patterns

**Hand-writing client types "just for now".** They drift immediately and hide the drift
behind green type checks.

**Editing generated files.** The edit is lost on the next generation, usually silently, and
the person who made it will not be the one who loses it.

**Not committing the schema.** Contract changes become invisible in review — the single
highest-value moment to catch a breaking change.

**Generating without CI verification.** Generation you have to remember is generation that
stops happening within a month.

**Treating type sync as testing.** Matching types prove the *shape* agrees. They prove
nothing about behaviour, error handling, or whether the endpoint does what it claims.
