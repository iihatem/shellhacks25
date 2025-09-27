# Services Directory

This directory contains all API services and backend interaction logic for the AI Agent Management Platform frontend.

## Architecture

The services are organized into separate modules for better maintainability:

### Core Files

- **`api.ts`** - Base API client with common HTTP methods and error handling
- **`types.ts`** - Shared TypeScript interfaces and types
- **`index.ts`** - Central export file for easy importing

### Service Modules

- **`agentsService.ts`** - All agent-related API calls
- **`tasksService.ts`** - All task-related API calls
- **`chatService.ts`** - All chat and messaging API calls

## Usage

### Basic Usage

```typescript
import { services } from "@/services";

// Get all agents
const response = await services.agents.getAgents();
if (response.data) {
  console.log("Agents:", response.data);
} else if (response.error) {
  console.error("Error:", response.error);
}
```

### Individual Service Import

```typescript
import { agentsService, tasksService, chatService } from "@/services";

// Use specific services
const agents = await agentsService.getAgents();
const tasks = await tasksService.getTasks();
const chatResponse = await chatService.sendMessage("Hello!");
```

### Type-Safe Responses

All services return a consistent `ApiResponse<T>` format:

```typescript
interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}
```

## Service Methods

### AgentsService

- `getAgents()` - Get all agents
- `getAgent(id)` - Get specific agent
- `createAgent(data)` - Create new agent
- `updateAgent(id, data)` - Update agent
- `deleteAgent(id)` - Delete agent
- `toggleAgentStatus(id, active)` - Toggle active status
- `getActiveAgents()` - Get only active agents
- `getAgentsByRole(role)` - Filter by role
- `findAgentByCapabilities(caps)` - Find by capabilities

### TasksService

- `getTasks()` - Get all tasks
- `getTask(id)` - Get specific task
- `createTask(data)` - Create new task
- `updateTask(id, data)` - Update task
- `deleteTask(id)` - Delete task
- `updateTaskStatus(id, status)` - Update status
- `assignTask(id, agentId)` - Assign to agent
- `getTasksByStatus(status)` - Filter by status
- `getPendingTasks()` - Get pending tasks
- `getCompletedTasks()` - Get completed tasks
- `getTasksByAgent(agentId)` - Get agent's tasks
- `getRecentTasks(limit)` - Get recent tasks
- `getTaskStats()` - Get statistics

### ChatService

- `sendMessage(message, userId)` - Send message to secretary
- `sendMessageWithContext(message, userId, context)` - Send with context
- `getChatHistory(userId, limit)` - Get chat history
- `clearChatHistory(userId)` - Clear history
- `getChatHelp()` - Get available commands
- `sendMessageToAgent(message, agentId, userId)` - Direct agent message
- `getAgentSuggestions(message)` - Get suggested agents
- `analyzeMessageIntent(message)` - Analyze message intent

## Configuration

The API base URL is configured via environment variables:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```

If not set, it defaults to `http://localhost:8001`.

## Error Handling

All services include comprehensive error handling:

```typescript
try {
  const response = await services.agents.getAgents();
  if (response.data) {
    // Success - use response.data
  } else if (response.error) {
    // Handle API error
    console.error("API Error:", response.error);
  }
} catch (error) {
  // Handle network or other errors
  console.error("Network Error:", error);
}
```

## Future Enhancements

- Authentication token management
- Request caching and optimization
- WebSocket integration for real-time updates
- Retry mechanisms for failed requests
- Request/response interceptors
- Background sync capabilities
