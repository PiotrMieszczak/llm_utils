# AG-UI Event Flow Template

Template for designing and documenting AG-UI event flows for your agent implementations.

## Template Structure

Use this template when planning your agent's event emissions:

```markdown
# Event Flow: [Feature Name]

## Overview
Brief description of what this flow accomplishes

## Trigger
What initiates this flow (user action, system event, etc.)

## Event Sequence
Ordered list of events with descriptions

## State Changes
What state updates occur during this flow

## Error Scenarios
How errors are handled and what events are emitted

## Performance Considerations
Expected throughput, timing, data volumes
```

---

## Example 1: Simple Text Response

### Overview
User asks a question, agent responds with text

### Trigger
User sends message via chat interface

### Event Sequence

```
1. RUN_STARTED
   - run_id: "run-123"
   - timestamp: "2024-01-15T10:00:00Z"

2. STATE_SNAPSHOT
   - state: { conversation: { messageCount: 1 } }

3. TEXT_MESSAGE_START
   - messageId: "msg-456"
   - role: "assistant"

4. TEXT_MESSAGE_CONTENT (repeated)
   - messageId: "msg-456"
   - delta: "Hello..." (streaming tokens)

5. TEXT_MESSAGE_END
   - messageId: "msg-456"

6. STATE_DELTA
   - delta: [{ op: "replace", path: "/conversation/messageCount", value: 2 }]

7. RUN_FINISHED
   - run_id: "run-123"
   - duration_ms: 1250
```

### State Changes
- `conversation.messageCount`: 1 → 2
- `conversation.lastMessageTime`: updated to current timestamp

### Error Scenarios
- **Timeout**: Emit RUN_ERROR with timeout message
- **API Failure**: Emit RUN_ERROR with error details

### Performance Considerations
- Expected duration: 1-3 seconds
- Token rate: ~50 tokens/second
- Event count: ~55 events (1 start + 50 content + 4 lifecycle/state)

---

## Example 2: Tool Execution Flow

### Overview
Agent needs to call external tool to answer user question

### Trigger
User asks question requiring real-time data (e.g., "What's the weather?")

### Event Sequence

```
1. RUN_STARTED
   - run_id: "run-789"

2. STATE_SNAPSHOT
   - state: { conversation: { messageCount: 3 } }

3. TEXT_MESSAGE_START
   - messageId: "msg-101"
   - role: "assistant"

4. TEXT_MESSAGE_CONTENT
   - messageId: "msg-101"
   - delta: "Let me check the weather for you..."

5. TEXT_MESSAGE_END
   - messageId: "msg-101"

6. TOOL_CALL_START
   - toolCallId: "tool-202"
   - toolName: "get_weather"

7. TOOL_CALL_ARGS
   - toolCallId: "tool-202"
   - arguments: { location: "San Francisco", units: "celsius" }

8. TOOL_CALL_END
   - toolCallId: "tool-202"
   - result: { temperature: 18, conditions: "partly cloudy" }

9. TEXT_MESSAGE_START
   - messageId: "msg-102"
   - role: "assistant"

10. TEXT_MESSAGE_CONTENT (repeated)
    - messageId: "msg-102"
    - delta: "The current temperature in San Francisco is 18°C..."

11. TEXT_MESSAGE_END
    - messageId: "msg-102"

12. STATE_DELTA
    - delta: [
        { op: "replace", path: "/conversation/messageCount", value: 5 },
        { op: "add", path: "/toolUsage/get_weather", value: 1 }
      ]

13. RUN_FINISHED
    - run_id: "run-789"
```

### State Changes
- `conversation.messageCount`: 3 → 5 (two assistant messages)
- `toolUsage.get_weather`: undefined → 1
- `conversation.lastToolCall`: updated with tool details

### Error Scenarios

**Tool Execution Failure:**
```
6. TOOL_CALL_START
   - toolCallId: "tool-202"
   - toolName: "get_weather"

7. TOOL_CALL_ARGS
   - toolCallId: "tool-202"
   - arguments: { location: "San Francisco" }

8. TOOL_CALL_END
   - toolCallId: "tool-202"
   - error: "API rate limit exceeded"

9. TEXT_MESSAGE_START
   - messageId: "msg-102"
   - role: "assistant"

10. TEXT_MESSAGE_CONTENT
    - messageId: "msg-102"
    - delta: "I'm unable to fetch weather data right now. Please try again later."

11. TEXT_MESSAGE_END
    - messageId: "msg-102"

12. RUN_FINISHED
```

