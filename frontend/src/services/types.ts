// Shared types for API services

export interface Agent {
  id: string;
  name: string;
  role: string;
  capabilities: string[];
  is_active: boolean;
}

export interface Task {
  id: string;
  description: string;
  assigned_agent_id?: string;
  status: string;
  created_at: string;
}

export interface ChatMessage {
  message: string;
  user_id: string;
}

export interface ChatResponse {
  response: string;
  agent_name: string;
  action_taken?: string;
}

export interface CreateAgentRequest {
  id: string;
  name: string;
  role: string;
  capabilities: string[];
  is_active?: boolean;
}

export interface CreateTaskRequest {
  id: string;
  description: string;
  assigned_agent_id?: string;
  status?: string;
  created_at: string;
}

// Frontend-specific types
export interface Message {
  id: string;
  text: string;
  sender: "user" | "agent";
  agentName?: string;
  timestamp: Date;
  actionTaken?: string;
}
