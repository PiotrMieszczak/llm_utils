# AG-UI Protocol Fundamentals

Core concepts, architecture, and event system of the AG-UI protocol.

## What is AG-UI?

AG-UI (Agent User Interaction Protocol) is an **open, lightweight, event-based protocol** that standardizes communication between AI agents and user-facing applications. It solves the fundamental mismatch between traditional REST/GraphQL APIs and the dynamic, long-running, non-deterministic nature of AI agents.

### The Problem It Solves

Traditional web APIs struggle with agent characteristics:
- **Long-running operations** - Agents may take seconds to minutes to complete
- **Nondeterministic behavior** - Same input can produce different outputs
- **Mixed IO patterns** - Structured data (JSON) mixed with unstructured text streams
- **Real-time interaction** - Users need to see thinking, intermediate steps, and provide input mid-execution
- **State synchronization** - Complex agent state needs efficient frontend representation

AG-UI addresses these by providing an event-based abstraction specifically designed for agentic systems.

## Architecture Overview

### High-Level Components

```
┌─────────────┐         ┌──────────────┐         ┌─────────┐
│ Application │ ◄─────► │  AG-UI       │ ◄─────► │  Agent  │
│  (Frontend) │         │  Client      │         │ (Backend)│
└─────────────┘         └──────────────┘         └─────────┘
                              │
                              ▼
                        ┌──────────────┐
                        │ Secure Proxy │ (Optional)
                        │  (Backend)   │
                        └──────────────┘
```

**Components:**
1. **Application** - User-facing interface (chat UI, AI-enabled tool)
2. **AG-UI Client** - Communication layer (e.g., HttpAgent)
3. **Agent** - Backend AI system processing requests
4. **Secure Proxy** - Optional service for additional capabilities (authentication, tool execution)

### Client-Server Model

AG-UI follows a client-server architecture where:
- **Client** initiates agent execution via `run(input: RunAgentInput)`
- **Server** (agent) emits events as execution progresses
- **Events** flow as an observable stream: `Observable<BaseEvent>`

### Design Principles

1. **Event-Driven Communication** - Agents emit standardized events during execution
2. **Lightweight Flexibility** - Events just need to be "AG-UI-compatible," not exact format matches
3. **Bidirectional Interaction** - Supports human-in-the-loop and collaborative workflows
4. **Transport Agnostic** - Works over SSE, WebSockets, binary protocols, or custom transports

## Event System

### Core Event Categories

#### 1. Lifecycle Events

Track run initialization and progression:

- **RUN_STARTED** - Agent execution begins
  - Contains run_id, configuration, initial state
  - First event in any stream

- **RUN_FINISHED** - Normal completion
  - Final state, execution summary
  - Signals successful termination

- **RUN_ERROR** - Error termination
  - Error details, stack trace
  - Indicates failure state

#### 2. Text Message Events

Enable streaming assistant responses:

- **TEXT_MESSAGE_START** - Begin new message
  - Message ID, role (assistant/user)
  - Metadata and context

- **TEXT_MESSAGE_CONTENT** - Stream text content
  - Incremental text chunks (delta)
  - Enables token-by-token streaming

- **TEXT_MESSAGE_END** - Complete message
  - Final content, metadata
  - Marks message completion

#### 3. Tool Call Events

Manage function execution lifecycle:

- **TOOL_CALL_START** - Tool invocation begins
  - Tool name, call ID
  - Context for execution

- **TOOL_CALL_ARGS** - Stream tool arguments
  - Incremental JSON arguments
  - Enables large payload streaming

- **TOOL_CALL_END** - Tool execution completes
  - Return value or error
  - Execution metadata

#### 4. State Management Events

Coordinate agent state synchronization:

- **STATE_SNAPSHOT** - Complete state transmission
  - Full state object
  - Used for initialization or reset

- **STATE_DELTA** - Incremental state update
  - JSON Patch (RFC 6902) operations
  - Minimizes data transfer

- **MESSAGES_SNAPSHOT** - Complete message history
  - All messages in current run
  - Useful for context reconstruction

#### 5. Special Events

Support extensibility and custom needs:

- **RAW** - Pass-through arbitrary data
  - No schema validation
  - Framework-specific extensions

- **CUSTOM** - Domain-specific events
  - User-defined event types
  - Custom business logic

### Event Flow Pattern

Typical event sequence for an agent run:

```
1. RUN_STARTED
2. STATE_SNAPSHOT (initial state)
3. TEXT_MESSAGE_START (assistant thinking)
4. TEXT_MESSAGE_CONTENT (streaming tokens...)
5. TEXT_MESSAGE_CONTENT (more tokens...)
6. TEXT_MESSAGE_END
7. TOOL_CALL_START (agent invokes tool)
8. TOOL_CALL_ARGS (tool parameters)
9. TOOL_CALL_END (tool result)
10. TEXT_MESSAGE_START (response with tool result)
11. TEXT_MESSAGE_CONTENT (streaming response...)
12. TEXT_MESSAGE_END
13. STATE_DELTA (update agent state)
14. RUN_FINISHED
```

## State Management

### State Synchronization Strategies

AG-UI provides two mechanisms for keeping frontend and backend state in sync:

#### 1. Snapshots (STATE_SNAPSHOT)

**Use Case:** Full state transmission

```json
{
  "type": "STATE_SNAPSHOT",
  "state": {
    "conversation": {...},
    "userPreferences": {...},
    "agentMemory": {...}
  }
}
```

**When to Use:**
- Initial state transmission at run start
- State reset or reload
- After significant state changes
- Reconnection after disconnect

**Tradeoffs:**
- ✅ Simple, complete state representation
- ✅ No risk of state drift
- ❌ Large payload for complex state
- ❌ Inefficient for small changes

