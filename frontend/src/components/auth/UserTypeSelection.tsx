"use client";

import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Briefcase,
  GraduationCap,
  Users,
  Palette,
  PenTool,
  CheckCircle,
} from "lucide-react";

const userTypes = [
  {
    id: "ceo",
    label: "CEO / Executive",
    icon: Briefcase,
    description:
      "Manage teams, delegate strategic tasks, and oversee business operations",
    agents: [
      "Executive Secretary",
      "Strategy Consultant",
      "Project Manager",
      "Data Analyst",
    ],
    color: "bg-blue-600",
  },
  {
    id: "student",
    label: "Student",
    icon: GraduationCap,
    description:
      "Get help with studies, assignments, research, and academic planning",
    agents: [
      "Study Assistant",
      "Research Helper",
      "Writing Tutor",
      "Schedule Manager",
    ],
    color: "bg-green-600",
  },
  {
    id: "tutor",
    label: "Tutor / Teacher",
    icon: Users,
    description:
      "Create educational content, manage students, and develop curricula",
    agents: [
      "Content Creator",
      "Assessment Builder",
      "Student Tracker",
      "Curriculum Designer",
    ],
    color: "bg-purple-600",
  },
  {
    id: "designer",
    label: "Designer",
    icon: Palette,
    description: "Manage creative projects, client work, and design workflows",
    agents: [
      "Creative Director",
      "Client Manager",
      "Asset Organizer",
      "Feedback Collector",
    ],
    color: "bg-pink-600",
  },
  {
    id: "content_creator",
    label: "Content Creator",
    icon: PenTool,
    description:
      "Streamline content production, publishing, and audience engagement",
    agents: [
      "Content Planner",
      "Social Media Manager",
      "Analytics Tracker",
      "Brand Manager",
    ],
    color: "bg-orange-600",
  },
];

export default function UserTypeSelection() {
  const { userProfile, updateUserType } = useAuth();
  const [selectedType, setSelectedType] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const handleSelectUserType = async () => {
    if (!selectedType) return;

    try {
      setLoading(true);
      await updateUserType(selectedType);
    } catch (error) {
      console.error("Error updating user type:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome, {userProfile?.displayName}!
          </h1>
          <p className="text-lg text-gray-700 mb-4">
            Choose your role to get personalized AI agents
          </p>
          <p className="text-gray-600">
            This will determine which types of agents are available in your
            workspace
          </p>
        </div>

        {/* User Type Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {userTypes.map((type) => {
            const Icon = type.icon;
            const isSelected = selectedType === type.id;

            return (
              <Card
                key={type.id}
                className={`cursor-pointer transition-all hover:shadow-lg ${
                  isSelected
                    ? "ring-2 ring-blue-500 shadow-lg"
                    : "hover:shadow-md"
                }`}
                onClick={() => setSelectedType(type.id)}
              >
                <CardHeader className="relative">
                  {isSelected && (
                    <div className="absolute top-4 right-4">
                      <CheckCircle className="w-6 h-6 text-blue-500" />
                    </div>
                  )}
                  <div
                    className={`w-12 h-12 rounded-lg ${type.color} flex items-center justify-center mb-3`}
                  >
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <CardTitle className="text-lg">{type.label}</CardTitle>
                  <CardDescription className="text-sm">
                    {type.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-sm font-medium text-gray-700">
                      Default Agents:
                    </p>
                    <div className="flex flex-wrap gap-1">
                      {type.agents.map((agent) => (
                        <Badge
                          key={agent}
                          variant="secondary"
                          className="text-xs"
                        >
                          {agent}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Continue Button */}
        <div className="text-center">
          <Button
            onClick={handleSelectUserType}
            disabled={!selectedType || loading}
            size="lg"
            className="px-8"
          >
            {loading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Setting up your workspace...
              </div>
            ) : (
              "Continue to Dashboard"
            )}
          </Button>

          {selectedType && (
            <p className="text-sm text-gray-600 mt-2">
              You can change this later in your profile settings
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
