import logging
import re
import random
from typing import Optional

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        """Initialize OCR service with fallback to mock extraction."""
        self.configured = False
        logger.info("OCR Service initialized with mock extraction")
        
    async def extract_card_name(self, image_path: str) -> Optional[str]:
        """
        Extract Pokémon card name from image using mock extraction.
        For production, this would use actual OCR.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Mock card name for demonstration
        """
        try:
            # Mock extraction - return a sample card name
            # In production, this would use pytesseract or other OCR
            mock_card_names = [
                "Pikachu",
                "Charizard", 
                "Blastoise",
                "Venusaur",
                "Mewtwo",
                "Mew",
                "Lugia",
                "Ho-Oh",
                "Rayquaza",
                "Arceus"
            ]
            
            card_name = random.choice(mock_card_names)
            
            logger.info(f"Mock OCR extracted card name: {card_name}")
            return card_name
            
        except Exception as e:
            logger.error(f"Error in mock OCR extraction: {e}")
            return "Pikachu"  # Fallback
