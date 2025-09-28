"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
  Send,
  Paperclip,
  Mic,
  Smile,
  MoreVertical,
  Phone,
  Video,
  Info,
  ArrowLeft,
} from "lucide-react";

interface ChatMessage {
  id: string;
  text: string;
  sender: "user" | "contact";
  timestamp: Date;
  type?: "text" | "file" | "voice";
  fileName?: string;
  fileSize?: string;
  status?: "sent" | "delivered" | "read";
}

interface MainChatInterfaceProps {
  activeContactId: string;
  onShowContactInfo: () => void;
  onBackToConversations?: () => void;
}

export default function MainChatInterface({
  activeContactId,
  onShowContactInfo,
  onBackToConversations,
}: MainChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Mock contact data
  const contactData = {
    "mary-franci": {
      name: "Mary Franci",
      phone: "+ (1) 234-543-4321",
      isOnline: true,
      messages: [
        {
          id: "1",
          text: "Can I try the software first?",
          sender: "contact" as const,
          timestamp: new Date(Date.now() - 300000),
          status: "read" as const,
        },
        {
          id: "2",
          text: "Sure. Here is the demo unit. You can use it as long as you want.",
          sender: "user" as const,
          timestamp: new Date(Date.now() - 240000),
          status: "read" as const,
        },
        {
          id: "3",
          text: "Thank you. Now I want to buy the software. Which type of subscription do you have?",
          sender: "contact" as const,
          timestamp: new Date(Date.now() - 180000),
          status: "read" as const,
        },
        {
          id: "4",
          text: "We have many type of subscription in this presentations. Please look at this showcase.",
          sender: "user" as const,
          timestamp: new Date(Date.now() - 120000),
          status: "delivered" as const,
        },
        {
          id: "5",
          text: "Presentation.pdf",
          sender: "user" as const,
          timestamp: new Date(Date.now() - 120000),
          type: "file" as const,
          fileName: "Presentation.pdf",
          fileSize: "254 KB",
          status: "delivered" as const,
        },
        {
          id: "6",
          text: "Thanks. I will watch it later!",
          sender: "contact" as const,
          timestamp: new Date(Date.now() - 60000),
          status: "read" as const,
        },
      ],
    },
  };

  const currentContact =
    contactData[activeContactId as keyof typeof contactData];

  useEffect(() => {
    if (currentContact) {
      setMessages(currentContact.messages);
    }
  }, [activeContactId, currentContact]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = () => {
    if (!inputValue.trim()) return;

    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      text: inputValue,
      sender: "user",
      timestamp: new Date(),
      status: "sent",
    };

    setMessages((prev) => [...prev, newMessage]);
    setInputValue("");

    // Simulate typing indicator
    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      // Could add auto-response here
    }, 2000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!currentContact) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Select a conversation
          </h3>
          <p className="text-gray-600">
            Choose a contact from the sidebar to start chatting
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center gap-3">
          {onBackToConversations && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onBackToConversations}
              className="lg:hidden"
            >
              <ArrowLeft className="w-4 h-4" />
            </Button>
          )}
          <Avatar className="w-10 h-10 bg-blue-500 flex items-center justify-center text-white font-medium">
            {currentContact.name
              .split(" ")
              .map((n) => n[0])
              .join("")}
          </Avatar>
          <div>
            <h3 className="font-medium text-gray-900">{currentContact.name}</h3>
            <div className="flex items-center gap-2">
              <Phone className="w-3 h-3 text-gray-400" />
              <span className="text-sm text-gray-500">
                {currentContact.phone}
              </span>
              {currentContact.isOnline && (
                <Badge className="bg-green-100 text-green-700 text-xs px-2 py-0.5">
                  Online
                </Badge>
              )}
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
          <Button variant="ghost" size="sm" onClick={onShowContactInfo}>
            <Info className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="sm">
            <MoreVertical className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[70%] rounded-2xl px-4 py-3 ${
                  message.sender === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-100 text-gray-900"
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

                <div
                  className={`flex items-center justify-between mt-2 text-xs ${
                    message.sender === "user"
                      ? "text-blue-100"
                      : "text-gray-500"
                  }`}
                >
                  <span>
                    {message.timestamp.toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </span>
                  {message.sender === "user" && message.status && (
                    <Badge
                      variant="outline"
                      className={`ml-2 text-xs ${
                        message.status === "delivered"
                          ? "bg-green-50 text-green-600 border-green-200"
                          : "bg-gray-50 text-gray-600 border-gray-200"
                      }`}
                    >
                      {message.status === "delivered"
                        ? "via SMS"
                        : message.status}
                    </Badge>
                  )}
                </div>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-2xl px-4 py-3">
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                  </div>
                  <span className="text-xs text-gray-600">Typing...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-200 bg-white">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm">
            <Paperclip className="w-4 h-4" />
          </Button>

          <div className="flex-1 relative">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="You are welcome!"
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
            disabled={!inputValue.trim()}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