### Performance Considerations
- Expected duration: 2-5 seconds
- Tool latency: 500ms-2s
- Event count: ~70 events
- Network dependency: External weather API

---

## Example 3: Multi-Step Reasoning with State Updates

### Overview
Agent performs multi-step analysis with intermediate state updates

### Trigger
User requests complex analysis requiring multiple reasoning steps

### Event Sequence

```
1. RUN_STARTED
   - run_id: "run-333"

2. STATE_SNAPSHOT
   - state: {
       conversation: { messageCount: 10 },
       analysis: { stage: "idle", progress: 0 }
     }

3. STATE_DELTA
   - delta: [
       { op: "replace", path: "/analysis/stage", value: "analyzing" },
       { op: "replace", path: "/analysis/progress", value: 0.1 }
     ]

4. TEXT_MESSAGE_START
   - messageId: "msg-401"
   - role: "assistant"

5. TEXT_MESSAGE_CONTENT
   - messageId: "msg-401"
   - delta: "Step 1: Analyzing input data..."

6. TEXT_MESSAGE_END
   - messageId: "msg-401"

7. STATE_DELTA
   - delta: [{ op: "replace", path: "/analysis/progress", value: 0.3 }]

8. TEXT_MESSAGE_START
   - messageId: "msg-402"
   - role: "assistant"

9. TEXT_MESSAGE_CONTENT
   - messageId: "msg-402"
   - delta: "Step 2: Comparing with historical patterns..."

10. TEXT_MESSAGE_END
    - messageId: "msg-402"

11. STATE_DELTA
    - delta: [{ op: "replace", path: "/analysis/progress", value: 0.6 }]

12. TEXT_MESSAGE_START
    - messageId: "msg-403"
    - role: "assistant"

13. TEXT_MESSAGE_CONTENT
    - messageId: "msg-403"
    - delta: "Step 3: Generating recommendations..."

14. TEXT_MESSAGE_END
    - messageId: "msg-403"

15. STATE_DELTA
    - delta: [
        { op: "replace", path: "/analysis/progress", value: 1.0 },
        { op: "replace", path: "/analysis/stage", value: "complete" }
      ]

16. TEXT_MESSAGE_START
    - messageId: "msg-404"
    - role: "assistant"

17. TEXT_MESSAGE_CONTENT (repeated)
    - messageId: "msg-404"
    - delta: "Based on my analysis, here are the recommendations..."

18. TEXT_MESSAGE_END
    - messageId: "msg-404"

19. RUN_FINISHED
    - run_id: "run-333"
```

### State Changes
- `analysis.stage`: "idle" → "analyzing" → "complete"
- `analysis.progress`: 0 → 0.1 → 0.3 → 0.6 → 1.0
- `conversation.messageCount`: 10 → 14

### Error Scenarios
- Analysis failure at any step emits RUN_ERROR
- State reverts to `analysis.stage: "error"`

### Performance Considerations
- Expected duration: 10-30 seconds
- Progress updates every 2-5 seconds
- Use deltas for frequent progress updates
- Consider periodic snapshots (every 10-20 deltas)

---

## Example 4: Human-in-the-Loop Confirmation

### Overview
Agent requests user confirmation before executing action

### Trigger
Agent needs to perform sensitive operation (delete files, send email, etc.)

### Event Sequence

