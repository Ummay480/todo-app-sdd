import { LoginForm } from "@/components/auth/LoginForm";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Login | Todo App",
  description: "Sign in to your account to access your tasks",
};

/**
 * Login Page
 * Reference: @specs/ui/pages.md
 */
export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12">
      <LoginForm />
    </main>
  );
}
