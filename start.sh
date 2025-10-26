#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Python
if ! command_exists python3; then
    echo "Python 3 is not installed. Please install it from https://python.org"
    exit 1
fi

# Check for Node.js
if ! command_exists node; then
    echo "Node.js is not installed. Please install it from https://nodejs.org"
    exit 1
fi

# Check for npm
if ! command_exists npm; then
    echo "npm is not installed. Please install Node.js from https://nodejs.org"
    exit 1
fi

echo "Starting Pocket Budget Hero..."

# Create Python virtual environment if it doesn't exist
if [ ! -d "backend/.venv" ]; then
    echo "Creating Python virtual environment..."
    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    pip install fastapi uvicorn sqlmodel python-dotenv
    cd ..
else
    cd backend
    source .venv/bin/activate
    cd ..
fi

# Install frontend dependencies if node_modules doesn't exist
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start backend server in the background
echo "Starting backend server..."
cd backend
source .venv/bin/activate
python3 -m uvicorn main:app --reload --port 8000 &
cd ..

# Start frontend development server
echo "Starting frontend development server..."
cd frontend
npm run dev
