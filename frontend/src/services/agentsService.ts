import { apiClient, ApiResponse } from './api';
import { Agent, CreateAgentRequest } from './types';

export class AgentsService {
  /**
   * Get all agents in the workspace
   */
  async getAgents(): Promise<ApiResponse<Agent[]>> {
    return apiClient.get<Agent[]>('/agents');
  }

  /**
   * Get a specific agent by ID
   */
  async getAgent(agentId: string): Promise<ApiResponse<Agent>> {
    return apiClient.get<Agent>(`/agents/${agentId}`);
  }

  /**
   * Create a new agent
   */
  async createAgent(agentData: CreateAgentRequest): Promise<ApiResponse<Agent>> {
    return apiClient.post<Agent>('/agents', agentData);
  }

  /**
   * Update an existing agent
   */
  async updateAgent(agentId: string, agentData: Partial<Agent>): Promise<ApiResponse<Agent>> {
    return apiClient.put<Agent>(`/agents/${agentId}`, agentData);
  }

  /**
   * Delete an agent
   */
  async deleteAgent(agentId: string): Promise<ApiResponse<void>> {
    return apiClient.delete<void>(`/agents/${agentId}`);
  }

  /**
   * Toggle agent active status
   */
  async toggleAgentStatus(agentId: string, isActive: boolean): Promise<ApiResponse<Agent>> {
    return apiClient.patch<Agent>(`/agents/${agentId}`, { is_active: isActive });
  }

  /**
   * Get active agents only
   */
  async getActiveAgents(): Promise<ApiResponse<Agent[]>> {
    const response = await this.getAgents();
    if (response.data) {
      const activeAgents = response.data.filter(agent => agent.is_active);
      return { ...response, data: activeAgents };
    }
    return response;
  }

  /**
   * Get agents by role
   */
  async getAgentsByRole(role: string): Promise<ApiResponse<Agent[]>> {
    const response = await this.getAgents();
    if (response.data) {
      const roleAgents = response.data.filter(agent => agent.role === role);
      return { ...response, data: roleAgents };
    }
    return response;
  }

  /**
   * Check if an agent with specific capabilities exists
   */
  async findAgentByCapabilities(capabilities: string[]): Promise<ApiResponse<Agent | null>> {
    const response = await this.getAgents();
    if (response.data) {
      const matchingAgent = response.data.find(agent => 
        agent.is_active && capabilities.some(cap => agent.capabilities.includes(cap))
      );
      return { ...response, data: matchingAgent || null };
    }
    return response;
  }
}

// Create and export a default instance
export const agentsService = new AgentsService();
