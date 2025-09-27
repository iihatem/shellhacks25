import { apiClient, ApiResponse } from './api';
import { ChatMessage, ChatResponse } from './types';

export class ChatService {
  /**
   * Send a message to the secretary agent
   */
  async sendMessage(message: string, userId: string = 'user-123'): Promise<ApiResponse<ChatResponse>> {
    const chatMessage: ChatMessage = {
      message,
      user_id: userId,
    };

    return apiClient.post<ChatResponse>('/chat', chatMessage);
  }

  /**
   * Send a message with additional context
   */
  async sendMessageWithContext(
    message: string, 
    userId: string = 'user-123',
    context?: {
      previousMessages?: number;
      taskContext?: string;
      agentPreference?: string;
    }
  ): Promise<ApiResponse<ChatResponse>> {
    const chatMessage = {
      message,
      user_id: userId,
      context,
    };

    return apiClient.post<ChatResponse>('/chat', chatMessage);
  }

  /**
   * Get chat history (if implemented in backend)
   */
  async getChatHistory(userId: string, limit?: number): Promise<ApiResponse<ChatMessage[]>> {
    const params = new URLSearchParams();
    if (limit) params.append('limit', limit.toString());
    
    const endpoint = `/chat/history/${userId}${params.toString() ? `?${params.toString()}` : ''}`;
    return apiClient.get<ChatMessage[]>(endpoint);
  }

  /**
   * Clear chat history (if implemented in backend)
   */
  async clearChatHistory(userId: string): Promise<ApiResponse<void>> {
    return apiClient.delete<void>(`/chat/history/${userId}`);
  }

  /**
   * Get available chat commands or help
   */
  async getChatHelp(): Promise<ApiResponse<{ commands: string[]; examples: string[] }>> {
    return apiClient.get<{ commands: string[]; examples: string[] }>('/chat/help');
  }

  /**
   * Send a message to a specific agent (if implemented)
   */
  async sendMessageToAgent(
    message: string, 
    agentId: string, 
    userId: string = 'user-123'
  ): Promise<ApiResponse<ChatResponse>> {
    const chatMessage = {
      message,
      user_id: userId,
      target_agent_id: agentId,
    };

    return apiClient.post<ChatResponse>('/chat/direct', chatMessage);
  }

  /**
   * Get agent suggestions based on message content
   */
  async getAgentSuggestions(message: string): Promise<ApiResponse<{
    suggested_agents: string[];
    reasoning: string;
  }>> {
    return apiClient.post<{
      suggested_agents: string[];
      reasoning: string;
    }>('/chat/suggest-agents', { message });
  }

  /**
   * Analyze message intent (if implemented)
   */
  async analyzeMessageIntent(message: string): Promise<ApiResponse<{
    intent: string;
    confidence: number;
    required_capabilities: string[];
    urgency: 'low' | 'medium' | 'high';
  }>> {
    return apiClient.post<{
      intent: string;
      confidence: number;
      required_capabilities: string[];
      urgency: 'low' | 'medium' | 'high';
    }>('/chat/analyze', { message });
  }
}

// Create and export a default instance
export const chatService = new ChatService();
