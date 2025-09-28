"use client";

import { useState } from "react";
import ChatSidebar from "./ChatSidebar";
import ConversationList from "./ConversationList";
import MainChatInterface from "./MainChatInterface";
import ContactInfoPanel from "./ContactInfoPanel";

export default function ChatLayout() {
  const [activeTab, setActiveTab] = useState("all");
  const [activeContactId, setActiveContactId] = useState("mary-franci");
  const [showContactInfo, setShowContactInfo] = useState(true);
  const [showConversationList, setShowConversationList] = useState(true);

  const handleContactSelect = (contactId: string) => {
    setActiveContactId(contactId);
    // On mobile, hide conversation list when a chat is selected
    setShowConversationList(false);
  };

  const handleShowContactInfo = () => {
    setShowContactInfo(true);
  };

  const handleCloseContactInfo = () => {
    setShowContactInfo(false);
  };

  const handleBackToConversations = () => {
    setShowConversationList(true);
  };

  return (
    <div className="h-screen flex bg-gray-100 overflow-hidden">
      {/* Left Sidebar - Hidden on mobile, shown on desktop */}
      <div className="hidden lg:block">
        <ChatSidebar activeTab={activeTab} onTabChange={setActiveTab} />
      </div>

      {/* Conversation List - Responsive visibility */}
      <div className={`${showConversationList ? "block" : "hidden"} lg:block`}>
        <ConversationList
          activeContactId={activeContactId}
          onContactSelect={handleContactSelect}
        />
      </div>

      {/* Main Chat Area - Always visible when contact selected */}
      <div
        className={`flex-1 ${
          !showConversationList ? "block" : "hidden"
        } lg:block`}
      >
        <MainChatInterface
          activeContactId={activeContactId}
          onShowContactInfo={handleShowContactInfo}
          onBackToConversations={handleBackToConversations}
        />
      </div>

      {/* Contact Info Panel - Hidden on mobile by default */}
      {showContactInfo && (
        <div className="hidden xl:block">
          <ContactInfoPanel
            activeContactId={activeContactId}
            onClose={handleCloseContactInfo}
          />
        </div>
      )}
    </div>
  );
}
