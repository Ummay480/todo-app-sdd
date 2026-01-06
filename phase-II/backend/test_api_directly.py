#!/usr/bin/env python3
"""
Test script to directly test the API endpoint function
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.auth import signup
from src.database import get_session
from pydantic import BaseModel
from typing import Generator

# Create a mock request object
class MockRequest:
    pass

class SignupPayload(BaseModel):
    full_name: str
    email: str
    password: str

def test_api_directly():
    print("Testing API endpoint directly...")

    # Get a session
    gen = get_session()
    db = next(gen)

    try:
        # Create a payload
        payload = SignupPayload(
            full_name="API Test User",
            email="apitest3@example.com",
            password="password123"
        )

        # Call the signup function directly
        result = signup(payload, db)
        print("API signup successful!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"API signup failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the session
        next(gen, None)  # Exhaust the generator to close the session

if __name__ == "__main__":
    test_api_directly()