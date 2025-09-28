"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Send, Bot, User, Loader2 } from "lucide-react";
import { services, Message } from "@/services";

interface ChatBotProps {
  onTaskCreated: () => void;
}

export default function ChatBot({ onTaskCreated }: ChatBotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Hello! I'm your Executive Secretary. I'm here to help you delegate tasks to the right team members. What would you like to get done today?",
      sender: "agent",
      agentName: "Executive Secretary",
      timestamp: new Date(),
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

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await services.chat.sendMessage(inputValue, "user-123");

      if (response.data) {
        const agentMessage: Message = {
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
          response.data.action_taken.includes("task")
        ) {
          onTaskCreated();
        }
      } else if (response.error) {
        throw new Error(response.error);
      }
    } catch (error) {
      console.error("Error sending message:", error);

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm sorry, I'm having trouble connecting to the backend. Please make sure the FastAPI server is running on port 8001.",
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
    <div className="flex flex-col h-full bg-white">
      {/* Messages Container */}
      <div className="flex-1 px-4 overflow-y-auto">
        <div className="space-y-4 py-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {message.sender === "agent" && (
                <Avatar className="w-8 h-8 bg-blue-600 flex items-center justify-center shadow-sm">
                  <Bot className="w-4 h-4 text-white" />
                </Avatar>
              )}

              <div
                className={`max-w-[80%] rounded-xl p-4 shadow-sm ${
                  message.sender === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-50 text-gray-900 border border-gray-100"
                }`}
              >
                {message.sender === "agent" && message.agentName && (
                  <div className="flex items-center gap-2 mb-2">
                    <Badge
                      variant="secondary"
                      className="text-xs bg-blue-100 text-blue-700"
                    >
                      {message.agentName}
                    </Badge>
                    {message.actionTaken && (
                      <Badge
                        variant="outline"
                        className="text-xs bg-green-50 text-green-700 border-green-200"
                      >
                        {message.actionTaken}
                      </Badge>
                    )}
                  </div>
                )}

                <p className="text-sm whitespace-pre-wrap leading-relaxed">
                  {message.text}
                </p>

                <div
                  className={`text-xs mt-2 ${
                    message.sender === "user"
                      ? "text-blue-100"
                      : "text-gray-500"
                  }`}
                >
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>

              {message.sender === "user" && (
                <Avatar className="w-8 h-8 bg-gray-600 flex items-center justify-center shadow-sm">
                  <User className="w-4 h-4 text-white" />
                </Avatar>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3 justify-start">
              <Avatar className="w-8 h-8 bg-blue-600 flex items-center justify-center shadow-sm">
                <Loader2 className="w-4 h-4 text-white animate-spin" />
              </Avatar>
              <div className="bg-gray-50 border border-gray-100 rounded-xl p-4 shadow-sm">
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
      <div className="border-t border-gray-100 bg-gray-50/50 p-4">
        <div className="flex gap-3">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Describe what you need done..."
            disabled={isLoading}
            className="flex-1 bg-white border-gray-200 focus:border-blue-500 focus:ring-blue-500"
          />
          <Button
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
        <p className="text-xs text-gray-600 mt-2 flex items-center gap-2">
          <span>Press Enter to send, Shift+Enter for new line</span>
          <Badge variant="outline" className="text-xs bg-white">
            Powered by AI
          </Badge>
        </p>
      </div>
    </div>
  );
}
