#!/bin/bash

# Pokémon Card Price Finder - Development Startup Script

echo "🎴 Starting Pokémon Card Price Finder..."

# Check if we're in the right directory
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Function to start backend
start_backend() {
    echo "🚀 Starting backend server..."
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate 2>/dev/null || venv\Scripts\activate 2>/dev/null
    
    # Install dependencies
    echo "📥 Installing backend dependencies..."
    pip install -r requirements.txt
    
    # Start backend
    echo "🔥 Backend starting on http://localhost:8000"
    python app/main.py &
    BACKEND_PID=$!
    
    cd ..
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting frontend server..."
    cd frontend
    
    # Install dependencies
    echo "📥 Installing frontend dependencies..."
    npm install
    
    # Start frontend
    echo "🔥 Frontend starting on http://localhost:3000"
    npm start &
    FRONTEND_PID=$!
    
    cd ..
}

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start services
start_backend
sleep 3
start_frontend

echo "✅ Both servers are running!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
wait
