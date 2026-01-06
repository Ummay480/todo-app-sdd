#!/usr/bin/env python3
"""
Test script to check the debug prints with TestClient
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from src.main import app

def test_with_testclient():
    print("Testing with TestClient...")

    client = TestClient(app)

    response = client.post(
        "/api/auth/signup",
        json={
            "full_name": "Debug TestClient User",
            "email": "debugtestclient@example.com",
            "password": "password123"
        }
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_with_testclient()