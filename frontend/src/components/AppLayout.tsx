"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/contexts/AuthContext";
import { services, Agent } from "@/services";
import AppSidebar from "./AppSidebar";
import StatisticsCard from "./StatisticsCard";
import FloatingChatInterface from "./FloatingChatInterface";
import Dashboard from "./Dashboard";
import AgentsList from "./AgentsList";
import TasksList from "./TasksList";
import SettingsPage from "./SettingsPage";
import { Search, Mail, Bell, Play, RefreshCw } from "lucide-react";

export default function AppLayout() {
  const { user, userProfile, logout } = useAuth();
  const [activeSection, setActiveSection] = useState("dashboard");
  const [showStatistics, setShowStatistics] = useState(true);

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  const getUserName = () => {
    return userProfile?.displayName || user?.displayName || "User";
  };

  const getUserAvatar = () => {
    return userProfile?.photoURL || user?.photoURL;
  };

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  };

  const renderMainContent = () => {
    switch (activeSection) {
      case "dashboard":
        return <DashboardContent />;
      case "agents":
        return <AgentsContent />;
      case "tasks":
        return <TasksContent />;
      case "settings":
        return <SettingsContent />;
      default:
        return <DashboardContent />;
    }
  };

  return (
    <div className="h-screen flex bg-background overflow-hidden">
      {/* Sidebar */}
      <AppSidebar
        activeSection={activeSection}
        onSectionChange={setActiveSection}
        onLogout={handleLogout}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-card border-b border-border px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex-1 mx-6 mr-10">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="Search agents, tasks, or settings..."
                  className="pl-10 bg-card border-border shadow-sm text-card-foreground placeholder:text-muted-foreground"
                />
              </div>
            </div>

            <div className="bg-card rounded-full shadow-sm border border-border px-6 py-3">
              <div className="flex items-center gap-2.5">
                <Button variant="ghost" size="sm">
                  <Mail className="w-5 h-5 text-gray-600" />
                </Button>
                <Button variant="ghost" size="sm">
                  <Bell className="w-5 h-5 text-gray-600" />
                </Button>
                <div className="flex items-center gap-3">
                  {getUserAvatar() ? (
                    <img
                      src={getUserAvatar()}
                      alt={getUserName()}
                      className="w-8 h-8 rounded-full object-cover"
                    />
                  ) : (
                    <Avatar className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 text-white text-sm font-medium">
                      {getInitials(getUserName())}
                    </Avatar>
                  )}
                  <span className="text-sm font-medium text-card-foreground">
                    {getUserName()}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 flex overflow-hidden">
          {/* Main Content */}
          <main
            className={`flex-1 overflow-y-auto ${showStatistics ? "mr-4" : ""}`}
          >
            {renderMainContent()}
          </main>

          {/* Statistics Panel - Fixed width sidebar */}
          {showStatistics && (
            <div className="flex-shrink-0">
              <StatisticsCard />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Dashboard Content Component
function DashboardContent() {
  const handleTaskCreated = () => {
    // Could refresh tasks or show notification
    console.log("Task created by AI agent");
  };

  return <FloatingChatInterface onTaskCreated={handleTaskCreated} />;
}

// Agents Content Component
function AgentsContent() {
  const { user } = useAuth();
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAgents();
  }, [user]);

  const getA2AAgents = (): Agent[] => {
    return [
      {
        id: "a2a-secretary",
        name: "Executive Secretary",
        role: "secretary",
        capabilities: [
          "coordination",
          "task_delegation",
          "workflow_management",
        ],
        is_active: true,
      },
      {
        id: "a2a-hiring-manager",
        name: "Hiring Manager",
        role: "hiring_manager",
        capabilities: [
          "agent_creation",
          "workforce_management",
          "specialization",
        ],
        is_active: true,
      },
      {
        id: "a2a-data-analyst",
        name: "Data Analyst",
        role: "data_analyst",
        capabilities: ["data_analysis", "statistics", "insights", "reporting"],
        is_active: true,
      },
      {
        id: "a2a-researcher",
        name: "Researcher",
        role: "researcher",
        capabilities: ["research", "fact_checking", "information_synthesis"],
        is_active: true,
      },
      {
        id: "a2a-content-creator",
        name: "Content Creator",
        role: "content_creator",
        capabilities: [
          "content_creation",
          "writing",
          "marketing",
          "creative_communications",
        ],
        is_active: true,
      },
      {
        id: "a2a-agent-builder",
        name: "Agent Builder Assistant",
        role: "agent_builder",
        capabilities: [
          "agent_building",
          "system_design",
          "yaml_configuration",
          "multi_agent_architecture",
        ],
        is_active: true,
      },
    ];
  };

  const fetchAgents = async () => {
    try {
      setLoading(true);
      const response = await services.agents.getAgents(user?.uid);
      const userAgents = response.data || [];
      const a2aAgents = getA2AAgents();

      // Combine user agents with A2A agents
      setAgents([...a2aAgents, ...userAgents]);

      if (response.error) {
        console.error("Error fetching user agents:", response.error);
      }
    } catch (error) {
      console.error("Error fetching agents:", error);
      // Still show A2A agents even if user agents fail to load
      setAgents(getA2AAgents());
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-card-foreground">AI Agents</h1>
          <p className="text-muted-foreground mt-1">
            Manage your specialized AI workforce • {agents.length} agents
            available
          </p>
        </div>
        <Button onClick={fetchAgents} variant="outline" size="sm">
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </Button>
      </div>
      <AgentsList agents={agents} loading={loading} />
    </div>
  );
}

// Tasks Content Component
function TasksContent() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Tasks</h1>
      <TasksList tasks={[]} loading={false} />
    </div>
  );
}

// Settings Content Component
function SettingsContent() {
  return <SettingsPage />;
}
