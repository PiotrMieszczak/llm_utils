# AG-UI Architectural Decisions

Decision frameworks, design patterns, and architectural guidance for AG-UI implementations.

## When to Use AG-UI

### AG-UI is Ideal For:

✅ **Long-Running Agent Operations**
- Tasks taking > 2 seconds
- Multi-step reasoning workflows
- Complex agent executions

✅ **Interactive Agent Experiences**
- Streaming responses token-by-token
- Human-in-the-loop workflows
- Real-time user feedback during execution

✅ **Stateful Agent Conversations**
- Multi-turn dialogues
- Context preservation across interactions
- Agent memory and learning

✅ **Multimodal Agent Interfaces**
- Image/file/audio processing
- Generative UI components
- Rich media interactions

✅ **Sub-Agent Composition**
- Hierarchical agent systems
- Agent handoff and delegation
- Multi-agent coordination

### Consider Alternatives When:

❌ **Simple Request-Response**
- Single-step operations < 1 second
- No streaming needed
- Simple REST API sufficient

❌ **Pure Tool Integration**
- Only connecting agents to tools/context
- Use MCP (Model Context Protocol) instead

❌ **Agent-to-Agent Communication**
- Direct agent collaboration
- Use A2A (Agent-to-Agent Protocol) instead

❌ **Static Content Delivery**
- No dynamic agent behavior
- Traditional web APIs work better

## AG-UI vs Other Protocols

### Decision Matrix

| Need | Protocol | Reason |
|------|----------|--------|
| Connect UI to agent | **AG-UI** | Event-driven, streaming, stateful |
| Connect agent to tools | **MCP** | Tool/context abstraction |
| Connect agents together | **A2A** | Agent orchestration |
| Simple CRUD operations | **REST** | Simpler, well-understood |
| Real-time data subscription | **GraphQL Subscriptions** | Better for non-agent real-time data |
| Background job processing | **Message Queue** | Better for async batch processing |

### Protocol Ecosystem Integration

```
┌─────────────────────────────────────┐
│         User Interface              │
│                                     │
│    ┌─────────────────────────┐     │
│    │      AG-UI Client       │     │
│    └──────────┬──────────────┘     │
└───────────────┼─────────────────────┘
                │ AG-UI Protocol
┌───────────────▼─────────────────────┐
│         Main Agent System           │
│                                     │
│  ┌──────────┐      ┌───────────┐   │
│  │  MCP     │      │    A2A    │   │
│  │ Client   │      │  Client   │   │
│  └────┬─────┘      └─────┬─────┘   │
└───────┼──────────────────┼──────────┘
        │                  │
┌───────▼─────┐    ┌──────▼──────┐
│   Tools &   │    │ Sub-Agents  │
│   Context   │    │   System    │
└─────────────┘    └─────────────┘
```

**Use Together:**
- AG-UI: User interaction layer
- MCP: Tool and context integration
- A2A: Agent collaboration

## Transport Mechanism Selection

### Server-Sent Events (SSE)

**Choose When:**
- Maximum compatibility required
- Behind corporate firewalls/proxies
- Simple infrastructure
- HTTP/1.1 environment

**Tradeoffs:**
- ✅ Broad compatibility
- ✅ Simple implementation
- ✅ Works through most proxies
- ❌ Text-based (larger payloads)
- ❌ Unidirectional only
- ❌ Browser connection limits (6 per domain)

**Example Use Case:**
Public-facing chat applications, enterprise environments with strict network policies.

### Binary Protocol

**Choose When:**
- Performance is critical
- High throughput needed
- Controlled network environment
- Large data volumes

**Tradeoffs:**
- ✅ Compact payloads
- ✅ Fast serialization
- ✅ Lower bandwidth
- ❌ More complex implementation
- ❌ Debugging harder
- ❌ May need custom infrastructure

**Example Use Case:**
Internal agent platforms, high-performance computing, data-intensive applications.

### WebSockets

**Choose When:**
- Bidirectional communication required
- Human-in-the-loop workflows
- Real-time agent steering
- Low latency critical

**Tradeoffs:**
- ✅ Full duplex communication
- ✅ Low latency
- ✅ Connection persistence
- ❌ More complex than SSE
- ❌ Firewall/proxy issues
- ❌ Connection management overhead