```
1. RUN_STARTED
   - run_id: "run-555"

2. TEXT_MESSAGE_START
   - messageId: "msg-601"
   - role: "assistant"

3. TEXT_MESSAGE_CONTENT
   - messageId: "msg-601"
   - delta: "I'm about to delete 100 old files. "

4. TEXT_MESSAGE_END
   - messageId: "msg-601"

5. CUSTOM (Request Confirmation)
   - action: "REQUEST_CONFIRMATION"
   - confirmationId: "conf-777"
   - prompt: "Do you want to proceed with deleting 100 files?"
   - options: ["Yes, proceed", "No, cancel"]
   - metadata: {
       files_to_delete: 100,
       estimated_space_freed: "5GB"
     }

6. STATE_DELTA
   - delta: [
       { op: "replace", path: "/pendingAction", value: {
           id: "conf-777",
           type: "file_deletion",
           status: "awaiting_confirmation"
         }}
     ]

[... Agent pauses, waiting for user response ...]

[User responds with new message: "Yes, proceed"]

7. TEXT_MESSAGE_START
   - messageId: "msg-602"
   - role: "assistant"

8. TEXT_MESSAGE_CONTENT
   - messageId: "msg-602"
   - delta: "Deleting files..."

9. TEXT_MESSAGE_END
   - messageId: "msg-602"

10. TOOL_CALL_START
    - toolCallId: "tool-888"
    - toolName: "delete_files"

11. TOOL_CALL_END
    - toolCallId: "tool-888"
    - result: { deleted: 100, space_freed: "5.2GB" }

12. TEXT_MESSAGE_START
    - messageId: "msg-603"
    - role: "assistant"

13. TEXT_MESSAGE_CONTENT
    - messageId: "msg-603"
    - delta: "Successfully deleted 100 files, freeing 5.2GB of space."

14. TEXT_MESSAGE_END
    - messageId: "msg-603"

15. STATE_DELTA
    - delta: [{ op: "remove", path: "/pendingAction" }]

16. RUN_FINISHED
    - run_id: "run-555"
```

### State Changes
- `pendingAction`: undefined → confirmation details → removed
- User cancellation path would skip tool execution

### Error Scenarios
- User cancels: Skip tool execution, emit cancellation message
- Tool execution fails: Emit error in TOOL_CALL_END

### Performance Considerations
- Variable duration (depends on user response time)
- Connection must stay open during user input
- Consider timeout for user response (e.g., 5 minutes)

---

## Creating Your Own Flow

### Step 1: Define the Scenario
```markdown
# Event Flow: [Your Feature Name]

## Overview
[What does this flow accomplish?]

## Trigger
[What initiates this flow?]
```

### Step 2: Map Event Sequence
List events in order with:
- Event type
- Key fields
- Purpose

### Step 3: Document State Changes
- Initial state
- Intermediate changes
- Final state

### Step 4: Plan Error Handling
- What can go wrong?
- What events to emit on error?
- How to recover?

### Step 5: Performance Estimates
- Expected duration
- Event count
- Data volumes
- Network dependencies

---

## Best Practices

1. **Always Start with RUN_STARTED**
   - Provides run_id for tracking
   - Establishes execution context

2. **Always End with RUN_FINISHED or RUN_ERROR**
   - Signals completion to frontend
   - Allows cleanup and UI state updates

3. **Send Initial STATE_SNAPSHOT**
   - Establishes baseline state
   - Prevents synchronization issues

4. **Use Deltas for Frequent Updates**
   - More efficient than snapshots
   - Good for progress indicators, counters

5. **Periodic Snapshots**
   - Every 50 deltas or major state change
   - Prevents drift from accumulated deltas

6. **Message Lifecycle**
   - START before any CONTENT
   - END after all CONTENT
   - Use unique messageId for tracking

7. **Tool Call Lifecycle**
   - START before ARGS
   - ARGS before END
   - Include result or error in END

8. **Error Events**
   - Emit RUN_ERROR for fatal errors
   - Include error message and context
   - Still emit RUN_FINISHED after (if applicable)

9. **Custom Events**
   - Use CUSTOM for domain-specific needs
   - Document custom event structure
   - Ensure frontend can handle them

10. **Performance**
    - Batch updates when possible
    - Don't emit unnecessary events
    - Consider network latency

---

## Validation Checklist

Before implementing your flow:

- [ ] All events have required fields
- [ ] Event sequence is logical and complete
- [ ] State transitions are clearly defined
- [ ] Error scenarios are handled
- [ ] Performance characteristics are acceptable
- [ ] Message lifecycle is correct (START → CONTENT → END)
- [ ] Tool calls are properly structured
- [ ] Initial snapshot is sent
- [ ] Periodic snapshots planned (if using deltas)
- [ ] RUN_FINISHED or RUN_ERROR always emitted

---

Use this template as a planning and communication tool when designing AG-UI implementations. Share with your team to align on expected behavior and event structures.
