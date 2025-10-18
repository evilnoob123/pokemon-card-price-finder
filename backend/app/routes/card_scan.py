from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import tempfile
import os
from typing import Optional
import logging

from app.services.ocr_service_simple import OCRService
from app.services.price_service import PriceService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
ocr_service = OCRService()
price_service = PriceService()

@router.post("/card/scan")
async def scan_card(image: UploadFile = File(...)):
    """
    Scan a Pokémon card image and return card information with current market price.
    
    Args:
        image: Uploaded image file
        
    Returns:
        JSON response with card information and price data
    """
    try:
        # Validate file type
        if not image.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            content = await image.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Extract card name using OCR
            logger.info("Extracting card name using OCR...")
            card_name = await ocr_service.extract_card_name(temp_file_path)
            
            if not card_name:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "Could not extract card name from image. Please ensure the card is clearly visible and try again."
                    }
                )
            
            logger.info(f"Extracted card name: {card_name}")
            
            # Fetch card information and price
            logger.info("Fetching card information and price...")
            card_data = await price_service.get_card_info(card_name)
            
            if not card_data:
                return JSONResponse(
                    status_code=404,
                    content={
                        "error": f"No information found for card: {card_name}",
                        "card_name": card_name
                    }
                )
            
            # Add the extracted card name to the response
            card_data["card_name"] = card_name
            
            logger.info(f"Successfully processed card: {card_name}")
            
            return JSONResponse(content=card_data)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing card scan: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/card/search/{card_name}")
async def search_card(card_name: str):
    """
    Search for a Pokémon card by name and return its information.
    
    Args:
        card_name: Name of the Pokémon card to search for
        
    Returns:
        JSON response with card information
    """
    try:
        card_data = await price_service.get_card_info(card_name)
        
        if not card_data:
            raise HTTPException(
                status_code=404,
                detail=f"No information found for card: {card_name}"
            )
        
        card_data["card_name"] = card_name
        return JSONResponse(content=card_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching for card: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