**Example Use Case:**
Collaborative agent interfaces, real-time co-editing, interactive simulations.

### Custom Transports

**Choose When:**
- Existing infrastructure to leverage
- Special requirements (queuing, pub/sub)
- Hybrid architectures

**Options:**
- Message queues (RabbitMQ, Kafka)
- gRPC streams
- HTTP/2 push
- Custom protocols

## State Management Strategies

### Snapshot vs Delta Decision Tree

```
Start
  │
  ├─ Is state < 10KB? ──Yes──> Use Snapshots
  │                              - Simple
  │                              - Fast to implement
  │
  ├─ State updates frequent? ──No──> Use Snapshots
  │                                   - Infrequent = snapshots fine
  │
  ├─ State updates < 1KB each? ──Yes──> Use Deltas
  │                                      - Efficient bandwidth
  │
  └─ Complex state structure? ──Yes──> Use Deltas
                                        - JSON Patch ideal
```

### Snapshot Strategy

**Use When:**
- Small state objects (< 10KB)
- Infrequent updates (< 1 per second)
- Simple state structure
- Initial state transmission
- State reset needed

**Pattern:**
```typescript
// Send full state on run start
{
  type: "STATE_SNAPSHOT",
  state: {
    conversation: {...},
    userPreferences: {...},
    memory: {...}
  }
}

// Use snapshots periodically to prevent drift
// Every 10-20 updates, send full snapshot
```

### Delta Strategy

**Use When:**
- Large state objects (> 10KB)
- Frequent updates (> 1 per second)
- Network efficiency critical
- Complex nested structures

**Pattern:**
```typescript
// Initial snapshot
{type: "STATE_SNAPSHOT", state: fullState}

// Then incremental updates
{
  type: "STATE_DELTA",
  delta: [
    {op: "replace", path: "/counter", value: 42},
    {op: "add", path: "/items/-", value: newItem}
  ]
}

// Periodic snapshot to prevent drift
{type: "STATE_SNAPSHOT", state: fullState} // Every 50 deltas
```

### Hybrid Strategy (Recommended)

**Best Practice:**
1. Send STATE_SNAPSHOT on RUN_STARTED
2. Use STATE_DELTA for updates during execution
3. Send STATE_SNAPSHOT every N deltas (e.g., 50) to prevent drift
4. Send STATE_SNAPSHOT on major state changes

## Tool Execution Models

### Frontend Tool Execution

**Execute in Browser/Client When:**
- Need access to client-side resources (camera, GPS, local files)
- UI operations (show modal, update display)
- Low-latency interactions
- Privacy-sensitive operations (keep data local)

**Examples:**
- Capture photo from webcam
- Read local file
- Update UI component
- Geolocation access

**Implementation:**
```typescript
const tools = [
  {
    name: "capture_screenshot",
    description: "Capture browser screenshot",
    executionLocation: "frontend", // Execute in browser
    handler: async () => {
      // Browser-only functionality
      return await captureScreen();
    }
  }
];
```

**Tradeoffs:**
- ✅ Access to browser APIs
- ✅ Lower latency for UI operations
- ✅ Privacy (data stays local)
- ❌ Security constraints (no server resources)
- ❌ Limited computational power
- ❌ User-specific results (not shareable)

### Backend Tool Execution

**Execute on Server When:**
- Need access to databases, APIs, secrets
- Heavy computation required
- Shared resources (multiple users)
- Security-sensitive operations

**Examples:**
- Database queries
- API calls to third-party services
- File processing on server
- Cryptographic operations

**Implementation:**
```python
tools = [
    {
        "name": "query_database",
        "description": "Query internal database",
        "executionLocation": "backend",  # Execute on server
    }
]

# Server handles execution
async def execute_tool(tool_name, args):
    if tool_name == "query_database":
        return await db.query(args["query"])
```

**Tradeoffs:**
- ✅ Access to server resources
- ✅ More computational power
- ✅ Secure credential management
- ❌ Higher latency (network round trip)
- ❌ No access to client resources
- ❌ Scaling considerations

### Hybrid Tool Execution

**Use Both When:**
- Complex workflows need both client and server capabilities
- Some tools client-side, others server-side

