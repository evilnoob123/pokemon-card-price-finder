#!/usr/bin/env python3
"""
Test script to verify PSA Images API response format.
"""

import requests
import json
import ssl
import aiohttp
import asyncio

async def test_psa_images_api():
    """Test the PSA Images API with the provided certificate number and token."""
    
    # Test certificate number
    cert_number = "27790785"
    
    # PSA API Token (provided by user)
    psa_token = "F8eGWk5nCAKONQ4hKNvK6I6QXuBWQH4IQHWS0cOxsU0dGrgO7HlE2MxEQu8INI3BZJscCAVB3ukrTU1EUOZGSdntk8zae9sQHEsF0OsqYs11fZC1tUzyibskcPETsgyIgo4MoEa8qYe40qPeepyZqvNCT6f2VM1EKvo-DZOVr946iIM0BF693CsiNsm8O86ANJlUXBeN453b1LTTe-7h43oO5C8SbNAxBGm2dWQr4YYXrK9J9vUIyZIQ6Wm3pRVmNk2T8r9O7XWZru6AUlo6qlRf9lv6u9knt27PPzfV8X2GHckp"
    
    # PSA Images API URL
    psa_images_url = f"https://api.psacard.com/publicapi/cert/GetImagesByCertNumber/{cert_number}"
    
    # Headers
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {psa_token}"
    }
    
    print(f"Testing PSA Images API...")
    print(f"URL: {psa_images_url}")
    print(f"Headers: {headers}")
    print("-" * 50)
    
    try:
        # Use aiohttp with SSL context disabled
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(psa_images_url, headers=headers, timeout=10) as response:
                print(f"Response Status Code: {response.status}")
                print(f"Response Headers: {dict(response.headers)}")
                
                if response.status == 200:
                    try:
                        data = await response.json()
                        print(f"Response JSON: {json.dumps(data, indent=2)}")
                        
                        # Try to extract image URL
                        image_url = None
                        if isinstance(data, list) and len(data) > 0:
                            first_image = data[0]
                            if isinstance(first_image, dict) and 'url' in first_image:
                                image_url = first_image['url']
                            elif isinstance(first_image, str):
                                image_url = first_image
                        elif isinstance(data, dict):
                            for field in ['url', 'imageUrl', 'image_url', 'frontImage', 'front_image']:
                                if field in data and data[field]:
                                    image_url = data[field]
                                    break
                        
                        print(f"Extracted Image URL: {image_url}")
                        
                    except json.JSONDecodeError:
                        text = await response.text()
                        print(f"Response Text (not JSON): {text}")
                else:
                    text = await response.text()
                    print(f"Response Text: {text}")
        
        return response.status == 200
        
    except Exception as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_psa_images_api())
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
