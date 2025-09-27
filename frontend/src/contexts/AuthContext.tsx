"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import {
  User,
  signInWithRedirect,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  getRedirectResult,
} from "firebase/auth";
import { doc, setDoc, getDoc, serverTimestamp } from "firebase/firestore";
import { auth, googleProvider, db } from "@/lib/firebase";
import { firestoreService } from "@/services/firestoreService";

interface UserProfile {
  uid: string;
  email: string;
  displayName: string;
  photoURL?: string;
  createdAt?: any;
  lastLoginAt?: any;
  userType?: string; // ceo, student, tutor, designer, content creator, etc.
}

interface AuthContextType {
  user: User | null;
  userProfile: UserProfile | null;
  loading: boolean;
  signInWithGoogle: () => Promise<void>;
  logout: () => Promise<void>;
  updateUserType: (userType: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  // Create or update user profile in Firestore
  const createUserProfile = async (user: User) => {
    if (!user) return null;

    const userRef = doc(db, "users", user.uid);
    const userSnap = await getDoc(userRef);

    if (!userSnap.exists()) {
      // Create new user profile
      const newUserProfile: UserProfile = {
        uid: user.uid,
        email: user.email || "",
        displayName: user.displayName || "",
        photoURL: user.photoURL || undefined,
        createdAt: serverTimestamp(),
        lastLoginAt: serverTimestamp(),
      };

      await setDoc(userRef, newUserProfile);
      return newUserProfile;
    } else {
      // Update last login time
      const existingProfile = userSnap.data() as UserProfile;
      await setDoc(
        userRef,
        {
          ...existingProfile,
          lastLoginAt: serverTimestamp(),
        },
        { merge: true }
      );
      return existingProfile;
    }
  };

  // Sign in with Google
  const signInWithGoogle = async () => {
    try {
      console.log("Starting Google sign-in...");
      setLoading(true);

      // Try popup first (better for development)
      const result = await signInWithPopup(auth, googleProvider);
      console.log("Popup sign-in successful:", result.user);

      // Create user profile immediately
      const profile = await createUserProfile(result.user);
      console.log("User profile created:", profile);
      setUserProfile(profile);
    } catch (error) {
      console.error("Error signing in with Google:", error);

      // If popup fails, try redirect as fallback
      if (
        error.code === "auth/popup-blocked" ||
        error.code === "auth/popup-closed-by-user"
      ) {
        console.log("Popup failed, trying redirect...");
        try {
          await signInWithRedirect(auth, googleProvider);
        } catch (redirectError) {
          console.error("Redirect also failed:", redirectError);
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    }
  };

  // Sign out
  const logout = async () => {
    try {
      await signOut(auth);
      setUser(null);
      setUserProfile(null);
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  // Update user type
  const updateUserType = async (userType: string) => {
    if (!user) return;

    try {
      const userRef = doc(db, "users", user.uid);
      await setDoc(userRef, { userType }, { merge: true });

      // Initialize default agents for the user type
      await firestoreService.initializeDefaultAgents(user.uid, userType);

      // Update local state
      setUserProfile((prev) => (prev ? { ...prev, userType } : null));
    } catch (error) {
      console.error("Error updating user type:", error);
    }
  };

  // Handle auth state changes
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      console.log(
        "Auth state changed:",
        user ? "User logged in" : "User logged out",
        user
      );

      if (user) {
        setUser(user);
        try {
          const profile = await createUserProfile(user);
          console.log("User profile created/updated:", profile);
          setUserProfile(profile);
        } catch (error) {
          console.error("Error creating user profile:", error);
        }
      } else {
        setUser(null);
        setUserProfile(null);
      }
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  // Handle redirect result (for Google sign-in)
  useEffect(() => {
    const handleRedirectResult = async () => {
      try {
        console.log("Checking for redirect result...");
        const result = await getRedirectResult(auth);
        console.log("Redirect result:", result);

        if (result?.user) {
          console.log("User from redirect:", result.user);
          const profile = await createUserProfile(result.user);
          console.log("Profile from redirect:", profile);
          setUserProfile(profile);
        } else {
          console.log("No redirect result found");
        }
      } catch (error) {
        console.error("Error handling redirect result:", error);
      }
    };

    handleRedirectResult();
  }, []);

  const value: AuthContextType = {
    user,
    userProfile,
    loading,
    signInWithGoogle,
    logout,
    updateUserType,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
