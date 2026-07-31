# AG-UI TypeScript/JavaScript Implementation Guide

Complete guide to implementing AG-UI in TypeScript and JavaScript applications.

## Installation

Install the AG-UI core package:

```bash
npm install @ag-ui/core
```

**TypeScript Support:**
The SDK is written in TypeScript with full type definitions included.

**Requirements:**
- Node.js 16+ or modern browser environment
- TypeScript 4.5+ (for TypeScript projects)

## Core Architecture

The TypeScript SDK provides a **streaming event-based architecture with strongly typed data structures**. All events and data types are fully typed for IDE autocomplete and type safety.

### Package Structure

```typescript
import {
  // Client
  HttpAgent,

  // Types
  RunAgentInput,
  BaseEvent,
  Message,
  Tool,
  Context,
  State,

  // Event Types
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
} from '@ag-ui/core';
```

## HttpAgent - Standard Client

The primary way to connect to AG-UI agents.

### Basic Setup

```typescript
import { HttpAgent } from '@ag-ui/core';

// Create client
const agent = new HttpAgent({
  baseUrl: 'https://your-agent-api.com',
  // Optional configuration
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Custom-Header': 'value'
  },
  timeout: 30000, // 30 seconds
});
```

### Running an Agent

```typescript
import type { RunAgentInput } from '@ag-ui/core';

const input: RunAgentInput = {
  // User message
  messages: [
    {
      role: 'user',
      content: 'Help me plan a trip to Tokyo'
    }
  ],

  // Agent configuration
  config: {
    model: 'gpt-4',
    temperature: 0.7,
    maxTokens: 2000
  },

  // Available tools (optional)
  tools: [
    {
      name: 'search_flights',
      description: 'Search for available flights',
      parameters: {
        type: 'object',
        properties: {
          origin: { type: 'string' },
          destination: { type: 'string' },
          date: { type: 'string' }
        },
        required: ['origin', 'destination', 'date']
      }
    }
  ],

  // Additional context (optional)
  context: {
    userId: 'user-123',
    sessionId: 'session-456',
    preferences: {
      language: 'en',
      timezone: 'America/New_York'
    }
  }
};

// Execute agent - returns Observable<BaseEvent>
const eventStream = agent.run(input);
```

## Event Stream Handling

AG-UI uses observables for event streams. The SDK is framework-agnostic but works well with RxJS.

### Basic Event Subscription

```typescript
// Subscribe to event stream
eventStream.subscribe({
  next: (event) => {
    console.log('Event received:', event.type);
    handleEvent(event);
  },
  error: (error) => {
    console.error('Stream error:', error);
  },
  complete: () => {
    console.log('Stream completed');
  }
});
```

### Type-Safe Event Handling

```typescript
import type { BaseEvent } from '@ag-ui/core';

function handleEvent(event: BaseEvent) {
  switch (event.type) {
    case 'RUN_STARTED':
      handleRunStarted(event);
      break;

    case 'TEXT_MESSAGE_START':
      handleMessageStart(event);
      break;

    case 'TEXT_MESSAGE_CONTENT':
      handleMessageContent(event);
      break;

    case 'TEXT_MESSAGE_END':
      handleMessageEnd(event);
      break;

    case 'TOOL_CALL_START':
      handleToolCallStart(event);
      break;

    case 'TOOL_CALL_END':
      handleToolCallEnd(event);
      break;

    case 'STATE_SNAPSHOT':
      handleStateSnapshot(event);
      break;

    case 'STATE_DELTA':
      handleStateDelta(event);
      break;

    case 'RUN_FINISHED':
      handleRunFinished(event);
      break;

    case 'RUN_ERROR':
      handleRunError(event);
      break;

    default:
      console.warn('Unknown event type:', event.type);
  }
}
```

### React Integration Example

