import jwt
import time
import os
from typing import Dict, Any

JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_THIS_TO_ENV_SECRET")  # Use environment variable
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_IN = 60 * 60  # 1 hour


class JWTService:
    @staticmethod
    def create_token(payload: Dict[str, Any]) -> str:
        now = int(time.time())
        token_payload = {
            **payload,
            "iat": now,
            "exp": now + JWT_EXPIRES_IN,
        }

        return jwt.encode(
            token_payload,
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
