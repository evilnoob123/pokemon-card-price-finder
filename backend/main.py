from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Pokémon Card Price Finder API",
    description="API for scanning Pokémon cards and fetching their market prices",
    version="1.0.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Pokémon Card Price Finder API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/card/scan")
async def scan_card():
    """Mock card scan endpoint for testing"""
    return {
        "card_name": "Pikachu",
        "set_name": "Base Set",
        "rarity": "Common",
        "image_url": "https://images.pokemontcg.io/base1/58_hires.png",
        "card_number": "58",
        "hp": "40",
        "types": ["Lightning"],
        "latest_market_price": 2.50,
        "price_history": []
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
