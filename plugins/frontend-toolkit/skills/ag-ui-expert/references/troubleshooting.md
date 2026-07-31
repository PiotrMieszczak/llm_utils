# AG-UI Troubleshooting Guide

Common issues, debugging strategies, and solutions for AG-UI implementations.

## Debugging Tools and Techniques

### 1. Event Stream Logging

**Log All Events:**
```typescript
// TypeScript
eventStream.subscribe({
  next: (event) => {
    console.log('[AG-UI Event]', {
      type: event.type,
      timestamp: new Date().toISOString(),
      data: event
    });
    handleEvent(event);
  }
});
```

```python
# Python
for event in event_stream:
    print(f"[AG-UI Event] {event.type} at {datetime.now()}")
    print(json.dumps(event.__dict__, indent=2))
    handle_event(event)
```

### 2. Network Inspection

**Browser DevTools:**
- Open Network tab
- Filter by `EventStream` or your API domain
- Inspect SSE messages in real-time
- Check for connection errors

**cURL Testing:**
```bash
# Test SSE endpoint
curl -N -H "Accept: text/event-stream" \
  https://your-api.com/agent/run \
  -d '{"messages":[{"role":"user","content":"test"}]}'
```

### 3. Event Validation

**Validate Event Structure:**
```typescript
function validateEvent(event: any): boolean {
  if (!event.type) {
    console.error('Event missing type:', event);
    return false;
  }

  // Type-specific validation
  switch (event.type) {
    case 'TEXT_MESSAGE_START':
      if (!event.messageId || !event.role) {
        console.error('Invalid TEXT_MESSAGE_START:', event);
        return false;
      }
      break;

    case 'TEXT_MESSAGE_CONTENT':
      if (!event.messageId || event.delta === undefined) {
        console.error('Invalid TEXT_MESSAGE_CONTENT:', event);
        return false;
      }
      break;

    // Add other validations
  }

  return true;
}
```

## Common Issues and Solutions

### Issue 1: Events Not Received

**Symptoms:**
- No events appearing in frontend
- Connection established but silent
- Timeout errors

**Possible Causes & Solutions:**

#### A. CORS Issues

**Problem:** Browser blocking cross-origin requests

**Solution:**
```python
# Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/agent/*": {"origins": "*"}})

# FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Verify:**
```bash
# Check CORS headers
curl -H "Origin: https://your-frontend.com" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS \
  https://your-api.com/agent/run
```

#### B. Buffering Issues

**Problem:** Proxy/server buffering events

**Solution:**
```python
# Disable buffering
response_headers = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",  # Nginx
    "Content-Type": "text/event-stream",
}
```

```nginx
# Nginx configuration
location /agent/ {
    proxy_pass http://backend;
    proxy_buffering off;
    proxy_cache off;
    proxy_set_header Connection '';
    proxy_http_version 1.1;
    chunked_transfer_encoding off;
}
```

#### C. Network Timeout

**Problem:** Request timing out before completion

**Solution:**
```typescript
// Increase timeout
const agent = new HttpAgent({
  baseUrl: 'https://api.example.com',
  timeout: 300000, // 5 minutes (increased from default)
});
```

```python
# Python
agent = HttpAgent(
    base_url="https://api.example.com",
    timeout=300.0  # 5 minutes
)
```

### Issue 2: Incomplete or Corrupted Messages

**Symptoms:**
- Messages cut off mid-stream
- Garbled text content
- Missing message endings

**Possible Causes & Solutions:**

#### A. Message Not Properly Ended

**Problem:** Missing TEXT_MESSAGE_END event

**Solution:**
```python
# Always emit END event
try:
    emit_event({"type": "TEXT_MESSAGE_START", "messageId": msg_id, "role": "assistant"})

    for chunk in generate_text():
        emit_event({"type": "TEXT_MESSAGE_CONTENT", "messageId": msg_id, "delta": chunk})

finally:
    # Always emit end, even on error
    emit_event({"type": "TEXT_MESSAGE_END", "messageId": msg_id})
```

#### B. Encoding Issues

**Problem:** Special characters not properly encoded

**Solution:**
```python
# Ensure UTF-8 encoding
import json

