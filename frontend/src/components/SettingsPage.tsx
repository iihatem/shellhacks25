"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar } from "@/components/ui/avatar";
import { useAuth } from "@/contexts/AuthContext";
import { useTheme } from "@/contexts/ThemeContext";
import {
  User,
  Mail,
  Shield,
  Bell,
  Palette,
  Globe,
  Moon,
  Sun,
  Monitor,
} from "lucide-react";

export default function SettingsPage() {
  const { user, userProfile, logout } = useAuth();
  const { theme, setTheme } = useTheme();

  // Debug: Log theme changes
  console.log("Current theme:", theme);
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    tasks: true,
    agents: false,
  });

  const getUserTypeLabel = (userType?: string) => {
    const types: Record<string, string> = {
      ceo: "CEO / Executive",
      student: "Student",
      tutor: "Tutor / Teacher",
      designer: "Designer",
      content_creator: "Content Creator",
    };
    return types[userType || ""] || "User";
  };

  const getUserTypeBadgeColor = (userType?: string) => {
    const colors: Record<string, string> = {
      ceo: "bg-blue-600 text-white",
      student: "bg-green-600 text-white",
      tutor: "bg-purple-600 text-white",
      designer: "bg-pink-600 text-white",
      content_creator: "bg-orange-600 text-white",
    };
    return colors[userType || ""] || "bg-gray-600 text-white";
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">Settings</h1>
        <p className="text-muted-foreground">
          Manage your account settings and preferences
        </p>
      </div>

      {/* Profile Section */}
      <Card className="bg-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-900 dark:text-white">
            <User className="w-5 h-5" />
            Profile Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-4">
            {userProfile?.photoURL || user?.photoURL ? (
              <img
                src={userProfile?.photoURL || user?.photoURL || ""}
                alt={userProfile?.displayName || user?.displayName || "User"}
                className="w-16 h-16 rounded-full object-cover"
              />
            ) : (
              <Avatar className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 text-white text-lg font-medium">
                {(userProfile?.displayName || user?.displayName || "U")
                  .split(" ")
                  .map((n) => n[0])
                  .join("")
                  .toUpperCase()}
              </Avatar>
            )}
            <div className="flex-1">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                {userProfile?.displayName || user?.displayName || "User"}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 flex items-center gap-2">
                <Mail className="w-4 h-4" />
                {userProfile?.email || user?.email}
              </p>
              <div className="mt-2">
                <Badge className={getUserTypeBadgeColor(userProfile?.userType)}>
                  {getUserTypeLabel(userProfile?.userType)}
                </Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Appearance Section */}
      <Card className="bg-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-900 dark:text-white">
            <Palette className="w-5 h-5" />
            Appearance
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">
              Theme
            </h4>
            <div className="grid grid-cols-3 gap-3">
              <Button
                variant={theme === "light" ? "default" : "outline"}
                onClick={() => setTheme("light")}
                className="flex items-center gap-2 justify-start"
              >
                <Sun className="w-4 h-4" />
                Light
              </Button>
              <Button
                variant={theme === "dark" ? "default" : "outline"}
                onClick={() => setTheme("dark")}
                className="flex items-center gap-2 justify-start"
              >
                <Moon className="w-4 h-4" />
                Dark
              </Button>
              <Button
                variant="outline"
                disabled
                className="flex items-center gap-2 justify-start opacity-50"
              >
                <Monitor className="w-4 h-4" />
                System
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notifications Section */}
      <Card className="bg-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-900 dark:text-white">
            <Bell className="w-5 h-5" />
            Notifications
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  Email Notifications
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Receive notifications via email
                </p>
              </div>
              <Button
                variant={notifications.email ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  setNotifications((prev) => ({ ...prev, email: !prev.email }))
                }
              >
                {notifications.email ? "On" : "Off"}
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  Push Notifications
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Receive push notifications in browser
                </p>
              </div>
              <Button
                variant={notifications.push ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  setNotifications((prev) => ({ ...prev, push: !prev.push }))
                }
              >
                {notifications.push ? "On" : "Off"}
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  Task Updates
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Get notified when tasks are completed
                </p>
              </div>
              <Button
                variant={notifications.tasks ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  setNotifications((prev) => ({ ...prev, tasks: !prev.tasks }))
                }
              >
                {notifications.tasks ? "On" : "Off"}
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  Agent Activity
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Get notified about agent status changes
                </p>
              </div>
              <Button
                variant={notifications.agents ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  setNotifications((prev) => ({
                    ...prev,
                    agents: !prev.agents,
                  }))
                }
              >
                {notifications.agents ? "On" : "Off"}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Security Section */}
      <Card className="bg-card border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-900 dark:text-white">
            <Shield className="w-5 h-5" />
            Security
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                Two-Factor Authentication
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Add an extra layer of security to your account
              </p>
            </div>
            <Button variant="outline" size="sm">
              Enable
            </Button>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                Password
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Last changed 30 days ago
              </p>
            </div>
            <Button variant="outline" size="sm">
              Change
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Danger Zone */}
      <Card className="bg-white dark:bg-gray-800 border-red-200 dark:border-red-800">
        <CardHeader>
          <CardTitle className="text-red-600 dark:text-red-400">
            Danger Zone
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                Sign Out
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Sign out of your account on this device
              </p>
            </div>
            <Button variant="destructive" size="sm" onClick={handleLogout}>
              Sign Out
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
