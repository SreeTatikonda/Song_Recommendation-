#!/bin/bash

# MoodTune Quick Start Script
# This script helps you set up and run the MoodTune system

echo "======================================"
echo "  MoodTune - Setup & Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 is installed"
echo ""

# Check if requirements are installed
echo "Checking dependencies..."
if pip3 show flask &> /dev/null; then
    echo "✓ Dependencies are already installed"
else
    echo "Installing dependencies..."
    pip3 install -r requirements.txt --break-system-packages
    if [ $? -eq 0 ]; then
        echo "✓ Dependencies installed successfully"
    else
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "======================================"
echo "  Choose an option:"
echo "======================================"
echo "1. Test Backend (mood detection)"
echo "2. Start API Server"
echo "3. Open Frontend (browser)"
echo "4. Run Everything"
echo "5. Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Running backend tests..."
        python3 backend.py
        ;;
    2)
        echo ""
        echo "Starting API server on http://localhost:5000"
        echo "Press Ctrl+C to stop the server"
        echo ""
        python3 api_server.py
        ;;
    3)
        echo ""
        echo "Opening frontend in browser..."
        if command -v open &> /dev/null; then
            open index.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open index.html
        elif command -v start &> /dev/null; then
            start index.html
        else
            echo "Please manually open index.html in your browser"
        fi
        ;;
    4)
        echo ""
        echo "Starting API server..."
        python3 api_server.py &
        API_PID=$!
        
        sleep 2
        
        echo ""
        echo "Opening frontend..."
        if command -v open &> /dev/null; then
            open index.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open index.html
        elif command -v start &> /dev/null; then
            start index.html
        else
            echo "Please manually open index.html in your browser"
        fi
        
        echo ""
        echo "✓ MoodTune is running!"
        echo "  API: http://localhost:5000"
        echo "  Frontend: index.html"
        echo ""
        echo "Press Ctrl+C to stop the server"
        
        wait $API_PID
        ;;
    5)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "  MoodTune - Session Complete"
echo "======================================"
