---
name: streaming-ui
description: Stream LLM responses to a browser over Server-Sent Events, including tool-call progress, citations, cancellation, and error handling mid-stream. Use when building a chat UI, adding token streaming, handling SSE in React, deciding between SSE and WebSockets, or debugging a stream that hangs, duplicates, or drops.
---

# Streaming UI

Stream model output to the browser so the user sees progress instead of a spinner.

The naive version — stream tokens, append to a string — works until it meets reality:
cancellation, errors after a partial answer, tool calls the user should see, reconnection,
and proxies that buffer.

## SSE or WebSockets?

**Use SSE** for LLM streaming unless you have a specific reason not to.

| | SSE | WebSocket |
|---|-----|-----------|
| Direction | Server → client | Bidirectional |
| Protocol | Plain HTTP | Upgrade handshake |
| Reconnect | Automatic in the browser | Manual |
| Auth | Normal headers and cookies | Awkward |
| Proxies | Standard HTTP path | Often needs configuration |

Chat is request/response with a streamed reply — the client sends one message and listens.
That is exactly SSE's shape. WebSockets earn their complexity when the client streams
*continuously* (live audio, collaborative editing, multiplayer state).

## Event types, not a token firehose

A stream carrying only text cannot express what a modern assistant does. Use named events:

```
event: tool
data: {"label":"Searched 3 documents","status":"running","id":"t1"}

event: tool
data: {"id":"t1","status":"done"}

event: token
data: {"text":"Opportunity attacks trigger when"}

event: citation
data: {"chunkId":812,"filename":"rulebook.pdf","page":195,"label":"S1"}

event: error
data: {"message":"Provider timed out","recoverable":true}

event: done
data: {"messageId":57}
```

Why separate events beat a single text stream:

- **Tool events** let the UI show what is happening during the pause before the first
  token, which is otherwise the longest dead air in the interaction
- **Citation events** arrive as they are resolved, so sources can render alongside text
- **An explicit `done`** distinguishes completion from a dropped connection — without it,
  the client cannot tell a finished answer from a broken pipe
- **Error events** allow failure *after* partial output, which is the common case

## Server (FastAPI)

```python
from fastapi.responses import StreamingResponse

async def stream_answer(question: str, campaign_id: str):
    async def gen():
        try:
            chunks = await retrieve(campaign_id, question)
            yield sse("tool", {"label": f"Searched {len(chunks)} documents",
                               "status": "done", "id": "t1"})

            for c in chunks:
                yield sse("citation", {"chunkId": c.id, "filename": c.filename,
                                       "page": c.page_from})

            async for token in gateway.stream(question, chunks):
                yield sse("token", {"text": token})

            yield sse("done", {"messageId": await persist(...)})

        except asyncio.CancelledError:
            # Client disconnected. Do not emit; just stop cleanly.
            raise
        except Exception as exc:
            logger.exception("stream failed")
            yield sse("error", {"message": str(exc), "recoverable": False})

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",   # nginx: do not buffer this response
        },
    )


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"
```

Three details that cause most production SSE bugs:

1. **`X-Accel-Buffering: no`** — nginx buffers responses by default, so the whole stream
   arrives at once and streaming appears broken in production but fine locally.
2. **The blank line after `data:`** — the event terminator. Without `\n\n`, nothing is
   dispatched and the stream silently hangs.
3. **`CancelledError` must propagate** — swallowing it leaks the generator and keeps the
   provider call running after the user has gone.

## Client (React)

```tsx
function useAssistantStream(conversationId: string) {
  const [message, setMessage] = useState("");
  const [tools, setTools] = useState<Tool[]>([]);
  const [citations, setCitations] = useState<Citation[]>([]);
  const [state, setState] = useState<"idle" | "streaming" | "error">("idle");
  const abortRef = useRef<AbortController | null>(null);

  const send = useCallback(async (text: string) => {
    abortRef.current?.abort();          // cancel any in-flight request
    const ctrl = new AbortController();
    abortRef.current = ctrl;

    setMessage(""); setTools([]); setCitations([]); setState("streaming");

    await fetchEventSource(`/api/v1/conversations/${conversationId}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
      signal: ctrl.signal,
      onmessage(ev) {
        const d = JSON.parse(ev.data);
        switch (ev.event) {
          case "token":    setMessage(m => m + d.text); break;
          case "tool":     setTools(t => upsert(t, d)); break;
          case "citation": setCitations(c => [...c, d]); break;
          case "error":    setState("error"); break;
          case "done":     setState("idle"); break;
        }
      },
      onerror(err) { setState("error"); throw err; },  // throw = stop retrying
    });
  }, [conversationId]);

  return { message, tools, citations, state, send,
           cancel: () => abortRef.current?.abort() };
}
```

**Why not the built-in `EventSource`?** It cannot send a POST body or custom headers — it
is GET-only. Sending a chat message needs a body, so use `fetch` with a streaming reader
(`@microsoft/fetch-event-source` handles the parsing).

**Throwing in `onerror` is deliberate.** The default behaviour retries forever; for a chat
message that means silently re-sending. Throw to stop, and let the user retry explicitly.

## Cancellation

Users change their mind, and long answers cost money. Cancellation must work end to end:

1. Client aborts the `AbortController`
2. The HTTP connection closes
3. FastAPI raises `CancelledError` inside the generator
4. The generator propagates it, closing the provider stream
5. Partial output is either persisted as partial or discarded — **decide which, and be
   consistent**

Untested cancellation usually breaks at step 4, where a broad `except Exception` swallows
`CancelledError` and the provider call keeps running, billing you for output nobody sees.

## Rendering while streaming

**Markdown mid-stream.** Partial markdown is malformed by definition — an unclosed code
fence, a half-written link. Either render plain text until `done`, or use a parser
tolerant of incomplete input. Naively re-parsing on every token produces visible flicker
as elements open and close.

**Autoscroll.** Follow the newest content, but stop the moment the user scrolls up. Nothing
is more hostile than being yanked back down while trying to read.

**The cursor.** A blinking block at the stream head reads as "still working" far better
than a spinner elsewhere on the page.

**Do not animate each token.** Per-token transitions look like a stutter at speed.

## Testing

```python
async def test_stream_emits_done_last():
    events = [e async for e in collect(stream_answer("q", "c1"))]
    assert events[-1].event == "done"

async def test_cancellation_stops_provider():
    task = asyncio.create_task(consume(stream_answer("q", "c1")))
    await asyncio.sleep(0.05)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert gateway.active_streams == 0     # nothing left running
```

Test the failure paths specifically: error after partial output, cancellation mid-stream,
and a provider that returns nothing at all. Those are where streaming implementations
break, and none of them show up in a happy-path test.

## Anti-patterns

**Buffering server-side then "streaming" the result.** Defeats the purpose; the user waits
the same total time with extra complexity.

**No `done` event.** The client cannot distinguish completion from a dropped connection,
so it either hangs or falsely reports failure.

**Retrying automatically on error.** For a chat message, a silent retry sends the message
twice and bills twice.

**Rendering markdown on every token without a tolerant parser.** Visible flicker as
elements repeatedly open and close.

**Assuming it works because it works locally.** Proxy buffering (`X-Accel-Buffering`) means
streaming commonly works in development and fails in production.