#### 2. Deltas (STATE_DELTA)

**Use Case:** Incremental updates via JSON Patch (RFC 6902)

```json
{
  "type": "STATE_DELTA",
  "delta": [
    {"op": "replace", "path": "/userPreferences/theme", "value": "dark"},
    {"op": "add", "path": "/agentMemory/facts/-", "value": "User prefers Python"}
  ]
}
```

**JSON Patch Operations:**
- `add` - Insert new value
- `remove` - Delete value
- `replace` - Update existing value
- `move` - Relocate value
- `copy` - Duplicate value
- `test` - Assert value (for conflict detection)

**When to Use:**
- Frequent small updates
- Large state objects
- Network efficiency matters
- Incremental state evolution

**Tradeoffs:**
- ✅ Minimal data transfer
- ✅ Efficient for large state
- ❌ More complex to implement
- ❌ Requires state consistency management

### State Management Best Practices

1. **Start with Snapshot** - Send STATE_SNAPSHOT on RUN_STARTED
2. **Use Deltas for Updates** - Switch to STATE_DELTA during execution
3. **Periodic Snapshots** - Occasionally send full snapshots to prevent drift
4. **Conflict Resolution** - Use JSON Patch `test` operation for optimistic updates

## Transport Mechanisms

AG-UI is transport-agnostic but commonly uses:

### 1. Server-Sent Events (SSE)

**Standard HTTP Transport:**
```
POST /agent/run
Content-Type: application/json

Response: text/event-stream
```

**Characteristics:**
- ✅ HTTP/1.1 compatible
- ✅ Firewall-friendly
- ✅ Simple to implement
- ❌ Text-based (larger payloads)
- ❌ Unidirectional (client can't send mid-stream)

**Use When:**
- Maximum compatibility needed
- Simple request-response with streaming
- Firewall/proxy constraints

### 2. Binary Protocol

**Custom Efficient Transport:**

**Characteristics:**
- ✅ Compact payloads
- ✅ High performance
- ✅ Efficient serialization
- ❌ More complex implementation
- ❌ May require custom infrastructure

**Use When:**
- Performance critical
- Large data volumes
- Controlled network environment

### 3. WebSockets

**Full Duplex Communication:**

**Characteristics:**
- ✅ Bidirectional real-time communication
- ✅ Low latency
- ✅ Connection persistence
- ❌ More complex than SSE
- ❌ May have proxy/firewall issues

**Use When:**
- Human-in-the-loop interaction needed
- Real-time agent steering
- Collaborative agent workflows

### 4. Custom Transports

AG-UI's flexibility allows:
- Webhooks
- Message queues (RabbitMQ, Kafka)
- gRPC streams
- Custom protocols

## Protocol Philosophy

### AG-UI vs Traditional APIs

| Aspect | REST/GraphQL | AG-UI |
|--------|--------------|-------|
| Communication | Request-Response | Event Stream |
| State | Stateless | Stateful with sync |
| Timing | Immediate | Long-running |
| Data Flow | Pull-based | Push-based |
| Uncertainty | Deterministic | Handles non-determinism |
| Interactivity | Single request | Bidirectional dialogue |

### AG-UI vs Other Agent Protocols

**MCP (Model Context Protocol):**
- Purpose: Connect agents to **tools and context**
- Scope: Agent ↔ Tool Server
- Use together: AG-UI for UI, MCP for tools

**A2A (Agent-to-Agent Protocol):**
- Purpose: Connect **agents to other agents**
- Scope: Agent ↔ Agent
- Use together: AG-UI for UI, A2A for agent composition

**AG-UI:**
- Purpose: Connect agents to **user-facing applications**
- Scope: Agent ↔ Frontend
- Primary use: User interaction layer

### Complementary Protocol Stack

```
┌──────────────────────────────┐
│    User Interface (AG-UI)    │
├──────────────────────────────┤
│    Agent System (A2A)        │
├──────────────────────────────┤
│    Tools & Context (MCP)     │
└──────────────────────────────┘
```

## Advanced Concepts

### Sub-Agent Composition

AG-UI supports hierarchical agent systems:

```
Main Agent (AG-UI to Frontend)
  └─> Sub-Agent 1 (Internal)
  └─> Sub-Agent 2 (Internal)
        └─> Sub-Agent 2.1 (Internal)
```

Events from sub-agents can be:
- Aggregated by parent
- Passed through transparently
- Transformed before forwarding

### Human-in-the-Loop

AG-UI enables user interrupts during execution:

1. Agent emits events showing current state
2. User provides input or correction
3. Agent adjusts execution based on feedback
4. Execution continues with new context

### Tool Execution Models

**Frontend Tools:**
- Execute in browser/client
- Access local resources (files, camera, GPS)
- Lower latency for UI operations

**Backend Tools:**
- Execute on server
- Access databases, APIs, secure resources
- Better for heavy computation

AG-UI supports both via tool definition parameters.

## Getting Started

To implement AG-UI:

1. **Choose SDK** - TypeScript (`@ag-ui/core`) or Python (`ag-ui-protocol`)
2. **Design Event Flow** - Map your agent's execution to event types
3. **Implement Agent** - Emit AG-UI events during execution
4. **Setup Client** - Use HttpAgent or custom client
5. **Handle Events** - Process event stream in frontend

See `typescript-implementation.md` and `python-implementation.md` for detailed SDK guidance.

## Key Takeaways

- AG-UI is **event-driven**, not request-response
- Events are **strongly typed** but **flexibly structured**
- State management uses **snapshots and deltas** efficiently
- **Transport agnostic** - works over SSE, WebSockets, binary, etc.
- **Complements** MCP (tools) and A2A (agents), doesn't replace them
- Designed for **long-running, interactive, non-deterministic** agent workflows
