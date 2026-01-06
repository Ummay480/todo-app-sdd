#!/bin/bash
# Helper script to run the Todo Backend

echo "🚀 Setting up the Todo Backend..."

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Start backend
echo "⚡ Starting backend server..."
cd src && python3 -m uvicorn main:app --reload
