"use client";

import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Bot, Users, UserCheck } from "lucide-react";

interface Agent {
  id: string;
  name: string;
  role: string;
  capabilities: string[];
  is_active: boolean;
}

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
    default:
      return <Bot className="w-4 h-4" />;
  }
};

const getRoleColor = (role: string) => {
  switch (role) {
    case "secretary":
      return "bg-blue-500";
    case "hiring_manager":
      return "bg-green-500";
    default:
      return "bg-purple-500";
  }
};

export default function AgentsList({ agents, loading }: AgentsListProps) {
  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2].map((i) => (
          <div
            key={i}
            className="flex items-center space-x-3 p-2 animate-pulse"
          >
            <div className="w-10 h-10 bg-gray-200 rounded-full"></div>
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-1"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (agents.length === 0) {
    return (
      <div className="text-center py-6 text-gray-500">
        <Bot className="w-12 h-12 mx-auto mb-2 opacity-50" />
        <p>No agents in your workspace yet</p>
        <p className="text-sm">Send a message to get started!</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {agents.map((agent) => (
        <div
          key={agent.id}
          className="flex items-start space-x-3 p-2 hover:bg-gray-50 rounded-lg transition-colors"
        >
          <Avatar
            className={`w-10 h-10 ${getRoleColor(
              agent.role
            )} flex items-center justify-center`}
          >
            {getRoleIcon(agent.role)}
          </Avatar>

          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-1">
              <h4 className="font-medium text-sm truncate">{agent.name}</h4>
              <Badge
                variant={agent.is_active ? "default" : "secondary"}
                className="text-xs"
              >
                {agent.is_active ? "Active" : "Inactive"}
              </Badge>
            </div>

            <p className="text-xs text-gray-600 capitalize mb-2">
              {agent.role.replace("_", " ")}
            </p>

            <div className="flex flex-wrap gap-1">
              {agent.capabilities.slice(0, 2).map((capability, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  {capability.replace("_", " ")}
                </Badge>
              ))}
              {agent.capabilities.length > 2 && (
                <Badge variant="outline" className="text-xs">
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
