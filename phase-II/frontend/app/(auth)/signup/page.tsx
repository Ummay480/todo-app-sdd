import { SignupForm } from "@/components/auth/SignupForm";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sign Up | Todo App",
  description: "Create a new account to start tracking your tasks",
};

/**
 * Signup Page
 * Reference: @specs/ui/pages.md
 */
export default function SignupPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12">
      <SignupForm />
    </main>
  );
}
