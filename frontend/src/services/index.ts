// Central export file for all services

import { agentsService } from './agentsService';
import { tasksService } from './tasksService';
import { chatService } from './chatService';

export { ApiClient, apiClient } from './api';
export { agentsService, AgentsService } from './agentsService';
export { tasksService, TasksService } from './tasksService';
export { chatService, ChatService } from './chatService';

// Re-export types for convenience
export type {
  Agent,
  Task,
  ChatMessage,
  ChatResponse,
  CreateAgentRequest,
  CreateTaskRequest,
  Message,
} from './types';

export type { ApiResponse } from './api';

// Service instances for easy importing
export const services = {
  agents: agentsService,
  tasks: tasksService,
  chat: chatService,
} as const;