**Example:**
```typescript
const tools = [
  // Client-side
  {
    name: "capture_image",
    executionLocation: "frontend",
    handler: async () => captureFromCamera()
  },

  // Server-side
  {
    name: "analyze_image",
    executionLocation: "backend"
    // Server will process the image
  }
];

// Workflow:
// 1. Agent calls capture_image (executes in browser)
// 2. Agent receives image data
// 3. Agent calls analyze_image with image (executes on server)
// 4. Agent returns analysis to user
```

## Sub-Agent Composition Patterns

### Pattern 1: Transparent Pass-Through

**When to Use:**
- Sub-agent events should reach frontend unchanged
- User needs full visibility into sub-agent operations

**Implementation:**
```python
# Main agent forwards all sub-agent events
async def run_with_subagent(input):
    emit_event({"type": "RUN_STARTED", ...})

    # Run sub-agent
    sub_stream = sub_agent.run(sub_input)

    # Forward all events
    async for event in sub_stream:
        emit_event(event)  # Pass through

    emit_event({"type": "RUN_FINISHED", ...})
```

### Pattern 2: Aggregated Events

**When to Use:**
- Sub-agent details not relevant to user
- Simplify frontend event handling
- Consolidate multiple sub-agents

**Implementation:**
```python
async def run_with_aggregation(input):
    emit_event({"type": "RUN_STARTED", ...})

    # Collect all text from sub-agent
    sub_result = ""
    async for event in sub_agent.run(sub_input):
        if event.type == "TEXT_MESSAGE_CONTENT":
            sub_result += event.delta
        # Don't forward individual events

    # Emit consolidated result
    emit_event({
        "type": "TEXT_MESSAGE_START",
        "messageId": "main-msg",
        "role": "assistant"
    })
    emit_event({
        "type": "TEXT_MESSAGE_CONTENT",
        "messageId": "main-msg",
        "delta": f"Sub-agent result: {sub_result}"
    })
    emit_event({
        "type": "TEXT_MESSAGE_END",
        "messageId": "main-msg"
    })

    emit_event({"type": "RUN_FINISHED", ...})
```

### Pattern 3: Transformed Events

**When to Use:**
- Need to modify sub-agent events before forwarding
- Add context or metadata
- Filter or enrich events

**Implementation:**
```python
async def run_with_transformation(input):
    emit_event({"type": "RUN_STARTED", ...})

    async for event in sub_agent.run(sub_input):
        # Transform event
        if event.type == "TEXT_MESSAGE_CONTENT":
            # Add context to sub-agent output
            transformed_event = {
                **event,
                "metadata": {
                    "source": "sub-agent-1",
                    "confidence": 0.95
                }
            }
            emit_event(transformed_event)
        else:
            emit_event(event)

    emit_event({"type": "RUN_FINISHED", ...})
```

## Human-in-the-Loop Design

### Pattern 1: Agent Pause for Input

**When to Use:**
- Need user confirmation before proceeding
- Collect additional information mid-execution
- User approval for actions

**Flow:**
```
1. Agent executes initial steps
2. Agent emits STATE_SNAPSHOT showing current state
3. Agent emits CUSTOM event: {"type": "CUSTOM", "action": "AWAITING_USER_INPUT"}
4. Frontend displays prompt to user
5. User provides input
6. Frontend sends new message to agent
7. Agent resumes execution
```

**Implementation:**
```python
async def run_with_user_input(input):
    # Initial steps
    emit_event({"type": "TEXT_MESSAGE_CONTENT", "delta": "I need to delete 100 files. "})

    # Request user confirmation
    emit_event({
        "type": "CUSTOM",
        "action": "REQUEST_CONFIRMATION",
        "prompt": "Do you want to proceed with deleting 100 files?",
        "options": ["Yes", "No"]
    })

    # Wait for user response (via new message)
    user_response = await wait_for_user_message()

    if user_response == "Yes":
        # Proceed with deletion
        emit_event({"type": "TEXT_MESSAGE_CONTENT", "delta": "Deleting files..."})
        delete_files()
    else:
        emit_event({"type": "TEXT_MESSAGE_CONTENT", "delta": "Operation cancelled."})
```

### Pattern 2: Real-Time Steering

**When to Use:**
- User wants to guide agent mid-execution
- Adjust parameters on the fly
- Collaborative problem-solving

