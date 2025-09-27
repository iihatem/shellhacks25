"use client";

import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Clock,
  CheckCircle,
  AlertCircle,
  XCircle,
  Calendar,
  User,
} from "lucide-react";
import { Task } from "@/services";

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
      return "bg-green-600 text-white";
    case "in_progress":
      return "bg-blue-600 text-white";
    case "failed":
      return "bg-red-600 text-white";
    default:
      return "bg-yellow-600 text-white";
  }
};

export default function TasksList({ tasks, loading }: TasksListProps) {
  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="p-3 border border-gray-100 rounded-lg bg-white"
          >
            <div className="flex items-start justify-between mb-2">
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-4 w-4 rounded-full" />
            </div>
            <Skeleton className="h-3 w-1/2 mb-2" />
            <div className="flex items-center justify-between">
              <Skeleton className="h-3 w-1/4" />
              <Skeleton className="h-5 w-16 rounded-full" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 border border-gray-100 rounded-lg bg-gray-50/50">
        <Clock className="w-16 h-16 mx-auto mb-4 text-gray-400" />
        <h3 className="font-medium text-gray-700 mb-2">No tasks yet</h3>
        <p className="text-sm text-gray-600">
          Tasks will appear here as you delegate work
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <div
          key={task.id}
          className="p-3 border border-gray-100 rounded-lg hover:border-gray-200 hover:shadow-sm transition-all duration-200 bg-white"
        >
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1 mr-3">
              <p className="text-sm font-medium text-gray-900 line-clamp-2 mb-1">
                {task.description}
              </p>
              <div className="flex items-center space-x-3 text-xs text-gray-500">
                <div className="flex items-center space-x-1">
                  <Calendar className="w-3 h-3" />
                  <span>{new Date(task.created_at).toLocaleDateString()}</span>
                </div>
                {task.assigned_agent_id && (
                  <div className="flex items-center space-x-1">
                    <User className="w-3 h-3" />
                    <span>Agent assigned</span>
                  </div>
                )}
              </div>
            </div>
            <div className="flex items-center space-x-2">
              {getStatusIcon(task.status)}
              <Badge className={`text-xs ${getStatusColor(task.status)}`}>
                {task.status.replace("_", " ")}
              </Badge>
            </div>
          </div>

          {task.assigned_agent_id && (
            <div className="pt-2 border-t border-gray-100">
              <Badge
                variant="outline"
                className="text-xs bg-blue-50 text-blue-700 border-blue-200"
              >
                <User className="w-3 h-3 mr-1" />
                {task.assigned_agent_id}
              </Badge>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
