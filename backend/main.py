from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import tempfile
import logging
import requests
import json
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3
import aiohttp
import ssl

# Disable SSL warnings for PSA API calls
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://pokemon-card-price-finder.vercel.app,https://pokemon-card-price-finder-q69lulmee-ctrl-collectibles.vercel.app,https://pokemon-card-price-finder-qj6cbqiq0-ctrl-collectibles.vercel.app,https://pokemon-card-price-finder-bjb5st0g0-ctrl-collectibles.vercel.app,https://pokemon-card-price-finder-5x5jvg0mv-ctrl-collectibles.vercel.app,https://pokemon-card-price-finder-6v3s9rvxg-ctrl-collectibles.vercel.app").split(",")
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

@app.get("/test-psa")
async def test_psa_api():
    """
    Test endpoint to verify PSA API connectivity.
    """
    try:
        # Test with a known certificate number
        test_cert = "27790785"
        psa_token = "F8eGWk5nCAKONQ4hKNvK6I6QXuBWQH4IQHWS0cOxsU0dGrgO7HlE2MxEQu8INI3BZJscCAVB3ukrTU1EUOZGSdntk8zae9sQHEsF0OsqYs11fZC1tUzyibskcPETsgyIgo4MoEa8qYe40qPeepyZqvNCT6f2VM1EKvo-DZOVr946iIM0BF693CsiNsm8O86ANJlUXBeN453b1LTTe-7h43oO5C8SbNAxBGm2dWQr4YYXrK9J9vUIyZIQ6Wm3pRVmNk2T8r9O7XWZru6AUlo6qlRf9lv6u9knt27PPzfV8X2GHckp"
        
        psa_url = f"https://api.psacard.com/publicapi/cert/GetByCertNumber/{test_cert}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {psa_token}"
        }
        
        logger.info(f"Testing PSA API with certificate: {test_cert}")
        logger.info(f"PSA API URL: {psa_url}")
        
        # Use aiohttp with SSL context disabled for PSA API calls
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(psa_url, headers=headers, timeout=10) as response:
                return {
                    "status": "success",
                    "certificate": test_cert,
                    "url": psa_url,
                    "response_status": response.status,
                    "response_headers": dict(response.headers),
                    "response_text": await response.text()
                }
        
    except Exception as e:
        logger.error(f"PSA API test error: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.post("/api/card/scan")
async def scan_card(image: UploadFile = File(...), retry_count: str = Form("0")):
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
        
        # Parse retry count
        try:
            retry_num = int(retry_count)
        except ValueError:
            retry_num = 0
        
        # Mock OCR - return different Pokémon names based on retry count
        pokemon_names = [
            "Pikachu", "Charizard", "Blastoise", "Venusaur", "Mewtwo", 
            "Mew", "Lugia", "Ho-Oh", "Rayquaza", "Garchomp",
            "Lucario", "Gardevoir", "Salamence", "Metagross", "Tyranitar",
            "Dragonite", "Snorlax", "Machamp", "Alakazam", "Gengar",
            "Arcanine", "Lapras", "Jolteon", "Flareon", "Vaporeon"
        ]
        
        # Use retry count to get different card (cycling through the list)
        card_index = retry_num % len(pokemon_names)
        card_name = pokemon_names[card_index]
        
        # Mock price data with some variation based on retry
        import random
        base_price = 10.0 + (retry_num * 5.0)  # Slightly different base price per retry
        price = round(random.uniform(base_price, base_price + 50.00), 2)
        
        # Generate price history (last 30 days)
        price_history = []
        for i in range(30):
            price_history.append({
                "date": f"2024-01-{i+1:02d}",
                "price": round(price + random.uniform(-10, 10), 2)
            })
        
        # Different sets based on retry count
        sets = ["Base Set", "Jungle", "Fossil", "Team Rocket", "Gym Heroes", "Neo Genesis", "Neo Discovery"]
        set_name = sets[retry_num % len(sets)]
        
        # Different rarities
        rarities = ["Common", "Uncommon", "Rare", "Holo Rare", "Ultra Rare", "Secret Rare"]
        rarity = rarities[retry_num % len(rarities)]
        
        logger.info(f"Mock scan completed for card: {card_name} (retry {retry_num})")
        
        return {
            "card_name": card_name,
            "set_name": set_name,
            "rarity": rarity,
            "image_url": f"https://images.pokemontcg.io/base1/{random.randint(1, 102)}_hires.png",
            "card_number": str(random.randint(1, 102)),
            "hp": str(random.randint(30, 300)),
            "types": random.choice([["Lightning"], ["Fire"], ["Water"], ["Grass"], ["Psychic"], ["Fighting"], ["Darkness"], ["Metal"]]),
            "latest_market_price": price,
            "price_history": price_history,
            "retry_count": retry_num
        }
        
    except Exception as e:
        logger.error(f"Error processing card scan: {str(e)}")
        return {
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }

@app.post("/api/card/psa-lookup")
async def psa_lookup(request_data: dict):
    """
    Lookup PSA certificate information and scrape price history.
    """
    try:
        cert_number = request_data.get("cert_number")
        if not cert_number:
            return {
                "error": "Certificate number is required",
                "status": "error"
            }

        # PSA API Token (hardcoded as requested)
        psa_token = "F8eGWk5nCAKONQ4hKNvK6I6QXuBWQH4IQHWS0cOxsU0dGrgO7HlE2MxEQu8INI3BZJscCAVB3ukrTU1EUOZGSdntk8zae9sQHEsF0OsqYs11fZC1tUzyibskcPETsgyIgo4MoEa8qYe40qPeepyZqvNCT6f2VM1EKvo-DZOVr946iIM0BF693CsiNsm8O86ANJlUXBeN453b1LTTe-7h43oO5C8SbNAxBGm2dWQr4YYXrK9J9vUIyZIQ6Wm3pRVmNk2T8r9O7XWZru6AUlo6qlRf9lv6u9knt27PPzfV8X2GHckp"
        
        # Call PSA API with correct endpoint format
        psa_url = f"https://api.psacard.com/publicapi/cert/GetByCertNumber/{cert_number}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {psa_token}"
        }
        
        logger.info(f"Calling PSA API for certificate: {cert_number}")
        logger.info(f"PSA API URL: {psa_url}")
        logger.info(f"PSA API Headers: {headers}")
        
        try:
            # Use aiohttp with SSL context disabled for PSA API calls
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
                async with session.get(psa_url, headers=headers, timeout=10) as response:
                    logger.info(f"PSA API Response Status: {response.status}")
                    logger.info(f"PSA API Response Headers: {dict(response.headers)}")
                    
                    if response.status == 404:
                        logger.warning(f"Certificate {cert_number} not found (404)")
                        return {
                            "error": "Sorry! This certificate number cannot be found.",
                            "status": "error"
                        }
                    
                    if response.status != 200:
                        logger.error(f"PSA API returned status {response.status}")
                        return {
                            "error": "Sorry! This certificate number cannot be found.",
                            "status": "error"
                        }
                    
                    psa_data = await response.json()
                    logger.info(f"PSA API response received for certificate: {cert_number}")
                    logger.info(f"PSA API response data: {psa_data}")
            
        except Exception as e:
            logger.error(f"PSA API error for certificate {cert_number}: {str(e)}")
            return {
                "error": "Sorry! This certificate number cannot be found.",
                "status": "error"
            }
        
        # Extract card information from PSA data
        # PSA API returns data in a "PSACert" object
        psa_cert = psa_data.get("PSACert", {})
        
        card_info = {
            "card_name": psa_cert.get("Subject", "Unknown"),
            "set_name": psa_cert.get("Brand", "Unknown"),
            "psa_grade": psa_cert.get("CardGrade", "Unknown"),
            "psa_cert_number": psa_cert.get("CertNumber", cert_number),
            "certification_date": "Unknown",  # Not provided in API response
            "card_condition": psa_cert.get("GradeDescription", "Unknown"),
            "rarity": psa_cert.get("Variety", "Unknown"),
            "card_number": psa_cert.get("CardNumber", "Unknown"),
            "image_url": "",  # Not provided in API response
            "latest_market_price": 0,  # Will be updated by scraping
            "price_history": [],
            "is_psa_card": True,
            "year": psa_cert.get("Year", "Unknown"),
            "total_population": psa_cert.get("TotalPopulation", 0),
            "population_higher": psa_cert.get("PopulationHigher", 0)
        }
        
        # Get PSA card image
        try:
            image_url = await get_psa_card_image(cert_number)
            if image_url:
                card_info["image_url"] = image_url
                logger.info(f"PSA card image retrieved for certificate: {cert_number}")
            else:
                # Fallback: Try to scrape PSA page for image or use placeholder
                scraped_image_url = await scrape_psa_page_for_image(cert_number)
                if scraped_image_url:
                    card_info["image_url"] = scraped_image_url
                    logger.info(f"PSA card image scraped from page for certificate: {cert_number}")
                else:
                    # Use a placeholder image for PSA cards
                    card_info["image_url"] = "https://via.placeholder.com/300x420/1f2937/ffffff?text=PSA+Card+Image"
                    logger.info(f"Using placeholder image for certificate: {cert_number}")
        except Exception as e:
            logger.warning(f"Failed to get PSA card image for certificate {cert_number}: {str(e)}")
            # Use a placeholder image
            card_info["image_url"] = "https://via.placeholder.com/300x420/1f2937/ffffff?text=PSA+Card+Image"
        
        logger.info(f"PSA lookup completed for certificate: {cert_number}")
        
        return card_info
        
    except Exception as e:
        logger.error(f"Error in PSA lookup: {str(e)}")
        return {
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }

async def get_psa_card_image(cert_number):
    """
    Get PSA card image URL for a specific certificate number.
    """
    try:
        # PSA API Token (hardcoded as requested)
        psa_token = "F8eGWk5nCAKONQ4hKNvK6I6QXuBWQH4IQHWS0cOxsU0dGrgO7HlE2MxEQu8INI3BZJscCAVB3ukrTU1EUOZGSdntk8zae9sQHEsF0OsqYs11fZC1tUzyibskcPETsgyIgo4MoEa8qYe40qPeepyZqvNCT6f2VM1EKvo-DZOVr946iIM0BF693CsiNsm8O86ANJlUXBeN453b1LTTe-7h43oO5C8SbNAxBGm2dWQr4YYXrK9J9vUIyZIQ6Wm3pRVmNk2T8r9O7XWZru6AUlo6qlRf9lv6u9knt27PPzfV8X2GHckp"
        
        # Call PSA Images API
        psa_images_url = f"https://api.psacard.com/publicapi/cert/GetImagesByCertNumber/{cert_number}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {psa_token}"
        }
        
        logger.info(f"Calling PSA Images API for certificate: {cert_number}")
        
        # Use aiohttp with SSL context disabled
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(psa_images_url, headers=headers, timeout=10) as response:
                logger.info(f"PSA Images API Response Status: {response.status}")
                
                if response.status == 404:
                    logger.warning(f"No images found for certificate {cert_number}")
                    return None
                
                if response.status == 500:
                    logger.warning(f"PSA Images API returned 500 error for certificate {cert_number} - images may not be available")
                    return None
                
                if response.status != 200:
                    logger.error(f"PSA Images API returned status {response.status}")
                    response_text = await response.text()
                    logger.error(f"PSA Images API error response: {response_text}")
                    return None
                
                images_data = await response.json()
                logger.info(f"PSA Images API response: {images_data}")
                
                # Extract image URL from response
                if isinstance(images_data, list) and len(images_data) > 0:
                    # If it's a list, take the first image
                    first_image = images_data[0]
                    if isinstance(first_image, dict) and 'url' in first_image:
                        return first_image['url']
                    elif isinstance(first_image, str):
                        return first_image
                elif isinstance(images_data, dict):
                    # If it's a dict, look for common image URL fields
                    for field in ['url', 'imageUrl', 'image_url', 'frontImage', 'front_image']:
                        if field in images_data and images_data[field]:
                            return images_data[field]
                
                logger.warning(f"No valid image URL found in PSA Images API response for certificate {cert_number}")
                return None
                
    except Exception as e:
        logger.error(f"Error getting PSA card image for certificate {cert_number}: {str(e)}")
        return None