**Requires:** WebSocket transport (bidirectional)

**Flow:**
```
1. Agent starts execution
2. Agent emits events showing progress
3. User sends steering input mid-execution
4. Agent adjusts behavior based on input
5. Agent continues with new direction
```

## Security & Privacy Patterns

### Secure Proxy Pattern

**When to Use:**
- Need to inject authentication
- Rate limiting required
- Logging and monitoring
- Security policies enforcement

**Architecture:**
```
┌──────────┐        ┌──────────────┐        ┌────────┐
│ Frontend │ ◄────► │ Secure Proxy │ ◄────► │ Agent  │
│ (Public) │        │  (Backend)   │        │(Private)│
└──────────┘        └──────────────┘        └────────┘
                           │
                           ├─ Auth verification
                           ├─ Rate limiting
                           ├─ Request logging
                           └─ Policy enforcement
```

**Implementation:**
```python
# Proxy server
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.post("/agent/run")
async def proxy_agent_run(
    request: RunAgentInput,
    authorization: str = Header(...)
):
    # Verify auth
    user = verify_token(authorization)
    if not user:
        raise HTTPException(401, "Unauthorized")

    # Rate limiting
    if not check_rate_limit(user.id):
        raise HTTPException(429, "Too many requests")

    # Log request
    log_request(user.id, request)

    # Forward to agent (with internal auth)
    agent = HttpAgent(
        base_url="https://internal-agent.private",
        headers={"X-Internal-Auth": INTERNAL_TOKEN}
    )

    event_stream = agent.run(request)

    # Stream events to frontend
    async for event in event_stream:
        yield event
```

## Performance Optimization

### Event Batching

**When to Use:**
- High-frequency state updates
- Network latency concerns
- Reduce frontend re-renders

**Pattern:**
```typescript
// Instead of sending individual deltas
emit({type: "STATE_DELTA", delta: [{op: "replace", path: "/counter", value: 1}]})
emit({type: "STATE_DELTA", delta: [{op: "replace", path: "/counter", value: 2}]})
emit({type: "STATE_DELTA", delta: [{op: "replace", path: "/counter", value: 3}]})

// Batch into single delta
emit({
  type: "STATE_DELTA",
  delta: [
    {op: "replace", path: "/counter", value: 1},
    {op: "replace", path: "/counter", value: 2},
    {op: "replace", path: "/counter", value: 3}
  ]
})
```

### Compression

**For Large Payloads:**
```python
import gzip
import json

def compress_event(event):
    """Compress large events."""
    json_str = json.dumps(event)

    if len(json_str) > 1024:  # > 1KB
        compressed = gzip.compress(json_str.encode())
        return {
            "type": "COMPRESSED",
            "data": base64.b64encode(compressed).decode(),
            "encoding": "gzip"
        }

    return event
```

## Best Practices Summary

1. **Start Simple** - Use SSE and snapshots, optimize later
2. **Progressive Enhancement** - Add features (deltas, WebSockets) as needed
3. **Type Safety** - Leverage TypeScript/Python types
4. **Error Handling** - Always handle errors gracefully
5. **State Consistency** - Use periodic snapshots to prevent drift
6. **Security** - Use secure proxy for auth and rate limiting
7. **Testing** - Mock event streams for testing
8. **Monitoring** - Log events for debugging and analytics

## Anti-Patterns to Avoid

❌ **Over-Engineering**
- Don't use deltas for small state
- Don't use WebSockets if SSE works
- Don't split into sub-agents unnecessarily

❌ **Poor Error Handling**
- Don't ignore RUN_ERROR events
- Don't crash on unexpected event types
- Don't expose internal errors to users

❌ **State Management Issues**
- Don't send only deltas (periodic snapshots needed)
- Don't mutate state without emitting events
- Don't skip state synchronization

❌ **Security Mistakes**
- Don't expose internal agent endpoints publicly
- Don't send sensitive data in events
- Don't trust client-side tool execution for security

## Next Steps

- See `protocol-fundamentals.md` for event system details
- See `typescript-implementation.md` or `python-implementation.md` for code examples
- See `troubleshooting.md` for debugging guidance
- Check `../assets/integration-checklist.md` for implementation checklist
