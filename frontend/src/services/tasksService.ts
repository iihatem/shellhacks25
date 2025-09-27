import { apiClient, ApiResponse } from './api';
import { firestoreService } from './firestoreService';
import { Task, CreateTaskRequest } from './types';

export class TasksService {
  /**
   * Get all tasks
   */
  async getTasks(userId?: string): Promise<ApiResponse<Task[]>> {
    if (userId) {
      // Use Firestore for authenticated users
      try {
        const tasks = await firestoreService.getUserTasks(userId);
        return { data: tasks, status: 200 };
      } catch (error) {
        return { 
          error: error instanceof Error ? error.message : 'Failed to fetch tasks',
          status: 500 
        };
      }
    }
    // Fallback to API for unauthenticated users
    return apiClient.get<Task[]>('/tasks');
  }

  /**
   * Get a specific task by ID
   */
  async getTask(taskId: string): Promise<ApiResponse<Task>> {
    return apiClient.get<Task>(`/tasks/${taskId}`);
  }

  /**
   * Create a new task
   */
  async createTask(taskData: CreateTaskRequest): Promise<ApiResponse<Task>> {
    return apiClient.post<Task>('/tasks', taskData);
  }

  /**
   * Update an existing task
   */
  async updateTask(taskId: string, taskData: Partial<Task>): Promise<ApiResponse<Task>> {
    return apiClient.put<Task>(`/tasks/${taskId}`, taskData);
  }

  /**
   * Delete a task
   */
  async deleteTask(taskId: string): Promise<ApiResponse<void>> {
    return apiClient.delete<void>(`/tasks/${taskId}`);
  }

  /**
   * Update task status
   */
  async updateTaskStatus(taskId: string, status: string): Promise<ApiResponse<Task>> {
    return apiClient.patch<Task>(`/tasks/${taskId}`, { status });
  }

  /**
   * Assign task to an agent
   */
  async assignTask(taskId: string, agentId: string): Promise<ApiResponse<Task>> {
    return apiClient.patch<Task>(`/tasks/${taskId}`, { assigned_agent_id: agentId });
  }

  /**
   * Get tasks by status
   */
  async getTasksByStatus(status: string): Promise<ApiResponse<Task[]>> {
    const response = await this.getTasks();
    if (response.data) {
      const filteredTasks = response.data.filter(task => task.status === status);
      return { ...response, data: filteredTasks };
    }
    return response;
  }

  /**
   * Get pending tasks
   */
  async getPendingTasks(): Promise<ApiResponse<Task[]>> {
    return this.getTasksByStatus('pending');
  }

  /**
   * Get completed tasks
   */
  async getCompletedTasks(): Promise<ApiResponse<Task[]>> {
    return this.getTasksByStatus('completed');
  }

  /**
   * Get tasks assigned to a specific agent
   */
  async getTasksByAgent(agentId: string): Promise<ApiResponse<Task[]>> {
    const response = await this.getTasks();
    if (response.data) {
      const agentTasks = response.data.filter(task => task.assigned_agent_id === agentId);
      return { ...response, data: agentTasks };
    }
    return response;
  }

  /**
   * Get recent tasks (last N tasks)
   */
  async getRecentTasks(limit: number = 10): Promise<ApiResponse<Task[]>> {
    const response = await this.getTasks();
    if (response.data) {
      const sortedTasks = response.data
        .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        .slice(0, limit);
      return { ...response, data: sortedTasks };
    }
    return response;
  }

  /**
   * Get task statistics
   */
  async getTaskStats(): Promise<ApiResponse<{
    total: number;
    pending: number;
    in_progress: number;
    completed: number;
    failed: number;
  }>> {
    const response = await this.getTasks();
    if (response.data) {
      const tasks = response.data;
      const stats = {
        total: tasks.length,
        pending: tasks.filter(t => t.status === 'pending').length,
        in_progress: tasks.filter(t => t.status === 'in_progress').length,
        completed: tasks.filter(t => t.status === 'completed').length,
        failed: tasks.filter(t => t.status === 'failed').length,
      };
      return { ...response, data: stats };
    }
    return response;
  }
}

// Create and export a default instance
export const tasksService = new TasksService();