async def scrape_psa_page_for_image(cert_number):
    """
    Scrape PSA page to find card image URL.
    """
    try:
        logger.info(f"Scraping PSA page for image: {cert_number}")
        
        # Scrape PSA website for card image
        psa_url = f"https://www.psacard.com/cert/{cert_number}/psa"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Use aiohttp with SSL context disabled
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(psa_url, headers=headers, timeout=15) as response:
                if response.status != 200:
                    logger.error(f"PSA page returned status {response.status}")
                    return None
                
                html_content = await response.text()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for card images in various possible locations
        image_selectors = [
            'img[src*="card"]',
            'img[src*="cert"]',
            'img[class*="card"]',
            'img[class*="cert"]',
            'img[class*="image"]',
            '.card-image img',
            '.cert-image img',
            '.psa-image img',
            'img[alt*="card"]',
            'img[alt*="cert"]'
        ]
        
        for selector in image_selectors:
            img_element = soup.select_one(selector)
            if img_element and img_element.get('src'):
                img_src = img_element.get('src')
                # Convert relative URLs to absolute
                if img_src.startswith('//'):
                    img_src = 'https:' + img_src
                elif img_src.startswith('/'):
                    img_src = 'https://www.psacard.com' + img_src
                elif not img_src.startswith('http'):
                    img_src = 'https://www.psacard.com/' + img_src
                
                logger.info(f"Found PSA card image with selector {selector}: {img_src}")
                return img_src
        
        logger.warning(f"No card image found on PSA page for certificate: {cert_number}")
        return None
        
    except Exception as e:
        logger.error(f"Error scraping PSA page for image {cert_number}: {str(e)}")
        return None

