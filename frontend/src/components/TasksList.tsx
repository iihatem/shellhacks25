"use client";

import { Badge } from "@/components/ui/badge";
import { Clock, CheckCircle, AlertCircle, XCircle } from "lucide-react";

interface Task {
  id: string;
  description: string;
  assigned_agent_id?: string;
  status: string;
  created_at: string;
}

interface TasksListProps {
  tasks: Task[];
  loading: boolean;
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case "completed":
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    case "in_progress":
      return <Clock className="w-4 h-4 text-blue-500" />;
    case "failed":
      return <XCircle className="w-4 h-4 text-red-500" />;
    default:
      return <AlertCircle className="w-4 h-4 text-yellow-500" />;
  }
};

const getStatusColor = (status: string) => {
  switch (status) {
    case "completed":
      return "bg-green-100 text-green-800";
    case "in_progress":
      return "bg-blue-100 text-blue-800";
    case "failed":
      return "bg-red-100 text-red-800";
    default:
      return "bg-yellow-100 text-yellow-800";
  }
};

export default function TasksList({ tasks, loading }: TasksListProps) {
  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="p-3 border rounded-lg animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="flex items-center justify-between">
              <div className="h-3 bg-gray-200 rounded w-1/3"></div>
              <div className="h-5 bg-gray-200 rounded w-16"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-6 text-gray-500">
        <Clock className="w-12 h-12 mx-auto mb-2 opacity-50" />
        <p>No tasks yet</p>
        <p className="text-sm">Tasks will appear here as you delegate work</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <div
          key={task.id}
          className="p-3 border rounded-lg hover:bg-gray-50 transition-colors"
        >
          <div className="flex items-start justify-between mb-2">
            <p className="text-sm font-medium line-clamp-2 flex-1 mr-2">
              {task.description}
            </p>
            <div className="flex items-center space-x-1">
              {getStatusIcon(task.status)}
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="text-xs text-gray-500">
              {new Date(task.created_at).toLocaleDateString()}
            </div>

            <Badge className={`text-xs ${getStatusColor(task.status)}`}>
              {task.status.replace("_", " ")}
            </Badge>
          </div>

          {task.assigned_agent_id && (
            <div className="mt-2">
              <Badge variant="outline" className="text-xs">
                Agent: {task.assigned_agent_id}
              </Badge>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
