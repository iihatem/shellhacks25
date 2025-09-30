"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import {
  LayoutDashboard,
  Users,
  CheckSquare,
  Settings,
  LogOut,
  Play,
} from "lucide-react";

interface AppSidebarProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
  onLogout?: () => void;
}

export default function AppSidebar({
  activeSection,
  onSectionChange,
  onLogout,
}: AppSidebarProps) {
  const navigationItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "agents", label: "Agents", icon: Users },
    { id: "tasks", label: "Task", icon: CheckSquare },
  ];

  const friends = [
    { id: "1", name: "Bagas Mahpie", role: "Friend", avatar: "BM" },
    { id: "2", name: "Sir Dandy", role: "Old Friend", avatar: "SD" },
    { id: "3", name: "Jhon Tosan", role: "Friend", avatar: "JT" },
  ];

  return (
    <div className="w-64 bg-card border-r border-border flex flex-col h-full">
      {/* Header */}
      <div className="p-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 flex items-center justify-center">
            <img src="/logo.svg" alt="Panoptes Logo" className="w-12 h-12" />
          </div>
          <h1 className="text-xl font-bold text-card-foreground">Panoptes</h1>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <div className="space-y-1 mb-8">
          <h3 className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-3">
            OVERVIEW
          </h3>
          {navigationItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onSectionChange(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-colors ${
                activeSection === item.id
                  ? "bg-accent text-accent-foreground border-r-2 border-r-blue-600"
                  : "text-card-foreground hover:bg-accent hover:text-accent-foreground"
              }`}
            >
              <item.icon
                className={`w-5 h-5 ${
                  activeSection === item.id ? "text-blue-600" : "text-gray-500"
                }`}
              />
              <span className="font-medium">{item.label}</span>
            </button>
          ))}
        </div>

        {/* Friends Section */}
        <div className="mb-8">
          <h3 className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-3">
            Collaborators
          </h3>
          <div className="space-y-2">
            {friends.map((friend) => (
              <div
                key={friend.id}
                className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-50"
              >
                <Avatar className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white text-xs font-medium">
                  {friend.avatar}
                </Avatar>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {friend.name}
                  </p>
                  <p className="text-xs text-gray-500">{friend.role}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </nav>

      {/* Settings Section */}
      <div className="p-4 border-t border-gray-100">
        <div className="space-y-1">
          <h3 className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-3">
            SETTINGS
          </h3>
          <button
            onClick={() => onSectionChange("settings")}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-colors ${
              activeSection === "settings"
                ? "bg-blue-50 text-blue-700"
                : "text-gray-700 hover:bg-gray-50 hover:text-gray-900"
            }`}
          >
            <Settings
              className={`w-5 h-5 ${
                activeSection === "settings" ? "text-blue-600" : "text-gray-500"
              }`}
            />
            <span className="font-medium">Setting</span>
          </button>

          <button
            onClick={onLogout}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-colors text-red-600 hover:bg-red-50"
          >
            <LogOut className="w-5 h-5 text-red-500" />
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </div>
    </div>
  );
}
