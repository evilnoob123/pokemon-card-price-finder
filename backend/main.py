from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import tempfile
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Pokémon Card Price Finder API",
    description="API for scanning Pokémon cards and fetching their market prices",
    version="1.0.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://pokemon-card-price-finder.vercel.app,https://pokemon-card-price-finder-q69lulmee-ctrl-collectibles.vercel.app,https://pokemon-card-price-finder-qj6cbqiq0-ctrl-collectibles.vercel.app").split(",")
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
async def scan_card(image: UploadFile = File(...)):
    """
    Scan a Pokémon card image and return card information with current market price.
    """
    try:
        # Validate file type
        if not image.content_type.startswith('image/'):
            return {
                "error": "File must be an image",
                "status": "error"
            }
        
        # Mock OCR - return random Pokémon name
        import random
        pokemon_names = [
            "Pikachu", "Charizard", "Blastoise", "Venusaur", "Mewtwo", 
            "Mew", "Lugia", "Ho-Oh", "Rayquaza", "Garchomp",
            "Lucario", "Gardevoir", "Salamence", "Metagross", "Tyranitar"
        ]
        card_name = random.choice(pokemon_names)
        
        # Mock price data
        import random
        price = round(random.uniform(1.50, 150.00), 2)
        
        # Generate price history (last 30 days)
        price_history = []
        for i in range(30):
            price_history.append({
                "date": f"2024-01-{i+1:02d}",
                "price": round(price + random.uniform(-10, 10), 2)
            })
        
        logger.info(f"Mock scan completed for card: {card_name}")
        
        return {
            "card_name": card_name,
            "set_name": "Base Set",
            "rarity": random.choice(["Common", "Uncommon", "Rare", "Holo Rare"]),
            "image_url": f"https://images.pokemontcg.io/base1/{random.randint(1, 102)}_hires.png",
            "card_number": str(random.randint(1, 102)),
            "hp": str(random.randint(30, 300)),
            "types": random.choice([["Lightning"], ["Fire"], ["Water"], ["Grass"], ["Psychic"], ["Fighting"], ["Darkness"], ["Metal"]]),
            "latest_market_price": price,
            "price_history": price_history
        }
        
    except Exception as e:
        logger.error(f"Error processing card scan: {str(e)}")
        return {
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
