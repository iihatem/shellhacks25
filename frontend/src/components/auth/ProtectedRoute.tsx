"use client";

import { useAuth } from "@/contexts/AuthContext";
import LoginPage from "./LoginPage";
import UserTypeSelection from "./UserTypeSelection";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { user, userProfile, loading } = useAuth();

  // Show loading spinner while checking auth state
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Show login page if user is not authenticated
  if (!user) {
    return <LoginPage />;
  }

  // Show user type selection if user hasn't selected their role yet
  if (!userProfile?.userType) {
    return <UserTypeSelection />;
  }

  // User is authenticated and has selected their role, show the protected content
  return <>{children}</>;
}
