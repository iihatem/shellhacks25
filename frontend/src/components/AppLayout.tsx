"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/contexts/AuthContext";
import AppSidebar from "./AppSidebar";
import StatisticsCard from "./StatisticsCard";
import SecretaryChat from "./SecretaryChat";
import Dashboard from "./Dashboard";
import AgentsList from "./AgentsList";
import TasksList from "./TasksList";
import { Search, Mail, Bell, Play } from "lucide-react";

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
    <div className="h-screen flex bg-gray-50 overflow-hidden">
      {/* Sidebar */}
      <AppSidebar
        activeSection={activeSection}
        onSectionChange={setActiveSection}
        onLogout={handleLogout}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex-1 max-w-lg">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="Search agents, tasks, or settings..."
                  className="pl-10 bg-gray-50 border-gray-200"
                />
              </div>
            </div>

            <div className="flex items-center gap-4">
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
                <span className="text-sm font-medium text-gray-900">
                  {getUserName()}
                </span>
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
  return <SecretaryChat />;
}

// Agents Content Component
function AgentsContent() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">AI Agents</h1>
      <AgentsList agents={[]} loading={false} />
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
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Settings</h1>
      <Card className="p-6">
        <p className="text-gray-600">Settings panel coming soon...</p>
      </Card>
    </div>
  );
}
