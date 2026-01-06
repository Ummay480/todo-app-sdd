#!/usr/bin/env python3
"""
Test script to call the signup service directly with raw data
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.auth.signup_service import signup_user
from src.database import get_session
from sqlmodel import Session

def test_raw_signup():
    print("Testing raw signup service...")

    # Get a session manually
    session_gen = get_session()
    db = next(session_gen)

    try:
        print("Calling signup_user directly...")
        result = signup_user(
            db=db,
            full_name="Raw Test",
            email="rawtest123@example.com",  # Use a fixed unique email
            password="password123"
        )
        print(f"Signup successful: {result}")
    except Exception as e:
        print(f"Signup failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the session
        try:
            next(session_gen)
        except StopIteration:
            pass  # Generator exhausted, which is expected

if __name__ == "__main__":
    test_raw_signup()