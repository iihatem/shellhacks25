"use client";

import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Bot, LogOut, Settings, User } from "lucide-react";

export default function Header() {
  const { userProfile, logout } = useAuth();

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
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Logo and Title */}
        <div className="flex items-center space-x-3">
          <Bot className="w-8 h-8 text-blue-600" />
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              AI Agent Platform
            </h1>
            <p className="text-sm text-gray-500">Your Personal AI Workforce</p>
          </div>
        </div>

        {/* User Menu */}
        <div className="flex items-center space-x-4">
          {/* User Type Badge */}
          <Badge className={getUserTypeBadgeColor(userProfile?.userType)}>
            {getUserTypeLabel(userProfile?.userType)}
          </Badge>

          {/* User Dropdown */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                className="relative h-10 w-10 rounded-full"
              >
                <Avatar className="h-10 w-10">
                  {userProfile?.photoURL ? (
                    <img
                      src={userProfile.photoURL}
                      alt={userProfile.displayName}
                      className="h-full w-full rounded-full object-cover"
                    />
                  ) : (
                    <div className="h-full w-full rounded-full bg-gray-300 flex items-center justify-center">
                      <User className="h-5 w-5 text-gray-600" />
                    </div>
                  )}
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="end" forceMount>
              <DropdownMenuLabel className="font-normal">
                <div className="flex flex-col space-y-1">
                  <p className="text-sm font-medium leading-none">
                    {userProfile?.displayName}
                  </p>
                  <p className="text-xs leading-none text-muted-foreground">
                    {userProfile?.email}
                  </p>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="cursor-pointer">
                <Settings className="mr-2 h-4 w-4" />
                <span>Settings</span>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                className="cursor-pointer text-red-600 focus:text-red-600"
                onClick={handleLogout}
              >
                <LogOut className="mr-2 h-4 w-4" />
                <span>Log out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}
