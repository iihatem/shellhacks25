import {
  collection,
  doc,
  getDocs,
  getDoc,
  addDoc,
  updateDoc,
  deleteDoc,
  query,
  where,
  orderBy,
  limit,
  serverTimestamp,
  Timestamp,
} from 'firebase/firestore';
import { db } from '@/lib/firebase';
import { Agent, Task } from './types';

export class FirestoreService {
  // Helper to get user-specific collection reference
  private getUserCollection(userId: string, collectionName: string) {
    return collection(db, 'users', userId, collectionName);
  }

  // AGENTS
  async getUserAgents(userId: string): Promise<Agent[]> {
    try {
      const agentsRef = this.getUserCollection(userId, 'agents');
      const snapshot = await getDocs(agentsRef);
      return snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data(),
      })) as Agent[];
    } catch (error) {
      console.error('Error fetching user agents:', error);
      throw error;
    }
  }

  async getUserAgent(userId: string, agentId: string): Promise<Agent | null> {
    try {
      const agentRef = doc(db, 'users', userId, 'agents', agentId);
      const snapshot = await getDoc(agentRef);
      
      if (snapshot.exists()) {
        return {
          id: snapshot.id,
          ...snapshot.data(),
        } as Agent;
      }
      return null;
    } catch (error) {
      console.error('Error fetching user agent:', error);
      throw error;
    }
  }

  async createUserAgent(userId: string, agentData: Omit<Agent, 'id'>): Promise<Agent> {
    try {
      const agentsRef = this.getUserCollection(userId, 'agents');
      const docRef = await addDoc(agentsRef, {
        ...agentData,
        created_at: serverTimestamp(),
        updated_at: serverTimestamp(),
      });
      
      const newAgent = {
        id: docRef.id,
        ...agentData,
      };
      
      return newAgent;
    } catch (error) {
      console.error('Error creating user agent:', error);
      throw error;
    }
  }

  async updateUserAgent(userId: string, agentId: string, updates: Partial<Agent>): Promise<void> {
    try {
      const agentRef = doc(db, 'users', userId, 'agents', agentId);
      await updateDoc(agentRef, {
        ...updates,
        updated_at: serverTimestamp(),
      });
    } catch (error) {
      console.error('Error updating user agent:', error);
      throw error;
    }
  }

  async deleteUserAgent(userId: string, agentId: string): Promise<void> {
    try {
      const agentRef = doc(db, 'users', userId, 'agents', agentId);
      await deleteDoc(agentRef);
    } catch (error) {
      console.error('Error deleting user agent:', error);
      throw error;
    }
  }

  // TASKS
  async getUserTasks(userId: string): Promise<Task[]> {
    try {
      const tasksRef = this.getUserCollection(userId, 'tasks');
      const q = query(tasksRef, orderBy('created_at', 'desc'));
      const snapshot = await getDocs(q);
      
      return snapshot.docs.map(doc => {
        const data = doc.data();
        return {
          id: doc.id,
          ...data,
          created_at: data.created_at instanceof Timestamp 
            ? data.created_at.toDate().toISOString()
            : data.created_at,
        };
      }) as Task[];
    } catch (error) {
      console.error('Error fetching user tasks:', error);
      throw error;
    }
  }

  async getUserTask(userId: string, taskId: string): Promise<Task | null> {
    try {
      const taskRef = doc(db, 'users', userId, 'tasks', taskId);
      const snapshot = await getDoc(taskRef);
      
      if (snapshot.exists()) {
        const data = snapshot.data();
        return {
          id: snapshot.id,
          ...data,
          created_at: data.created_at instanceof Timestamp 
            ? data.created_at.toDate().toISOString()
            : data.created_at,
        } as Task;
      }
      return null;
    } catch (error) {
      console.error('Error fetching user task:', error);
      throw error;
    }
  }

  async createUserTask(userId: string, taskData: Omit<Task, 'id' | 'created_at'>): Promise<Task> {
    try {
      const tasksRef = this.getUserCollection(userId, 'tasks');
      const docRef = await addDoc(tasksRef, {
        ...taskData,
        created_at: serverTimestamp(),
        updated_at: serverTimestamp(),
      });
      
      const newTask = {
        id: docRef.id,
        ...taskData,
        created_at: new Date().toISOString(),
      };
      
      return newTask;
    } catch (error) {
      console.error('Error creating user task:', error);
      throw error;
    }
  }

  async updateUserTask(userId: string, taskId: string, updates: Partial<Task>): Promise<void> {
    try {
      const taskRef = doc(db, 'users', userId, 'tasks', taskId);
      await updateDoc(taskRef, {
        ...updates,
        updated_at: serverTimestamp(),
      });
    } catch (error) {
      console.error('Error updating user task:', error);
      throw error;
    }
  }

  async deleteUserTask(userId: string, taskId: string): Promise<void> {
    try {
      const taskRef = doc(db, 'users', userId, 'tasks', taskId);
      await deleteDoc(taskRef);
    } catch (error) {
      console.error('Error deleting user task:', error);
      throw error;
    }
  }

  // Get tasks by status
  async getUserTasksByStatus(userId: string, status: string): Promise<Task[]> {
    try {
      const tasksRef = this.getUserCollection(userId, 'tasks');
      const q = query(
        tasksRef, 
        where('status', '==', status),
        orderBy('created_at', 'desc')
      );
      const snapshot = await getDocs(q);
      
      return snapshot.docs.map(doc => {
        const data = doc.data();
        return {
          id: doc.id,
          ...data,
          created_at: data.created_at instanceof Timestamp 
            ? data.created_at.toDate().toISOString()
            : data.created_at,
        };
      }) as Task[];
    } catch (error) {
      console.error('Error fetching user tasks by status:', error);
      throw error;
    }
  }

  // Get recent tasks
  async getRecentUserTasks(userId: string, limitCount: number = 10): Promise<Task[]> {
    try {
      const tasksRef = this.getUserCollection(userId, 'tasks');
      const q = query(
        tasksRef,
        orderBy('created_at', 'desc'),
        limit(limitCount)
      );
      const snapshot = await getDocs(q);
      
      return snapshot.docs.map(doc => {
        const data = doc.data();
        return {
          id: doc.id,
          ...data,
          created_at: data.created_at instanceof Timestamp 
            ? data.created_at.toDate().toISOString()
            : data.created_at,
        };
      }) as Task[];
    } catch (error) {
      console.error('Error fetching recent user tasks:', error);
      throw error;
    }
  }

  // Initialize default agents for a new user based on their type
  async initializeDefaultAgents(userId: string, userType: string): Promise<void> {
    const defaultAgents: Record<string, Agent[]> = {
      ceo: [
        {
          id: 'executive-secretary',
          name: 'Executive Secretary',
          role: 'secretary',
          capabilities: ['task_delegation', 'communication', 'scheduling', 'meeting_management'],
          is_active: true,
        },
        {
          id: 'hiring-manager',
          name: 'Hiring Manager',
          role: 'hiring_manager',
          capabilities: ['agent_creation', 'skill_assessment', 'recruitment', 'team_building'],
          is_active: true,
        },
        {
          id: 'strategy-consultant',
          name: 'Strategy Consultant',
          role: 'consultant',
          capabilities: ['strategic_planning', 'analysis', 'reporting', 'decision_support'],
          is_active: true,
        },
      ],
      student: [
        {
          id: 'study-secretary',
          name: 'Study Secretary',
          role: 'secretary',
          capabilities: ['task_delegation', 'study_planning', 'deadline_management'],
          is_active: true,
        },
        {
          id: 'tutor-manager',
          name: 'Tutor Manager',
          role: 'hiring_manager',
          capabilities: ['agent_creation', 'subject_assessment', 'learning_support'],
          is_active: true,
        },
        {
          id: 'research-assistant',
          name: 'Research Assistant',
          role: 'assistant',
          capabilities: ['research', 'information_gathering', 'citation_help', 'fact_checking'],
          is_active: true,
        },
      ],
      tutor: [
        {
          id: 'teaching-secretary',
          name: 'Teaching Secretary',
          role: 'secretary',
          capabilities: ['task_delegation', 'lesson_planning', 'student_management'],
          is_active: true,
        },
        {
          id: 'curriculum-manager',
          name: 'Curriculum Manager',
          role: 'hiring_manager',
          capabilities: ['agent_creation', 'content_development', 'assessment_creation'],
          is_active: true,
        },
        {
          id: 'content-creator',
          name: 'Educational Content Creator',
          role: 'creator',
          capabilities: ['content_creation', 'material_development', 'quiz_generation'],
          is_active: true,
        },
      ],
      designer: [
        {
          id: 'creative-secretary',
          name: 'Creative Secretary',
          role: 'secretary',
          capabilities: ['task_delegation', 'project_management', 'client_communication'],
          is_active: true,
        },
        {
          id: 'creative-director',
          name: 'Creative Director',
          role: 'hiring_manager',
          capabilities: ['agent_creation', 'design_review', 'creative_strategy'],
          is_active: true,
        },
        {
          id: 'asset-manager',
          name: 'Asset Manager',
          role: 'manager',
          capabilities: ['asset_organization', 'version_control', 'file_management'],
          is_active: true,
        },
      ],
      content_creator: [
        {
          id: 'content-secretary',
          name: 'Content Secretary',
          role: 'secretary',
          capabilities: ['task_delegation', 'content_planning', 'publishing_schedule'],
          is_active: true,
        },
        {
          id: 'brand-manager',
          name: 'Brand Manager',
          role: 'hiring_manager',
          capabilities: ['agent_creation', 'brand_consistency', 'audience_analysis'],
          is_active: true,
        },
        {
          id: 'social-media-manager',
          name: 'Social Media Manager',
          role: 'manager',
          capabilities: ['social_media_posting', 'engagement_tracking', 'hashtag_research'],
          is_active: true,
        },
      ],
    };

    const agents = defaultAgents[userType] || defaultAgents.ceo;
    
    try {
      for (const agent of agents) {
        await this.createUserAgent(userId, agent);
      }
    } catch (error) {
      console.error('Error initializing default agents:', error);
      throw error;
    }
  }
}

// Create and export a default instance
export const firestoreService = new FirestoreService();
