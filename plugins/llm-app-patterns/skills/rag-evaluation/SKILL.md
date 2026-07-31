---
name: rag-evaluation
description: Measure whether a retrieval system actually finds the right material, before and after changing it. Use when building or debugging RAG, when deciding between keyword and vector search, when someone proposes adding embeddings, when answers are wrong and you need to know whether retrieval or generation is at fault, or when asked to evaluate search quality.
---

# RAG Evaluation

Retrieval quality is measurable. Most teams never measure it, then argue about embeddings
from intuition.

This skill builds the measurement first, so changes to retrieval can be justified with
evidence instead of vibes.

## The question that comes first

When a RAG answer is wrong, exactly one of two things failed:

1. **Retrieval** — the right material was never fetched. The model never had a chance.
2. **Generation** — the right material was fetched and the model still got it wrong.

These have opposite fixes. Adding a better model does nothing for a retrieval failure;
tuning chunk size does nothing for a generation failure.

**Always diagnose this before changing anything:**

```
Take a failing question.
  Manually find the passage that answers it.
  Is that passage in the retrieved set?
    NO  → retrieval problem. Work on indexing, chunking, or query handling.
    YES → generation problem. Work on the prompt or the model.
```

Teams routinely spend weeks on vector search for what turns out to be a prompt problem.
One hour of this diagnosis saves that.

## Build an evaluation set

Nothing else in this skill works without one. It does not need to be large — **20 to 50
question/expected-passage pairs** beats no measurement by an enormous margin, and beats a
2,000-pair set you never actually build.

```jsonc
// eval/retrieval.jsonl — one case per line
{"q": "what happens if I move away from an enemy in melee",
 "expect_chunk_ids": [812],
 "expect_contains": "opportunity attack",
 "note": "paraphrased - user does not know the term of art"}

{"q": "who runs the Vey Consortium",
 "expect_contains": "Doran Vey",
 "note": "proper noun, exact match should be easy"}

{"q": "what is the airspeed of an unladen swallow",
 "expect_empty": true,
 "note": "not in corpus - retrieval must return nothing, not something plausible"}
```

Three case types, all necessary:

| Type | Purpose |
|------|---------|
| **Exact-term** | Proper nouns, terms of art. Keyword search should ace these |
| **Paraphrased** | The user does not know the jargon. This is where keyword search fails |
| **Out-of-corpus** | Must retrieve nothing. Guards against confidently wrong answers |

The third type is the one everyone forgets, and it protects the property that matters
most: a system that answers "I don't know" correctly is more useful than one that always
answers.

### Sourcing real questions

Invented questions are biased toward what you already know works. Better sources: logged
user queries, support requests, questions asked in the product's own domain. If the system
is not live yet, ask someone who is not on the team to write twenty questions.

## Metrics that matter

Keep it to a few numbers people will actually look at.

| Metric | Definition | Why |
|--------|------------|-----|
| **Recall@k** | Share of cases where an expected chunk appears in the top *k* | The ceiling on answer quality — nothing downstream can recover a miss |
| **MRR** | Mean of 1/rank of the first correct chunk | Rewards ranking the answer first, not fifth |
| **Correct-refusal rate** | Share of out-of-corpus cases retrieving nothing | Guards against plausible fabrication |

**Recall@k is the primary number.** If the passage is not retrieved, no prompt or model
fixes it.

Track *k* at the value you actually put in the prompt. Recall@50 is irrelevant if you
send the top 5.

## The harness

Keep it boring and runnable in CI.

```python
def evaluate(search_fn, cases, k=5):
    hits = refusals_ok = reciprocal = 0
    scored = refusal_cases = 0

    for case in cases:
        results = search_fn(case["q"], k=k)

        if case.get("expect_empty"):
            refusal_cases += 1
            refusals_ok += not results
            continue

        scored += 1
        rank = _first_match_rank(results, case)
        if rank:
            hits += 1
            reciprocal += 1 / rank

    return {
        "recall_at_k": hits / scored if scored else 0.0,
        "mrr": reciprocal / scored if scored else 0.0,
        "correct_refusal": refusals_ok / refusal_cases if refusal_cases else None,
        "k": k,
        "n": len(cases),
    }
```

Print per-case failures, not just aggregates. The list of *which* questions failed is what
tells you what to fix; a single number tells you nothing actionable.

## Using it to make decisions

### "Should we add vector search?"

The question this skill exists to answer with evidence.

1. Measure current keyword recall on the evaluation set.
2. Look at **which** cases fail. If failures cluster in the paraphrased group, semantic
   search is likely to help. If failures are spread across exact-term cases, the problem
   is chunking or indexing, and embeddings will not fix it.
3. Implement the alternative, measure the same set, compare.
4. Weigh the gain against the cost: embedding every document at ingest, a new dependency,
   and a second thing that can be stale.

A common outcome: keyword recall is already 0.85, the failures are chunk-boundary
problems, and better chunking beats embeddings for a fraction of the cost.

### "Which chunking strategy?"

Chunking is usually higher-leverage than the retrieval algorithm and gets far less
attention. Vary one parameter, hold everything else, re-measure:

- Chunk size and overlap
- Splitting on headings versus fixed length
- Whether the heading is prepended to each chunk's indexed text

That last one is frequently worth several points of recall on its own, because it gives an
otherwise context-free paragraph its topic.

### "Did that change break retrieval?"

Run the harness in CI. Fail the build on a recall regression beyond a threshold. Retrieval
quality degrades silently otherwise — nothing throws an exception when search gets worse.

## Honest reporting

- Report **n**. "Recall improved to 0.9" on 8 cases is noise.
- Report the *k* used, since recall is meaningless without it.
- Report **which** cases changed, not just the aggregate. A change that fixes three
  paraphrase cases and breaks two exact-match cases is not obviously an improvement.
- Never report a metric you did not run.

## Anti-patterns

**Evaluating with an LLM judge as the only signal.** Useful for answer quality, circular
for retrieval — the judge sees only what was retrieved, so it cannot detect what was
missed. Recall needs ground truth.

**Tuning on the evaluation set until it passes.** That measures memorisation. Keep a
holdout, or periodically add fresh cases from real usage.

**Measuring end-to-end answer quality only.** It conflates the two failure modes this
skill separates, and points at the wrong fix.

**Building the perfect eval set before shipping.** Twenty cases today beats two hundred
next quarter.
