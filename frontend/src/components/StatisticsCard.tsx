"use client";

import { useState, useEffect } from "react";
import { Avatar } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import {
  MoreHorizontal,
  Plus,
  CheckCircle,
  Clock,
  AlertCircle,
} from "lucide-react";

interface StatisticsCardProps {
  // No props needed since we'll get user data from auth context
}

export default function StatisticsCard({}: StatisticsCardProps) {
  const { user, userProfile } = useAuth();
  const [tasks, setTasks] = useState([
    {
      id: 1,
      title: "Review AI Agent Performance",
      status: "pending",
      priority: "high",
    },
    {
      id: 2,
      title: "Update Task Delegation Rules",
      status: "in_progress",
      priority: "medium",
    },
    {
      id: 3,
      title: "Train New Agent Model",
      status: "completed",
      priority: "high",
    },
    {
      id: 4,
      title: "Optimize Response Time",
      status: "pending",
      priority: "low",
    },
  ]);

  const [agents, setAgents] = useState([
    {
      id: 1,
      name: "Executive Secretary",
      role: "Secretary",
      status: "online",
      avatar: "ES",
    },
    {
      id: 2,
      name: "Hiring Manager",
      role: "HR",
      status: "online",
      avatar: "HM",
    },
    {
      id: 3,
      name: "Data Analyst",
      role: "Analytics",
      status: "offline",
      avatar: "DA",
    },
  ]);

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  };

  const getUserName = () => {
    return userProfile?.displayName || user?.displayName || "User";
  };

  const getUserAvatar = () => {
    return userProfile?.photoURL || user?.photoURL;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case "in_progress":
        return <Clock className="w-4 h-4 text-blue-500" />;
      case "pending":
        return <AlertCircle className="w-4 h-4 text-yellow-500" />;
      default:
        return <Clock className="w-4 h-4 text-gray-400" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "bg-red-100 text-red-700";
      case "medium":
        return "bg-yellow-100 text-yellow-700";
      case "low":
        return "bg-green-100 text-green-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  return (
    <div className="w-80 bg-white rounded-xl shadow-lg border border-gray-200 flex flex-col h-fit max-h-[calc(100vh-8rem)] overflow-y-auto my-4 mr-4">
      {/* Header */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Statistic</h2>
          <Button variant="ghost" size="sm">
            <MoreHorizontal className="w-4 h-4" />
          </Button>
        </div>

        {/* User Profile */}
        <div className="flex flex-col items-center mb-6">
          <div className="mb-4">
            <div className="w-20 h-20 rounded-full flex items-center justify-center overflow-hidden">
              {getUserAvatar() ? (
                <img
                  src={getUserAvatar()!}
                  alt={getUserName()}
                  className="w-full h-full object-cover rounded-full"
                />
              ) : (
                <Avatar className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 text-white text-lg font-bold">
                  {getInitials(getUserName())}
                </Avatar>
              )}
            </div>
          </div>

          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              Good Morning {getUserName()} 👋
            </h3>
            <p className="text-sm text-gray-600">
              Manage your AI agents and delegate tasks efficiently!
            </p>
          </div>
        </div>
      </div>

      {/* Tasks Section */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900">Your Tasks</h3>
          <Button variant="ghost" size="sm">
            <Plus className="w-4 h-4" />
          </Button>
        </div>

        <div className="space-y-3">
          {tasks.slice(0, 4).map((task) => (
            <div
              key={task.id}
              className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
            >
              {getStatusIcon(task.status)}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {task.title}
                </p>
                <div className="flex items-center gap-2 mt-1">
                  <Badge
                    className={`text-xs px-2 py-0.5 ${getPriorityColor(
                      task.priority
                    )}`}
                  >
                    {task.priority}
                  </Badge>
                  <span className="text-xs text-gray-500 capitalize">
                    {task.status.replace("_", " ")}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Agents Section */}
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900">Your Agents</h3>
          <Button variant="ghost" size="sm">
            <Plus className="w-4 h-4" />
          </Button>
        </div>

        <div className="space-y-3">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
            >
              <div className="relative">
                <Avatar className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-600 text-white text-sm font-medium">
                  {agent.avatar}
                </Avatar>
                <div
                  className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white ${
                    agent.status === "online" ? "bg-green-500" : "bg-gray-400"
                  }`}
                ></div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {agent.name}
                </p>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-xs text-gray-500">{agent.role}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
