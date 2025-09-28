"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Search, Phone, MessageSquare } from "lucide-react";

interface Contact {
  id: string;
  name: string;
  phone: string;
  avatar?: string;
  lastMessage: string;
  timestamp: string;
  isOnline?: boolean;
  hasUnread?: boolean;
  messageType?: "text" | "voice" | "file";
  status?: "delivered" | "read" | "sent";
}

interface ConversationListProps {
  activeContactId: string;
  onContactSelect: (contactId: string) => void;
}

export default function ConversationList({
  activeContactId,
  onContactSelect,
}: ConversationListProps) {
  const [searchQuery, setSearchQuery] = useState("");

  // Mock data - in real app this would come from props or API
  const contacts: Contact[] = [
    {
      id: "mary-franci",
      name: "Mary Franci",
      phone: "+ (1) 234-543-4321",
      lastMessage: "Can I try the software first?",
      timestamp: "12:38",
      hasUnread: true,
      messageType: "text",
    },
    {
      id: "aspen-workman",
      name: "Aspen Workman",
      phone: "+ (1) 234-543-4321",
      lastMessage: "Hello! I am looking for a new p...",
      timestamp: "12:38",
      messageType: "text",
    },
    {
      id: "rhiel-madsen",
      name: "Rhiel Madsen",
      phone: "+ (1) 234-543-4321",
      lastMessage: "Typing...",
      timestamp: "12:38",
      isOnline: true,
      messageType: "text",
    },
    {
      id: "carla-dokidis",
      name: "Carla Dokidis",
      phone: "+ (1) 234-543-4321",
      lastMessage: "It works for me! Thanks",
      timestamp: "12:38",
      messageType: "text",
    },
    {
      id: "maria-vetrovs",
      name: "Maria Vetrovs",
      phone: "+ (1) 234-543-4321",
      lastMessage: "Let's stay in touch!",
      timestamp: "12:38",
      status: "delivered",
    },
    {
      id: "mary-franci-2",
      name: "Mary Franci",
      phone: "+ (1) 234-543-4321",
      lastMessage: "Thanks. I will watch it later...",
      timestamp: "12:38",
      messageType: "text",
    },
    {
      id: "omar-vetrovs",
      name: "Omar Vetrovs",
      phone: "+ (1) 234-543-4321",
      lastMessage: "Voice message",
      timestamp: "12:38",
      messageType: "voice",
    },
    {
      id: "marcus-bergson",
      name: "Marcus Bergson",
      phone: "+ (1) 234-543-4321",
      lastMessage: "Hello! I am looking for a new p...",
      timestamp: "12:38",
      messageType: "text",
    },
  ];

  const filteredContacts = contacts.filter(
    (contact) =>
      contact.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      contact.phone.includes(searchQuery)
  );

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  };

  const getAvatarColor = (name: string) => {
    const colors = [
      "bg-blue-500",
      "bg-green-500",
      "bg-purple-500",
      "bg-pink-500",
      "bg-yellow-500",
      "bg-indigo-500",
      "bg-red-500",
      "bg-teal-500",
    ];
    const index = name.charCodeAt(0) % colors.length;
    return colors[index];
  };

  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Chat</h2>
          <div className="flex gap-2">
            <span className="text-sm text-gray-500">Contacts</span>
            <span className="text-sm text-gray-500">Templates</span>
            <span className="text-sm text-gray-500">My Projects</span>
          </div>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 bg-gray-50 border-gray-200"
          />
        </div>
      </div>

      {/* Conversations */}
      <div className="flex-1 overflow-y-auto">
        {filteredContacts.map((contact) => (
          <div
            key={contact.id}
            onClick={() => onContactSelect(contact.id)}
            className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 transition-colors ${
              activeContactId === contact.id
                ? "bg-blue-50 border-r-2 border-r-blue-500"
                : ""
            }`}
          >
            <div className="flex items-start gap-3">
              {/* Avatar */}
              <div className="relative">
                <Avatar
                  className={`w-12 h-12 ${getAvatarColor(
                    contact.name
                  )} flex items-center justify-center text-white font-medium`}
                >
                  {getInitials(contact.name)}
                </Avatar>
                {contact.isOnline && (
                  <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white"></div>
                )}
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <h3 className="font-medium text-gray-900 truncate">
                    {contact.name}
                  </h3>
                  <span className="text-xs text-gray-500">
                    {contact.timestamp}
                  </span>
                </div>

                <div className="flex items-center gap-1 mb-1">
                  <Phone className="w-3 h-3 text-gray-400" />
                  <span className="text-xs text-gray-500">{contact.phone}</span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    {contact.messageType === "voice" && (
                      <MessageSquare className="w-3 h-3 text-gray-400 flex-shrink-0" />
                    )}
                    <p
                      className={`text-sm truncate ${
                        contact.hasUnread
                          ? "text-gray-900 font-medium"
                          : "text-gray-600"
                      } ${
                        contact.isOnline && contact.lastMessage === "Typing..."
                          ? "text-blue-500 italic"
                          : ""
                      }`}
                    >
                      {contact.lastMessage}
                    </p>
                  </div>

                  <div className="flex items-center gap-2 ml-2">
                    {contact.status === "delivered" && (
                      <Badge
                        variant="outline"
                        className="text-xs bg-green-50 text-green-600 border-green-200"
                      >
                        via SMS
                      </Badge>
                    )}
                    {contact.hasUnread && (
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