```typescript
import { useState, useEffect } from 'react';
import { HttpAgent, type BaseEvent } from '@ag-ui/core';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

function ChatComponent() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentMessage, setCurrentMessage] = useState<string>('');
  const [isRunning, setIsRunning] = useState(false);

  const agent = new HttpAgent({
    baseUrl: 'https://api.example.com/agent'
  });

  const runAgent = async (userMessage: string) => {
    setIsRunning(true);

    // Add user message to UI
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: userMessage
    };
    setMessages(prev => [...prev, userMsg]);

    // Run agent
    const eventStream = agent.run({
      messages: [
        ...messages.map(m => ({ role: m.role, content: m.content })),
        { role: 'user', content: userMessage }
      ]
    });

    let assistantMessageId: string | null = null;

    eventStream.subscribe({
      next: (event: BaseEvent) => {
        switch (event.type) {
          case 'TEXT_MESSAGE_START':
            assistantMessageId = event.messageId;
            setMessages(prev => [...prev, {
              id: event.messageId,
              role: 'assistant',
              content: ''
            }]);
            break;

          case 'TEXT_MESSAGE_CONTENT':
            if (assistantMessageId) {
              setMessages(prev => prev.map(msg =>
                msg.id === assistantMessageId
                  ? { ...msg, content: msg.content + event.delta }
                  : msg
              ));
            }
            break;

          case 'TEXT_MESSAGE_END':
            assistantMessageId = null;
            break;
        }
      },
      error: (error) => {
        console.error('Agent error:', error);
        setIsRunning(false);
      },
      complete: () => {
        setIsRunning(false);
      }
    });
  };

  return (
    <div>
      <div className="messages">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>

      <input
        type="text"
        value={currentMessage}
        onChange={(e) => setCurrentMessage(e.target.value)}
        onKeyPress={(e) => {
          if (e.key === 'Enter' && !isRunning) {
            runAgent(currentMessage);
            setCurrentMessage('');
          }
        }}
        disabled={isRunning}
      />
    </div>
  );
}
```

## Working with Messages

### Message Structure

```typescript
interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;

  // Optional fields
  name?: string;
  toolCallId?: string;
  toolCalls?: ToolCall[];
}
```

### Streaming Message Pattern

```typescript
interface StreamingMessage {
  id: string;
  role: string;
  content: string;
  isComplete: boolean;
}

class MessageManager {
  private messages: Map<string, StreamingMessage> = new Map();

  handleEvent(event: BaseEvent) {
    switch (event.type) {
      case 'TEXT_MESSAGE_START':
        this.messages.set(event.messageId, {
          id: event.messageId,
          role: event.role,
          content: '',
          isComplete: false
        });
        break;

      case 'TEXT_MESSAGE_CONTENT':
        const msg = this.messages.get(event.messageId);
        if (msg) {
          msg.content += event.delta;
        }
        break;

      case 'TEXT_MESSAGE_END':
        const finalMsg = this.messages.get(event.messageId);
        if (finalMsg) {
          finalMsg.isComplete = true;
        }
        break;
    }
  }

  getMessages(): StreamingMessage[] {
    return Array.from(this.messages.values());
  }
}
```

## Tool Handling

### Tool Definition

```typescript
interface Tool {
  name: string;
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, any>;
    required?: string[];
  };
}

const tools: Tool[] = [
  {
    name: 'get_weather',
    description: 'Get current weather for a location',
    parameters: {
      type: 'object',
      properties: {
        location: {
          type: 'string',
          description: 'City name or coordinates'
        },
        units: {
          type: 'string',
          enum: ['celsius', 'fahrenheit'],
          default: 'celsius'
        }
      },
      required: ['location']
    }
  },

  {
    name: 'search_database',
    description: 'Search internal knowledge database',
    parameters: {
      type: 'object',
      properties: {
        query: { type: 'string' },
        limit: { type: 'number', default: 10 }
      },
      required: ['query']
    }
  }
];
```

### Tool Execution Pattern

```typescript
interface ToolCall {
  id: string;
  name: string;
  arguments: Record<string, any>;
}

class ToolExecutor {
  private toolRegistry: Map<string, Function> = new Map();

  constructor() {
    // Register tool implementations
    this.toolRegistry.set('get_weather', this.getWeather);
    this.toolRegistry.set('search_database', this.searchDatabase);
  }

  async handleToolCall(event: ToolCallStartEvent, argsEvent: ToolCallArgsEvent) {
    const toolName = event.toolName;
    const toolArgs = argsEvent.arguments;

    const toolFn = this.toolRegistry.get(toolName);
    if (!toolFn) {
      throw new Error(`Unknown tool: ${toolName}`);
    }

    try {
      const result = await toolFn(toolArgs);
      return result;
    } catch (error) {
      console.error(`Tool execution failed: ${toolName}`, error);
      throw error;
    }
  }

  private async getWeather(args: { location: string; units?: string }) {
    // Implementation
    const response = await fetch(
      `https://api.weather.com/v1/current?location=${args.location}&units=${args.units || 'celsius'}`
    );
    return await response.json();
  }

  private async searchDatabase(args: { query: string; limit?: number }) {
    // Implementation
    return {
      results: [/* search results */],
      count: 42
    };
  }
}
```

## State Management

### Handling State Snapshots

```typescript
interface AgentState {
  conversation: {
    messageCount: number;
    topics: string[];
  };
  userPreferences: {
    theme: string;
    language: string;
  };
  memory: Record<string, any>;
}

