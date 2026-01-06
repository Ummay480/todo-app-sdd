# API Contract: Authentication (Better Auth)

## Base Path
`/api/auth` (Next.js Side)

## Endpoints

### POST /signup
Creates a new user account.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "name": "John Doe"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe"
    }
  }
  ```

### POST /login
Authenticates an existing user.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "user": { "..." },
    "session": { "..." }
  }
  ```

### GET /jwks
Exposes public keys for JWT verification (used by FastAPI).
- **Response (200 OK)**:
  ```json
  {
    "keys": [
      {
        "kty": "OKP",
        "use": "sig",
        "crv": "Ed25519",
        "kid": "...",
        "x": "..."
      }
    ]
  }
  ```

## JWT Claims (Ed25519)
- `sub`: User ID
- `email`: User Email
- `exp`: Expiration Unix Timestamp
- `iat`: Issued-at Unix Timestamp
