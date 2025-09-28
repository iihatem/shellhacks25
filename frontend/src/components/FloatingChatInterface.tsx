"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { services, Message } from "@/services";
import {
  Send,
  Paperclip,
  Mic,
  Smile,
  Phone,
  Video,
  Info,
  Loader2,
} from "lucide-react";

interface ChatMessage {
  id: string;
  text: string;
  sender: "user" | "contact" | "agent";
  timestamp: Date;
  type?: "text" | "file" | "voice";
  fileName?: string;
  fileSize?: string;
  status?: "sent" | "delivered" | "read";
  agentName?: string;
  actionTaken?: string;
}

interface FloatingChatInterfaceProps {
  onTaskCreated?: () => void;
}

export default function FloatingChatInterface({
  onTaskCreated,
}: FloatingChatInterfaceProps) {
  const { user, userProfile } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      text: "Can I try the software first?",
      sender: "contact",
      timestamp: new Date(Date.now() - 300000),
      status: "read",
    },
    {
      id: "2",
      text: "Sure. Here is the demo unit. You can use it as long as you want.",
      sender: "user",
      timestamp: new Date(Date.now() - 240000),
      status: "delivered",
    },
    {
      id: "3",
      text: "Thank you. Now I want to buy the software. Which type of subscription do you have?",
      sender: "contact",
      timestamp: new Date(Date.now() - 180000),
      status: "read",
    },
    {
      id: "4",
      text: "We have many type of subscription in this presentations. Please look at this showcase.",
      sender: "user",
      timestamp: new Date(Date.now() - 120000),
      status: "delivered",
    },
    {
      id: "5",
      text: "Presentation.pdf",
      sender: "user",
      timestamp: new Date(Date.now() - 120000),
      type: "file",
      fileName: "Presentation.pdf",
      fileSize: "254 KB",
      status: "delivered",
    },
    {
      id: "6",
      text: "Thanks. I will watch it later!",
      sender: "contact",
      timestamp: new Date(Date.now() - 60000),
      status: "read",
    },
    // Separator message
    {
      id: "separator",
      text: "--- New Conversation ---",
      sender: "agent",
      agentName: "System",
      timestamp: new Date(Date.now() - 30000),
    },
    // AI Agent welcome message
    {
      id: "welcome",
      text: "Hello! I'm your AI Secretary. I can help you manage tasks, delegate work to specialized agents, and coordinate your AI workforce. What would you like to accomplish today?",
      sender: "agent",
      agentName: "Executive Secretary",
      timestamp: new Date(Date.now() - 10000),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: inputValue,
      sender: "user",
      timestamp: new Date(),
      status: "sent",
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      // Get user ID from auth context
      const userId = user?.uid || "user-123";
      const response = await services.chat.sendMessage(inputValue, userId);

      if (response.data) {
        const agentMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          text: response.data.response,
          sender: "agent",
          agentName: response.data.agent_name,
          timestamp: new Date(),
          actionTaken: response.data.action_taken,
        };

        setMessages((prev) => [...prev, agentMessage]);

        // If a task was created, refresh the tasks list
        if (
          response.data.action_taken &&
          response.data.action_taken.includes("task") &&
          onTaskCreated
        ) {
          onTaskCreated();
        }
      } else if (response.error) {
        throw new Error(response.error);
      }
    } catch (error) {
      console.error("Error sending message:", error);

      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: "I'm sorry, I'm having trouble connecting to the AI agents. Please make sure the backend server is running and try again.",
        sender: "agent",
        agentName: "System",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
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

  return (
    <div className="mx-4 my-4 bg-white rounded-xl shadow-lg border border-gray-200 flex flex-col h-[calc(100vh-8rem)] overflow-hidden">
      {/* Chat Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-100 bg-gray-50 rounded-t-xl">
        <div className="flex items-center gap-3">
          <Avatar className="w-10 h-10 bg-blue-500 flex items-center justify-center text-white font-medium">
            MF
          </Avatar>
          <div>
            <h3 className="font-medium text-gray-900">Mary Franci</h3>
            <div className="flex items-center gap-2">
              <Phone className="w-3 h-3 text-gray-400" />
              <span className="text-sm text-gray-500">+ (1) 234-543-4321</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm">
            <Phone className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="sm">
            <Video className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="sm">
            <Info className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
        <div className="space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {(message.sender === "contact" || message.sender === "agent") && (
                <Avatar className="w-8 h-8 bg-blue-500 flex items-center justify-center text-white text-xs font-medium mr-3 mt-1">
                  {message.sender === "contact"
                    ? "MF"
                    : message.agentName === "Executive Secretary"
                    ? "ES"
                    : message.agentName === "System"
                    ? "SYS"
                    : "AI"}
                </Avatar>
              )}

              <div className="flex flex-col max-w-[70%]">
                {(message.sender === "contact" ||
                  message.sender === "agent") && (
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-medium text-gray-900">
                      {message.sender === "contact"
                        ? "Mary Franci"
                        : message.agentName || "AI Agent"}
                    </span>
                    <span className="text-xs text-gray-500">
                      {message.timestamp.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                  </div>
                )}

                {message.sender === "agent" && message.actionTaken && (
                  <div className="flex items-center gap-2 mb-1">
                    <Badge className="text-xs bg-green-50 text-green-700 border-green-200">
                      {message.actionTaken}
                    </Badge>
                  </div>
                )}

                <div
                  className={`rounded-2xl px-4 py-3 ${
                    message.sender === "user"
                      ? "bg-blue-500 text-white self-end"
                      : "bg-white text-gray-900 border border-gray-200"
                  }`}
                >
                  {message.type === "file" ? (
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-red-500 rounded-lg flex items-center justify-center">
                        <Paperclip className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <p className="font-medium">{message.fileName}</p>
                        <p className="text-sm opacity-75">{message.fileSize}</p>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm">{message.text}</p>
                  )}
                </div>

                {message.sender === "user" && (
                  <div className="flex items-center justify-end gap-2 mt-1">
                    <span className="text-xs text-gray-500">
                      {message.timestamp.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                    {message.status === "delivered" && (
                      <Badge className="text-xs bg-green-50 text-green-600 border-green-200">
                        via SMS
                      </Badge>
                    )}
                  </div>
                )}
              </div>

              {message.sender === "user" && (
                <Avatar className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-xs font-medium ml-3 mt-1">
                  {getInitials(getUserName())}
                </Avatar>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <Avatar className="w-8 h-8 bg-blue-600 flex items-center justify-center text-white text-xs font-medium mr-3 mt-1">
                <Loader2 className="w-4 h-4 animate-spin" />
              </Avatar>
              <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                  </div>
                  <span className="text-xs text-gray-600">
                    AI is thinking...
                  </span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-100 bg-white rounded-b-xl">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm">
            <Paperclip className="w-4 h-4" />
          </Button>

          <div className="flex-1 relative">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask your AI assistant anything..."
              disabled={isLoading}
              className="pr-10 border-gray-200 focus:border-blue-500 focus:ring-blue-500"
            />
            <Button
              variant="ghost"
              size="sm"
              className="absolute right-2 top-1/2 transform -translate-y-1/2"
            >
              <Smile className="w-4 h-4" />
            </Button>
          </div>

          <Button variant="ghost" size="sm">
            <Mic className="w-4 h-4" />
          </Button>

          <Button
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 rounded-full"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
