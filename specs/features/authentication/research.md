# Research: Better Auth JWT with Next.js 15 and FastAPI Integration

## Overview
This document outlines the research and best practices for integrating **Better Auth** (using the JWT plugin) in a **Next.js 15** (App Router) frontend and a **FastAPI** backend.

## 1. Configuring Better Auth with JWT plugin in Next.js 15

### Auth Configuration (`auth.ts`)
The JWT plugin should be added to the Better Auth configuration. It enables the generation of JWTs for external services (like our FastAPI backend) while maintaining standard cookie-based sessions for the Next.js frontend.

```typescript
// /frontend/src/lib/auth.ts
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
    // ... basic auth config (database, social providers, etc)
    plugins: [
        jwt({
            jwt: {
              // Optional: Configure algorithm (default: EdDSA)
              // issuer: "my-todo-app",
              // expirationTime: "1h",
            }
        })
    ]
});
```

### Server Components vs Client Components
- **Client Side**: Use `authClient.jwt.token()` (from `jwtClient()` plugin) to retrieve the token for API calls.
- **Server Side**: Better Auth provides methods to get the session on the server. If calling the API from a Server Component, the JWT can be generated server-side or retrieved from the user session.

## 2. Passing the JWT to a FastAPI Backend

### Frontend API Client logic
Best practice is to use an `Authorization: Bearer <token>` header in all requests to the backend.

```typescript
// /frontend/src/lib/api.ts
const getToken = async () => {
    const session = await authClient.getSession();
    // Better Auth JWT plugin usually exposes a way to get the JWT
    // or you can call the /.well-known/jwks.json equivalent or /api/auth/token
    const res = await authClient.jwt.getToken();
    return res.data?.token;
};

const apiRequest = async (path: string, options: RequestInit = {}) => {
    const token = await getToken();
    return fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
        ...options,
        headers: {
            ...options.headers,
            Authorization: `Bearer ${token}`,
        },
    });
};
```

## 3. Validating Better Auth JWT in FastAPI

### Strategy: Public Key Verification (JWKS)
Better Auth exposes its public keys via a **JWKS (JSON Web Key Set)** endpoint. This allows the FastAPI backend to verify the token's signature locally without querying the database or the authentication server for every request.

- **Standard JWKS Endpoint**: `http://frontend:3000/api/auth/jwks`
- **Algorithm**: Better Auth defaults to **EdDSA** (specifically Ed25519).

#### JWT Payload Anatomy
By default, Better Auth includes the entire user object in the JWT payload. Key claims include:
- `sub`: User ID
- `iss`: Base URL of the auth server
- `aud`: Base URL of the auth server
- `exp`: Expiration timestamp (default: 15 minutes)
- `iat`: Issued at timestamp
- `user`: Object containing `id`, `email`, `role`, etc. (customizable via `definePayload`)

#### FastAPI Verification Implementation
The backend should use the `PyJWT` or `python-jose` library. Since Better Auth often uses EdDSA (Ed25519), ensuring the correct library support is crucial (e.g., `PyJWT[crypto]`).

```python
# /backend/auth/verify.py implementation details
import httpx
from jose import jwt, jwk
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Global cache for JWKS
_jwks_cache = None

async def get_jwks():
    global _jwks_cache
    if not _jwks_cache:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://frontend:3000/api/auth/jwks")
            _jwks_cache = response.json()
    return _jwks_cache

async def get_current_user(token: str = Depends(oauth2_scheme)):
    jwks = await get_jwks()

    # 1. Get the 'kid' (Key ID) from JWT header
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")

    # 2. Find the corresponding key in JWKS
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == kid:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key.get("use"),
                "n": key.get("n"),
                "e": key.get("e"),
                "crv": key.get("crv"), # For EdDSA
                "x": key.get("x")      # For EdDSA
            }
            break

    if rsa_key:
        try:
            # 3. Decode and verify the token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["EdDSA"],
                audience="http://localhost:3000", # Must match Better Auth configuration
                issuer="http://localhost:3000"
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    raise HTTPException(status_code=401, detail="Key not found")
```

### 4. Handling Token Expiration and Refresh Logic

### Detailed Token Flow
1. **Initial Login**: User logs in on the frontend. Better Auth sets a secure HTTP-only session cookie.
2. **First API Request**: Frontend client detects no JWT in memory. It calls `authClient.jwt.getToken()`.
3. **JWT Generation**: The `getToken()` call sends the session cookie to the Next.js auth endpoint. Better Auth verifies the session and returns a signed JWT.
4. **FastAPI Request**: Frontend attaches JWT: `Authorization: Bearer <jwt>`.
5. **Validation**: FastAPI verifies the signature using the cached public key.
6. **Expiry**: JWT expires in 15 minutes.
7. **Refresh**: On the next API call, the frontend client (if using an interceptor) detects the expired token or receives a 401. It calls `getToken()` again, which gets a fresh JWT using the still-valid session cookie.
8. **Session Expiry**: When the session cookie itself expires, `getToken()` will fail, and the user must re-authenticate.

### Best Practices for JWT in Next.js 15
- **Avoid LocalStorage**: Do not store the JWT in `localStorage` to prevent XSS. Keep it in a React state variable or an in-memory variable in your API client.
- **Service-to-Service**: If the Next.js server needs to call the FastAPI backend (e.g., in a Server Action), it can use `auth.api.generateJWT` internally to create a token for the request.
- **Middleware Check**: Ensure Next.js middleware handles routing based on the *session*, not the *JWT*. The JWT is strictly for backend communication.

### Token Expiry Checklist:
- [ ] Frontend: Expire JWT in memory, do not store in `localStorage` if possible (use `sessionStorage` or just a variable).
- [ ] Backend: Check `exp` claim in JWT.
- [ ] Backend: Check `iat` (issued at) to prevent replay attacks if necessary.

## Sources
- [Better Auth JWT Plugin Documentation](https://www.better-auth.com/docs/plugins/jwt)
- [Better Auth Session Management](https://www.better-auth.com/docs/concepts/session-management)
- [Next.js 15 Middleware and Auth](https://nextjs.org/docs/app/building-your-application/routing/middleware)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
