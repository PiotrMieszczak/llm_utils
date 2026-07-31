# AG-UI Python Implementation Guide

Complete guide to implementing AG-UI in Python applications.

## Installation

Install the AG-UI Python SDK via pip:

```bash
pip install ag-ui-protocol
```

**Python Version Requirements:**
- Python 3.8+
- Recommended: Python 3.10+ for best type hint support

**Optional Dependencies:**
```bash
# For async support
pip install aiohttp

# For type checking
pip install mypy
```

## Core Architecture

The Python SDK provides a **streaming event-based architecture with strongly typed data structures** using Python's type hints and dataclasses.

### Package Structure

```python
from ag_ui.core import (
    # Client
    HttpAgent,

    # Base types
    RunAgentInput,
    BaseEvent,
    Message,
    Tool,
    Context,
    State,

    # Event types
    RunStartedEvent,
    RunFinishedEvent,
    RunErrorEvent,
    TextMessageStartEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
    ToolCallStartEvent,
    ToolCallEndEvent,
    StateSnapshotEvent,
    StateDeltaEvent,
)

from ag_ui.encoder import (
    # Serialization utilities
    encode_event_stream,
    decode_event_stream,
)
```

## HttpAgent - Standard Client

The primary way to connect to AG-UI agents in Python.

### Basic Setup

```python
from ag_ui.core import HttpAgent

# Create client
agent = HttpAgent(
    base_url="https://your-agent-api.com",
    # Optional configuration
    headers={
        "Authorization": "Bearer YOUR_TOKEN",
        "Custom-Header": "value"
    },
    timeout=30.0,  # 30 seconds
)
```

### Running an Agent (Synchronous)

```python
from ag_ui.core import RunAgentInput, Message

# Prepare input
input_data = RunAgentInput(
    messages=[
        Message(
            role="user",
            content="Help me plan a trip to Tokyo"
        )
    ],

    config={
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 2000
    },

    tools=[
        {
            "name": "search_flights",
            "description": "Search for available flights",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "date": {"type": "string"}
                },
                "required": ["origin", "destination", "date"]
            }
        }
    ],

    context={
        "user_id": "user-123",
        "session_id": "session-456",
        "preferences": {
            "language": "en",
            "timezone": "America/New_York"
        }
    }
)

# Execute agent - returns Generator[BaseEvent, None, None]
event_stream = agent.run(input_data)

# Process events
for event in event_stream:
    print(f"Event received: {event.type}")
    handle_event(event)
```

### Running an Agent (Asynchronous)

```python
import asyncio
from ag_ui.core import AsyncHttpAgent

async def run_agent():
    agent = AsyncHttpAgent(
        base_url="https://your-agent-api.com"
    )

    input_data = RunAgentInput(
        messages=[Message(role="user", content="Hello")]
    )

    # Returns AsyncGenerator[BaseEvent, None]
    event_stream = agent.run(input_data)

    async for event in event_stream:
        print(f"Event: {event.type}")
        await handle_event(event)

# Run async function
asyncio.run(run_agent())
```

## Event Stream Handling

### Type-Safe Event Handling

```python
from ag_ui.core import BaseEvent
from typing import Any

def handle_event(event: BaseEvent) -> None:
    """Process AG-UI events with type safety."""

    match event.type:
        case "RUN_STARTED":
            handle_run_started(event)

        case "TEXT_MESSAGE_START":
            handle_message_start(event)

        case "TEXT_MESSAGE_CONTENT":
            handle_message_content(event)

        case "TEXT_MESSAGE_END":
            handle_message_end(event)

        case "TOOL_CALL_START":
            handle_tool_call_start(event)

        case "TOOL_CALL_END":
            handle_tool_call_end(event)

        case "STATE_SNAPSHOT":
            handle_state_snapshot(event)

        case "STATE_DELTA":
            handle_state_delta(event)

        case "RUN_FINISHED":
            handle_run_finished(event)

        case "RUN_ERROR":
            handle_run_error(event)

        case _:
            print(f"Unknown event type: {event.type}")


def handle_message_content(event: TextMessageContentEvent) -> None:
    """Handle streaming message content."""
    print(event.delta, end="", flush=True)


def handle_tool_call_start(event: ToolCallStartEvent) -> None:
    """Handle tool call initiation."""
    print(f"\nCalling tool: {event.tool_name}")


def handle_run_error(event: RunErrorEvent) -> None:
    """Handle execution errors."""
    print(f"Error: {event.error}")
```

