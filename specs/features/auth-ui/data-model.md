# Data Model: Authentication

## Entities

### User
Extracted from Better Auth schema:
- **id**: `string` (UUID/KSUID) - Primary Key
- **email**: `string` - Unique, validated
- **name**: `string`
- **emailVerified**: `boolean`
- **image**: `string` (Optional)
- **createdAt**: `Date`
- **updatedAt**: `Date`

### Session
- **id**: `string`
- **userId**: `string` (FK -> User)
- **token**: `string` (opaque or JWT depending on config)
- **expiresAt**: `Date`
- **ipAddress**: `string`
- **userAgent**: `string`

## Validations
- **Email**: Must match standard email regex.
- **Password**: Minimum 8 characters, at least 1 number or special character (Frontend check before Better Auth call).
- **Name**: Required (Minimum 2 characters).
