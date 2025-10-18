import pytesseract
from PIL import Image
import logging
import re
import os
from typing import Optional

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        """Initialize OCR service with Tesseract configuration."""
        # Configure Tesseract path (adjust for your system)
        # For Windows, you might need to set the path to tesseract.exe
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # For Linux/Mac, tesseract should be in PATH
        # You can also set it explicitly if needed:
        # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        
        self.configured = self._check_tesseract_installation()
        
    def _check_tesseract_installation(self) -> bool:
        """Check if Tesseract is properly installed and configured."""
        try:
            pytesseract.get_tesseract_version()
            logger.info("Tesseract OCR is properly configured")
            return True
        except Exception as e:
            logger.error(f"Tesseract OCR not found: {e}")
            logger.error("Please install Tesseract OCR:")
            logger.error("Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
            logger.error("Mac: brew install tesseract")
            logger.error("Linux: sudo apt-get install tesseract-ocr")
            return False
    
    async def extract_card_name(self, image_path: str) -> Optional[str]:
        """
        Extract Pokémon card name from image using OCR.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted card name or None if extraction fails
        """
        if not self.configured:
            logger.error("Tesseract OCR is not configured")
            return None
            
        try:
            # Load and preprocess image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance image for better OCR
            enhanced_image = self._enhance_image_for_ocr(image)
            
            # Extract text using OCR
            text = pytesseract.image_to_string(
                enhanced_image,
                config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 '
            )
            
            logger.info(f"Raw OCR text: {text}")
            
            # Extract Pokémon card name from text
            card_name = self._extract_pokemon_name(text)
            
            return card_name
            
        except Exception as e:
            logger.error(f"Error in OCR extraction: {e}")
            return None
    
    def _enhance_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """
        Enhance image for better OCR accuracy.
        
        Args:
            image: PIL Image object
            
        Returns:
            Enhanced PIL Image object
        """
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # You can add more image enhancement here:
            # - Resize image if too small
            # - Apply filters for better contrast
            # - Crop to focus on text areas
            
            return image
            
        except Exception as e:
            logger.error(f"Error enhancing image: {e}")
            return image
    
    def _extract_pokemon_name(self, text: str) -> Optional[str]:
        """
        Extract Pokémon card name from OCR text.
        
        Args:
            text: Raw OCR text
            
        Returns:
            Extracted Pokémon name or None
        """
        try:
            # Clean up the text
            text = text.strip()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Common Pokémon name patterns
            pokemon_patterns = [
                r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # Capitalized words
                r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+\d+$',  # Name with number
            ]
            
            # Look for potential Pokémon names in the text
            for line in lines:
                # Skip very short or very long lines
                if len(line) < 3 or len(line) > 50:
                    continue
                
                # Skip lines that look like numbers only
                if line.isdigit():
                    continue
                
                # Skip common non-name words
                skip_words = ['pokemon', 'card', 'trading', 'game', 'set', 'series']
                if any(word in line.lower() for word in skip_words):
                    continue
                
                # Check if line matches Pokémon name patterns
                for pattern in pokemon_patterns:
                    if re.match(pattern, line):
                        logger.info(f"Found potential Pokémon name: {line}")
                        return line
            
            # If no pattern matches, try to find the longest meaningful line
            meaningful_lines = [line for line in lines if len(line) > 5 and not line.isdigit()]
            if meaningful_lines:
                # Return the longest meaningful line
                longest_line = max(meaningful_lines, key=len)
                logger.info(f"Using longest meaningful line as card name: {longest_line}")
                return longest_line
            
            logger.warning("No Pokémon name found in OCR text")
            return None
            
        except Exception as e:
            logger.error(f"Error extracting Pokémon name: {e}")
            return None
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract all text from image (for debugging purposes).
        
        Args:
            image_path: Path to the image file
            
        Returns:
            All extracted text
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return ""
