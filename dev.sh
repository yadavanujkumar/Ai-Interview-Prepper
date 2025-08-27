#!/bin/bash

# Development startup script for AI Interview Prepper
# This script starts both the Flask backend and Vite frontend development servers

echo "🚀 Starting AI Interview Prepper Development Environment"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "📦 Activating virtual environment and installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Install Node.js dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Create uploads directory if it doesn't exist
mkdir -p uploads

echo "🔧 Setting up environment..."
export FLASK_ENV=development
export FLASK_DEBUG=1

# Function to cleanup processes on exit
cleanup() {
    echo "🛑 Shutting down development servers..."
    kill $FLASK_PID $VITE_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Flask backend
echo "🐍 Starting Flask backend server on http://localhost:5000..."
python3 app.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 2

# Start Vite frontend development server
echo "⚡ Starting Vite frontend development server on http://localhost:3000..."
npm run dev &
VITE_PID=$!

echo ""
echo "✅ Development environment is running!"
echo "   📱 Frontend (with hot reload): http://localhost:3000"
echo "   🐍 Backend API: http://localhost:5000"
echo "   📚 API Documentation: http://localhost:5000/api/v1/health"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for processes
wait $FLASK_PID $VITE_PID