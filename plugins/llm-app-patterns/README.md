# llm-app-patterns

Patterns for building AI-powered applications.

```bash
/plugin install llm-app-patterns@llm-utils
```

| Skill | Use when |
|-------|----------|
| `rag-evaluation` | Deciding between keyword and vector search, or diagnosing why answers are wrong |
| `grounded-generation` | The assistant must answer only from sources, refuse otherwise, and cite |
| `streaming-ui` | Streaming responses to a browser over SSE, with tool progress and cancellation |
| `openai-api` | Anything touching OpenAI models, pricing, or API shape |

## The through-line

These four cover one pipeline: **retrieve → ground → stream**, with a provider reference.

The order matters. Most RAG debugging starts in the wrong place — tuning prompts when
retrieval never returned the right passage, or swapping models when the prompt permits
unsourced answers.

**`rag-evaluation` first.** It answers the only question worth asking when an answer is
wrong: was the right material retrieved at all? Retrieval and generation failures have
opposite fixes, and teams routinely spend weeks on embeddings for what turns out to be a
prompt problem.

**`grounded-generation` second.** Once retrieval works, the model must actually use it —
and refuse when it cannot. Refusal is the property most likely to break silently, because
everything still looks fluent.

**`streaming-ui` last.** Delivery. Correct answers presented badly are still a bad product,
but a well-streamed wrong answer is worse.

## A recurring theme

Each skill pushes toward **measuring instead of assuming**:

- Build a 20-case eval set before arguing about embeddings
- Test refusal on plausible-but-absent questions, on every provider you ship
- Test cancellation and mid-stream errors, not just the happy path
- Verify model names and prices rather than quoting them from memory

The cost of measuring is a few hours. The cost of not measuring is a quarter spent
optimising the wrong layer.
