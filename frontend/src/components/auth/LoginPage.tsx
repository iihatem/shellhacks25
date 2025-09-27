"use client";

import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Bot,
  Users,
  Briefcase,
  GraduationCap,
  Palette,
  PenTool,
} from "lucide-react";

export default function LoginPage() {
  const { signInWithGoogle, loading } = useAuth();

  const userTypes = [
    {
      id: "ceo",
      label: "CEO / Executive",
      icon: Briefcase,
      description: "Manage teams and delegate strategic tasks",
    },
    {
      id: "student",
      label: "Student",
      icon: GraduationCap,
      description: "Get help with studies and assignments",
    },
    {
      id: "tutor",
      label: "Tutor / Teacher",
      icon: Users,
      description: "Create educational content and manage students",
    },
    {
      id: "designer",
      label: "Designer",
      icon: Palette,
      description: "Manage creative projects and workflows",
    },
    {
      id: "content_creator",
      label: "Content Creator",
      icon: PenTool,
      description: "Streamline content production and publishing",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Bot className="w-12 h-12 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">
              AI Agent Platform
            </h1>
          </div>
          <p className="text-xl text-gray-700 mb-2">
            Your Personal AI Workforce Management System
          </p>
          <p className="text-gray-600">
            Delegate tasks to specialized AI agents tailored to your role
          </p>
        </div>

        {/* User Types Preview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {userTypes.map((type) => {
            const Icon = type.icon;
            return (
              <Card
                key={type.id}
                className="text-center hover:shadow-md transition-shadow"
              >
                <CardContent className="pt-6">
                  <Icon className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {type.label}
                  </h3>
                  <p className="text-sm text-gray-700">{type.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Login Card */}
        <Card className="max-w-md mx-auto">
          <CardHeader className="text-center">
            <CardTitle>Get Started</CardTitle>
            <CardDescription>
              Sign in with Google to access your personalized AI workspace
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Button
              onClick={signInWithGoogle}
              disabled={loading}
              className="w-full"
              size="lg"
            >
              {loading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Signing in...
                </div>
              ) : (
                <div className="flex items-center">
                  <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                    <path
                      fill="currentColor"
                      d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                    />
                    <path
                      fill="currentColor"
                      d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                    />
                    <path
                      fill="currentColor"
                      d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                    />
                    <path
                      fill="currentColor"
                      d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                    />
                  </svg>
                  Continue with Google
                </div>
              )}
            </Button>

            <div className="text-center text-sm text-gray-500">
              <p>
                By signing in, you agree to our Terms of Service and Privacy
                Policy
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Features */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div>
            <Bot className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <h3 className="font-semibold mb-1">Smart Delegation</h3>
            <p className="text-sm text-gray-700">
              AI secretary analyzes tasks and assigns them to the right agents
            </p>
          </div>
          <div>
            <Users className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <h3 className="font-semibold mb-1">Dynamic Team Building</h3>
            <p className="text-sm text-gray-700">
              Hiring manager creates new specialized agents as needed
            </p>
          </div>
          <div>
            <Briefcase className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <h3 className="font-semibold mb-1">Role-Specific Workflows</h3>
            <p className="text-sm text-gray-700">
              Tailored agent capabilities for your specific use case
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