class StateManager {
  private state: AgentState | null = null;

  handleEvent(event: BaseEvent) {
    if (event.type === 'STATE_SNAPSHOT') {
      this.state = event.state as AgentState;
      this.notifySubscribers();
    } else if (event.type === 'STATE_DELTA') {
      this.applyDelta(event.delta);
    }
  }

  private applyDelta(delta: any[]) {
    if (!this.state) return;

    // Apply JSON Patch operations
    for (const op of delta) {
      switch (op.op) {
        case 'replace':
          this.setValueAtPath(this.state, op.path, op.value);
          break;
        case 'add':
          this.addValueAtPath(this.state, op.path, op.value);
          break;
        case 'remove':
          this.removeValueAtPath(this.state, op.path);
          break;
      }
    }

    this.notifySubscribers();
  }

  private setValueAtPath(obj: any, path: string, value: any) {
    const parts = path.split('/').filter(p => p);
    const last = parts.pop()!;
    const target = parts.reduce((o, key) => o[key], obj);
    target[last] = value;
  }

  private addValueAtPath(obj: any, path: string, value: any) {
    const parts = path.split('/').filter(p => p);
    const last = parts.pop()!;
    const target = parts.reduce((o, key) => o[key], obj);

    if (Array.isArray(target) && last === '-') {
      target.push(value);
    } else {
      target[last] = value;
    }
  }

  private removeValueAtPath(obj: any, path: string) {
    const parts = path.split('/').filter(p => p);
    const last = parts.pop()!;
    const target = parts.reduce((o, key) => o[key], obj);

    if (Array.isArray(target)) {
      target.splice(Number(last), 1);
    } else {
      delete target[last];
    }
  }

  getState(): AgentState | null {
    return this.state;
  }

  private notifySubscribers() {
    // Notify UI components of state changes
  }
}
```

### React State Integration

```typescript
import { useState, useEffect } from 'react';

function useAgentState(eventStream: Observable<BaseEvent>) {
  const [state, setState] = useState<AgentState | null>(null);

  useEffect(() => {
    const subscription = eventStream.subscribe({
      next: (event) => {
        if (event.type === 'STATE_SNAPSHOT') {
          setState(event.state as AgentState);
        } else if (event.type === 'STATE_DELTA') {
          setState(prevState => {
            if (!prevState) return null;
            return applyJsonPatch(prevState, event.delta);
          });
        }
      }
    });

    return () => subscription.unsubscribe();
  }, [eventStream]);

  return state;
}
```

## Advanced Patterns

### Error Handling

```typescript
class AgentClient {
  private agent: HttpAgent;

  constructor(baseUrl: string) {
    this.agent = new HttpAgent({ baseUrl });
  }

  async runWithErrorHandling(input: RunAgentInput): Promise<void> {
    const eventStream = this.agent.run(input);

    eventStream.subscribe({
      next: (event) => {
        if (event.type === 'RUN_ERROR') {
          this.handleRunError(event);
        } else {
          this.handleEvent(event);
        }
      },
      error: (error) => {
        // Network or connection error
        if (error.code === 'NETWORK_ERROR') {
          this.handleNetworkError(error);
        } else if (error.code === 'TIMEOUT') {
          this.handleTimeout(error);
        } else {
          this.handleUnknownError(error);
        }
      },
      complete: () => {
        console.log('Stream completed successfully');
      }
    });
  }

  private handleRunError(event: RunErrorEvent) {
    console.error('Agent execution error:', event.error);
    // Show user-friendly error message
  }

  private handleNetworkError(error: any) {
    console.error('Network error:', error);
    // Offer retry option
  }

  private handleTimeout(error: any) {
    console.error('Request timeout:', error);
    // Show timeout message
  }

  private handleUnknownError(error: any) {
    console.error('Unknown error:', error);
    // Generic error handling
  }
}
```

### Cancellation

```typescript
import { Subscription } from 'rxjs';

class CancellableAgent {
  private currentSubscription: Subscription | null = null;

  run(input: RunAgentInput) {
    // Cancel previous run if exists
    this.cancel();

    const agent = new HttpAgent({ baseUrl: 'https://api.example.com' });
    const eventStream = agent.run(input);

    this.currentSubscription = eventStream.subscribe({
      next: (event) => this.handleEvent(event),
      error: (error) => this.handleError(error),
      complete: () => {
        this.currentSubscription = null;
      }
    });
  }

