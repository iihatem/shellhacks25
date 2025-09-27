"use client";

import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import ChatBot from "@/components/ChatBot";
import AgentsList from "@/components/AgentsList";
import TasksList from "@/components/TasksList";

interface Agent {
  id: string;
  name: string;
  role: string;
  capabilities: string[];
  is_active: boolean;
}

interface Task {
  id: string;
  description: string;
  assigned_agent_id?: string;
  status: string;
  created_at: string;
}

export default function Dashboard() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAgents();
    fetchTasks();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch("http://localhost:8001/agents");
      if (response.ok) {
        const data = await response.json();
        setAgents(data);
      }
    } catch (error) {
      console.error("Error fetching agents:", error);
    }
  };

  const fetchTasks = async () => {
    try {
      const response = await fetch("http://localhost:8001/tasks");
      if (response.ok) {
        const data = await response.json();
        setTasks(data);
      }
    } catch (error) {
      console.error("Error fetching tasks:", error);
    } finally {
      setLoading(false);
    }
  };

  const activeAgents = agents.filter((agent) => agent.is_active);
  const pendingTasks = tasks.filter((task) => task.status === "pending");

  return (
    <div className="container mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          AI Agent Management Platform
        </h1>
        <p className="text-lg text-gray-600">
          Delegate tasks to your AI workforce and watch them collaborate
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
            <Badge variant="secondary">{activeAgents.length}</Badge>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeAgents.length}</div>
            <p className="text-xs text-muted-foreground">
              Ready to handle your tasks
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Tasks</CardTitle>
            <Badge variant="outline">{pendingTasks.length}</Badge>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{pendingTasks.length}</div>
            <p className="text-xs text-muted-foreground">Awaiting assignment</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tasks</CardTitle>
            <Badge>{tasks.length}</Badge>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{tasks.length}</div>
            <p className="text-xs text-muted-foreground">All time</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chat Section - Takes up 2 columns on large screens */}
        <div className="lg:col-span-2">
          <Card className="h-[600px]">
            <CardHeader>
              <CardTitle>Chat with Your Secretary</CardTitle>
              <CardDescription>
                Describe what you need done, and your AI secretary will delegate
                tasks to the right agents
              </CardDescription>
            </CardHeader>
            <CardContent className="h-[500px]">
              <ChatBot onTaskCreated={fetchTasks} />
            </CardContent>
          </Card>
        </div>

        {/* Side Panel */}
        <div className="space-y-6">
          {/* Agents List */}
          <Card>
            <CardHeader>
              <CardTitle>Your Agents</CardTitle>
              <CardDescription>AI agents in your workspace</CardDescription>
            </CardHeader>
            <CardContent>
              <AgentsList agents={agents} loading={loading} />
            </CardContent>
          </Card>

          <Separator />

          {/* Recent Tasks */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Tasks</CardTitle>
              <CardDescription>Latest task assignments</CardDescription>
            </CardHeader>
            <CardContent>
              <TasksList tasks={tasks.slice(0, 5)} loading={loading} />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
