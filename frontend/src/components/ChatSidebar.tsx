"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Inbox,
  User,
  UserX,
  MessageCircle,
  Shield,
  Trash2,
  Crown,
  Sparkles,
} from "lucide-react";

interface ChatSidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export default function ChatSidebar({
  activeTab,
  onTabChange,
}: ChatSidebarProps) {
  const navigationItems = [
    { id: "all", label: "All", icon: Inbox, count: null },
    { id: "assigned", label: "Assigned to Me", icon: User, count: null },
    { id: "unassigned", label: "Unassigned", icon: UserX, count: null },
    { id: "live-chat", label: "Live Chat", icon: MessageCircle, count: null },
    { id: "blocked", label: "Blocked", icon: Shield, count: null, isPro: true },
    { id: "trash", label: "Trash", icon: Trash2, count: null },
  ];

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-full">
      {/* Header */}
      <div className="p-6 border-b border-gray-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-600 rounded-lg flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <h1 className="text-xl font-bold">Attmosfire</h1>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <div className="space-y-1">
          {navigationItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeTab === item.id
                  ? "bg-purple-600 text-white"
                  : "text-gray-300 hover:bg-gray-800 hover:text-white"
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="flex-1">{item.label}</span>
              {item.isPro && (
                <Badge className="bg-purple-500 text-white text-xs px-2 py-0.5">
                  PRO
                </Badge>
              )}
              {item.count && (
                <Badge
                  variant="secondary"
                  className="bg-gray-700 text-gray-300"
                >
                  {item.count}
                </Badge>
              )}
            </button>
          ))}
        </div>
      </nav>

      {/* Pro Plan Section */}
      <div className="p-4 border-t border-gray-800">
        <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl p-4 text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Crown className="w-5 h-5 text-yellow-300" />
            <span className="font-semibold">Pro Plan</span>
          </div>
          <p className="text-2xl font-bold mb-1">
            $189<span className="text-sm font-normal">/month</span>
          </p>
          <p className="text-sm text-purple-100 mb-4">
            Open a lot of cool features with our Premium Pro Plan
          </p>
          <Button
            className="w-full bg-gray-900 hover:bg-gray-800 text-white"
            size="sm"
          >
            Get Pro Plan
          </Button>
        </div>
      </div>
    </div>
  );
}
