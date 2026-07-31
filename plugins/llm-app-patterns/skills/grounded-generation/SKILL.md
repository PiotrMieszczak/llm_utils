---
name: grounded-generation
description: Make an assistant answer only from supplied source material, refuse when the material does not cover the question, and cite what it used. Use when building a RAG assistant, a docs Q&A bot, or any feature where a confidently wrong answer is worse than no answer, and when adding citations or testing refusal behaviour.
model-hint: opus
---

# Grounded Generation

Make a model answer **from supplied material only**, say so when the material does not
cover the question, and show what it used.

The failure this prevents: a plausible, fluent, wrong answer. In domains where the user
cannot easily verify — rules lookups, medical or legal information, internal
documentation — a confident fabrication is worse than "I don't know", because it is acted
on.

## Three properties, in priority order

1. **Refusal** — when the context does not answer the question, say so
2. **Attribution** — every factual claim traces to a retrieved source
3. **Fluency** — the answer reads well

Most implementations optimise these in reverse. Fluency is the easiest to get and the
least valuable; refusal is the hardest and the one that makes the system trustworthy.

## Prompt structure

Keep the grounding instruction in **one place** in the codebase. If it is duplicated
per-call-site, the rule will drift and some path will quietly lose it.

```
You answer questions using ONLY the source material provided below.

Rules:
- If the sources do not contain the answer, say so plainly. Do not use general
  knowledge to fill the gap.
- Cite the source id for each factual claim, as [S1], [S2].
- If sources conflict, say they conflict and show both.
- Partial answers are fine. Answer what the sources support and state what
  they do not cover.

Sources:
[S1] (rulebook.pdf, p.195, "Opportunity Attacks")
<chunk text>

[S2] (module.pdf, p.12, "The Vey Consortium")
<chunk text>

Question: <user question>
```

What each rule buys:

| Rule | Prevents |
|------|----------|
| "ONLY the source material" | Blending training knowledge with retrieved facts invisibly |
| "say so plainly" | The fluent fabrication |
| Source ids | Unverifiable claims |
| Conflict handling | Silently picking one of two contradictory sources |
| "Partial answers are fine" | All-or-nothing refusal when half the answer is present |

That last rule matters more than it looks. Without it, models tend to refuse entirely when
sources cover most but not all of a question — which users experience as uselessness.

## Structure sources so citation is possible

A citation the user cannot follow is decoration. Each source needs a stable id, a document
reference, and a location:

```python
def format_sources(chunks):
    return "\n\n".join(
        f"[S{i}] ({c.filename}, p.{c.page_from}, {c.heading!r})\n{c.content}"
        for i, c in enumerate(chunks, start=1)
    )
```

Keep the id → chunk mapping server-side. When the response comes back with `[S2]`, resolve
it to a real chunk id and return that with the message, so the UI can link to the source.

## Verify attribution — do not trust it

A model can emit `[S1]` after a sentence that `[S1]` does not support. Citations are a
claim about the model's reasoning, not proof of it.

Cheap check that catches the worst cases:

```python
def unsupported_citations(answer, sources, min_overlap=0.3):
    """Flag citations whose claim shares little vocabulary with the cited source."""
    problems = []
    for sentence, cited_ids in _sentences_with_citations(answer):
        for sid in cited_ids:
            source = sources.get(sid)
            if source is None:
                problems.append((sentence, sid, "cites a source that was not supplied"))
                continue
            if _token_overlap(sentence, source.content) < min_overlap:
                problems.append((sentence, sid, "low overlap with cited source"))
    return problems
```

Lexical overlap is a weak signal — a correct paraphrase can score low. Use it to **flag for
review**, not to block responses. Its real value is in tests, where a spike in unsupported
citations after a prompt change is a genuine regression signal.

## Test refusal explicitly

Refusal is the property most likely to silently break, because everything still *looks*
fine — you get fluent answers, just wrong ones.

```python
OUT_OF_CORPUS = [
    "what is the capital of France",           # general knowledge, not in corpus
    "what are the rules for starship combat",  # plausible for the domain, absent
    "who is Zephyr Blackwater",                # invented proper noun
]

@pytest.mark.parametrize("question", OUT_OF_CORPUS)
def test_refuses_when_material_absent(question, assistant):
    answer = assistant.ask(question)
    assert _is_refusal(answer), f"answered without sources: {answer!r}"
```

The middle case is the important one: **plausible but absent**. A question that sounds like
it belongs in the corpus is where models are most tempted to help.

### Test on every provider

A capable hosted model and a small local model behave very differently here. The weaker
model is far more likely to answer unsourced. Passing on one provider is not evidence for
the other — run the refusal suite against every provider the product offers.

## Distinguishing retrieval from creativity

Many products want both: factual lookup *and* generation ("draft a scene", "suggest a
name"). These need opposite rules — one forbids invention, the other requires it.

Do not blend them behind one prompt. Separate them, and make the mode visible to the user:

- **Retrieval mode** — grounded, cited, refuses when unsupported
- **Creative mode** — explicitly generative, clearly labelled as invention

A user who cannot tell which mode produced an answer will eventually trust a creative
output as fact.

## Anti-patterns

**"Use the context if relevant."** Hedged instructions produce hedged behaviour. The model
will fall back to general knowledge and you will not be able to tell when it did.

**Citations rendered as plain text.** If `[S1]` does not resolve to something clickable, it
is theatre. Users cannot verify, so they either trust everything or nothing.

**Stuffing the context window.** More chunks is not better grounding — irrelevant material
dilutes attention and increases the chance the model latches onto a near-miss passage.
Retrieve fewer, better chunks (see `rag-evaluation`).

**Silent truncation.** If retrieved context exceeds the window, dropping chunks quietly can
remove the one that mattered. Truncate explicitly and say what was dropped.

**Testing refusal only on obviously absurd questions.** "What is the capital of France"
proves little. Test plausible-but-absent questions, which is where real failures live.