def emit_event(event):
    json_str = json.dumps(event, ensure_ascii=False)
    yield f"data: {json_str}\n\n".encode('utf-8')
```

#### C. Event Order Issues

**Problem:** Events arriving out of order

**Solution:**
```typescript
// Track event sequence
class EventSequencer {
  private expectedSequence = 0;
  private eventBuffer: Map<number, BaseEvent> = new Map();

  handleEvent(event: BaseEvent & { sequence?: number }) {
    if (!event.sequence) {
      // No sequence number, process immediately
      this.processEvent(event);
      return;
    }

    if (event.sequence === this.expectedSequence) {
      // Expected event, process it and any buffered events
      this.processEvent(event);
      this.expectedSequence++;

      // Process buffered events in sequence
      while (this.eventBuffer.has(this.expectedSequence)) {
        this.processEvent(this.eventBuffer.get(this.expectedSequence)!);
        this.eventBuffer.delete(this.expectedSequence);
        this.expectedSequence++;
      }
    } else {
      // Out of order, buffer it
      this.eventBuffer.set(event.sequence, event);
    }
  }
}
```

### Issue 3: State Synchronization Problems

**Symptoms:**
- Frontend state doesn't match backend
- State updates not reflecting in UI
- State drift over time

**Possible Causes & Solutions:**

#### A. Delta Application Errors

**Problem:** JSON Patch operations failing silently

**Solution:**
```typescript
import { applyPatch } from 'fast-json-patch';

function applyStateDelta(currentState: any, delta: any[]) {
  try {
    const { newDocument, errors } = applyPatch(
      currentState,
      delta,
      /* validate */ true,
      /* mutate */ false
    );

    if (errors && errors.length > 0) {
      console.error('Patch application errors:', errors);
      // Request full snapshot
      requestStateSnapshot();
      return currentState; // Keep current state
    }

    return newDocument;
  } catch (error) {
    console.error('Failed to apply state delta:', error);
    requestStateSnapshot();
    return currentState;
  }
}
```

#### B. Missing Snapshots

**Problem:** Only deltas sent, no initial snapshot

**Solution:**
```python
# Always send snapshot at start
async def run_agent(input):
    emit_event({"type": "RUN_STARTED", ...})

    # Send initial state snapshot
    emit_event({
        "type": "STATE_SNAPSHOT",
        "state": get_current_state()
    })

    # Then send deltas during execution
    # ...
```

#### C. State Drift

**Problem:** Accumulated delta errors causing state divergence

**Solution:**
```python
# Periodic snapshots to prevent drift
delta_count = 0
MAX_DELTAS_BEFORE_SNAPSHOT = 50

async def update_state(new_state):
    global delta_count

    if delta_count >= MAX_DELTAS_BEFORE_SNAPSHOT:
        # Send full snapshot
        emit_event({"type": "STATE_SNAPSHOT", "state": new_state})
        delta_count = 0
    else:
        # Send delta
        delta = compute_delta(current_state, new_state)
        emit_event({"type": "STATE_DELTA", "delta": delta})
        delta_count += 1
```

### Issue 4: Tool Execution Failures

**Symptoms:**
- Tools not being called
- Tool errors not surfaced
- Execution hangs on tool calls

**Possible Causes & Solutions:**

#### A. Invalid Tool Definitions

**Problem:** Tool schema doesn't match expected format

**Solution:**
```typescript
// Validate tool definitions
import Ajv from 'ajv';

const ajv = new Ajv();

const toolSchema = {
  type: 'object',
  required: ['name', 'description', 'parameters'],
  properties: {
    name: { type: 'string' },
    description: { type: 'string' },
    parameters: {
      type: 'object',
      required: ['type', 'properties'],
      properties: {
        type: { const: 'object' },
        properties: { type: 'object' },
        required: { type: 'array', items: { type: 'string' } }
      }
    }
  }
};

