#!/usr/bin/env python3
"""
Debug script to test the signup functionality directly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import get_session, init_db
from src.auth.signup_service import signup_user
from sqlmodel import Session

def test_signup():
    print("Testing signup functionality...")

    # Initialize database
    init_db()

    # Get a session
    gen = get_session()
    db = next(gen)

    try:
        # Test signup
        result = signup_user(
            db=db,
            full_name="Test User",
            email="test2@example.com",  # Use a different email
            password="password123"
        )
        print("Signup successful!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Signup failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the session
        next(gen, None)  # Exhaust the generator to close the session

if __name__ == "__main__":
    test_signup()