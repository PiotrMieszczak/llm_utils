---
name: openai-api
description: Reference for the OpenAI API and SDKs - the Responses API, Chat Completions, streaming, tool calling, structured outputs, embeddings, and model or pricing selection. Use whenever OpenAI, GPT, the openai package, or an OpenAI model id appears in the task, and before answering any question about OpenAI model choice, cost, context limits, or API shape. Do not answer these from memory.
model-hint: sonnet
---

# OpenAI API

**Verify before you answer.** OpenAI's model lineup, pricing, and default API surface
change every few months. Anything in this file may be stale; the sources below are
authoritative and this document is not.

Skip this skill when the work targets a different provider — for Anthropic, use the
`claude-api` skill.

## Verify first

Before quoting a model name, a price, or a context limit:

```bash
# Models actually available to this account, right now
curl -s https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq -r '.data[].id' | sort
```

| Question | Source |
|----------|--------|
| Which models exist / what are they for | <https://platform.openai.com/docs/models> |
| Current pricing | <https://openai.com/api/pricing/> |
| API shapes and parameters | <https://platform.openai.com/docs/api-reference> |
| SDK usage | <https://github.com/openai/openai-python> · <https://github.com/openai/openai-node> |

The SDK READMEs are the most reliable machine-readable signal for *current* idiom — they
are updated with each release and their examples show the interface OpenAI expects you to
use.

## Responses vs Chat Completions

Two APIs coexist. **Responses is the current default**; Chat Completions remains supported
and is not being removed.

```python
from openai import OpenAI
client = OpenAI()

# Responses API — current default
resp = client.responses.create(
    model="gpt-5.5",
    instructions="You are a terse assistant.",
    input="Summarise this changelog.",
)
print(resp.output_text)

# Chat Completions — still supported, familiar message array
resp = client.chat.completions.create(
    model="gpt-5.5",
    messages=[
        {"role": "system", "content": "You are a terse assistant."},
        {"role": "user", "content": "Summarise this changelog."},
    ],
)
print(resp.choices[0].message.content)
```

Differences worth knowing:

| | Responses | Chat Completions |
|---|-----------|------------------|
| System prompt | `instructions` | `system` role message |
| User content | `input` | `messages` array |
| Convenience accessor | `resp.output_text` | `resp.choices[0].message.content` |
| Built-in tools | Yes (web search, file search) | No |
| State across turns | Can be server-managed | Client resends history |

**Choosing:** new code → Responses. Existing Chat Completions code → no urgency to migrate;
migrate when you want a Responses-only feature. Porting a working integration for its own
sake is churn.

## Streaming

```python
stream = client.responses.create(
    model="gpt-5.5",
    input="Explain SSE buffering.",
    stream=True,
)
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
```

```python
# Async
stream = await client.responses.create(..., stream=True)
async for event in stream:
    ...
```

Responses streaming is **typed events**, not raw text chunks — check `event.type` rather
than assuming every event carries text. Lifecycle events (created, completed) and tool
events arrive on the same stream.

For delivering this to a browser, see the `streaming-ui` skill: the provider stream should
be normalised into your own event contract rather than forwarded raw, so switching
providers does not change your frontend.

## Tool calling

```python
tools = [{
    "type": "function",
    "name": "search_documents",
    "description": "Search indexed campaign documents.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search terms"},
            "limit": {"type": "integer", "default": 5},
        },
        "required": ["query"],
        "additionalProperties": False,
    },
}]

resp = client.responses.create(model="gpt-5.5", input=question, tools=tools)
```

The loop: call → inspect output for tool calls → execute → append results → call again
until no tool calls remain. **Always cap the iterations.** An unbounded tool loop is a
runaway bill; 5–10 is a reasonable ceiling with an explicit error beyond it.

Write descriptions for a reader who cannot see your code. `"limit"` tells the model
nothing; `"Maximum results to return, default 5"` tells it when to set the parameter.

## Structured outputs