async def scrape_psa_prices(cert_number, card_info):
    """
    Scrape PSA price history asynchronously.
    """
    try:
        logger.info(f"Starting price scraping for certificate: {cert_number}")
        
        # Scrape PSA website for price history
        psa_url = f"https://www.psacard.com/cert/{cert_number}/psa"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(psa_url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the sales table
        sales_table = soup.find('table', {'class': 'sales-table'}) or soup.find('table', {'id': 'sales-table'})
        
        price_history = []
        latest_price = 0
        
        if sales_table:
            rows = sales_table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    try:
                        sold_date = cells[0].get_text(strip=True)
                        sold_price_text = cells[1].get_text(strip=True)
                        grade = cells[2].get_text(strip=True)
                        seller_type = cells[3].get_text(strip=True)
                        
                        # Extract price (remove $ and commas)
                        price_str = sold_price_text.replace('$', '').replace(',', '')
                        sold_price = float(price_str)
                        
                        price_history.append({
                            "date": sold_date,
                            "price": sold_price,
                            "grade": grade,
                            "seller_type": seller_type
                        })
                        
                        if sold_price > latest_price:
                            latest_price = sold_price
                            
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Error parsing price row: {e}")
                        continue
        
        # Update card info with scraped data
        if price_history:
            card_info["latest_market_price"] = latest_price
            card_info["price_history"] = price_history
            logger.info(f"Successfully scraped {len(price_history)} price records for certificate: {cert_number}")
        else:
            # Fallback to mock data
            import random
            mock_price = round(random.uniform(50.0, 500.0), 2)
            card_info["latest_market_price"] = mock_price
            
            # Generate mock price history
            mock_history = []
            for i in range(30):
                date = datetime.now().replace(day=i+1).strftime("%Y-%m-%d")
                price = round(mock_price + random.uniform(-20, 20), 2)
                mock_history.append({
                    "date": date,
                    "price": price,
                    "grade": card_info["psa_grade"],
                    "seller_type": "Mock Data"
                })
            card_info["price_history"] = mock_history
            logger.info(f"Using mock price data for certificate: {cert_number}")
            
    except Exception as e:
        logger.error(f"Error scraping PSA prices for certificate {cert_number}: {str(e)}")
        
        # Fallback to mock data
        import random
        mock_price = round(random.uniform(50.0, 500.0), 2)
        card_info["latest_market_price"] = mock_price
        
        # Generate mock price history
        mock_history = []
        for i in range(30):
            date = datetime.now().replace(day=i+1).strftime("%Y-%m-%d")
            price = round(mock_price + random.uniform(-20, 20), 2)
            mock_history.append({
                "date": date,
                "price": price,
                "grade": card_info["psa_grade"],
                "seller_type": "Mock Data (Scraping Failed)"
            })
        card_info["price_history"] = mock_history

@app.post("/api/card/psa-price-history")
async def psa_price_history(request_data: dict):
    """
    Scrape PSA price history for a specific certificate number.
    """
    try:
        cert_number = request_data.get("cert_number")
        if not cert_number:
            return {
                "error": "Certificate number is required",
                "status": "error"
            }

        logger.info(f"Starting PSA price scraping for certificate: {cert_number}")
        
        # Scrape PSA website for price history
        psa_url = f"https://www.psacard.com/cert/{cert_number}/psa"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Use aiohttp with SSL context disabled
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(psa_url, headers=headers, timeout=15) as response:
                if response.status != 200:
                    logger.error(f"PSA website returned status {response.status}")
                    return {
                        "error": "Failed to access PSA website",
                        "status": "error"
                    }
                
                html_content = await response.text()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the sales table - look for various possible table structures
        sales_table = None
        
        # Try different selectors for the sales table
        table_selectors = [
            'table[class*="sales"]',
            'table[class*="similar"]',
            'table[class*="history"]',
            'table[id*="sales"]',
            'table[id*="similar"]',
            'table[id*="history"]',
            '.sales-table',
            '.similar-items-table',
            '.price-history-table'
        ]
        
        for selector in table_selectors:
            sales_table = soup.select_one(selector)
            if sales_table:
                logger.info(f"Found sales table with selector: {selector}")
                break
        
        price_history = []
        latest_price = 0
        
        if sales_table:
            rows = sales_table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:
                    try:
                        # Extract data from cells
                        sold_date = cells[0].get_text(strip=True)
                        sold_price_text = cells[1].get_text(strip=True)
                        grade = cells[2].get_text(strip=True) if len(cells) > 2 else "Unknown"
                        seller_type = cells[3].get_text(strip=True) if len(cells) > 3 else "Unknown"
                        
                        # Extract price (remove $ and commas)
                        price_str = sold_price_text.replace('$', '').replace(',', '').replace('USD', '').strip()
                        
                        # Try to extract numeric value
                        import re
                        price_match = re.search(r'[\d,]+\.?\d*', price_str)
                        if price_match:
                            sold_price = float(price_match.group().replace(',', ''))
                            
                            price_history.append({
                                "date": sold_date,
                                "price": sold_price,
                                "grade": grade,
                                "seller_type": seller_type
                            })
                            
                            if sold_price > latest_price:
                                latest_price = sold_price
                                
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Error parsing price row: {e}")
                        continue
        
        if price_history:
            logger.info(f"Successfully scraped {len(price_history)} price records for certificate: {cert_number}")
            return {
                "status": "success",
                "certificate": cert_number,
                "price_history": price_history,
                "latest_price": latest_price,
                "total_records": len(price_history)
            }
        else:
            logger.warning(f"No price history found for certificate: {cert_number}")
            return {
                "error": "No sales history found for this certificate. This card may not have recent sales data available.",
                "status": "error"
            }
            
    except Exception as e:
        logger.error(f"Error scraping PSA price history for certificate {cert_number}: {str(e)}")
        return {
            "error": f"Unable to retrieve sales history: {str(e)}",
            "status": "error"
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
