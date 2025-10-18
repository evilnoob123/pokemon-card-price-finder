@echo off
REM Pokémon Card Price Finder - Quick Deploy Script for Windows

echo 🎴 Pokémon Card Price Finder - Quick Deploy to Vercel
echo ==================================================

REM Check if we're in the right directory
if not exist "frontend" (
    echo ❌ Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing Vercel CLI...
    npm install -g vercel
)

REM Navigate to frontend directory
cd frontend

echo 🔧 Building frontend...
call npm install
call npm run build

echo 🚀 Deploying to Vercel...
call vercel --prod

echo ✅ Deployment complete!
echo.
echo 📝 Next steps:
echo 1. Deploy your backend to Render/Railway
echo 2. Set REACT_APP_API_URL environment variable in Vercel
echo 3. Update CORS_ORIGINS in your backend
echo.
echo 📖 See DEPLOYMENT.md for detailed instructions
pause
