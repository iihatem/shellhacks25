"use client";

import { useState } from "react";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  Phone,
  Mail,
  Calendar,
  ChevronDown,
  ChevronUp,
  FileText,
  Link,
  BookOpen,
  X,
} from "lucide-react";

interface ContactInfoPanelProps {
  activeContactId: string;
  onClose: () => void;
}

export default function ContactInfoPanel({
  activeContactId,
  onClose,
}: ContactInfoPanelProps) {
  const [expandedSections, setExpandedSections] = useState({
    general: true,
    notes: true,
    sharedFiles: false,
    sharedLinks: false,
    documentations: false,
  });

  // Mock contact data
  const contactData = {
    "mary-franci": {
      name: "Mary Franci",
      phone: "+ (1) 234-543-4321",
      email: "mary_franci@gmail.com",
      dateCreated: "Oct 12, 2022 • 11:43",
      status: "Active User",
      notes: [
        {
          id: "1",
          text: "Eget pulvinar blandit tellus suspendisse augue sem lectus varius. Suspendisse sed imperdiet adipiscing.",
          date: "23 Oct, 2023",
        },
        {
          id: "2",
          text: "Eget pulvinar blandit tellus suspendisse.",
          date: "23 Oct, 2023",
        },
      ],
    },
  };

  const currentContact =
    contactData[activeContactId as keyof typeof contactData];

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  };

  if (!currentContact) {
    return null;
  }

  return (
    <div className="w-80 bg-white border-l border-gray-200 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">General info</h2>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Contact Info */}
      <div className="flex-1 overflow-y-auto">
        {/* Profile Section */}
        <div className="p-4">
          <div className="text-center mb-6">
            <Avatar className="w-16 h-16 bg-blue-500 flex items-center justify-center text-white font-medium text-lg mx-auto mb-3">
              {getInitials(currentContact.name)}
            </Avatar>
            <h3 className="font-semibold text-gray-900 mb-1">
              {currentContact.name}
            </h3>
            <div className="flex items-center justify-center gap-1 text-sm text-gray-600 mb-2">
              <Phone className="w-3 h-3" />
              <span>{currentContact.phone}</span>
            </div>
            <div className="flex items-center justify-center gap-1 text-sm text-gray-600 mb-3">
              <Mail className="w-3 h-3" />
              <span>{currentContact.email}</span>
            </div>
            <Badge className="bg-green-100 text-green-700 px-3 py-1">
              {currentContact.status}
            </Badge>
          </div>

          {/* General Info Section */}
          <div className="mb-6">
            <button
              onClick={() => toggleSection("general")}
              className="flex items-center justify-between w-full text-left mb-3"
            >
              <h4 className="font-medium text-gray-900">General info</h4>
              {expandedSections.general ? (
                <ChevronUp className="w-4 h-4 text-gray-500" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-500" />
              )}
            </button>

            {expandedSections.general && (
              <div className="space-y-3 text-sm">
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4 text-gray-400" />
                  <div>
                    <p className="text-gray-600">Email</p>
                    <p className="text-gray-900">{currentContact.email}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-gray-400" />
                  <div>
                    <p className="text-gray-600">Date Created</p>
                    <p className="text-gray-900">
                      {currentContact.dateCreated}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 flex items-center justify-center">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  </div>
                  <div>
                    <p className="text-gray-600">Status</p>
                    <p className="text-gray-900">{currentContact.status}</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          <Separator className="mb-6" />

          {/* Notes Section */}
          <div className="mb-6">
            <button
              onClick={() => toggleSection("notes")}
              className="flex items-center justify-between w-full text-left mb-3"
            >
              <h4 className="font-medium text-gray-900">Notes</h4>
              {expandedSections.notes ? (
                <ChevronUp className="w-4 h-4 text-gray-500" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-500" />
              )}
            </button>

            {expandedSections.notes && (
              <div className="space-y-4">
                {currentContact.notes.map((note) => (
                  <div key={note.id} className="bg-gray-50 rounded-lg p-3">
                    <p className="text-sm text-gray-700 mb-2">{note.text}</p>
                    <p className="text-xs text-gray-500">{note.date}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <Separator className="mb-6" />

          {/* Additional Info Section */}
          <div className="mb-6">
            <button
              onClick={() => toggleSection("sharedFiles")}
              className="flex items-center justify-between w-full text-left mb-3"
            >
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-gray-500" />
                <h4 className="font-medium text-gray-900">Shared Files</h4>
              </div>
              {expandedSections.sharedFiles ? (
                <ChevronUp className="w-4 h-4 text-gray-500" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-500" />
              )}
            </button>

            {expandedSections.sharedFiles && (
              <div className="text-sm text-gray-600 pl-6">
                No shared files yet
              </div>
            )}
          </div>

          <div className="mb-6">
            <button
              onClick={() => toggleSection("sharedLinks")}
              className="flex items-center justify-between w-full text-left mb-3"
            >
              <div className="flex items-center gap-2">
                <Link className="w-4 h-4 text-gray-500" />
                <h4 className="font-medium text-gray-900">Shared Links</h4>
              </div>
              {expandedSections.sharedLinks ? (
                <ChevronUp className="w-4 h-4 text-gray-500" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-500" />
              )}
            </button>

            {expandedSections.sharedLinks && (
              <div className="text-sm text-gray-600 pl-6">
                No shared links yet
              </div>
            )}
          </div>

          <div className="mb-6">
            <button
              onClick={() => toggleSection("documentations")}
              className="flex items-center justify-between w-full text-left mb-3"
            >
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-gray-500" />
                <h4 className="font-medium text-gray-900">Documentations</h4>
              </div>
              {expandedSections.documentations ? (
                <ChevronUp className="w-4 h-4 text-gray-500" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-500" />
              )}
            </button>

            {expandedSections.documentations && (
              <div className="text-sm text-gray-600 pl-6">
                No documentation yet
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
