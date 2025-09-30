"use client";

import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Bot, Users, UserCheck, Activity, Zap } from "lucide-react";
import { Agent } from "@/services";

interface AgentsListProps {
  agents: Agent[];
  loading: boolean;
}

const getRoleIcon = (role: string) => {
  switch (role) {
    case "secretary":
      return <UserCheck className="w-4 h-4" />;
    case "hiring_manager":
      return <Users className="w-4 h-4" />;
    case "data_analyst":
      return <Activity className="w-4 h-4" />;
    case "researcher":
      return <Zap className="w-4 h-4" />;
    case "content_creator":
      return <Bot className="w-4 h-4" />;
    case "agent_builder":
      return <Bot className="w-4 h-4" />;
    default:
      return <Bot className="w-4 h-4" />;
  }
};

const getRoleColor = (role: string) => {
  switch (role) {
    case "secretary":
      return "bg-blue-600";
    case "hiring_manager":
      return "bg-green-600";
    case "data_analyst":
      return "bg-orange-600";
    case "researcher":
      return "bg-purple-600";
    case "content_creator":
      return "bg-pink-600";
    case "agent_builder":
      return "bg-indigo-600";
    default:
      return "bg-gray-600";
  }
};

export default function AgentsList({ agents, loading }: AgentsListProps) {
  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="flex items-start space-x-3 p-3 border border-gray-100 rounded-lg"
          >
            <Skeleton className="w-10 h-10 rounded-full" />
            <div className="flex-1 space-y-2">
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-3 w-1/2" />
              <div className="flex space-x-2">
                <Skeleton className="h-5 w-16" />
                <Skeleton className="h-5 w-20" />
              </div>
            </div>
            <Skeleton className="h-6 w-16" />
          </div>
        ))}
      </div>
    );
  }

  if (agents.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 border border-gray-100 rounded-lg bg-gray-50/50">
        <Bot className="w-16 h-16 mx-auto mb-4 text-gray-400" />
        <h3 className="font-medium text-gray-700 mb-2">No agents available</h3>
        <p className="text-sm text-gray-600">
          Start a conversation to activate AI agents!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {agents.map((agent) => (
        <div
          key={agent.id}
          className="flex items-start space-x-3 p-3 border border-gray-100 rounded-lg hover:border-gray-200 hover:shadow-sm transition-all duration-200 bg-white"
        >
          <Avatar
            className={`w-10 h-10 ${getRoleColor(
              agent.role
            )} flex items-center justify-center shadow-sm`}
          >
            {getRoleIcon(agent.role)}
          </Avatar>

          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <h4 className="font-medium text-sm text-gray-900 truncate">
                  {agent.name}
                </h4>
                {agent.id.startsWith("a2a-") && (
                  <Badge
                    variant="outline"
                    className="text-xs bg-blue-50 text-blue-700 border-blue-200"
                  >
                    A2A
                  </Badge>
                )}
              </div>
              <div className="flex items-center space-x-2">
                {agent.is_active && (
                  <div className="flex items-center space-x-1">
                    <Activity className="w-3 h-3 text-green-500" />
                    <span className="text-xs text-green-600">Online</span>
                  </div>
                )}
                <Badge
                  variant={agent.is_active ? "default" : "secondary"}
                  className={`text-xs ${
                    agent.is_active
                      ? "bg-green-100 text-green-800 border-green-200"
                      : "bg-gray-100 text-gray-600 border-gray-200"
                  }`}
                >
                  {agent.is_active ? "Active" : "Inactive"}
                </Badge>
              </div>
            </div>

            <p className="text-xs text-gray-600 capitalize mb-3 font-medium">
              {agent.role.replace("_", " ")}
            </p>

            <div className="flex flex-wrap gap-1">
              {agent.capabilities.slice(0, 2).map((capability, index) => (
                <Badge
                  key={index}
                  variant="outline"
                  className="text-xs bg-blue-50 text-blue-700 border-blue-200"
                >
                  <Zap className="w-3 h-3 mr-1" />
                  {capability.replace("_", " ")}
                </Badge>
              ))}
              {agent.capabilities.length > 2 && (
                <Badge
                  variant="outline"
                  className="text-xs bg-gray-50 text-gray-600 border-gray-200"
                >
                  +{agent.capabilities.length - 2} more
                </Badge>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
