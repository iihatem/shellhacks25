"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { Send, Paperclip, Mic, Smile, FileText } from "lucide-react";
import { services } from "@/services";

interface ChatMessage {
  id: string;
  text: string;
  sender: "user" | "agent";
  timestamp: Date;
  agentName?: string;
  actionTaken?: string;
  type?: "text" | "file";
  fileName?: string;
  fileSize?: string;
  status?: "sent" | "delivered" | "read";
}

export default function SecretaryChat() {
  const { user, userProfile } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      text: "Hello! I'm your Executive Secretary. I'm here to help you delegate tasks to the right team members. What would you like to get done today?",
      sender: "agent",
      agentName: "Executive Secretary",
      timestamp: new Date(Date.now() - 300000),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

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

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    console.log("Sending message:", inputValue); // Debug log

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: inputValue,
      sender: "user",
      timestamp: new Date(),
      status: "sent",
    };

    setMessages((prev) => [...prev, userMessage]);
    const messageText = inputValue; // Store message before clearing input
    setInputValue("");
    setIsLoading(true);

    try {
      console.log("Calling services.chat.sendMessage..."); // Debug log
      const response = await services.chat.sendMessage(
        messageText,
        user?.uid || "user-123"
      );
      console.log("Response received:", response); // Debug log

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
      } else if (response.error) {
        throw new Error(response.error);
      }
    } catch (error) {
      console.error("Error sending message:", error);

      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: "I'm sorry, I'm having trouble connecting to the backend. Please make sure the FastAPI server is running on port 8000.",
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

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 flex flex-col h-[calc(100vh-8rem)] mx-4 my-4">
      {/* Chat Header */}
      <div className="p-4 border-b border-gray-100 rounded-t-xl bg-gray-50">
        <div className="flex items-center gap-3">
          <Avatar className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 text-white font-medium">
            ES
          </Avatar>
          <div>
            <h3 className="font-semibold text-gray-900">Executive Secretary</h3>
            <p className="text-sm text-gray-600">AI Assistant • Online</p>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
        <div className="space-y-4">
          {messages.map((message) => (
            <div key={message.id} className="flex flex-col">
              {/* Message Header with Avatar and Name */}
              <div
                className={`flex items-center gap-2 mb-2 ${
                  message.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {message.sender === "agent" && (
                  <>
                    <Avatar className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 text-white text-xs font-medium">
                      ES
                    </Avatar>
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {message.agentName || "Executive Secretary"}
                      </p>
                      <p className="text-xs text-gray-500">
                        {message.timestamp.toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </p>
                    </div>
                  </>
                )}
                {message.sender === "user" && (
                  <>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">
                        {getUserName()}
                      </p>
                      <p className="text-xs text-gray-500">
                        {message.timestamp.toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </p>
                    </div>
                    {getUserAvatar() ? (
                      <img
                        src={getUserAvatar()!}
                        alt={getUserName()}
                        className="w-8 h-8 rounded-full object-cover"
                      />
                    ) : (
                      <Avatar className="w-8 h-8 bg-gradient-to-br from-green-500 to-blue-500 text-white text-xs font-medium">
                        {getInitials(getUserName())}
                      </Avatar>
                    )}
                  </>
                )}
              </div>

              {/* Message Content */}
              <div
                className={`flex ${
                  message.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[70%] rounded-2xl px-4 py-3 ${
                    message.sender === "user"
                      ? "bg-blue-500 text-white ml-10"
                      : "bg-white text-gray-900 border border-gray-200 mr-10"
                  }`}
                >
                  {message.type === "file" ? (
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-red-500 rounded-lg flex items-center justify-center">
                        <FileText className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <p className="font-medium">{message.fileName}</p>
                        <p className="text-sm opacity-75">{message.fileSize}</p>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm leading-relaxed">{message.text}</p>
                  )}

                  {/* Status and Action Badges */}
                  <div className="flex items-center justify-between mt-2">
                    <div className="flex items-center gap-2">
                      {message.actionTaken && (
                        <Badge
                          variant="outline"
                          className="text-xs bg-green-50 text-green-700 border-green-200"
                        >
                          {message.actionTaken}
                        </Badge>
                      )}
                    </div>
                    {message.sender === "user" && message.status && (
                      <div className="flex items-center gap-1">
                        <Badge
                          variant="outline"
                          className={`text-xs ${
                            message.status === "delivered"
                              ? "bg-green-50 text-green-600 border-green-200"
                              : "bg-gray-50 text-gray-600 border-gray-200"
                          }`}
                        >
                          {message.status === "delivered"
                            ? "via SMS"
                            : message.status}
                        </Badge>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="flex items-center gap-2 mb-2">
                <Avatar className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 text-white text-xs font-medium">
                  ES
                </Avatar>
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    Executive Secretary
                  </p>
                  <p className="text-xs text-gray-500">typing...</p>
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
          <Button variant="ghost" size="sm" className="text-gray-500">
            <Paperclip className="w-4 h-4" />
          </Button>

          <Button variant="ghost" size="sm" className="text-gray-500">
            <Mic className="w-4 h-4" />
          </Button>

          <div className="flex-1 relative">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="You are welcome!"
              disabled={isLoading}
              className="pr-10 border-gray-200 focus:border-blue-500 focus:ring-blue-500 rounded-full"
            />
            <Button
              variant="ghost"
              size="sm"
              className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500"
            >
              <Smile className="w-4 h-4" />
            </Button>
          </div>

          <Button
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="bg-blue-500 hover:bg-blue-600 text-white rounded-full w-10 h-10 p-0"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
