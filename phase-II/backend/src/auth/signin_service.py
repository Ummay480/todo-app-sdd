from sqlmodel import select
from src.models.user import User
from src.auth.password_service import PasswordService
from src.auth.jwt_service import JWTService
from sqlmodel import Session
from sqlalchemy import select as sqlalchemy_select


def signin_user(db: Session, email: str, password: str):
    # Find user by email
    result = db.execute(sqlalchemy_select(User).where(User.email == email))
    user_row = result.first()
    if not user_row:
        raise ValueError("Signin failed")

    user = user_row._asdict() if hasattr(user_row, '_asdict') else user_row
    if hasattr(user, '__dict__'):
        user = user
    else:
        user = user_row[0] if user_row else None

    # Handle the case where result.first() returns a tuple
    if user_row:
        user = user_row[0] if hasattr(user_row, '__iter__') and not isinstance(user_row, dict) and not hasattr(user_row, '_asdict') else user_row
    else:
        user = None

    # Get the actual user object - it should be the first element if it's a tuple/row
    if user_row:
        # If it's a Row object from SQLAlchemy, get the first actual object
        user_obj = user_row[0] if hasattr(user_row, '__getitem__') and len(user_row) > 0 else user_row
    else:
        raise ValueError("Signin failed")

    # Verify password
    if not PasswordService.verify_password(password, user_obj.hashed_password):
        raise ValueError("Signin failed")

    # Create JWT token
    token = JWTService.create_token({
        "user_id": str(user_obj.id),
        "email": user_obj.email,
    })

    return {
        "access_token": token,
        "user": {
            "id": str(user_obj.id),
            "email": user_obj.email,
            "name": user_obj.name
        }
    }