  cancel() {
    if (this.currentSubscription) {
      this.currentSubscription.unsubscribe();
      this.currentSubscription = null;
      console.log('Agent run cancelled');
    }
  }
}
```

### Multimodal Attachments

```typescript
interface MessageWithAttachments {
  role: 'user';
  content: string;
  attachments?: Array<{
    type: 'image' | 'file' | 'audio';
    url?: string;
    data?: string; // base64
    mimeType: string;
    filename?: string;
  }>;
}

// Send message with image
const input: RunAgentInput = {
  messages: [
    {
      role: 'user',
      content: 'What is in this image?',
      attachments: [
        {
          type: 'image',
          url: 'https://example.com/image.jpg',
          mimeType: 'image/jpeg'
        }
      ]
    }
  ]
};

// Send message with file upload
const fileInput = document.querySelector<HTMLInputElement>('#file-input');
const file = fileInput?.files?.[0];

if (file) {
  const reader = new FileReader();
  reader.onload = () => {
    const base64Data = reader.result as string;

    const input: RunAgentInput = {
      messages: [
        {
          role: 'user',
          content: 'Analyze this document',
          attachments: [
            {
              type: 'file',
              data: base64Data.split(',')[1], // Remove data:... prefix
              mimeType: file.type,
              filename: file.name
            }
          ]
        }
      ]
    };

    agent.run(input);
  };

  reader.readAsDataURL(file);
}
```

## Testing

### Unit Testing with Jest

```typescript
import { HttpAgent } from '@ag-ui/core';
import { of } from 'rxjs';

describe('AgentClient', () => {
  let agent: HttpAgent;

  beforeEach(() => {
    agent = new HttpAgent({
      baseUrl: 'https://test-api.example.com'
    });
  });

  it('should handle text message events', (done) => {
    const mockEventStream = of(
      { type: 'RUN_STARTED', runId: 'test-run' },
      { type: 'TEXT_MESSAGE_START', messageId: 'msg-1', role: 'assistant' },
      { type: 'TEXT_MESSAGE_CONTENT', messageId: 'msg-1', delta: 'Hello' },
      { type: 'TEXT_MESSAGE_CONTENT', messageId: 'msg-1', delta: ' world' },
      { type: 'TEXT_MESSAGE_END', messageId: 'msg-1' },
      { type: 'RUN_FINISHED', runId: 'test-run' }
    );

    jest.spyOn(agent, 'run').mockReturnValue(mockEventStream);

    const messages: string[] = [];

    agent.run({ messages: [] }).subscribe({
      next: (event) => {
        if (event.type === 'TEXT_MESSAGE_CONTENT') {
          messages.push(event.delta);
        }
      },
      complete: () => {
        expect(messages.join('')).toBe('Hello world');
        done();
      }
    });
  });
});
```

## Best Practices

### 1. Type Safety
```typescript
// Always use types from SDK
import type { RunAgentInput, BaseEvent, Message } from '@ag-ui/core';

// Enable strict TypeScript
// tsconfig.json: "strict": true
```

### 2. Event Stream Management
```typescript
// Always unsubscribe to prevent memory leaks
const subscription = eventStream.subscribe(/*...*/);

// In React useEffect
return () => subscription.unsubscribe();

// In class component
componentWillUnmount() {
  this.subscription?.unsubscribe();
}
```

### 3. Error Boundaries
```typescript
// Wrap agent interactions in try-catch
try {
  const eventStream = agent.run(input);
  // Handle events
} catch (error) {
  console.error('Failed to start agent:', error);
  // Show user error
}
```

### 4. Performance
```typescript
// Use memo for expensive state computations
const processedState = useMemo(() => {
  return expensiveStateTransform(agentState);
}, [agentState]);

// Debounce rapid state updates
import { debounceTime } from 'rxjs/operators';

eventStream.pipe(
  debounceTime(100)
).subscribe(/*...*/);
```

## Common Pitfalls

1. **Forgetting to unsubscribe** - Leads to memory leaks
2. **Not handling errors** - Crashes user experience
3. **Blocking UI on events** - Use async handlers
4. **Ignoring event order** - Events arrive sequentially, process accordingly
5. **Not validating tool arguments** - Can cause runtime errors

## Next Steps

- See `protocol-fundamentals.md` for event system details
- See `architectural-decisions.md` for design patterns
- See `troubleshooting.md` for debugging help
- Check official docs: https://docs.ag-ui.com/sdk/js/core/overview
