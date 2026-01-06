import { NextResponse, type NextRequest } from "next/server";

export default async function middleware(request: NextRequest) {
	// For this frontend app, we'll allow all routes to load
	// Authentication will be handled on the client-side
	// since the auth API is on the backend server
	return NextResponse.next();
}

export const config = {
	matcher: [
        "/",
        "/login",
        "/signup",
        "/dashboard/:path*",
        "/tasks/:path*",
    ],
};