### Flask Integration Example

```python
from flask import Flask, request, jsonify, stream_with_context, Response
from ag_ui.core import HttpAgent, RunAgentInput, Message
import json

app = Flask(__name__)

agent = HttpAgent(base_url="https://backend-agent.com")

@app.route("/chat", methods=["POST"])
def chat():
    """Stream chat responses using AG-UI."""

    data = request.json
    user_message = data.get("message", "")

    input_data = RunAgentInput(
        messages=[Message(role="user", content=user_message)]
    )

    def generate():
        """Generator for SSE streaming."""
        event_stream = agent.run(input_data)

        for event in event_stream:
            # Convert event to JSON
            event_json = json.dumps({
                "type": event.type,
                "data": event.__dict__
            })

            # SSE format
            yield f"data: {event_json}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )

if __name__ == "__main__":
    app.run(debug=True)
```

### FastAPI Integration Example

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from ag_ui.core import AsyncHttpAgent, RunAgentInput, Message
from pydantic import BaseModel
import json

app = FastAPI()

agent = AsyncHttpAgent(base_url="https://backend-agent.com")

class ChatRequest(BaseModel):
    message: str
    context: dict = {}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Stream chat responses using AG-UI with FastAPI."""

    input_data = RunAgentInput(
        messages=[Message(role="user", content=request.message)],
        context=request.context
    )

    async def event_generator():
        """Async generator for SSE streaming."""
        event_stream = agent.run(input_data)

        async for event in event_stream:
            event_json = json.dumps({
                "type": event.type,
                "data": event.dict()
            })

            yield f"data: {event_json}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
```

## Working with Messages

### Message Structure

```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Message:
    role: str  # "user" | "assistant" | "system"
    content: str

    # Optional fields
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[dict]] = None
```

### Streaming Message Manager

```python
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class StreamingMessage:
    id: str
    role: str
    content: str = ""
    is_complete: bool = False

class MessageManager:
    """Manage streaming messages from AG-UI events."""

    def __init__(self):
        self.messages: Dict[str, StreamingMessage] = {}

    def handle_event(self, event: BaseEvent) -> None:
        """Update message state based on event."""

        match event.type:
            case "TEXT_MESSAGE_START":
                self.messages[event.message_id] = StreamingMessage(
                    id=event.message_id,
                    role=event.role,
                    content="",
                    is_complete=False
                )

            case "TEXT_MESSAGE_CONTENT":
                if event.message_id in self.messages:
                    msg = self.messages[event.message_id]
                    msg.content += event.delta

            case "TEXT_MESSAGE_END":
                if event.message_id in self.messages:
                    self.messages[event.message_id].is_complete = True

    def get_messages(self) -> List[StreamingMessage]:
        """Get all messages in order."""
        return list(self.messages.values())

    def get_message(self, message_id: str) -> Optional[StreamingMessage]:
        """Get specific message by ID."""
        return self.messages.get(message_id)
```

## Tool Handling

### Tool Definition

```python
from typing import TypedDict, List

class ToolParameter(TypedDict):
    type: str
    description: str
    enum: List[str] | None
    default: any

class ToolDefinition(TypedDict):
    name: str
    description: str
    parameters: dict

# Define tools
tools: List[ToolDefinition] = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or coordinates"
                },
                "units": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "default": "celsius"
                }
            },
            "required": ["location"]
        }
    },

    {
        "name": "search_database",
        "description": "Search internal knowledge database",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "number", "default": 10}
            },
            "required": ["query"]
        }
    }
]
```

### Tool Execution Pattern

```python
from typing import Callable, Dict, Any
import requests

class ToolExecutor:
    """Execute tools called by the agent."""

    def __init__(self):
        self.tool_registry: Dict[str, Callable] = {
            "get_weather": self.get_weather,
            "search_database": self.search_database,
        }

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool by name with arguments."""

        tool_fn = self.tool_registry.get(tool_name)
        if not tool_fn:
            raise ValueError(f"Unknown tool: {tool_name}")

        try:
            result = tool_fn(**arguments)
            return result
        except Exception as e:
            print(f"Tool execution failed: {tool_name}")
            raise

    def get_weather(self, location: str, units: str = "celsius") -> Dict[str, Any]:
        """Get weather data for a location."""
        response = requests.get(
            f"https://api.weather.com/v1/current",
            params={"location": location, "units": units}
        )
        response.raise_for_status()
        return response.json()

    def search_database(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search internal database."""
        # Implementation
        return {
            "results": [
                # Search results
            ],
            "count": 42
        }

# Usage
executor = ToolExecutor()

for event in event_stream:
    if event.type == "TOOL_CALL_START":
        tool_name = event.tool_name
        # Collect arguments from TOOL_CALL_ARGS events

    elif event.type == "TOOL_CALL_END":
        # Tool completed
        pass
```

### Async Tool Execution

```python
import asyncio
import aiohttp
from typing import Dict, Any

class AsyncToolExecutor:
    """Async tool executor for better performance."""

    async def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute tool asynchronously."""

        match tool_name:
            case "get_weather":
                return await self.get_weather(**arguments)

            case "search_database":
                return await self.search_database(**arguments)

            case _:
                raise ValueError(f"Unknown tool: {tool_name}")

    async def get_weather(self, location: str, units: str = "celsius") -> Dict[str, Any]:
        """Async weather fetch."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.weather.com/v1/current",
                params={"location": location, "units": units}
            ) as response:
                return await response.json()

    async def search_database(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Async database search."""
        # Async implementation
        await asyncio.sleep(0.1)  # Simulate async operation
        return {"results": [], "count": 0}
```

## State Management

### Handling State Snapshots

```python
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import copy

@dataclass
class AgentState:
    conversation: Dict[str, Any]
    user_preferences: Dict[str, Any]
    memory: Dict[str, Any]

class StateManager:
    """Manage agent state with snapshots and deltas."""

    def __init__(self):
        self.state: Optional[AgentState] = None
        self.subscribers = []

    def handle_event(self, event: BaseEvent) -> None:
        """Process state-related events."""

        match event.type:
            case "STATE_SNAPSHOT":
                self.state = self._parse_state(event.state)
                self._notify_subscribers()

            case "STATE_DELTA":
                self._apply_delta(event.delta)
                self._notify_subscribers()

    def _parse_state(self, state_dict: Dict[str, Any]) -> AgentState:
        """Parse state dictionary into AgentState."""
        return AgentState(
            conversation=state_dict.get("conversation", {}),
            user_preferences=state_dict.get("user_preferences", {}),
            memory=state_dict.get("memory", {})
        )

    def _apply_delta(self, delta: List[Dict[str, Any]]) -> None:
        """Apply JSON Patch operations to state."""
        if not self.state:
            return

        state_dict = asdict(self.state)

        for op in delta:
            operation = op["op"]
            path = op["path"]

            if operation == "replace":
                self._set_value_at_path(state_dict, path, op["value"])

            elif operation == "add":
                self._add_value_at_path(state_dict, path, op["value"])

            elif operation == "remove":
                self._remove_value_at_path(state_dict, path)

        self.state = self._parse_state(state_dict)

    def _set_value_at_path(self, obj: Dict, path: str, value: Any) -> None:
        """Set value at JSON Pointer path."""
        parts = [p for p in path.split('/') if p]
        target = obj

        for key in parts[:-1]:
            target = target[key]

        target[parts[-1]] = value

    def _add_value_at_path(self, obj: Dict, path: str, value: Any) -> None:
        """Add value at JSON Pointer path."""
        parts = [p for p in path.split('/') if p]
        target = obj

        for key in parts[:-1]:
            target = target[key]

        last_key = parts[-1]

        if isinstance(target, list) and last_key == "-":
            target.append(value)
        else:
            target[last_key] = value

    def _remove_value_at_path(self, obj: Dict, path: str) -> None:
        """Remove value at JSON Pointer path."""
        parts = [p for p in path.split('/') if p]
        target = obj

        for key in parts[:-1]:
            target = target[key]

        last_key = parts[-1]

        if isinstance(target, list):
            target.pop(int(last_key))
        else:
            del target[last_key]

    def get_state(self) -> Optional[AgentState]:
        """Get current state."""
        return copy.deepcopy(self.state)

    def subscribe(self, callback: Callable) -> None:
        """Subscribe to state changes."""
        self.subscribers.append(callback)

    def _notify_subscribers(self) -> None:
        """Notify all subscribers of state change."""
        for callback in self.subscribers:
            callback(self.state)
```

## Advanced Patterns

### Error Handling

```python
from ag_ui.core import HttpAgent, RunAgentInput
import logging

logger = logging.getLogger(__name__)

class AgentClient:
    """Robust agent client with error handling."""

    def __init__(self, base_url: str):
        self.agent = HttpAgent(base_url=base_url)

    def run_with_error_handling(self, input_data: RunAgentInput) -> None:
        """Execute agent with comprehensive error handling."""

        try:
            event_stream = self.agent.run(input_data)

            for event in event_stream:
                try:
                    if event.type == "RUN_ERROR":
                        self._handle_run_error(event)
                    else:
                        self._handle_event(event)

                except Exception as e:
                    logger.error(f"Event processing error: {e}")
                    # Continue processing other events

        except TimeoutError:
            logger.error("Request timeout")
            self._handle_timeout()

        except ConnectionError:
            logger.error("Network error")
            self._handle_network_error()

        except Exception as e:
            logger.error(f"Unknown error: {e}")
            self._handle_unknown_error(e)

    def _handle_run_error(self, event: RunErrorEvent) -> None:
        """Handle agent execution error."""
        logger.error(f"Agent error: {event.error}")

    def _handle_timeout(self) -> None:
        """Handle request timeout."""
        print("Request timed out. Please try again.")

    def _handle_network_error(self) -> None:
        """Handle network connection error."""
        print("Network error. Check your connection.")

    def _handle_unknown_error(self, error: Exception) -> None:
        """Handle unexpected errors."""
        print(f"An error occurred: {error}")
```

### Context Managers

```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def agent_session(base_url: str) -> Generator[HttpAgent, None, None]:
    """Context manager for agent sessions."""

    agent = HttpAgent(base_url=base_url)

    try:
        yield agent
    finally:
        # Cleanup if needed
        pass

# Usage
with agent_session("https://api.example.com") as agent:
    input_data = RunAgentInput(
        messages=[Message(role="user", content="Hello")]
    )

    for event in agent.run(input_data):
        handle_event(event)
```

### Multimodal Attachments

```python
import base64
from pathlib import Path
from typing import List, Dict, Any

@dataclass
class Attachment:
    type: str  # "image" | "file" | "audio"
    url: str | None = None
    data: str | None = None  # base64
    mime_type: str = ""
    filename: str | None = None

def create_message_with_image(text: str, image_path: Path) -> Message:
    """Create message with image attachment."""

    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    return Message(
        role="user",
        content=text,
        attachments=[
            {
                "type": "image",
                "data": image_data,
                "mime_type": "image/jpeg",
                "filename": image_path.name
            }
        ]
    )

def create_message_with_file(text: str, file_path: Path) -> Message:
    """Create message with file attachment."""

    with open(file_path, "rb") as f:
        file_data = base64.b64encode(f.read()).decode()

    return Message(
        role="user",
        content=text,
        attachments=[
            {
                "type": "file",
                "data": file_data,
                "mime_type": "application/pdf",
                "filename": file_path.name
            }
        ]
    )

# Usage
input_data = RunAgentInput(
    messages=[
        create_message_with_image(
            "What's in this image?",
            Path("photo.jpg")
        )
    ]
)
```

## Testing

### Unit Testing with pytest

```python
import pytest
from unittest.mock import Mock, patch
from ag_ui.core import HttpAgent, RunAgentInput, Message

@pytest.fixture
def mock_agent():
    """Create mock agent for testing."""
    return HttpAgent(base_url="https://test.example.com")

def test_message_handling(mock_agent):
    """Test message event handling."""

    # Mock event stream
    mock_events = [
        Mock(type="RUN_STARTED", run_id="test-run"),
        Mock(type="TEXT_MESSAGE_START", message_id="msg-1", role="assistant"),
        Mock(type="TEXT_MESSAGE_CONTENT", message_id="msg-1", delta="Hello"),
        Mock(type="TEXT_MESSAGE_CONTENT", message_id="msg-1", delta=" world"),
        Mock(type="TEXT_MESSAGE_END", message_id="msg-1"),
        Mock(type="RUN_FINISHED", run_id="test-run"),
    ]

    with patch.object(mock_agent, 'run', return_value=iter(mock_events)):
        messages = []

        for event in mock_agent.run(RunAgentInput(messages=[])):
            if event.type == "TEXT_MESSAGE_CONTENT":
                messages.append(event.delta)

        assert "".join(messages) == "Hello world"

def test_error_handling(mock_agent):
    """Test error event handling."""

    error_event = Mock(
        type="RUN_ERROR",
        error="Test error message"
    )

    with patch.object(mock_agent, 'run', return_value=iter([error_event])):
        for event in mock_agent.run(RunAgentInput(messages=[])):
            if event.type == "RUN_ERROR":
                assert event.error == "Test error message"
```

## Best Practices

### 1. Type Hints
```python
from typing import List, Dict, Any, Optional
from ag_ui.core import BaseEvent, Message

def handle_event(event: BaseEvent) -> None:
    """Always use type hints for clarity."""
    pass

def process_messages(messages: List[Message]) -> Dict[str, Any]:
    """Type hints improve code quality."""
    return {}
```

### 2. Error Handling
```python
# Always wrap agent calls in try-except
try:
    for event in agent.run(input_data):
        handle_event(event)
except Exception as e:
    logger.error(f"Agent error: {e}")
    # Handle gracefully
```

### 3. Resource Management
```python
# Use context managers for cleanup
with agent_session("https://api.example.com") as agent:
    # Agent automatically cleaned up
    pass
```

### 4. Async for Performance
```python
# Use async for concurrent operations
async def process_multiple_agents():
    tasks = [
        agent1.run(input1),
        agent2.run(input2),
        agent3.run(input3),
    ]

    results = await asyncio.gather(*tasks)
```

## Common Pitfalls

1. **Not handling exceptions** - Always wrap in try-except
2. **Blocking event loops** - Use async for long operations
3. **Ignoring event order** - Events are sequential
4. **Memory leaks** - Clean up large states
5. **Not validating tool args** - Validate before execution

## Next Steps

- See `protocol-fundamentals.md` for event system details
- See `architectural-decisions.md` for design patterns
- See `troubleshooting.md` for debugging help
- Check official docs: https://docs.ag-ui.com/sdk/python/core/overview
