import { createAuthClient } from "better-auth/client";
import { jwt } from "better-auth/plugins";

// Create a client-only auth instance that connects to our backend API
export const auth = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || process.env.BETTER_AUTH_URL || "http://localhost:8000",
  plugins: [
    jwt(),
  ],
});

export type Session = any; // Define type as any since we're using the client
