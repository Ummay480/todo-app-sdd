from sqlmodel import select
from src.models.user import User
from src.auth.password_service import PasswordService
from src.auth.jwt_service import JWTService
from sqlmodel import Session
from sqlalchemy import select as sqlalchemy_select


def signup_user(db: Session, full_name: str, email: str, password: str):
    # Check if user already exists
    result = db.execute(sqlalchemy_select(User).where(User.email == email))
    existing_user = result.first()
    if existing_user:
        # Do NOT leak info
        raise ValueError("Signup failed")

    # Hash the password
    hashed = PasswordService.hash_password(password)

    # Create new user
    user = User(
        name=full_name,
        email=email,
        hashed_password=hashed
    )

    # Add user to database
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create JWT token
    token = JWTService.create_token({
        "user_id": str(user.id),
        "email": user.email,
    })

    return {
        "access_token": token,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name
        }
    }
