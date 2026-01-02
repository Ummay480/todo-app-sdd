# Better Auth Frontend Client Schema

## Initialization
`const authClient = createAuthClient({ baseURL: process.env.NEXT_PUBLIC_API_URL })`

## Methods

### signUp.email
- **Inputs**:
  - `email`: string
  - `password`: string
  - `name`: string
  - `image`: string (optional)
- **Response**:
  - `data`: Session object
  - `error`: BetterAuthError

### signIn.email
- **Inputs**:
  - `email`: string
  - `password`: string
- **Response**:
  - `data`: Session object
  - `error`: BetterAuthError

### signOut
- **Inputs**: none
- **Response**: void

### getSession
- **Format**: `authClient.useSession()` hook
- **Return**: `{ data: Session | null, isPending: boolean, error: any }`
