#!/bin/bash
# Morrowind AI Framework - Server Startup Script for Unix-like systems

echo "Starting Morrowind AI Framework Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python not found. Please install Python 3.9 or later."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please ensure you have Python 3.9 or later installed."
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -d "venv/lib/python3.*/site-packages/websockets" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies."
        deactivate
        exit 1
    fi
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Make sure the script is executable
chmod +x run_server.py

# Start the server
echo "Starting server..."
python run_server.py

# Deactivate virtual environment
deactivate
