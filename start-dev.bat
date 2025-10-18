@echo off
REM Pokémon Card Price Finder - Development Startup Script for Windows

echo 🎴 Starting Pokémon Card Price Finder...

REM Check if we're in the right directory
if not exist "frontend" (
    echo ❌ Please run this script from the project root directory
    pause
    exit /b 1
)
if not exist "backend" (
    echo ❌ Please run this script from the project root directory
    pause
    exit /b 1
)

echo 🚀 Starting backend server...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing backend dependencies...
pip install -r requirements.txt

REM Start backend
echo 🔥 Backend starting on http://localhost:8000
start "Backend Server" cmd /k "python app/main.py"

cd ..

echo 🎨 Starting frontend server...
cd frontend

REM Install dependencies
echo 📥 Installing frontend dependencies...
npm install

REM Start frontend
echo 🔥 Frontend starting on http://localhost:3000
start "Frontend Server" cmd /k "npm start"

cd ..

echo ✅ Both servers are starting!
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul
