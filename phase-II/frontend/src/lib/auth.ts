import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { PrismaClient } from "@prisma/client";
import { prismaAdapter } from "better-auth/adapters/prisma";

const prisma = new PrismaClient();

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),
  emailAndPassword: {
    enabled: true,
  },
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  plugins: [
    jwt({
      // JWT token expiration time (default: 7 days)
      expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
    }),
  ],
});

export type Session = typeof auth.$Infer.Session;
