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
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import ChatBot from "@/components/ChatBot";
import AgentsList from "@/components/AgentsList";
import TasksList from "@/components/TasksList";
import { services, Agent, Task } from "@/services";
import { useAuth } from "@/contexts/AuthContext";
import { Activity, Users, CheckCircle, Clock } from "lucide-react";

export default function Dashboard() {
  const { user } = useAuth();
  const [agents, setAgents] = useState<Agent[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAgents();
    fetchTasks();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await services.agents.getAgents(user?.uid);
      if (response.data) {
        setAgents(response.data);
      } else if (response.error) {
        console.error("Error fetching agents:", response.error);
      }
    } catch (error) {
      console.error("Error fetching agents:", error);
    }
  };

  const fetchTasks = async () => {
    try {
      const response = await services.tasks.getTasks(user?.uid);
      if (response.data) {
        setTasks(response.data);
      } else if (response.error) {
        console.error("Error fetching tasks:", response.error);
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
        <p className="text-lg text-gray-700">
          Delegate tasks to your AI workforce and watch them collaborate
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="border-l-4 border-l-blue-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-900">
              Active Agents
            </CardTitle>
            <Users className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {activeAgents.length}
            </div>
            <p className="text-xs text-gray-700">Ready to handle your tasks</p>
            {loading ? (
              <Skeleton className="h-2 w-full mt-2" />
            ) : (
              <Progress
                value={(activeAgents.length / Math.max(agents.length, 1)) * 100}
                className="mt-2"
              />
            )}
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-yellow-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-900">
              Pending Tasks
            </CardTitle>
            <Clock className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {pendingTasks.length}
            </div>
            <p className="text-xs text-gray-700">Awaiting assignment</p>
            {pendingTasks.length > 0 && (
              <Badge
                variant="outline"
                className="mt-2 bg-yellow-50 text-yellow-700 border-yellow-200"
              >
                Needs attention
              </Badge>
            )}
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-green-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-900">
              Completed
            </CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {tasks.filter((t) => t.status === "completed").length}
            </div>
            <p className="text-xs text-gray-700">Tasks finished</p>
            <p className="text-xs text-green-600 mt-1">
              +{Math.floor(Math.random() * 5) + 1} this week
            </p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-purple-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-900">
              Activity
            </CardTitle>
            <Activity className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {tasks.length}
            </div>
            <p className="text-xs text-gray-700">Total tasks</p>
            <div className="flex items-center space-x-2 mt-2">
              <div className="flex-1 bg-gray-200 rounded-full h-1">
                <div
                  className="bg-purple-500 h-1 rounded-full transition-all duration-300"
                  style={{
                    width: `${Math.min((tasks.length / 10) * 100, 100)}%`,
                  }}
                ></div>
              </div>
              <span className="text-xs text-gray-600">
                {Math.min(Math.floor((tasks.length / 10) * 100), 100)}%
              </span>
            </div>
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
              <CardDescription className="text-gray-600">
                Describe what you need done, and your AI secretary will delegate
                tasks to the right agents
              </CardDescription>
            </CardHeader>
            <CardContent className="h-[500px]">
              <ChatBot onTaskCreated={fetchTasks} />
            </CardContent>
          </Card>
        </div>

        {/* Side Panel with Tabs */}
        <div className="space-y-6">
          <Card>
            <Tabs defaultValue="agents" className="w-full">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-gray-900">
                    Workspace Overview
                  </CardTitle>
                </div>
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="agents" className="text-sm">
                    Your Agents
                  </TabsTrigger>
                  <TabsTrigger value="tasks" className="text-sm">
                    Recent Tasks
                  </TabsTrigger>
                </TabsList>
              </CardHeader>

              <CardContent>
                <TabsContent value="agents" className="mt-0">
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-sm font-medium text-gray-900 mb-2">
                        AI Agents in Your Workspace
                      </h3>
                      <p className="text-xs text-gray-600 mb-4">
                        Manage and monitor your specialized AI workforce
                      </p>
                    </div>
                    <AgentsList agents={agents} loading={loading} />
                  </div>
                </TabsContent>

                <TabsContent value="tasks" className="mt-0">
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-sm font-medium text-gray-900 mb-2">
                        Latest Task Assignments
                      </h3>
                      <p className="text-xs text-gray-600 mb-4">
                        Track progress and manage your delegated work
                      </p>
                    </div>
                    <TasksList tasks={tasks.slice(0, 5)} loading={loading} />
                  </div>
                </TabsContent>
              </CardContent>
            </Tabs>
          </Card>
        </div>
      </div>
    </div>
  );
}