When you need parseable output, constrain it rather than asking politely and hoping.

```python
from pydantic import BaseModel

class Quest(BaseModel):
    title: str
    status: str
    steps_total: int

resp = client.responses.parse(
    model="gpt-5.5",
    input="Extract the quest from: 'Hunt the dragon, 0 of 2 steps, in progress'",
    text_format=Quest,
)
quest = resp.output_parsed   # a typed Quest, not a string to json.loads
```

Prefer schema-constrained parsing over `{"type": "json_object"}`. The latter guarantees
*valid JSON*, not JSON matching your shape — you still get to write the validation and the
retry.

Even so, **validate on receipt**. A schema constrains structure, not semantics: a `status`
field can be correctly typed and still hold a value your state machine does not accept.

## Embeddings

```python
resp = client.embeddings.create(
    model="text-embedding-3-small",
    input=["first chunk", "second chunk"],   # batch — far cheaper than one per call
)
vectors = [d.embedding for d in resp.data]
```

Batch aggressively; per-item calls dominate cost and latency at any real corpus size.

Before adding embeddings at all, read `rag-evaluation`. Measure whether keyword retrieval
is actually failing — embedding an entire corpus is a recurring cost that is frequently
paid for a problem better solved by chunking.

## Cost control

Verify current prices at <https://openai.com/api/pricing/> before quoting any figure. As of
mid-2026, the flagship `gpt-5.5` was around **$5 per million input tokens** and **$30 per
million output**, with cached input roughly a tenth of the input price — but treat that as
a shape, not a quote.

Two properties that hold regardless of the numbers:

**Output costs several times more than input.** Cutting response length saves more than
trimming prompts.

**Cached input is dramatically cheaper.** Put the stable part of a prompt — system
instructions, retrieved context, few-shot examples — at the **front**, and keep it
byte-identical between calls. Caching matches on prefix; a timestamp at the top of the
prompt defeats it entirely.

Other levers:

- **Right-size the model.** Extraction and classification rarely need the flagship. Route
  by task; measure quality before assuming the cheap model is inadequate.
- **Batch API** for anything not interactive — substantially cheaper for bulk work with a
  latency tolerance.
- **Cap `max_output_tokens`.** Bounds the worst case.
- **Log token usage per request** from `resp.usage`. Cost you do not measure is cost you
  cannot manage.

## Errors and reliability

```python
from openai import RateLimitError, APITimeoutError, APIStatusError

try:
    resp = client.responses.create(model="gpt-5.5", input=q, timeout=30.0)
except RateLimitError:
    ...   # back off and retry; the SDK already retries some of these
except APITimeoutError:
    ...   # safe to retry
except APIStatusError as e:
    ...   # 4xx: usually a bug in the request. Do not blind-retry
```

The SDK retries certain failures automatically (`max_retries`, default 2). Do not layer
your own retry on top without accounting for that, or one user action becomes many billed
calls.

**Always set an explicit timeout.** The default is generous, and a hung request holding a
connection during a live interaction is worse than a fast failure.

## Multi-provider work

If the application supports more than one provider, keep OpenAI specifics behind a gateway
so provider differences do not leak into call sites. Event shapes, tool-call formats, and
token accounting all differ.

Test behaviour against **every** provider you ship. A capable hosted model and a small
local one behave very differently on instruction-following — particularly refusal, where a
weaker model is much more likely to answer without support. Passing on one is not evidence
for the other.

## Anti-patterns

**Quoting model names or prices from memory.** They change; the doc pages are one fetch
away.

**Hardcoding a model id across the codebase.** Put it in configuration. Models are
deprecated, and you want one place to change.

**Asking for JSON in the prompt and parsing hopefully.** Use structured outputs.

**Unbounded tool loops.** Cap the iterations.

**Prefix-breaking cache.** A dynamic value at the top of an otherwise stable prompt
silently multiplies input cost.

**Assuming the SDK does not already retry.** It does — check before adding your own.