function validateTool(tool: any): boolean {
  const validate = ajv.compile(toolSchema);
  const valid = validate(tool);

  if (!valid) {
    console.error('Invalid tool definition:', validate.errors);
    return false;
  }

  return true;
}
```

#### B. Tool Execution Timeout

**Problem:** Tool takes too long, blocks event stream

**Solution:**
```python
import asyncio

async def execute_tool_with_timeout(tool_name, args, timeout=30):
    """Execute tool with timeout."""
    try:
        result = await asyncio.wait_for(
            execute_tool(tool_name, args),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        error_msg = f"Tool '{tool_name}' timed out after {timeout}s"
        emit_event({
            "type": "TOOL_CALL_END",
            "toolCallId": tool_call_id,
            "error": error_msg
        })
        raise
```

#### C. Tool Arguments Not Validated

**Problem:** Invalid arguments causing runtime errors

**Solution:**
```python
from jsonschema import validate, ValidationError

def execute_tool(tool_name, args):
    """Execute tool with validation."""

    tool_def = get_tool_definition(tool_name)

    # Validate arguments against schema
    try:
        validate(instance=args, schema=tool_def['parameters'])
    except ValidationError as e:
        emit_event({
            "type": "TOOL_CALL_END",
            "error": f"Invalid arguments: {e.message}"
        })
        return

    # Execute tool
    try:
        result = tool_registry[tool_name](**args)
        emit_event({
            "type": "TOOL_CALL_END",
            "result": result
        })
    except Exception as e:
        emit_event({
            "type": "TOOL_CALL_END",
            "error": str(e)
        })
```

### Issue 5: Memory Leaks

**Symptoms:**
- Increasing memory usage over time
- Browser/server performance degradation
- Eventually crashes

**Possible Causes & Solutions:**

#### A. Event Listeners Not Cleaned Up

**Problem:** Subscriptions not unsubscribed

**Solution:**
```typescript
// React example
useEffect(() => {
  const subscription = eventStream.subscribe({
    next: handleEvent
  });

  // IMPORTANT: Cleanup on unmount
  return () => {
    subscription.unsubscribe();
  };
}, [eventStream]);

// Class component
class AgentComponent extends React.Component {
  private subscription: Subscription | null = null;

  componentDidMount() {
    this.subscription = eventStream.subscribe({
      next: this.handleEvent
    });
  }

  componentWillUnmount() {
    // IMPORTANT: Cleanup
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}
```

#### B. Large State Objects Accumulating

**Problem:** State growing indefinitely

**Solution:**
```python
# Limit state size
MAX_MESSAGE_HISTORY = 100

def update_state(state, new_messages):
    """Update state with message limit."""

    state['messages'].extend(new_messages)

    # Trim old messages
    if len(state['messages']) > MAX_MESSAGE_HISTORY:
        state['messages'] = state['messages'][-MAX_MESSAGE_HISTORY:]

    return state
```

#### C. Circular References

**Problem:** Objects referencing each other preventing GC

**Solution:**
```typescript
// Avoid circular references
class MessageManager {
  private messages: Map<string, Message> = new Map();

  addMessage(msg: Message) {
    // Store only necessary data, not full objects with references
    this.messages.set(msg.id, {
      id: msg.id,
      content: msg.content,
      role: msg.role
      // Don't store parent/child references
    });
  }

  clear() {
    this.messages.clear(); // Explicitly clear
  }
}
```

### Issue 6: Performance Degradation

**Symptoms:**
- Slow event processing
- UI freezing
- Delayed updates

**Possible Causes & Solutions:**

#### A. Synchronous Blocking Operations

**Problem:** Heavy processing blocking event loop

**Solution:**
```typescript
// Use Web Workers for heavy processing
const worker = new Worker('event-processor.worker.js');

worker.postMessage({ event });

worker.onmessage = (e) => {
  const processedEvent = e.data;
  updateUI(processedEvent);
};
```

```python
# Use async for I/O operations
async def process_event(event):
    """Non-blocking event processing."""

    if event.type == "TOOL_CALL_START":
        # Use async for I/O
        result = await fetch_data_async(event.args)
    else:
        # CPU-bound work
        result = await asyncio.to_thread(heavy_computation, event)

    return result
```

#### B. Excessive Re-renders

**Problem:** UI updating too frequently

**Solution:**
```typescript
// Debounce state updates
import { debounce } from 'lodash';

const [state, setState] = useState({});

const debouncedSetState = useMemo(
  () => debounce((newState) => setState(newState), 100),
  []
);

// In event handler
if (event.type === 'STATE_DELTA') {
  const newState = applyDelta(state, event.delta);
  debouncedSetState(newState); // Debounced update
}
```

#### C. Large DOM Updates

**Problem:** Rendering large lists inefficiently

**Solution:**
```typescript
// Use virtualization for long lists
import { VirtualList } from 'react-virtual';

function MessageList({ messages }) {
  return (
    <VirtualList
      items={messages}
      renderItem={(msg) => <Message key={msg.id} {...msg} />}
      itemHeight={50}
    />
  );
}
```

## Debugging Checklist

When troubleshooting AG-UI issues:

- [ ] Check browser console for errors
- [ ] Inspect network tab for failed requests
- [ ] Verify CORS headers are correct
- [ ] Log all events to see what's being received
- [ ] Validate event structure matches expected format
- [ ] Check for missing event types (START without END)
- [ ] Verify state synchronization with snapshots
- [ ] Test tool definitions against schema
- [ ] Monitor memory usage over time
- [ ] Check for unsubscribed event listeners
- [ ] Verify timeout settings are adequate
- [ ] Test with minimal example to isolate issue
- [ ] Review server logs for backend errors
- [ ] Check network infrastructure (proxies, firewalls)
- [ ] Validate JSON encoding/decoding

## Testing Strategies

### Unit Testing Events

```typescript
// Mock event stream
import { of } from 'rxjs';

describe('Event Handling', () => {
  it('should handle message events', () => {
    const mockEvents = of(
      { type: 'TEXT_MESSAGE_START', messageId: '1', role: 'assistant' },
      { type: 'TEXT_MESSAGE_CONTENT', messageId: '1', delta: 'Hello' },
      { type: 'TEXT_MESSAGE_END', messageId: '1' }
    );

    const handler = new EventHandler();
    mockEvents.subscribe(handler.handleEvent);

    expect(handler.messages[0].content).toBe('Hello');
  });
});
```

### Integration Testing

```python
# Test full event flow
import pytest

@pytest.mark.asyncio
async def test_agent_run():
    """Test complete agent execution."""

    agent = HttpAgent(base_url="http://localhost:8000")

    input_data = RunAgentInput(
        messages=[Message(role="user", content="test")]
    )

    events = []
    async for event in agent.run(input_data):
        events.append(event)

    # Verify event sequence
    assert events[0].type == "RUN_STARTED"
    assert events[-1].type == "RUN_FINISHED"

    # Verify messages
    message_events = [e for e in events if 'MESSAGE' in e.type]
    assert len(message_events) > 0
```

## Performance Monitoring

### Add Metrics

```typescript
class PerformanceMonitor {
  private eventCount = 0;
  private startTime = Date.now();

  trackEvent(event: BaseEvent) {
    this.eventCount++;

    // Log metrics every 100 events
    if (this.eventCount % 100 === 0) {
      const elapsed = Date.now() - this.startTime;
      const eventsPerSecond = this.eventCount / (elapsed / 1000);

      console.log(`[Metrics] ${eventsPerSecond.toFixed(2)} events/sec`);
    }
  }
}
```

## Getting Help

If issues persist after troubleshooting:

1. **Check Official Documentation**
   - Use gemini-delegate skill to fetch latest docs
   - https://docs.ag-ui.com/

2. **Minimal Reproduction**
   - Create minimal example demonstrating issue
   - Test with simple agent/client setup

3. **Community Resources**
   - GitHub issues for SDK
   - Community forums
   - Stack Overflow with `ag-ui` tag

4. **Debug Logs**
   - Enable verbose logging
   - Capture full event stream
   - Share sanitized logs when seeking help

## Next Steps

- Review `protocol-fundamentals.md` for event system details
- Check `architectural-decisions.md` for design patterns
- See implementation guides for code examples
- Use `../assets/integration-checklist.md` for validation
