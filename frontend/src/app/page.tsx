import Dashboard from "@/components/Dashboard";
import Header from "@/components/Header";
import ProtectedRoute from "@/components/auth/ProtectedRoute";

export default function Home() {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main>
          <Dashboard />
        </main>
      </div>
    </ProtectedRoute>
  );
}
