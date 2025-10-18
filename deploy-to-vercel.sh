#!/bin/bash

# Pokémon Card Price Finder - Quick Deploy Script

echo "🎴 Pokémon Card Price Finder - Quick Deploy to Vercel"
echo "=================================================="

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Navigate to frontend directory
cd frontend

echo "🔧 Building frontend..."
npm install
npm run build

echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Deploy your backend to Render/Railway"
echo "2. Set REACT_APP_API_URL environment variable in Vercel"
echo "3. Update CORS_ORIGINS in your backend"
echo ""
echo "📖 See DEPLOYMENT.md for detailed instructions"
