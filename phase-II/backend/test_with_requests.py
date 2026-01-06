#!/usr/bin/env python3
"""
Test script to make API requests using Python requests
"""
import requests
import json

def test_api():
    print("Testing API with Python requests...")

    url = "http://localhost:8000/api/auth/signup"

    payload = {
        "full_name": "Python Test User",
        "email": "pythontest@example.com",
        "password": "password123"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed with error: {e}")

if __name__ == "__main__":
    test_api()