import AppLayout from "@/components/AppLayout";
import ProtectedRoute from "@/components/auth/ProtectedRoute";

export default function Home() {
  return (
    <ProtectedRoute>
      <AppLayout />
    </ProtectedRoute>
  );
}
